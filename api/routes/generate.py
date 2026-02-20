# api/routes/generate.py
from fastapi import APIRouter
from pydantic import BaseModel
import uuid

from app.container import build_pipeline

router = APIRouter()


class GenerateRequest(BaseModel):
    theme: str


@router.post("/generate")
async def generate(req: GenerateRequest):
    pipeline = build_pipeline()

    job_id = str(uuid.uuid4())

    await pipeline.run(req.theme)

    return {"job_id": job_id, "status": "processing"}