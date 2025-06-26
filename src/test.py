#!/usr/bin/env python3
"""
Simple test script to verify the device manager system works correctly.
This script tests the core functionality without running the full demonstration.
"""

import sys

from src.device_manager import DeviceManager
from src.models import Switch, Dimmer, Lock, Thermostat, Hub, Dwelling


def test_basic_functionality():
    """Test basic functionality"""
    print("Testing basic functionality...")
    
    # Initialize device manager
    manager = DeviceManager()
    
    # Test device creation
    switch_id = manager.create_device("switch", "Test Switch")
    dimmer_id = manager.create_device("dimmer", "Test Dimmer")
    lock_id = manager.create_device("lock", "Test Lock", pin="1234")
    thermostat_id = manager.create_device("thermostat", "Test Thermostat")
    
    assert switch_id is not None, "Switch creation failed"
    assert dimmer_id is not None, "Dimmer creation failed"
    assert lock_id is not None, "Lock creation failed"
    assert thermostat_id is not None, "Thermostat creation failed"
    
    print("✓ Device creation works")
    
    # Test device listing
    devices = manager.list_devices()
    assert len(devices) == 4, f"Expected 4 devices, got {len(devices)}"
    print("✓ Device listing works")
    
    # Test device modification
    success = manager.modify_device(switch_id, power="on")
    assert success, "Switch modification failed"
    
    device_info = manager.get_device_info(switch_id)
    assert device_info["state"]["power"] == "on", "Switch state not updated"
    print("✓ Device modification works")
    
    # Test hub creation and pairing
    hub_id = manager.create_main_hub("Test Hub")
    assert hub_id is not None, "Hub creation failed"
    
    success = manager.pair_device(switch_id)
    assert success, "Device pairing failed"
    
    paired_devices = manager.list_hub_devices()
    assert len(paired_devices) == 1, "Device not properly paired"
    print("✓ Hub operations work")
    
    # Test dwelling creation and hub installation
    dwelling_id = manager.create_dwelling("Test Home", "123 Test St")
    assert dwelling_id is not None, "Dwelling creation failed"
    
    success = manager.install_hub(dwelling_id)
    assert success, "Hub installation failed"
    
    manager.set_dwelling_occupied(dwelling_id, True)
    dwelling_info = manager.get_dwelling_info(dwelling_id)
    assert dwelling_info["is_occupied"] == True, "Dwelling occupancy not set"
    print("✓ Dwelling operations work")
    
    print("All basic functionality tests passed!")


def test_error_handling():
    """Test error handling and edge cases"""
    print("\nTesting error handling...")
    
    manager = DeviceManager()
    
    # Test invalid device creation
    invalid_device_id = manager.create_device("invalid_type", "Test")
    assert invalid_device_id is None, "Should not create invalid device type"
    print("✓ Invalid device type handling works")
    
    # Test device deletion of paired device
    switch_id = manager.create_device("switch", "Test Switch")
    manager.create_main_hub("Test Hub")
    manager.pair_device(switch_id)
    
    success = manager.delete_device(switch_id)
    assert not success, "Should not delete paired device"
    print("✓ Paired device deletion protection works")
    
    # Test invalid operations
    device_state = manager.get_device_state("fake-device")
    assert device_state is None, "Should return None for invalid device"
    print("✓ Invalid operation handling works")
    
    print("All error handling tests passed!")


def test_device_types():
    """Test all device types and their specific functionality"""
    print("\nTesting device types...")
    
    manager = DeviceManager()
    
    # Test Switch
    switch_id = manager.create_device("switch", "Test Switch")
    manager.modify_device(switch_id, power="on")
    device_info = manager.get_device_info(switch_id)
    assert device_info["state"]["power"] == "on", "Switch power not set"
    print("✓ Switch functionality works")
    
    # Test Dimmer
    dimmer_id = manager.create_device("dimmer", "Test Dimmer")
    manager.modify_device(dimmer_id, power="on", brightness=75)
    device_info = manager.get_device_info(dimmer_id)
    assert device_info["state"]["power"] == "on", "Dimmer power not set"
    assert device_info["state"]["brightness"] == 75, "Dimmer brightness not set"
    print("✓ Dimmer functionality works")
    
    # Test Lock
    lock_id = manager.create_device("lock", "Test Lock", pin="5678")
    manager.modify_device(lock_id, state="unlocked")
    device_info = manager.get_device_info(lock_id)
    assert device_info["state"]["state"] == "unlocked", "Lock state not set"
    print("✓ Lock functionality works")
    
    # Test Thermostat
    thermostat_id = manager.create_device("thermostat", "Test Thermostat")
    manager.modify_device(thermostat_id, target_temp=68.0, mode="heat")
    device_info = manager.get_device_info(thermostat_id)
    assert device_info["state"]["target_temperature"] == 68.0, "Thermostat target not set"
    assert device_info["state"]["mode"] == "heat", "Thermostat mode not set"
    print("✓ Thermostat functionality works")
    
    print("All device type tests passed!")


def main():
    """Run all tests"""
    print("Running Tests")
    print("=" * 50)
    
    try:
        test_basic_functionality()
        test_error_handling()
        test_device_types()
        
        print("\n" + "=" * 50)
        print("ALL TESTS PASSED! ✅")
        
    except Exception as e:
        print(f"\nTEST FAILED: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 