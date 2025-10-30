import httpx

from pdfdrive_api.constants import REQUEST_HEADERS, BASE_URL


class Session:
    """Pdf-drive-api httpx based request session"""

    def __init__(self, base_url: str = BASE_URL, **httpx_client_kwargs):
        httpx_client_kwargs.setdefault("headers", REQUEST_HEADERS)
        self.async_client = httpx.AsyncClient(
            base_url=base_url, **httpx_client_kwargs
        )

    async def get(self, *args, **kwargs) -> httpx.Response:
        resp = await self.async_client.get(*args, **kwargs)
        resp.raise_for_status()
        return resp
