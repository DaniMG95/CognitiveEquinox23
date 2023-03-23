from fastapi import APIRouter
from api.utils.qdrant import Qdrant
from api.const import SERVER, PORT, COLLECTION_NAME

router = APIRouter(
    prefix="/song",
    tags=["song"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=dict)
def get_song_notice(phrase: str):
    qdrant = Qdrant(server=SERVER, port=PORT, collection_name=COLLECTION_NAME)
    data = qdrant.search_song(phrase=phrase)
    return {"song": data}
