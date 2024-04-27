from __future__ import annotations

import asyncio
import socket

import aiohttp
import async_timeout

from homeassistant.core import State

from .const import LOGGER

class HaiApiClientError(Exception):
    """Exception to indicate a general API error."""


class HaiApiClientCommunicationError(
    HaiApiClientError
):
    """Exception to indicate a communication error."""


class HaiApiClientAuthenticationError(
    HaiApiClientError
):
    """Exception to indicate an authentication error."""

class HaiApiClient:
    """Sample API Client."""

    def __init__(
        self,
        url: str,
        auth_token: str,
        ssl:bool,
        session: aiohttp.ClientSession,
    ) -> None:
        """Sample API Client."""
        self._url = url
        self._auth_token = auth_token
        self._session = session
        self._ssl = ssl

    async def async_get_state(self, entity_id) -> str | None:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(10):
                protocol = "https" if self._ssl else "http"
                response = await self._session.request(
                    method = "get",
                    url = f"{protocol}://{self._url}/api/states/{entity_id}",
                    headers = {
                        "Authorization": f"Bearer {self._auth_token}",
                        "Content-Type": "application/json",
                    }
                )

                if response.status in (401, 403):
                    raise HaiApiClientAuthenticationError(
                        "Invalid credentials",
                    )
                response.raise_for_status()
                json = await response.json()

                return json

        except asyncio.TimeoutError as exception:
            raise HaiApiClientCommunicationError(
                "Timeout error fetching information",
            ) from exception
        except (aiohttp.ClientError, socket.gaierror) as exception:
            raise HaiApiClientCommunicationError(
                "Error fetching information",
            ) from exception
        except Exception as exception:  # pylint: disable=broad-except
            raise HaiApiClientError(
                "Something really wrong happened!"
            ) from exception

