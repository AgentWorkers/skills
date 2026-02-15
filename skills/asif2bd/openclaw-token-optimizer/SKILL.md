---
name: token-optimizer
description: 通过智能模型路由、心跳信号优化、预算跟踪以及多供应商备用方案来减少 OpenClaw 的令牌使用量和 API 成本。当令牌成本较高、API 使用频率达到限制，或需要大规模托管多个代理时，建议采用这些方法。系统提供了可用于任务分类、使用情况监控以及优化心跳信号调度的现成脚本。所有操作仅基于本地文件分析，无需进行网络请求或代码执行。详情请参阅 SECURITY.md。
---

# 令牌优化器

这是一个全面的工具包，用于减少 OpenClaw 部署中的令牌使用量和 API 成本。它结合了智能模型路由、优化的心跳间隔、使用情况跟踪以及多提供商策略。

## 快速入门

**立即可执行的操作**（无需配置更改）：

1. **生成优化的 AGENTS.md 文件（最大的节省！）：**
   ```bash
   python3 scripts/context_optimizer.py generate-agents
   # Creates AGENTS.md.optimized — review and replace your current AGENTS.md
   ```

2. **检查您实际需要的上下文内容：**
   ```bash
   python3 scripts/context_optimizer.py recommend "hi, how are you?"
   # Shows: Only 2 files needed (not 50+!)
   ```

3. **安装优化后的心跳机制：**
   ```bash
   cp assets/HEARTBEAT.template.md ~/.openclaw/workspace/HEARTBEAT.md
   ```

4. **为日常聊天使用成本较低的模型：**
   ```bash
   python3 scripts/model_router.py "thanks!"
   # Shows: Use Haiku, not Opus!
   ```

5. **检查当前的令牌预算：**
   ```bash
   python3 scripts/token_tracker.py check
   ```

**预期节省效果：**对于典型工作负载，令牌成本可降低 50-80%（上下文优化是最大的节省因素！）

## 核心功能

### 1. 上下文优化（新功能！）

**最大的令牌节省方式** — 只加载您实际需要的文件，而不仅仅是全部文件。

**问题：** 默认情况下，OpenClaw 会在每次会话中加载所有上下文文件：
- SOUL.md、AGENTS.md、USER.md、TOOLS.md、MEMORY.md
- docs/**/*.md（数百个文件）
- memory/2026-*.md（每日日志）
- 总计：通常在用户说话之前就已经使用了 50,000 多个令牌！

**解决方案：** 根据提示的复杂性进行延迟加载。

**使用方法：**
```bash
python3 scripts/context_optimizer.py recommend "<user prompt>"
```

**示例：**
```bash
# Simple greeting → minimal context (2 files only!)
context_optimizer.py recommend "hi"
→ Load: SOUL.md, IDENTITY.md
→ Skip: Everything else
→ Savings: ~80% of context

# Standard work → selective loading
context_optimizer.py recommend "write a function"
→ Load: SOUL.md, IDENTITY.md, memory/TODAY.md
→ Skip: docs, old memory, knowledge base
→ Savings: ~50% of context

# Complex task → full context
context_optimizer.py recommend "analyze our entire architecture"
→ Load: SOUL.md, IDENTITY.md, MEMORY.md, memory/TODAY+YESTERDAY.md
→ Conditionally load: Relevant docs only
→ Savings: ~30% of context
```

**输出格式：**
```json
{
  "complexity": "simple",
  "context_level": "minimal",
  "recommended_files": ["SOUL.md", "IDENTITY.md"],
  "file_count": 2,
  "savings_percent": 80,
  "skip_patterns": ["docs/**/*.md", "memory/20*.md"]
}
```

**集成模式：**
在为新会话加载上下文之前：
```python
from context_optimizer import recommend_context_bundle

user_prompt = "thanks for your help"
recommendation = recommend_context_bundle(user_prompt)

if recommendation["context_level"] == "minimal":
    # Load only SOUL.md + IDENTITY.md
    # Skip everything else
    # Save ~80% tokens!
```

**生成优化的 AGENTS.md 文件：**
```bash
context_optimizer.py generate-agents
# Creates AGENTS.md.optimized with lazy loading instructions
# Review and replace your current AGENTS.md
```

**预期节省效果：**上下文令牌使用量可降低 50-80%。

### 2. 智能模型路由（增强功能！）

自动对任务进行分类，并将其路由到合适的模型层级。

**新功能：** 强制使用通信模式 — 永远不要在“hi”或“thanks”等简单消息上浪费 Opus 令牌！

