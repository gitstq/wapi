#!/usr/bin/env python3
"""
Contact Manager - Manage WhatsApp contacts
"""

import json
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any

from ..config.loader import ConfigLoader


class ContactManager:
    """Manages WhatsApp contacts with groups and tags"""

    def __init__(self):
        """Initialize contact manager"""
        self.contacts_file = ConfigLoader.get_contacts_file()
        self.contacts: List[Dict[str, Any]] = []
        self._load_contacts()

    def _load_contacts(self):
        """Load contacts from file"""
        if self.contacts_file.exists():
            try:
                self.contacts = json.loads(self.contacts_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                self.contacts = []
        else:
            self.contacts = []

    def _save_contacts(self):
        """Save contacts to file"""
        self.contacts_file.parent.mkdir(parents=True, exist_ok=True)
        self.contacts_file.write_text(
            json.dumps(self.contacts, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

    def add_contact(
        self,
        name: str,
        phone: str,
        group: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> str:
        """Add a new contact

        Args:
            name: Contact name
            phone: Phone number (with country code preferred)
            group: Optional group name
            tags: Optional list of tags

        Returns:
            Contact ID
        """
        contact_id = str(uuid.uuid4())[:8]

        contact = {
            "id": contact_id,
            "name": name,
            "phone": self._normalize_phone(phone),
            "group": group,
            "tags": tags or [],
            "created_at": str(uuid.uuid1())
        }

        # Check for duplicate phone
        if any(c.get("phone") == contact["phone"] for c in self.contacts):
            raise ValueError(f"Contact with phone {phone} already exists")

        self.contacts.append(contact)
        self._save_contacts()

        return contact_id

    def update_contact(self, contact_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing contact

        Args:
            contact_id: Contact ID to update
            updates: Fields to update

        Returns:
            True if updated successfully
        """
        for contact in self.contacts:
            if contact.get("id") == contact_id:
                if "phone" in updates:
                    updates["phone"] = self._normalize_phone(updates["phone"])
                contact.update(updates)
                self._save_contacts()
                return True
        return False

    def delete_contact(self, contact_id: str) -> bool:
        """Delete a contact by ID

        Args:
            contact_id: Contact ID to delete

        Returns:
            True if deleted successfully
        """
        original_count = len(self.contacts)
        self.contacts = [c for c in self.contacts if c.get("id") != contact_id]

        if len(self.contacts) < original_count:
            self._save_contacts()
            return True
        return False

    def get_contact(self, contact_id: str) -> Optional[Dict[str, Any]]:
        """Get a contact by ID

        Args:
            contact_id: Contact ID

        Returns:
            Contact dict or None
        """
        for contact in self.contacts:
            if contact.get("id") == contact_id:
                return contact
        return None

    def list_contacts(
        self,
        group: Optional[str] = None,
        tag: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """List contacts with optional filters

        Args:
            group: Filter by group name
            tag: Filter by tag
            search: Search in name or phone

        Returns:
            List of contacts
        """
        result = self.contacts

        if group:
            result = [c for c in result if c.get("group") == group]

        if tag:
            result = [c for c in result if tag in c.get("tags", [])]

        if search:
            search_lower = search.lower()
            result = [
                c for c in result
                if search_lower in c.get("name", "").lower()
                or search_lower in c.get("phone", "").lower()
            ]

        return result

    def get_groups(self) -> List[str]:
        """Get all unique group names

        Returns:
            List of group names
        """
        groups = set()
        for contact in self.contacts:
            if contact.get("group"):
                groups.add(contact["group"])
        return sorted(list(groups))

    def get_tags(self) -> List[str]:
        """Get all unique tags

        Returns:
            List of tags
        """
        tags = set()
        for contact in self.contacts:
            tags.update(contact.get("tags", []))
        return sorted(list(tags))

    def export_contacts(
        self,
        format: str = "json",
        group: Optional[str] = None
    ) -> str:
        """Export contacts to specified format

        Args:
            format: Export format ('json', 'csv', 'vcard')
            group: Optional group filter

        Returns:
            Exported data as string
        """
        contacts = self.list_contacts(group=group)

        if format == "json":
            return json.dumps(contacts, indent=2, ensure_ascii=False)

        elif format == "csv":
            lines = ["name,phone,group,tags"]
            for c in contacts:
                tags = "|".join(c.get("tags", []))
                lines.append(f"{c.get('name')},{c.get('phone')},{c.get('group', '')},{tags}")
            return "\n".join(lines)

        elif format == "vcard":
            vcards = []
            for c in contacts:
                vcard = [
                    "BEGIN:VCARD",
                    "VERSION:3.0",
                    f"FN:{c.get('name')}",
                    f"TEL:{c.get('phone')}",
                ]
                if c.get("group"):
                    vcard.append(f"NOTE;TYPE={c.get('group')}")
                if c.get("tags"):
                    vcard.append(f"TAGS:{','.join(c.get('tags', []))}")
                vcard.append("END:VCARD")
                vcards.append("\n".join(vcard))
            return "\n\n".join(vcards)

        else:
            raise ValueError(f"Unsupported export format: {format}")

    @staticmethod
    def _normalize_phone(phone: str) -> str:
        """Normalize phone number format

        Args:
            phone: Raw phone number

        Returns:
            Normalized phone number
        """
        # Remove all non-digit characters except +
        digits = "".join(c for c in phone if c.isdigit() or c == "+")

        # Ensure starts with country code
        if not digits.startswith("+") and not digits.startswith("00"):
            if len(digits) == 10 or len(digits) == 11:
                digits = "+" + digits

        return digits
