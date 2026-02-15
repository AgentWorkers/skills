---
name: 2slides
description: **基于AI的演示文稿生成工具：使用2Slides API**  
该工具能够根据文本内容自动生成演示文稿幻灯片，同时支持匹配参考图片的样式，并可将文档内容汇总为演示文稿。适用于用户需要“创建演示文稿”、“制作幻灯片”、“生成幻灯片集”或“根据现有内容/文档/图片创建演示文稿”等场景。支持多种主题选择、多语言支持，以及同步和异步生成模式。
---

# 2Slides 演示文稿生成

使用 2Slides AI API 生成专业的演示文稿。支持基于内容的生成、从参考图片中匹配样式以及文档摘要功能。

## 设置要求

用户必须拥有 2Slides API 密钥：

1. 访问 https://2slides.com/api 创建 API 密钥
2. 将密钥存储在环境变量中：`SLIDES_2SLIDES_API_KEY`

```bash
export SLIDES_2SLIDES_API_KEY="your_api_key_here"
```

## 工作流程决策树

根据用户的需求选择合适的方法：

```
User Request
│
├─ "Create slides from this content/text"
│  └─> Use Content-Based Generation (Section 1)
│
├─ "Create slides like this image"
│  └─> Use Reference Image Generation (Section 2)
│
├─ "Create slides from this document"
│  └─> Use Document Summarization (Section 3)
│
└─ "Search for themes" or "What themes are available?"
   └─> Use Theme Search (Section 4)
```

---

## 1. 基于内容的生成

根据用户提供的文本内容生成幻灯片。

### 使用场景
- 用户直接在消息中提供内容
- 用户要求“创建关于 X 的演示文稿”
- 用户提供结构化的提纲或项目符号列表

### 工作流程

**步骤 1：准备内容**

为了获得最佳效果，请清晰地组织内容：

```
Title: [Main Topic]

Section 1: [Subtopic]
- Key point 1
- Key point 2
- Key point 3

Section 2: [Subtopic]
- Key point 1
- Key point 2
```

**步骤 2：选择主题（必选）**

搜索合适的主题（需要提供主题 ID）：

```bash
python scripts/search_themes.py --query "business"
python scripts/search_themes.py --query "professional"
python scripts/search_themes.py --query "creative"
```

从结果中选择一个主题 ID。

**步骤 3：生成幻灯片**

使用 `generate_slides.py` 脚本并传入主题 ID：

```bash
# Basic generation (theme ID required)
python scripts/generate_slides.py --content "Your content here" --theme-id "theme123"

# In different language
python scripts/generate_slides.py --content "Your content" --theme-id "theme123" --language "Spanish"

# Async mode for longer presentations
python scripts/generate_slides.py --content "Your content" --theme-id "theme123" --mode async
```

**步骤 4：处理结果**

**同步模式响应：**
```json
{
  "slideUrl": "https://2slides.com/slides/abc123",
  "pdfUrl": "https://2slides.com/slides/abc123/download",
  "status": "completed"
}
```

向用户提供两个 URL：
- `slideUrl`：交互式在线幻灯片
- `pdfUrl`：可下载的 PDF 版本

**异步模式响应：**
```json
{
  "jobId": "job123",
  "status": "pending"
}
```

通过 `get_job_status.py` 软件轮询结果：

```bash
python scripts/get_job_status.py --job-id "job123"
```

---

## 2. 参考图片生成

根据参考图片的样式生成幻灯片。

### 使用场景
- 用户提供图片 URL 并要求“生成类似这样的幻灯片”
- 用户希望匹配现有的品牌/设计风格
- 用户有想要模仿的模板图片

### 工作流程

**步骤 1：验证图片 URL**

确保参考图片满足以下条件：
- 是公开可访问的 URL
- 是有效的图片格式（PNG、JPG 等）
- 能够代表所需的幻灯片风格

**步骤 2：生成幻灯片**

使用 `generate_slides.py` 脚本并传入 `--reference-image` 参数：

```bash
python scripts/generate_slides.py \
  --content "Your presentation content" \
  --reference-image "https://example.com/template.jpg" \
  --language "Auto"
```

**可选参数：**
```bash
--aspect-ratio "16:9"           # width:height format (e.g., "16:9", "4:3")
--resolution "2K"               # "1K", "2K" (default), or "4K"
--page 5                        # Number of slides (0 for auto-detection, max 100)
--content-detail "concise"      # "concise" (brief) or "standard" (detailed)
```

**注意：** 此模式使用 Nano Banana Pro 服务，需要支付费用：
- 1K/2K 分辨率：每页 100 信用点
- 4K 分辨率：每页 200 信用点

**步骤 3：处理结果**

此模式始终以同步方式运行，并返回以下内容：
```json
{
  "slideUrl": "https://2slides.com/workspace?jobId=...",
  "pdfUrl": "https://...pdf...",
  "status": "completed",
  "message": "Successfully generated N slides",
  "slidePageCount": N
}
```

向用户提供两个 URL：
- `slideUrl`：在 2Slides 工作区中查看幻灯片
- `pdfUrl`：直接下载 PDF 文件（有效期为 1 小时）

**处理时间：** 每页约 30 秒（1-2 页通常需要 30-60 秒）

---

## 3. 文档摘要

根据文档内容生成幻灯片。

### 使用场景
- 用户上传文档（PDF、DOCX、TXT 等）
- 用户要求“根据此文档创建幻灯片”
- 用户希望将长文档内容总结为演示文稿格式

### 工作流程

**步骤 1：读取文档**

使用适当的工具读取文档内容：
- PDF：使用 PDF 阅读工具
- DOCX：使用 DOCX 阅读工具
- TXT/MD：使用相应的阅读工具

