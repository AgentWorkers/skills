---
name: siphonclaw
description: 文档智能处理流程：包含可视化搜索、光学字符识别（OCR）以及字段数据捕获功能
version: 1.2.0
metadata:
  siphonclaw:
    emoji: "\U0001F50D"
    requires:
      plugins: []
---
# SiphonClaw

这是一个与领域无关的文档智能处理平台，能够将PDF文件、图片和电子表格导入到一个可搜索的知识库中。该知识库支持双轨检索（文本+视觉信息），具备OCR（光学字符识别）功能、置信度评分以及字段数据捕获能力。

SiphonClaw专为现场服务工程师、研究人员、机械师以及任何需要从大量文档中快速获取信息的人士设计。

## SiphonClaw的主要功能

- **文档导入**：将PDF、Excel文件、图片和截图导入到本地向量数据库中，并生成相应的文本和视觉嵌入信息。
- **高效检索**：采用三重混合检索机制（BM25关键词匹配 + 语义文本向量 + 视觉页面嵌入），并结合RRF（Retrieval with RFF）技术进行重新排序。
- **设备识别**：利用视觉模型从图片中识别设备、零件或组件，然后在这些信息的基础上在本地知识库中进行搜索。
- **知识库构建**：将现场维修记录和修理笔记作为高质量的知识库条目保存下来，以便将来再次查询使用。
- **结果评估**：对每个检索结果进行综合评估（包括检索准确性、信息完整性、相关性以及覆盖范围），并附上来源引用信息。

## MCP工具

SiphonClaw通过MCP（Model Configuration Platform）提供了五种工具，以便与其他MCP兼容的客户端集成。

---

### siphonclaw_search

使用三重混合检索机制（文本+视觉+关键词）在知识库中进行搜索。

**参数：**

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|----------|-------------|
| `query` | 字符串 | 是 | 自然语言搜索查询或具体的零件编号/错误代码 |
| `top_k` | 整数 | 否 | 返回的结果数量（默认：5，最大值：20） |
| `filters` | 对象 | 否 | 元数据过滤器（例如：`{"source_type": "service_manual", "model": "ModelA"}`） |
| `mode` | 字符串 | 否 | 搜索模式："hybrid"（默认）、"text"、"visual"、"keyword" |

**返回值：**

```json
{
  "results": [
    {
      "content": "Extracted text from the matching chunk or page",
      "source": "ServiceManual_ModelA.pdf",
      "page": 42,
      "section": "4.3 Transformer Replacement",
      "score": 0.92,
      "match_type": "hybrid"
    }
  ],
  "confidence": 0.87,
  "confidence_tier": "Confident - verify part number",
  "keywords_used": ["low voltage supply", "assembly mount", "ModelA"],
  "citations": ["[1] ServiceManual_ModelA, page 42", "[2] Parts Catalog PC-1102, page 15"]
}
```

---

### siphonclaw_ingest

将文档或图片添加到知识库中。支持导入PDF、Excel文件、JPG/PNG格式的图片以及截图。

**参数：**

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|----------|-------------|
| `file_path` | 字符串 | 是 | 需要导入的文件的绝对路径 |
| `source_type` | 字符串 | 否 | 文档类型提示："manual"、"parts_catalog"、"field_note"、"photo"、"other"（默认：自动检测） |
| `metadata` | 对象 | 否 | 可附加的元数据（例如：`{"model": "ModelA", "domain": "industrial"}`） |

**返回值：**

```json
{
  "status": "ingested",
  "file": "ServiceManual_ModelA.pdf",
  "pages_processed": 127,
  "chunks_created": 843,
  "visual_pages_indexed": 127,
  "ocr_pages": 12,
  "duration_seconds": 45.2
}
```

---

### siphonclaw_field_note

将现场维修记录或修理笔记保存为知识库条目。这些条目会被索引，以便在未来的搜索中再次使用，从而形成一个持续学习的循环。

**参数：**

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|----------|-------------|
| `note` | 字符串 | 是 | 维修过程或观察结果的自由文本描述 |
| `model` | 字符串 | 否 | 设备型号或标识符（例如："ModelA"） |
| `parts` | 字符串数组 | 否 | 用于维修的零件编号（例如：`["12345", "67890"]`） |
| `procedure_ref` | 字符串 | 否 | 手册中相关程序的引用（例如："ServiceManual_ModelA section 4.3"） |
| `tags` | 字符串数组 | 否 | 用于分类的标签（例如："hv_transformer", "calibration"） |

**返回值：**

```json
{
  "status": "saved",
  "field_note_id": "fn-2026-02-09-001",
  "indexed": true,
  "model": "ModelA",
  "parts_cross_referenced": ["12345"],
  "retrievable": true
}
```

---

### siphonclaw_identify

上传设备的图片、零件、标签或错误屏幕截图。SiphonClaw会使用视觉模型进行识别，然后在本地知识库中查找相关文档；如果本地识别效果不佳，会转而使用网络搜索。

**参数：**

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|----------|-------------|
| `image_path` | 字符串 | 是 | 图片的绝对路径（JPG、PNG、HEIC格式） |
| `context` | 字符串 | 否 | 关于图片的附加描述（例如："设备内部的电路板"） |
| `search_after` | 布尔值 | 是否在识别后自动在知识库中搜索（默认：`true`） |

