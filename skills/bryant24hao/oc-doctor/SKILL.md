---
name: oc-doctor
description: 对本地安装的 OpenClaw 进行全面的 11 项健康检查。能够诊断配置错误、会话占用过多、模型漂移、Cron 任务问题、安全配置错误、网关问题以及系统指令令牌的使用情况。生成包含严重（CRITICAL）、警告（WARNING）和信息（INFO）等级问题的结构化报告，并提供交互式的一键修复功能。可使用以下命令调用该工具：`openclaw doctor`、`claw doctor`、`claw health check`、`openclaw diagnose`，或用于 OpenClaw 的故障排除。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - openclaw
        - jq
    emoji: "stethoscope"
    homepage: https://github.com/bryant24hao/oc-doctor
    os:
      - macos
      - linux
---
# OpenClaw Doctor

OpenClaw Doctor 是一个全面的系统健康检查工具，用于诊断 OpenClaw 安装中的问题，并生成包含严重性级别和可操作修复建议的结构化诊断报告。

## 语言

该工具会使用用户调用该功能时所使用的语言进行响应。如果通过斜杠命令调用且未提供其他文本，系统会从上下文（如最近的对话记录、工作区文件内容（例如 AGENTS.md 中的中文内容或 cron 作业负载）以及系统区域设置）中推断用户偏好的语言。如果未找到语言信息，系统将默认使用英语。

## 先决条件

```bash
command -v openclaw >/dev/null || echo "CRITICAL: openclaw not found in PATH"
command -v jq >/dev/null || echo "CRITICAL: jq not found — install with: brew install jq (macOS) or apt install jq (Linux)"
```

## 路径检测

该工具会在运行时自动检测所有路径，请勿硬编码特定平台的路径。

```bash
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
OPENCLAW_CONFIG="$OPENCLAW_HOME/openclaw.json"
OPENCLAW_DIST=""
if command -v openclaw &>/dev/null; then
  OPENCLAW_DIST="$(dirname "$(readlink -f "$(command -v openclaw)")")/../lib/node_modules/openclaw/dist"
  [ -d "$OPENCLAW_DIST" ] || OPENCLAW_DIST=""
fi
SESSIONS_DIR="$OPENCLAW_HOME/agents/main/sessions"
SESSIONS_INDEX="$SESSIONS_DIR/sessions.json"
MODELS_JSON="$OPENCLAW_HOME/agents/main/agent/models.json"
WORKSPACE_GLOB="$OPENCLAW_HOME/workspace-*"
LOGS_DIR="$OPENCLAW_HOME/logs"
BROWSER_CACHE="$OPENCLAW_HOME/browser"
CRON_DIR="$OPENCLAW_HOME/cron"
```

如果某个路径不存在，系统会记录该情况并跳过相应的检查部分。

## 诊断内容

系统会按顺序执行以下所有诊断部分，并为每个问题分配相应的严重性级别：
- `CRITICAL`：功能故障，存在数据丢失风险
- `WARNING`：配置不佳，可能存在问题
- `INFO`：仅提供信息，建议进行优化

### 1. 安装与版本

使用内置的 `status` 命令作为主要数据来源：

```bash
openclaw status --all 2>&1
openclaw --version 2>/dev/null
```

报告内容包括版本信息、网关运行状态、LaunchAgent 的状态以及各个通道的健康状况。

### 2. 配置一致性

读取 `$OPENCLAW_CONFIG` 文件并检查以下内容：
1. **默认模型的有效性**：`agents.defaults.model.primary` 是否为已知模型？请与 `agents.defaults.models` 中的条目进行核对。
2. **备用模型**：`agentsdefaults.model.fallbacks` 中列出的所有模型是否都在 `models` 列表中？
3. **旧版配置文件**：检查 `$OPENCLAW_HOME/` 目录下是否存在 `clawdbot.json` 或其他旧版配置文件。
4. **备份文件积累**：统计 `$OPENCLAW_HOME/` 目录下的 `*.bak*` 文件数量。如果数量超过 2 个，则提示为 `WARNING`。
5. **通道配置**：
   - Telegram：检查每个组的 `requireMention` 设置。如果设置为 `false`，则表示机器人会响应所有消息（`WARNING`）。
   - Feishu：检查 `groupPolicy`。如果设置为 `"open"`，则表示任何组都可以与机器人交互（`WARNING`）。

