#!/usr/bin/env python3
"""
Standalone validation test for directory dependencies.

This script tests the fix for issue #3: allowing directories as dependencies
in Elyra pipelines.
"""
import os
import sys
from pathlib import Path

# Add elyra to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from elyra.pipeline.validation import PipelineValidationManager, ValidationResponse


def test_directory_dependency():
    """Test that directories can be used as dependencies."""

    print("=" * 70)
    print("Testing Directory Dependency Support")
    print("=" * 70)

    # Setup
    test_dir = Path(__file__).parent
    sample_data_dir = test_dir / "sample_data"

    # Verify test directory exists
    if not sample_data_dir.exists():
        print(f"❌ FAIL: Test directory not found: {sample_data_dir}")
        return False

    print(f"\n✓ Test directory exists: {sample_data_dir}")
    print(f"  Contents: {', '.join(os.listdir(sample_data_dir))}")

    # Initialize validation manager
    pvm = PipelineValidationManager.instance(root_dir=str(test_dir))

    # Test 1: Directory should be REJECTED by default
    print("\n" + "-" * 70)
    print("Test 1: Directory validation with allow_directory=False (default)")
    print("-" * 70)

    response1 = ValidationResponse()
    pvm._validate_filepath(
        node_id="test-node-1",
        node_label="Test Node 1",
        property_name="dependencies",
        filename=str(sample_data_dir),
        response=response1,
        binary_file_ok=True,
        allow_directory=False,  # Should reject
    )

    issues1 = response1.to_json().get("issues", [])
    if len(issues1) > 0 and "invalidFilePath" in issues1[0]["type"]:
        print("✓ PASS: Directory correctly rejected when allow_directory=False")
    else:
        print("❌ FAIL: Directory should be rejected when allow_directory=False")
        return False

    # Test 2: Directory should be ACCEPTED with allow_directory=True
    print("\n" + "-" * 70)
    print("Test 2: Directory validation with allow_directory=True")
    print("-" * 70)

    response2 = ValidationResponse()
    pvm._validate_filepath(
        node_id="test-node-2",
        node_label="Test Node 2",
        property_name="dependencies",
        filename=str(sample_data_dir),
        response=response2,
        binary_file_ok=True,
        allow_directory=True,  # Should accept
    )

    issues2 = response2.to_json().get("issues", [])
    if len(issues2) == 0:
        print("✓ PASS: Directory correctly accepted when allow_directory=True")
    else:
        print(f"❌ FAIL: Directory should be accepted when allow_directory=True")
        print(f"  Issues: {issues2}")
        return False

    # Test 3: Relative path should work
    print("\n" + "-" * 70)
    print("Test 3: Relative directory path validation")
    print("-" * 70)

    response3 = ValidationResponse()
    pvm._validate_filepath(
        node_id="test-node-3",
        node_label="Test Node 3",
        property_name="dependencies",
        filename="sample_data",
        response=response3,
        file_dir=str(test_dir),
        binary_file_ok=True,
        allow_directory=True,
    )

    issues3 = response3.to_json().get("issues", [])
    if len(issues3) == 0:
        print("✓ PASS: Relative directory path works correctly")
    else:
        print(f"❌ FAIL: Relative directory path should be accepted")
        print(f"  Issues: {issues3}")
        return False

    # Test 4: Files should still work (backward compatibility)
    print("\n" + "-" * 70)
    print("Test 4: Backward compatibility - file validation")
    print("-" * 70)

    response4 = ValidationResponse()
    pvm._validate_filepath(
        node_id="test-node-4",
        node_label="Test Node 4",
        property_name="dependencies",
        filename=str(sample_data_dir / "config.json"),
        response=response4,
        binary_file_ok=True,
        allow_directory=True,  # Files should work with or without this flag
    )

    issues4 = response4.to_json().get("issues", [])
    if len(issues4) == 0:
        print("✓ PASS: File dependencies still work (backward compatibility)")
    else:
        print(f"❌ FAIL: File dependencies should still work")
        print(f"  Issues: {issues4}")
        return False

    # Cleanup
    PipelineValidationManager.clear_instance()

    print("\n" + "=" * 70)
    print("✅ ALL TESTS PASSED!")
    print("=" * 70)
    print("\nDirectory dependencies are working correctly.")
    print("Issue #3 fix validated successfully.\n")

    return True


if __name__ == "__main__":
    try:
        success = test_directory_dependency()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
