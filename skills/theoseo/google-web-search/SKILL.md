---
name: google-web-search
description: 该功能通过自动在 Gemini 模型中执行 Google 搜索工具，实现了基于事实的问答。当所需信息属于最新内容（即在知识更新截止日期之后发布的）或需要可验证的引用来源时，应使用此功能。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "env": ["GEMINI_API_KEY"] },
        "primaryEnv": "GEMINI_API_KEY",
        "install":
          [
            {
              "id": "python-deps",
              "kind": "shell",
              "command": "pip install -r {baseDir}/requirements.txt",
              "label": "Install Python dependencies (google-genai, pydantic-settings)",
            },
          ],
      },
  }
---

# 谷歌网页搜索

## 概述

该技能通过 Gemini API 的 `google_search` 工具提供实时网页搜索功能。它旨在获取网络上最新的信息，以提供有根据的、可引用的回答来满足用户查询需求。

**主要特点：**
- 通过 Gemini API 进行实时网页搜索
- 提供带有可验证引用的有根据的回答
- 支持模型选择
- 使用简单的 Python API

## 使用方法

该技能提供了 Gemini API 的 `google_search` 工具。当用户需要 **实时信息**、**最近的事件** 或 **可验证的引用** 时，应使用该工具。

### 执行环境

核心逻辑位于 `scripts/example.py` 文件中。此脚本需要以下环境变量：
- **GEMINI_API_KEY**（必填）：您的 Gemini API 密钥
- **GEMINI_MODEL**（可选）：要使用的模型（默认值：`gemini-2.5-flash-lite`）

**支持的模型：**
- `gemini-2.5-flash-lite`（默认）：快速且经济高效
- `gemini-3-flash-preview`：最新的闪存模型
- `gemini-3-pro-preview`：功能更强大，但速度较慢
- `gemini-2.5-flash-lite-preview-09-2025`：特定版本

### Python 工具实现方式

在将此技能集成到更大的工作流程中时，辅助脚本应在安装了 `google-genai` 库的环境中执行，并且需要设置 `GEMINI_API_KEY`。

示例 Python 调用结构：
```python
from skills.google-web-search.scripts.example import get_grounded_response

# Basic usage (uses default model):
prompt = "What is the latest market trend?"
response_text = get_grounded_response(prompt)
print(response_text)

# Using a specific model:
response_text = get_grounded_response(prompt, model="gemini-3-pro-preview")
print(response_text)

# Or set via environment variable:
import os
os.environ["GEMINI_MODEL"] = "gemini-3-flash-preview"
response_text = get_grounded_response(prompt)
print(response_text)
```

### 故障排除

如果脚本失败，请检查以下原因：
1. **缺少 API 密钥**：确保在执行环境中设置了 `GEMINI_API_KEY`。
2. **缺少库**：确认已安装 `google-genai` 库（使用 `pip install google-generativeai` 安装）。
3. **API 使用限制**：查看 Google AI Studio 仪表板上的 API 使用限制。
4. **无效的模型**：如果设置了 `GEMINI_MODEL`，请确保它是有效的 Gemini 模型名称。
5. **模型不支持搜索功能**：某些模型可能不支持 `google_search` 工具。请使用 `gemini-2.5-flash-lite` 或 `gemini-3-flash-preview` 等模型。