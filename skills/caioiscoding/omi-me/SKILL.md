---
name: omi-me
description: 完成 Omi.me 与记忆、待办事项（任务）以及对话的集成。支持 OpenClaw 的全部 CRUD（创建、读取、更新、删除）操作，并具备同步功能。
homepage: https://omi.me
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["omi", "omi-token"]
      env: ["OMI_API_TOKEN"]
---

# OpenClaw 的 Omi.me 集成

与 Omi.me 完整集成，以实现记忆、待办事项（任务）和对话的同步与管理。提供命令行界面（CLI）工具。

## 目录结构

- [设置](#setup)
- [令牌管理](#token-management)
- [CLI 命令](#cli-commands)
  - [记忆](#memories)
  - [待办事项 / 任务](#action-items--tasks)
  - [对话](#conversations)
  - [同步](#sync)
- [使用示例](#usage-examples)

## 设置

### 自动设置

```bash
# Run the setup script
bash /home/ubuntu/.openclaw/workspace/skills/omi-me/scripts/setup.sh
```

设置脚本将：
1. 创建配置目录 `~/.config/omi-me/`
2. 指导您配置 API 令牌
3. 为 `omi` 和 `omi-token` 命令创建符号链接

### 手动设置

```bash
# Create config directory
mkdir -p ~/.config/omi-me

# Save your API token
echo "omi_dev_your_token_here" > ~/.config/omi-me/token
chmod 600 ~/.config/omi-me/token
```

### 获取 API 令牌

1. 访问 https://docs.omi.me/doc/developer/api/overview
2. 生成开发者 API 密钥
3. 使用以下命令进行配置：

```bash
# Interactive (recommended)
omi-token.sh set

# Or manually
echo "your-token" > ~/.config/omi-me/token
```

## 令牌管理

```bash
omi-token.sh set    # Configure API token interactively
omi-token.sh get    # Print current token
omi-token.sh test   # Test connection to Omi.me
```

### 令牌文件

默认位置：`~/.config/omi-me/token`

您也可以通过环境变量来设置令牌：

```bash
export OMI_API_TOKEN="your-token"
```

### 文件

- `~/.config/omi-me/token` - API 令牌存储位置

## CLI 命令

### 令牌管理

| 命令 | 描述 |
|---------|-------------|
| `omi-token.sh set` | 交互式配置 API 令牌 |
| `omi-token.sh get` | 打印当前 API 令牌 |
| `omi-token.sh test` | 测试与 Omi.me 的连接 |

### 记忆

| 命令 | 描述 |
|---------|-------------|
| `omi memories list` | 列出所有记忆 |
| `omi memories get <id>` | 获取特定记忆 |
| `omi memories create "内容"` | 创建新的记忆 |
| `omi memories create "内容" --type 优先级` | 指定记忆类型 |
| `omi memories update <id> "新内容"` | 更新记忆内容 |
| `omi memories delete <id>` | 删除记忆 |
| `omi memories search "查询"` | 搜索记忆 |

### 待办事项 / 任务

| 命令 | 描述 |
|---------|-------------|
| `omi tasks list` | 列出所有待办事项 |
| `omi tasks get <id>` | 获取特定任务 |
| `omi tasks create "标题"` | 创建新任务 |
| `omi tasks create "标题" --desc "描述" --due "2024-01-15"` | 带有详细信息的任务创建 |
| `omi tasks update <id> --title "新标题"` | 更新任务标题 |
| `omi tasks complete <id>` | 将任务标记为已完成 |
| `omi tasks pending <id>` | 将任务标记为待处理 |
| `omi tasks delete <id>` | 删除任务 |

### 对话

| 命令 | 描述 |
|---------|-------------|
| `omi conversations list` | 列出所有对话 |
| `omi conversations get <id>` | 获取特定对话 |
| `omi conversations create --title "我的聊天" --participants "user1,user2"` | 创建对话 |
| `omi conversations create --participants "user1,user2" --message "Hello!"` | 创建带有初始消息的对话 |
| `omi conversations add-message <id> user "Hello world"` | 向对话中添加消息 |
| `omi conversations delete <id>` | 删除对话 |
| `omi conversations search "查询"` | 搜索对话 |

### 同步

| 命令 | 描述 |
|---------|-------------|
| `omi sync memories` | 从 Omi.me 同步记忆 |
| `omi sync tasks` | 从 Omi.me 同步待办事项 |
| `omi sync conversations` | 从 Omi.me 同步对话 |
| `omi sync all` | 同步所有数据 |

## 使用示例

### 令牌配置

**交互式设置:**
```bash
omi-token.sh set
```

**测试连接:**
```bash
omi-token.sh test
```

**获取当前令牌:**
```bash
omi-token.sh get
```

### CLI 示例

**列出记忆:**
```bash
omi memories list
```

**创建记忆:**
```bash
omi memories create "Caio prefers working in English" --type preference
```

**创建任务:**
```bash
omi tasks create "Review Omi integration" --desc "Check if sync is working" --due "2024-02-01"
```

**标记任务已完成:**
```bash
omi tasks complete <task-id>
```

**创建对话:**
```bash
omi conversations create --title "Team Sync" --participants "alice,bob" --message "Let's discuss the project"
```

**添加消息:**
```bash
omi conversations add-message <conv-id> user "I agree!"
```

**同步所有数据:**
```bash
omi sync all
```

## 速率限制

Omi.me API 的速率限制：
- 每个 API 密钥每分钟 100 次请求
- 每用户每天 10,000 次请求

客户端会自动跟踪速率限制信息，并处理 429 状态码的响应。

## 故障排除

### “令牌未配置”
```bash
# Configure interactively
omi-token.sh set

# Or check manually
cat ~/.config/omi-me/token

# If empty, add your token
echo "omi_dev_your_token" > ~/.config/omi-me/token
```

### “连接失败”或 401 错误
```bash
# Test connection
omi-token.sh test

# Reconfigure if needed
omi-token.sh set
```

### 无法创建符号链接
```bash
# Use full path instead
bash /home/ubuntu/.openclaw/workspace/skills/omi-me/scripts/omi-cli.sh memories list
```