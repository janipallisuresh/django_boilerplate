from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.ask_engine import ask_question

app = FastAPI()

templates = Jinja2Templates(directory="app/templates")

class QueryRequest(BaseModel):
    query: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )

@app.post("/ask")
async def ask_api(req: QueryRequest):
    answer = ask_question(req.query)
    return {"response": answer}
