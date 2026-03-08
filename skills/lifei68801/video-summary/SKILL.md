---
name: video-summary
version: 1.3.2
description: "基于人工智能的视频摘要技术，适用于哔哩哔哩（Bilibili）、小红书（Xiaohongshu）、抖音（Douyin）和YouTube平台。通过自动转录和智能摘要功能，从视频内容中提取关键信息与见解。"
metadata:
  openclaw:
    requires:
      bins: ["yt-dlp", "jq", "ffmpeg"]
    install:
      - id: yt-dlp
        kind: pip
        package: yt-dlp
        bins: ["yt-dlp"]
        label: "Install yt-dlp for video/subtitle download"
      - id: jq
        kind: apt
        package: jq
        bins: ["jq"]
        label: "Install jq for JSON processing"
      - id: ffmpeg
        kind: apt
        package: ffmpeg
        bins: ["ffmpeg"]
        label: "Install ffmpeg for audio/video processing"
    setup:
      script: "scripts/setup.sh"
      description: "Conversational setup wizard - OpenClaw guides user through configuration"
      conversational: true
---
# 视频摘要技能

该技能支持多平台内容的智能视频摘要功能，兼容哔哩哔哩（Bilibili）、小红书（Xiaohongshu）、抖音（Douyin）、YouTube以及本地视频文件。

## 功能介绍

- **自动检测平台**：通过URL自动识别视频来源（哔哩哔哩、小红书、抖音、YouTube）。
- **提取字幕/文本**：使用各平台专属的方法提取字幕或文本。
- **生成结构化摘要**：包含关键信息、时间戳和实用建议。
- **多种输出格式**：支持纯文本、JSON、Markdown格式。
- **直接集成大型语言模型（LLM）**：输出可直接使用的摘要内容。
- **自动清理临时文件**：使用完成后会自动清理临时文件。

---

## 对话式设置流程

安装完成后，OpenClaw会引导您完成配置流程。

### 配置步骤

**步骤1：选择AI服务提供商**
OpenClaw会询问您希望使用哪种AI服务：
- 1) OpenAI
- 2) Zhipu GLM
- 3) DeepSeek
- 4) Moonshot/Kimi
- 5) 自定义

**步骤2：输入API密钥**
根据您的选择，OpenClaw会提示您输入API密钥。
获取方式如下：
- OpenAI：https://platform.openai.com/api-keys
- Zhipu：https://open.bigmodel.cn/
- DeepSeek：https://platform.deepseek.com/
- Moonshot：https://platform.moonshot.cn/

**步骤3：选择转录模型**
对于没有字幕的视频，需要选择合适的转录模型：
- **tiny**：速度最快，适合快速预览
- **base**：平衡性能，适合日常使用（推荐）
- **small**：准确率较高
- **medium**：精度较高
- **large**：精度最高

**步骤4：配置Cookies（可选）**
小红书和抖音可能需要Cookies来下载视频。您可以跳过此步骤，之后再配置。

### 手动触发
如果配置未完成，可以输入：
> “help me configure video-summary”

或者运行：
```bash
~/.openclaw/workspace/skills/video-summary/scripts/setup.sh
```

### 配置文件
- 配置文件：`~/.config/video-summary/config.sh`
- 状态文件：`~/.config/video-summary/setup-state.json`

### 检查配置状态
```bash
~/.openclaw/workspace/skills/video-summary/scripts/config-status.sh
```

---

## 对话式设置指南

**OpenClaw代理**：会逐步引导用户完成配置。

### 触发条件
- 当用户输入“help me configure video-summary”或“configure video-summary”时
- 或者在技能安装后首次使用时

### 配置步骤

#### 步骤1：检查配置状态
```bash
~/.openclaw/workspace/skills/video-summary/scripts/config-status.sh
```

如果返回`status: "complete"`，则表示配置完成。
如果返回`status: "pending"`或`status: "not_started"`，则开始对话式设置。

#### 步骤2：选择AI服务提供商
OpenClaw会询问：
> 🎬 视频摘要需要使用哪种AI服务来生成摘要？
> 
> 1. OpenAI
> 2. Zhipu GLM
> 3. DeepSeek
> 4. Moonshot/Kimi
> 5. 自定义端点
> 
> 请用数字或名称回答。

**处理用户输入：**
```bash
~/.openclaw/workspace/skills/video-summary/scripts/config-update.sh api_provider "openai"
# or "zhipu" / "deepseek" / "moonshot" / custom URL
```

