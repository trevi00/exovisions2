"""
예측 API 엔드포인트
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from .....application.dto import PredictionRequest
from .....application.use_cases import (
    PredictExoplanetUseCase,
    GetPredictionsUseCase,
    GetPredictionByIdUseCase,
    DeletePredictionUseCase,
    DeleteAllPredictionsUseCase
)
from ...dependencies import (
    get_predict_exoplanet_use_case,
    get_get_predictions_use_case,
    get_get_prediction_by_id_use_case,
    get_delete_prediction_use_case,
    get_delete_all_predictions_use_case
)
from ..schemas import (
    PredictionRequestSchema,
    PredictionResponseSchema,
    PredictionsListResponseSchema,
    DeleteResponseSchema
)


router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post(
    "/",
    response_model=PredictionResponseSchema,
    status_code=201,
    summary="외계행성 예측",
    description="광도 곡선 데이터 또는 특징값을 사용하여 외계행성 여부를 예측합니다."
)
async def predict_exoplanet(
    request: PredictionRequestSchema,
    use_case: PredictExoplanetUseCase = Depends(get_predict_exoplanet_use_case)
):
    """
    외계행성 예측 API

    **Parameters:**
    - light_curve_data: 광도 곡선 데이터 (time, flux, flux_err)
    - features: 추출된 특징값 딕셔너리
    - save_result: 결과 저장 여부 (기본값: True)

    **Returns:**
    - 예측 결과 (is_exoplanet, classification, probabilities, confidence)
    """
    try:
        # DTO 생성
        prediction_request = PredictionRequest(
            light_curve_data=request.light_curve_data,
            features=request.features
        )

        # Use Case 실행
        result = await use_case.execute(
            request=prediction_request,
            save_result=request.save_result
        )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"예측 중 오류 발생: {str(e)}")


@router.get(
    "/",
    response_model=PredictionsListResponseSchema,
    summary="예측 목록 조회",
    description="저장된 모든 예측 결과를 조회합니다."
)
async def get_predictions(
    skip: int = Query(0, ge=0, description="건너뛸 개수"),
    limit: int = Query(100, ge=1, le=1000, description="조회할 개수"),
    is_exoplanet: Optional[bool] = Query(None, description="외계행성 여부 필터"),
    use_case: GetPredictionsUseCase = Depends(get_get_predictions_use_case)
):
    """
    예측 목록 조회 API

    **Parameters:**
    - skip: 건너뛸 개수 (페이지네이션)
    - limit: 조회할 개수 (최대 1000)
    - is_exoplanet: 외계행성 여부 필터 (True/False/None)

    **Returns:**
    - 예측 결과 리스트
    """
    try:
        predictions = await use_case.execute(
            skip=skip,
            limit=limit,
            is_exoplanet=is_exoplanet
        )

        return PredictionsListResponseSchema(
            predictions=predictions,
            total=len(predictions),
            skip=skip,
            limit=limit
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"조회 중 오류 발생: {str(e)}")


@router.get(
    "/{prediction_id}",
    response_model=PredictionResponseSchema,
    summary="예측 단건 조회",
    description="ID로 특정 예측 결과를 조회합니다."
)
async def get_prediction(
    prediction_id: str,
    use_case: GetPredictionByIdUseCase = Depends(get_get_prediction_by_id_use_case)
):
    """
    예측 단건 조회 API

    **Parameters:**
    - prediction_id: 예측 ID

    **Returns:**
    - 예측 결과
    """
    try:
        result = await use_case.execute(prediction_id)

        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"예측 ID {prediction_id}를 찾을 수 없습니다"
            )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"조회 중 오류 발생: {str(e)}")


@router.delete(
    "/{prediction_id}",
    response_model=DeleteResponseSchema,
    summary="예측 삭제",
    description="ID로 특정 예측 결과를 삭제합니다."
)
async def delete_prediction(
    prediction_id: str,
    use_case: DeletePredictionUseCase = Depends(get_delete_prediction_use_case)
):
    """
    예측 삭제 API

    **Parameters:**
    - prediction_id: 삭제할 예측 ID

    **Returns:**
    - 삭제 결과 메시지
    """
    try:
        success = await use_case.execute(prediction_id)

        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"예측 ID {prediction_id}를 찾을 수 없습니다"
            )

        return DeleteResponseSchema(
            message=f"Successfully deleted prediction {prediction_id}",
            deleted_count=1
        )

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"삭제 중 오류 발생: {str(e)}")


@router.delete(
    "/",
    response_model=DeleteResponseSchema,
    summary="전체 예측 삭제",
    description="모든 예측 결과를 삭제합니다."
)
async def delete_all_predictions(
    is_exoplanet: Optional[bool] = Query(None, description="외계행성 여부 필터"),
    use_case: DeleteAllPredictionsUseCase = Depends(get_delete_all_predictions_use_case)
):
    """
    전체 예측 삭제 API

    **Parameters:**
    - is_exoplanet: 외계행성 여부 필터 (True/False/None)
      - True: 외계행성으로 예측된 결과만 삭제
      - False: 외계행성이 아닌 결과만 삭제
      - None: 모든 결과 삭제

    **Returns:**
    - 삭제 결과 메시지 및 삭제된 개수
    """
    try:
        deleted_count = await use_case.execute(is_exoplanet=is_exoplanet)

        filter_msg = ""
        if is_exoplanet is True:
            filter_msg = " (exoplanets only)"
        elif is_exoplanet is False:
            filter_msg = " (non-exoplanets only)"

        return DeleteResponseSchema(
            message=f"Successfully deleted {deleted_count} predictions{filter_msg}",
            deleted_count=deleted_count
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"삭제 중 오류 발생: {str(e)}")
