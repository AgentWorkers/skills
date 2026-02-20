---
name: intelligent-router
description: 智能模型路由机制，用于子代理任务的分配。根据任务的复杂性、成本和能力要求选择最合适的模型。通过将简单任务分配给成本更低的模型来降低成本，同时确保复杂任务的质量得到保障。
version: 3.1.0
core: true
---
# 智能路由器 — 核心技能

> **核心技能**：此技能属于基础设施范畴，而非操作指南。需通过运行 `bash skills/intelligent-router/install.sh` 命令来激活该技能。

## 功能概述

该技能能够自动将任务分为不同的难度等级（简单/中等/复杂/需要推理/关键），并推荐最适合处理该任务的模型（同时确保成本最低）。

**解决的问题**：在没有路由机制的情况下，所有定时任务（cron jobs）和子代理（sub-agents）默认使用成本较高的 Sonnet 模型；而通过路由机制后，监控任务可以使用免费的本地模型，从而节省 80-95% 的成本。

---

## 强制性协议（通过 AGENTS.md 文件强制执行）

### 在创建任何子代理之前：
```bash
python3 skills/intelligent-router/scripts/router.py classify "task description"
```

### 在创建任何定时任务之前：
```bash
python3 skills/intelligent-router/scripts/spawn_helper.py "task description"
# Outputs the exact model ID and payload snippet to use
```

### 验证定时任务是否已配置相应的模型：
```bash
python3 skills/intelligent-router/scripts/spawn_helper.py --validate '{"kind":"agentTurn","message":"..."}'
```

### ✌ **禁止的行为**：
```python
# Cron job without model = Sonnet default = expensive waste
{"kind": "agentTurn", "message": "check server..."}  # ← WRONG
```

### ✅ **正确做法**：
```python
# Always specify model from router recommendation
{"kind": "agentTurn", "message": "check server...", "model": "ollama/glm-4.7-flash"}
```

---

## 任务难度等级系统

| 等级 | 适用场景 | 主要使用的模型 | 成本 |
|------|---------|---------------|------|
| 🟢 简单 | 监控、检查、汇总 | `ollama/glm-4.7-flash` | 免费 |
| 🟡 中等 | 代码修复、补丁、研究 | DeepSeek V3.2 | 每分钟 0.40 美元 |
| 🟠 复杂 | 功能开发、架构设计、调试 | Sonnet 4.6 | 每分钟 3 美元 |
| 🔵 需要推理 | 证明逻辑、形式化推理 | DeepSeek R1 32B | 每分钟 0.20 美元 |
| 🔴 关键 | 安全相关、生产环境 | Opus 4.6 | 每分钟 5 美元 |

**简单任务的默认处理流程**：`ollama/glm-4.7-flash` → `anthropic-proxy-4/glm-4.7` → `anthropic-proxy-6/glm-4.5-air`

---

## 安装（核心技能的配置）

运行一次安装命令后，该技能会自动集成到 AGENTS.md 文件中，确保所有相关配置的一致性：
```bash
bash skills/intelligent-router/install.sh
```

此操作会更新 AGENTS.md 文件中的强制性协议内容，确保所有代理始终遵循该协议。

---

## 命令行接口（CLI）参考

```bash
# Classify + recommend model
python3 skills/intelligent-router/scripts/router.py classify "task"

# Get model id only (for scripting)
python3 skills/intelligent-router/scripts/spawn_helper.py --model-only "task"

# Show spawn command
python3 skills/intelligent-router/scripts/spawn_helper.py "task"

# Validate cron payload has model set
python3 skills/intelligent-router/scripts/spawn_helper.py --validate '{"kind":"agentTurn","message":"..."}'

# List all models by tier
python3 skills/intelligent-router/scripts/router.py models

# Detailed scoring breakdown
python3 skills/intelligent-router/scripts/router.py score "task"

# Config health check
python3 skills/intelligent-router/scripts/router.py health

# Auto-discover working models (NEW)
python3 skills/intelligent-router/scripts/discover_models.py

# Auto-discover + update config
python3 skills/intelligent-router/scripts/discover_models.py --auto-update

# Test specific tier only
python3 skills/intelligent-router/scripts/discover_models.py --tier COMPLEX
```

