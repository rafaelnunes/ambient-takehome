from typing import Dict, List, Optional, Any
import uuid
from .models import (
    Device, Switch, Dimmer, Lock, Thermostat, Hub, Dwelling,
    DeviceType
)


class DeviceManager:
    """Main service class for managing devices, hub, and dwellings"""

    def __init__(self):
        self.devices: Dict[str, Device] = {}
        self.main_hub: Optional[Hub] = None
        self.dwellings: Dict[str, Dwelling] = {}

    def create_device(self, device_type: str, name: str, **kwargs) -> Optional[str]:
        """Create a new device"""
        device_id = str(uuid.uuid4())

        try:
            if device_type.lower() == "switch":
                device = Switch(device_id, name)
            elif device_type.lower() == "dimmer":
                device = Dimmer(device_id, name)
            elif device_type.lower() == "lock":
                pin = kwargs.get("pin", "0000")
                device = Lock(device_id, name, pin)
            elif device_type.lower() == "thermostat":
                device = Thermostat(device_id, name)
            else:
                return None

            self.devices[device_id] = device
            return device_id
        except Exception:
            return None

    def delete_device(self, device_id: str) -> bool:
        """Delete a device that is not currently paired"""
        if device_id not in self.devices:
            return False

        device = self.devices[device_id]
        if device.is_paired:
            return False

        del self.devices[device_id]
        return True

    def get_device_info(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve the current state of a device"""
        if device_id not in self.devices:
            return None

        return self.devices[device_id].to_dict()

    def modify_device(self, device_id: str, **kwargs) -> bool:
        """Change the state of the device"""
        if device_id not in self.devices:
            return False

        device = self.devices[device_id]
        return device.modify_state(**kwargs)

    def list_devices(self) -> List[Dict[str, Any]]:
        """List all devices"""
        return [device.to_dict() for device in self.devices.values()]

    def create_hub(self, name: str = "Main Hub") -> str:
        """Create the main hub"""
        if self.main_hub is not None:
            return self.main_hub.hub_id

        hub_id = str(uuid.uuid4())
        self.main_hub = Hub(hub_id, name)
        return hub_id

    def get_hub_id(self) -> Optional[str]:
        """Get the main hub ID if it exists"""
        return self.main_hub.hub_id if self.main_hub else None

    def pair_device(self, device_id: str) -> bool:
        """Pair a previously created device to the main hub"""
        if self.main_hub is None or device_id not in self.devices:
            return False

        device = self.devices[device_id]
        return self.main_hub.pair_device(device)

    def get_device_state(self, device_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a device's current state through the main hub"""
        if self.main_hub is None:
            return None

        return self.main_hub.get_device_state(device_id)

    def list_hub_devices(self) -> List[Dict[str, Any]]:
        """Get a list of devices paired to the main hub"""
        if self.main_hub is None:
            return []

        return self.main_hub.list_devices()

    def remove_device(self, device_id: str) -> bool:
        """Unpair a device from the main hub"""
        if self.main_hub is None:
            return False

        return self.main_hub.remove_device(device_id)

    def create_dwelling(self, name: str, address: str) -> str:
        """Create a new dwelling"""
        dwelling_id = str(uuid.uuid4())
        dwelling = Dwelling(dwelling_id, name, address)
        self.dwellings[dwelling_id] = dwelling
        return dwelling_id

    def set_dwelling_occupied(self, dwelling_id: str, occupied: bool) -> bool:
        """Set dwelling occupancy status"""
        if dwelling_id not in self.dwellings:
            return False

        dwelling = self.dwellings[dwelling_id]
        dwelling.set_occupied(occupied)
        return True

    def install_hub(self, dwelling_id: str) -> bool:
        """Associate the main hub with a dwelling"""
        if dwelling_id not in self.dwellings or self.main_hub is None:
            return False

        dwelling = self.dwellings[dwelling_id]
        return dwelling.install_hub(self.main_hub)

    def list_dwellings(self) -> List[Dict[str, Any]]:
        """Get a list of all dwellings"""
        return [dwelling.to_dict() for dwelling in self.dwellings.values()]

    def get_hub_info(self) -> Optional[Dict[str, Any]]:
        """Get main hub information"""
        if self.main_hub is None:
            return None

        return self.main_hub.to_dict()

    def get_dwelling_info(self, dwelling_id: str) -> Optional[Dict[str, Any]]:
        """Get dwelling information"""
        if dwelling_id not in self.dwellings:
            return None

        return self.dwellings[dwelling_id].to_dict()

    def get_devices_by_type(self, device_type: str) -> List[Dict[str, Any]]:
        """Get all devices of a specific type"""
        try:
            device_type_enum = DeviceType(device_type.lower())
            return [
                device.to_dict() 
                for device in self.devices.values() 
                if device.device_type == device_type_enum
            ]
        except ValueError:
            return []

    def get_paired_devices(self) -> List[Dict[str, Any]]:
        """Get all paired devices"""
        return [
            device.to_dict() 
            for device in self.devices.values() 
            if device.is_paired
        ]

    def get_unpaired_devices(self) -> List[Dict[str, Any]]:
        """Get all unpaired devices"""
        return [
            device.to_dict() 
            for device in self.devices.values() 
            if not device.is_paired
        ]
