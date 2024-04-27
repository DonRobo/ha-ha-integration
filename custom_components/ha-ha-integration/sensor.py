"""Sensor platform for ha-ha-integration."""
from __future__ import annotations

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription

from .const import DOMAIN
from .coordinator import HaiDataUpdateCoordinator
from .entity import IntegrationBlueprintEntity

ENTITY_DESCRIPTIONS = (
    SensorEntityDescription(
        key="ha-ha-integration",
        name="Integration Sensor",
        icon="mdi:format-quote-close",
    ),
)


async def async_setup_entry(hass, entry, async_add_devices):
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_devices(
        IntegrationBlueprintSensor(
            coordinator=coordinator,
            entity_description=entity_description,
        )
        for entity_description in ENTITY_DESCRIPTIONS
    )


class IntegrationBlueprintSensor(IntegrationBlueprintEntity, SensorEntity):
    """ha-ha-integration Sensor class."""

    def __init__(
        self,
        coordinator: HaiDataUpdateCoordinator,
        entity_description: SensorEntityDescription,
    ) -> None:
        """Initialize the sensor class."""
        super().__init__(coordinator)
        self.entity_description = entity_description

    @property
    def state_class(self) -> str:
        """Return the state class of the sensor."""
        return self.coordinator.data["attributes"]["state_class"]

    @property
    def device_class(self) -> str:
        """Return the device class of the sensor."""
        return self.coordinator.data["attributes"]["device_class"]

    @property
    def native_unit_of_measurement(self) -> str:
        """Return the unit of measurement of the sensor."""
        return self.coordinator.data["attributes"]["unit_of_measurement"]

    @property
    def native_value(self) -> str:
        """Return the native value of the sensor."""
        return self.coordinator.data["state"]
