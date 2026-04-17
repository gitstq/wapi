#!/usr/bin/env python3
"""
Message Sender - Core message sending functionality
"""

import time
import random
from typing import Optional, Dict, Any

from .browser import BrowserManager
from ..config.loader import ConfigLoader


class MessageSender:
    """Handles message sending operations with anti-ban strategies"""

    def __init__(self, browser: str = "chrome", headless: bool = False):
        """Initialize message sender

        Args:
            browser: Browser to use
            headless: Run in headless mode
        """
        self.browser_manager = BrowserManager(browser=browser, headless=headless)
        self.config = ConfigLoader.load_config()
        self.stats = {
            "sent": 0,
            "failed": 0,
            "total_messages": 0
        }

    def send_single(self, recipient: str, message: str, delay: Optional[int] = None) -> bool:
        """Send a single message to a recipient

        Args:
            recipient: Phone number or contact name
            message: Message content
            delay: Optional delay in seconds before sending

        Returns:
            True if message sent successfully
        """
        try:
            # Check daily limit
            if self._check_daily_limit():
                print("Daily message limit reached. Please wait.")
                return False

            # Optional delay
            if delay:
                time.sleep(delay)

            # Open WhatsApp Web
            if not self.browser_manager.open_whatsapp(wait_for_login=True):
                print("Failed to connect to WhatsApp Web")
                return False

            # Find the chat
            chat = self.browser_manager.find_chat(recipient)
            if not chat:
                print(f"Contact '{recipient}' not found")
                return False

            # Send message with anti-ban delay
            min_delay = self.config.get("anti_ban", {}).get("min_interval", 5)
            max_delay = self.config.get("anti_ban", {}).get("max_interval", 15)
            time.sleep(random.uniform(min_delay, max_delay))

            success = self.browser_manager.send_message(message)

            if success:
                self.stats["sent"] += 1
                self._log_message(recipient, message)
            else:
                self.stats["failed"] += 1

            self.stats["total_messages"] += 1
            return success

        except Exception as e:
            print(f"Error sending message: {e}")
            self.stats["failed"] += 1
            return False

    def send_to_group(self, group_name: str, message: str) -> bool:
        """Send message to a group

        Args:
            group_name: Name of the group
            message: Message content

        Returns:
            True if message sent successfully
        """
        return self.send_single(group_name, message)

    def send_batch(
        self,
        recipients: list,
        message: str,
        use_delay: bool = True,
        min_interval: int = 5,
        max_interval: int = 15
    ) -> Dict[str, int]:
        """Send batch messages to multiple recipients

        Args:
            recipients: List of phone numbers or contact names
            message: Message content
            use_delay: Use random delay between messages
            min_interval: Minimum delay in seconds
            max_interval: Maximum delay in seconds

        Returns:
            Statistics dict with sent/failed counts
        """
        results = {"sent": 0, "failed": 0}

        for i, recipient in enumerate(recipients, 1):
            print(f"Sending to {recipient} ({i}/{len(recipients)})...")

            # Check daily limit
            if self._check_daily_limit():
                print("Daily limit reached. Stopping batch.")
                break

            success = self.send_single(recipient, message)
            if success:
                results["sent"] += 1
            else:
                results["failed"] += 1

            # Delay between messages
            if use_delay and i < len(recipients):
                delay = random.uniform(min_interval, max_interval)
                print(f"Waiting {delay:.1f}s before next message...")
                time.sleep(delay)

        return results

    def _check_daily_limit(self) -> bool:
        """Check if daily message limit is reached"""
        daily_limit = self.config.get("anti_ban", {}).get("daily_limit", 50)
        return self.stats["total_messages"] >= daily_limit

    def _log_message(self, recipient: str, message: str):
        """Log sent message to file"""
        from ..config.loader import ConfigLoader
        import json
        from datetime import datetime

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "recipient": recipient,
            "message": message,
            "status": "sent"
        }

        log_file = ConfigLoader.get_log_file()
        logs = []

        # Read existing logs
        if log_file.exists():
            try:
                logs = json.loads(log_file.read_text())
            except:
                logs = []

        logs.append(log_entry)

        # Keep last 1000 entries
        logs = logs[-1000:]

        # Write back
        log_file.write_text(json.dumps(logs, indent=2, ensure_ascii=False))

    def get_stats(self) -> Dict[str, int]:
        """Get sending statistics"""
        return self.stats.copy()

    def close(self):
        """Close the browser"""
        self.browser_manager.quit()
