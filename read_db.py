from qdrant_client import QdrantClient

if __name__ == '__main__':

    client = QdrantClient()

    my_collection_info = client.get_collection("songs")
    print(my_collection_info.dict())
client.scroll()