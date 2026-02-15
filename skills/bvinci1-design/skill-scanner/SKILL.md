---
name: skill-scanner
description: 在安装 Clawdbot 和 MCP 之前，请扫描它们以检测是否存在恶意软件、间谍软件、加密矿工程序以及恶意代码模式。该安全审计工具能够识别数据泄露、系统篡改尝试、后门程序以及混淆技术。
---

# 技能扫描器（Skill Scanner）

这是一个用于检测 Clawdbot/MCP 技能中的安全威胁的工具，能够识别恶意软件、间谍软件、加密挖矿行为以及其他恶意活动。

## 功能
- 扫描技能文件夹以发现安全威胁
- 检测数据泄露的迹象
- 识别系统被篡改的尝试
- 发现加密挖矿的迹象
- 标记任意代码执行的风险
- 查找后门和混淆技术
- 以 Markdown 或 JSON 格式输出报告
- 通过 Streamlit 提供 Web 用户界面

## 使用方法

### 命令行
```bash
python skill_scanner.py /path/to/skill-folder
```

### 在 Clawdbot 内部使用
```
"Scan the [skill-name] skill for security issues using skill-scanner"
"Use skill-scanner to check the youtube-watcher skill"
"Run a security audit on the remotion skill"
```

### Web 用户界面
```bash
pip install streamlit
streamlit run streamlit_ui.py
```

## 系统要求
- Python 3.7 及以上版本
- 无需额外依赖（仅使用 Python 标准库）
- Streamlit（可选，用于 Web 用户界面）

## 入口点
- **命令行界面：** `skill_scanner.py`
- **Web 用户界面：** `streamlit_ui.py`

## 关键标签
#安全 #恶意软件 #间谍软件 #加密挖矿 #扫描器 #审计 #代码分析 #MCP #Clawdbot #代理技能 #安全性 #威胁检测 #漏洞