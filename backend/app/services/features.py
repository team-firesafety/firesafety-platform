from typing import Dict, Any
import time

def feature_1_visualization(query: str) -> Dict[str, Any]:
    return {"message": f"1번 기능 호출, 입력 쿼리: {query}"}


def feature_2_doc_pdf(query: str) -> Dict[str, Any]:
    time.sleep(3)
    # PDF 생성
    filename = "document.pdf"
    # 다운로드 엔드포인트를 가리키는 URL 반환
    return {
        "pdf_filename": filename,
        "download_url": f"/pdf/download/{filename}",
    }


def feature_3_map_predict(query: str) -> Dict[str, Any]:
    return {"message": f"3번 기능 호출, 입력 쿼리: {query}"}


def feature_4_general_chat(query: str) -> Dict[str, Any]:
    return {"message": f"4번 기능 호출, 입력 쿼리: {query}"}