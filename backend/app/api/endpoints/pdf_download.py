from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

router = APIRouter()
PDF_DIR = os.path.join(os.getcwd(), "tmp")

@router.get("/download/{filename}")
async def download_pdf(filename: str):
    file_path = os.path.join(PDF_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF 파일을 찾을 수 없습니다.")

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="document.pdf",  # 브라우저 저장 시 기본 파일명 지정
    )