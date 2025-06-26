import json
from typing import Any
from src.device_manager import DeviceManager


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}")


def print_json(data: Any, title: str = ""):
    """Print data as formatted JSON"""
    if title:
        print(f"\n{title}:")
    print(json.dumps(data, indent=2))


def demo_device_operations():
    """Demonstrate all device operations"""
    print_section("DEVICE OPERATIONS DEMO")

    # Initialize device manager
    manager = DeviceManager()

    print("\n1. Creating devices...")

    # Create different types of devices
    switch_id = manager.create_device("switch", "Living Room Light")
    dimmer_id = manager.create_device("dimmer", "Bedroom Light")
    lock_id = manager.create_device("lock", "Front Door Lock", pin="5678")
    thermostat_id = manager.create_device("thermostat", "Main Thermostat")

    print(f"Created devices:")
    print(f"  Switch: {switch_id}")
    print(f"  Dimmer: {dimmer_id}")
    print(f"  Lock: {lock_id}")
    print(f"  Thermostat: {thermostat_id}")

    print("\n2. Listing all devices...")
    devices = manager.list_devices()
    print_json(devices, "All Devices")

    print("\n3. Getting device info...")
    switch_info = manager.get_device_info(switch_id)
    print_json(switch_info, "Switch Info")

    print("\n4. Modifying device states...")

    # Modify switch
    manager.modify_device(switch_id, power="on")
    print("Turned switch ON")

    # Modify dimmer
    manager.modify_device(dimmer_id, power="on", brightness=75)
    print("Turned dimmer ON with 75% brightness")

    # Modify lock
    manager.modify_device(lock_id, state="unlocked")
    print("Unlocked the door")

    # Modify thermostat
    manager.modify_device(thermostat_id, target_temp=68.0, mode="heat")
    print("Set thermostat to 68°F in heat mode")

    print("\n5. Getting updated device states...")
    updated_devices = manager.list_devices()
    print_json(updated_devices, "Updated Device States")

    print("\n6. Getting devices by type...")
    switches = manager.get_devices_by_type("switch")
    print_json(switches, "All Switches")

    return manager, [switch_id, dimmer_id, lock_id, thermostat_id]


def demo_hub_operations(manager: DeviceManager, device_ids: list):
    """Demonstrate all hub operations"""
    print_section("HUB OPERATIONS DEMO")

    print("\n1. Creating main hub...")
    hub_id = manager.create_hub("Main Hub")
    print(f"Created main hub: {hub_id}")

    print("\n2. Pairing devices to main hub...")

    # Pair all devices to main hub
    manager.pair_device(device_ids[0])  # Switch
    manager.pair_device(device_ids[1])  # Dimmer
    manager.pair_device(device_ids[2])  # Lock
    manager.pair_device(device_ids[3])  # Thermostat
    print("Paired all devices to Main Hub")
    
    print("\n3. Listing devices paired to main hub...")
    hub_devices = manager.list_hub_devices()
    print_json(hub_devices, f"Devices paired to Main Hub ({hub_id})")
    
    print("\n4. Getting device states through main hub...")
    switch_state = manager.get_device_state(device_ids[0])
    print_json(switch_state, "Switch state from Main Hub")
    
    lock_state = manager.get_device_state(device_ids[2])
    print_json(lock_state, "Lock state from Main Hub")
    
    print("\n5. Modifying devices through hub...")
    # Modify switch through hub
    manager.modify_device(device_ids[0], power="off")
    print("Turned switch OFF through hub")
    
    updated_switch_state = manager.get_device_state(device_ids[0])
    print_json(updated_switch_state, "Updated switch state")
    
    print("\n6. Removing device from hub...")
    manager.remove_device(device_ids[1])  # Remove dimmer
    print("Removed dimmer from Main Hub")
    
    remaining_devices = manager.list_hub_devices()
    print_json(remaining_devices, "Remaining devices in Main Hub")
    
    return hub_id


