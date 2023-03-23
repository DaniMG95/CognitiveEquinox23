from fastapi import APIRouter
from ..utils.qdrant import Qdrant
from ..const import SERVER_QDRANT, PORT_QDRANT, COLLECTION_NAME

router = APIRouter(
    prefix="/song",
    tags=["song"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=dict)
def get_song_notice(phrase: str):
    qdrant = Qdrant(server=SERVER_QDRANT, port=PORT_QDRANT, collection_name=COLLECTION_NAME)
    data = qdrant.search_song(phrase=phrase)
    return {"song": data}
