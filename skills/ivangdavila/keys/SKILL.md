---
name: Keys
description: 使用代理（broker）进行安全的 API 密钥管理。密钥永远不会暴露给代理（agent）环境。
metadata: {"clawdbot":{"emoji":"🔑","requires":{"bins":["curl","jq","bash"]},"os":["linux","darwin"]}}
---

## 使用方法

无需显示密钥即可进行经过身份验证的 API 调用：

```bash
keys-broker call '{"action":"call","service":"openai","url":"https://api.openai.com/v1/chat/completions","method":"POST","body":{"model":"gpt-4","messages":[{"role":"user","content":"Hello"}]}}'
```

响应：
```json
{"ok": true, "status": 200, "body": {...}}
```

## 支持的服务

仅支持预先配置好的服务（此设置旨在防止密钥泄露）：
- `openai` → api.openai.com
- `anthropic` → api.anthropic.com  
- `stripe` → api.stripe.com
- `github` → api.github.com

如需添加新的服务，请编辑 `keys-broker.sh` 文件中的 `ALLOWED_URLS` 配置。

## 规则

1. **严禁直接获取密钥** — 必须始终使用 `keys-broker` 来发起 API 调用。
2. **严禁让用户通过聊天窗口输入密钥** — 应引导他们使用密钥管理工具（如 Keychain）来操作密钥。

## 其他任务

- 首次设置：请参考 `setup.md` 文件（并安装 `keys-broker.sh`）。
- 添加/删除/轮换密钥：请参考 `manage.md` 文件。

## 限制

该工具不支持以下环境：
- Docker 容器
- WSL（Windows Subsystem for Linux）
- 无密钥管理功能的 Linux 服务器（无法访问密钥管理工具）。