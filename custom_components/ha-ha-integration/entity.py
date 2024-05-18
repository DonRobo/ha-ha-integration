"""BlueprintEntity class."""
from __future__ import annotations

from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, VERSION
from .coordinator import HaiDataUpdateCoordinator


class HaiEntity(CoordinatorEntity):
    """BlueprintEntity class."""

    def __init__(self, coordinator: HaiDataUpdateCoordinator, context: str) -> None:
        """Initialize."""
        super().__init__(coordinator, context=context)

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            name=coordinator.config_entry.data["name"],
            model=VERSION,
            manufacturer="Home Assistant",
        )
