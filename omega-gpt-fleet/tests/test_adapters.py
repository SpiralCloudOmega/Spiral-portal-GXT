#!/usr/bin/env python3
"""
Test suite for OmegaGPT Fleet Adapters

This test suite validates the adapter system functionality and ensures
all adapters can be imported and initialized properly.
"""

import sys
import os
import unittest
from pathlib import Path

# Add the omega-gpt-fleet to Python path
fleet_path = Path(__file__).parent.parent
sys.path.insert(0, str(fleet_path))

try:
    from adapters.base_adapter import BaseAdapter
    from adapters.cad import FreeCadAdapter, SolveSpaceAdapter
    from adapters.eda import VTRAdapter
    from adapters.web import CaddyAdapter, CaddyDockerAdapter
    from adapters.research import NASAAdapter
    from adapters.networking import NetBirdAdapter, DockerAdapter
    from adapters.data import CassandraAdapter
    from adapters.vision_ml import PyTorch3DAdapter
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


class TestAdapterSystem(unittest.TestCase):
    """Test the OmegaGPT Fleet adapter system."""
    
    def test_base_adapter_import(self):
        """Test that BaseAdapter can be imported and instantiated."""
        # This would need a concrete implementation for testing
        self.assertTrue(BaseAdapter)
    
    def test_cad_adapters(self):
        """Test CAD adapter imports and basic functionality."""
        adapters = [
            FreeCadAdapter(),
            SolveSpaceAdapter()
        ]
        
        for adapter in adapters:
            self.assertIsNotNone(adapter)
            self.assertEqual(adapter.metadata["type"], "cad")
            self.assertIn("capabilities", adapter.metadata)
    
    def test_eda_adapters(self):
        """Test EDA adapter imports and basic functionality."""
        adapter = VTRAdapter()
        self.assertIsNotNone(adapter)
        self.assertEqual(adapter.metadata["type"], "eda")
    
    def test_web_adapters(self):
        """Test Web adapter imports and basic functionality."""
        adapters = [
            CaddyAdapter(),
            CaddyDockerAdapter()
        ]
        
        for adapter in adapters:
            self.assertIsNotNone(adapter)
            self.assertEqual(adapter.metadata["type"], "web")
    
    def test_research_adapters(self):
        """Test Research adapter imports and basic functionality."""
        adapter = NASAAdapter()
        self.assertIsNotNone(adapter)
        self.assertEqual(adapter.metadata["type"], "research")
    
    def test_networking_adapters(self):
        """Test Networking adapter imports and basic functionality."""
        adapters = [
            NetBirdAdapter(),
            DockerAdapter()
        ]
        
        for adapter in adapters:
            self.assertIsNotNone(adapter)
            self.assertEqual(adapter.metadata["type"], "networking")
    
    def test_data_adapters(self):
        """Test Data adapter imports and basic functionality."""
        adapter = CassandraAdapter()
        self.assertIsNotNone(adapter)
        self.assertEqual(adapter.metadata["type"], "data")
    
    def test_vision_ml_adapters(self):
        """Test Vision/ML adapter imports and basic functionality."""
        adapter = PyTorch3DAdapter()
        self.assertIsNotNone(adapter)
        self.assertEqual(adapter.metadata["type"], "vision_ml")
    
    def test_adapter_lifecycle(self):
        """Test adapter initialization and cleanup lifecycle."""
        adapter = FreeCadAdapter()
        
        # Test initialization
        self.assertTrue(adapter.initialize())
        self.assertEqual(adapter.status, "ready")
        
        # Test validation
        self.assertTrue(adapter.validate())
        
        # Test cleanup
        self.assertTrue(adapter.cleanup())
        self.assertEqual(adapter.status, "cleaned")
    
    def test_adapter_execution(self):
        """Test adapter command execution."""
        adapter = FreeCadAdapter()
        adapter.initialize()
        
        # Test command execution
        result = adapter.execute("create_box", {"width": 10, "height": 10, "depth": 10})
        self.assertTrue(result["success"])
        self.assertIn("data", result)
        self.assertIn("message", result)
        
        adapter.cleanup()
    
    def test_adapter_configuration(self):
        """Test adapter configuration handling."""
        config = {
            "workspace": "/tmp/test_workspace",
            "freecad_path": "/usr/bin/freecad"
        }
        
        adapter = FreeCadAdapter(config)
        self.assertEqual(adapter.config, config)
        self.assertEqual(adapter.workspace, "/tmp/test_workspace")


class TestUpgradeSystem(unittest.TestCase):
    """Test the upgrade system functionality."""
    
    def test_upgrade_script_import(self):
        """Test that the upgrade script can be imported."""
        try:
            sys.path.insert(0, str(fleet_path))
            import upgrade
            self.assertTrue(hasattr(upgrade, 'OmegaGPTFleetUpgrader'))
        except ImportError:
            self.fail("Upgrade script could not be imported")


if __name__ == "__main__":
    print("Running OmegaGPT Fleet Adapter Tests...")
    print(f"Testing from path: {fleet_path}")
    
    # Create test loader and runner
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)