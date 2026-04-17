#!/usr/bin/env python3
"""Configuration Loader - Handle config files and templates"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional


class ConfigLoader:
    """Handles loading and saving configuration files"""

    # Default config directory
    CONFIG_DIR = Path.home() / ".wapi"
    CONFIG_FILE = CONFIG_DIR / "config.yaml"
    CONTACTS_FILE = CONFIG_DIR / "contacts.json"
    TASKS_FILE = CONFIG_DIR / "tasks.json"
    TEMPLATES_DIR = CONFIG_DIR / "templates"
    LOGS_DIR = CONFIG_DIR / "logs"
    LOG_FILE = LOGS_DIR / "messages.json"

    @classmethod
    def get_config_dir(cls) -> Path:
        """Get or create config directory"""
        cls.CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        return cls.CONFIG_DIR

    @classmethod
    def get_contacts_file(cls) -> Path:
        """Get contacts file path"""
        cls.get_config_dir()
        return cls.CONTACTS_FILE

    @classmethod
    def get_tasks_file(cls) -> Path:
        """Get tasks file path"""
        cls.get_config_dir()
        return cls.TASKS_FILE

    @classmethod
    def get_templates_dir(cls) -> Path:
        """Get templates directory path"""
        cls.TEMPLATES_DIR.mkdir(parents=True, exist_ok=True)
        return cls.TEMPLATES_DIR

    @classmethod
    def get_log_file(cls) -> Path:
        """Get log file path"""
        cls.LOGS_DIR.mkdir(parents=True, exist_ok=True)
        return cls.LOG_FILE

    @classmethod
    def load_config(cls) -> Dict[str, Any]:
        """Load main configuration file

        Returns:
            Configuration dict
        """
        default_config = {
            "browser": "chrome",
            "headless": False,
            "anti_ban": {
                "min_interval": 5,
                "max_interval": 15,
                "daily_limit": 50
            },
            "whatsapp": {
                "wait_timeout": 60,
                "qr_timeout": 120
            }
        }

        if cls.CONFIG_FILE.exists():
            try:
                with open(cls.CONFIG_FILE, "r", encoding="utf-8") as f:
                    user_config = yaml.safe_load(f)
                    if user_config:
                        default_config.update(user_config)
            except Exception as e:
                print(f"Error loading config: {e}")

        return default_config

    @classmethod
    def save_config(cls, config: Dict[str, Any]):
        """Save configuration file

        Args:
            config: Configuration dict to save
        """
        cls.get_config_dir()
        with open(cls.CONFIG_FILE, "w", encoding="utf-8") as f:
            yaml.dump(config, f, default_flow_style=False, allow_unicode=True)

    @classmethod
    def load_batch(cls, file_path: str) -> Dict[str, Any]:
        """Load batch message file

        Args:
            file_path: Path to YAML file

        Returns:
            Batch configuration dict
        """
        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @classmethod
    def load_templates(cls) -> Dict[str, Any]:
        """Load all message templates

        Returns:
            Dict of template name -> template config
        """
        templates = {}
        templates_dir = cls.get_templates_dir()

        if templates_dir.exists():
            for file in templates_dir.glob("*.yaml"):
                try:
                    with open(file, "r", encoding="utf-8") as f:
                        template_data = yaml.safe_load(f)
                        if template_data:
                            # Use filename without extension as template name
                            name = file.stem
                            templates[name] = template_data
                except Exception as e:
                    print(f"Error loading template {file}: {e}")

        # Add default templates if none exist
        if not templates:
            templates = {
                "greeting": {
                    "template": "Hello {name}! This is {sender}.",
                    "description": "Simple greeting message",
                    "variables": ["name", "sender"]
                },
                "reminder": {
                    "template": "Reminder: {message}",
                    "description": "Simple reminder",
                    "variables": ["message"]
                }
            }

        return templates

    @classmethod
    def save_template(cls, name: str, template: Dict[str, Any]):
        """Save a message template

        Args:
            name: Template name
            template: Template config dict
        """
        templates_dir = cls.get_templates_dir()
        file_path = templates_dir / f"{name}.yaml"

        with open(file_path, "w", encoding="utf-8") as f:
            yaml.dump(template, f, default_flow_style=False, allow_unicode=True)

    @classmethod
    def render_template(cls, template_name: str, variables: Dict[str, str]) -> Optional[str]:
        """Render a template with variables

        Args:
            template_name: Name of the template
            variables: Dict of variable values

        Returns:
            Rendered message or None
        """
        templates = cls.load_templates()
        if template_name not in templates:
            return None

        template = templates[template_name]["template"]
        try:
            return template.format(**variables)
        except KeyError as e:
            print(f"Missing variable: {e}")
            return None
