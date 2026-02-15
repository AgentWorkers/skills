---
name: freeride
description: 该工具用于管理 OpenRouter 提供的免费 AI 模型，并将其集成到 OpenClaw 系统中。它能够自动根据模型质量对模型进行排序，配置速率限制处理方案，并更新 `openclaw.json` 配置文件。当用户需要使用免费 AI 模型、切换模型、处理速率限制问题，或希望降低 AI 使用成本时，可优先使用该工具。
---

# FreeRide - 为 OpenClaw 提供免费的 AI 模型

该插件配置 OpenClaw 使用来自 OpenRouter 的免费 AI 模型，并支持自动切换备用模型。

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

### `status` - 检查配置

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

## 行为规则

- **主要模型**：根据请求类型自动选择最适合的模型（而非 OpenRouter 自带的模型），以确保响应的一致性。
- **首选备用模型**：始终使用 `openrouter/free`——OpenRouter 提供的智能备用模型，该模型会根据请求的特征（如视觉需求、工具等）自动进行选择。
- **其他备用模型**：按照模型质量得分进行排序。
- **配置保留**：仅更新与模型相关的配置，其他设置（如网关、频道、插件等）保持不变。

## 模型评分标准

评分（0-1 分）基于以下因素：
- **上下文长度**（40%）
- **模型功能**（30%）
- **模型更新频率**（20%）
- **模型提供者的可信度**（10%）

## 标志参数

| 标志 | 命令 | 说明 |
|------|----------|-------------|
| `-f` | `switch`, `auto` | 仅使用备用模型，保留主要模型配置 |
| `-c N` | `auto`, `fallbacks` | 指定备用模型的数量 |
| `--no-fallbacks` | `switch` | 忽略备用模型配置 |
| `--setup-auth` | `switch`, `auto` | 添加 OpenRouter 的认证配置 |
| `-n N` | `list` | 显示要显示的模型列表 |
| `-r` | `list` | 强制更新模型缓存 |

## 配置输出

配置信息会保存到 `~/.openclaw/openclaw.json` 文件中：

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

## 故障排除

- 如果出现 “OPENROUTER_API_KEY 未设置” 的错误，请导出该密钥或将其添加到 shell 配置文件中。
- 如果配置更新失败，请检查 `~/.openclaw/openclaw.json` 文件的权限设置。
- 如果更改没有生效，请重启 OpenClaw。