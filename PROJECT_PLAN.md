# 项目自研方案：wapi - WhatsApp Business API CLI

## 1. 项目概述

**项目名称**: wapi (WhatsApp API CLI)  
**项目定位**: 面向开发者和企业的WhatsApp Business自动化CLI工具  
**核心价值**: 通过YAML配置驱动，实现WhatsApp消息发送、联系人管理、群发自动化等功能  
**灵感来源**: 参考steipete/wacli的WhatsApp CLI思路，做差异化扩展

## 2. 差异化分析

| 功能维度 | 参考项目(wacli) | 自研项目(wapi) |
|---------|----------------|---------------|
| 消息发送 | 仅基础发送 | 支持YAML配置化消息模板 |
| 自动化 | 无 | 支持定时任务、触发式自动化 |
| 联系人管理 | 无 | 内置联系人分组、标签管理 |
| 群发支持 | 无 | 支持大规模群发+防封策略 |
| 输出格式 | 仅文本 | terminal/JSON/Markdown多格式 |

## 3. 技术栈选型

```
语言: Python 3.8+
核心依赖:
  - selenium (浏览器自动化)
  - webdriver-manager (驱动管理)
  - pyyaml (YAML配置解析)
  - schedule (定时任务)
  - click (CLI框架)
  - rich (美化输出)
零外部依赖目标: 否 (需selenium)
```

## 4. 核心功能清单

### 4.1 核心模块
- [ ] `wapi send` - 发送单条/批量消息
- [ ] `wapi contact add/list/delete` - 联系人管理
- [ ] `wapi group send` - 群发消息
- [ ] `wapi template list/create` - 消息模板管理
- [ ] `wapi schedule create/list` - 定时任务管理
- [ ] `wapi status` - 连接状态检查

### 4.2 配置模块
- [ ] YAML配置文件支持 (config.yaml)
- [ ] 消息模板配置 (templates/)
- [ ] 联系人数据存储 (contacts.json)
- [ ] 发送日志记录 (logs/)

### 4.3 防封策略
- [ ] 发送间隔随机化
- [ ] 每日发送上限配置
- [ ] 自动冷却机制

## 5. 技术架构

```
wapi/
├── __init__.py
├── cli.py              # Click CLI入口
├── core/
│   ├── __init__.py
│   ├── browser.py      # 浏览器驱动管理
│   ├── sender.py       # 消息发送核心
│   ├── contact.py      # 联系人管理
│   └── scheduler.py    # 定时任务
├── config/
│   ├── __init__.py
│   └── loader.py       # 配置加载器
├── templates/          # 消息模板
├── logs/               # 发送日志
├── data/
│   └── contacts.json   # 联系人数据
├── tests/
│   └── test_*.py       # 单元测试
├── pyproject.toml
├── README.md
└── README_zh-TW.md
```

## 6. 自测标准

1. **CLI功能测试**: 所有子命令可正常执行
2. **YAML配置解析**: 模板文件可正确加载
3. **浏览器自动化**: WhatsApp Web可正常登录
4. **消息发送**: 单条消息可成功发送
5. **联系人管理**: CRUD操作正常工作
6. **防封策略**: 间隔和上限配置生效

## 7. 环境要求

- Python 3.8+
- Chrome/Firefox浏览器
- ChromeDriver/GeckoDriver
- 有效的WhatsApp账号
