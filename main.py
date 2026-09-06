from fastapi import FastAPI
from routers import logistics, marketplace

app = FastAPI(title="MahaKrishi Link API")

app.include_router(logistics.router)
app.include_router(marketplace.router)