### 3. 会话维护配置

检查 `openclaw.json` 文件中的 `session.maintenance` 配置：
1. **维护模式**：如果缺失或设置为 `"warn"`，则表示会话会不断累积且未被清理（`WARNING`）。建议设置为 `"enforce"`。
2. `pruneAfter`：如果缺失或超过 30 天，则提示为 `INFO`。建议设置为 `"7d"` 到 `"14d"`。
3. `maxEntries`：如果缺失或超过 200 个，则提示为 `INFO`。默认值为 500，实际建议值为 50-100。
4. `maxDiskBytes`：如果缺失，则提示为 `INFO`。建议设置一个上限，例如 `"100mb"`。

### 4. 压缩配置

检查 `openclaw.json` 文件中的 `agents.defaults.compaction` 配置：
1. `mode` 应设置为 `"safeguard"`（默认值，表示安全模式）。如果缺失，则提示为 `WARNING`。
2. `reserveTokensFloor`：如果缺失，则提示为 `WARNING`。如果没有这个缓冲区，压缩时可能会导致上下文溢出。建议设置为 `20000`。
3. `keepRecentTokens`：如果缺失，则提示为 `INFO`。该参数控制压缩时保留的最近会话内容的数量。建议设置为 `8000`。

### 5. 模型对齐

使用内置的会话列表，并与配置文件进行对比：

```bash
openclaw sessions 2>&1
```

此外，还可以通过编程方式读取 `sessions.json` 文件来检查以下内容：
1. **会话模型不一致**：列出 `model` 字段与配置的默认模型不同的会话。特别关注 Telegram 和 Feishu 通道的会话。
2. **`contextTokens` 与模型 `contextWindow` 的不匹配**：比较每个会话的 `contextTokens` 与其模型在 `models.json` 或内置注册表中的 `contextWindow` 是否一致。如果不匹配，则提示为 `WARNING`（例如，如果模型大小为 200k，但 `contextTokens` 超过 272k 可能会导致溢出）。
3. **前向兼容性补丁**：通过搜索 `$OPENCLAW_DIST/*.js` 文件中的非标准常量（例如不在官方 `XHIGH_MODEL_REFS` 中的模型 ID 或自定义的 `resolveForwardCompatModel` 添加内容）来检查是否有本地应用的补丁。
4. **思维配置**：读取思维配置文件（使用 `grep -rl "XHIGH_MODEL_REFS" $OPENCLAW_DIST/` 查找），并确认当前默认模型是否包含在 `XHIGH_MODEL_REFS` 中（如果该模型支持 xhigh 思维模式）。
5. **`models.json` 的覆盖设置**：读取 `$MODELS_JSON` 文件，检查其中的模型定义是否与 `openclaw.json` 中的设置一致。

### 6. 会话健康状况

使用内置的清理测试作为主要数据来源：

```bash
openclaw sessions cleanup --dry-run --fix-missing 2>&1
```

此外，还需进行文件系统检查：
1. **孤立的 JSONL 文件**：目录中存在但未被 `sessions.json` 引用的文件。统计这些文件的总大小。
2. **无效的会话条目**：`sessions.json` 中引用的文件实际上并不存在。
3. **空的 JSONL 文件**：被引用的文件大小为 0 字节。
4. **累积的已删除文件**：统计键中包含 `:cron:` 的文件。如果数量超过 20 个，说明清理功能可能存在问题。

### 7. Cron 作业健康状况