**步骤 2：提取关键信息**

分析文档并提取以下内容：
- 主要主题和要点
- 每个部分的关键内容
- 重要的数据、引用或示例
- 逻辑结构和内容框架

**步骤 3：组织内容**

将提取的信息格式化为演示文稿的结构：

```
Title: [Document Main Topic]

Introduction
- Context
- Purpose
- Overview

[Section 1 from document]
- Key point 1
- Key point 2
- Supporting detail

[Section 2 from document]
- Key point 1
- Key point 2
- Supporting detail

Conclusion
- Summary
- Key takeaways
- Next steps
```

**步骤 4：生成幻灯片**

使用基于内容的生成流程（步骤 1）。首先搜索一个主题，然后生成幻灯片：

```bash
# Search for appropriate theme
python scripts/search_themes.py --query "business"

# Generate with theme ID
python scripts/generate_slides.py --content "[Structured content from step 3]" --theme-id "theme123"
```

**提示：**
- 保持幻灯片简洁（每页 3-5 个要点）
- 重点展示关键见解，而非全部文本
- 使用文档标题作为幻灯片标题
- 包含重要的统计数据或引用
- 询问用户是否希望突出显示特定部分

---

## 4. 主题搜索

查找适合演示文稿的主题。

### 使用场景
- 在生成具有特定样式的幻灯片之前
- 用户询问“有哪些可用的主题？”
- 用户希望获得专业或品牌化的演示文稿外观

### 工作流程

**搜索主题：**

```bash
# Search for specific style (query is required)
python scripts/search_themes.py --query "business"
python scripts/search_themes.py --query "creative"
python scripts/search_themes.py --query "education"
python scripts/search_themes.py --query "professional"

# Get more results
python scripts/search_themes.py --query "modern" --limit 50
```

**主题选择：**

1. 向用户展示可用的主题及其名称和描述
- 让用户选择主题或使用默认主题
- 在生成请求中使用所选的主题 ID

---

## 使用 MCP 服务器

如果已在 Claude Desktop 中配置了 2Slides MCP 服务器，可以直接使用集成工具，而无需编写脚本。

**两种配置方式：**

1. **流式 HTTP 协议（推荐）**
   - 最简单的设置方式，无需本地安装
   - 配置方式：`"url": "https://2slides.com/api/mcp?apikey=YOUR_API_KEY"`

2. **NPM 包（stdio）**
   - 使用本地 npm 包
   - 配置方式：`"command": "npx", "args": ["2slides-mcp"]`

**可用的 MCP 工具：**
- `slides_generate` - 根据内容生成幻灯片
- `slides_create_like_this` - 根据参考图片生成幻灯片
- `themes_search` - 搜索主题
- `jobs_get` - 查看任务状态

请参阅 [mcp-integration.md](references/mcp-integration.md) 以获取完整的设置说明和工具文档。

**何时使用 MCP 与脚本：**
- 在 Claude Desktop 中配置好 MCP 服务器时，使用 MCP
- 当 MCP 不可用时，使用脚本

---

## 高级功能

### 同步模式与异步模式

**同步模式（默认）：**
- 等待生成完成（30-60 秒）
- 立即返回结果
- 适合快速创建演示文稿

**异步模式：**
- 立即返回任务 ID
- 使用 `get_job_status.py` 软件轮询结果
- 适合处理大量演示文稿或批量处理

### 语言支持

支持多种语言生成幻灯片（使用完整的语言名称）：

```bash
--language "Auto"                # Automatic detection (default)
--language "English"             # English
--language "Simplified Chinese"  # 简体中文
--language "Traditional Chinese" # 繁體中文
--language "Spanish"             # Español
--language "French"              # Français
--language "German"              # Deutsch
--language "Japanese"            # 日本語
--language "Korean"              # 한국어
```

支持的语言包括：阿拉伯语、葡萄牙语、印度尼西亚语、俄语、印地语、越南语、土耳其语、波兰语、意大利语

### 错误处理

**常见问题：**

1. **缺少 API 密钥**
   ```
   Error: API key not found
   Solution: Set SLIDES_2SLIDES_API_KEY environment variable
   ```

2. **速率限制**
   ```
   Error: 429 Too Many Requests
   Solution: Wait before retrying or check plan limits
   ```

3. **内容无效**
   ```
   Error: 400 Bad Request
   Solution: Verify content format and parameters
   ```

---

## 完整的 API 参考文档

有关详细的 API 文档，请参阅 [api-reference.md](references/api-reference.md)

内容包括：
- 所有端点和参数
- 请求/响应格式
- 认证详情
- 速率限制和最佳实践
- 错误代码及处理方法

---

## 优化结果的建议

**内容结构：**
- 使用清晰的标题和子标题
- 保持项目符号列表的简洁性
- 每个部分限制 3-5 个要点
- 包含相关的示例或数据

**主题选择：**
- 标准生成需要提供主题 ID
- 使用与演示文稿目的匹配的关键词进行搜索
- 常见搜索词：商业、专业、创意、教育、现代
- 每个主题都有独特的样式和布局

**参考图片：**
- 使用高质量的图片以获得最佳效果
- 可以使用 URL 或 Base64 编码的图片
- 确保图片 URL 是公开可访问的
- 根据质量需求选择合适的分辨率（1K/2K/4K）
- 使用 `page=0` 来自动检测幻灯片数量

**文档处理：**
- 仅提取关键信息
- 不要尝试将整个文档内容放入幻灯片中
- 重点展示主要观点和要点
- 询问用户是否希望突出显示某些部分