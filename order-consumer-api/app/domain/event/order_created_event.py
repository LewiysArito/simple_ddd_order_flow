from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import List, Dict, Any
from app.domain.model.value_objects import OrderStatus

class OrderCreatedEvent(BaseModel):
    """Domain Event для Consumer при создании"""
    
    event_id: UUID
    event_type: str
    event_version: int
    occurred_on: datetime
    order_id: UUID
    user_id: UUID
    status: OrderStatus
    total_amount: float
    currency: str
    items: List[Dict[str, Any]]
    correlation_id: UUID
    causation_id: UUID

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OrderCreatedEvent':
        """Десериализация из словаря, который достаем из брокера сообщений"""
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