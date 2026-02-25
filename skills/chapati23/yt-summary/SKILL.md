---
name: youtube-summary
version: "1.3.2"
author: giskard
description: "您可以通过在聊天中输入 YouTube 视频的链接来总结该视频的内容。该功能支持自定义提示——只需粘贴视频链接并附上您的要求（例如：“重点介绍技术细节”）。该功能会在检测到 YouTube 链接时触发并执行相应的操作。"
tags: [youtube, video, summary, transcript]
license: MIT
homepage: https://github.com/chapati23
metadata:
  openclaw:
    emoji: "📺"
    requires:
      bins: [python3]
      env: [TRANSCRIPT_API_KEY]
    primaryEnv: TRANSCRIPT_API_KEY
---
# YouTube摘要功能

通过使用[TranscriptAPI.com](https://transcriptapi.com)提取视频字幕，并生成结构化的摘要来总结YouTube视频内容。

## 设置

### 先决条件

- Python 3.10及以上版本
- 一个TranscriptAPI.com账户（每月5美元，可获取1000条字幕）
- 可选：使用`pass`（Unix密码管理工具）来安全存储API密钥

### 安装

1. 在[transcriptapi.com](https://transcriptapi.com)注册并获取您的API密钥。
2. 通过以下方式之一提供API密钥：
   - **环境变量（最简单的方法）：** `export TRANSCRIPT_API_KEY="your-key-here"`
   - **使用`pass`密码管理工具（最安全的方法）：** `pass insert transcriptapi/api-key`
3. 安装Python依赖项：
   ```bash
   pip install -r skills/youtube-summary/requirements.txt
   ```

## 检测规则

当检测到包含以下YouTube URL的消息时，触发该功能：
- `youtube.com/watch?v=ID`
- `youtu.be/ID`
- `youtube.com/shorts/ID`
- `m.youtube.com/watch?v=ID`
- `youtube.com/live/ID`

## ⚠️ 重要规则

- **绝对不要使用网络搜索作为备用方案。** 如果提取字幕失败，请报告错误并停止操作。
- **绝对不要伪造字幕内容。** 只能总结提取脚本返回的内容。
- **务必运行提取脚本。** 即使是对知名视频，也不要跳过此步骤。

## 工作流程

### 第1步：提取字幕

**如果使用`pass`：**
```bash
_yt_key_file=$(mktemp) && pass transcriptapi/api-key > "$_yt_key_file" && python3 skills/youtube-summary/scripts/extract.py "YOUTUBE_URL_OR_ID" --api-key-file "$_yt_key_file"; rm -f "$_yt_key_file"
```

**如果使用环境变量：**
```bash
python3 skills/youtube-summary/scripts/extract.py "YOUTUBE_URL_OR_ID"
```
（自动从环境变量中读取`TRANSCRIPT_API_KEY`。）

**安全提示：** 使用`pass`和临时文件的方法可以避免在`ps`输出或shell历史记录中泄露API密钥。虽然环境变量的方法更简单，但密钥会在进程环境中显示。

解析标准输出（stdout）：
- `PROGRESS:`行 → 作为状态更新发送给用户（可选）
- `ERROR:`行 → 向用户显示错误信息并停止操作
- `RESULT:`行 → 解析`RESULT:`之后的JSON内容 — 包含：`header`、`transcript`、`language`、`tokens`、`title`、`channel`、`duration_str`

### 第2步：生成摘要

使用提取到的字幕生成摘要。摘要的语言必须与字幕的语言字段匹配。

- **如果字幕中的字符数小于50000个**：一次性请求并生成完整摘要。
- **如果字幕中的字符数大于或等于50000个**：告知用户视频较长，并仅总结前40000个字符，并注明内容已被截断。

**默认摘要格式**（当没有自定义提示时使用）：
```
{header}

**TL;DR:** 2-3 sentence summary.

**Key Points:**
• Point one
• Point two
• (3-7 total)

**Notable Quotes:** (only if genuinely quotable lines exist)
> "Quote here"
```

**自定义提示**：如果用户在URL中提供了额外说明，请将其作为摘要的附加指令一并包含。

### 第3步：回复用户

- 保持回复内容的长度在4000个字符以内（适用于Telegram）。
- 如果摘要超过4000个字符，先发送简短摘要（TL;DR），然后再发送剩余内容。
- 始终包含提取结果中的标题行。

## 错误处理

- `ERROR: API_ERROR: Invalid API key` → “TranscriptAPI密钥无效。请检查`pass transcriptapi/api-key`。”
- `ERROR: No transcript available` → “该视频没有字幕。”
- `ERROR: Video not found` → “无法找到该视频，请重新检查URL。”
- 其他错误：**直接将错误信息原样发送给用户。** **绝对不要使用网络搜索作为备用方案。**

## 为什么选择TranscriptAPI？

YouTube会严格限制某些数据中心/IPv6范围访问字幕数据。大多数云服务器（如Hetzner、DigitalOcean、AWS等）都会被屏蔽，因此从服务器直接获取字幕会失败。

TranscriptAPI.com通过居民IP地址代理请求，能够可靠地绕过这些限制。每月5美元的套餐包含1000次字幕提取服务。

💡 **提示：** 在URL后添加自定义提示，以便对摘要内容进行进一步定制（例如：“重点介绍技术细节”）。