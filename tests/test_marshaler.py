import aio_pika
import pytest
from hydromill.message.message import Message

from hydromill_amqp.marshaler import Marshaler


async def test_init():
    marshaler = Marshaler(not_persistent_delivery_mode=True)
    assert marshaler.not_persistent_delivery_mode is True


async def test_marshal():
    msg = Message(metadata={}, payload=b"")
    amqp_msg = Marshaler().marshal(msg)
    assert type(amqp_msg) is aio_pika.Message


# async def test_unmarshal():
#     msg = Message(metadata={}, payload=b"")
#     imsg = aio_pika.IncomingMessage(msg)


@pytest.mark.parametrize(
    "header",
    [
        ("content_type"),
    ],
)
async def test_postprocess_publishing_properties(header):
    VALUE = "test"
    msg = aio_pika.Message(headers={header: VALUE}, body=b"")
    Marshaler().postprocess_publishing(msg)
    assert msg.content_type == VALUE
