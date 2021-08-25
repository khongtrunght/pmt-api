from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from hust.routers import mark,student

app = FastAPI()

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