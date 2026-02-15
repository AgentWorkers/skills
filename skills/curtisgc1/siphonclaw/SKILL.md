---
name: siphonclaw
description: 文档智能处理流程：包含可视化搜索、光学字符识别（OCR）以及字段数据捕获功能
version: 1.0.0
metadata:
  siphonclaw:
    emoji: "\U0001F50D"
    requires:
      plugins: []
---

# SiphonClaw

这是一个与领域无关的文档智能处理平台，能够将PDF文件、图片和电子表格导入到一个可搜索的知识库中。该知识库支持双重检索方式（文本 + 图像），并具备OCR（光学字符识别）功能、置信度评分以及字段数据捕获能力。

SiphonClaw专为现场服务工程师、研究人员、机械师以及任何需要从大量文档中快速获取信息的人士设计。

## SiphonClaw的主要功能

- **文档导入**：将PDF、Excel文件、图片和截图导入到本地向量数据库中，同时生成文本和图像嵌入数据。
- **高效搜索**：采用三重混合检索机制（BM25关键词匹配 + 语义文本向量 + 图像页面嵌入），并结合RRF（Retrieval with Re-ranking）算法进行结果重新排序。
- **设备识别**：利用视觉模型从图片中识别设备、部件或组件，并在本地知识库中查找相关信息。
- **字段记录**：将维修记录和修复笔记保存为高质量的知识库条目，以便后续查询使用。
- **结果评估**：对每个搜索结果进行综合评估（包括检索效果、准确性、相关性及覆盖范围），并附上来源引用信息。

## MCP工具

SiphonClaw通过MCP（Model Configuration Platform）提供了五种工具，以便与其他系统和客户端集成。

---

### siphonclaw_search

使用三重混合检索机制（文本 + 图像 + 关键词）在知识库中进行搜索。

**参数：**

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|---------|-------------------|
| `query` | 字符串 | 是 | 自然语言搜索查询或具体的部件编号/错误代码 |
| `top_k` | 整数 | 否 | 返回的结果数量（默认：5，最大：20） |
| `filters` | 对象 | 否 | 元数据过滤条件（例如：`{"source_type": "service_manual", "model": "ModelA"}`） |
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
|------|------|---------|-------------------|
| `file_path` | 字符串 | 是 | 要导入文件的绝对路径 |
| `source_type` | 字符串 | 否 | 文档类型（提示：`"manual"`、`"parts_catalog"`、`"field_note"`、`"photo"`、`"other"`（默认：自动检测） |
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

将维修记录或修复笔记保存为知识库条目。这些条目会被索引，可用于未来的搜索，从而形成持续的学习循环。

**参数：**

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|---------|-------------------|
| `note` | 字符串 | 是 | 维修内容、操作步骤或观察结果的自由文本描述 |
| `model` | 字符串 | 否 | 设备型号或标识符（例如：`"ModelA"`） |
| `parts` | 字符串数组 | 否 | 用于描述的部件编号（例如：`["12345", "67890"]`） |
| `procedure_ref` | 字符串 | 否 | 手册中的参考步骤（例如：`"ServiceManual_ModelA section 4.3"`） |
| `tags` | 字符串数组 | 否 | 用于分类的标签（例如：`["hv_transformer", "calibration"]`） |

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

上传设备、部件、标签或错误屏幕的图片。SiphonClaw会使用视觉模型进行识别，然后在本地知识库中查找相关文档；如果本地识别效果不佳，则会转而使用网络搜索。

**参数：**

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|---------|-------------------|
| `image_path` | 字符串 | 是 | 图片的绝对路径（JPG、PNG、HEIC格式） |
| `context` | 字符串 | 否 | 关于图片的附加描述（例如：`设备内部的电路板`） |
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

提供系统运行状态、文档导入统计信息、模型可用性以及成本跟踪数据。

**参数：**

| 名称 | 类型 | 是否必填 | 描述 |
|------|------|---------|-------------------|
| `detail` | 字符串 | 是否必填 | 详细程度（默认：`summary`）、`full`、`costs`、`models` |

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

## 配置方式

### 模式A：本地+云端混合模式（推荐）

本地模型负责文档的导入（OCR处理和嵌入生成），完全免费。云端API负责智能处理（信息生成和推理），每次查询仅需少量费用。

**每月成本：典型使用情况下约为0.50-5美元。**

```bash
# 1. Install SiphonClaw
pip install siphonclaw
# or: openclaw skill install siphonclaw
# or: git clone https://github.com/openclaw/siphonclaw && pip install -r requirements.txt

# 2. Install Ollama and pull local models (~10 GB total)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen3-vl:latest          # 6.1 GB - OCR
ollama pull bge-m3:latest             # ~1.5 GB - text embeddings
ollama pull qwen3-vl-embed:2b        # ~2 GB - visual embeddings

# 3. Get OpenRouter API key (ONE key for all intelligence models)
#    Visit: https://openrouter.ai -> Sign up -> Copy API key
siphonclaw config set openrouter_key sk-or-v1-xxxxx

# 4. (Optional) Get Brave Search API key for web search fallback
#    Visit: https://brave.com/search/api -> Sign up -> Free tier: 2,000 queries/mo
siphonclaw config set brave_key BSA-xxxxx

# 5. Point to your documents and ingest
siphonclaw config set docs_path /path/to/my/docs
siphonclaw ingest

# 6. Search
siphonclaw search "part number for compressor valve"
```

### 模式B：全云端模式

所有功能通过OpenRouter平台运行。设置更简单（无需Ollama），但导入大量文档需要支付API费用（50-100美元以上）。

**首月费用：约50-105美元。之后：每月约0.50美元。**

---

### 成本对比

| 操作 | 模式A（混合模式） | 模式B（全云端模式） |
|------|-----------------|---------------------|
| 导入3,000份PDF文件 | 0美元（本地处理） | 约50-100美元（OCR和嵌入处理） |
| 每月100次搜索 | 约0.50美元（API费用） | 约0.50美元（相同费用） |
| 总成本 | **每月约0.50-5美元** | **首月约50-105美元，之后每月约0.50美元** |

## 配置参考

SiphonClaw从`config/models.yaml`文件和环境变量中读取配置信息。

**环境变量（通过`.env`文件或shell设置）：**

| 变量 | 是否必填 | 描述 |
|------|---------|-------------------|
| `OPENROUTER_API_KEY` | 模式A/B | OpenRouter API密钥（用于智能处理） |
| `BRAVE_SEARCH_API_KEY` | 否 | Brave Search API密钥（用于网络搜索备用） |
| `OLLAMA_BASE_URL` | 否 | Ollama服务器地址（默认：`http://127.0.0.1:11434`） |
| `SIPHONCLAW_BUDGET_DAILY` | 否 | 每日API使用额度（美元）（默认：5.00美元） |
| `SIPHONCLAW_DOCS_PATH` | 否 | 文档导入目录路径 |

**代理配置示例（`config.json`文件）：**

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

**模型配置：**详细模型配置信息请参见`config/models.yaml`文件，其中包含导入和智能处理的相关设置。