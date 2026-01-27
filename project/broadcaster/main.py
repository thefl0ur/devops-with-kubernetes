import asyncio
import json
import logging
import sys

import httpx
import nats

from broadcaster.settings import settings


handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)

logger.addHandler(handler)
logger.setLevel(logging.INFO)


async def handle_message(msg):
    data = json.loads(msg.data.decode())

    payload = {
        "user": "bot",
        "event": data["event"],
        "item": {
            "id": data["todo"]["id"],
            "text": data["todo"]["text"],
            "is_completed": data["todo"]["is_complete"]
        }
    }

    logger.info(payload)

    if settings.is_debug:
        return

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.webhook_url, json=payload, timeout=10)

        response.raise_for_status()

    except Exception:
        logger.exception("Webhook failed")


async def main():
    nc = await nats.connect(settings.nats_url)
    logger.info("connected")

    await nc.subscribe(settings.subject, queue=settings.queue_group, cb=handle_message)

    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    logger.info("starting")
    asyncio.run(main())
