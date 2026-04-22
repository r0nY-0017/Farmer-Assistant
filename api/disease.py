import uuid
import aiofiles
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse

from services.vision_service import analyze_crop_image
from core.config import settings

router = APIRouter(prefix="/disease", tags=["Disease Detection"])

ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp", "image/jpg"}
MAX_BYTES = settings.max_file_size_mb * 1024 * 1024


@router.post("/analyze", summary="ফসলের রোগ বিশ্লেষণ করো")
async def analyze_disease(
    image: UploadFile = File(..., description="ফসলের ছবি (JPG/PNG/WEBP)"),
    crop_name: str = Form("", description="ফসলের নাম (ঐচ্ছিক) — যেমন: ধান, টমেটো"),
):
    # validate type
    if image.content_type not in ALLOWED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"শুধু JPG, PNG, WEBP ছবি গ্রহণযোগ্য। পাঠানো হয়েছে: {image.content_type}",
        )

    image_bytes = await image.read()

    # validate size
    if len(image_bytes) > MAX_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"ছবির সাইজ {settings.max_file_size_mb}MB এর বেশি হওয়া যাবে না।",
        )

    # run AI analysis
    try:
        result = await analyze_crop_image(image_bytes, crop_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI বিশ্লেষণে সমস্যা হয়েছে: {str(e)}")

    return JSONResponse(
        content={
            "success": True,
            "crop_hint": crop_name or "উল্লেখ করা হয়নি",
            "analysis": result,
        }
    )


@router.get("/health", summary="Service health check")
async def health():
    return {"status": "ok", "service": "AI Farmer Assistant — Disease Detection"}
