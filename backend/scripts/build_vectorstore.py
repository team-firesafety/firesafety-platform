"""
CSV → FAISS 인덱스 파일 변환 스크립트
최초 1회 실행 (CSV가 갱신되면 다시 실행)
$ python -m backend.scripts.build_vectorstore
"""
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from langchain_community.document_loaders.dataframe import DataFrameLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

# 0. 환경 & 경로 -----------------------------------------------------------
load_dotenv()                                          # OPENAI_API_KEY 로드
BASE_DIR  = Path(__file__).resolve().parents[1]
CSV_PATH  = BASE_DIR / "data" / "상세정보_화재안전기술_상세정보.csv"
INDEX_DIR = BASE_DIR / "vectorstore_FAISS"

def main() -> None:
    # 1. CSV → DataFrame ---------------------------------------------------
    df = pd.read_csv(CSV_PATH)
    df["text"] = (
            df["CONT_TTL"].fillna("") + "\n" +
            df["CONT_SUB_TTL"].fillna("") + "\n" +
            df["CONTENTS"].fillna("")
    )

    # 2. DataFrame → Documents --------------------------------------------
    docs = DataFrameLoader(df, page_content_column="text").load()

    # 3. 문서 분할 ----------------------------------------------------------
    splitter   = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200,
        separators=["\n\n", "\n", " ", ""],
    )
    split_docs = splitter.split_documents(docs)

    # 4. 임베딩 & 인덱싱 ----------------------------------------------------
    embeddings  = OpenAIEmbeddings(chunk_size=32)   # ★ 핵심: 배치 토큰수↓
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    # 5. 저장 --------------------------------------------------------------
    vectorstore.save_local(str(INDEX_DIR))
    print(f"✅  FAISS 인덱스가 {INDEX_DIR} 폴더에 저장되었습니다.")

if __name__ == "__main__":
    main()
