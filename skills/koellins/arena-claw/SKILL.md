---
name: are.na-claw
description: 这是一个简单的命令行界面（CLI）封装工具，用于调用 are.na API。该工具可以列出频道信息、添加内容块以及订阅数据源（feeds）。它不支持人工智能功能，也不具备自动化处理能力，更不支持与外部系统的集成；它仅依赖于 API 调用来完成各项操作。
read_when:
  - Managing are.na channels and blocks via API
  - Listing channel contents
  - Adding images/links to channels
  - Watching channels for changes
metadata: {"clawdbot":{"emoji":"🪬","requires":{"bins":["curl","jq"]}}}
allowed-tools: Bash(arena:*) - No file writes, no exec beyond curl
---
# are.na-claw

这是一个简单、透明的命令行工具（CLI），用于与 are.na API 进行交互。该工具不使用人工智能，也不具备自动化功能，更没有隐藏的额外功能。

## 主要功能

- 向 are.na 发送 API 请求
- 列出频道和区块信息
- 向频道添加图片或链接
- 监控频道的变化
- 在多个账户之间切换

## 不支持的功能

- ✗ 人工智能驱动的内容推荐
- ✗ 自动内容发现
- ✗ 跨平台同步
- ✗ 外部集成
- ✗ 图像分析或颜色提取
- ✗ 定时自动化操作

## 安装

```bash
# Install locally
git clone /Users/mika/.openclaw/workspace/skills/arena-claw ~/arena-claw
chmod +x ~/arena-claw/arena
export PATH="$HOME/arena-claw:$PATH"
```

## 认证

**您的 API 令牌仅存储在您的本地机器上。**

令牌的存储位置如下：
- 单个账户：`~/.arena_token`
- 多个账户：`~/.openclaw/.arena_tokens`

该工具绝不会将您的令牌发送到任何其他地方，只会用于与 are.na API 的通信。

```bash
# Add your account
arena auth YOUR_API_TOKEN

# Or add named account
arena auth YOUR_API_TOKEN myaccount

# Switch accounts
arena switch myaccount

# List accounts
arena accounts
```

## 使用方法

```bash
# Check your account
arena me

# List your channels
arena channels

# Get channel contents
arena channel channel-name

# Add image to channel
arena add image https://example.com/image.jpg --channel my-channel

# Add link to channel  
arena add link https://example.com --channel my-channel --title "Example"

# Watch for new items
arena watch channel-name --interval 60

# Search channels
arena search glitch

# Create channel
arena create "my-channel"
```

## 多账户支持

```bash
# Add multiple accounts
arena auth TOKEN1 account1
arena auth TOKEN2 account2

# Use specific account
arena -a account1 me
arena -a account2 channel shared-channel

# Switch default account
arena switch account1
```

## 命令列表

| 命令          | 功能描述                                      |
|-----------------|---------------------------------------------|
| `arena auth <token> [name]` | 添加 API 令牌                        |
| `arena accounts`     | 列出已配置的账户                         |
| `arena switch <name>`    | 切换默认账户                         |
| `arena me`       | 显示当前用户                         |
| `arena channels [user]`    | 列出用户所属的频道                         |
| `arena channel <slug>`    | 获取指定频道的详细信息                   |
| `arena add <type> <url> --channel <name>` | 向指定频道添加内容                     |
| `arena watch <slug>`     | 监控指定频道的更新                     |
| `arena search <query>`    | 搜索频道                         |
| `arena create <title>`    | 创建新频道                         |
| `arena trending`     | 查找热门频道                         |
| `arena explore <keywords>` | 根据关键词搜索频道                     |
| `arena analyze <slug>`    | 统计频道的区块类型                         |
| `arena doctor`     | 检查连接状态                         |

## 安全性

- **不会收集您的凭证**：令牌仅存储在您的个人目录中
- **仅与 are.na API 通信**：不会与其他外部服务交互
- **数据不会被泄露**：所有数据都保留在本地
- **所有操作均为手动执行**：每个命令都需要用户明确输入
- **无依赖库**：仅使用 curl 和 shell 的内置功能

## 卸载

```bash
rm -rf ~/arena-claw
rm ~/.arena_token ~/.openclaw/.arena_tokens
```

## 无保修声明

这是一个简单的工具，使用过程中请自行承担风险。在运行任何命令之前，请务必了解其具体功能。