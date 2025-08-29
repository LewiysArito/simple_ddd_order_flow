from abc import ABC, abstractmethod
import asyncio
from aiokafka import AIOKafkaProducer
from aiokafka.errors import KafkaTimeoutError
import json
from typing import Any, Dict
from uuid import UUID

class KafkaEventProducer(AIOKafkaProducer):
    """Асинхронный Kafka производитель"""
    
    def __init__(self, bootstrap_servers: str, topic: str):
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.producer: AIOKafkaProducer = None
    
    async def connect(self)->None:
        """Поключение к Kafka"""
        if self.producer is None:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
                value_serializer=lambda v: json.dumps().encode("utf-8")
                key_serializer=lambda v: v.encode('utf-8') if v else None,,
                acks='all',
                retries=3,
                enable_idempotence=True,
                compression_type='gzip' 
            )
            await self.producer.start()
    
    async def disconnect(self) -> None:
        """Отключение от Kafka"""
        if self.producer:
            await self.producer.stop()
            self.producer = None
            
    async def publish_event(
        self,
        event_data: Dict[str, Any],
        publish_timeout: float = 10.0 
    ):
        if self.producer is None:
            await self.connect()
        
        try:
            
            key = str(event_data.order_id) if event_data.order_id else None
            
            await self.producer.send(
                topic=self.topic,
                key=key,
                value=event_data
            )
        except KafkaTimeoutError:
            raise Exception("Kafka publish timeout - message may not be delivered")
        except Exception as e:
            raise Exception(f"Error to publish event to Kafka: {str(e)}")
        
    async def health_check(self) -> bool:
        """Проверяет работоспособность кластера"""
        try:
            if self.producer:
                await self.producer.client._wait_on_metadata(self.topic)
                return True
            return False
        except Exception:
            return False