def demo_dwelling_operations(manager: DeviceManager):
    """Demonstrate all dwelling operations"""
    print_section("DWELLING OPERATIONS DEMO")
    
    print("\n1. Creating dwellings...")
    dwelling1_id = manager.create_dwelling("Smith Residence", "123 Main St, Anytown, USA")
    dwelling2_id = manager.create_dwelling("Johnson Apartment", "456 Oak Ave, Somewhere, USA")
    
    print(f"Created dwellings:")
    print(f"  Smith Residence: {dwelling1_id}")
    print(f"  Johnson Apartment: {dwelling2_id}")
    
    print("\n2. Installing main hub in dwelling...")
    # Only install in the first dwelling since we only have one hub
    manager.install_hub(dwelling1_id)
    print("Installed Main Hub in Smith Residence")
    
    print("\n3. Setting dwelling occupancy...")
    manager.set_dwelling_occupied(dwelling1_id, True)
    manager.set_dwelling_occupied(dwelling2_id, False)
    
    print("Set Smith Residence as OCCUPIED")
    print("Set Johnson Apartment as VACANT")
    
    print("\n4. Listing all dwellings...")
    dwellings = manager.list_dwellings()
    print_json(dwellings, "All Dwellings")
    
    print("\n5. Getting dwelling information...")
    dwelling1_info = manager.get_dwelling_info(dwelling1_id)
    print_json(dwelling1_info, "Smith Residence Info")
    
    dwelling2_info = manager.get_dwelling_info(dwelling2_id)
    print_json(dwelling2_info, "Johnson Apartment Info")
    
    return [dwelling1_id, dwelling2_id]


def demo_advanced_operations(manager: DeviceManager):
    """Demonstrate advanced operations and edge cases"""
    print_section("ADVANCED OPERATIONS DEMO")
    
    print("\n1. Creating additional devices for testing...")
    
    # Create some unpaired devices
    unpaired_switch_id = manager.create_device("switch", "Garage Light")
    unpaired_dimmer_id = manager.create_device("dimmer", "Backyard Light")
    
    print("Created unpaired devices:")
    print(f"  Garage Light: {unpaired_switch_id}")
    print(f"  Backyard Light: {unpaired_dimmer_id}")
    
    print("\n2. Testing device deletion...")
    
    # Try to delete a paired device (should fail)
    paired_devices = manager.get_paired_devices()
    if paired_devices:
        first_paired_id = paired_devices[0]["device_id"]
        delete_result = manager.delete_device(first_paired_id)
        print(f"Attempted to delete paired device {first_paired_id}: {'SUCCESS' if delete_result else 'FAILED (expected)'}")
    
    # Delete an unpaired device (should succeed)
    delete_result = manager.delete_device(unpaired_switch_id)
    print(f"Attempted to delete unpaired device {unpaired_switch_id}: {'SUCCESS' if delete_result else 'FAILED'}")
    
    print("\n3. Getting paired vs unpaired devices...")
    paired_devices = manager.get_paired_devices()
    print_json(paired_devices, "Paired Devices")
    
    unpaired_devices = manager.get_unpaired_devices()
    print_json(unpaired_devices, "Unpaired Devices")
    
    print("\n4. Testing invalid operations...")
    
    # Try to pair non-existent device
    fake_device_id = "fake-device-id"
    
    pair_result = manager.pair_device(fake_device_id)
    print(f"Attempted to pair non-existent device: {'SUCCESS' if pair_result else 'FAILED (expected)'}")
    
    # Try to get state of non-existent device
    state_result = manager.get_device_state(fake_device_id)
    print(f"Attempted to get state of non-existent device: {'FOUND' if state_result else 'NOT FOUND (expected)'}")
    
    print("\n5. Testing device type filtering...")
    all_switches = manager.get_devices_by_type("switch")
    print_json(all_switches, "All Switches")
    
    all_dimmers = manager.get_devices_by_type("dimmer")
    print_json(all_dimmers, "All Dimmers")
    
    all_locks = manager.get_devices_by_type("lock")
    print_json(all_locks, "All Locks")
    
    all_thermostats = manager.get_devices_by_type("thermostat")
    print_json(all_thermostats, "All Thermostats")
    
    print("\n6. Getting main hub information...")
    hub_info = manager.get_hub_info()
    print_json(hub_info, "Main Hub Info")


def run_complete_demo():
    """Run the complete demonstration of all operations"""
    print_section("COMPLETE DEVICE MANAGER DEMONSTRATION")
    print("This demo shows all required operations from the README requirements")
    print("Using a single main hub architecture")

    # Run all demos
    manager, device_ids = demo_device_operations()
    demo_hub_operations(manager, device_ids)
    demo_dwelling_operations(manager)


if __name__ == "__main__":
    run_complete_demo() 