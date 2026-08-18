from fastapi import FastAPI
from app.webhook import router as webhook_router
from app.routers.reviews import router as reviews_router
from app.routers.stats import router as stats_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="AI Code Review Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(webhook_router)
app.include_router(reviews_router)
app.include_router(stats_router)

@app.get("/health")
def health():
    return {"status": "ok"}
