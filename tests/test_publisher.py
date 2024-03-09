import pytest

from hydromill_amqp.config import new_durable_pubsub_config
from hydromill_amqp.connection import ConnectionWrapper


@pytest.fixture()
async def get_config():
    return await new_durable_pubsub_config("amqp://guest:guest@localhost:5672/")


@pytest.fixture()
async def get_connection(get_config):
    return ConnectionWrapper(get_config)


@pytest.fixture()
async def get_channel(get_connection):
    return await get_connection.amqp_connection.channel()


# async def test_init(get_config, get_connection, get_channel):
#     publisher = Publisher(get_config, get_connection, get_channel)
#     assert publisher._config == get_config
#     assert publisher._connection == get_connection

# async def test_publish(mocker, get_config):
#     mocker.patch('hydromill_amqp.publisher.new_publisher')
#     publisher = await new_publisher(get_config)

# async def test_new_publisher(mocker, get_config):
#     mocker.patch('hydromill_amqp.connection.new_connection')
#     mocker.patch('hydromill_amqp.connection.ConnectionWrapper.amqp_connection.channel')

#     publisher = await new_publisher(get_config)