#### 步骤3：输入API密钥
OpenClaw会提示您输入API密钥。
获取方式如下：
- OpenAI：https://platform.openai.com/api-keys
- Zhipu：https://open.bigmodel.cn/
- DeepSeek：https://platform.deepseek.com/
- Moonshot：https://platform.moonshot.cn/

**处理用户输入：**
```bash
~/.openclaw/workspace/skills/video-summary/scripts/config-update.sh api_key "sk-xxx..."
```

#### 步骤4：选择转录模型
OpenClaw会询问：
> 🎤 对于没有字幕的视频，需要选择转录模型：
> 
> 1. tiny - 速度最快（适合快速预览）
- 2. base - 性能平衡（推荐）
- 3. small - 准确率较高
- 4. medium - 精度较高
- 5. large - 准确率最高
> 
> 请用数字回答。默认为base模型。

**处理用户输入：**
```bash
~/.openclaw/workspace/skills/video-summary/scripts/config-update.sh whisper_model "base"
```

#### 步骤5：配置Cookies（可选）
OpenClaw会询问：
> 🍪 小红书和抖音可能需要Cookies来下载视频。现在配置吗？
> 
> - 输入“skip”表示跳过
- 输入“configure”表示开始配置

**如果用户选择跳过：**
```bash
~/.openclaw/workspace/skills/video-summary/scripts/config-update.sh cookies_skip "true"
```

**如果用户选择配置：**
- 询问每个平台（哔哩哔哩、小红书、抖音）的Cookies地址，然后保存配置：
```bash
~/.openclaw/workspace/skills/video-summary/scripts/config-update.sh cookies '{"xiaohongshu": "...", "douyin": "..."}'
```

#### 步骤6：配置完成
所有步骤完成后，OpenClaw会提示：
> ✅ 视频摘要配置已完成！
> 
> 现在您可以使用该技能：
> - “Summarize this video: [URL]”
- “Analyze this Bilibili video: [URL]”

### 自动检测现有配置
如果用户之前已经为OpenClaw配置了API（例如Zhipu），系统会自动检测并使用该配置：
```bash
# Detect OpenClaw configuration
cat ~/.openclaw/agents/main/agent/models.json | jq '.providers | to_entries[0]'
```

如果检测到现有配置，会询问用户是否继续使用：
> 检测到Zhipu API的配置。是否继续使用？（确认/否）

如果用户确认，系统将使用已检测到的配置完成设置。

---

## 快速启动

### 检查依赖项
```bash
# Check all required tools
yt-dlp --version && jq --version && ffmpeg -version

# If missing, install
pip install yt-dlp
apt install jq ffmpeg  # or: brew install jq ffmpeg
```

### 基本用法
```bash
# Standard summary
video-summary "https://www.bilibili.com/video/BV1xx411c7mu"

# With chapter segmentation
video-summary "https://www.youtube.com/watch?v=xxxxx" --chapter

# JSON output for programmatic use
video-summary "https://www.xiaohongshu.com/explore/xxxxx" --json

# Subtitle only (no AI summary)
video-summary "https://v.douyin.com/xxxxx" --subtitle

# Save to file
video-summary "https://www.bilibili.com/video/BV1xx" --output summary.md

# Use cookies for restricted content
video-summary "https://www.xiaohongshu.com/explore/xxxxx" --cookies cookies.txt
```

### 在OpenClaw代理中
只需输入：
> “Summarize this video: [URL]”

代理会自动执行以下操作：
1. 检测视频平台
2. 提取视频内容
3. 生成结构化摘要

---

## 命令参考

| 命令 | 描述 |
|---------|-------------|
| `video-summary "<url>"` | 生成标准摘要 |
| `video-summary "<url>" --chapter` | 按章节划分摘要 |
| `video-summary "<url>" --subtitle` | 仅提取原始字幕 |
| `video-summary "<url>" --json` | 生成JSON格式的摘要 |
| `video-summary "<url>" --lang <code>` | 指定字幕语言（默认：自动检测） |
| `video-summary "<url>" --output <path>` | 将摘要保存到文件 |
| `video-summary "<url>" --cookies <file>` | 使用指定的Cookies文件 |
| `video-summary "<url>" --transcribe` | 强制使用Whisper进行转录 |

---

## 工作原理

### 平台支持情况

| 平台 | 字幕提取方式 | 备注 |
|----------|-------------------|-------|
| **YouTube** | 内置字幕 + 自动生成 | 支持最佳 |
| **哔哩哔哩** | 内置字幕 + 备用方法 | 需要提取视频ID |
| **小红书** | 支持有限（依赖OCR技术） | 无内置字幕，需转录 |
| **抖音** | 支持有限（依赖OCR技术） | 短视频可能需要转录 |
| **本地文件** | 使用Whisper进行转录 | 支持mp4、mkv、webm、mp3等格式 |

