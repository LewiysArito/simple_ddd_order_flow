
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from datetime import datetime
from typing import List, Dict, Any
from enum import Enum

from app.domain.models.order import Order
from app.domain.models.value_objects import OrderStatus
from app.domain.models.order_item import OrderItem

class OrderCreatedEvent(BaseModel):
    """Domain Event - Создан новый заказ"""
    # Метаданные события
    event_id: UUID = Field(default_factory=lambda: uuid4)
    event_type: str = Field(default="OrderCreatedEvent")
    event_version: int = Field(default=1)
    occurred_on: datetime = Field(default_factory=datetime.utcnow)

    # Данные агрегата
    order_id: UUID
    user_id: UUID
    status: OrderStatus
    total_amount: float
    currency: str
    items: List[Dict[str, Any]]

    # Метаданные для трассировки
    correlation_id: UUID  # Для отслеживания цепочки событий
    causation_id: UUID  # ID события, которое вызвало это событие
    
    @classmethod
    def from_order(cls, order: Order, correlation_id: UUID = None, causation_id: UUID = None)-> "OrderCreatedEvent":
        """Фабричный метод для создания события агрегата"""
        if correlation_id is None:
            correlation_id = uuid4()
        if causation_id is None:
            causation_id = uuid4()
        
        items_as_dicts = []
        for item in order.items:
            item_dict = {
                "product_id": str(item.product_id),
                "product_name": item.product_name,
                "price": item.price.amount,
                "currency": item.price.currency,
                "quantity": item.quantity,
                "total": item.calculate_total().amount
            }
            items_as_dicts.append(item_dict)
        
        return cls(
            order_id=order.id,
            user_id=order.user_id,
            status=order.status,
            total_amount=order.total_amount.amount,
            currency=order.total_amount.currency,
            items=items_as_dicts,
            correlation_id=correlation_id,
            causation_id=causation_id
        )

    def to_dict(self) -> Dict[str, Any]:
        """Сериализация события в словарь для брокера сообщений"""
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type,
            "event_version": self.event_version,
            "occurred_on": self.occurred_on.isoformat(),
            "order_id": str(self.order_id),
            "user_id": str(self.user_id),
            "status": self.status.value if hasattr(self.status, 'value') else self.status,
            "total_amount": self.total_amount,
            "currency": self.currency,
            "items": self.items,
            "correlation_id": str(self.correlation_id),
            "causation_id": str(self.causation_id)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrderCreatedEvent':
        """Десериализация события из словаря"""
        return cls(
            event_id=UUID(data['event_id']),
            event_type=data['event_type'],
            event_version=data['event_version'],
            occurred_on=datetime.fromisoformat(data['occurred_on']),
            order_id=UUID(data['order_id']),
            user_id=UUID(data['user_id']),
            status=OrderStatus(data['status']),
            total_amount=data['total_amount'],
            currency=data['currency'],
            items=data['items'],
            correlation_id=UUID(data['correlation_id']),
            causation_id=UUID(data['causation_id'])
        )

    def __str__(self) -> str:
        """Изменяем стандарный вывод"""
        return f"OrderCreatedEvent(order_id={self.order_id}, total={self.total_amount} {self.currency})"
    