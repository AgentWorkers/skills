---
name: agentmail-cli
description: 通过 AgentMail API 管理电子邮件收件箱和消息。可以创建临时收件箱、发送/接收电子邮件以及列出所有消息。当代理需要发送或接收电子邮件、创建临时收件箱或检查新收到的消息时，可以使用该 API。
metadata: {"openclaw":{"emoji":"📧","requires":{"bins":["agentmail"],"env":["AGENTMAIL_API_KEY"]},"primaryEnv":"AGENTMAIL_API_KEY","install":[{"id":"npm","kind":"node","package":"@stepandel/agentmail-cli","bins":["agentmail"],"label":"Install agentmail-cli via npm"}]}}
homepage: https://github.com/stepandel/agentmail-cli
---

**[AgentMail](https://agentmail.to) 的命令行界面 (CLI) —— 创建收件箱、发送消息和读取邮件**

## API 密钥设置

在使用任何命令之前，必须先配置 API 密钥。有两种配置方式：

1. **配置文件（推荐用于长期使用的代理）：**
   ```
agentmail config set-key YOUR_API_KEY
```
   密钥会保存在 `~/.agentmail/config.json` 文件中，并在会话之间保持持久化。

2. **环境变量：**
   ```
export AGENTMAIL_API_KEY=YOUR_API_KEY
```

**验证配置：**
   ```
agentmail config show
```

如果命令因认证错误而失败，请重新运行 `agentmail config set-key` —— 单纯使用环境变量可能无法在不同的 shell 会话之间保持配置。

## 始终使用 `--json` 参数

在每个命令后都必须添加 `--json` 参数，以便输出结果以 JSON 格式呈现。需要时可以使用 `jq` 工具解析 JSON 数据。

## 收件箱相关命令

- 创建收件箱：  
  ```
agentmail inbox create --json
agentmail inbox create --domain example.com --json
agentmail inbox create --username support --domain example.com --display-name "Support Team" --json
```

- 列出所有收件箱：  
  ```
agentmail inbox list --json
agentmail inbox list --limit 10 --json
```

- 获取收件箱详情：  
  ```
agentmail inbox get <inbox-id> --json
```

- 删除收件箱：  
  ```
agentmail inbox delete <inbox-id>
```

## 消息相关命令

- 发送消息：  
  ```
agentmail message send --from <inbox-id> --to recipient@example.com --subject "Subject" --text "Body text" --json
```

- 发送带 HTML 格式的消息：  
  ```
agentmail message send --from <inbox-id> --to recipient@example.com --subject "Subject" --html "<h1>Hello</h1>" --json
```

- 多个收件人、抄送 (CC) 和密送 (BCC)：  
  ```
agentmail message send --from <inbox-id> --to "a@example.com,b@example.com" --cc "cc@example.com" --bcc "bcc@example.com" --subject "Subject" --text "Body" --json
```

- 列出收件箱中的所有消息：  
  ```
agentmail message list <inbox-id> --json
agentmail message list <inbox-id> --limit 20 --json
```

- 获取特定消息：  
  ```
agentmail message get <inbox-id> <message-id> --json
```

- 删除消息（同时删除该消息所属的整个邮件线程）：  
  ```
agentmail message delete <inbox-id> <message-id>
```

## 常见工作流程  

```bash
# 1. Create inbox, capture ID
INBOX_ID=$(agentmail inbox create --json | jq -r '.inboxId')

# 2. Send email
agentmail message send --from "$INBOX_ID" --to user@example.com --subject "Hello" --text "Message body" --json

# 3. Check for replies
agentmail message list "$INBOX_ID" --json
```

## 注意事项：

- 可在 [https://agentmail.to](https://agentmail.to) 获取 API 密钥。
- 配置文件的位置为 `~/.agentmail/config.json`。
- 环境变量 `AGENTMAIL_API_KEY` 的优先级高于配置文件中的设置。
- 删除消息会同时删除该消息所属的整个邮件线程。