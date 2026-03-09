---
name: codex-auth
description: 用于手动触发/完成 OpenAI Codex OAuth 配置文件认证刷新的 Telegram 命令（采用斜杠分隔的格式）。该命令可用于执行 `/codex_auth` 操作，或配合 `/codex_auth <profile>` 使用；同时也可用于处理回调 URL 的相关逻辑。
---
运行 `scripts/codex_auth.py` 以生成登录 URL，并将回调 URL 令牌应用到 `auth-profiles.json` 文件中。

## 命令
- `/codex_auth` → 用于选择要处理的配置文件（已发现的配置文件列表）
- `/codex_auth <profile>` → 用于处理指定的配置文件
- `/codex_auth finish <profile> <callback_url>` → 用于完成配置文件的认证过程，并设置回调 URL

## 运行步骤
启动流程：

```bash
python3 skills/codex-auth/scripts/codex_auth.py start --profile default
```

在浏览器跳转完成之后，执行流程的后续步骤：

```bash
python3 skills/codex-auth/scripts/codex_auth.py finish --profile default --callback-url "http://localhost:1455/auth/callback?code=...&state=..."
```

执行安全的应用流程（在后台启动或停止网关）：

```bash
python3 skills/codex-auth/scripts/codex_auth.py finish --profile default --callback-url "http://localhost:1455/auth/callback?code=...&state=..." --queue-apply
python3 skills/codex-auth/scripts/codex_auth.py status
```

## 注意事项
- 该脚本使用与 OpenClaw 注册流程相同的 OpenAI Codex OAuth 常量和方法（回调地址为 `auth.openai.com` + `localhost`）。
- 通过文件锁定机制将更新后的 `auth-profiles.json` 文件写入 `~/.openclaw/agents/main/agent/auth-profiles.json`，以避免在网关运行期间出现数据竞争问题。
- 配置文件的标识符映射规则如下：
  - `default` → `openai-codex:default`（如果 `default` 不存在，则使用第一个发现的 Codex 配置文件）
  - 其他配置文件 → `openai-codex:<selector>`
- 待认证的配置文件状态会被存储在 `/tmp/openclaw/codex-auth-pending.json` 文件中。