**使用方法：**
```bash
python3 scripts/model_router.py "<user prompt>" [current_model] [force_tier]
```

**示例：**
```bash
# Communication (NEW!) → ALWAYS Haiku
python3 scripts/model_router.py "thanks!"
python3 scripts/model_router.py "hi"
python3 scripts/model_router.py "ok got it"
→ Enforced: Haiku (NEVER Sonnet/Opus for casual chat)

# Simple task → suggests Haiku
python3 scripts/model_router.py "read the log file"

# Medium task → suggests Sonnet
python3 scripts/model_router.py "write a function to parse JSON"

# Complex task → suggests Opus
python3 scripts/model_router.py "design a microservices architecture"
```

**强制使用的通信模式（仅限 Haiku，禁止使用 Sonnet/Opus）：**

* 问候语：hi, hey, hello, yo
* 感谢：thanks, thank you, thx
* 回应：ok, sure, got it, understood
* 简短回答：yes, no, yep, nope
* 单个单词或非常短的短语

* 背景任务：**
- 心跳检查：check email, monitor servers
- 定时任务：scheduled task, periodic check, reminder
- 文档解析：parse CSV, extract data from log, read JSON
- 日志扫描：scan error logs, process logs

**集成模式：**
```python
from model_router import route_task

user_prompt = "show me the config"
routing = route_task(user_prompt)

if routing["should_switch"]:
    # Use routing["recommended_model"]
    # Save routing["cost_savings_percent"]
```

**自定义：**
在 `scripts/model_router.py` 中编辑 `ROUTING_RULES` 或 `COMMUNICATION_PATTERNS` 以调整模式和关键词。

### 3. 心跳优化

通过智能间隔跟踪，减少心跳轮询中的 API 调用次数：

**设置：**
```bash
# Copy template to workspace
cp assets/HEARTBEAT.template.md ~/.openclaw/workspace/HEARTBEAT.md

# Plan which checks should run
python3 scripts/heartbeat_optimizer.py plan
```

**命令：**
```bash
# Check if specific type should run now
heartbeat_optimizer.py check email
heartbeat_optimizer.py check calendar

# Record that a check was performed
heartbeat_optimizer.py record email

# Update check interval (seconds)
heartbeat_optimizer.py interval email 7200  # 2 hours

# Reset state
heartbeat_optimizer.py reset
```

**工作原理：**
- 记录每种类型的最后检查时间（电子邮件、日历、天气等）
- 强制规定重新检查的最小间隔
- 遵守安静时段（23:00-08:00） — 跳过所有检查
- 当没有需要处理的内容时返回 `HEARTBEAT_OK`（节省令牌）

**默认间隔：**
- 电子邮件：60 分钟
- 日历：2 小时
- 天气：4 小时
- 社交：2 小时
- 监控：30 分钟

**在 HEARTBEAT.md 中的集成：**
```markdown
## Email Check
Run only if: `heartbeat_optimizer.py check email` → `should_check: true`
After checking: `heartbeat_optimizer.py record email`
```

**预期节省效果：**心跳 API 调用次数可减少 50%。

**模型强制规定：** 心跳始终应使用 Haiku 模型 — 请参阅更新后的 `HEARTBEAT.template.md` 以获取模型覆盖说明。

### 4. 定时任务优化（新功能！）

**问题：** 即使是常规任务，定时任务也经常默认使用成本较高的模型（Sonnet/Opus）。

**解决方案：** 90% 的定时任务都应指定使用 Haiku 模型。

**参见：** `assets/cronjob-model-guide.md` 以获取包含示例的完整指南。

**快速参考：**

| 任务类型 | 模型 | 示例 |
|-----------|-------|---------|
| 监控/警报 | Haiku | 检查服务器健康状况、磁盘空间 |
| 数据解析 | Haiku | 解析 CSV/JSON/日志 |
| 提醒 | Haiku | 每日站会、备份提醒 |
| 简单报告 | Haiku | 状态摘要 |
| 内容生成 | Sonnet | 博文摘要（质量要求较高） |
| 深度分析 | Sonnet | 周度洞察 |
| 复杂推理 | 定时任务中永远不要使用 Opus |

**示例（正确用法）：**
```bash
# Parse daily logs with Haiku
cron add --schedule "0 2 * * *" \
  --payload '{
    "kind":"agentTurn",
    "message":"Parse yesterday error logs and summarize",
    "model":"anthropic/claude-haiku-4"
  }' \
  --sessionTarget isolated
```

