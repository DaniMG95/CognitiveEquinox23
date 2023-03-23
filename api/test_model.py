from api.musicvec.model import Song, SongRepository
from qdrant_client import QdrantClient

song = Song(
    id=1,
    artist_name="Los Gandules",
    track_name="Cleptocupromano",
    lyrics="lkajsdf lkasdjfh lkajfdhlkj aldksfj hlaksdjfh lafdjkh asdfasd"
)

repo = SongRepository(client=QdrantClient())

repo.create_collection(force=True)
repo.add_songs([song])
