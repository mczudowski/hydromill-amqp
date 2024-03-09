import aio_pika
from hydromill.message.message import Message

PROPERTIES = [
    "app_id",
    "content_encoding",
    "content_type",
    "correlation_id",
    "expiration",
    "message_id",
    "priority",
    "reply_to",
    "timestamp",
    "type",
    "user_id",
]
TRACEPARENT = "traceparent"


class Marshaler:
    def __init__(
        self,
        not_persistent_delivery_mode: bool = False,
    ):
        self.not_persistent_delivery_mode = not_persistent_delivery_mode

    def marshal(self, msg: Message) -> aio_pika.Message:
        """ """
        publishing = aio_pika.Message(
            body=msg.payload,
            headers=msg.metadata,
        )

        if not self.not_persistent_delivery_mode:
            publishing.delivery_mode = aio_pika.DeliveryMode.PERSISTENT

        self.postprocess_publishing(publishing)

        return publishing

    def unmarshal(self, msg: aio_pika.IncomingMessage) -> Message:
        """ """
        message = Message(
            payload=msg.body,
            metadata=msg.headers,
        )

        return message

    def postprocess_publishing(
        self,
        publishing: aio_pika.Message,
    ) -> aio_pika.Message:
        """ """
        for property in PROPERTIES:
            setattr(
                publishing,
                property,
                publishing.headers.pop(property, getattr(publishing, property)),
            )

        try:
            import elasticapm
        except ModuleNotFoundError:
            return publishing

        if TRACEPARENT not in publishing.headers:
            traceparent = elasticapm.get_trace_parent_header()
            if traceparent is not None:
                publishing.headers[TRACEPARENT] = traceparent

        return publishing
