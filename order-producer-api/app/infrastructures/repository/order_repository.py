from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from app.domain.models.order import Order

class OrderRepository(ABC):
    """
    Абстрактный репозиторий для агрегата, который с заказом
    """
    
    @abstractmethod
    async def get_by_id(self, order_id: UUID)->Optional[Order]:
        """Получает по идентификатору заказы"""
        pass

    @abstractmethod
    async def get_by_user_id(self, order_id: UUID)->List[Order]:
        """Получает по идентификатору пользователя все его заказы"""
        pass

    @abstractmethod
    async def add(self, order: Order) -> None:
        """Добавляет новый заказ"""
        pass

    @abstractmethod
    async def delete(self, order_id: Order) -> None:
        """Удаляет заказ по идентификатору"""
        pass

    @abstractmethod
    async def update(self, order: Order) -> None:
        """Обновляет заказ"""
        pass

    @abstractmethod
    async def exists(self, order_id: UUID) -> bool:
        """Проверяет на существование заказ по идентификатору"""
        pass