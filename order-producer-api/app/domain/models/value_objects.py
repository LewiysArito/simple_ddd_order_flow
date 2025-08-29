from pydantic import BaseModel, Field, field_validator
from uuid import UUID, uuid4
from enum import Enum

class OrderStatus(str, Enum):
    CREATED = "CREATED"
    VALIDATED = "VALIDATED"
    PAID = "PAID"
    DELIVERING = "DELIVERING"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Money(BaseModel):
    amount: float = Field(gt=0)
    currency: str = Field(default="RUB", min_length=3, max_length=3)

    @field_validator('amount')
    @classmethod
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be greater than zero")
        return round(v, 2)

