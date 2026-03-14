---
name: fetch
description: 这是一个用于公开网页内容的检索与清洗的引擎。用户可以在需要从公开网址获取、下载、查看、清洗或保存内容时使用该工具。它支持安全地获取公开网页信息，能够提取页面标题、文本和链接，并将结果存储在本地；同时会记录所有的操作历史记录。该引擎无需任何用户名或密码，无需登录流程，也不支持与云端的同步。
---
# 数据获取（Fetch）

将公共 URL 转换为可使用的本地内容。

## 核心原则
1. 仅获取公共网页内容。
2. 优先选择格式清晰、易于处理的提取文本，而非包含大量杂乱信息的原始 HTML。
3. 将原始响应和提取后的结构化数据都保存到本地。
4. 保持简单的本地作业记录，以便随时查看之前的获取操作。

## 运行时要求
- 必须安装 Python 3，并确保其可被识别为 `python3`。
- 不需要任何外部包。

## 安全限制
- 仅处理公共 URL。
- 不涉及登录流程。
- 不使用 cookies 或浏览器自动化工具。
- 不需要 API 密钥或凭证。
- 不进行外部上传或云同步。
- 所有获取的数据仅存储在本地。

## 本地存储位置
所有数据存储在以下路径：
- `~/.openclaw/workspace/memory/fetch/jobs.json`
- `~/.openclaw/workspace/memory/fetch/pages/`

## 主要工作流程
- **获取 URL**: `fetch_url.py --url "https://example.com"`
- **保存处理后的输出**: `save_output.py --url "https://example.com" --title "示例"`
- **列出作业历史**: `list_jobs.py`
- **显示作业详情**: `show_job.py --id JOB-XXXX`

## 脚本说明
| 脚本 | 功能 |
|---|---|
| `init_storage.py` | 初始化本地存储 |
| `fetch_url.py` | 获取公共 URL 并提取内容 |
| `save_output.py` | 以自定义标题保存处理后的输出 |
| `list_jobs.py` | 列出之前的获取作业 |
| `show_job.py` | 显示已保存的作业详情 |