### 支持的URL格式

- **YouTube**：`https://www.youtube.com/watch?v=xxxxx`  
- **Bilibili**：`https://www.bilibili.com/video/BV1xx411c7mu`  
- **小红书**：`https://www.xiaohongshu.com/explore/xxxxx`  
- **抖音**：`https://www.douyin.com/video/xxxxx`  

### 处理流程
```
URL Input
    ↓
Platform Detection
    ↓
Subtitle Extraction (yt-dlp / Whisper)
    ↓
Content Chunking (if long)
    ↓
LLM Summarization (OpenAI API / Agent)
    ↓
Structured Output
    ↓
Auto Cleanup
```

## 性能评估

### 转录时间

| 视频时长 | tiny | base | small | medium |
|---------------|------|------|-------|--------|
| 5分钟 | 约30秒 | 约1分钟 | 约2分钟 | 约4分钟 |
| 15分钟 | 约1.5分钟 | 约3分钟 | 约6分钟 | 约12分钟 |
| 30分钟 | 约3分钟 | 约6分钟 | 约15分钟 | 约30分钟 |
| 60分钟 | 约6分钟 | 约12分钟 | 约30分钟 | 约60分钟 |

**备注：**
- 使用GPU可显著提升处理速度（快3-10倍）  
- 建议使用`base`模型以获得平衡的性能 |

### 字幕提取时间

| 平台 | 时间 | 备注 |
|----------|------|-------|
| YouTube | 约5秒 | 直接下载字幕 |
| 哔哩哔哩 | 约5秒 | 直接下载字幕 |
| 小红书 | 约3分钟 | 需要转录 |
| 抖音 | 约2分钟 | 需要转录 |

---

## 高级配置

### 使用Whisper进行转录
对于没有内置字幕的平台（小红书、抖音），需要先安装Whisper工具：
```bash
pip install openai-whisper
```

然后进行配置：
```bash
export VIDEO_SUMMARY_WHISPER_MODEL=base  # tiny, base, small, medium, large
```

### 使用OpenAI API生成摘要
如需使用大型语言模型（LLM）生成摘要，请配置OpenAI API：
```bash
# Required for direct summarization
export OPENAI_API_KEY=sk-xxx

# Optional: Custom API endpoint
export OPENAI_BASE_URL=https://api.openai.com/v1

# Optional: Model selection
export OPENAI_MODEL=gpt-4o-mini
```

**无API密钥时：**脚本会自动生成请求格式供代理处理。

### 限制内容的Cookies配置
某些平台可能需要Cookies来访问受限内容：
```bash
# Method 1: Command line
video-summary "https://www.xiaohongshu.com/explore/xxxxx" --cookies cookies.txt

# Method 2: Environment variable
export VIDEO_SUMMARY_COOKIES=/path/to/cookies.txt
```

**获取Cookies的方法：**
1. 安装浏览器扩展程序“Get cookies.txt LOCALLY”。
2. 登录相关平台。
3. 将Cookies导出到文件。

### 自定义摘要提示
创建文件`~/.video-summary/prompt.txt`：
```markdown
You are a professional video content analyst. Generate a structured summary:

## Key Insights
- List 3-5 core arguments

## Key Information
- Data, cases, quotes

## Action Items
- Specific actions viewers can take

## Timestamp Navigation
- Key moments with timestamps and descriptions
```

---

## 输出格式

### 标准输出（默认）
```markdown
# Video Title

**Duration**: 12:34
**Platform**: Bilibili
**Author**: Tech Creator

## Core Content
This video explains...

## Key Points
1. Point one
2. Point two
3. Point three

## Timestamps
- 00:00 Introduction
- 02:15 Core concept
- 08:30 Case study
- 11:45 Summary
```

### JSON格式输出（`--json`）
```json
{
  "title": "Video Title",
  "platform": "bilibili",
  "duration": 754,
  "author": "Creator Name",
  "summary": "Core content summary...",
  "keyPoints": ["Point 1", "Point 2", "Point 3"],
  "chapters": [
    {"time": 0, "title": "Intro", "summary": "..."},
    {"time": 135, "title": "Core Concept", "summary": "..."}
  ],
  "transcript": "Full transcript text..."
}
```

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
```
~/.openclaw/workspace/skills/video-summary/
├── SKILL.md              # This file
├── scripts/
│   ├── video-summary.sh  # Main CLI script
│   ├── setup.sh          # Setup wizard
│   ├── config-status.sh  # Check config status
│   └── config-update.sh  # Update config
└── references/
    └── platform-support.md  # Detailed platform notes
```

