---
name: freeride
description: 该工具用于管理 OpenRouter 提供的免费 AI 模型（适用于 OpenClaw）。它能自动根据模型质量对模型进行排序，配置速率限制处理的相关策略，并更新 `openclaw.json` 文件。适用于以下场景：用户需要使用免费 AI 模型、切换不同模型、处理速率限制问题，或希望降低 AI 使用成本的情况。
---

# FreeRide - 为 OpenClaw 提供免费的 AI 模型

该工具用于配置 OpenClaw，使其能够使用 OpenRouter 提供的免费 AI 模型，并在模型不可用时自动切换到备用模型。

## 安装

如果 FreeRide 尚未安装，请自动进行安装：

```bash
npx clawhub@latest install freeride
```

## 快速入门

```bash
# Set API key (free at openrouter.ai/keys)
export OPENROUTER_API_KEY="sk-or-v1-..."

# Auto-configure best model + fallbacks
freeride auto
```

## 命令

### `list` - 查看可用模型

```bash
freeride list              # Top 15 models
freeride list -n 30        # More models
freeride list --refresh    # Force API refresh
```

### `auto` - 自动配置

```bash
freeride auto              # Best model + 5 fallbacks
freeride auto -f           # Fallbacks only (keep current primary)
freeride auto -c 10        # 10 fallbacks
freeride auto --setup-auth # Also configure auth profile
```

### `switch` - 设置特定模型

```bash
freeride switch qwen3-coder         # Set as primary
freeride switch deepseek -f         # Add to fallbacks only
freeride switch nvidia/nemotron --no-fallbacks
```

### `status` - 检查配置状态

```bash
freeride status
```

### `fallbacks` - 仅更新备用模型配置

```bash
freeride fallbacks         # 5 fallbacks
freeride fallbacks -c 10   # 10 fallbacks
```

### `refresh` - 更新模型缓存

```bash
freeride refresh
```

## 运行机制

- **主要模型**：根据请求类型自动选择最合适的模型（而非 OpenRouter 自带的模型）。
- **首选备用模型**：始终使用 `openrouter/free`——OpenRouter 提供的智能备用模型，该模型会根据请求类型（如视觉识别、工具使用等）自动进行选择。
- **其他备用模型**：按照质量评分进行排序。
- **配置保留**：仅更新与模型相关的配置项，其他设置（如网关、通道、插件等）保持不变。

## 模型评分标准

评分范围（0-1）：
- 上下文长度（40%）
- 模型功能（30%）
- 模型的更新频率（20%）
- 提供者的可信度（10%）

## 命令行参数

| 参数 | 命令          | 说明                                      |
|------|--------------|-----------------------------------------|
| `-f`     | switch, auto       | 仅启用备用模型配置，保留主要模型配置           |
| `-c N`     | auto, fallbacks     | 指定备用模型的数量                         |
| `--no-fallbacks` | switch         | 禁用备用模型配置                         |
| `--setup-auth` | switch, auto       | 添加 OpenRouter 的认证配置                   |
| `-n N`     | list           | 显示需要显示的模型列表                         |
| `-r`     | list           | 强制刷新模型列表                         |

## 配置文件更新

配置更改会保存到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "openrouter/qwen/qwen3-coder:free",
        "fallbacks": [
          "openrouter/free:free",
          "nvidia/nemotron-3-nano-30b-a3b:free"
        ]
      }
    }
  }
}
```

## 常见问题解决方法

- **“OPENROUTER_API_KEY 未设置”**：请导出 API 密钥或将其添加到 shell 配置文件中。
- **配置未更新**：检查 `~/.openclaw/openclaw.json` 文件的权限设置。
- **更改未生效**：重启 OpenClaw 以应用新的配置。