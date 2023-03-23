from dataclasses import dataclass
from typing import Optional, List, Any

import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.http import models

from musicvec.utils.vectorize import DataToVector


@dataclass
class Song:
    id: int
    artist_name: str
    track_name: str
    lyrics: str
    release_year: Optional[int] = None
    genre: Optional[str] = None  # TODO: Make a enum for genres
    topic: Optional[str] = None
    age: Optional[float] = None
    _vector: Optional = None

    @property
    def vector(self):
        if self._vector is None:
            vectorizer = DataToVector()
            self._vector = list(float(f) for f in vectorizer.prepare_input(self.lyrics)[0])
        return self._vector


class SongRepository:
    COLLECTION = "songs"

    def __init__(self, client: QdrantClient):
        self.client = client

    def create_collection(self, force=False):
        try:
            collection_info = self.client.get_collection(self.COLLECTION)
        except:
            collection_info = None

        if collection_info is None or force:
            self.client.recreate_collection(
                collection_name=self.COLLECTION,
                vectors_config=models.VectorParams(size=512, distance=models.Distance.COSINE)
            )

    def add_songs(self, songs: List[Song]):
        ids = []
        payloads = []
        vectors = []

        for song in songs:
            ids.append(song.id)
            payloads.append({
                "artist_name": song.artist_name,
                "track_name": song.track_name,
                "lyrics": song.lyrics,
                "release_year": song.release_year,
                "genre": song.genre,
                "topic": song.topic,
                "age": song.age,
            })
            vectors.append(song.vector)

        self.client.upsert(
            collection_name=self.COLLECTION,
            points=models.Batch(
                ids=ids,
                payloads=payloads,
                vectors=vectors
            )
        )

    def search_songs(self, offset=0, limit=10, score_threshold=None, vector=None, **kwargs):
        filters = {
            "must": [],
            "should": [],
            "must_not": []
        }

        for key, value in kwargs.items():
            key_tokens = key.split("__")
            len_tokens = len(key_tokens)
            filter_key = key_tokens[0]
            if len_tokens == 1:
                filter = "must"
                op = "match"
            elif len_tokens == 2:
                if key_tokens[1] in ("must", "should", "must_not"):
                    filter = key_tokens[1]
                    op = "match"
                else:
                    filter = "match"
                    op = key_tokens[1]
            else:
                filter = key_tokens[1]
                op = key_tokens[2]

            if filter_key in ("id", "pk"):
                op = "has_id"

            if op == "match":
                match_obj = models.MatchValue(value=value)
            elif op == "in":
                match_obj = models.MatchAny(any=list(value))
            elif op == "like":
                match_obj = models.MatchText(text=value)
            elif op in ("gt", "lt", "gte", "lte"):
                match_obj = models.Range(**{op: value})
            elif op == "has_id":
                match_obj = models.HasIdCondition(
                    has_id=[value] if isinstance(value, int) else value
                )
            else:
                raise ValueError(f"Filter ({ key } = {value}) is now allowed")

            if op == "has_id":
                filters[filter].append(
                    match_obj
                )
            else:
                filters[filter].append(
                    models.FieldCondition(
                        key=filter_key,
                        match=match_obj
                    )
                )

        print(filters)

        filter = models.Filter(
            **filters
        )
        if vector is None:
            return self.client.scroll(
                collection_name=self.COLLECTION,
                offset=offset,
                limit=limit,
                scroll_filter=filter
            )
        return self.client.search(
            collection_name=self.COLLECTION,
            offset=offset,
            limit=limit,
            query_filter=filter,
            query_vector=vector,
            score_threshold=score_threshold
        )
