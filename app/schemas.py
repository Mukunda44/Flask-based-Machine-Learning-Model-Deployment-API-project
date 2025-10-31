# app/schemas.py
# Pydantic models for validating API inputs/outputs.

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, model_validator
import math


class PredictRequest(BaseModel):
    """
    Request body for /predict (single input).
    We expect exactly 4 numeric features for the Iris model.
    """
    features: List[float] = Field(..., description="Exactly 4 numbers: [sepal_length, sepal_width, petal_length, petal_width]")
    id: Optional[str] = Field(default=None, description="Optional correlation ID echoed back in the response")

    @model_validator(mode="after")
    def _check_features(self):
        # length must be exactly 4
        if len(self.features) != 4:
            raise ValueError("features must contain exactly 4 numbers")
        # all must be finite numbers
        for v in self.features:
            if not isinstance(v, (int, float)) or not math.isfinite(float(v)):
                raise ValueError("each feature must be a finite number")
        return self


class BatchItem(BaseModel):
    """
    One item in a /batch_predict request.
    """
    id: str = Field(..., description="Unique ID for this item")
    features: List[float] = Field(..., description="Exactly 4 numeric features")

    @model_validator(mode="after")
    def _check_features(self):
        if len(self.features) != 4:
            raise ValueError("each item.features must contain exactly 4 numbers")
        for v in self.features:
            if not isinstance(v, (int, float)) or not math.isfinite(float(v)):
                raise ValueError("each item.features value must be a finite number")
        return self


class BatchRequest(BaseModel):
    """
    Request body for /batch_predict (multiple inputs).
    """
    items: List[BatchItem] = Field(..., min_length=1, description="Non-empty list of BatchItem")


class PredictResponse(BaseModel):
    """
    Standard response for predictions.
    """
    id: Optional[str] = None
    label: str
    probability: float
    model_version: str


class ErrorResponse(BaseModel):
    """
    Standard error body returned by the API.
    """
    error: str
    code: int
    details: Optional[str] = None
