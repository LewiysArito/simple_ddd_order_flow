from abc import ABC, abstractmethod
from typing import Any, Dict

class EventProducer(ABC):
    """Абстрактный класс для производителя для брокера сообщений"""
    
    @abstractmethod
    async def publish_event(self, event: Dict[str, Any]) -> None:
        """Публикует доменное событие"""
        pass
    
    @abstractmethod
    async def close() -> None:
        """Отключаемся от брокера сообщений"""
        pass

    @abstractmethod
    async def connect() -> None:
        """Подключается к брокеру"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Проверяет работоспособность"""
        pass