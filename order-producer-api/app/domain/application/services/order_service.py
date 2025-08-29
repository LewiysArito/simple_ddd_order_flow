from uuid import UUID
from typing import List

from app.domain.models.order import Order
from app.domain.models.order_item import OrderItem 
from app.domain.models.value_objects import Money
from app.infrastructures.repository.order_repository import OrderRepository
from app.domain.events.order_created_event import OrderCreatedEvent 
from app.infrastructures.kafka.producer import KafkaEventProducer

class OrderService:
    """Application сервис для операций с заказом"""

    def __init__(
        self,
        order_repository: OrderRepository,
        event_producer: KafkaEventProducer
    ):
        self.order_repository = order_repository
        self.event_producer = event_producer
    
    async def create_order(
        self,
        user_id: UUID,
        items: List[Order]
    )->Order:
        """
        Создается новый заказ и формируется сообщение
        """
        order = Order.create_order(user_id=user_id, items=items)
        await self.order_repository.add(order)
        event = OrderCreatedEvent.from_order(order)
        
        return order
    
    async def get_order(
        self, 
        order_id:UUID
    ):
        """Получить заказ по идентификатору"""
        order = await self.order_repository.get_by_id(order_id)
        if not order:
            raise ValueError(f"Order with id = {order_id} not found") 
        
        return order
    
    async def get_user_orders(self, user_id: UUID) -> List[Order]:
        """Получает все заказы пользователя"""
        return await self.order_repository.get_by_user_id(user_id)

    async def update_order_status(
        self, 
        order_id: UUID, 
        new_status: str
    ) -> Order:
        """Обновляет статус доставки"""
        order = await self.get_order(order_id)
        order.change_status(new_status)
        
        await self.order_repository.update(order)
    
    