读取 `$CRON_DIR/jobs.json` 文件并检查：
1. **重复的作业**：具有相同 `name`、`schedule` 和 `enabled: true` 的作业。标记为 `WARNING` 并建议删除重复项。
2. **禁用的作业**：统计 `enabled: false` 的作业数量。如果数量超过 10 个，则提示为 `INFO`（如果用户确认这些作业不需要，建议进行清理）。
3. **临时文件积累**：统计 `$CRON_DIR` 目录下的 `jobs.json.*.tmp` 文件。这些文件是废弃的临时文件。如果数量大于 0 且没有进程正在使用它们（使用 `lsof` 命令检查），则可以安全删除。
4. **Cron 运行日志**：检查 `$CRON_DIR/runs/` 目录下的运行日志文件，统计其数量和总大小。
5. **过期的启用作业**：检查 `state.lastRunAtMs` 值超过预期时间的启用作业（例如，每天运行的作业如果 3 天以上未执行，则提示为 `WARNING`）。

### 8. 安全审计

检查 `openclaw.json` 文件中的以下内容：
1. **Feishu groupPolicy`：如果设置为 `"open"`，则表示任何 Feishu 组都可以与机器人交互（`CRITICAL`）。
2. **Feishu/Telegram allowFrom`：如果设置为 `["*"]`，则表示没有限制（`WARNING`）。
3. **Telegram 的 requireMention` 设置**：如果设置为 `false`，则表示机器人会响应所有消息（`WARNING`）。
4. **网关认证模式**：从配置文件中读取 `gateway.auth.mode`。如果设置为 `"token"`，则表示正常；如果设置为 `"none"`，则表示严重问题（`CRITICAL`）。
5. **非 Git 目录中的敏感信息**：检查 `$OPENCLAW_HOME/` 目录下是否包含可能被意外同步的文件（例如，检查是否存在 `.git` 目录）。
6. **`models.json` 中的 API 密钥**：注意 `models.json` 中是否以明文形式存储 API 密钥（这是正常现象，但需要特别说明）。

### 9. 资源使用情况

```bash
du -sh $OPENCLAW_HOME/browser/ 2>/dev/null    # Browser cache
du -sh $OPENCLAW_HOME/logs/ 2>/dev/null       # Logs
du -sh $SESSIONS_DIR/ 2>/dev/null             # Sessions
du -sh $OPENCLAW_HOME/media/ 2>/dev/null      # Media files
du -sh $OPENCLAW_HOME/memory/ 2>/dev/null     # Memory files
du -sh $CRON_DIR/ 2>/dev/null                 # Cron data
du -sh $OPENCLAW_HOME/ 2>/dev/null            # Total

# Log file sizes
ls -lhS $LOGS_DIR/ 2>/dev/null

