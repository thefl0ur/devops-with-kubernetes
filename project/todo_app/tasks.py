from datetime import datetime
from pathlib import Path

import httpx

from todo_app.config import settings


def _should_update(image_file) -> bool:
    if not image_file.exists():
        return True

    now = datetime.now().timestamp()
    if image_file.stat().st_ctime + settings.image_ttl < now:
        return True

    return False


async def update_image():
    image_file = Path(settings.image_cache_folder) / settings.image_name

    if not _should_update(image_file):
        return

    async with httpx.AsyncClient() as client:
        response = await client.get(settings.random_image_source, follow_redirects=True)

    if response.status_code != 200:
        return

    image_file.write_bytes(response.content)
