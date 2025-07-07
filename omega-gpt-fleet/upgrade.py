#!/usr/bin/env python3
"""
OmegaGPT Fleet Upgrade Script

This script provides automated upgrade capabilities for the OmegaGPT Fleet
adapter system, enabling propagation of updates across multiple repositories
and automated maintenance of the adapter ecosystem.
"""

import os
import sys
import json
import subprocess
import argparse
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path


class OmegaGPTFleetUpgrader:
    """
    Main upgrader class for OmegaGPT Fleet adapter system.
    
    This class handles upgrades, propagation, and maintenance of the
    adapter system across multiple repositories and environments.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the upgrader.
        
        Args:
            config_path: Path to the upgrade configuration file
        """
        self.config_path = config_path or "./upgrade_config.json"
        self.config = self._load_config()
        self.logger = self._setup_logging()
        self.repositories = self.config.get("repositories", [])
        self.adapters = self.config.get("adapters", {})
        
    def _load_config(self) -> Dict[str, Any]:
        """Load upgrade configuration."""
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return json.load(f)
        else:
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict[str, Any]:
        """Create default upgrade configuration."""
        default_config = {
            "version": "1.0.0",
            "repositories": [
                {
                    "name": "spiral-portal-gxt",
                    "url": "https://github.com/SpiralCloudOmega/Spiral-portal-GXT.git",
                    "branch": "main",
                    "adapter_path": "omega-gpt-fleet/adapters"
                }
            ],
            "adapters": {
                "cad": ["freecad", "solvespace", "pythonocc", "build123d", "freecad_library", "openjscad"],
                "eda": ["vtr"],
                "web": ["caddy", "caddy_docker"],
                "research": ["nasa"],
                "networking": ["netbird", "docker", "exporter", "diagram", "dashboard"],
                "data": ["cassandra"],
                "vision_ml": ["pytorch3d", "pytorch_lightning", "pytorch_image_models"]
            },
            "upgrade_options": {
                "backup_before_upgrade": True,
                "run_tests": True,
                "auto_commit": False,
                "notification_webhook": ""
            }
        }
        
        # Save default config
        with open(self.config_path, "w") as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('omega_gpt_fleet_upgrade.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger('OmegaGPTFleetUpgrader')
    
    def upgrade_all(self) -> bool:
        """
        Perform full upgrade of all repositories and adapters.
        
        Returns:
            bool: True if upgrade successful, False otherwise
        """
        try:
            self.logger.info("Starting OmegaGPT Fleet upgrade process")
            
            # Backup current state if enabled
            if self.config.get("upgrade_options", {}).get("backup_before_upgrade", True):
                self._backup_current_state()
            
            # Update each repository
            for repo in self.repositories:
                self._upgrade_repository(repo)
            
            # Run validation tests
            if self.config.get("upgrade_options", {}).get("run_tests", True):
                self._run_validation_tests()
            
            self.logger.info("OmegaGPT Fleet upgrade completed successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Upgrade failed: {e}")
            return False
    
    def _backup_current_state(self):
        """Create backup of current adapter state."""
        backup_dir = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        # Copy current adapter files
        subprocess.run(["cp", "-r", "omega-gpt-fleet", backup_dir], check=True)
        self.logger.info(f"Backup created in {backup_dir}")
    
    def _upgrade_repository(self, repo: Dict[str, Any]):
        """
        Upgrade a specific repository.
        
        Args:
            repo: Repository configuration dictionary
        """
        self.logger.info(f"Upgrading repository: {repo['name']}")
        
        # Clone or update repository
        repo_dir = f"./repos/{repo['name']}"
        if os.path.exists(repo_dir):
            # Update existing repository
            subprocess.run(["git", "pull"], cwd=repo_dir, check=True)
        else:
            # Clone repository
            os.makedirs("./repos", exist_ok=True)
            subprocess.run(["git", "clone", repo["url"], repo_dir], check=True)
        
        # Update adapters in repository
        adapter_path = os.path.join(repo_dir, repo["adapter_path"])
        if os.path.exists(adapter_path):
            # Copy latest adapters
            subprocess.run(["cp", "-r", "omega-gpt-fleet/adapters/*", adapter_path], 
                         shell=True, check=True)
            self.logger.info(f"Adapters updated in {repo['name']}")
        else:
            self.logger.warning(f"Adapter path not found in {repo['name']}")
    
    def _run_validation_tests(self):
        """Run validation tests on upgraded adapters."""
        self.logger.info("Running validation tests")
        
        # Test adapter imports
        try:
            sys.path.insert(0, "omega-gpt-fleet")
            from adapters import BaseAdapter
            self.logger.info("Base adapter import test passed")
            
            # Test each adapter domain
            for domain in self.adapters.keys():
                try:
                    domain_module = __import__(f"adapters.{domain}", fromlist=[""])
                    self.logger.info(f"Domain {domain} import test passed")
                except ImportError as e:
                    self.logger.warning(f"Domain {domain} import test failed: {e}")
                    
        except Exception as e:
            self.logger.error(f"Validation tests failed: {e}")
    
    def propagate_to_repositories(self, repositories: Optional[List[str]] = None):
        """
        Propagate adapter updates to specified repositories.
        
        Args:
            repositories: List of repository names to update, or None for all
        """
        target_repos = repositories or [repo["name"] for repo in self.repositories]
        
        for repo_config in self.repositories:
            if repo_config["name"] in target_repos:
                self._upgrade_repository(repo_config)
    
    def generate_upgrade_report(self) -> Dict[str, Any]:
        """
        Generate upgrade status report.
        
        Returns:
            Dict containing upgrade report data
        """
        report = {
            "timestamp": datetime.now().isoformat(),
            "version": self.config.get("version", "unknown"),
            "repositories": len(self.repositories),
            "adapter_domains": len(self.adapters),
            "total_adapters": sum(len(adapters) for adapters in self.adapters.values()),
            "status": "completed"
        }
        
        return report


def main():
    """Main entry point for the upgrade script."""
    parser = argparse.ArgumentParser(description="OmegaGPT Fleet Upgrade Script")
    parser.add_argument("--config", help="Path to upgrade configuration file")
    parser.add_argument("--repositories", nargs="*", help="Specific repositories to upgrade")
    parser.add_argument("--report-only", action="store_true", help="Generate report only")
    parser.add_argument("--backup", action="store_true", help="Create backup before upgrade")
    
    args = parser.parse_args()
    
    # Initialize upgrader
    upgrader = OmegaGPTFleetUpgrader(args.config)
    
    if args.report_only:
        # Generate report only
        report = upgrader.generate_upgrade_report()
        print(json.dumps(report, indent=2))
    else:
        # Perform upgrade
        if args.repositories:
            upgrader.propagate_to_repositories(args.repositories)
        else:
            upgrader.upgrade_all()


if __name__ == "__main__":
    main()