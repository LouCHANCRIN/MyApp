from fastapi import FastAPI
from .routers import user, auth, item
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(item.router)
my_post = [{'title': 'post 1', 'content': 'content post 1', 'id': '423112'}]


@app.get("/")
async def root():
    return {"message": "Hello World!"}
