from datetime import datetime
from pathlib import Path

import httpx

from todo_app.config import IMAGE_CACHE_DIR, IMAGE_NAME, IMAGE_TTL, RANDOM_IMAGE_SOURCE


def _should_update(image_file) -> bool:
    if not image_file.exists():
        return True

    now = datetime.now().timestamp()
    if image_file.stat().st_ctime + IMAGE_TTL < now:
        return True

    return False


async def update_image():
    image_file = Path(IMAGE_CACHE_DIR) / IMAGE_NAME

    if not _should_update(image_file):
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(RANDOM_IMAGE_SOURCE, follow_redirects=True)

    if response.status_code != 200:
        return

    image_file.write_bytes(response.content)
