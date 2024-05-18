"""Sensor platform for ha-ha-integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity

from .const import DOMAIN
from .coordinator import HaiDataUpdateCoordinator
from .entity import HaiEntity
from typing import Any

async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    await coordinator.async_config_entry_first_refresh()

    async_add_devices(
        HaiSensor(coordinator, entity["entity_id"]) for entity in coordinator.data if entity["entity_id"].startswith("sensor.") and (
            "attributes" not in entity or "device_class" not in entity["attributes"] or entity["attributes"]["device_class"] != "timestamp"
        )
    )


class HaiSensor(HaiEntity, SensorEntity):
    """ha-ha-integration Sensor class."""

    def __init__(
        self,
        coordinator: HaiDataUpdateCoordinator,
        remote_id: str,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator, context=remote_id)
        self._remote_id = remote_id
        self._remote_id_name_part = remote_id.replace("sensor.", "")
        self._attr_unique_id = coordinator.config_entry.entry_id+ "_" + remote_id
        self._attr_has_entity_name = True
        self._attr_name = self._remote_id_name_part.replace("_", " ").title()
        self._attr_entity_registry_enabled_default = False


    def _get_remote_entity(self) -> Any | None:
        """Get remote entity."""
        for entity in self.coordinator.data:
            if entity["entity_id"] == self._remote_id:
                return entity
        return None

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        remote_entity = self._get_remote_entity()
        if remote_entity is None or "attributes" not in remote_entity or "state_class" not in remote_entity["attributes"]:
            return None
        return remote_entity["attributes"]["state_class"]

    @property
    def device_class(self) -> str:
        """Return the device class of the sensor."""
        remote_entity = self._get_remote_entity()
        if remote_entity is None or "attributes" not in remote_entity or "device_class" not in remote_entity["attributes"]:
            return None
        return remote_entity["attributes"]["device_class"]


    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor."""
        remote_entity = self._get_remote_entity()
        if remote_entity is None or "attributes" not in remote_entity or "unit_of_measurement" not in remote_entity["attributes"]:
            return None
        return remote_entity["attributes"]["unit_of_measurement"]

    @property
    def native_value(self) -> str | None:
        """Return the native value of the sensor."""
        remote_entity = self._get_remote_entity()
        if remote_entity is None or "state" not in remote_entity:
            return None
        state= self._get_remote_entity()["state"]
        if state == "unknown" or state == "unavailable":
            return None
        else:
            return state

    @property
    def unique_id(self)->str:
        """Return a unique ID."""
        return self._remote_id_name_part

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._remote_id_name_part
