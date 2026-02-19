---
name: groupme-cli
description: 通过 GroupMe CLI 发送和接收消息。当需要从命令行列出群组、读取消息、向群组发送消息或管理 GroupMe 的私信时，可以使用该工具。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["groupme"] },
        "install":
          [
            {
              "id": "source",
              "kind": "source",
              "repo": "https://github.com/cuuush/groupme-cli",
              "bins": ["groupme"],
              "label": "Install groupme-cli (from source)",
            },
          ],
      },
  }
---
# GroupMe CLI

使用 `groupme` CLI 从命令行发送和接收 GroupMe 消息。

## 设置

### 安装

```bash
git clone https://github.com/cuuush/groupme-cli
cd groupme-cli
npm install
npm run build
npm link
```

### 认证

从 [dev.groupme.com](https://dev.groupme.com/) 获取您的 GroupMe API 令牌（访问令牌），然后进行配置：

```bash
groupme config --token YOUR_ACCESS_TOKEN
```

或者使用 `GROUPME_TOKEN` 环境变量，或者在任何命令后添加 `--token` 参数。

## 核心命令

### 列出群组

```bash
groupme groups
groupme groups --json
```

### 读取消息

```bash
# Latest messages from a group
groupme read --group GROUP_ID

# More messages
groupme read --group GROUP_ID --limit 50

# Paginate older messages
groupme read --group GROUP_ID --before MESSAGE_ID

# JSON output
groupme read --group GROUP_ID --json
```

### 发送消息

```bash
groupme send --group GROUP_ID --message "Hello!"
```

### 直接消息（Private Message）

```bash
# Read DMs
groupme dm-read --user USER_ID

# Send a DM
groupme dm --user USER_ID --message "Hey!"
```

### 列出私信对话记录

```bash
groupme chats
groupme chats --page 2 --per-page 10
```

### 当前用户信息

```bash
groupme me
```

## 模糊匹配群组名称

群组名称支持模糊匹配——在命令中引用群组时可以使用部分名称。

## 全局选项

- `--token <token>` — 覆盖已配置的令牌
- `--json` — 以机器可读的 JSON 格式输出结果
- `--help` — 显示帮助信息

## 提示

- 运行 `groupme groups --json` 可以获取用于其他命令的 GROUP_ID
- 使用 `--json` 格式输出结果，以便将其传递给其他工具或用于脚本编写
- 配置文件存储在 `~/.config/groupme/config.json` 中