---

## 评分系统

评分系统采用 15 个维度的加权评分标准（不仅仅基于关键词）：

1. **推理能力**（0.18）：是否需要证明、推导等逻辑操作
2. **代码含量**（0.15）：代码块的数量及文件扩展名
3. **多步骤逻辑结构**（0.12）：任务是否包含明确的步骤顺序
4. **任务的执行类型**（0.10）：是否涉及运行、修复、部署等操作
5. **技术术语的使用**（0.10）：文档中是否包含技术术语（如架构、安全、协议等）
6. **文本长度**（0.08）：文本的复杂度（通过长度判断）
7. **创造性表达**（0.05）：文档中是否包含创意性内容（如故事叙述、头脑风暴等）
8. **问题的复杂性**（0.05）：问题中是否包含多个“谁/什么/如何”等要素
9. **约束条件**（0.04）：任务是否具有明确的约束条件
10. **命令动词的使用**（0.03）：文档中是否使用命令式动词（如分析、评估等）
11. **输出格式**（0.03）：输出格式是否为 JSON、表格或 Markdown
12. **基本操作**（0.02）：文档中是否包含基本的检查、获取、显示等操作
13. **领域特异性**（0.02）：文档内容是否与特定领域相关（如使用缩写、点表示法等）
14. **参考内容的依赖性**（0.02）：文档中是否引用了其他内容
15. **否定表达的复杂性**（0.01）：文档中是否包含否定词（如“不”、“从未”等）

**置信度计算公式**：`1 / (1 + exp(-8 × (得分 - 0.5)))`

---

## 配置设置

模型信息存储在 `config.json` 文件中。新增模型时，智能路由器会自动识别并使用这些模型。本地 Ollama 模型的使用成本为零，因此简单任务优先选择这些模型。

---

## 自动发现机制（自我修复功能）

智能路由器能够**自动从所有已配置的模型提供者中找到可用模型**：

### 工作原理：

1. **模型提供者扫描**：读取 `~/.openclaw/openclaw.json` 文件，测试每个模型的可用性
2. **健康检查**：发送简单的测试请求以验证模型的认证状态和连接性
3. **自动分类**：根据模型的成本、功能及提供者类型对其进行分类
4. **配置更新**：替换无法使用的模型（例如失效的 OAuth 令牌）
5. **定时任务集成**：每小时更新模型列表，确保其始终是最新的

### 使用方法

```bash
# One-time discovery
python3 skills/intelligent-router/scripts/discover_models.py

# Auto-update config with working models only
python3 skills/intelligent-router/scripts/discover_models.py --auto-update

# Set up hourly refresh cron
openclaw cron add --job '{
  "name": "Model Discovery Refresh",
  "schedule": {"kind": "every", "everyMs": 3600000},
  "payload": {
    "kind": "systemEvent",
    "text": "Run: bash skills/intelligent-router/scripts/auto_refresh_models.sh",
    "model": "ollama/glm-4.7-flash"
  }
}'
```

### 主要优势：

✅ **自我修复**：自动移除失效的模型（如过期的 OAuth 令牌）
✅ **零维护成本**：无需手动更新模型列表
✅ **自动更新**：新发布的模型会自动被添加到使用列表中
✅ **成本优化**：始终使用每个难度等级下最便宜且可用的模型

### 发现结果存储位置

发现的结果会保存在 `skills/intelligent-router/discovered-models.json` 文件中：
```json
{
  "scan_timestamp": "2026-02-19T21:00:00",
  "total_models": 25,
  "available_models": 23,
  "unavailable_models": 2,
  "providers": {
    "anthropic": {
      "available": 2,
      "unavailable": 0,
      "models": [...]
    }
  }
}
```

### 固定模型的使用

即使某个模型在自动发现过程中被标记为不可用，也可以通过特定配置将其固定下来，确保该模型仍能被使用：
```json
{
  "id": "special-model",
  "tier": "COMPLEX",
  "pinned": true  // Never remove during auto-update
}
```