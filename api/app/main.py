import urllib

import html2text
import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .routers import song
from .utils.qdrant import Qdrant
from .const import SERVER_QDRANT, PORT_QDRANT, COLLECTION_NAME


templates = Jinja2Templates(directory="./app/templates")
qdrant = Qdrant(server=SERVER_QDRANT, port=PORT_QDRANT, collection_name=COLLECTION_NAME)


app = FastAPI()


for router in [song]:
    app.include_router(router.router)


@app.get("/", response_class=HTMLResponse)
async def home(rq: Request):
    return templates.TemplateResponse("index.html", {"request": rq})


@app.post("/", response_class=HTMLResponse)
async def get_song(rq: Request, phrase: str):
    import pdb; pdb.set_trace()
    text = None
    url = None
    if url:
        response_url = requests.get(url)
        if response_url.status_code == 200:
            text = html2text.HTML2Text(response_url.text)

    data = qdrant.search_song(phrase=text or phrase)
    values = data[0].payload
    track_name = values.get("track_name")
    artist_name = values.get("artist_name")
    link = ''
    if track_name or artist_name:
        search_query_youtube = urllib.parse.quote(f"{track_name} {artist_name}")
        link = f"https://www.youtube.com/results?search_query={search_query_youtube}"

    return templates.TemplateResponse("index.html", {
        "request": rq,
        "age": values.get("age"),
        "artist_name": artist_name,
        "genre": values.get("genre"),
        "lyrics": values.get("lyrics"),
        "release_year": values.get("release_year"),
        "topic": values.get("topic"),
        "track_name": track_name,
        "link": link
    })

