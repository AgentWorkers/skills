---
name: youtube-scrapper
description: 一种无需API密钥或登录即可根据类别和位置发现并抓取YouTube频道的技能。
---

# YouTube 数据抓取技能

该技能提供了一个可靠的流程，用于通过 Google 搜索发现 YouTube 频道，并使用 Playwright 抓取频道的详细元数据（订阅者数量、观看次数、描述、最新视频等）。

## 功能

- **频道发现**：通过搜索特定类别和地区（例如：“印度科技博主”）来找到 YouTube 频道。
- **详细数据抓取**：提取频道信息，包括订阅者数量、观看次数、视频数量、加入频道日期、所在国家以及最新视频的元数据。
- **反检测机制**：内置机制可模仿人类行为，从而绕过基本的机器人检测系统。
- **流程协调**：能够无缝地从频道发现阶段过渡到数据抓取阶段，并提供进度跟踪和故障恢复功能。

## 先决条件

- **Python 3.8 或更高版本**
- **Playwright**：用于浏览器自动化操作。
- **依赖库**：需要安装 `pip install playwright aiohttp python-dotenv Pillow tqdm`
- **Playwright 浏览器插件**：需要安装 `playwright install chromium`

## 使用方法

### 1. 简单的频道发现
运行发现脚本以查找频道，并生成一个队列文件：
```bash
python scripts/youtube_channel_discovery.py --categories tech --locations India
```

### 2. 抓取队列中的数据
当队列文件（位于 `data/queue/` 目录下）生成后，运行数据抓取脚本：
```bash
python scripts/youtube_channel_scraper.py --queue data/queue/your_queue_file.json
```

### 3. 完整的流程协调
同时运行频道发现和数据抓取脚本：
```bash
python scripts/youtube_orchestrator.py --config resources/scraper_config_ind.json
```

## 配置
该技能使用位于 `config/` 目录下的 JSON 配置文件来管理区域搜索设置和延迟时间。

## 输出结果

- **数据**：抓取到的频道数据以 JSON 格式保存在 `data/output/` 目录下。
- **缩略图**：下载的频道头像、横幅和视频缩略图保存在 `thumbnails/` 目录下。
- **进度记录**：整个流程的进度信息保存在 `data/progress/` 目录下。