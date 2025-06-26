from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime


class DeviceType(Enum):
    SWITCH = "switch"
    DIMMER = "dimmer"
    LOCK = "lock"
    THERMOSTAT = "thermostat"


class DeviceState(Enum):
    ON = "on"
    OFF = "off"
    LOCKED = "locked"
    UNLOCKED = "unlocked"


class Device(ABC):
    """Abstract base class for all devices"""

    def __init__(self, device_id: str, name: str, device_type: DeviceType):
        self.device_id = device_id
        self.name = name
        self.device_type = device_type
        self.created_at = datetime.now()
        self.is_paired = False
        self.hub_id = None

    @abstractmethod
    def get_state(self) -> Dict[str, Any]:
        """Get current device state"""
        pass

    @abstractmethod
    def modify_state(self, **kwargs) -> bool:
        """Modify device state"""
        pass

    def to_dict(self) -> Dict[str, Any]:
        """Convert device to dictionary representation"""
        return {
            "device_id": self.device_id,
            "name": self.name,
            "device_type": self.device_type.value,
            "created_at": self.created_at.isoformat(),
            "is_paired": self.is_paired,
            "hub_id": self.hub_id,
            "state": self.get_state()
        }


class Switch(Device):
    """Switch device that can be turned on/off"""

    def __init__(self, device_id: str, name: str):
        super().__init__(device_id, name, DeviceType.SWITCH)
        self._state = DeviceState.OFF

    def get_state(self) -> Dict[str, Any]:
        return {"power": self._state.value}

    def modify_state(self, power: str = None) -> bool:
        if power is not None:
            if power.lower() in ["on", "off"]:
                self._state = DeviceState.ON if power.lower() == "on" else DeviceState.OFF
                return True
        return False


class Dimmer(Device):
    """Dimmer device that provides variable lighting"""

    def __init__(self, device_id: str, name: str):
        super().__init__(device_id, name, DeviceType.DIMMER)
        self._brightness = 0
        self._power = DeviceState.OFF

    def get_state(self) -> Dict[str, Any]:
        return {
            "power": self._power.value,
            "brightness": self._brightness
        }

    def modify_state(self, power: str = None, brightness: int = None) -> bool:
        if power is not None:
            if power.lower() in ["on", "off"]:
                self._power = DeviceState.ON if power.lower() == "on" else DeviceState.OFF
                if self._power == DeviceState.OFF:
                    self._brightness = 0
 
        if brightness is not None:
            if 0 <= brightness <= 100:
                self._brightness = brightness
                if self._brightness > 0:
                    self._power = DeviceState.ON
                return True

        return power is not None or brightness is not None


class Lock(Device):
    """Lock device that can be locked/unlocked with PIN"""

    def __init__(self, device_id: str, name: str, pin: str = "0000"):
        super().__init__(device_id, name, DeviceType.LOCK)
        self._state = DeviceState.LOCKED
        self._pin = pin
        self._is_armed = True

    def get_state(self) -> Dict[str, Any]:
        return {
            "state": self._state.value,
            "is_armed": self._is_armed
        }

    def modify_state(self, state: str = None, pin: str = None, is_armed: bool = None) -> bool:
        if state is not None:
            if state.lower() in ["locked", "unlocked"]:
                self._state = DeviceState.LOCKED if state.lower() == "locked" else DeviceState.UNLOCKED

        if pin is not None:
            self._pin = pin

        if is_armed is not None:
            self._is_armed = is_armed

        return state is not None or pin is not None or is_armed is not None

    def unlock_with_pin(self, pin: str) -> bool:
        """Attempt to unlock with PIN"""
        if pin == self._pin:
            self._state = DeviceState.UNLOCKED
            return True
        return False


class Thermostat(Device):
    """Thermostat device for controlling temperature"""

    def __init__(self, device_id: str, name: str):
        super().__init__(device_id, name, DeviceType.THERMOSTAT)
        self._current_temp = 72.0
        self._target_temp = 72.0
        self._mode = "heat"
        self._is_running = False

    def get_state(self) -> Dict[str, Any]:
        return {
            "current_temperature": self._current_temp,
            "target_temperature": self._target_temp,
            "mode": self._mode,
            "is_running": self._is_running
        }

    def modify_state(self, target_temp: float = None, mode: str = None) -> bool:
        if target_temp is not None:
            if 50 <= target_temp <= 90:
                self._target_temp = target_temp
  
        if mode is not None:
            if mode.lower() in ["heat", "cool", "auto", "off"]:
                self._mode = mode.lower()
                self._is_running = mode.lower() != "off"

        return target_temp is not None or mode is not None

    def update_current_temp(self, temp: float):
        """Update current temperature"""
        self._current_temp = temp


class Hub:
    """Hub that manages paired devices"""

    def __init__(self, hub_id: str, name: str):
        self.hub_id = hub_id
        self.name = name
        self.created_at = datetime.now()
        self.paired_devices: Dict[str, Device] = {}
        self.dwelling_id = None

    def pair_device(self, device: Device) -> bool:
        """Pair a device to this hub"""
        if device.is_paired:
            return False

        device.is_paired = True
        device.hub_id = self.hub_id
        self.paired_devices[device.device_id] = device
        return True

    def remove_device(self, device_id: str) -> bool:
        """Remove a device from this hub"""
        if device_id not in self.paired_devices:
            return False

        device = self.paired_devices[device_id]
        device.is_paired = False
        device.hub_id = None
        del self.paired_devices[device_id]
        return True

    def get_device_state(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get state of a paired device"""
        if device_id not in self.paired_devices:
            return None
        return self.paired_devices[device_id].get_state()

    def list_devices(self) -> List[Dict[str, Any]]:
        """List all paired devices"""
        return [device.to_dict() for device in self.paired_devices.values()]

    def to_dict(self) -> Dict[str, Any]:
        """Convert hub to dictionary representation"""
        return {
            "hub_id": self.hub_id,
            "name": self.name,
            "created_at": self.created_at.isoformat(),
            "dwelling_id": self.dwelling_id,
            "paired_devices_count": len(self.paired_devices)
        }


class Dwelling:
    """Dwelling where hubs and devices are installed"""

    def __init__(self, dwelling_id: str, name: str, address: str):
        self.dwelling_id = dwelling_id
        self.name = name
        self.address = address
        self.created_at = datetime.now()
        self.is_occupied = False
        self.installed_hubs: Dict[str, Hub] = {}

    def set_occupied(self, occupied: bool):
        """Set dwelling occupancy status"""
        self.is_occupied = occupied

    def install_hub(self, hub: Hub) -> bool:
        """Install a hub in this dwelling"""
        if hub.dwelling_id is not None:
            return False

        hub.dwelling_id = self.dwelling_id
        self.installed_hubs[hub.hub_id] = hub
        return True

    def remove_hub(self, hub_id: str) -> bool:
        """Remove a hub from this dwelling"""
        if hub_id not in self.installed_hubs:
            return False

        hub = self.installed_hubs[hub_id]
        hub.dwelling_id = None
        del self.installed_hubs[hub_id]
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Convert dwelling to dictionary representation"""
        return {
            "dwelling_id": self.dwelling_id,
            "name": self.name,
            "address": self.address,
            "created_at": self.created_at.isoformat(),
            "is_occupied": self.is_occupied,
            "installed_hubs_count": len(self.installed_hubs)
        }