**示例（错误用法）：**
```bash
# ❌ Using Opus for simple check (60x more expensive!)
cron add --schedule "*/15 * * * *" \
  --payload '{
    "kind":"agentTurn",
    "message":"Check email",
    "model":"anthropic/claude-opus-4"
  }' \
  --sessionTarget isolated
```

**节省效果：** 对于 10 个每日定时任务，使用 Haiku 而不是 Opus 每个代理每月可节省 $17.70。**

**与 model_router 的集成：**
```bash
# Test if your cronjob should use Haiku
model_router.py "parse daily error logs"
# → Output: Haiku (background task pattern detected)
```

### 5. 令牌预算跟踪**

监控令牌使用情况，并在接近预算限制时发出警报：

**设置：**
```bash
# Check current daily usage
python3 scripts/token_tracker.py check

# Get model suggestions
python3 scripts/token_tracker.py suggest general

# Reset daily tracking
python3 scripts/token_tracker.py reset
```

**输出格式：**
```json
{
  "date": "2026-02-06",
  "cost": 2.50,
  "tokens": 50000,
  "limit": 5.00,
  "percent_used": 50,
  "status": "ok",
  "alert": null
}
```

**状态等级：**
- `ok`：低于每日预算的 80%
- `warning`：达到每日预算的 80-99%
- `exceeded`：超过每日预算

**集成模式：**
在开始高成本操作之前，检查预算：
```python
import json
import subprocess

result = subprocess.run(
    ["python3", "scripts/token_tracker.py", "check"],
    capture_output=True, text=True
)
budget = json.loads(result.stdout)

if budget["status"] == "exceeded":
    # Switch to cheaper model or defer non-urgent work
    use_model = "anthropic/claude-haiku-4"
elif budget["status"] == "warning":
    # Use balanced model
    use_model = "anthropic/claude-sonnet-4-5"
```

**自定义：**
在函数调用中编辑 `daily_limit_usd` 和 `warn_threshold` 参数。

### 6. 多提供商策略

请参阅 `references/PROVIDERS.md` 以获取以下内容的完整指南：
- 替代提供商（OpenRouter、Together.ai、Google AI Studio）
- 成本对比表
- 根据任务复杂性选择的路由策略
- 针对速率限制情况的备用方案
- API 密钥管理

**快速参考：**

| 提供商 | 模型 | 成本/MTok | 使用场景 |
|----------|-------|-----------|----------|
| Anthropic | Haiku 4 | $0.25 | 简单任务 |
| Anthropic | Sonnet 4.5 | $3.00 | 平衡默认配置 |
| Anthropic | Opus 4 | $15.00 | 复杂推理 |
| OpenRouter | Gemini 2.5 Flash | $0.075 | 批量操作 |
| Google AI | Gemini 2.0 Flash Exp | 免费 | 开发/测试 |
| Together | Llama 3.3 70B | $0.18 | 开源替代方案 |

## 配置补丁

请参阅 `assets/config-patches.json` 以获取高级优化设置：

**此技能已实现的功能：**
- ✅ 心跳优化（完全可用）
- ✅ 令牌预算跟踪（完全可用）
- ✅ 模型路由逻辑（完全可用）

**需要 OpenClaw 核心支持的功能：**
- ⏳ 提示缓存（Anthropic API 功能，OpenClaw 集成待定）
- ⏳ 延迟上下文加载（需要核心代码更改）
- ⏳ 多提供商备用方案（部分支持）

**应用配置补丁：**
```bash
# Example: Enable multi-provider fallback
gateway config.patch --patch '{"providers": [...]}'
```

## 部署模式

### 个人使用
1. 安装优化的 `HEARTBEAT.md`
2. 在执行高成本操作前检查预算
3. 仅在需要时手动将复杂任务路由到 Opus 模型

**预期节省效果：** 20-30%

### 管理型托管（如 xCloud 等）
1. 将所有代理默认设置为使用 Haiku 模型
2. 将用户交互路由到 Sonnet 模型
3. 仅将 Opus 模型用于特别复杂的请求
4. 对后台操作使用 Gemini Flash 模型
5. 为每个客户设置每日预算上限

**预期节省效果：** 40-60%

### 高容量部署
1. 使用多提供商备用方案（OpenRouter + Together.ai）
2. 实施积极的路由策略（80% 使用 Gemini，15% 使用 Haiku，5% 使用 Sonnet）
3. 部署本地的 Ollama 模型用于离线/低成本操作
4. 批量执行心跳检查（每 2-4 小时一次，而不是每 30 分钟）

**预期节省效果：** 70-90%

## 集成示例

