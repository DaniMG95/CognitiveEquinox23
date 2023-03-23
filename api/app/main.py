from fastapi import FastAPI
from .routers import song

app = FastAPI()


for router in [song]:
    app.include_router(router.router)
