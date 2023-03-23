from fastapi import APIRouter
from ..utils.qdrant import Qdrant
from ..const import SERVER_QDRANT, PORT_QDRANT, COLLECTION_NAME

router = APIRouter(
    prefix="/song",
    tags=["song"],
    responses={404: {"description": "Not found"}},
)


qdrant = Qdrant(server=SERVER_QDRANT, port=PORT_QDRANT, collection_name=COLLECTION_NAME)


@router.get("", response_model=dict)
@router.get("/", response_model=dict)
def get_song_notice(phrase: str):
    data = qdrant.search_song(phrase=phrase)
    return {"song": data}

