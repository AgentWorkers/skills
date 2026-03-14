---
name: scraper
description: **结构化提取与清洗工具**：适用于公开网页及用户授权访问的网页。当用户需要从这些网页中收集、整理、汇总或转换内容，并将其转化为可重用的文本或数据时，可使用该工具。**请注意**：该工具仅用于合法、合规的目的，不得用于绕过登录系统、支付墙、验证码、机器人限制或访问控制机制。**输出结果仅限于本地使用。**
---
# Scraper

将杂乱无章的公共页面转换成结构清晰、可重复使用的数据。

## 核心功能
Scraper 是一种用于提取公共页面数据的工具，适用于用户授权的页面。它可以帮助代理执行以下操作：
- 从指定 URL 获取页面内容
- 提取可读的文本
- 尽可能去除冗余的模板代码
- 将处理后的数据保存到本地
- 为后续的总结或分析做好准备

## 安全限制
- 仅适用于公共页面或用户授权的页面
- 不得绕过登录机制、付费墙、验证码、机器人限制或速率限制
- 不得请求或存储用户的凭证信息
- 不得进行隐秘的爬取行为、创建新账户或伪装用户身份
- 数据仅保存在本地

## 运行时要求
- 必须安装 Python 3，并确保其可被识别为 `python3`
- 不需要额外的第三方库

## 本地存储
所有处理后的数据会保存在以下本地路径：
- `~/.openclaw/workspace/memory/scraper/jobs.json`
- `~/.openclaw/workspace/memory/scraper/output/`

## 主要工作流程
- **抓取页面**: `fetch_page.py --url "https://example.com"`
- **提取可读文本**: `extract_text.py --url "https://example.com"`
- **保存处理后的数据**: `save_output.py --url "https://example.com" --title "Example"`
- **列出之前的抓取任务**: `list_jobs.py`

## 脚本说明
| 脚本 | 功能 |
|---|---|
| `init_storage.py` | 初始化数据存储结构 |
| `fetch_page.py` | 使用标准请求头下载页面内容 |
| `extract_text.py` | 将 HTML 页面转换为纯文本 |
| `save_output.py` | 保存提取的数据并记录抓取任务 |
| `list_jobs.py` | 显示之前的抓取任务记录 |