---
name: agent-swarm
displayName: Agent Swarm | OpenClaw Skill
description: IMPORTANT: OpenRouter is required. Routes tasks to the right model and always delegates work through sessions_spawn.
version: 1.7.7
---

# Agent Swarm | OpenClaw 技能

## 描述

**重要提示：** 需要安装 OpenRouter。该技能会将任务路由到合适的模型，并始终通过 `sessions_spawn` 来执行任务。

### 安装前准备

- **OPENCLAW_HOME**：非必需。该技能仅在设置了 `OPENCLAW_HOME` 时才会使用该环境变量；否则会使用默认值 `~/.openclaw`。这一点在元数据（`_meta.json` 中的 `optionalEnv` 字段中有所说明）和实际行为中都是一致的。
- **对 `openclaw.json` 文件的读取权限**：该技能会读取本地的 `openclaw.json` 文件（位于 `$OPENCLAW_HOME/openclaw.json` 或 `~/.openclaw/openclaw.json`）。仅会读取 `tools.exec.host` 和 `tools.exec.node` 两个字段；不会读取任何网关密钥或 API 密钥。在安装前，请确保您允许程序对这些文件进行读取操作。

## 示例

### 单个任务

路由器的输出示例：
`{"task":"写一首诗","model":"openrouter/moonshotai/kimi-k2.5","sessionTarget":"isolated"}`

然后调用：
`sessions_spawn(task="写一首诗", model="openrouter/moonshotai/kimi-k2.5", sessionTarget="isolated")`

### 并行任务

```bash
python3 workspace/skills/agent-swarm/scripts/router.py spawn --json --multi "fix bug and write poem"
```

这将返回多个子代理的配置信息。每个配置会启动一个子代理来执行任务。

## 命令

**仅限手动或通过 CLI 使用。** 下面的示例将任务作为单个参数传递；如果需要处理来自不可信用户的输入，应始终通过 `subprocess.run(..., [..., user_message], ...)` 来调用路由器（请参阅安全注意事项）。切勿直接从用户输入构建 shell 命令字符串。

```bash
python scripts/router.py default
python scripts/router.py classify "fix lint errors"
python scripts/router.py spawn --json "write a poem"
python scripts/router.py spawn --json --multi "fix bug and write poem"
python scripts/router.py models
```

## 该技能的功能

Agent Swarm 是一个用于管理 AI 模型的任务调度工具。它会为每个任务选择最合适的模型，然后启动一个子代理来执行任务。

**重要提示：** 需要安装 OpenRouter

**必需的平台配置：**
- **OpenRouter API 密钥**：必须在 OpenClaw 平台设置中配置（该技能不提供此密钥）。
- **OPENCLAW_HOME**（可选）：指向 OpenClaw 工作区根目录的环境变量。如果未设置，默认值为 `~/.openclaw`。
- **对 `openclaw.json` 的访问权限**：路由器会从 `openclaw.json` 文件中读取 `tools.exec.host` 和 `tools.exec.node`（文件位于 `$OPENCLAW_HOME/openclaw.json` 或 `~/.openclaw/openclaw.json`）。仅会访问这两个字段；不会读取任何网关密钥或 API 密钥。

**模型要求：**
- 模型 ID 必须以 `openrouter/` 为前缀。
- 如果 OpenRouter 未在 OpenClaw 中配置，任务调度将会失败。

## 该技能的优势

- 更快的响应速度（使用高效的调度器，智能分配任务给相应的模型）。
- 更高的任务质量（代码相关任务会分配给相应的模型，写作相关任务会分配给写作模型）。
- 更低的成本（不会使用最昂贵的模型来执行所有任务）。

## 核心规则（不可协商）

对于用户提交的任务，调度器必须负责将任务分配给合适的模型，**不能直接执行任务**。

请始终按照以下流程操作：
1. 运行路由器。**从调度器代码中，使用 `subprocess` 并传递参数列表（切勿使用用户输入进行 shell 插值）：**
   ```python
   import subprocess
   result = subprocess.run(
       ["python3", "/path/to/workspace/skills/agent-swarm/scripts/router.py", "spawn", "--json", user_message],
       capture_output=True,
       text=True
   )
   data = json.loads(result.stdout) if result.returncode == 0 else {}
   ```
   **仅限 CLI 使用（手动测试；切勿在处理不可信用户输入时使用代码）：**
   `python3 workspace/skills/agent-swarm/scripts/router.py spawn --json "你的任务内容"`
   如果不在工作区根目录下，请使用 `OPENCLAW_HOME` 或绝对路径来执行脚本。
2. 如果 `needs_config_patch` 为 `true`，则停止任务并向用户报告错误。
3. 否则，调用：
   `sessions_spawn(task=..., model=..., sessionTarget=...)`
4. 等待 `sessions_spawn` 的执行结果。
5. 将子代理的执行结果返回给用户。

如果 `sessions_spawn` 失败，只需返回失败信息，**不要尝试自行执行任务**。

## 配置基础

请编辑技能根目录（`scripts/` 的上级目录）中的 `config.json` 文件以更改任务调度规则。

### 可以修改的配置项

| 配置项 | 关键字 | 作用 |
|------|-----|--------|
| 调度器/会话的默认模型 | `default_model` | 主代理和新会话使用的默认模型（例如 Gemini 2.5 Flash） |
| 每个任务层级的特定模型 | `routing_rules.<TIER>.primary` | 与任务层级匹配的模型 |
| 主模型失败时的备用模型 | `routing_rules.<TIER>.fallback` | 用于替代的主模型列表 |

