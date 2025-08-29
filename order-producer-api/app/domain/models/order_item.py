from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from app.domain.models.value_objects import Money

class OrderItem(BaseModel):
    product_id: UUID
    product_name: str = Field(min_length=1, max_length=100)
    price: Money
    quantity: int = Field(gt=0)

    @field_validator('quantity')
    @classmethod
    def validate_quantity(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than zero")
        return round(v, 2)

    def calculate_total(self)->Money:
        """
        Метод для подсчета денег
        """
        total_amount = self.price.amount * self.quantity
        return Money(amount=total_amount, currency=self.price.currency)