import urllib

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .routers import song
from .utils.qdrant import Qdrant
from .const import SERVER_QDRANT, PORT_QDRANT, COLLECTION_NAME
from .utils.scrapping_youtube import ScrappingYoutube

templates = Jinja2Templates(directory="./app/templates")
qdrant = Qdrant(server=SERVER_QDRANT, port=PORT_QDRANT, collection_name=COLLECTION_NAME)


app = FastAPI()


for router in [song]:
    app.include_router(router.router)


@app.get("/", response_class=HTMLResponse)
async def home(rq: Request):
    return templates.TemplateResponse("index.html", {"request": rq})


@app.post("/", response_class=HTMLResponse)
async def get_song(rq: Request, phrase: str = Form(...)):
    data = qdrant.search_song(phrase=phrase)
    values = data[0].payload
    track_name = values.get("track_name")
    artist_name = values.get("artist_name")
    link = ''
    if track_name or artist_name:
        video_id = ScrappingYoutube.search_song(phrase=f"{track_name} {artist_name}")
        link = f'https://www.youtube.com/watch?v={video_id}'
        embed_link = f'https://www.youtube.com/embed/{video_id}'

    return templates.TemplateResponse("index.html", {
        "request": rq,
        "age": values.get("age"),
        "artist_name": artist_name,
        "genre": values.get("genre"),
        "lyrics": values.get("lyrics"),
        "release_year": values.get("release_year"),
        "topic": values.get("topic"),
        "track_name": track_name,
        "link": link,
        "embed_link": embed_link
    })