**返回值：**

```json
{
  "identification": "Industrial power supply board, Model PSU-200",
  "visual_features": ["green PCB", "3 large capacitors", "manufacturer logo visible", "part label partially obscured"],
  "ocr_text": "PSU-200 REV C  SN: 4829103",
  "search_results": [
    {
      "content": "PSU-200 replacement procedure...",
      "source": "ServiceManual_ModelA.pdf",
      "page": 67,
      "score": 0.94
    }
  ],
  "confidence": 0.91,
  "web_search_used": false
}
```

---

### siphonclaw_status

提供管道运行状态、文档导入统计信息、模型可用性以及成本跟踪数据。

**参数：**

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|----------|-------------|
| `detail` | 字符串 | 是否必填 | 详细程度："summary"（默认）、"full"、"costs"、"models" |

**返回值：**

```json
{
  "status": "healthy",
  "knowledge_base": {
    "total_documents": 3164,
    "total_chunks": 656000,
    "visual_pages_indexed": 31200,
    "last_ingestion": "2026-02-09T14:30:00Z"
  },
  "models": {
    "ocr": {"model": "qwen3-vl:latest", "provider": "ollama", "available": true},
    "text_embedding": {"model": "bge-m3:latest", "provider": "ollama", "available": true},
    "visual_embedding": {"model": "qwen3-vl-embed:2b", "provider": "ollama", "available": true},
    "generation": {"model": "MiniMax-M2.5", "provider": "openrouter", "available": true},
    "reasoning": {"model": "kimi-k2.5", "provider": "openrouter", "available": true},
    "fallback": {"model": "glm-4.7-flash:latest", "provider": "ollama", "available": true}
  },
  "costs": {
    "today": "$0.12",
    "this_month": "$2.45",
    "daily_budget": "$5.00",
    "budget_remaining": "$4.88"
  },
  "dead_letter_queue": {
    "pending_retry": 2,
    "permanently_failed": 1
  }
}
```

## MCP服务器

SiphonClaw作为MCP服务器运行，任何MCP兼容的客户端（如OpenClaw代理、Claude Desktop等）都可以连接到该服务器。

---

**OpenClaw代理配置（`~/.openclaw/openclaw.json`）：**

```json
{
  "mcpServers": {
    "siphonclaw": {
      "command": "python",
      "args": ["mcp_server.py"],
      "cwd": "/path/to/siphonclaw"
    }
  }
}
```

**Claude Desktop配置（`claude_desktop_config.json`）：**

```json
{
  "mcpServers": {
    "siphonclaw": {
      "command": "python",
      "args": ["/path/to/siphonclaw/mcp_server.py"]
    }
  }
}
```

## 设置方案

### 方案A：本地+云混合模式（推荐）

本地模型负责文档的导入（包括OCR处理和嵌入信息的生成），完全免费；而智能处理（如信息生成和推理）则通过云API完成，每次查询只需支付少量费用。

**每月成本：典型使用情况下约为0.50至5美元。**

---

### 方案B：全云模式

所有功能都通过OpenRouter平台运行，设置更为简单（无需使用Ollama），但导入大量文档需要支付API费用（50至100美元以上）。

**首月费用：约50至105美元；之后每月费用约为0.50美元。**

---

### 成本对比

| 操作 | 方案A（混合模式） | 方案B（全云模式） |
|-----------|-----------------|---------------------|
| 导入3,000份PDF文件 | 0美元（本地处理） | 约50至100美元（OCR处理和嵌入信息生成） |
| 每月100次搜索 | 约0.50美元（API调用费用） | 约0.50美元（相同费用） |
| 总月成本 | **约0.50至5美元** | **首月约50至105美元，之后每月约0.50美元** |

## 配置参考

SiphonClaw从`config/models.yaml`文件和环境变量中读取配置信息。

**环境变量（通过`.env`文件或shell设置）：**

| 变量 | 是否必填 | 描述 |
|----------|----------|-------------|
| `OPENROUTER_API_KEY` | 方案A/B | 用于智能模型的OpenRouter API密钥 |
| `BRAVE_SEARCH_API_KEY` | 否 | 用于备用网络搜索的Brave Search API密钥 |
| `OLLAMA_BASE_URL` | 否 | Ollama服务器地址（默认：`http://127.0.0.1:11434`） |
| `SIPHONCLAW_BUDGET_DAILY` | 否 | 每日API使用费用上限（美元）（默认：5.00美元） |
| `SIPHONCLAW_DOCS_PATH` | 否 | 文档导入目录的路径 |

**代理配置示例（`config.json`）：**

```json
{
  "skills": {
    "entries": {
      "siphonclaw": {
        "openrouter_key": "sk-or-v1-xxxxx",
        "brave_key": "BSA-xxxxx",
        "docs_path": "/path/to/docs",
        "ingestion_mode": "local",
        "ollama_url": "http://127.0.0.1:11434"
      }
    }
  }
}
```

**模型配置：**详细模型配置（包括导入和智能处理设置）请参见`config/models.yaml`文件。