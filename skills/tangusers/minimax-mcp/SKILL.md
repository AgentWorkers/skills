---
name: minimax-mcp
description: MiniMax MCP服务器用于网络搜索和图像处理。适用于以下场景：  
(1) 通过MiniMax API进行网络搜索；  
(2) 分析/描述图像；  
(3) 从URL中提取内容。  
使用该服务器需要MINIMAX_API_KEY（中国地区：api.minimaxi.com；全球地区：api.minimax.io）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍",
        "requires": { "bins": ["uvx"], "env": ["MINIMAX_API_KEY", "MINIMAX_API_HOST"] },
        "primaryEnv": "MINIMAX_API_KEY",
        "install":
          [
            {
              "id": "region",
              "kind": "select",
              "label": "Select Region",
              "options": ["Global (minimax.io)", "Mainland China (minimaxi.com)"],
              "default": "Mainland China (minimaxi.com)"
            },
            {
              "id": "api_key",
              "kind": "input",
              "label": "MiniMax API Key",
              "description": "Global: https://www.minimax.io/platform/user-center/basic-information/interface-key | China: https://platform.minimaxi.com/user-center/basic-information/interface-key",
              "secret": true,
              "envVar": "MINIMAX_API_KEY"
            },
            {
              "id": "uv",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uvx"],
              "label": "Install uv (required for MCP server)"
            }
          ]
      }
  }
---

# MiniMax MCP 技能

## 概述

这是一个官方的 MiniMax 模型上下文协议（MCP）服务器，专为编码计划（coding-plan）用户设计，提供基于人工智能的搜索和图像分析功能。

## 功能

| 工具 | 功能 | 支持的格式 |
|------|----------|-------------------|
| **web_search** | 基于结构的网页搜索（包括标题、链接和摘要） | - |
| **understand_image** | 人工智能图像分析和内容识别 | JPEG、PNG、WebP |

## 触发场景

当用户说出以下指令时，可以使用此技能：
- “搜索 xxx” / “查找 xxx”
- “看看这张图片” / “分析这张照片”
- “这张图片里有什么” / “描述这张照片”
- “从 URL 中提取内容” / “获取这个网页”

## 快速入门

### 1. 获取 API 密钥

| 地区 | API 密钥地址 | API 服务器 |
|--------|-------------|----------|
| 🇨🇳 中国 | platform.minimaxi.com | https://api.minimaxi.com |
| 🇺🇳 全球 | minimax.io | https://api.minimax.io |

### 2. 配置 mcporter（推荐）

```bash
# Add MCP server
mcporter config add minimax \
  --command "uvx minimax-coding-plan-mcp -y" \
  --env MINIMAX_API_KEY="your-key" \
  --env MINIMAX_API_HOST="https://api.minimaxi.com"

# Test connection
mcporter list
```

### 3. 直接使用

```bash
# Search
mcporter call minimax.web_search query="keywords"

# Analyze image
mcporter call minimax.understand_image prompt="Describe this image" image_source="image-url-or-path"
```

## 使用示例

请参阅 [references/examples.md](references/examples.md)。

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `MINIMAX_API_KEY` | ✅ | 你的 MiniMax API 密钥 |
| `MINIMAX_API_HOST` | ✅ | API 端点 |

## 重要提示

⚠️ **API 密钥必须与服务器所在地区匹配！**

| 地区 | API 密钥来源 | API 服务器 |
|--------|---------------|----------|
| 全球 | minimax.io | https://api.minimax.io |
| 中国 | minimaxi.com | https://api.minimaxi.com |

如果出现“无效的 API 密钥”错误，请检查你的密钥和服务器是否来自同一地区。

## 故障排除

- **“uvx 未找到”**：安装 uv：`brew install uv` 或 `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **“无效的 API 密钥”**：确认 API 密钥和服务器是否来自同一地区
- **图像下载失败**：确保图像 URL 可以公开访问，并且支持 JPEG/PNG/WebP 格式

## 相关资源

- GitHub: https://github.com/MiniMax-AI/MiniMax-Coding-Plan-MCP
- MiniMax 平台：https://platform.minimaxi.com（中国）/ https://www.minimax.io（全球）