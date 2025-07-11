from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from main import HealthAgentNetwork
from markupsafe import Markup, escape
import markdown2
import uvicorn

app = FastAPI(title="Health Agent Network")
templates = Jinja2Templates(directory="templates")
network = HealthAgentNetwork()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response_html": None
    })

@app.post("/", response_class=HTMLResponse)
async def process_health_data(
    request: Request,
    user_input: str = Form(...),
    data_type: str = Form(None),
    file: UploadFile = File(None)
):
    if file:
        file_content = await file.read()
        user_input += f"\n[File uploaded: {file.filename}]"
    response_text = network.process_user_input(user_input, data_type)
    response_html = Markup(markdown2.markdown(
        escape(response_text), extras=["fenced-code-blocks", "break-on-newline"]
    ))
    agents_used = network.router.get_agents_for_input(
        data_type or network.router.classify_input(user_input)
    )
    return templates.TemplateResponse("index.html", {
        "request": request,
        "response_html": response_html,
        "agents_used": agents_used,
        "user_input": user_input
    })

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
