---
name: freeride
description: 该工具用于管理 OpenRouter 提供的免费 AI 模型（适用于 OpenClaw）。它能自动根据模型质量对模型进行排序，配置速率限制处理的相关策略，并更新 `openclaw.json` 文件。适用于以下场景：用户需要使用免费 AI 模型、切换模型、处理速率限制问题，或希望降低 AI 使用成本的情况。
---
# FreeRide – 为 OpenClaw 提供免费的 AI 服务

## FreeRide 的功能

FreeRide 功能用于配置 OpenClaw，使其使用 OpenRouter 提供的免费 AI 模型。系统会自动将最佳的免费模型设置为默认模型，并设置多个备用模型，以确保在遇到速率限制时用户仍能正常使用服务，同时保留用户的原有配置设置。

## 先决条件

在运行任何 FreeRide 命令之前，请确保满足以下条件：

1. **已设置 `OPENROUTER_API_KEY`。** 通过 `echo $OPENROUTER_API_KEY` 进行检查。如果该变量为空，用户需要从 [https://openrouter.ai/keys](https://openrouter.ai/keys) 获取免费 API 密钥，并将其设置到系统中：
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-..."
   # Or persist it:
   openclaw config set env.OPENROUTER_API_KEY "sk-or-v1-..."
   ```

2. **已安装 `freeride` CLI 工具。** 通过 `which freeride` 命令进行验证。如果未安装，请先安装该工具：
   ```bash
   cd ~/.openclaw/workspace/skills/free-ride
   pip install -e .
   ```

## 主要使用流程

当用户希望使用免费 AI 服务时，请按以下步骤操作：

```bash
# Step 1: Configure best free model + fallbacks
freeride auto

# Step 2: Restart gateway so OpenClaw picks up the changes
openclaw gateway restart
```

完成以上操作后，用户即可享受免费的 AI 服务，同时系统会自动在可用模型之间进行切换。

用户可以通过发送 `/status` 命令来查看当前正在使用的模型。

## 命令参考

| 命令          | 使用场景                |
|------------------|----------------------|
| `freeride auto`    | 设置免费的 AI 模型（最常用）         |
| `freeride auto -f`    | 启用备用模型，同时保留当前默认模型     |
| `freeride auto -c 10`   | 增加备用模型的数量（默认为 5 个）       |
| `freeride list`    | 查看所有可用的免费模型           |
| `freeride list -n 30`   | 查看所有免费的 AI 模型           |
| `freeride switch <model>` | 切换到指定的模型           |
| `freeride switch <model> -f` | 仅将指定模型设置为备用模型       |
| `freeride status`    | 查看当前的 FreeRide 配置          |
| `freeride fallbacks`    | 仅更新备用模型列表           |
| `freeride refresh`    | 强制刷新模型列表             |

**在修改配置后，请务必运行 `openclaw gateway restart` 以使更改生效。**

## FreeRide 对配置文件的影响

FreeRide 仅更新 `~/.openclaw/openclaw.json` 文件中的以下字段：

- `agentsdefaults.model.primary`：例如 `openrouter/qwen/qwen3-coder:free`  
- `agentsdefaults.model.fallbacks`：例如 `["openrouter/free", "nvidia/nemotron:free", ...]`  
- `agentsdefaults.models`：该字段用于控制 `/model` 命令的显示结果，确保仅显示免费模型  

其他配置项（如网关设置、频道配置、插件、环境变量、自定义指令以及命名代理等）将保持不变。

系统始终会优先使用 `openrouter/free` 作为第一个备用模型；OpenRouter 会根据用户的请求自动选择最佳的免费模型。

## 可选功能（Watcher）

为了在遇到速率限制时实现模型自动切换，用户可以运行以下命令：

```bash
freeride-watcher --daemon    # Continuous monitoring
freeride-watcher --rotate    # Force rotate now
freeride-watcher --status    # Check rotation history
```

## 常见问题及解决方法

| 问题                | 解决方法                        |
|------------------|---------------------------|
| `freeride` 命令无法执行    | 执行 `cd ~/.openclaw/workspace/skills/free-ride && pip install -e .`   |
| `OPENROUTER_API_KEY` 未设置    | 用户需要从 [https://openrouter.ai/keys](https://openrouter.ai/keys) 获取 API 密钥 |
| 更改未生效            | 先运行 `openclaw gateway restart`，然后重新启动会话（使用 `/new` 命令） |
| 代理显示的令牌数为 0         | 检查 `freeride status`，确保默认模型设置为 `openrouter/<provider>/<model>:free` |