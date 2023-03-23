from qdrant_client import QdrantClient


class Qdrant:
    __client = None

    def __new__(cls, server, port, collection_name, *args, **kwargs):
        if cls.__client is None:
            cls.__client = QdrantClient(host=server, port=port)
        return object.__new__(cls, *args, **kwargs)

    def __init__(self, server: str, port: int, collection_name: str):
        self.__collection_name = collection_name

    def search_song(self, phrase):
        vector = self.__vectorize(phrase=phrase)
        song = self.__client.search(collection_name=self.__collection_name, query_vector=vector, limit=1)
        return song

    @staticmethod
    def __vectorize(phrase: str) -> list[float]:
        return [0.2]*512
