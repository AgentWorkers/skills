---
name: codex-auth
description: 手动执行的 Telegram 命令（使用斜杠格式），用于启动或完成 OpenAI Codex 的 OAuth 配置文件认证刷新流程。该命令可用于执行 `/codex_auth` 操作，或配合 `/codex_auth <profile>` 命令使用；同时也可用于处理回调 URL 的相关逻辑。
---
运行 `scripts/codex_auth.py` 以生成登录 URL，并将回调 URL 令牌应用到 `auth-profiles.json` 文件中。

## 安全默认设置
- 将回调 URL/令牌视为敏感信息，切勿完整显示其内容。
- 使用队列处理机制来控制服务的重启行为。
- 有关允许或禁止的操作范围，请参阅 `RISK.md` 文件。

## 命令
- `/codex_auth` → 用于选择要操作的代码库配置文件。
- `/codex_auth <profile>` → 选择特定的代码库配置文件进行操作。
- `/codex_auth finish <profile> <callback_url>` → 完成对选定代码库配置文件的操作，并设置回调 URL。

## 用户交互适配器
- 如果支持内联按钮：显示用于选择代码库配置文件的按钮。
- 如果不支持内联按钮：则使用文本作为替代方式（例如：`default | <profile>`）。
- 回调消息的处理过程中严禁显示完整的回调 URL（因为这些信息属于敏感数据）。
- 使用前缀 `codex_auth_` 来命名回调数据相关的变量，以避免命名冲突。

## 运行流程
- **启动操作流程：**  
  ```bash
python3 skills/codex-auth/scripts/codex_auth.py start --profile default
```

- **完成操作流程（在浏览器重定向后）：**  
  ```bash
python3 skills/codex-auth/scripts/codex_auth.py finish --profile default --callback-url "http://localhost:1455/auth/callback?code=...&state=..."
```

- **安全地执行后续操作（在后台控制服务的重启）：**  
  ```bash
python3 skills/codex-auth/scripts/codex_auth.py finish --profile default --callback-url "http://localhost:1455/auth/callback?code=...&state=..." --queue-apply
python3 skills/codex-auth/scripts/codex_auth.py status
```

## 安全策略
- 该技能不允许执行远程 shell 命令（如 `curl|bash`、`wget|sh`）。
- 该技能不允许执行 `sudo` 操作或修改系统包。
- OAuth 回调 URL 属于敏感信息，因此在聊天输出中严禁显示其完整内容或令牌。
- 所有数据写入操作都受到文件锁的保护，以确保数据一致性。

## 注意事项
- 该技能使用与 OpenClaw 注册流程相同的 OpenAI Codex OAuth 常量和方法（回调地址为 `auth.openai.com` 和 `localhost`）。
- 仅允许将回调请求发送到 OpenAI 的认证服务器或本地服务器；严禁将回调请求发送到第三方服务器。
- 数据写入 `~/.openclaw/agents/main/agent/auth-profiles.json` 文件时，会使用文件锁来防止数据竞争问题。
- 代码库配置文件的标识方式如下：
  - `default` → `openai-codex:default`（如果 `default` 不存在，则使用首次检测到的代码库配置文件）
  - 其他配置文件 → `openai-codex:<selector>`
- 待处理的认证状态信息会存储在 `/tmp/openclaw/codex-auth-pending.json` 文件中。