### 各任务层级的具体配置（可单独修改模型）

| 层级 | 需要修改的配置项 | 常见用途 |
|------|------------------------|-------------|
| **FAST** | `routing_rules.FAST.primary` | 简单任务：检查、列表、状态查询、数据获取 |
| **REASONING** | `routing_rules.REASONING.primary` | 逻辑分析、数学计算、逐步分析 |
| **CREATIVE** | `routing_rules.CREATIVE.primary` | 写作任务、故事创作、用户界面/用户体验设计 |
| **RESEARCH** | `routing_rules.RESEARCH.primary` | 研究任务、信息检索 |
| **CODE** | `routing_rules.CODE.primary` | 代码编写、调试、重构、实现 |
| **QUALITY** | `routing_rules.QUALITY.primary` | 复杂任务或架构相关任务 |
| **COMPLEX** | `routing_rules.COMPLEX.primary` | 多步骤或复杂的系统任务 |
| **VISION** | `routing_rules.VISION.primary` | 图像分析、截图处理、视觉任务 |

**要更改所有任务层级的模型配置**，请分别修改上述的 `routing_rules.<TIER>.primary`。请使用 `config.json` 中 `models` 数组中的模型 ID（模型 ID 必须以 `openrouter/` 开头）。

### 简单的配置示例

**仅针对调度器（各层级的默认配置保持不变）：**
```json
{
  "default_model": "openrouter/google/gemini-2.5-flash"
}
```
（其他配置项如 `routing_rules` 和 `models` 可以保持 `config.json` 中的默认值。）

**更改某个层级（例如将 `CODE` 层级的模型更改为 MiniMax）：**
```json
"routing_rules": {
  "CODE": {
    "primary": "openrouter/minimax/minimax-m2.5",
    "fallback": ["openrouter/qwen/qwen3-coder-flash"]
  }
}
```

**同时更改多个层级（仅修改主模型）：**
```json
"routing_rules": {
  "CREATIVE": { "primary": "openrouter/moonshotai/kimi-k2.5", "fallback": [] },
  "CODE":     { "primary": "openrouter/z-ai/glm-4.7-flash", "fallback": ["openrouter/minimax/minimax-m2.5"] },
  "RESEARCH": { "primary": "openrouter/x-ai/grok-4.1-fast", "fallback": [] }
}
```
只需修改您希望覆盖的层级；其他层级的配置会从完整的 `config.json` 中读取。

## 安全性

### 输入验证

路由器会对所有输入进行验证和清理，以防止注入攻击：
- **任务字符串**：检查长度（最多 10KB）、空字节以及可疑的字符串模式。
- **配置更新**：仅允许修改 `tools.exec.host` 和 `tools.exec.node`（仅允许这些字段的修改）。
- **标签**：检查长度和是否存在空字节。

### 安全执行

**重要提示：** 从调度器代码调用 `router.py` 时，必须使用 `subprocess` 并传递参数列表，**绝对不能使用 shell 字符串插值**：

```python
# ✅ SAFE: Use subprocess with list arguments
import subprocess
result = subprocess.run(
    ["python3", "/path/to/router.py", "spawn", "--json", user_message],
    capture_output=True,
    text=True
)

# ❌ UNSAFE: Shell string interpolation (vulnerable to injection)
import os
os.system(f'python3 router.py spawn --json "{user_message}"')  # DON'T DO THIS
```

路由器使用了 Python 的 `argparse` 模块来安全地处理参数。如果用户输入包含 shell 元字符，shell 字符串插值可能会导致命令注入攻击。

### 配置更新的安全性

`recommended_config_patch` 仅修改以下安全相关的字段：
- `tools.exec.host`（只能设置为 `sandbox` 或 `node`）。
- `tools.exec.node`（仅当主机设置为 `node` 时允许修改）。

所有配置更新在返回之前都会经过验证。调度器在将更新应用到 `openclaw.json` 之前应再次进行验证。

### 防止提示注入

任务字符串会先传递给 `sessions_spawn`，然后再由子代理执行。虽然路由器会验证输入格式，但防止提示注入的主要责任在于：
1. 调度器（验证任务字符串）。
2. 子代理（防止提示注入）。
3. OpenClaw 平台（清理 `sessions_spawn` 的输入内容）。

### 文件访问权限

**必需的文件访问权限：**
- **读取权限**：`openclaw.json`（通过 `OPENCLAW_HOME` 环境变量或 `~/.openclaw/openclaw.json` 访问）
  - **访问的字段**：仅 `tools.exec.host` 和 `tools.exec.node`。
  - **用途**：确定子代理的执行环境。
  - **安全性**：路由器不会读取任何网关密钥、API 密钥或其他敏感配置信息。

**写入权限**：
- **写入权限**：该技能不会写入任何文件。
- **配置更新**：该技能可能会返回 `recommended_config_patch` JSON 数据，由调度器负责应用，但技能本身不会修改 `openclaw.json` 文件的内容。

**安全保障：**
- 路由器不会保存、上传或传输任何令牌或凭据。
- 仅从 `openclaw.json` 中读取 `tools.exec.host` 和 `tools.exec.node` 的信息。
- 除了经过验证的配置更新外，所有文件访问均为只读。

### 其他安全注意事项

- 该技能不会暴露任何网关密钥。
- 请单独使用 `gateway-guard` 来管理网关/身份验证。
- 路由器不会执行任意代码，也不会修改配置更新之外的文件。
- 文档中提到的“节省成本”是指**使用更便宜的模型来执行简单任务**，而非指令牌的存储或收集。