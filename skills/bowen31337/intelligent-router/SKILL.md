---
name: intelligent-router
description: 智能模型路由系统用于子代理任务的分配。根据任务的复杂性、成本和能力要求来选择最合适的模型。通过将简单任务分配给成本更低的模型来降低成本，同时确保复杂任务的质量不受影响。
version: 3.2.0
core: true
---
# 智能路由器——核心技能

> **核心技能**：此技能属于基础设施范畴，而非指导性内容。需通过运行 `bash skills/intelligent-router/install.sh` 命令来激活该技能。

## 功能概述

该技能能够自动将任务分类为不同的难度等级（简单/中等/复杂/需要推理/关键），并推荐最适合处理该任务的模型（同时确保成本最低）。

**解决的问题**：在没有路由机制的情况下，所有定时任务（cron jobs）和子代理（sub-agents）默认会使用成本较高的 Sonnet 模型；而通过路由机制后，监控任务可以使用免费的本地模型，从而节省 80% 至 95% 的成本。

---

## 强制性协议（通过 AGENTS.md 文件实施）

### 在创建任何子代理之前：
```bash
python3 skills/intelligent-router/scripts/router.py classify "task description"
```

### 在创建任何定时任务之前：
```bash
python3 skills/intelligent-router/scripts/spawn_helper.py "task description"
# Outputs the exact model ID and payload snippet to use
```

### 验证定时任务是否已设置合适的模型：
```bash
python3 skills/intelligent-router/scripts/spawn_helper.py --validate '{"kind":"agentTurn","message":"..."}'
```

### ❌ 禁止的行为：
```python
# Cron job without model = Sonnet default = expensive waste
{"kind": "agentTurn", "message": "check server..."}  # ← WRONG
```

### ✅ 正确的操作：
```python
# Always specify model from router recommendation
{"kind": "agentTurn", "message": "check server...", "model": "ollama/glm-4.7-flash"}
```

---

## 任务难度等级划分

| 等级 | 适用场景 | 主要使用的模型 | 成本（美元/分钟） |
|------|---------|---------------|------|
| 🟢 简单 | 监控、心跳检测、数据汇总 | `anthropic-proxy-6/glm-4.7`（备用：proxy-4） | 0.50美元/分钟 |
| 🟡 中等 | 代码修复、补丁应用、数据分析 | `nvidia-nim/meta/llama-3.3-70b-instruct` | 0.40美元/分钟 |
| 🟠 复杂 | 新功能开发、架构设计、多文件处理、调试 | `anthropic/claude-sonnet-4-6` | 3美元/分钟 |
| 🔵 需要推理 | 逻辑验证、深度分析 | `nvidia-nim/moonshotai/kimi-k2-thinking` | 1美元/分钟 |
| 🔴 关键 | 安全相关任务、生产环境 | `anthropic/claude-opus-4-6` | 5美元/分钟 |

**简单任务的默认处理流程**：`anthropic-proxy-4/glm-4.7` → `nvidia-nim/qwen/qwen2.5-7b-instruct`（0.15美元/分钟）

> ⚠️ **`ollama-gpu-server` 被禁止用于定时任务或子代理的创建**。Ollama 模型默认绑定到 `127.0.0.1` 地址，OpenClaw 主机无法通过局域网访问该地址；`router_policy.py` 会拒绝任何引用该地址的定时任务。

**等级划分依据**（不仅考虑成本）：
- `effective_params`（50%）：从模型 ID 或 `known-model-params.json` 文件中提取的参数
- `context_window`（20%）：模型处理的数据量越大，能力越强
- `cost_input`（20%）：价格可作为模型质量的参考（但参考价值较低，主要用于未知规模的场景）
- `reasoning_flag`（10%）：针对需要专门推理能力的任务（如 R1、QwQ、Kimi-K2 模型）

---

## 策略执行器（v3.2.0 新功能）

`router_policy.py` 会在模型被创建之前就检查其是否合适，而非在任务执行失败后才进行验证。

### 在提交定时任务之前验证模型：
```bash
python3 skills/intelligent-router/scripts/router_policy.py check \
  '{"kind":"agentTurn","model":"ollama-gpu-server/glm-4.7-flash","message":"check server"}'
# Output: VIOLATION: Blocked model 'ollama-gpu-server/glm-4.7-flash'. Recommended: anthropic-proxy-6/glm-4.7
```

### 获取任务的推荐模型：
```bash
python3 skills/intelligent-router/scripts/router_policy.py recommend "monitor alphastrike service"
# Output: Tier: SIMPLE  Model: anthropic-proxy-6/glm-4.7

python3 skills/intelligent-router/scripts/router_policy.py recommend "monitor alphastrike service" --alt
# Output: Tier: SIMPLE  Model: anthropic-proxy-4/glm-4.7  ← alternate key for load distribution
```

