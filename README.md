### How to run

You can import and use the system programmatically:

```python
from src.device_manager import DeviceManager

# Initialize the device manager
manager = DeviceManager()

# Create devices
switch_id = manager.create_device("switch", "Living Room Light")
dimmer_id = manager.create_device("dimmer", "Bedroom Light")
lock_id = manager.create_device("lock", "Front Door", pin="1234")
thermostat_id = manager.create_device("thermostat", "Main Thermostat")

# Create the main hub
hub_id = manager.create_hub("Main Hub")

# Pair devices to main hub
manager.pair_device(switch_id)
manager.pair_device(dimmer_id)

# Create a dwelling
dwelling_id = manager.create_dwelling("My Home", "123 St")

# Install main hub in dwelling
manager.install_hub(dwelling_id)

# Set dwelling as occupied
manager.set_dwelling_occupied(dwelling_id, True)
```

## Device Operations

### Creating Devices

```python
# Create different types of devices
switch_id = manager.create_device("switch", "Living Room Light")
dimmer_id = manager.create_device("dimmer", "Bedroom Light", brightness=50)
lock_id = manager.create_device("lock", "Front Door", pin="5678")
thermostat_id = manager.create_device("thermostat", "Main Thermostat")
```

**Supported device types:**
- `switch` - Simple on/off device
- `dimmer` - Variable brightness device (0-100%)
- `lock` - Door lock with PIN protection
- `thermostat` - Temperature control device

### Device Information and State

```python
# Get device information
device_info = manager.get_device_info(device_id)

# List all devices
all_devices = manager.list_devices()

# Get devices by type
switches = manager.get_devices_by_type("switch")
dimmers = manager.get_devices_by_type("dimmer")
```

### Modifying Device States

```python
# Switch operations
manager.modify_device(switch_id, power="on")
manager.modify_device(switch_id, power="off")

# Dimmer operations
manager.modify_device(dimmer_id, power="on", brightness=75)
manager.modify_device(dimmer_id, brightness=50)

# Lock operations
manager.modify_device(lock_id, state="unlocked")
manager.modify_device(lock_id, state="locked")
manager.modify_device(lock_id, pin="9999")

# Thermostat operations
manager.modify_device(thermostat_id, target_temp=68.0, mode="heat")
manager.modify_device(thermostat_id, mode="cool")
manager.modify_device(thermostat_id, target_temp=72.0)
```

### Deleting Devices

```python
# Delete a device (only works if device is not paired)
success = manager.delete_device(device_id)
```

## Hub Operations

### Creating and Managing the Main Hub

```python
# Create the main hub (only one hub allowed)
hub_id = manager.create_hub("Main Hub")

# Get main hub information
hub_info = manager.get_hub_info()

# Get main hub ID
hub_id = manager.get_main_hub_id()
```

**Note**: The system only supports one main hub. If you call `create_main_hub()` multiple times, it will return the same hub ID.

### Device Pairing

```python
# Pair a device to the main hub
success = manager.pair_device(device_id)

# List devices paired to the main hub
paired_devices = manager.list_hub_devices()

# Get device state through the main hub
device_state = manager.get_device_state(device_id)

# Remove device from the main hub
success = manager.remove_device(device_id)
```

## Dwelling Operations

### Creating and Managing Dwellings

```python
# Create a dwelling
dwelling_id = manager.create_dwelling("My Home", "123 Main St, Anytown, USA")

# Get dwelling information
dwelling_info = manager.get_dwelling_info(dwelling_id)

# List all dwellings
all_dwellings = manager.list_dwellings()
```

### Dwelling Occupancy

```python
# Set dwelling as occupied
manager.set_dwelling_occupied(dwelling_id, True)

# Set dwelling as vacant
manager.set_dwelling_occupied(dwelling_id, False)
```

### Hub Installation

```python
# Install the main hub in a dwelling
success = manager.install_hub(dwelling_id)
```

## Some More Operations

### Filtering and Queries

```python
# Get all paired devices
paired_devices = manager.get_paired_devices()

# Get all unpaired devices
unpaired_devices = manager.get_unpaired_devices()

# Get devices by type
switches = manager.get_devices_by_type("switch")
dimmers = manager.get_devices_by_type("dimmer")
locks = manager.get_devices_by_type("lock")
thermostats = manager.get_devices_by_type("thermostat")
```

### Device States

Each device type has specific state properties:

**Switch:**
```json
{
  "power": "on" | "off"
}
```

**Dimmer:**
```json
{
  "power": "on" | "off",
  "brightness": 0-100
}
```

**Lock:**
```json
{
  "state": "locked" | "unlocked",
  "is_armed": true | false
}
```

**Thermostat:**
```json
{
  "current_temperature": 72.0,
  "target_temperature": 68.0,
  "mode": "heat" | "cool" | "auto" | "off",
  "is_running": true | false
}
```

### Complete Device Object

```json
{
  "device_id": "uuid-string",
  "name": "Device Name",
  "device_type": "switch|dimmer|lock|thermostat",
  "created_at": "2024-01-01T12:00:00",
  "is_paired": true | false,
  "hub_id": "hub-uuid-or-null",
  "state": { /* device-specific state */ }
}
```

### Main Hub Object

```json
{
  "hub_id": "uuid-string",
  "name": "Main Hub",
  "created_at": "2024-01-01T12:00:00",
  "dwelling_id": "dwelling-uuid-or-null",
  "paired_devices_count": 5
}
```

## Testing

The system includes comprehensive driver functions that demonstrate all operations. You can run specific demonstrations:

```python
from src.driver import (
    demo_device_operations,
    demo_hub_operations,
    demo_dwelling_operations,
    demo_advanced_operations
)

# Run individual demos
manager, device_ids = demo_device_operations()
hub_id = demo_hub_operations(manager, device_ids)
dwelling_ids = demo_dwelling_operations(manager)
```

## Requirements

- Python 3.7+
- No external dependencies required (uses only standard library)
