"""Adds config flow for Blueprint."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_create_clientsession

from .api import (
    HaiRestApiClient,
    HaiApiClientAuthenticationError,
    HaiApiClientCommunicationError,
    HaiApiClientError,
)
from .const import DOMAIN, LOGGER


class BlueprintFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Blueprint."""

    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict | None = None,
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_credentials(
                    url=user_input["url"],
                    auth_token=user_input["auth_token"],
                    ssl=user_input["ssl"],
                )
            except HaiApiClientAuthenticationError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "auth"
            except HaiApiClientCommunicationError as exception:
                LOGGER.error(exception)
                _errors["base"] = "connection"
            except HaiApiClientError as exception:
                LOGGER.exception(exception)
                _errors["base"] = "unknown"
            else:
                return self.async_create_entry(
                    title=user_input["name"],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("name"): str,
                    vol.Required("url"): str,
                    vol.Required("auth_token"): str,
                    vol.Required("ssl", default=True): bool,
                }
            ),
            errors=_errors,
        )

    async def _test_credentials(self, url: str, auth_token: str, ssl:bool) -> None:
        """Validate credentials."""
        client = HaiRestApiClient(
            url=url,
            auth_token=auth_token,
            ssl=ssl,
            session=async_create_clientsession(self.hass),
        )
        await client.async_get_all_states()
