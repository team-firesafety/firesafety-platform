import openai
from typing import Dict, List, Optional, Any
from sqlalchemy.orm import Session
from ..config import settings
from .visualization_metadata_service import VisualizationMetadataService
import re
import logging

logger = logging.getLogger(__name__)

class VisualizationAIQueryService:
    """OpenAI를 활용한 자연어 쿼리 생성 서비스"""
    
    def __init__(self, db: Session):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.db = db
        self.metadata_service = VisualizationMetadataService(db)
    
    def generate_sql_query(self, question: str, dataset_type: Optional[str] = None) -> Dict[str, Any]:
        """자연어 질문을 SQL 쿼리로 변환"""
        try:
            # dataset_type이 없는 경우 질문에서 자동 추론
            if not dataset_type:
                dataset_type = self._infer_dataset_type(question)
            
            # 메타데이터 컨텍스트 구성
            context = self.metadata_service.build_context_for_ai(dataset_type)
            
            # 프롬프트 구성
            prompt = self._build_prompt(question, context, dataset_type)
            
            # OpenAI API 호출
            response = self._call_openai_api(prompt)
            
            # SQL 추출 및 검증
            sql = self._extract_and_validate_sql(response)
            
            return {
                "success": True,
                "sql": sql,
                "raw_response": response,
                "context_used": context,
                "inferred_dataset_type": dataset_type
            }
            
        except Exception as e:
            logger.error(f"Error generating SQL query: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "sql": None
            }
    
    def _infer_dataset_type(self, question: str) -> Optional[str]:
        """질문에서 데이터셋 타입 자동 추론 (메타데이터 기반)"""
        try:
            # 모든 사용 가능한 데이터셋 스키마 조회
            available_schemas = self.metadata_service.get_all_schemas()
            
            if not available_schemas:
                logger.warning("No dataset schemas available")
                return None
            
            # AI를 활용한 데이터셋 매칭
            schema_info = []
            for ds_type, info in available_schemas.items():
                schema_fields = info.get('schema_definition', {}).get('fields', {})
                field_names = list(schema_fields.keys())
                
                schema_info.append(f"""
- {ds_type}: {info['description']}
  주요 필드: {', '.join(field_names[:10])}  
  예시 쿼리: {'; '.join(info.get('query_examples', [])[:2])}
""")
            
            schema_context = "\n".join(schema_info)
            
            prompt = f"""
다음 데이터셋들 중에서 사용자 질문에 가장 적합한 데이터셋을 선택하세요.

사용 가능한 데이터셋:
{schema_context}

사용자 질문: "{question}"

각 데이터셋의 설명, 필드명, 예시 쿼리를 분석하여 사용자가 원하는 정보가 어떤 데이터셋에 있을지 판단하세요.

응답 형식:
- 적합한 데이터셋이 있으면: 데이터셋 타입명만 반환 (예: seoul_fire_dispatch)
- 적합한 데이터셋이 없거나 모든 데이터셋을 검색해야 하면: 'all'
- 질문이 불명확하면: 'none'
"""
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system", 
                        "content": "당신은 데이터 분석 전문가입니다. 사용자 질문을 분석하여 가장 적합한 데이터셋을 선택하세요."
                    },
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=100
            )
            
            inferred = response.choices[0].message.content.strip().lower()
            
            # 응답 처리
            if inferred == 'all':
                logger.info("AI recommended searching all datasets")
                return None  # 모든 데이터셋 검색
            elif inferred == 'none':
                logger.warning("AI could not determine appropriate dataset")
                return None
            elif inferred in available_schemas:
                logger.info(f"AI inferred dataset_type: {inferred}")
                return inferred
            else:
                # 부분 매칭 시도
                for ds_type in available_schemas.keys():
                    if ds_type.lower() in inferred or inferred in ds_type.lower():
                        logger.info(f"AI inferred dataset_type (partial match): {ds_type}")
                        return ds_type
                
                logger.warning(f"AI returned unrecognized dataset type: {inferred}")
                return None
            
        except Exception as e:
            logger.error(f"Dataset type inference failed: {e}", exc_info=True)
            return None
    
    def _build_prompt(self, question: str, context: str, dataset_type: Optional[str] = None) -> str:
        """AI용 프롬프트 구성 (하이브리드 테이블 구조)"""
        
        # 메타데이터에서 테이블 정보 추출
        table_name = "fire_safety_data"  # 기본값
        if dataset_type and context:
            # context에서 table_name 추출 시도
            context_lines = context.split('\n')
            for line in context_lines:
                if 'table_name:' in line.lower():
                    table_name = line.split(':')[-1].strip()
                    break
        
        base_prompt = f"""
당신은 PostgreSQL 쿼리 전문가입니다.

데이터베이스 구조:
- 하이브리드 테이블 구조로 각 데이터셋별 전용 테이블 사용
- 주요 테이블들: seoul_fire_dispatch, seoul_rescue_dispatch, national_fire_status 등

사용 가능한 데이터 정보:
{context}

사용자 질문: "{question}"

요구사항:
1. PostgreSQL SELECT 쿼리만 생성하세요
2. 적절한 테이블명을 사용하세요 (context에서 table_name 확인)
3. 일반적인 PostgreSQL 컬럼 접근 방식 사용 (JSONB 연산자 불필요)
4. 숫자 비교시 적절한 형변환 사용 (::integer, ::numeric)
5. 날짜 비교시 적절한 형변환 사용 (::date, ::timestamp)
6. LIMIT {settings.MAX_QUERY_RESULTS} 기본 적용
7. 결과는 SQL 쿼리만 반환 (설명 불필요)

예시:
- SELECT * FROM seoul_fire_dispatch WHERE dth_cnt > 0 LIMIT 100
- SELECT * FROM seoul_rescue_dispatch WHERE injpsn_cnt >= 1 LIMIT 100
"""

        if dataset_type:
            base_prompt += f"\n대상 데이터셋: {dataset_type}"
        
        return base_prompt
    
    def _call_openai_api(self, prompt: str) -> str:
        """OpenAI API 호출"""
        try:
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {
                        "role": "system", 
                        "content": "당신은 PostgreSQL과 JSONB에 특화된 SQL 쿼리 전문가입니다. 사용자의 자연어 질문을 정확한 SQL 쿼리로 변환하세요."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI API call failed: {e}", exc_info=True)
            raise Exception(f"AI 서비스 호출 실패: {e}")
    
    def _extract_and_validate_sql(self, response: str) -> str:
        """응답에서 SQL 추출 및 기본 검증"""
        try:
            # SQL 코드 블록에서 추출
            sql_match = re.search(r'```sql\n(.*?)\n```', response, re.DOTALL)
            if sql_match:
                sql = sql_match.group(1).strip()
            else:
                # 코드 블록이 없는 경우 전체 응답 사용
                sql = response.strip()
            
            # 기본 검증
            sql = self._validate_sql_safety(sql)
            
            return sql
            
        except Exception as e:
            logger.error(f"SQL extraction failed: {e}")
            raise Exception(f"SQL 추출 실패: {e}")
    
    def _validate_sql_safety(self, sql: str) -> str:
        """SQL 안전성 검증"""
        sql = sql.strip()
        
        # 위험한 키워드 차단
        dangerous_keywords = [
            'DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE', 
            'TRUNCATE', 'REPLACE', 'MERGE', 'GRANT', 'REVOKE'
        ]
        
        sql_upper = sql.upper()
        for keyword in dangerous_keywords:
            if keyword in sql_upper:
                raise Exception(f"안전하지 않은 SQL 키워드 감지: {keyword}")
        
        # SELECT로 시작하는지 확인
        if not sql_upper.startswith('SELECT'):
            raise Exception("SELECT 쿼리만 허용됩니다")
        
        # 세미콜론으로 끝나는 경우 제거 (단일 쿼리만 허용)
        if sql.endswith(';'):
            sql = sql[:-1]
        
        # 다중 쿼리 방지
        if ';' in sql:
            raise Exception("다중 쿼리는 허용되지 않습니다")
        
        return sql
    
    def explain_query(self, sql: str) -> str:
        """생성된 쿼리에 대한 설명 생성"""
        try:
            prompt = f"""
다음 PostgreSQL 쿼리를 한국어로 간단히 설명해주세요:

{sql}

설명은 다음 형식으로 작성하세요:
1. 어떤 데이터를 조회하는지
2. 어떤 조건을 사용하는지  
3. 결과가 어떻게 정렬/제한되는지
"""
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=300
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Query explanation failed: {e}")
            return "쿼리 설명을 생성할 수 없습니다."
    
    def suggest_related_questions(self, original_question: str, dataset_type: Optional[str] = None) -> List[str]:
        """관련 질문 제안"""
        try:
            context = self.metadata_service.build_context_for_ai(dataset_type)
            
            prompt = f"""
사용자가 다음과 같은 질문을 했습니다: "{original_question}"

데이터 컨텍스트:
{context}

이 질문과 관련된 다른 유용한 질문 3개를 제안해주세요. 
각 질문은 한 줄로 작성하고, 번호를 붙여주세요.
"""
            
            response = self.client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            suggestions = response.choices[0].message.content.strip()
            
            # 번호가 붙은 항목들을 추출
            lines = [line.strip() for line in suggestions.split('\n') if line.strip()]
            questions = []
            
            for line in lines:
                # "1. ", "2. " 등의 번호 제거
                if re.match(r'^\d+\.', line):
                    question = re.sub(r'^\d+\.\s*', '', line)
                    questions.append(question)
            
            return questions[:3]  # 최대 3개만 반환
            
        except Exception as e:
            logger.error(f"Related questions suggestion failed: {e}")
            return []