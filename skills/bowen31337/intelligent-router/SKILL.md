---
name: intelligent-router
description: 智能模型路由机制用于子代理任务的分配。根据任务的复杂性、成本和能力要求来选择最合适的模型。通过将简单任务分配给成本更低的模型来降低成本，同时确保复杂任务的执行质量不受影响。
version: 3.2.0
core: true
---
# 智能路由器 — 核心技能

> **核心技能**：此技能属于基础设施层面，而非指导性内容。需通过运行 `bash skills/intelligent-router/install.sh` 命令来激活该技能。

## 功能概述

该技能能够自动将任务分类为不同的难度等级（简单/中等/复杂/需要推理/关键），并推荐最适合处理该任务的模型（同时确保成本最低）。

**解决的问题**：在没有路由机制的情况下，所有定时任务（cron job）和子代理（sub-agent）都会默认使用成本较高的 Sonnet 模型；而通过路由机制，监控任务可以使用免费的本地模型，从而节省 80-95% 的成本。

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

### 注意：**严禁** 违反这些规则：
```python
# Cron job without model = Sonnet default = expensive waste
{"kind": "agentTurn", "message": "check server..."}  # ← WRONG
```

### 正确的操作方式：
```python
# Always specify model from router recommendation
{"kind": "agentTurn", "message": "check server...", "model": "ollama/glm-4.7-flash"}
```

---

## 任务难度等级系统

| 等级 | 适用场景 | 主要使用的模型 | 成本（美元/分钟） |
|------|---------|---------------|------|
| 🟢 简单 | 监控、心跳检测、数据汇总 | `anthropic-proxy-6/glm-4.7`（备用：proxy-4） | $0.50/分钟 |
| 🟡 中等 | 代码修复、补丁应用、数据分析 | `nvidia-nim/meta/llama-3.3-70b-instruct` | $0.40/分钟 |
| 🟠 复杂 | 新功能开发、架构设计、多文件处理、调试 | `anthropic/claude-sonnet-4-6` | $3.00/分钟 |
| 🔵 需要推理的任务 | 证明性逻辑处理、深度分析 | `nvidia-nim/moonshotai/kimi-k2-thinking` | $1.00/分钟 |
| 🔴 关键任务 | 安全相关、生产环境、高风险操作 | `anthropic/claude-opus-4-6` | $5.00/分钟 |

**简单任务的默认处理流程**：`anthropic-proxy-4/glm-4.7` → `nvidia-nim/qwen/qwen2.5-7b-instruct`（$0.15/分钟）

> ⚠️ **`ollama-gpu-server` 禁止用于定时任务或子代理的创建**。Ollama 模型默认绑定到 `127.0.0.1` 地址，而 OpenClaw 主机无法通过局域网访问该地址；`router_policy.py` 会拒绝任何引用该服务器的定时任务。

**等级分类依据**（不仅考虑成本）：
- `effective_params`（50%）：从模型 ID 或 `known-model-params.json` 文件中提取的参数
- `context_window`（20%）：模型处理上下文的复杂度
- `cost_input`（20%）：模型价格（作为质量参考，适用于未知规模的场景）
- `reasoning_flag`（10%）：专为需要高级推理能力的任务设计的模型（如 R1、QwQ、Kimi-K2）

---

## 策略执行器（v3.2.0 新功能）

`router_policy.py` 会在模型被创建之前就检测并阻止错误的模型分配。

### 在提交定时任务之前进行验证：
```bash
python3 skills/intelligent-router/scripts/router_policy.py check \
  '{"kind":"agentTurn","model":"ollama-gpu-server/glm-4.7-flash","message":"check server"}'
# Output: VIOLATION: Blocked model 'ollama-gpu-server/glm-4.7-flash'. Recommended: anthropic-proxy-6/glm-4.7
```

### 获取任务所需的推荐模型：
```bash
python3 skills/intelligent-router/scripts/router_policy.py recommend "monitor alphastrike service"
# Output: Tier: SIMPLE  Model: anthropic-proxy-6/glm-4.7

python3 skills/intelligent-router/scripts/router_policy.py recommend "monitor alphastrike service" --alt
# Output: Tier: SIMPLE  Model: anthropic-proxy-4/glm-4.7  ← alternate key for load distribution
```

### 审查所有现有的定时任务：
```bash
python3 skills/intelligent-router/scripts/router_policy.py audit
# Scans all crons, reports any with blocked or missing models
```

### 显示被禁止使用的模型列表：
```bash
python3 skills/intelligent-router/scripts/router_policy.py blocklist
```

