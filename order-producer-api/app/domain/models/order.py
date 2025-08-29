from uuid import UUID, uuid4
from datetime import datetime
from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator

from app.domain.models.order_item import OrderItem
from app.domain.models.value_objects import Money, OrderStatus
from app.domain.events.order_created_event import OrderCreatedEvent

class Order(BaseModel):
    """Aggregate Root для заказа"""
    id: UUID
    user_id: UUID
    items: List[OrderItem] = Field(min_length=1)
    status: OrderStatus = OrderStatus.CREATED
    total_amount: Money = Field(default_factory=lambda: Money(amount=0, currency="USD"))
    create_time: datetime = Field(default=lambda: datetime.now(datetime.utcnow))
    version: int = Field(default=0, ge=0)

    @model_validator("after")
    def validate_order(self) -> 'Order':
        if not self.item:
            raise ValueError("Order must have one at least one items")
        
        currencies = {item.price.currency for item in self.items}
        if len(currencies) > 1:
            raise ValueError('All items must have the same currency')
        
        return self
    
    def calculate_total(self)->None:
        """Рассчитываем общую сумму"""
        if not self.items:
            self.total_amount = Money(amount=0, currency="RUB")
            return
    
        total = sum(item.calculate_total().amount for item in self.items)
    
    def add_item(self, item: OrderItem)->None:
        """Добавляем товар в заказ"""
        if self.items and item.price.currency != self.items[0].price.currency:
            raise ValueError("New item mush have the same currency as existing items")
        
        self.items.append(item)
        self.calculate_total()
        self.version += 1
        
    def change_status(self, new_status=OrderStatus) -> None:
        """Изменяем статус с текущего на новый"""
        if self.status == OrderStatus.CANCELLED and new_status != OrderStatus.CANCELLED:
            raise ValueError("Cannot change status from CANCELLED")
        
        self.status = new_status
        self.version += 1
    
    def to_order_created_event(self) -> OrderCreatedEvent:
        """Создает событие из агрегата"""
        return OrderCreatedEvent.from_order(self)
    
    @classmethod
    def create_order(cls, user_id: UUID, items: List[OrderItem]) -> 'Order':
        """Фабричный метод для создания заказа"""
        order = cls(user_id=user_id, items=items)
        order.calculate_total()
        return order
