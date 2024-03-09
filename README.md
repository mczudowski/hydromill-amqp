# Hydromill AMQP Pub/Sub

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/)

AMQP Pub/Sub for the Hydromill project. This project is a direct port of [Watermill AMQP Pub/Sub](https://github.com/ThreeDotsLabs/watermill-amqp).

## Usage

Example publisher:
```py
amqp_uri = "amqp://guest:guest@localhost:5672/"
amqp_config = await new_durable_pubsub_config(amqp_uri)

publisher = await new_publisher(amqp_config)

message = Message(payload=b"simple")
await publisher.publish("topic", messages=[message])
```

## References

[Watermill AMQP Pub/Sub](https://github.com/ThreeDotsLabs/watermill-amqp)

## License

[MIT License](./LICENSE)
