---
name: video-news-downloader
description: "**具有AI字幕校对功能的自动化每日新闻视频下载工具**  
该工具能够从YouTube下载CBS晚间新闻（CBS Evening News）和BBC十点新闻（BBC News at Ten），并利用DeepSeek技术提取和校对这些新闻的视频字幕。下载后的视频可通过HTTP协议提供，并内置播放器供用户直接观看。  
**适用场景：**  
1. 自动化每日新闻视频的下载流程  
2. 下载带有字幕的CBS/BBC新闻内容  
3. 利用AI技术对字幕文件进行校对  
4. 构建支持网络播放器的本地视频流媒体服务器  
5. 通过Cron作业实现视频内容的定时更新  
**主要功能：**  
- 自动从YouTube下载指定新闻视频  
- 使用DeepSeek技术提取并校对视频字幕  
- 通过HTTP协议提供下载后的视频文件（包含嵌入式播放器）  
- 支持多种视频格式和字幕格式  
- 配置灵活的下载和更新计划  
**实用价值：**  
- 提高新闻视频下载的效率  
- 确保字幕内容的准确性和一致性  
- 便于用户随时随地观看带有字幕的新闻视频  
- 适用于新闻媒体、视频网站或个人视频库的构建  
**技术亮点：**  
- 结合AI技术实现高效字幕校对  
- 支持多种视频和字幕格式  
- 灵活的配置选项和调度机制  
**适用人群：**  
- 新闻媒体工作者  
- 视频内容制作人员  
- 自动化系统开发人员  
- 需要定期更新视频资源的用户"
---
# 带有AI字幕校对功能的视频新闻下载器

一个完整的流程，用于下载每日新闻视频、处理字幕，并通过HTTP接口使用网页播放器进行播放。

## 概述

该工具可自动化以下操作：
1. **视频下载**：从YouTube下载CBS晚间新闻和BBC十点新闻。
2. **字幕处理**：提取自动生成的字幕并将其转换为VTT格式。
3. **AI校对**：使用DeepSeek工具修复语音识别错误。
4. **HTTP流媒体服务**：通过嵌入的网页播放器提供视频流。
5. **定时更新**：根据配置的时间表每天自动执行任务。

## 快速入门

### 1. 下载最新新闻

```bash
python3 scripts/video_download.py --cbs --bbc
```

### 2. 校对字幕

```bash
python3 scripts/subtitle_proofreader.py /path/to/subtitle.vtt
```

或者直接使用DeepSeek工具：
> `deepseek /path/to/subtitle.vtt` （用于校对字幕文件）

### 3. 启动HTTP服务器

```bash
bash scripts/setup_server.sh
```

### 4. 设置定时任务

```bash
bash scripts/setup_cron.sh
```

## 命令

### 视频下载脚本

**仅下载CBS新闻：**
```bash
python3 scripts/video_download.py --cbs
```

**仅下载BBC新闻：**
```bash
python3 scripts/video_download.py --bbc
```

**同时下载CBS和BBC新闻：**
```bash
python3 scripts/video_download.py --cbs --bbc
```

**包含字幕校对功能：**
```bash
python3 scripts/video_download.py --cbs --bbc --proofread
```

### 字幕校对

**校对单个字幕文件：**
```bash
python3 scripts/subtitle_proofreader.py <vtt_file_path>
```

**自动校对所有新闻字幕：**
```bash
python3 scripts/subtitle_proofreader.py --all
```

### 服务器管理

**启动服务器：**
```bash
bash scripts/setup_server.sh start
```

**检查服务器状态：**
```bash
bash scripts/setup_server.sh status
```

**停止服务器：**
```bash
bash scripts/setup_server.sh stop
```

## 文件结构

```
/workspace/
├── cbs-live-local/
│   ├── cbs_latest.mp4
│   ├── cbs_latest.en.vtt          # Original subtitle
│   ├── cbs_latest.en.vtt-backup   # Backup
│   ├── cbs_latest-corrected.txt   # DeepSeek corrected text
│   └── cbs_latest-corrections.md  # Error list
│
├── bbc-news-live/
│   ├── bbc_news_latest.mp4
│   ├── bbc_news_latest.en.vtt
│   ├── bbc_news_latest.en.vtt-backup
│   ├── bbc_news_latest-corrected.txt
│   └── bbc_news_latest-corrections.md
│
└── temp/                           # Temporary download files
```

## HTTP接口

| 接口地址 | 功能描述 |
|------------|-------------------|
| http://IP:8093/ | CBS晚间新闻播放器 |
| http://IP:8093/cbs_latest.mp4 | CBS新闻视频（直接链接） |
| http://IP:8095/ | BBC十点新闻播放器 |
| http://IP:8095/bbc_news_latest.mp4 | BBC新闻视频（直接链接） |

## 定时任务

### 默认时间表（北京时间）

| 时间 | 任务 |
|------|------|
| 20:00 | 下载最新的CBS和BBC视频 |
| 20:30 | 使用DeepSeek工具校对字幕 |

### 手动配置定时任务

详细配置指南请参见 [references/cron-setup.md](references/cron-setup.md)。

## DeepSeek字幕校对

### 可修复的问题：

- 语音识别错误（例如：“noraster” → “nor’easter”）
- 名称错误（例如：“trunk” → “Trump”）
- 地点名称错误
- 专业术语错误
- 明显的拼写错误

### 输出文件

对于每个字幕文件，系统会生成以下文件：
1. `-backup.vtt` - 原始字幕文件（未经修改）
2. `-corrected.txt` - 经AI校正后的纯文本文件
3. `-corrections.md` - 校正内容列表

## 故障排除

### 视频下载失败

- 确保已安装`yt-dlp`工具：`yt-dlp --version`
- 检查YouTube视频链接是否可用
- 先尝试手动下载

### 字幕提取失败

- 有些视频没有自动生成的字幕
- 检查`--list-subs`命令是否能显示可用的字幕语言

### 服务器无法启动

- 确保端口8093/8095未被占用：`lsof -i :8093`
- 确保Python的http.server模块可用

### 校对问题

- 确保DeepSeek模型已安装并可用
- 检查字幕文件是否存在且格式正确（VTT格式）

## 相关文档

- [references/workflow.md](references/workflow.md) - 完整的工作流程文档
- [references/cron-setup.md](references/cron-setup.md) - 定时任务配置指南