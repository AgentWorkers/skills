---
name: secret-portal
description: **快速搭建一次性Web界面**：用于安全地输入密钥和环境变量。该界面支持引导式操作、单密钥输入模式以及CloudFlared隧道技术。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔐",
        "requires": { "bins": ["uv"] },
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# Secret Portal

这是一个临时性的、一次性使用的Web界面，用于安全地输入密钥和环境变量。所有密钥信息都不会被记录到聊天历史记录或终端日志中。

## 快速开始

```bash
# Single key with cloudflared tunnel (recommended)
uv run --with secret-portal secret-portal \
  -k API_KEY_NAME \
  -f ~/.secrets/target-env-file \
  --tunnel cloudflared

# With guided instructions and a link to the key's console
uv run --with secret-portal secret-portal \
  -k OPENAI_API_KEY \
  -f ~/.env \
  -i '<strong>Get your key:</strong><ol><li>Go to platform.openai.com</li><li>Click API Keys</li><li>Create new key</li></ol>' \
  -l "https://platform.openai.com/api-keys" \
  --link-text "Open OpenAI dashboard →" \
  --tunnel cloudflared

# Multi-key mode (no -k flag, user enters key names and values)
uv run --with secret-portal secret-portal \
  -f ~/.secrets/keys.env \
  --tunnel cloudflared
```

## 选项

| 标志 | 描述 |
|------|-------------|
| `-k, --key` | 预填充一个密钥名称（用户只需输入对应的值） |
| `-f, --env-file` | 保存密钥的文件路径（默认：`~/.env`） |
| `-i, --instructions` | 显示在输入框上方的HTML说明文本 |
| `-l, --link` | 用于获取/创建密钥的链接按钮的URL |
| `--link-text` | 链接按钮的标签文本（默认：“打开控制台 →”） |
| `--tunnel` | 可选隧道服务：`cloudflared`、`ngrok` 或 `none`（推荐使用`cloudflared`） |
| `-p, --port` | 绑定的端口号（默认：随机生成） |
| `--timeout` | 自动关闭前的等待时间（秒）（默认：300秒） |

## 隧道服务

**推荐使用 `--tunnel cloudflared`**：该服务免费、无需注册账户、无广告页面，并提供HTTPS加密；如果缺少相关二进制文件，会自动下载。

`ngrok` 的免费版本会显示广告页面，这可能会影响移动设备或自动化脚本的使用。

如果没有使用隧道服务，你需要确保相应的端口在防火墙或安全组中是开放的。如果命令行工具检测到端口无法访问，会给出警告。

## 安全性

- 一次性使用：提交一次后，该门户会立即失效。
- 使用令牌认证：生成的URL包含一个32字节的随机令牌。
- 密钥值**绝不会**被输出到标准输出（stdout）或标准错误（stderr）中（通过测试验证）。
- 环境变量文件仅对文件所有者具有读写权限（权限设置为`600`）。
- 所有密钥信息都不会被记录到聊天历史记录或终端日志中。

## 来源代码

https://github.com/Olafs-World/secret-portal