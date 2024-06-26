"""DataUpdateCoordinator for ha-ha-integration."""
from __future__ import annotations

from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)
from homeassistant.exceptions import ConfigEntryAuthFailed

from .api import (
    HaiRestApiClient,
    HaiApiClientAuthenticationError,
    HaiApiClientError,
)
from .const import LOGGER


# https://developers.home-assistant.io/docs/integration_fetching_data#coordinated-single-api-poll-for-data-for-all-entities
class HaiDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching data from the API."""

    config_entry: ConfigEntry

    def __init__(
        self,
        hass: HomeAssistant,
        client: HaiRestApiClient,
        name: str,
    ) -> None:
        """Initialize."""
        self.client = client
        super().__init__(
            hass=hass,
            logger=LOGGER,
            name=name,
            update_interval=timedelta(minutes=5),
        )

    async def _async_update_data(self):
        """Update data via library."""
        try:
            LOGGER.debug("Fetching data from API")
            return await self.client.async_get_all_states()
        except HaiApiClientAuthenticationError as exception:
            raise ConfigEntryAuthFailed(exception) from exception
        except HaiApiClientError as exception:
            raise UpdateFailed(exception) from exception
