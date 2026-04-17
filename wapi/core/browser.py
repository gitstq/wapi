#!/usr/bin/env python3
"""
Browser Manager - WhatsApp Web driver management
"""

import os
import sys
import time
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


class BrowserManager:
    """Manages browser instances for WhatsApp Web automation"""

    def __init__(self, browser: str = "chrome", headless: bool = False):
        """Initialize browser manager

        Args:
            browser: Browser to use ('chrome' or 'firefox')
            headless: Run browser in headless mode
        """
        self.browser = browser.lower()
        self.headless = headless
        self.driver: Optional[webdriver.Chrome] = None

    def _get_chrome_options(self) -> Options:
        """Get Chrome options"""
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1280,720")
        options.add_argument("--user-data-dir=/tmp/whatsapp-data")
        # Anti-detection
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)
        return options

    def get_driver(self) -> webdriver.Chrome:
        """Get or create WebDriver instance"""
        if self.driver is None:
            if self.browser == "chrome":
                options = self._get_chrome_options()
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=options)
            elif self.browser == "firefox":
                service = Service(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service)
                if self.headless:
                    self.driver.headless = True
            else:
                raise ValueError(f"Unsupported browser: {self.browser}")

            # Anti-detection
            self.driver.execute_script(
                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
            )

        return self.driver

    def open_whatsapp(self, wait_for_login: bool = True, timeout: int = 60) -> bool:
        """Open WhatsApp Web and optionally wait for login

        Args:
            wait_for_login: Wait for user to scan QR code
            timeout: Timeout in seconds for waiting

        Returns:
            True if successfully logged in
        """
        driver = self.get_driver()
        driver.get("https://web.whatsapp.com")

        if wait_for_login:
            try:
                # Wait for chat list to appear (indicates logged in)
                WebDriverWait(driver, timeout).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@data-testid="chat-list"]'))
                )
                return True
            except:
                return False
        return True

    def find_chat(self, contact_name: str) -> Optional[object]:
        """Find a chat by contact name

        Args:
            contact_name: Name or phone number to search

        Returns:
            Chat element or None
        """
        driver = self.get_driver()

        # Search box
        try:
            search_box = driver.find_element(By.XPATH, '//div[@data-testid="chat-list-search"]')
            search_box.click()
            search_box.clear()
            search_box.send_keys(contact_name)
            time.sleep(1)

            # Find chat
            chat = driver.find_element(
                By.XPATH,
                f'//span[contains(@title,"{contact_name}")]'
            )
            chat.click()
            return chat
        except Exception as e:
            print(f"Chat not found: {e}")
            return None

    def send_message(self, message: str) -> bool:
        """Send message in the currently opened chat

        Args:
            message: Message text to send

        Returns:
            True if message sent successfully
        """
        driver = self.get_driver()

        try:
            # Find message input box
            msg_box = driver.find_element(
                By.XPATH,
                '//footer//div[@contenteditable="true"][@data-tab="10"]'
            )
            msg_box.click()

            # Type message with small delays to avoid detection
            for char in message:
                msg_box.send_keys(char)
                time.sleep(0.01)

            time.sleep(0.1)

            # Find and click send button
            send_btn = driver.find_element(
                By.XPATH,
                '//button[@data-testid="send"]'
            )
            send_btn.click()

            return True
        except Exception as e:
            print(f"Failed to send message: {e}")
            return False

    def quit(self):
        """Close browser and cleanup"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.quit()
