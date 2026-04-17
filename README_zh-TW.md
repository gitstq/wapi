# wapi - WhatsApp 商務自動化 CLI 工具

<p align="center">

🌐 **語言切換**：[English](README.md) | [简体中文](README_zh-CN.md) | [繁體中文](README_zh-TW.md)

</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="版本">
  <img src="https://img.shields.io/badge/python-3.8+-green.svg" alt="Python">
  <img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="授權">
</p>

<p align="center">
  🚀 | YAML驅動的WhatsApp商務自動化工具 | CLI優先 | 零學習成本
</p>

---

## 🎯 專案介紹

**wapi** 是一個面向開發者和企業的WhatsApp Business自動化CLI工具。透過YAML設定檔案驅動，實現訊息傳送、聯絡人管理、群發自動化、定時任務等功能的命令列操作。

### 🔥 核心價值

- **💬 YAML設定化訊息傳送** - 告別重複勞動，一鍵批量傳送
- **👥 智慧聯絡人管理** - 分組、標籤、搜尋，一應俱全
- **⏰ 定時任務自動化** - 設定時間，自動執行
- **🛡️ 防封號策略** - 智慧間隔傳送，保護帳號安全
- **📊 多格式輸出** - Terminal表格/JSON/Markdown，靈活展示

### 💡 靈感來源

專案靈感來源於 WhatsApp CLI 社群創新實踐，專注於為開發者提供：
- 更強大的YAML設定化能力
- 更完善的聯絡人管理系統
- 更智慧的防封策略
- 更靈活的訊息範本引擎

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔐 **WhatsApp Web整合** | 基於Selenium實現，無需額外API |
| 📝 **YAML訊息設定** | 支援變數替換的範本訊息 |
| 👥 **聯絡人管理** | 分組、標籤、匯入匯出 |
| 📤 **批量群發** | 支援大規模群發，防封策略 |
| ⏰ **定時任務** | 每日/間隔/自定義調度 |
| 📊 **傳送日誌** | 完整的訊息傳送記錄 |
| 🎨 **Rich美化輸出** | 彩色終端，表格展示 |

---

## 🚀 快速開始

### 📦 安裝

```bash
# 從原始碼安裝
git clone https://github.com/gitstq/wapi.git
cd wapi
pip install -e .

# 或者直接安裝
pip install wapi
```

### 🔧 環境要求

- Python 3.8+
- Chrome/Firefox 瀏覽器
- ChromeDriver/GeckoDriver (自動安裝)
- 有效的 WhatsApp 帳號

### 📋 首次設定

```bash
# 初始化設定目錄
wapi config --init
```

### 💬 傳送單條訊息

```bash
# 傳送訊息給聯絡人
wapi send single --to "+8613812345678" --message "你好！這是wapi傳送的訊息"

# 使用訊息範本
wapi send single --to "+8613812345678" --template greeting
```

### 📤 批量傳送

建立訊息設定檔案 `messages.yaml`:

```yaml
messages:
  - to: "+8613812345678"
    message: "你好，這是一條測試訊息"
  - to: "+8613898765432"
    message: "Hello from wapi!"
```

執行批量傳送:

```bash
# 預覽模式
wapi send batch --file messages.yaml --dry-run

# 實際傳送
wapi send batch --file messages.yaml
```

---

## 📖 詳細使用指南

### 👥 聯絡人管理

```bash
# 新增聯絡人
wapi contact add --name "張三" --phone "+8613812345678" --group "朋友" --tags "重要,工作"

# 檢視聯絡人列表
wapi contact list

# 按分組篩選
wapi contact list --group "朋友"

# 按標籤篩選
wapi contact list --tag "重要"

# 刪除聯絡人
wapi contact delete 12345678
```

### 📝 訊息範本

```bash
# 建立範本
wapi template create --name "問候" --template "你好 {name}！{message}" --description "通用問候範本"

# 檢視所有範本
wapi template list

# 使用範本傳送
wapi send single --to "+8613812345678" --message "你好張三！這是範本訊息"
```

### ⏰ 定時任務

```bash
# 檢視定時任務
wapi schedule list

# 立即執行任務
wapi schedule run 12345678
```

### 🔐 WhatsApp 狀態檢查

```bash
# 檢查連線狀態
wapi status
```

---

## 💡 設計思路

### 🎯 設計理念

1. **CLI優先** - 所有功能透過命令列操作，無需圖形介面
2. **YAML設定驅動** - 複雜任務透過YAML檔案定義，簡潔高效
3. **零外部依賴可選** - 核心功能僅需標準庫，高級功能按需安裝
4. **防封策略內建** - 自動處理傳送間隔，降低帳號風險

### 🏗️ 技術架構

```
wapi/
├── cli.py              # Click CLI入口
├── core/               # 核心功能模組
│   ├── browser.py      # 瀏览器驅動管理
│   ├── sender.py       # 訊息傳送核心
│   ├── contact.py      # 聯絡人管理
│   └── scheduler.py    # 定時任務
├── config/             # 設定模組
│   └── loader.py       # 設定載入器
├── templates/          # 訊息範本目錄
└── logs/               # 傳送日誌目錄
```

### 🔮 後續迭代計畫

- [ ] 支援更多訊息類型（圖片、檔案、影片）
- [ ] Web介面管理
- [ ] 多帳號支援
- [ ] 雲端同步設定
- [ ] API服務模式

---

## 📦 打包與部署

### 🔨 開發安裝

```bash
# 克隆專案
git clone https://github.com/gitstq/wapi.git
cd wapi

# 安裝依賴
pip install -e ".[dev]"

# 執行測試
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

## 🤝 貢獻指南

歡迎提交Issue和Pull Request！

1. Fork 本倉庫
2. 建立特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送至分支 (`git push origin feature/AmazingFeature`)
5. 建立Pull Request

---

## 📄 開源協議

本專案採用 [MIT License](LICENSE) 開源協議。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
