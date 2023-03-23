from qdrant_client import QdrantClient

from app.musicvec.utils.vectorize import DataToVector


class Qdrant:
    __client = None

    def __new__(cls, server, port, collection_name, *args, **kwargs):
        if cls.__client is None:
            cls.__client = QdrantClient(host=server, port=port)
        return object.__new__(cls, *args, **kwargs)

    def __init__(self, server: str, port: int, collection_name: str):
        self.__collection_name = collection_name
        self.__data_to_vector = DataToVector()

    def search_song(self, phrase):
        vector = self.__data_to_vector.prepare_input(input_string=phrase)
        song = self.__client.search(collection_name=self.__collection_name, query_vector=vector, limit=6)
        return song
