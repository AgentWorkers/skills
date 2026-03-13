---
name: video-summary
version: 1.6.4
description: "适用于哔哩哔哩（Bilibili）、小红书（Xiaohongshu）、抖音（Douyin）和YouTube的视频摘要功能。通过转录和总结技术，从视频内容中提取有价值的见解。"

# 🔒 Security Declaration
# This skill downloads videos/subtitles from YouTube/Bilibili/Xiaohongshu/Douyin.
# It does NOT directly call external LLM APIs - it outputs structured requests for agent processing.
# OPENAI_API_KEY and OPENAI_BASE_URL are optional - used by agent, not by this script.
# Cookie files are read locally only, never transmitted externally.
# No config files written. No secrets stored. No telemetry, no analytics.
metadata:
  openclaw:
    requires:
      bins: ["yt-dlp", "jq", "ffmpeg", "ffprobe", "bc"]
      credentials:
        - name: "OPENAI_API_KEY"
          required: false
          description: "API key for LLM summarization (optional, script outputs request for agent processing)"
        - name: "OPENAI_BASE_URL"
          required: false
          description: "Custom API endpoint (e.g., for Zhipu, DeepSeek)"
        - name: "VIDEO_SUMMARY_COOKIES"
          required: false
          description: "Path to cookies file for restricted video content"
    behavior:
      networkAccess: indirect
      description: "Downloads videos/subtitles from video platforms using yt-dlp. Summarization requests are output as structured text for agent/external LLM processing. Script itself makes no direct LLM API calls. Requires yt-dlp, jq, ffmpeg. Optional: VIDEO_SUMMARY_WHISPER_MODEL, VIDEO_SUMMARY_COOKIES, OPENAI_BASE_URL, OPENAI_MODEL."
---
# 视频摘要技能

该技能支持跨平台视频内容的智能摘要生成，兼容哔哩哔哩（Bilibili）、小红书（Xiaohongshu）、抖音（Douyin）、YouTube以及本地视频文件。

## 功能概述

- **自动识别平台**：根据URL自动判断视频来自哪个平台（哔哩哔哩、小红书、抖音或YouTube）。
- **提取字幕/文本**：使用平台专属的方法提取字幕或文本。
- **生成结构化摘要**：包含关键信息、时间戳和实用建议。
- **多种输出格式**：支持纯文本、JSON和Markdown格式。
- **集成大型语言模型（LLM）**：可直接输出可供使用的摘要结果。
- **自动清理临时文件**：使用完毕后自动删除临时文件。

---

## 快速设置

**运行该技能无需API密钥**。它仅负责提取视频内容并生成摘要请求，具体的摘要生成工作由代理（或外部工具）通过LLM完成。

---

## 工作原理：
1. 脚本提取视频的字幕或文本。
2. 脚本生成结构化的摘要请求（JSON或文本格式）。
3. 代理或外部工具使用该请求调用LLM API。
4. 该脚本本身不直接调用任何外部API。

### 支持的LLM提供商

