---
name: agent-factory
description: >
  **代理创建与代理间切换（v1.0.1 - 配置会自动更新）**  
  **使用方法：**  
  - `/create_agent <名称>`：创建新代理并将其添加到配置文件中。  
  - `/switch <代理ID>`：切换当前使用的代理。
---
# 代理工厂（Agent Factory）

用于代理管理：创建代理以及代理之间的切换。

## 1. `/create_agent` 命令

用于创建新的代理：

```
/create_agent Muhasebeci
/create_agent Coderman
/create_agent Analist
```

### 参数

- **名称**：代理的显示名称
- **表情符号**：默认值：🤖
- **任务**：默认值：“帮助用户”

### 脚本使用方法

```bash
/home/ubuntu/.openclaw/workspace/skills/agent-factory/scripts/create_agent.sh \
  --id "ajan-id" \
  --name "İsim" \
  --emoji "⚙️" \
  --task "Görev tanımı"
```

### 创建的文件

脚本会自动创建以下文件：
- `IDENTITY.md`：身份信息文件
- `SOUL.md`：任务与行为规则
- `USER.md`：用户信息
- `AGENTS.md`：工作规则
- `TOOLS.md`：工具
- `MEMORY.md`：长期存储数据
- `HEARTBEAT.md`：空文件（心跳功能关闭）

## 2. `/switch` 命令

用于切换代理：

```
/switch angarya
/switch main
```

### 其他切换方法

**通过 Telegram：**
- `angarya: <消息>`：直接向代理发送消息
- `/pm angarya <消息>`：相同的功能

**作为子代理（Sub-agent）：**
- “让 Angarya 做……” → 调用代理

## 3. 向代理发送任务

你可以通过我向其他代理发送任务：

```
Angarya'ya sor ne yapıyor
Angarya'ya şunu yaptır: çalışan servisleri kontrol et
```

## 默认模型

新创建的代理会使用 OpenClaw 主代理的默认模型：

- **Primary**：`minimax-portal/MiniMax-M2.5`
- **备用模型（Fallbacks）：**
  - `ollama/glm-5:cloud`
  - `minimax-portal/MiniMax-M2.1`
  - `google/gemini-3-flash-preview`
  - `ollama/phi3.5`
  - `qwen-portal/coder-model`
  - `qwen-portal/vision-model`

这些模型是 OpenClaw 的默认模型设置——任何安装此技能的人都会使用其 OpenClaw 中的模型配置。

## 示例用法

| 命令 | 说明 |
|-------|---------|
| `/create_agent Muhasebeci` | 创建一个名为“Muhasebeci”的新代理 |
| `/switch angarya` | 切换到 Angarya 代理 |
| `angarya: merhaba` | 向 Angarya 发送消息 |
| “Angarya, 你在做什么？” | 查问 Angarya 的状态 |
| “Angarya, 执行 `ls -la`” | 向 Angarya 发送任务 |

## 注意事项

- 创建的代理会自动添加到配置文件中
- 需要重启 Gateway：`/restart`