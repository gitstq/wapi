#!/usr/bin/env python3
"""Unit tests for ContactManager"""

import pytest
import tempfile
import os
import json
from pathlib import Path
from unittest.mock import patch


class TestContactManager:
    """Test cases for ContactManager"""

    @pytest.fixture
    def temp_config_dir(self):
        """Create temporary config directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def contact_manager(self, temp_config_dir):
        """Create ContactManager with temp directory"""
        with patch("wapi.config.loader.ConfigLoader.get_contacts_file") as mock:
            contacts_file = temp_config_dir / "contacts.json"
            mock.return_value = contacts_file

            from wapi.core.contact import ContactManager
            return ContactManager()

    def test_add_contact(self, contact_manager):
        """Test adding a new contact"""
        contact_id = contact_manager.add_contact(
            name="John Doe",
            phone="+1234567890",
            group="Friends",
            tags=["important", "work"]
        )

        assert contact_id is not None
        assert len(contact_id) == 8

        contacts = contact_manager.list_contacts()
        assert len(contacts) == 1
        assert contacts[0]["name"] == "John Doe"
        assert contacts[0]["phone"] == "+1234567890"
        assert contacts[0]["group"] == "Friends"

    def test_add_duplicate_phone(self, contact_manager):
        """Test that duplicate phone numbers are rejected"""
        contact_manager.add_contact(name="John", phone="+1234567890")

        with pytest.raises(ValueError, match="already exists"):
            contact_manager.add_contact(name="Jane", phone="+1234567890")

    def test_delete_contact(self, contact_manager):
        """Test deleting a contact"""
        contact_id = contact_manager.add_contact(name="John", phone="+1234567890")

        assert contact_manager.delete_contact(contact_id)
        assert len(contact_manager.list_contacts()) == 0

        # Deleting non-existent should return False
        assert not contact_manager.delete_contact("nonexistent")

    def test_list_contacts_filter_by_group(self, contact_manager):
        """Test filtering contacts by group"""
        contact_manager.add_contact(name="John", phone="+1111111111", group="Friends")
        contact_manager.add_contact(name="Jane", phone="+2222222222", group="Work")
        contact_manager.add_contact(name="Bob", phone="+3333333333", group="Friends")

        friends = contact_manager.list_contacts(group="Friends")
        assert len(friends) == 2

        work = contact_manager.list_contacts(group="Work")
        assert len(work) == 1

    def test_list_contacts_filter_by_tag(self, contact_manager):
        """Test filtering contacts by tag"""
        contact_manager.add_contact(name="John", phone="+1111111111", tags=["vip"])
        contact_manager.add_contact(name="Jane", phone="+2222222222", tags=["regular"])
        contact_manager.add_contact(name="Bob", phone="+3333333333", tags=["vip", "priority"])

        vip = contact_manager.list_contacts(tag="vip")
        assert len(vip) == 2

        priority = contact_manager.list_contacts(tag="priority")
        assert len(priority) == 1

    def test_normalize_phone(self):
        """Test phone number normalization"""
        from wapi.core.contact import ContactManager

        assert ContactManager._normalize_phone("1234567890") == "+1234567890"
        assert ContactManager._normalize_phone("+1234567890") == "+1234567890"
        assert ContactManager._normalize_phone("+86-138-0000-0000") == "+8613800000000"
        assert ContactManager._normalize_phone("(123) 456-7890") == "+1234567890"

    def test_get_groups(self, contact_manager):
        """Test getting unique groups"""
        contact_manager.add_contact(name="John", phone="+1111111111", group="Friends")
        contact_manager.add_contact(name="Jane", phone="+2222222222", group="Work")
        contact_manager.add_contact(name="Bob", phone="+3333333333", group="Friends")

        groups = contact_manager.get_groups()
        assert set(groups) == {"Friends", "Work"}

    def test_export_json(self, contact_manager):
        """Test exporting contacts to JSON"""
        contact_manager.add_contact(name="John", phone="+1234567890", group="Friends")

        exported = contact_manager.export_contacts(format="json")
        data = json.loads(exported)

        assert len(data) == 1
        assert data[0]["name"] == "John"

    def test_export_csv(self, contact_manager):
        """Test exporting contacts to CSV"""
        contact_manager.add_contact(name="John", phone="+1234567890", group="Friends")

        exported = contact_manager.export_contacts(format="csv")
        lines = exported.split("\n")

        assert len(lines) == 2  # Header + 1 contact
        assert "John" in lines[1]
        assert "+1234567890" in lines[1]