# Large JSONL sessions (top 5)
ls -lhS $SESSIONS_DIR/*.jsonl 2>/dev/null | head -5
```

如果发现以下情况，会发出警告：
- 浏览器缓存大小超过 200MB：`WARNING`
- 日志文件大小超过 50MB：`WARNING`
- 任何单个 JSONL 文件大小超过 10MB：`INFO`
- `$OPENCLAW_HOME/` 目录下的文件总大小超过 1GB：`WARNING`

### 10. 网关与进程健康状况

从 `openclaw.json` 文件中读取 `gateway.port` 以确定正确的网关端口（请勿硬编码）。

```bash
# Check for stuck/zombie openclaw processes
ps aux | grep -E "openclaw-gateway|openclaw " | grep -v grep

# Check gateway port binding (use port from config)
lsof -i :<port> 2>/dev/null | head -5

# Check gateway error log for recent errors
tail -20 $LOGS_DIR/gateway.err.log 2>/dev/null
```

如果发现以下情况，会发出警告：
- 启用了多个网关进程：`CRITICAL`
- 网关未在配置的端口上监听：`CRITICAL`
- `gateway.err.log` 文件中记录了最近发生的错误：`WARNING`（显示最近 5 条错误）

### 11. 系统指令使用情况

该工具会测量系统指令使用的令牌数量。这一部分与第 5 部分（运行时会话压力）一起构成了系统的整体资源使用情况。

#### 步骤 A：数据收集（确定性脚本）

从技能目录中找到并运行内置的收集脚本：

```bash
# Find the skill directory (works whether installed via skills.sh, clawhub, or manually)
SKILL_DIR="$(find ~/.claude/skills ~/.agents/skills -maxdepth 3 -name 'sysinstruction-check.sh' -path '*/oc-doctor/*' 2>/dev/null | head -1 | xargs dirname)"
bash "$SKILL_DIR/sysinstruction-check.sh"
```

该脚本会自动检测工作区目录并生成结构化的 JSON 数据。详细信息请参阅 [scripts/sysinstruction-check.sh](scripts/sysinstruction-check.sh)。

输出格式如下：
```json
{
  "workspace_files": [
    {"file": "workspace-name/FILE.md", "chars": 0, "lines": 0, "est_tokens": 0, "is_empty_template": false}
  ],
  "total_est_tokens": 0,
  "largest_file": "AGENTS.md",
  "empty_template_files": [],
  "tool_bloat_files": [],
  "tool_bloat_est_tokens": 0,
  "bootstrap_still_present": false,
  "context_window": 200000,
  "context_window_source": "models.json | default_fallback",
  "pct_of_context": "0.0"
}
```

#### 步骤 B：大语言模型（LLM）分析

根据以下维度分析 JSON 数据：
1. **上下文使用情况**（补充第 5 部分的运行时检查）：
   - `pct_of_context < 2%`：`INFO`，表示系统健康
   - `2-5%`：`INFO`，表示可以使用，但建议检查
   - `5-10%`：`WARNING`，建议进行优化
   - `10-15%`：`WARNING`，建议积极优化
   - `> 15%`：`CRITICAL`，仅在同时存在运行时优化问题的情况下才显示警告
   - 如果 `context_window_source` 设置为 `"default_fallback"`，请注意这些阈值可能不准确

2. **工具描述文件冗余**：
   - 如果 `tool_bloat_files` 文件非空，表示存在冗余文件（`WARNING`），并列出这些文件及估计的令牌消耗量
   - 这些文件是由 OpenClaw 自动插入的（例如 Feishu 相关的工具文件），请检查是否所有文件都是必要的

3. **可回收的空间**（查看 `empty_template_files` 和 `bootstrap_still_present`）：
   - 如果 `bootstrap_still_present` 为 `true`，表示这些文件在初始设置后可以删除（`INFO`）
   - 如果 `empty_template_files` 非空，列出这些文件及估计的令牌节省量

4. **单个文件分析**：
   - 如果单个文件占用的令牌数量超过总令牌数量的 40%，建议对其进行分割
   - 如果单个文件占用的上下文窗口大小超过 2%，建议单独检查
   - 通常 `AGENTS.md` 文件占用的令牌数量最多（尤其是内存、群组聊天和心跳规则相关的文件），但如果文件大小超过 5000 个令牌，建议进行检查

5. **基准测试**（根据实际上下文窗口动态计算）：
   ```
   Healthy:        < 2% of context_window
   Needs review:   2-5% of context_window
   Needs optimization: > 5% of context_window
   ```

6. **文件引用完整性**：
   - 扫描最大的工作区文件（通常是 `AGENTS.md`），检查其中是否引用了其他 `.md` 文件（例如 `HEARTBEAT.md`、`BOOTSTRAP.md`、`MEMORY.md`）。
   - 对于每个被引用的文件，检查它们是否存在于 `workspace-*/` 目录中，以及它们是否为空模板文件。
   - 如果文件被引用但实际不存在，则提示为 `WARNING`——这意味着机器人使用的指令依赖于不存在的文件。可以基于用户的实际配置生成相应的文件。
   - 如果文件被引用但为空模板，则提示为 `WARNING`——这意味着文件实际上没有内容，因此相关的指令无效。可以建议用户根据实际需求生成相应的文件或删除这些无效引用。

#### 输出结果（整合到主报告中）

在诊断报告中添加一个关于系统指令使用情况的章节：

```
### [SEVERITY] System Instruction Token Usage

