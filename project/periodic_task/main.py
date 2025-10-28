import os

import httpx


def get_link() -> str:
    response = httpx.get(os.getenv("SOURCE_KEY"), follow_redirects=False)
    code = response.status_code
    if code >= 400:
        response.raise_for_status()
    elif code < 300:
        raise ValueError(f"Unexpected result: expect response in range 3XX, got {code}")

    return response.headers["location"]


def main() -> None:
    target = os.getenv("TARGET_KEY")

    link = None
    # respect restriction from exercise 1.13
    while True:
        link = get_link()
        if len(link) <= 140:
            break

    response = httpx.post(
        target,
        content=link,
        headers={"Content-Type": "text/plain"},
    )
    response.raise_for_status()


if __name__ == "__main__":
    main()
