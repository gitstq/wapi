# wapi - WhatsApp Business Automation CLI

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License">
</p>

<p align="center">
  🚀 | YAML驱动的WhatsApp商业自动化工具 | CLI优先 | 零学习成本
</p>

---

## 🎯 项目介绍

**wapi** 是一个面向开发者和企业的WhatsApp Business自动化CLI工具。通过YAML配置文件驱动，实现消息发送、联系人管理、群发自动化、定时任务等功能的命令行操作。

### 🔥 核心价值

- **💬 YAML配置化消息发送** - 告别重复劳动，一键批量发送
- **👥 智能联系人管理** - 分组、标签、搜索，一应俱全
- **⏰ 定时任务自动化** - 设定时间，自动执行
- **🛡️ 防封号策略** - 智能间隔发送，保护账号安全
- **📊 多格式输出** - Terminal表格/JSON/Markdown，灵活展示

### 💡 灵感来源

项目灵感来源于 WhatsApp CLI 社区创新实践，专注于为开发者提供：
- 更强大的YAML配置化能力
- 更完善的联系人管理系统
- 更智能的防封策略
- 更灵活的消息模板引擎

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔐 **WhatsApp Web集成** | 基于Selenium实现，无需额外API |
| 📝 **YAML消息配置** | 支持变量替换的模板消息 |
| 👥 **联系人管理** | 分组、标签、导入导出 |
| 📤 **批量群发** | 支持大规模群发，防封策略 |
| ⏰ **定时任务** | 每日/间隔/自定义调度 |
| 📊 **发送日志** | 完整的消息发送记录 |
| 🎨 **Rich美化输出** | 彩色终端，表格展示 |

---

## 🚀 快速开始

### 📦 安装

```bash
# 从源码安装
git clone https://github.com/gitstq/wapi.git
cd wapi
pip install -e .

# 或者直接安装
pip install wapi
```

### 🔧 环境要求

- Python 3.8+
- Chrome/Firefox 浏览器
- ChromeDriver/GeckoDriver (自动安装)
- 有效的 WhatsApp 账号

### 📋 首次配置

```bash
# 初始化配置目录
wapi config --init
```

### 💬 发送单条消息

```bash
# 发送消息给联系人
wapi send single --to "+8613812345678" --message "Hello from wapi!"

# 使用消息模板
wapi send single --to "+8613812345678" --template greeting
```

### 📤 批量发送

创建消息配置文件 `messages.yaml`:

```yaml
messages:
  - to: "+8613812345678"
    message: "你好，这是一条测试消息"
  - to: "+8613898765432"
    message: "Hello from wapi!"
```

执行批量发送:

```bash
# 预览模式
wapi send batch --file messages.yaml --dry-run

# 实际发送
wapi send batch --file messages.yaml
```

---

## 📖 详细使用指南

### 👥 联系人管理

```bash
# 添加联系人
wapi contact add --name "张三" --phone "+8613812345678" --group "朋友" --tags "重要,工作"

# 查看联系人列表
wapi contact list

# 按分组筛选
wapi contact list --group "朋友"

# 按标签筛选
wapi contact list --tag "重要"

# 删除联系人
wapi contact delete 12345678
```

### 📝 消息模板

```bash
# 创建模板
wapi template create --name "问候" --template "你好 {name}！{message}" --description "通用问候模板"

# 查看所有模板
wapi template list

# 使用模板发送
wapi send single --to "+8613812345678" --message "你好张三！这是模板消息"
```

### ⏰ 定时任务

```bash
# 查看定时任务
wapi schedule list

# 立即执行任务
wapi schedule run 12345678
```

### 🔐 WhatsApp 状态检查

```bash
# 检查连接状态
wapi status
```

---

## 💡 设计思路

### 🎯 设计理念

1. **CLI优先** - 所有功能通过命令行操作，无需图形界面
2. **YAML配置驱动** - 复杂任务通过YAML文件定义，简洁高效
3. **零外部依赖可选** - 核心功能仅需标准库，高级功能按需安装
4. **防封策略内置** - 自动处理发送间隔，降低账号风险

### 🏗️ 技术架构

```
wapi/
├── cli.py              # Click CLI入口
├── core/               # 核心功能模块
│   ├── browser.py      # 浏览器驱动管理
│   ├── sender.py       # 消息发送核心
│   ├── contact.py      # 联系人管理
│   └── scheduler.py    # 定时任务
├── config/             # 配置模块
│   └── loader.py       # 配置加载器
├── templates/          # 消息模板目录
└── logs/               # 发送日志目录
```

### 🔮 后续迭代计划

- [ ] 支持更多消息类型（图片、文件、视频）
- [ ] Web界面管理
- [ ] 多账号支持
- [ ] 云端同步配置
- [ ] API服务模式

---

## 📦 打包与部署

### 🔨 开发安装

```bash
# 克隆项目
git clone https://github.com/gitstq/wapi.git
cd wapi

# 安装依赖
pip install -e ".[dev]"

# 运行测试
pytest tests/
```

### 🐳 Docker部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y chromium && rm -rf /var/lib/apt/lists/*
RUN pip install wapi selenium webdriver-manager

CMD ["wapi", "status"]
```

### 📱 跨平台打包

```bash
# Windows
pyinstaller --onefile --console wapi/cli.py

# macOS/Linux
pyinstaller --onefile --console wapi/cli.py
```

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
