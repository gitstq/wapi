#!/usr/bin/env python3
"""Scheduler Manager - Schedule and manage automated tasks"""

import json
import uuid
import time
import threading
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta

from ..config.loader import ConfigLoader


class SchedulerManager:
    """Manages scheduled messaging tasks"""

    def __init__(self):
        """Initialize scheduler manager"""
        self.tasks_file = ConfigLoader.get_tasks_file()
        self.tasks: List[Dict[str, Any]] = []
        self.running = False
        self._thread = None
        self._load_tasks()

    def _load_tasks(self):
        """Load tasks from file"""
        if self.tasks_file.exists():
            try:
                self.tasks = json.loads(self.tasks_file.read_text(encoding="utf-8"))
            except:
                self.tasks = []
        else:
            self.tasks = []

    def _save_tasks(self):
        """Save tasks to file"""
        self.tasks_file.parent.mkdir(parents=True, exist_ok=True)
        self.tasks_file.write_text(json.dumps(self.tasks, indent=2, ensure_ascii=False), encoding="utf-8")

    def create_task(self, name: str, message: str, recipients: List[str],
                    schedule_type: str, schedule_value: str, enabled: bool = True) -> str:
        """Create a new scheduled task"""
        task_id = str(uuid.uuid4())[:8]
        task = {
            "id": task_id,
            "name": name,
            "message": message,
            "recipients": recipients,
            "schedule_type": schedule_type,
            "schedule_value": schedule_value,
            "enabled": enabled,
            "created_at": datetime.now().isoformat(),
            "last_run": None,
            "next_run": self._calculate_next_run(schedule_type, schedule_value),
            "run_count": 0
        }
        self.tasks.append(task)
        self._save_tasks()
        return task_id

    def update_task(self, task_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing task"""
        for task in self.tasks:
            if task.get("id") == task_id:
                task.update(updates)
                self._save_tasks()
                return True
        return False

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID"""
        original_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t.get("id") != task_id]
        if len(self.tasks) < original_count:
            self._save_tasks()
            return True
        return False

    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Get a task by ID"""
        for task in self.tasks:
            if task.get("id") == task_id:
                return task
        return None

    def list_tasks(self) -> List[Dict[str, Any]]:
        """List all tasks"""
        return self.tasks.copy()

    def run_task(self, task_id: str) -> bool:
        """Execute a task immediately"""
        task = self.get_task(task_id)
        if not task:
            return False
        try:
            from ..core.sender import MessageSender
            sender = MessageSender()
            for recipient in task["recipients"]:
                sender.send_single(recipient, task["message"])
            task["last_run"] = datetime.now().isoformat()
            task["run_count"] = task.get("run_count", 0) + 1
            self._save_tasks()
            return True
        except Exception as e:
            print(f"Error running task: {e}")
            return False

    def start(self):
        """Start the scheduler background thread"""
        if self.running:
            return
        self.running = True
        self._thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._thread.start()

    def stop(self):
        """Stop the scheduler background thread"""
        self.running = False

    def _run_scheduler(self):
        """Background scheduler loop"""
        while self.running:
            time.sleep(1)

    def _calculate_next_run(self, schedule_type: str, schedule_value: str) -> Optional[str]:
        """Calculate next run time for a task"""
        now = datetime.now()
        if schedule_type == "daily":
            try:
                hour, minute = map(int, schedule_value.split(":"))
                next_run = now.replace(hour=hour, minute=minute, second=0)
                if next_run <= now:
                    next_run += timedelta(days=1)
                return next_run.isoformat()
            except:
                return None
        elif schedule_type == "interval":
            try:
                minutes = int(schedule_value)
                return (now + timedelta(minutes=minutes)).isoformat()
            except:
                return None
        return None
