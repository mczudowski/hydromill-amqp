from typing import Callable, Dict, Optional

from aio_pika import ExchangeType
from pydantic import AmqpDsn, BaseModel


class AMQPConfig(BaseModel):
    client_properties: Dict[str, str]


class ConnectionConfig(BaseModel):
    amqp_uri: AmqpDsn
    amqp_config: Optional[AMQPConfig] = None


class ExchangeConfig(BaseModel):
    generate_name: Callable
    exchange_type: ExchangeType
    durable: Optional[bool] = False
    auto_deleted: Optional[bool] = False
    internal: Optional[bool] = False
    arguments: Optional[Dict[str, str]] = None


class QueueConfig(BaseModel):
    generate_name: Callable
    durable: Optional[bool] = False
    auto_delete: Optional[bool] = False
    exclusive: Optional[bool] = False
    arguments: Optional[Dict[str, str]] = None


class QueueBindConfig(BaseModel):
    generate_routing_key: Callable
    arguments: Optional[Dict[str, str]] = None


class PublishConfig(BaseModel):
    generate_routing_key: Callable
    confirm_delivery: bool


class Config(BaseModel):
    connection: ConnectionConfig
    exchange: ExchangeConfig
    publish: PublishConfig
    queue: Optional[QueueConfig] = None
    queue_bind: Optional[QueueBindConfig] = None

    # fix this
    @property
    def topology_builder(self):
        from hydromill_amqp.topology_builder import (
            TopologyBuilder,
            TopologyBuilderInterface,
        )

        topology_builder: Optional[TopologyBuilderInterface] = TopologyBuilder()
        return topology_builder


async def new_durable_pubsub_config(amqp_uri: str) -> Config:
    return Config(
        connection=ConnectionConfig(
            amqp_uri=amqp_uri,
        ),
        exchange=ExchangeConfig(
            generate_name=lambda topic: topic,
            exchange_type=ExchangeType.FANOUT,
            durable=True,
        ),
        queue_bind=QueueBindConfig(
            generate_routing_key=lambda topic: "",
        ),
        publish=PublishConfig(
            generate_routing_key=lambda topic: "",
            confirm_delivery=True,
        ),
    )
