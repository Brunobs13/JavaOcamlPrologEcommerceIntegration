from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class LineItemRequest(BaseModel):
    item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class QuoteRequest(BaseModel):
    customer_id: int = Field(..., gt=0)
    lines: List[LineItemRequest]
