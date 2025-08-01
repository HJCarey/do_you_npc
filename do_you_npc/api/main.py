"""Main FastAPI application for Do You NPC API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from do_you_npc.api.routers import campaigns, personas, prompts, tags

app = FastAPI(
    title="Do You NPC API",
    description="AI-powered NPC generation system API",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(campaigns.router, prefix="/api/v1/campaigns", tags=["campaigns"])
app.include_router(personas.router, prefix="/api/v1/personas", tags=["personas"])
app.include_router(prompts.router, prefix="/api/v1/prompts", tags=["prompts"])
app.include_router(tags.router, prefix="/api/v1/tags", tags=["tags"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to Do You NPC API"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}