- **OpenAI**：[https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Zhipu GLM**：[https://open.bigmodel.cn/](https://open.bigmodel.cn/)
- **DeepSeek**：[https://platform.deepseek.com/](https://platform.deepseek.com/)
- **Moonshot**：[https://platform.moonshot.cn/](https://platform.moonshot.cn/)

只需将 `OPENAI_BASE_URL` 设置为相应提供商的API地址即可。

### Cookie配置（可选）

对于某些视频，小红书和抖音可能需要使用Cookie：

---

**⚠️ Cookie安全提示：**
- Cookie文件包含会话令牌，属于敏感信息。
- 仅使用来自您自己浏览器的Cookie。
- 请勿与他人共享Cookie文件。
- 该脚本仅在本地读取Cookie文件，不会将其传输到外部。

### 手动触发

如果配置不完整，可以输入：
> `help me configure video-summary`

---

## 快速入门

### 检查依赖项

---

### 基本用法

---

### 在OpenClaw代理中使用

只需输入：
> `Summarize this video: [URL]`

代理将自动完成以下操作：
1. 识别平台。
2. 提取视频内容。
3. 生成结构化摘要。

---

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `video-summary "<url>"` | 生成标准摘要 |
| `video-summary "<url>" --chapter` | 按章节分段生成摘要 |
| `video-summary "<url>" --subtitle` | 仅提取原始字幕文本 |
| `video-summary "<url>" --json` | 生成JSON格式的摘要 |
| `video-summary "<url>" --lang <code>` | 指定字幕语言（默认：自动检测） |
| `video-summary "<url>" --output <path>` | 将摘要保存到指定文件 |
| `video-summary "<url>" --cookies <file>` | 使用指定的Cookie文件 |
| `video-summary "<url>" --transcribe` | 强制使用Whisper工具进行转录 |

---

## 平台支持情况

| 平台 | 字幕提取方式 | 备注 |
|--------|-------------------|-------|
| **YouTube** | 内置字幕 + 自动生成 | 支持最佳 |
| **Bilibili** | 内置字幕 + 备用方法 | 需要提取视频ID |
| **Xiaohongshu** | 支持有限（依赖OCR技术） | 无内置字幕，需手动转录 |
| **Douyin** | 支持有限（依赖OCR技术） | 短视频可能需手动转录 |
| **本地文件** | 使用Whisper工具进行转录 | 支持mp4、mkv、webm、mp3等格式 |

### 支持的URL格式

- **YouTube**：`https://www.youtube.com/watch?v=xxxxx` 或 `https://youtu.be/xxxxx`
- **Bilibili**：`https://www.bilibili.com/video/BV1xx411c7mu` 或 `https://www.bilibili.com/video/av123456`
- **Xiaohongshu**：`https://www.xiaohongshu.com/explore/xxxxx` 或 `https://xhslink.com/xxxxx`
- **Douyin**：`https://www.douyin.com/video/xxxxx` 或 `https://v.douyin.com/xxxxx`

### 处理流程

---

## 性能评估

### Whisper转录时间

| 视频时长 | 极短 | 短 | 中等 | 长 |
|---------|------|------|-------|--------|
| 5分钟 | 约30秒 | 约1分钟 | 约2分钟 | 约4分钟 |
| 15分钟 | 约1.5分钟 | 约3分钟 | 约6分钟 | 约12分钟 |
| 30分钟 | 约3分钟 | 约6分钟 | 约15分钟 | 约30分钟 |
| 60分钟 | 约6分钟 | 约12分钟 | 约30分钟 | 约60分钟 |

**备注：**
- 使用GPU可显著提升转录速度（快3-10倍）。
- 建议使用“base”模型以获得平衡的性能。

### 字幕提取时间

| 平台 | 时间 | 备注 |
|---------|------|-------|
| YouTube | 约5秒 | 直接下载字幕 |
| Bilibili | 约5秒 | 直接下载字幕 |
| Xiaohongshu | 约3分钟 | 需要手动转录 |
| Douyin | 约2分钟 | 需要手动转录 |

---

## 高级配置

### 使用Whisper进行转录

对于没有内置字幕的平台（如小红书和抖音），请先安装Whisper工具：

---

然后进行相应的配置：

---

### 使用OpenAI API进行摘要生成

**该脚本本身不直接调用LLM API**。它仅生成结构化的请求供代理处理。

如果您希望代理通过LLM生成摘要，请进行相应的配置：

---

**注意事项：**
- 无需API密钥：脚本仅输出摘要请求和数据结构，代理负责实际的摘要生成工作。

### 对于需要认证的内容

某些平台可能要求使用Cookie来访问受限制的内容：

---

## 获取Cookie的方法：

1. 安装浏览器扩展程序“Get cookies.txt LOCALLY”。
2. 登录目标平台。
3. 将Cookie文件导出。

### 自定义摘要提示

创建文件 `~/.video-summary/prompt.txt`：

---

## 输出格式

### 标准输出（默认格式）

---

### JSON格式输出（使用 `--json` 参数）

---

## 技术细节

### 依赖项

| 工具 | 必需 | 用途 |
|------|----------|---------|
| **yt-dlp** | 是 | 用于下载视频和字幕 |
| **jq** | 是 | 用于处理JSON数据 |
| **ffmpeg** | 是 | 用于处理音频和视频 |
| **whisper** | 可选 | 用于本地转录 |

### 文件结构

---

### 环境变量

| 变量 | 默认值 | 说明 |
|---------|---------|-------------|
| `OPENAI_API_KEY` | - | **可选** - 用于LLM摘要生成的API密钥（由代理使用，非脚本本身所需） |
| `OPENAI_BASE_URL` | `https://api.openai.com/v1` | **可选** - 自定义API地址 |
| `OPENAI_MODEL` | `gpt-4o-mini` | **可选** - 用于摘要生成的模型 |
| `VIDEO_SUMMARY_WHISPER_MODEL` | `base` | 使用的Whisper模型版本 |
| `VIDEO_SUMMARY_COOKIES` | - | **可选** | Cookie文件路径（仅用于本地读取） |

---

## 常见问题及解决方法

- **“未找到字幕”**：可能是因为视频没有字幕或字幕未被正确提取。可以尝试使用 `--transcribe` 参数。
- **“yt-dlp: command not found”**：请确保已正确安装相关工具。
- **“缺少依赖项”**：请检查是否已安装所有必需的工具。
- **视频过长**：超过1小时的视频会自动分割成10分钟的小段，分别进行处理后再合并。

---

## 功能对比

| 功能 | OpenClaw summarize | video-summary |
|---------|-------------------|---------------|
| YouTube | 支持 | 支持 |
| Bilibili | 不支持 | 支持（需手动转录） |
| Xiaohongshu | 不支持 | 支持（需手动转录） |
| 分章节功能 | 不支持 | 支持 |
| 时间戳显示 | 不支持 | 支持 |
| 字幕提取 | 不支持 | 支持 |
| JSON输出 | 不支持 | 支持 |
| 保存到文件 | 不支持 | 支持 |
| Cookie支持 | 不支持 | 支持 |

---

## 参考资料

- [平台支持详情](references/platform-support.md)
- [yt-dlp文档](https://github.com/yt-dlp/yt-dlp)
- [OpenAI Whisper](https://github.com/openai/whisper)

---

## 贡献方式

如果发现漏洞或希望添加新的平台支持，请在ClawHub上提交问题或代码Pull Request。

---

## 更新记录

### v1.6.4 (2026-03-13)
- 修复了脚本语法错误。
- 明确说明脚本不直接调用LLM API，仅生成结构化请求。
- 更新了API密钥的相关说明。
- 增加了关于Cookie安全性的提示。

### v1.6.3 (2026-03-12)
- 修复了 `_meta.json` 和 `SKILL.md` 之间的版本不一致问题。

### v1.6.2 (2026-03-12)
- 修复了版本信息的一致性问题。

### v1.6.1 (2026-03-12)
- 优化了文档和代码结构。
- 修改了API密钥的相关说明。

### v1.5.1 (2026-03-12)
- 优化了安全相关代码，提高了安全性。

### v1.4.6 (2026-03-12)
- 修复了文档中的错误信息。
- 简化了配置流程。

---

## 注意事项

- 请在使用前设置环境变量 `OPENAI_API_KEY`。

---

*让视频内容更易于使用。减少观看时间，提升学习效率。*