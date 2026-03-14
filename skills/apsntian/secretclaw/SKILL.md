---
name: secretclaw
description: >
  **安全地输入 API 密钥和敏感信息到 OpenClaw 中，而无需在聊天框中直接输入这些信息。**  
  该方法通过使用本地 HTTP 服务器结合 Cloudflare Tunnel 来提供一个 HTTPS 形式的数据提交接口。适用于注册 API 密钥、令牌、密码或任何其他敏感配置信息的情况。
---
# SecretClaw

这是一个用于安全输入密钥和敏感信息的技能，无需通过 Discord 或任何聊天频道传递这些信息。

该技能使用本地 HTTP 服务器与 Cloudflare Tunnel 来提供 HTTPS 形式页面，然后通过 `openclaw config set` 命令保存用户提交的值。

## 使用场景

- 在注册 API 密钥、令牌、密码或其他敏感信息时
- 为了避免在聊天中直接输入敏感内容

**示例：** FAL_KEY、Notion API 密钥、OpenAI 密钥等

## 正在使用的隧道

→ 请参阅 `workspace/TUNNELS.md`（由代理程序自动管理）

## 使用方法

```bash
python3 <skill_dir>/scripts/secret_server.py \
  --config-key "env.FAL_KEY" \
  --label "FAL_KEY"
```

### 参数
- `--config-key`：openclaw 配置文件的路径（使用点表示法）
  - 例如：`env.FAL_KEY`、`env.OPENAI_KEY`、`channels.discord.token`
- `--label`：在表单上显示的、人类可读的名称
- `--service`：记录在 `TUNNELS.md` 中的服务名称（默认值：`secret-input`）

## 代理程序的执行步骤

1. 以后台进程的方式运行以下命令
2. 从标准输出（stdout）中提取 `SECRET_URL:` 这一行，并将其发送给用户
3. 当出现 `SECRET_SAVED:` 时，表示值已成功保存
4. 检查是否需要重启服务器（某些密钥可能需要重启）

```python
# Example background exec
python3 /opt/homebrew/lib/node_modules/openclaw/skills/secret-input/scripts/secret_server.py \
  --config-key "env.FAL_KEY" \
  --label "FAL_KEY"
```

## TUNNELS.md 的结构

正在使用的隧道信息会记录在 `workspace/TUNNELS.md` 文件中。代理程序会读取该文件以获取当前打开的隧道 URL。服务器关闭后，相关条目会自动被删除。

## 安全性

- 任何敏感信息都不会被存储在聊天历史记录中
- 通过 Cloudflare 的 TLS 协议实现 HTTPS 连接（快速隧道）
- URL 中嵌入了一次性生成的随机令牌
- 提交数据后服务器会立即销毁
- 使用 Cloudflare 的快速隧道服务（无需注册账户；每次运行时 URL 都会更新）

## 注意事项

- 如果机器重启，服务器会关闭，相应的 Cloudflare URL 也会失效
- 要重新输入数据，只需再次运行该技能以生成新的 URL
- `TUNNELS.md` 仅记录当前正在使用的隧道（不包含历史记录中的 URL）