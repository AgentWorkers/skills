---
name: codex-profiler
description: Combined Codex profile operations skill: usage checks + OAuth auth refresh for OpenAI Codex profiles via Telegram commands /codex_usage and /codex_auth.
---

该技能整合了以下两个脚本：
- `scripts/codex_usage.py`（用于检查代码的使用情况及限制）
- `scripts/codex_auth.py`（用于启动/OAuth认证流程以及处理排队中的安全应用请求）

## 命令
### 代码使用检查
- `/codex_usage` → 选择器（默认值：/kyle / mine / all）
- `/codex_usage <profile>`

### OAuth认证
- `/codex_auth` → 选择器（用于选择认证使用的用户配置文件）
- `/codex_auth <profile>`
- `/codex_auth finish <profile> <callback_url>`（用于完成OAuth认证流程，并将结果发送到指定的回调URL）

## 用户体验要求（Telegram）
- 对于`/codex_usage`命令，系统会首先发送一条即时进度提示信息：“正在执行代码使用情况检查…”
- 在处理排队中的认证请求时，系统会在重启前发出警告：“系统将通过后台任务重新启动认证流程。请避免执行耗时较长的操作。”

## 运行方式
```bash
python3 skills/codex-profiler/scripts/codex_usage.py --profile all --timeout-sec 25 --retries 1 --debug
python3 skills/codex-profiler/scripts/codex_auth.py start --profile default
python3 skills/codex-profiler/scripts/codex_auth.py finish --profile default --callback-url "http://localhost:1455/auth/callback?code=...&state=..." --queue-apply
python3 skills/codex-profiler/scripts/codex_auth.py status
```

## 注意事项
- 系统默认使用位于`~/.openclaw/agents/main/agent/auth-profiles.json`文件中的认证配置文件。
- 代码使用情况检查的API地址为：`https://chatgpt.com/backend-api/wham/usage`
- OAuth认证流程使用OpenAI的认证服务，并通过本地端口1455进行回调处理。