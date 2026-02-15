---
name: gemini-deep-research
description: 使用 Gemini Deep Research Agent 执行复杂、耗时的研究任务。当需要研究涉及多源信息整合、竞争分析、市场调研或需要系统化网络搜索与分析的综合性技术课题时，请使用该工具。
metadata: {"clawdbot":{"emoji":"🔬","requires":{"env":["GEMINI_API_KEY"]},"primaryEnv":"GEMINI_API_KEY"}}
---

# Gemini 深度研究

使用 Gemini 的深度研究代理来执行复杂、耗时的上下文收集和综合任务。

## 先决条件

- `GEMINI_API_KEY` 环境变量（来自 Google AI Studio）
- **注意**：此功能不支持 Antigravity OAuth 令牌，需要直接使用 Gemini API 密钥。

## 工作原理

深度研究代理具备以下功能：
1. 将复杂的查询分解为多个子问题
2. 系统地搜索互联网
3. 将搜索结果整合成全面的报告
4. 提供实时的进度更新

## 使用方法

### 基本研究

```bash
scripts/deep_research.py --query "Research the history of Google TPUs"
```

### 自定义输出格式

```bash
scripts/deep_research.py --query "Research the competitive landscape of EV batteries" \
  --format "1. Executive Summary\n2. Key Players (include data table)\n3. Supply Chain Risks"
```

### 带文件搜索（可选）

```bash
scripts/deep_research.py --query "Compare our 2025 fiscal year report against current public web news" \
  --file-search-store "fileSearchStores/my-store-name"
```

### 实时进度监控

```bash
scripts/deep_research.py --query "Your research topic" --stream
```

## 输出结果

脚本会将结果保存为带时间戳的文件：
- `deep-research-YYYY-MM-DD-HH-MM-SS.md` – 最终的 markdown 格式报告
- `deep-research-YYYY-MM-DD-HH-MM-SS.json` – 完整的交互元数据

## API 详情

- **端点**：`https://generativelanguage.googleapis.com/v1beta/interactions`
- **代理名称**：`deep-research-pro-preview-12-2025`
- **认证方式**：使用 `x-goog-api-key` 头部信息（不支持 OAuth Bearer 令牌）

## 限制

- 需要 Gemini API 密钥（可从 [Google AI Studio](https://aistudio.google.com/apikey) 获取）
- 不支持 Antigravity OAuth 认证方式
- 需要较长时间来完成任务（根据任务复杂度，可能需要几分钟到几小时）
- 可能会产生 API 使用费用（取决于您的使用额度）