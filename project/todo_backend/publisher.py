import json
import logging

import nats


logger = logging.getLogger(__name__)


class NatsPublisher:
    def __init__(self, nats_url: str):
        self.url = nats_url
        self.nc = None
        self.connected = False

    async def connect(self):
        if not self.url:
            return

        try:
            self.nc = await nats.connect(self.url)
        except Exception:
            logger.exception("Failed to connect to NATS server")
            self.connected = False
        else:
            self.connected = True
            logger.info(f"Connected to NATS server at {self.url}")

    async def publish_todo_event(self, event_type: str, todo: dict):
        if not self.url or not self.connected or not self.nc:
            return

        payload = {
            "event": event_type,
            "todo": todo,
        }

        try:
            await self.nc.publish(
                "todo.events",
                json.dumps(payload).encode()
            )
        except Exception:
            logger.exception(f"Failed to publish {event_type} event")