### 策略规则：
1. **必须设置模型**：如果任务中未指定模型，将默认使用成本较高的 Sonnet 模型。
2. **禁止使用被禁止的模型**：`ollama-gpu-server/*` 和 `ollama/*` 系列的模型不能用于定时任务。
3. **关键任务**：如果使用非 `anthropic/claude-opus-4-6` 模型，系统会发出警告。

---

## 安装步骤（核心技能的配置）

运行一次安装脚本，即可将此技能集成到 `agents.md` 文件中：
```bash
bash skills/intelligent-router/install.sh
```

该脚本会更新 `agents.md` 文件中的强制性协议内容，确保所有任务都能遵循这些规则。

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

1. **推理能力**（0.18 分）：涉及证明、定理推导等逻辑操作
2. **代码含量**（0.15 分）：代码块、文件扩展名等代码相关元素
3. **任务复杂性**（0.12 分）：任务是否包含多步骤操作或需要按顺序执行
4. **任务性质**（0.10 分）：任务是否涉及运行、修复、部署或构建等操作
5. **技术术语的使用**（0.10 分）：文档中是否包含技术术语（如架构、安全、协议等）
6. **文本长度**（0.08 分）：文本长度反映任务的复杂性
7 **创造性**（0.05 分）：文档中是否包含故事叙述、创意构思或头脑风暴内容
8. **问题复杂性**（0.05 分）：问题是否涉及多个主体、对象或执行方式
9. **约束条件**（0.04 分）：任务是否包含明确的约束或要求
10. **命令动词**（0.03 分）：文档中是否使用命令式动词（如分析、评估、审计等）
11 **输出格式**（0.03 分）：输出格式是否为 JSON、表格或 Markdown
12 **简单性**（0.02 分）：文档是否包含简单的检查、获取或显示操作
13 **领域特异性**（0.02 分）：文档中是否使用缩写或点状表示法
14 **引用复杂性**（0.02 分）：文档中是否提及其他参考资料
15 **否定表达**（0.01 分）：文档中是否包含否定或例外情况的表述

**评分公式**：`Confidence = 1 / (1 + exp(-8 × (score - 0.5)))`

---

## 配置设置

模型信息存储在 `config.json` 文件中。新增模型时，系统会自动识别并使用它们。本地 Ollama 模型的使用成本为零，因此在简单任务中优先选择这些模型。

---

## 自动发现机制

智能路由器能够通过实时推理测试自动识别可用模型（而非仅依赖配置文件的存在性检查）。

### 工作原理：

1. **模型扫描**：读取 `~/.openclaw/openclaw.json` 文件，列出所有可用的模型。
2. **实时推理测试**：向每个模型发送请求 „hi“，检查模型是否能够正常响应（排除认证失败、配额耗尽、404 错误或超时等情况）。
3. **OAuth 优化**：使用 `sk-ant-oat01-*` 令牌（Anthropic OAuth）的模型在 HTTP 请求中会被自动跳过；OpenClaw 会自动更新这些模型的可用状态。
4. **推理能力判断**：返回 `content=None` 且 `reasoning_content` 不为空的模型（如 GLM-4.7、Kimi-K2、Qwen3-thinking）会被正确识别为可用模型。
5. **模型分级**：使用 `tier_classifier.py` 根据 4 个指标对模型进行分类。
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

### 功能优势：

- **自动修复**：系统会自动移除无法正常使用的模型（例如 OAuth 令牌过期的模型）。
- **零维护**：无需手动更新模型列表。
- **自动更新**：新发布的模型会自动被添加到可用模型列表中。
- **成本优化**：系统始终会选择每个等级中最便宜且可用的模型。

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

即使模型在初次检测时无法使用，系统也会将其保留：

```json
{
  "id": "special-model",
  "tier": "COMPLEX",
  "pinned": true  // Never remove during auto-update
}
```

## 注意事项（2026-03-04）：当前路由机制仍为被动式，而非主动式：
- 只有在收到 429 错误代码后才会触发备用模型。
- 系统无法识别同一代理上的多个并发请求。
- 系统无法跟踪并发请求的冷却时间。

**需要改进的地方**：
1. 记录每个提供者的最近一次 429 错误时间，如果在冷却期内则跳过该提供者的模型。
2. 记录每个提供者的并发请求数量，如果并发请求超过一定数量，则优先使用 OAuth 服务。
3. 在创建多个子代理之前，需要检查单个提供者是否能够处理这些并发请求。
4. 提供 `router.get_best_available(n_concurrent=2)` 的 API，以便更方便地获取最佳可用模型。