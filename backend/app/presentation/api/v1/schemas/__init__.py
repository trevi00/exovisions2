"""API Schemas"""
from .prediction_schemas import (
    PredictionRequestSchema,
    PredictionResponseSchema,
    PredictionsListResponseSchema,
    DeleteResponseSchema
)

__all__ = [
    'PredictionRequestSchema',
    'PredictionResponseSchema',
    'PredictionsListResponseSchema',
    'DeleteResponseSchema'
]
