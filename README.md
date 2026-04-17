# wapi - WhatsApp Business Automation CLI

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
</p>

<p align="center">
  🚀 | YAML-driven WhatsApp Business Automation | CLI-first | Zero Learning Curve
</p>

---

## 🎯 Introduction

**wapi** is a powerful WhatsApp Business automation CLI tool designed for developers and businesses. Using YAML configuration files as the driving force, it enables command-line operations for message sending, contact management, mass broadcasting, scheduled tasks, and more.

### 🔥 Core Value

- **💬 YAML-configured Message Sending** - Say goodbye to repetitive work, batch send with one click
- **👥 Smart Contact Management** - Groups, tags, and search - all you need
- **⏰ Automated Scheduled Tasks** - Set it and forget it
- **🛡️ Anti-ban Strategy** - Intelligent sending intervals to protect your account
- **📊 Multiple Output Formats** - Terminal table/JSON/Markdown, flexible display

### 💡 Inspiration

Inspired by WhatsApp CLI community innovations, focusing on providing developers with:
- More powerful YAML configuration capabilities
- More complete contact management system
- Smarter anti-ban strategies
- More flexible message template engine

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 **WhatsApp Web Integration** | Selenium-based, no extra API required |
| 📝 **YAML Message Config** | Template messages with variable substitution |
| 👥 **Contact Management** | Groups, tags, import/export |
| 📤 **Mass Broadcasting** | Large-scale sending with anti-ban strategy |
| ⏰ **Scheduled Tasks** | Daily/interval/custom scheduling |
| 📊 **Send Logs** | Complete message sending records |
| 🎨 **Rich Beautified Output** | Colorful terminal, table display |

---

## 🚀 Quick Start

### 📦 Installation

```bash
# Install from source
git clone https://github.com/gitstq/wapi.git
cd wapi
pip install -e .

# Or install directly
pip install wapi
```

### 🔧 Requirements

- Python 3.8+
- Chrome/Firefox browser
- ChromeDriver/GeckoDriver (auto-installed)
- Valid WhatsApp account

### 📋 Initial Setup

```bash
# Initialize config directory
wapi config --init
```

### 💬 Send a Single Message

```bash
# Send message to a contact
wapi send single --to "+8613812345678" --message "Hello from wapi!"

# Use message template
wapi send single --to "+8613812345678" --template greeting
```

### 📤 Batch Sending

Create message config file `messages.yaml`:

```yaml
messages:
  - to: "+8613812345678"
    message: "Hello, this is a test message"
  - to: "+8613898765432"
    message: "Greetings from wapi!"
```

Execute batch sending:

```bash
# Preview mode
wapi send batch --file messages.yaml --dry-run

# Actual sending
wapi send batch --file messages.yaml
```

---

## 📖 Detailed Usage Guide

### 👥 Contact Management

```bash
# Add contact
wapi contact add --name "John" --phone "+8613812345678" --group "Friends" --tags "Important,Work"

# List contacts
wapi contact list

# Filter by group
wapi contact list --group "Friends"

# Filter by tag
wapi contact list --tag "Important"

# Delete contact
wapi contact delete 12345678
```

### 📝 Message Templates

```bash
# Create template
wapi template create --name "greeting" --template "Hello {name}! {message}" --description "General greeting template"

# List all templates
wapi template list

# Send using template
wapi send single --to "+8613812345678" --message "Hello John! This is a template message"
```

### ⏰ Scheduled Tasks

```bash
# List scheduled tasks
wapi schedule list

# Run task immediately
wapi schedule run 12345678
```

### 🔐 WhatsApp Status Check

```bash
# Check connection status
wapi status
```

---

## 💡 Design Philosophy

### 🎯 Core Principles

1. **CLI-first** - All features operated via command line, no GUI required
2. **YAML-driven** - Complex tasks defined in YAML files, simple and efficient
3. **Zero external dependencies (optional)** - Core features only need standard library
4. **Built-in anti-ban strategy** - Auto-handles sending intervals to reduce account risk

### 🏗️ Technical Architecture

```
wapi/
├── cli.py              # Click CLI entry point
├── core/               # Core functionality modules
│   ├── browser.py      # Browser driver management
│   ├── sender.py       # Message sending core
│   ├── contact.py      # Contact management
│   └── scheduler.py    # Scheduled tasks
├── config/             # Configuration module
│   └── loader.py       # Config loader
├── templates/          # Message template directory
└── logs/               # Send log directory
```

### 🔮 Future Roadmap

- [ ] Support more message types (images, files, videos)
- [ ] Web interface management
- [ ] Multi-account support
- [ ] Cloud sync configuration
- [ ] API service mode

---

## 📦 Packaging & Deployment

### 🔨 Development Installation

```bash
# Clone project
git clone https://github.com/gitstq/wapi.git
cd wapi

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### 🐳 Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y chromium && rm -rf /var/lib/apt/lists/*
RUN pip install wapi selenium webdriver-manager

CMD ["wapi", "status"]
```

### 📱 Cross-platform Packaging

```bash
# Windows
pyinstaller --onefile --console wapi/cli.py

# macOS/Linux
pyinstaller --onefile --console wapi/cli.py
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
