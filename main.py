from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from hust.routers import mark,student

app = FastAPI()


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def index():
    with open("resources/frontend/index.html") as html_file:
        return HTMLResponse(html_file.read())

@app.get("/name/")
async def name():
    with open("resources/frontend/name_index.html") as html_file:
        return HTMLResponse(html_file.read())

app.include_router(mark.router)
app.include_router(student.router)