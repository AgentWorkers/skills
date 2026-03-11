---
name: research  
description: "基于网络数据的综合性研究，包含明确的引用。适用于需要多源信息整合的情况——如比较分析、时事报道、市场分析或详细报告等。"
---# 研究技能

能够对任何主题进行全面的调研，包括自动收集资料、分析数据以及生成带有引用信息的调研结果。

## 认证

该脚本通过 Tavily MCP 服务器使用 OAuth 进行认证。**无需手动设置**——首次运行时，它会：
1. 检查 `~/.mcp-auth/` 文件夹中是否存在已有的 OAuth 令牌；
2. 如果未找到令牌，会自动打开浏览器进行 OAuth 认证。

> **注意：** 您必须拥有一个 Tavily 账户。此 OAuth 流程仅支持登录，不支持账户创建。如果您还没有账户，请先访问 [tavily.com](https://tavily.com) 注册。

### 替代方案：API 密钥

如果您更喜欢使用 API 密钥，可以在 [https://tavily.com](https://tavily.com) 获取密钥，并将其添加到 `~/.claude/settings.json` 文件中：
```json
{
  "env": {
    "TAVILY_API_KEY": "tvly-your-api-key-here"
  }
}
```

## 快速启动

> **提示：** 研究过程可能需要 30 到 120 秒。按 **Ctrl+B** 可以在后台运行该脚本。

### 使用脚本的方法

```bash
./scripts/research.sh '<json>' [output_file]
```

**示例：**

```bash
# Basic research
./scripts/research.sh '{"input": "quantum computing trends"}'

# With pro model for comprehensive analysis
./scripts/research.sh '{"input": "AI agents comparison", "model": "pro"}'

# Save to file
./scripts/research.sh '{"input": "market analysis for EVs", "model": "pro"}' ./ev-report.md

# Quick targeted research
./scripts/research.sh '{"input": "climate change impacts", "model": "mini"}'
```

## 参数

| 参数名 | 类型 | 默认值 | 说明 |
|---------|--------|---------|-----------------------------|
| `input` | string | 必填 | 需要研究的主题或问题 |
| `model` | string | `"mini"` | 可选模型：`mini`、`pro`、`auto` |

## 模型选择

**使用建议**：
- “X 的功能是什么？” → 选择 `mini` 模型；
- “X 与 Y、Z 的比较” 或 “……的最佳方法” → 选择 `pro` 模型；
- 脚本会根据问题的复杂性自动选择 `auto` 模型。

| 模型 | 适用场景 | 处理速度 |
|-------|-----------|-------------------------|
| `mini` | 单一主题的针对性研究 | 约 30 秒 |
| `pro` | 全面的多角度分析 | 约 60 至 120 秒 |
| `auto` | 脚本根据问题复杂性自动选择模型 | 处理时间不定 |

## 示例

### 快速概览

```bash
./scripts/research.sh '{"input": "What is retrieval augmented generation?", "model": "mini"}'
```

### 技术对比

```bash
./scripts/research.sh '{"input": "LangGraph vs CrewAI for multi-agent systems", "model": "pro"}'
```

### 市场调研

```bash
./scripts/research.sh '{"input": "Fintech startup landscape 2025", "model": "pro"}' fintech-report.md
```