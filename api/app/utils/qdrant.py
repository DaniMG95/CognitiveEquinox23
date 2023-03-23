from qdrant_client import QdrantClient


class Qdrant:

    def __init__(self, server: str, port: int, collection_name: str):
        self.__client = QdrantClient(host=server, port=port)
        self.__collection_name = collection_name

    def search_song(self, phrase):
        vector = self.__vectorize(phrase=phrase)
        song = self.__client.search(collection_name=self.__collection_name, query_vector=vector, limit=1)
        return song

    @staticmethod
    def __vectorize(phrase: str) -> list[float]:
        return [0.2, 0.1, 0.9, 0.7]
