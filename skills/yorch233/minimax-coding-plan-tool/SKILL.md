---
name: minimax-coding-plan-tool
description: 这是一个轻量级的 MiniMax 编码计划工具技能，它直接使用纯 JavaScript 调用官方的 MCP API。无需使用任何外部 MCP 服务器或工具桥接，也不涉及子进程的调用。该工具的设计旨在实现最小的开销，并能够快速集成到 OpenClaw 中。
metadata: {"openclaw":{"emoji":"🧩","requires":{"bins":["node"],"env":["MINIMAX_API_KEY"]},"primaryEnv":"MINIMAX_API_KEY"}}
---
# MiniMax 编码计划工具

> ⚠️ 需要一个 **编码计划 API 密钥**  
> 订阅地址：[https://platform.minimaxi.com/subscribe/coding-plan](https://platform.minimaxi.com/subscribe/coding-plan)  

这是一个轻量级的 MiniMax 编码计划工具，它使用纯 JavaScript 直接调用官方的 MCP API。  
无需依赖任何外部 MCP 服务器或工具桥接，也不需要调用子进程。  

该工具设计用于实现最小的开销，并能快速集成到 OpenClaw 中。  

---

## ✨ 功能  

该工具提供了 MiniMax 编码计划 MCP 的两个原生功能：  

### 1. `minimax_web_search`  

- 基于 MiniMax 编码计划 API 的网页搜索功能：  
  - 实时信息检索  
  - 采用轻量级的 API 实现  
  - 无需依赖外部搜索引擎  

### 2. `minimax_understand_image`  

- 通过 MiniMax VLM（视觉语言模型）实现图像理解：  
  - 图像语义分析  
  - 视觉内容描述  
  - 支持多模态推理  

---

## 🧩 架构  

- 完全使用 JavaScript 实现  
- 直接通过 HTTPS 调用 API  
- 无需运行 MCP 服务器  
- 无需依赖任何外部工具  
- 资源消耗极低  

---

## 🔑 配置  

```bash
openclaw config set skills.entries.minimax-coding-plan-tool.apiKey "sk-your-key"
```  

或  

```json
{
  "skills": {
    "entries": {
      "minimax-coding-plan-tool": {
        "apiKey": "sk-your-key"
      }
    }
  }
}
```  

请从 `openclaw.json` 文件中获取 API 密钥。  

---

# 工具发现  

通过设置环境变量 `MINIMAX_API_KEY` 来动态注册这些工具：  

```bash
MINIMAX_API_KEY="sk-your-key" node minimax_coding_plan_tool.js tools
```  

输出格式：  

```json
{
  "tools": [
    {
      "name": "minimax_web_search",
      "description": "...",
      "inputSchema": { ... }
    },
    {
      "name": "minimax_understand_image",
      "description": "...",
      "inputSchema": { ... }
    }
  ]
}
```  

---

## 工具 1 — `minimax_web_search`  

**用途**：  
使用 MiniMax 编码计划的搜索 API 进行实时网页搜索。  

**命令行调用方式：**  

```bash
MINIMAX_API_KEY="sk-your-key" node minimax_coding_plan_tool.js web_search "<查询>"
```  

示例：  

```bash
MINIMAX_API_KEY="sk-your-key" node minimax_coding_plan_tool.js web_search "OpenAI GPT-5 release date"
```  

**输入格式：**  

```json
{
  "query": "string"
}
```  

**输出格式：**  

成功时：  

```json
{
  "success": true,
  "query": "...",
  "results": [
    {
      "title": "...",
      "link": "...",
      "snippet": "...",
      "date": "..."
    }
  ],
  "related_searches": []
}
```  

失败时：  

```json
{
  "error": "错误信息"
}
```  

---

## 工具 2 — `minimax_understand_image`  

**用途：**  
使用 MiniMax 编码计划的 VLM API 进行图像理解。  
仅支持主流图像格式（如 JPEG/JPG、PNG、WebP 和 GIF）。  

**支持方式：**  
- HTTP/HTTPS 图像链接  
- 本地文件路径  
- 使用 `@localfile.jpg` 作为文件路径的简写形式  

本地文件会自动转换为 Base64 格式的 URL。  

**安全提示：**  
该工具需要访问外部网络。如果提供本地图像，其内容会被传输到远程的 MiniMax API 进行处理，这可能存在数据泄露的风险。  
请确保您完全理解这一风险，再提交敏感、私密或受监管的图像。  

**命令行调用方式：**  

```bash
MINIMAX_API_KEY="sk-your-key" node minimax_coding_plan_tool.js understand_image <图像来源> "<提示>"
```  

示例：  

- 远程图像：  
```bash
MINIMAX_API_KEY="sk-your-key" node minimax_coding_plan_tool.js understand_image https://example.com/image.jpg "描述这张图片"
```  

- 本地图像：  
```bash
MINIMAX_API_KEY="sk-your-key" node minimax_coding_plan_tool.js understand_image ./photo.png "图片中有哪些物体？"
```  

- 使用 `@` 前缀：  
```bash
MINIMAX_API_KEY="sk-your-key" node minimax_coding_plan_tool.js understand_image @photo.png "总结场景中的元素"
```  

**输入格式：**  

```json
{
  "image_source": "string",
  "prompt": "string"
}
```  

**输出格式：**  

成功时：  

```json
{
  "success": true,
  "prompt": "...",
  "image_source": "...",
  "analysis": "模型分析结果"
}
```  

失败时：  

```json
{
  "error": "错误信息"
}
```