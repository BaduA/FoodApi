from fastapi import FastAPI
import database
from fastapi.middleware.cors import CORSMiddleware
from routers import user


app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
