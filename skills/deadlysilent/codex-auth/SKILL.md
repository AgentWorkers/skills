---
name: codex-auth
description: 这是一个用于手动触发/完成 OpenAI Codex OAuth 个人资料认证刷新的 Telegram 命令。该命令适用于以下场景：`/codex_auth`、`/codex_auth <profile>` 以及回调 URL 的处理。
---
运行 `scripts/codex_auth.py` 以生成登录 URL，并将回调 URL 令牌应用到 `auth-profiles.json` 文件中。

## 命令
- `/codex_auth` → 用于选择要处理的代码库配置文件（已发现的配置文件）
- `/codex_auth <profile>` → 选择特定的代码库配置文件进行处理
- `/codex_auth finish <profile> <callback_url>` → 完成对选定代码库配置文件的处理，并设置回调 URL

## 交互适配器
- 如果支持内联按钮：显示用于选择代码库配置文件的按钮。
- 如果不支持内联按钮：则发送文本作为替代方式（例如：“default”或 `<profile>`）。
- 回调消息的处理过程中严禁直接显示完整的回调 URL（因为这些信息属于敏感数据）。
- 使用前缀 `codex_auth_` 来命名回调数据相关的变量，以避免命名冲突。

## 运行流程
- **启动流程：**  
  ```bash
python3 skills/codex-auth/scripts/codex_auth.py start --profile default
```

- **完成流程（在浏览器跳转至指定 URL 后）：**  
  ```bash
python3 skills/codex-auth/scripts/codex_auth.py finish --profile default --callback-url "http://localhost:1455/auth/callback?code=...&state=..."
```

- **安全地应用处理结果（在后台启动/停止网关服务）：**  
  ```bash
python3 skills/codex-auth/scripts/codex_auth.py finish --profile default --callback-url "http://localhost:1455/auth/callback?code=...&state=..." --queue-apply
python3 skills/codex-auth/scripts/codex_auth.py status
```

## 注意事项
- 该脚本使用与 OpenClaw 的 OAuth 配置相同的常量和方法（回调地址为 `auth.openai.com` 和 `localhost`）。
- 处理完成后，脚本会将结果写入 `~/.openclaw/agents/main/agent/auth-profiles.json` 文件，并通过文件锁定机制来防止并发访问导致的数据竞争问题。
- 代码库配置文件的标识方式如下：
  - `default` → `openai-codex:default`（如果 `default` 不存在，则使用第一个发现的代码库配置文件）
  - 其他配置文件 → `openai-codex:<selector>`
- 待处理的认证状态会被存储在 `/tmp/openclaw/codex-auth-pending.json` 文件中。