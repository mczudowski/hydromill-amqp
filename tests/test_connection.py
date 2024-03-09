import pytest

from hydromill_amqp.config import new_durable_pubsub_config
from hydromill_amqp.connection import (
    ConnectionException,
    ConnectionWrapper,
    new_connection,
)


@pytest.fixture()
async def get_config():
    return await new_durable_pubsub_config("amqp://guest:guest@localhost:5672/")


# async def test_close_raises(mocker, get_config):
#     mocker.patch('hydromill_amqp.connection.ConnectionWrapper.close',
# side_effect=Exception())
#     connection_wrapper = ConnectionWrapper(get_config.connection)
#     with pytest.raises(ConnectionCloseException):
#         await connection_wrapper.close()


async def test_close(mocker, get_config):
    mocker.patch("hydromill_amqp.connection.ConnectionWrapper.close")  # sure?
    connection_wrapper = ConnectionWrapper(get_config.connection)
    await connection_wrapper.close()


async def test_init(get_config):
    connection_wrapper = ConnectionWrapper(get_config.connection)
    assert connection_wrapper.config == get_config.connection
    assert connection_wrapper.closed is True


async def test_connect_raises(mocker, get_config):
    mocker.patch("aio_pika.connect_robust", side_effect=Exception())
    connection_wrapper = ConnectionWrapper(get_config.connection)
    with pytest.raises(ConnectionException):
        await connection_wrapper._connect()


async def test_connect(mocker, get_config):
    mocker.patch("aio_pika.connect_robust")
    connection_wrapper = ConnectionWrapper(get_config.connection)
    await connection_wrapper._connect()


async def test_new_connection(mocker, get_config):
    mocker.patch("hydromill_amqp.connection.ConnectionWrapper._connect")
    await new_connection(get_config.connection)
