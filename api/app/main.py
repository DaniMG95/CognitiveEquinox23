import time
import urllib

import html2text
import requests
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .routers import song
from .utils.qdrant import Qdrant
from .const import SERVER_QDRANT, PORT_QDRANT, COLLECTION_NAME
from typing import Optional
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
async def get_song(rq: Request, phrase: Optional[str] = Form(None), url: Optional[str] = Form(None)):
    try:
        text = None
        set_url = False
        t_init_url_to_text = None
        t_fin_url_to_text = None
        t_init_search_youtube = None
        t_fin_search_youtube = None

        if url:
            try:
                t_init_url_to_text = time.time()
                response_url = requests.get(url)
                if response_url.status_code == 200:
                    text = html2text.html2text(response_url.text)
                t_fin_url_to_text = time.time()

                set_url = True
            except Exception:
                pass
        t_init_search_db = time.time()
        data = qdrant.search_song(phrase=text or phrase or url)
        t_fin_search_db = time.time()

        values = data[0].payload
        track_name = values.get("track_name")
        artist_name = values.get("artist_name")
        link = ''
        embed_link = ''
        if track_name or artist_name:
            t_init_search_youtube = time.time()
            video_id = ScrappingYoutube.search_song(phrase=f"{track_name} {artist_name}")
            link = f'https://www.youtube.com/watch?v={video_id}'
            embed_link = f'https://www.youtube.com/embed/{video_id}'
            t_fin_search_youtube = time.time()

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
            "embed_link": embed_link,
            "url_input": url if set_url else None,
            "time_url_to_text": int((t_fin_url_to_text - t_init_url_to_text) * 1000) if t_init_url_to_text and t_fin_url_to_text else None,
            "time_search_db": int((t_fin_search_db - t_init_search_db) * 1000) if t_init_search_db and t_fin_search_db else None,
            "time_search_youtube": int((t_fin_search_youtube - t_init_search_youtube) * 1000) if t_init_search_youtube and t_fin_search_youtube else None
        })
    except Exception:
        return templates.TemplateResponse("index.html", {"request": rq})

