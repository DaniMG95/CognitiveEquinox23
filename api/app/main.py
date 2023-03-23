from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .routers import song
from .utils.qdrant import Qdrant
from .const import SERVER_QDRANT, PORT_QDRANT, COLLECTION_NAME


templates = Jinja2Templates(directory="./api/app/templates")
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
    song = data[0].payload.get("city")
    return templates.TemplateResponse("index.html", {"request": rq, "song": song})

