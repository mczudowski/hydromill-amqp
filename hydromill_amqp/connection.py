import aio_pika

from hydromill_amqp.config import ConnectionConfig


class ConnectionCloseException(Exception):
    pass


class ConnectionException(Exception):
    pass


class ConnectionWrapper:
    def __init__(
        self,
        config: ConnectionConfig,
    ):
        self.config = config
        self.closed = True

    async def close(self):
        # mark as closed
        # if self.closed:
        #    return
        try:
            await self.amqp_connection.close()
        except Exception:
            raise ConnectionCloseException

    async def _connect(self):
        amqp_config = self.config.amqp_config
        client_properties = (
            amqp_config.client_properties if amqp_config is not None else None
        )
        try:
            self.amqp_connection = await aio_pika.connect_robust(
                str(self.config.amqp_uri),
                client_properties=client_properties,
            )
        except Exception:
            raise ConnectionException


async def new_connection(
    config: ConnectionConfig,
):
    pubsub = ConnectionWrapper(
        config,
    )
    await pubsub._connect()
    return pubsub