### 工作流程：智能任务处理
```bash
# 1. User sends message
user_msg="debug this error in the logs"

# 2. Route to appropriate model
routing=$(python3 scripts/model_router.py "$user_msg")
model=$(echo $routing | jq -r .recommended_model)

# 3. Check budget before proceeding
budget=$(python3 scripts/token_tracker.py check)
status=$(echo $budget | jq -r .status)

if [ "$status" = "exceeded" ]; then
    # Use cheapest model regardless of routing
    model="anthropic/claude-haiku-4"
fi

# 4. Process with selected model
# (OpenClaw handles this via config or override)
```

### 工作流程：优化心跳机制
```markdown
## HEARTBEAT.md

# Plan what to check
result=$(python3 scripts/heartbeat_optimizer.py plan)
should_run=$(echo $result | jq -r .should_run)

if [ "$should_run" = "false" ]; then
    echo "HEARTBEAT_OK"
    exit 0
fi

# Run only planned checks
planned=$(echo $result | jq -r '.planned[].type')

for check in $planned; do
    case $check in
        email) check_email ;;
        calendar) check_calendar ;;
    esac
    python3 scripts/heartbeat_optimizer.py record $check
done
```

## 故障排除

**问题：** 脚本出现“模块未找到”的错误**
- **解决方法：** 确保已安装 Python 3.7 或更高版本。脚本仅使用标准库。

**问题：** 状态文件无法持久化**
- **解决方法：** 检查 `~/.openclaw/workspace/memory/` 目录是否存在且可写入。

**问题：** 预算跟踪显示为 $0.00**
- **解决方法：** `token_tracker.py` 需要与 OpenClaw 的 `session_status` 工具集成。目前是手动记录使用情况。

**问题：** 路由建议错误的模型层级**
- **解决方法：** 在 `model.router.py` 中自定义 `ROUTING_RULES` 以适应您的特定模式。

## 维护

**每日：**
- 检查预算状态：`token_tracker.py check`

**每周：**
- 审查路由准确性（建议是否正确？）
- 根据活动情况调整心跳间隔

**每月：**
- 比较优化前后的成本
- 审查并更新 `PROVIDERS.md` 中的选项

## 成本估算

**示例：每天使用 100,000 个令牌的工作负载**

**不使用此技能时：**
- 50,000 个上下文令牌 + 50,000 个对话令牌 = 总计 100,000 个令牌
- 全部使用 Sonnet 模型：100,000 × $3/MTok = 每天 $0.30 = 每月 $9**

| 策略 | 上下文 | 模型 | 日成本 | 每月成本 | 节省金额 |
|----------|---------|-------|-----------|---------|---------|
| 基线（无优化） | 50,000 | Sonnet | $0.30 | $9.00 | 0% |
| 仅优化上下文 | 10,000 | Sonnet | $0.18 | $5.40 | 40% |
| 仅优化模型路由 | 50,000 | 混合模型 | $0.18 | $5.40 | 40% |
| **同时使用这两种策略** | 10,000 | 混合模型 | $0.09 | $2.70 | 70% |
| 使用 Gemini 模型（更激进策略） | 10,000 | Gemini | $0.03 | $0.90 | 90% |

**关键洞察：** 上下文优化（从 50,000 个令牌减少到 10,000 个令牌）的节省效果更显著！

**xCloud 托管场景**（100 位客户，每位客户每天使用 50,000 个令牌）：
- 基线（全部使用 Sonnet 模型）：每月 $450
- 使用令牌优化器后：每月 $135
- **节省金额：每位客户每月 $315（节省 70%）**

## 资源

### 脚本（共 4 个）
- **`context_optimizer.py`** — 上下文加载优化和延迟加载（新功能！）
- **`model_router.py`** — 任务分类、模型推荐和通信模式强制执行（增强功能！）
- **`heartbeat_optimizer.py`** — 间隔管理和检查调度
- **`token_tracker.py`** — 预算监控和警报

### 参考资料
- `PROVIDERS.md` — 替代 AI 提供商、定价和路由策略

### 资源文件（共 3 个）
- **`HEARTBEAT.template.md` — 带有 Haiku 模型强制执行的优化心跳模板（增强功能！）
- **`cronjob-model-guide.md** — 选择定时任务模型的完整指南（新功能！）
- **`config-patches.json** — 高级配置示例

## 未来改进计划

- **自动路由集成** — 与 OpenClaw 消息管道集成
- **实时使用情况跟踪** — 自动解析 `session_status`
- **成本预测** — 根据近期使用情况预测每月成本
- **提供商性能监控** — 跟踪 API 延迟和故障
- **A/B 测试** — 比较不同路由策略的质量