### 审计所有现有的定时任务：
```bash
python3 skills/intelligent-router/scripts/router_policy.py audit
# Scans all crons, reports any with blocked or missing models
```

### 显示被禁止使用的模型列表：
```bash
python3 skills/intelligent-router/scripts/router_policy.py blocklist
```

### 策略规则：
1. **必须设置模型**：如果定时任务中未指定模型，将默认使用 Sonnet 模型，从而导致成本浪费。
2. **禁止使用被禁止的模型**：`ollama-gpu-server/*` 及类似的模型无法用于定时任务。
3. **关键任务**：如果使用非 Opus 系列的模型进行关键任务处理，系统会发出警告。

---

## 安装（核心技能的配置）

只需运行一次安装命令，该技能就会自动集成到 `AGENTS.md` 文件中，确保所有相关配置始终符合规定。

---

## 命令行接口（CLI）参考

```bash
# ── Policy enforcer (run before creating any cron/spawn) ──
python3 skills/intelligent-router/scripts/router_policy.py check '{"kind":"agentTurn","model":"...","message":"..."}'
python3 skills/intelligent-router/scripts/router_policy.py recommend "task description"
python3 skills/intelligent-router/scripts/router_policy.py recommend "task" --alt  # alternate proxy key
python3 skills/intelligent-router/scripts/router_policy.py audit     # scan all crons
python3 skills/intelligent-router/scripts/router_policy.py blocklist

# ── Core router ──
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

1. **推理能力**（0.18 分）：是否涉及证明、定理推导等逻辑操作
2. **代码含量**（0.15 分）：代码块的存在与否、文件扩展名
3. **任务复杂性**（0.12 分）：任务是否包含多步骤操作或有序列表
4. **任务性质**（0.10 分）：任务是否涉及运行、修复、部署或构建等操作
5. **技术术语使用**（0.10 分）：文档中是否包含技术术语（如架构、安全、协议等）
6. **文本长度**（0.08 分）：文本长度反映任务的复杂性
7 **创造性**（0.05 分）：文档中是否包含故事叙述、创意表达或头脑风暴内容
8. **问题复杂性**（0.05 分）：问题是否包含多个“谁/什么/如何”等要素
9. **约束条件**（0.04 分）：任务是否包含明确的约束条件
10. **命令动词**（0.03 分）：文档中是否使用命令式动词（如分析、评估、审计等）
11 **输出格式**（0.03 分）：输出格式是否为 JSON、表格或 Markdown
12 **简单性**（0.02 分）：文档结构是否简单（如是否包含检查、获取、显示等操作）
13 **领域特异性**（0.02 分）：文档内容是否涉及特定领域（如缩写、点表示法等）
14 **引用复杂性**（0.02 分）：文档中是否提及其他参考资料
15 **否定表达**（0.01 分）：文档中是否包含否定词（如“不”、“从未”等）

**评分公式**：`Confidence = 1 / (1 + exp(-8 × (score - 0.5)))`

---

## 配置设置

模型信息存储在 `config.json` 文件中。新增模型后，智能路由器会自动识别并使用它们。本地部署的 Ollama 模型使用成本为零，因此在简单任务中优先选择这些模型。

---

## 自动发现机制（自我修复功能）

智能路由器能够通过实时推理测试，自动识别出可用的模型：

### 工作原理：

1. **模型扫描**：读取 `~/.openclaw/openclaw.json` 文件，列出所有可用的模型。
2. **实时推理测试**：向每个模型发送请求 “hi”，检查模型是否能够正常响应（排除身份验证失败、配额耗尽、404 错误或超时等情况）。
3. **OAuth 优化**：使用 `sk-ant-oat01-*` 令牌（Anthropic 提供的 OAuth 令牌）的模型会在 HTTP 请求中被跳过；OpenClaw 会自动更新这些模型的可用状态。
4. **推理能力判断**：返回 `content=None` 且 `reasoning_content` 不为空的模型（如 GLM-4.7、Kimi-K2、Qwen3-thinking）会被正确识别为可用模型。
5. **模型等级划分**：使用 `tier_classifier.py` 根据 4 个关键指标对模型进行分类。
6. **配置更新**：系统会自动移除不可用的模型，并重新确定各等级的默认模型。
7. **定时任务更新**：每小时自动更新模型列表（定时任务 ID：`a8992c1f`），并在模型可用性发生变化时发出警报。

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

✅ **自我修复**：自动移除无法使用的模型（例如过期的 OAuth 令牌）。
✅ **无需维护**：无需手动更新模型列表。
✅ **自动更新**：新发布的模型会自动被添加到可用模型列表中。
✅ **成本优化**：始终使用每个等级中最便宜的可用模型。

### 发现结果保存位置

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

### 固定模型

即使模型在初次发现时不可用，也可以通过特定配置将其固定为可用状态：

```json
{
  "id": "special-model",
  "tier": "COMPLEX",
  "pinned": true  // Never remove during auto-update
}
```