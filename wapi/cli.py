#!/usr/bin/env python3
"""
WAPI CLI - Command Line Interface
"""

import sys
import os
import click
from rich.console import Console
from rich.table import Table
from rich import print as rprint

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from wapi.core.browser import BrowserManager
from wapi.core.sender import MessageSender
from wapi.core.contact import ContactManager
from wapi.core.scheduler import SchedulerManager
from wapi.config.loader import ConfigLoader

console = Console()


@click.group()
@click.version_option(version="1.0.0")
def main():
    """WAPI - WhatsApp Business Automation CLI

    A YAML-driven WhatsApp messaging automation tool for developers and businesses.
    """
    pass


@main.group()
def send():
    """Send messages via WhatsApp"""
    pass


@send.command()
@click.option("--to", "-t", required=True, help="Recipient phone number or contact name")
@click.option("--message", "-m", required=True, help="Message content")
@click.option("--template", "-tp", help="Use message template from config")
def single(to, message, template):
    """Send a single message"""
    console.print(f"[green]Sending message to {to}...[/green]")
    try:
        sender = MessageSender()
        success = sender.send_single(to, message)
        if success:
            console.print(f"[bold green]Message sent successfully![/bold green]")
        else:
            console.print(f"[bold red]Failed to send message[/bold red]")
            sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@send.command()
