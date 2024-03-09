from typing import Callable, Dict, List

import aio_pika
from hydromill.message.message import Message
from hydromill.message.pubsub import PublisherInterface

from hydromill_amqp.config import Config
from hydromill_amqp.connection import ConnectionWrapper, new_connection
from hydromill_amqp.marshaler import Marshaler


class Publisher(PublisherInterface):
    def __init__(
        self,
        config: Config,
        connection: ConnectionWrapper,
        channel: aio_pika.Channel,
        close_publisher: Callable,
    ):
        self._config = config
        self._connection = connection
        self._channel = channel
        self._publish_bindings_prepared: Dict[str, dict] = {}
        self._close_publisher = close_publisher

    async def publish(
        self,
        topic: str,
        messages: List[Message],
    ) -> None:
        """ """
        await self._prepare_publish_bindings(
            topic=topic,
            channel=self._channel,
        )

        exchange_name = self._config.exchange.generate_name(topic)
        routing_key = self._config.publish.generate_routing_key(topic)

        try:
            import elasticapm

            with elasticapm.async_capture_span(
                name=f"Publish {self._config.connection.amqp_uri.host}",
                span_type="external",
                span_subtype="amqp",
            ):
                for message in messages:
                    await self._publish_message(
                        exchange_name=exchange_name,
                        routing_key=routing_key,
                        msg=message,
                        channel=self._channel,
                    )
        except ModuleNotFoundError:
            for message in messages:
                await self._publish_message(
                    exchange_name=exchange_name,
                    routing_key=routing_key,
                    msg=message,
                    channel=self._channel,
                )

    async def close(self):
        return await self._close_publisher()

    async def _publish_message(
        self,
        exchange_name: str,
        routing_key: str,
        msg: Message,
        channel: aio_pika.Channel,
    ):
        """ """
        amqp_msg = Marshaler().marshal(msg)
        await self._exchange.publish(amqp_msg, routing_key=routing_key)
        if not self._config.publish.confirm_delivery:
            # log message published
            return
        # log wait for confirmation

    async def _prepare_publish_bindings(
        self,
        topic: str,
        channel: aio_pika.Channel,
    ) -> None:
        if (
            self._publish_bindings_prepared != {}
            and self._publish_bindings_prepared[topic] == {}
        ):
            return
        if self._config.exchange.generate_name(topic) != "":
            self._exchange = await self._config.topology_builder.exchange_declare(
                channel=channel,
                exchange_name=self._config.exchange.generate_name(topic),
                config=self._config,
            )
        self._publish_bindings_prepared[topic] = {}


async def new_publisher(
    config: Config,
) -> Publisher:
    connection: ConnectionWrapper = await new_connection(
        config.connection,
    )
    channel = await connection.amqp_connection.channel()

    async def close_publisher():
        await channel.close()
        return await connection.close()

    return Publisher(
        config=config,
        connection=connection,
        channel=channel,
        close_publisher=close_publisher,
    )


async def new_publisher_with_connection(
    config: Config,
    connection: ConnectionWrapper,
) -> Publisher:
    channel = await connection.amqp_connection.channel()

    async def close_publisher():
        await channel.close()

    return Publisher(
        config=config,
        connection=connection,
        channel=channel,
        close_publisher=close_publisher,
    )
