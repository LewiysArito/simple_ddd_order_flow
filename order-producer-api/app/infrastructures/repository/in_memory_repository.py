from typing import Optional, List, Dict
from uuid import UUID
from app.domain.models.order import Order
from app.infrastructures.repository import OrderRepository

class InMemoryOrder(OrderRepository):
    """Репозиторий для тестирования, а также разработки"""
    
    def __init__(self):
        self._orders: Dict[UUID, Order] = {}

    async def get_by_id(self, order_id: UUID)->Optional[Order]:
        """
        Метод для получения данных по id
        """
        return self._orders.get(order_id)
    
    async def get_by_order_by_id(self, user_id: UUID)->List[Order]:
        """Получает по идентификатору пользователя все его заказы"""
        return [order for order in self._orders.values() if order.user_id == user_id]

    async def update(self, order: Order)->None:
        """Оновляем заказ по инентификатору"""

        if not self._orders.get(order.id):
            raise ValueError(f"Order with id = {order.id} not found")

        self._orders[order.id] = order
    
    async def add(self, order: Order)->None:
        """Добавляет новый заказ"""

        if self._orders.get(order.id):
            raise ValueError(f"Order with id = {order.id} already exists")

        self._orders[order.id] = order

    async def delete(self, order_id: UUID)->None:
        """Удаляет заказ по идентификатору"""
        if not self._orders.get(order_id):
            raise ValueError(f"Order with id = {order_id} not found")  
        self._orders.pop(order_id)

    async def exists(self, order_id: UUID):
        """Проверяет на существование заказ по идентификатору"""
        return bool(self._orders.get(order_id))
    
    async def clear(self) -> None:
        """Убирает все заказы до единого"""
        self._orders.clear()
    
