from enum import IntEnum

class FeatureID(IntEnum):
    VISUALIZATION = 1
    DOC_PDF = 2
    MAP_PREDICT = 3
    GENERAL_CHAT = 4

FEATURE_NAME_MAP = {
    FeatureID.VISUALIZATION: "데이터 시각화",
    FeatureID.DOC_PDF: "공문서 제작",
    FeatureID.MAP_PREDICT: "화재 발생 구간 예측 지도",
    FeatureID.GENERAL_CHAT: "일반 대화",
}