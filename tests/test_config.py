from hydromill_amqp.config import new_durable_pubsub_config


async def test_new_durable_pubsub_config():
    await new_durable_pubsub_config("amqp://guest:guest@localhost:5672/")
