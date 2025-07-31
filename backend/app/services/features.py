from typing import Dict, Any

def feature_1_visualization(query: str) -> Dict[str, Any]:
    return {"message": f"1번 기능 호출, 입력 쿼리: {query}"}


def feature_2_doc_pdf(query: str) -> Dict[str, Any]:
    return {"message": f"2번 기능 호출, 입력 쿼리: {query}"}


def feature_3_map_predict(query: str) -> Dict[str, Any]:
    return {"message": f"3번 기능 호출, 입력 쿼리: {query}"}


def feature_4_general_chat(query: str) -> Dict[str, Any]:
    return {"message": f"4번 기능 호출, 입력 쿼리: {query}"}