#!/usr/bin/env python3
"""
Test script to demonstrate Python Enum round-trip behavior.
Tests if MyEnum(x.value) == x where x is an instance of MyEnum.
"""

from enum import Enum, IntEnum, auto


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


class Direction(Enum):
    NORTH = "north"
    SOUTH = "south"
    EAST = "east"
    WEST = "west"


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Status(Enum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETE = auto()


def test_enum_roundtrip():
    """Test round-trip behavior: MyEnum(x.value) == x"""
    
    print("Testing Enum round-trip behavior: MyEnum(x.value) == x")
    print("=" * 60)
    
    # Test with integer values
    print("\n1. Testing Color enum (integer values):")
    for color in Color:
        reconstructed = Color(color.value)
        is_equal = reconstructed == color
        is_same_object = reconstructed is color
        print(f"  {color.name}: value={color.value}")
        print(f"    Color({color.value}) == {color}: {is_equal}")
        print(f"    Same object (is): {is_same_object}")
    
    # Test with string values
    print("\n2. Testing Direction enum (string values):")
    for direction in Direction:
        reconstructed = Direction(direction.value)
        is_equal = reconstructed == direction
        is_same_object = reconstructed is direction
        print(f"  {direction.name}: value='{direction.value}'")
        print(f"    Direction('{direction.value}') == {direction}: {is_equal}")
        print(f"    Same object (is): {is_same_object}")
    
    # Test with IntEnum
    print("\n3. Testing Priority IntEnum:")
    for priority in Priority:
        reconstructed = Priority(priority.value)
        is_equal = reconstructed == priority
        is_same_object = reconstructed is priority
        print(f"  {priority.name}: value={priority.value}")
        print(f"    Priority({priority.value}) == {priority}: {is_equal}")
        print(f"    Same object (is): {is_same_object}")
    
    # Test with auto() values
    print("\n4. Testing Status enum (auto() values):")
    for status in Status:
        reconstructed = Status(status.value)
        is_equal = reconstructed == status
        is_same_object = reconstructed is status
        print(f"  {status.name}: value={status.value}")
        print(f"    Status({status.value}) == {status}: {is_equal}")
        print(f"    Same object (is): {is_same_object}")
    
    # Test edge cases
    print("\n5. Edge cases:")
    
    # Test with direct value access
    red_value = Color.RED.value
    red_reconstructed = Color(red_value)
    print(f"  Direct value: Color.RED.value = {red_value}")
    print(f"  Color({red_value}) == Color.RED: {red_reconstructed == Color.RED}")
    
    # Test that values are preserved
    print(f"\n  Value preservation:")
    print(f"    Color.RED.value: {Color.RED.value}")
    print(f"    Color(1).value: {Color(1).value}")
    print(f"    Values equal: {Color.RED.value == Color(1).value}")


if __name__ == "__main__":
    test_enum_roundtrip()