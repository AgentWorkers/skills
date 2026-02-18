---
name: are.na-claw
description: 这是一个简单的命令行界面（CLI）封装工具，用于调用 are.na API。该工具支持以下功能：列出频道、添加内容块、订阅信息源。它不包含任何人工智能功能，也不支持自动化操作或外部集成，仅依赖于 API 调用来实现相应功能。
read_when:
  - Managing are.na channels and blocks via API
  - Listing channel contents
  - Adding images/links to channels
  - Watching channels for changes
metadata: {"clawdbot":{"emoji":"🪬","requires":{"bins":["curl","python3"]}}}
allowed-tools: Bash(arena:*) - No file writes, no exec beyond curl
---
# are.na-claw

这是一个简单、透明的命令行工具（CLI），用于与 are.na API 进行交互。该工具不使用人工智能（AI），也不具备自动化功能，更没有隐藏的额外功能。

## 功能介绍

- 向 are.na 发送 API 请求  
- 列出频道和内容块  
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
# Clone the repository
git clone https://github.com/yourusername/arena-claw ~/arena-claw

# Or copy just the arena script
cp arena-claw/arena ~/bin/arena
chmod +x ~/bin/arena

# Add to PATH (add to ~/.zshrc or ~/.bashrc)
export PATH="$HOME/bin:$PATH"
```

## 源代码

该 CLI 是一个简单的 Python 脚本：`arena`。它仅使用以下工具：  
- `curl` 用于发送 API 请求  
- `python3` 用于数据解析  
- 本地文件用于存储 API 令牌  

该工具没有依赖项，也不需要导入任何外部库。  

## 认证机制

**您的 API 令牌仅存储在您的本地机器上。**  
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

## 多账户管理

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
| `arena auth <token> [name]` | 添加 API 令牌                          |
| `arena accounts`     | 列出已配置的账户                          |
| `arena switch <name>`    | 切换默认账户                          |
| `arena me`       | 显示当前用户                          |
| `arena channels [user]`    | 列出用户所属的频道                          |
| `arena channel <slug>`    | 获取指定频道的详细信息                      |
| `arena add <type> <url> --channel <name>` | 向频道添加内容块                          |
| `arena watch <slug>`    | 监控指定频道的变化                        |
| `arena search <query>`    | 搜索频道                            |
| `arena create <title>`     | 创建新频道                          |
| `arena trending`     | 查找热门频道                          |
| `arena explore <keywords>` | 根据关键词搜索频道                        |
| `arena analyze <slug>`    | 统计频道中的内容块类型                        |
| `arena doctor`     | 检查连接是否正常                          |

## 安全性

- **数据安全**：令牌仅存储在用户的本地目录中  
- **无外部连接**：仅与 are.na API 交互  
- **数据隔离**：所有数据都保留在本地  
- **手动操作**：所有命令都需要用户明确输入  
- **无依赖项**：仅依赖 `curl` 和 Python 的内置功能  

## 卸载方法

```bash
rm -rf ~/arena-claw
rm ~/.arena_token ~/.openclaw/.arena_tokens
```

## 免责声明

这是一个简单的工具，使用过程中请自行承担风险。在运行任何命令之前，请务必了解其具体功能。