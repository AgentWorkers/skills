---
name: agent-swarm
displayName: Agent Swarm | OpenClaw Skill
description: "重要提示：必须使用 OpenRouter。它负责将任务路由到正确的模型，并始终通过 sessions_spawn 来分配工作。"
version: 1.7.5
---
# Agent Swarm | OpenClaw 技能

## 该技能的功能

Agent Swarm 是一个用于管理 AI 模型的任务分配工具。它会为每个任务选择最合适的模型，并启动一个子代理来执行相应的任务。

### 注意：需要 OpenRouter

**所需平台配置：**
- **OpenRouter API 密钥**：必须在 OpenClaw 平台设置中配置（此技能不提供该密钥）
- **OPENCLAW_HOME**（可选）：指向 OpenClaw 工作区根目录的环境变量。如果未设置，默认为 `~/.openclaw`
- **openclaw.json**：路由器会从 `openclaw.json` 文件中读取 `tools.exec.host` 和 `tools.exec.node` 的值（文件位于 `$OPENCLAW_HOME/openclaw.json` 或 `~/.openclaw/openclaw.json`）。仅会读取这两个字段，不会读取网关密钥或 API 密钥。

**模型要求：**
- 模型 ID 必须以 `openrouter/...` 为前缀
- 如果 OpenRouter 未在 OpenClaw 中配置，任务分配将失败

## 该技能的优势

- 更快的响应速度（高效的调度机制，智能的子代理路由）
- 更高的任务质量（代码相关任务由代码模型处理，写作相关任务由写作模型处理）
- 更低的成本（无需使用最昂贵的模型来执行所有任务）

## 核心规则（不可协商）

对于用户提交的任务，调度器必须负责任务的分发，**不得直接执行任务**。

请按照以下流程操作：
1. 运行路由器：
   ```bash
   python3 workspace/skills/agent-swarm/scripts/router.py spawn --json "<user message>"
   ```

   **注意：** 使用从 OpenClaw 工作区根目录开始的相对路径，或者设置 `OPENCLAW_HOME` 环境变量，并使用 `$OPENCLAW_HOME/workspace/skills/agent-swarm/scripts/router.py`。
2. 如果 `needs_config_patch` 为 `true`，则停止执行并向用户报告该配置问题。
3. 否则，调用：
   `sessions_spawn(task=..., model=..., sessionTarget=...)`
4. 等待 `sessions_spawn` 的执行结果。
5. 将子代理的执行结果返回给用户。

如果 `sessions_spawn` 失败，只需返回失败信息，**不得自行执行任务**。

## 快速示例

### 单个任务

路由器输出：
`{"task":"写一首诗","model":"openrouter/moonshotai/kimi-k2.5","sessionTarget":"isolated"}`

然后调用：
`sessions_spawn(task="写一首诗", model="openrouter/moonshotai/kimi-k2.5", sessionTarget="isolated")`

### 并行任务

```bash
python3 workspace/skills/agent-swarm/scripts/router.py spawn --json --multi "fix bug and write poem"
```

此时会返回多个任务配置。每个配置会启动一个子代理来执行。

## 命令

```bash
python scripts/router.py default
python scripts/router.py classify "fix lint errors"
python scripts/router.py spawn --json "write a poem"
python scripts/router.py spawn --json --multi "fix bug and write poem"
python scripts/router.py models
```

## 配置基础

通过编辑 `config.json` 来修改任务分配规则：
- `default_model`：调度器的默认模型
- `routing_rules.<TIER>.primary`：该层级的默认模型
- `routing_rules.<TIER>.fallback`：备用模型

## 安全性

### 输入验证

路由器会对所有输入进行验证和清理，以防止注入攻击：
- **任务字符串**：检查长度（最大 10KB）、空字节以及可疑的模式
- **配置补丁**：仅允许修改 `tools.exec.host` 和 `tools.exec.node` 的值（采用白名单机制）
- **标签**：检查长度和是否存在空字节

### 安全执行

**重要提示**：当从调度器代码中调用 `router.py` 时，务必使用 `subprocess` 并传递参数列表，**严禁使用 shell 字符串插值**：

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

路由器使用 Python 的 `argparse` 模块来安全地处理参数。如果用户输入的字符串包含 shell 元字符，shell 字符串插值可能会导致命令注入攻击。

### 配置补丁的安全性

`recommended_config_patch` 仅修改以下安全字段：
- `tools.exec.host`（只能是 'sandbox' 或 'node'）
- `tools.exec.node`（仅当 `tools.exec.host` 为 'node' 时）

所有配置补丁在返回前都会经过验证。调度器在将补丁应用到 `openclaw.json` 之前应再次进行验证。

### 防止提示注入

任务字符串会被传递给 `sessions_spawn`，然后再由子代理执行。虽然路由器会验证输入格式，但防止提示注入的主要责任在于：
1. 调度器（验证任务字符串）
2. 子代理 LLM（防止提示注入）
3. OpenClaw 平台（清理 `sessions_spawn` 的输入）

### 文件访问权限

**所需文件访问权限：**
- **读取**：`openclaw.json`（通过 `OPENCLAW_HOME` 环境变量或 `~/.openclaw/openclaw.json` 访问）
  - **访问的字段**：仅 `tools.exec.host` 和 `tools.exec.node`
  **用途**：确定子代理的执行环境
  **安全性**：路由器不会读取网关密钥、API 密钥或其他敏感配置

**写入权限：**
- **写入**：无（此技能不会写入任何文件）
- **配置补丁**：技能可能会返回 `recommended_config_patch` JSON 数据，由调度器负责应用，但技能本身不会修改 `openclaw.json`

**安全保障：**
- 路由器不会保存、上传或传输任何令牌或凭据
- 仅从 `openclaw.json` 中读取 `tools.exec.host` 和 `tools.exec.node`
- 除了经过验证的配置补丁外，所有文件访问均为只读

### 其他安全注意事项：
- 该技能不会暴露网关密钥。
- 请单独使用 `gateway-guard` 来管理网关/身份验证。
- 路由器不会执行任意代码或修改配置补丁之外的文件。
- 文档中的 “saves tokens” 指的是**通过使用更便宜的模型来降低成本**，而非存储或收集令牌。