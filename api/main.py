from fastapi import FastAPI
from api.routers import song

app = FastAPI()


for router in [song]:
    app.include_router(router.router)