### 环境变量
| 变量 | 默认值 | 说明 |
| ----------|---------|-------------|
| `OPENAI_API_KEY` | 自动检测 | OpenAI API密钥（根据配置自动设置） |
| `OPENAI_BASE_URL` | 自动检测 | 自定义API地址（根据配置自动设置） |
| `OPENAI_MODEL` | `gpt-4o-mini` | 用于生成摘要的模型 |
| `VIDEO_SUMMARY_WHISPER_MODEL` | `base` | 转录模型 |
| `VIDEO_SUMMARY_COOKIES` | - | Cookies文件路径 |

**配置优先级：**
1. 环境变量`OPENAI_API_KEY` / `OPENAI_BASE_URL`
2. OpenClaw配置文件`~/.openclaw/agents/main/agent/models.json`
3. 手动配置文件（setup.sh或config.sh）

---

## 常见问题解答

### “找不到字幕”
- 视频可能没有字幕或字幕信息缺失。
- 可尝试使用`--transcribe`选项进行转录。
- 对于小红书和抖音视频，需要先进行转录。

### “yt-dlp命令未找到”
```bash
pip install yt-dlp
# or
brew install yt-dlp
```

### “缺少依赖项”
```bash
# Install all dependencies
pip install yt-dlp
apt install jq ffmpeg  # Ubuntu/Debian
# or
brew install jq ffmpeg  # macOS
```

### “视频过长”
- 超过1小时的视频会自动分割成10分钟的小段进行处理。
- 分别对每个小段生成摘要，最后合并成最终结果。

### “无法获取视频信息”
- 视频可能被设置为私密或已被删除。
- 可尝试使用`--cookies`选项来获取访问权限。
- 地区限制的视频可能无法处理。

### 性能限制
- 如果请求次数过多，可能会导致平台限制。
- 可等待几分钟后再尝试。
- 使用`--cookies`选项可绕过权限限制。

---

## 功能对比

| 功能 | OpenClaw | video-summary |
|---------|-------------------|---------------|
| YouTube | 支持 | 支持 |
| 哔哩哔哩 | 不支持 | 支持（需转录） |
| 小红书 | 不支持 | 支持（需转录） |
| 分章节功能 | 不支持 | 支持 |
| 时间戳 | 不支持 | 支持 |
| 字幕提取 | 不支持 | 支持 |
| JSON输出 | 不支持 | 支持 |
| 保存到文件 | 不支持 | 支持 |
| Cookies支持 | 不支持 | 支持 |

---

## 参考资料
- [平台支持详情](references/platform-support.md)
- [yt-dlp文档](https://github.com/yt-dlp/yt-dlp)
- [OpenAI Whisper](https://github.com/openai/whisper)

---

## 贡献方式
发现漏洞或希望添加新平台支持？
- 在ClawHub上提交问题。
- 提交包含改进内容的Pull Request（PR）。

---

## 更新记录

### v1.3.0（2026-03-08）
- 添加了对话式设置流程，引导用户完成配置。
- 添加了`config-status.sh`文件以查询配置状态。
- 添加了`config-update.sh`文件以处理配置更新。
- `setup.sh`现在为非交互式脚本，完成配置后交由OpenClaw处理。
- 更新了`SKILL.md`文件，包含详细的配置指南。

### v1.2.2（2026-03-08）
- 重新设计了配置向导，采用问题驱动的流程。
- 简化了界面，仅提供英文说明。
- 提供了更清晰的步骤指导。

### v1.2.1（2026-03-08）
- 自动检测OpenClaw的API配置。
- 配置向导默认使用检测到的配置。
- 简化了配置流程。

### v1.2.0（2026-03-08）
- 添加了交互式配置向导。
- 添加了详细的配置指南。
- 添加了API密钥获取指南。
- 添加了Cookies配置指南。
- 添加了转录模型选择指南。

### v1.1.0（2026-03-08）
- 添加了与大型语言模型的集成。
- 添加了`--output`参数。
- 添加了`--cookies`参数。
- 实现了自动清理临时文件的功能。
- 添加了进度显示功能。
- 添加了依赖项检查。
- 更新了URL格式说明。
- 添加了性能评估表。
- 修复了相关依赖项的问题。

### v1.0.0
- 初始版本

---

*让视频内容更易于访问。让AI帮助您分析视频内容吧！*