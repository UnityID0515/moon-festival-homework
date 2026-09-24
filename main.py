from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.games.mooncake.router import router as mooncake_router

app = FastAPI(
    title="中秋小遊戲樂園 | Mid-Autumn Games Arcade",
    description="以 FastAPI + HTMX + TailwindCSS 構建的中秋主題休閒遊戲大廳",
    version="1.0.0"
)

templates = Jinja2Templates(directory="app/templates")

# Mount game sub-routers
app.include_router(mooncake_router)


@app.get("/")
def get_hub(request: Request):
    """Render the central Mid-Autumn Games Hub / Arcade Portal."""
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
def health_check():
    """Health check endpoint for deployments."""
    return {"status": "ok", "app": "Mid-Autumn Games Arcade"}
