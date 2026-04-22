from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from api.disease import router as disease_router

app = FastAPI(
    title="AI Farmer Assistant",
    description="ফসলের রোগ নির্ণয় ও কৃষি পরামর্শ API — OpenAI Vision দিয়ে",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(disease_router)


@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(os.path.join("static", "index.html"))