| File | Lines | Chars | ~Tokens | % of Context |
|------|-------|-------|---------|--------------|
| AGENTS.md | N | N | N | N% |
| SOUL.md | N | N | N | N% |
| ... | ... | ... | ... | ... |
| **Total** | **N** | **N** | **N** | **N%** |

- Status: Healthy / Elevated / Needs Optimization
- Suggestions: (specific optimization actions, if any)
```

## 输出格式

以结构化诊断报告的形式呈现结果：

```
# OpenClaw Doctor Report

## Summary
- Version: x.x.x
- Gateway: running/stopped
- Overall Health: HEALTHY / NEEDS ATTENTION / CRITICAL

## Findings

### [SEVERITY] Finding Title
- Description: ...
- Impact: ...
- Fix: (specific command or config change)

(repeat for each finding)

## Quick Stats
| Metric | Value |
|---|---|
| Active sessions | N |
| Cron jobs (enabled/disabled) | N / N |
| Orphan files | N (size) |
| Browser cache | size |
| Total disk usage | size |

## Recommended Actions
1. (prioritized list of suggested fixes)
```

## 交互模式

在展示报告后，用用户的语言询问用户：
> “您希望我修复这些问题吗？我可以逐一修复这些问题，或者批量修复所有 `WARNING` 级别及以下的问题。`CRITICAL` 级别的问题需要用户逐一确认。”

对于需要修复的问题，系统会提供以下选项：
- **孤立的/已删除的文件**：建议删除这些文件，并提供文件大小统计信息。
- **模型不一致/上下文令牌不匹配**：建议将所有会话的模型设置为默认值，并调整 `contextWindow`。
- **配置问题**：显示具体的配置更改内容，用户确认后即可应用。
- **Cron 作业重复/临时文件清理**：显示将要删除的文件内容，用户确认后即可应用。
- **维护配置**：建议最优的配置值，用户确认后即可应用。
- **资源清理**：建议清除浏览器缓存、旋转日志文件。
- **安全问题**：显示配置更改内容，并解释相关影响，用户确认后即可应用。
- **工具描述冗余**：建议将 `BOOTSTRAP.md` 文件归档（重命名为 `.bak`），清理空模板文件，并标记不必要的工具描述文件。
- **引用的文件不存在/为空**：根据用户的实际配置生成相应的文件。对于 `HEARTBEAT.md`，建议分析 cron 作业、通道设置和 `agents.md` 中的心跳规则，以生成实用的文件版本。

## 保密处理（强制要求）

在报告中显示配置信息时，**必须对敏感数据进行保密处理**：
- API 密钥/令牌：仅显示前 8 个字符及后面的省略号（例如：`8263689670:A...`）
- 密码/敏感信息：显示为 `***REDACTED***`
- 绝不要在报告中显示完整的 `botToken`、`appSecret`、`auth token` 或 API 密钥。

## 安全性与隐私

该工具仅在本地运行，不会发送网络请求。然而，诊断报告会作为大语言模型对话的一部分被显示给用户。

**读取的文件**（除非用户同意修复，否则仅读）：
- `$OPENCLAW_HOME/openclaw.json` — 主配置文件
- `$OPENCLAW_HOME/agents/main/agent/models.json` — 模型定义文件
- `$OPENCLAW_HOME/agents/main/sessions/sessions.json` — 会话索引文件
- `$OPENCLAW_HOME/workspace-*/*.md` — 系统指令文件
- `$OPENCLAW_HOME/cron/jobs.json` — Cron 作业配置文件
- `$OPENCLAW_HOME/logs/gateway.err.log` — 最近的网关错误日志
- `$OPENCLAW_DIST/*.js` — 安装的 dist 文件（用于检测补丁）

**修改的文件**（仅在用户明确同意的情况下）：
- 会话相关的 JSONL 文件（清理孤儿文件）
- 配置文件（进行优化）
- 工作区 `.md` 文件（归档 `BOOTSTRAP.md` 文件）
- Cron 临时文件（清理）

**读取的环境变量**：`OPENCLAW_HOME`（可自定义）

**该工具不会传输或记录任何敏感信息**。但在诊断报告中可能会显示部分配置内容。