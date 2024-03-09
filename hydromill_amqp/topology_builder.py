import abc

from aio_pika import Channel

from hydromill_amqp.config import Config


class ExchangeDeclareException(Exception):
    pass


class QueueDeclareException(Exception):
    pass


class QueueBindException(Exception):
    pass


class TopologyBuilderInterface(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "build_topology")
            and callable(subclass.build_topology)
            and hasattr(subclass, "exchange_declare")
            and callable(subclass.exchange_declare)
        )

    @abc.abstractmethod
    def build_topology(
        self,
        channel: Channel,
        queue_name: str,
        exchange_name: str,
        config: Config,
    ):
        """ """
        raise NotImplementedError

    @abc.abstractmethod
    def exchange_declare(
        self,
        channel: Channel,
        exchange_name: str,
        config: Config,
    ):
        """ """
        raise NotImplementedError


class TopologyBuilder(TopologyBuilderInterface):
    async def build_topology(
        self,
        channel: Channel,
        queue_name: str,
        exchange_name: str,
        config: Config,
    ):
        """ """
        try:
            queue = await channel.declare_queue(
                name=queue_name,
                durable=config.queue.durable,
                exclusive=config.queue.exclusive,
                auto_delete=config.queue.auto_delete,
                arguments=config.queue.arguments,
            )
        except Exception:
            raise QueueDeclareException

        try:
            exchange = await self.exchange_declare(
                channel=channel,
                name=exchange_name,
                config=config,
            )
        except Exception:
            raise ExchangeDeclareException

        try:
            await queue.bind(
                exchange=exchange,
                routing_key=config.queue_bind.generate_routing_key(queue_name),
                arguments=config.queue_bind.arguments,
            )
        except Exception:
            raise QueueBindException

    async def exchange_declare(
        self,
        channel: Channel,
        exchange_name: str,
        config: Config,
    ):
        """ """
        return await channel.declare_exchange(
            name=exchange_name,
            type=config.exchange.exchange_type,
            durable=config.exchange.durable,
            auto_delete=config.exchange.auto_deleted,
            internal=config.exchange.internal,
            arguments=config.exchange.arguments,
        )
