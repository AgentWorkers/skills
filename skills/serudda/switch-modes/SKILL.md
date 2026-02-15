---
name: switch-modes
description: 动态切换AI模型以优化成本和性能。当用户输入如“节能模式”、“平衡模式”、“智能模式”或“最高性能模式”等指令时，系统会自动切换相应的模式；用户也可以通过“/modes status”查看当前模式的状态，或使用“/modes setup”来配置模式设置。
license: MIT
metadata:
  author: serudda
  version: "1.0.0"
---

# 切换模式

动态切换AI模型，以优化成本和性能。

## 何时使用此功能

当用户提及以下内容时，激活此功能：

- 模式切换命令：`eco mode`、`balanced mode`、`smart mode`、`max mode`
- 状态检查：`/modes status`
- 配置：`/modes setup`

## 工作原理

该功能管理4种预定义的模式，每种模式对应一个特定的AI模型：

- **eco** → 最经济的模型（适用于摘要生成、简单问答）
- **balanced** → 适用于日常工作的模型
- **smart** → 适用于复杂推理的模型
- **max** → 最强大的模型（适用于关键任务）

配置信息存储在 `~/.openclaw/workspace/switch-modes.json` 文件中。

## 分步操作说明

### 1. 检测模式切换命令

当用户消息包含以下内容时：

- `eco mode` 或 `eco`（单独输入）
- `balanced mode` 或 `balanced`
- `smart mode` 或 `smart`
- `max mode` 或 `max`
- `/modes status`
- `/modes setup`

### 2. 处理配置命令（`/modes setup`）

如果配置文件不存在或用户请求进行配置：

1. 使用 `AskUserQuestion` 功能收集用户对每种模式的偏好：
   - **ECO模式**：推荐 `anthropic/claude-3.5-haiku`
   - **BALANCED模式**：推荐 `anthropic/claude-sonnet-4-5`
   - **SMART模式**：推荐 `anthropic/claude-opus-4-5`
   - **MAX模式**：推荐 `anthropic/claude-opus-4-6` 或 `openai/o1-pro`

2. 使用以下结构创建或更新 `~/.openclaw/workspace/switch-modes.json` 文件：

```json
{
	"eco": "model-id",
	"balanced": "model-id",
	"smart": "model-id",
	"max": "model-id"
}
```

3. 向用户确认配置已完成。

### 3. 处理状态检查命令（`/modes status`）

1. 读取 `~/.openclaw/openclaw.json` 文件中的OpenClaw配置信息，以获取当前使用的模型。
2. 读取 `~/.openclaw/workspace/switch-modes.json` 文件中的模式映射关系。
3. 根据当前使用的模型确定当前激活的模式。
4. 显示提示：`✅ 当前处于 [MODE] 模式，使用 [MODEL_ID]`

### 4. 处理模式切换命令

当用户请求切换模式时：

1. **读取配置信息**：

   ```bash
   cat ~/.openclaw/workspace/switch-modes.json
   ```

   如果配置文件不存在，提示用户先运行 `/modes setup` 命令。

2. 根据用户请求的模式（eco/balanced/smart/max），从配置文件中获取目标模型。

3. **更新OpenClaw配置**：
   - 读取当前的配置文件：`~/.openclaw/openclaw.json`
   - 将 `model` 字段更新为新的模型ID。
   - 将更新后的配置写回 `~/.openclaw/openclaw.json` 文件。

4. 向用户确认切换结果：
   ```
   ✅ [MODE] mode activated
   Now using: [MODEL_ID]
   ```

## 示例

### 示例1：模式切换

```
User: eco mode
Agent: [reads switch-modes.json, gets model for "eco"]
Agent: [updates openclaw.json with new model]
Agent: ✅ ECO mode activated
      Now using: anthropic/claude-3.5-haiku
```

### 示例2：状态检查

```
User: /modes status
Agent: [reads openclaw.json for current model]
Agent: [reads switch-modes.json for mode mappings]
Agent: ✅ Currently in BALANCED mode using anthropic/claude-sonnet-4-5
```

### 示例3：首次配置

```
User: /modes setup
Agent: [uses AskUserQuestion for each mode]
Agent: [creates ~/.openclaw/workspace/switch-modes.json]
Agent: ✅ Setup complete! You can now use:
      - eco mode
      - balanced mode
      - smart mode
      - max mode
```

## 文件位置

- **配置文件**：`~/.openclaw/workspace/switch-modes.json`
- **OpenClaw配置文件**：`~/.openclaw/openclaw.json`
- **示例配置文件**：请参阅技能目录下的 `example-config.json`

## 常见问题及处理方式

1. **配置文件缺失**：提示用户运行 `/modes setup` 命令。
2. **模型ID无效**：显示错误信息，并要求用户重新配置该模式。
3. **模型不可用**：建议检查API密钥和OpenClaw中的模型访问权限。
4. **输入不明确**：即使只输入了“eco”或“smart”而没有指定模式，也视为模式切换命令。
5. **大小写不敏感**：“ECO MODE”、“Eco Mode”或“eco mode”均被视为有效命令。

## 重要说明

- 模式切换是即时生效的，无需重启程序。
- 更改仅影响当前会话的默认模型设置。
- 更新模型时，保留 `openclaw.json` 文件中的其他所有设置。
- 在写入配置文件之前，务必验证JSON数据的有效性。
- 使用绝对路径（如 `~/.openclaw/...`），而非相对路径。

## 参考资料

有关详细的故障排除方法、支持的模型列表和常见问题解答，请参阅 [./REFERENCE.md](references/REFERENCE.md)。