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

        if collection_info is None:
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