@click.option("--file", "-f", required=True, type=click.Path(exists=True), help="YAML file with messages")
@click.option("--dry-run", is_flag=True, help="Preview without sending")
def batch(file, dry_run):
    """Send batch messages from YAML file"""
    console.print(f"[cyan]Loading messages from {file}...[/cyan]")
    try:
        config = ConfigLoader.load_batch(file)
        messages = config.get("messages", [])

        if dry_run:
            console.print(f"[yellow]DRY RUN - Previewing {len(messages)} messages:[/yellow]")
            for i, msg in enumerate(messages, 1):
                console.print(f"\n{i}. To: {msg.get('to', 'N/A')}")
                console.print(f"   Message: {msg.get('message', 'N/A')[:50]}...")
            return

        sender = MessageSender()
        success_count = 0
        for i, msg in enumerate(messages, 1):
            console.print(f"[cyan]Sending {i}/{len(messages)}...[/cyan]")
            if sender.send_single(msg["to"], msg["message"]):
                success_count += 1

        console.print(f"[bold green]Completed: {success_count}/{len(messages)} messages sent[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@main.group()
def contact():
    """Manage contacts"""
    pass


@contact.command("add")
@click.option("--name", "-n", required=True, help="Contact name")
@click.option("--phone", "-p", required=True, help="Phone number")
@click.option("--group", "-g", help="Contact group")
@click.option("--tags", "-t", help="Comma-separated tags")
def contact_add(name, phone, group, tags):
    """Add a new contact"""
    try:
        manager = ContactManager()
        contact_id = manager.add_contact(name, phone, group, tags.split(",") if tags else [])
        console.print(f"[bold green]Contact added: {name} (ID: {contact_id})[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@contact.command("list")
@click.option("--group", "-g", help="Filter by group")
@click.option("--tag", "-t", help="Filter by tag")
@click.option("--format", "-f", type=click.Choice(["table", "json"]), default="table", help="Output format")
def contact_list(group, tag, format):
    """List all contacts"""
    try:
        manager = ContactManager()
        contacts = manager.list_contacts(group=group, tag=tag)

        if format == "json":
            import json
            console.print(json.dumps(contacts, indent=2))
        else:
            table = Table(title="Contacts")
            table.add_column("ID", style="cyan")
            table.add_column("Name", style="green")
            table.add_column("Phone", style="yellow")
            table.add_column("Group", style="magenta")
            table.add_column("Tags", style="blue")

            for c in contacts:
                table.add_row(
                    str(c.get("id", "")),
                    c.get("name", ""),
                    c.get("phone", ""),
                    c.get("group", "") or "-",
                    ", ".join(c.get("tags", [])) or "-"
                )
            console.print(table)
            console.print(f"\n[cyan]Total: {len(contacts)} contacts[/cyan]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@contact.command("delete")
@click.argument("contact_id", type=int)
def contact_delete(contact_id):
    """Delete a contact by ID"""
    try:
        manager = ContactManager()
        if manager.delete_contact(contact_id):
            console.print(f"[bold green]Contact {contact_id} deleted[/bold green]")
        else:
            console.print(f"[bold red]Contact {contact_id} not found[/bold red]")
            sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@main.group()
def template():
    """Manage message templates"""
    pass


@template.command("list")
def template_list():
    """List all message templates"""
    try:
        templates = ConfigLoader.load_templates()
        table = Table(title="Message Templates")
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="green")
        table.add_column("Variables", style="yellow")

        for name, tmpl in templates.items():
            variables = ", ".join(tmpl.get("variables", []))
            desc = tmpl.get("description", "")[:50]
            table.add_row(name, desc, variables)

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@template.command("create")
@click.option("--name", "-n", required=True, help="Template name")
@click.option("--template", "-t", required=True, help="Template text with {variable} placeholders")
@click.option("--description", "-d", help="Template description")
def template_create(name, template, description):
    """Create a new message template"""
    try:
        import re
        variables = re.findall(r'\{(\w+)\}', template)

        ConfigLoader.save_template(name, {
            "template": template,
            "description": description or "",
            "variables": variables
        })
        console.print(f"[bold green]Template '{name}' created with variables: {variables}[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@main.group()
def schedule():
    """Manage scheduled tasks"""
    pass


@schedule.command("list")
def schedule_list():
    """List all scheduled tasks"""
    try:
        manager = SchedulerManager()
        tasks = manager.list_tasks()

        if not tasks:
            console.print("[yellow]No scheduled tasks[/yellow]")
            return

        table = Table(title="Scheduled Tasks")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Schedule", style="yellow")
        table.add_column("Status", style="magenta")
        table.add_column("Next Run", style="blue")

        for task in tasks:
            status_color = "green" if task.get("enabled") else "red"
            table.add_row(
                str(task.get("id", "")),
                task.get("name", ""),
                task.get("schedule", ""),
                f"[{status_color}]{'Enabled' if task.get('enabled') else 'Disabled'}[/{status_color}]",
                task.get("next_run", "N/A") or "N/A"
            )

        console.print(table)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@schedule.command("run")
@click.argument("task_id", type=int)
def schedule_run(task_id):
    """Run a scheduled task immediately"""
    try:
        manager = SchedulerManager()
        if manager.run_task(task_id):
            console.print(f"[bold green]Task {task_id} executed successfully[/bold green]")
        else:
            console.print(f"[bold red]Task {task_id} not found or failed[/bold red]")
            sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@main.command()
def status():
    """Check WhatsApp Web connection status"""
    try:
        browser = BrowserManager()
        driver = browser.get_driver()

        console.print("[cyan]Navigating to WhatsApp Web...[/cyan]")
        driver.get("https://web.whatsapp.com")

        console.print("[yellow]Please scan the QR code if not already logged in.[/yellow]")
        console.print("[yellow]Press Enter when ready to continue...[/yellow]")
        input()

        # Check if logged in
        try:
            driver.find_element("xpath", '//div[@data-testid="chat-list"]')
            console.print("[bold green]WhatsApp Web is connected![/bold green]")
        except:
            console.print("[bold red]Not connected. Please scan the QR code.[/bold red]")
            sys.exit(1)

        browser.quit()
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        sys.exit(1)


@main.command()
@click.option("--init", is_flag=True, help="Initialize configuration directory")
def config(init):
    """Manage WAPI configuration"""
    if init:
        config_dir = os.path.expanduser("~/.wapi")
        os.makedirs(config_dir, exist_ok=True)
        os.makedirs(os.path.join(config_dir, "templates"), exist_ok=True)
        os.makedirs(os.path.join(config_dir, "logs"), exist_ok=True)
        console.print(f"[bold green]Configuration directory created: {config_dir}[/bold green]")
    else:
        config_dir = os.path.expanduser("~/.wapi")
        console.print(f"Configuration directory: {config_dir}")
        console.print(f"Config file: {os.path.join(config_dir, 'config.yaml')}")
        console.print(f"Templates: {os.path.join(config_dir, 'templates')}")
        console.print(f"Logs: {os.path.join(config_dir, 'logs')}")


if __name__ == "__main__":
    main()
