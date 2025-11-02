import httpx
from pydantic import HttpUrl

from pdfdrive_api.constants import BASE_URL, REQUEST_HEADERS


class Session:
    """Pdf-drive-api httpx based request session"""

    def __init__(self, base_url: str = BASE_URL, **httpx_client_kwargs):
        httpx_client_kwargs.setdefault("headers", REQUEST_HEADERS)
        httpx_client_kwargs.setdefault("follow_redirects", True)

        self.async_client = httpx.AsyncClient(
            base_url=base_url, **httpx_client_kwargs
        )

    async def get(self, *args, **kwargs) -> httpx.Response:
        if args:
            args = list(args)
            url = args[0]

            if isinstance(url, HttpUrl):
                args.replace(url, str(url))

        resp = await self.async_client.get(*args, **kwargs)
        resp.raise_for_status()
        return resp
