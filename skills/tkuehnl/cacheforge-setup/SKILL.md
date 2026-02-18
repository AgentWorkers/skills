---
name: cacheforge-setup
description: >
  **设置 CacheForge：**  
  只需 30 秒即可完成注册、配置上游服务并获取 API 密钥。
license: MIT
homepage: https://app.anvil-ai.io
user-invocable: true
metadata: {"openclaw":{"emoji":"⚒️","homepage":"https://app.anvil-ai.io","requires":{"bins":["python3"]}}}
---
## 何时使用此技能

当用户需要执行以下操作时，请使用此技能：
- 首次设置 CacheForge；
- 注册新的 CacheForge 账户；
- 将他们的 LLM（大型语言模型）API 提供商连接到 CacheForge；
- 获取 CacheForge API 密钥。

## 设置流程

1. **检测现有的 API 密钥** — 检查环境中是否已设置 `OPENAI_API_KEY`、`OPENROUTER_API_KEY`、`ANTHROPIC_API_KEY`。
2. **收集凭据** — 如果用户未提供这些信息，請请求他们的电子邮件和密码。
3. **自动检测提供商类型** — 根据密钥前缀判断提供商类型：
   - `sk-or-` → openrouter
   - `sk-ant-` → anthropic
   - `sk-` → 自定义（兼容 OpenAI；仍接受旧的 `openai` 别名）
   - 预设的默认基础 URL：
     - openrouter → `https://openrouter.ai/api/v1`
     - anthropic → `https://api.anthropic.com`
     - custom → `https://api.fireworks.ai/inference/v1`
4. **进行配置** — 运行 `python3 setup.py provision` 命令以完成注册/身份验证并获取 CacheForge API 密钥。
   - 如果注册模式为仅限邀请（invite-only），请传递 `--invite-code` 参数（或设置 `CACHEFORGE_INVITE_CODE`）。
   - 如果启用了电子邮件验证，请完成验证后重新运行 `provision` 命令以生成租户 API 密钥。
5. **验证配置** — 运行 `python3 setup.py validate` 命令，通过代理发送测试请求以确认配置是否正确。
6. **配置 OpenClaw（推荐）** — 打印 OpenClaw 的配置代码片段，并在获得批准后将其应用到 `~/.openclaw/openclaw.json` 文件中：
   - 打印配置代码：`python3 setup.py openclaw-snippet`
   - 应用配置：`python3 setup.py openclaw-apply --set-default`
   - 如果上游提供商是 OpenRouter，该配置片段会自动注册多个常用模型，用户可以在 `/model` 中直接切换模型。
7. **充值信用额度** — 在首次使用代理服务之前，至少通过 Stripe 或其他方式充值 $10：
   - `python3 skills/cacheforge-ops/ops.py topup --amount 10 --method stripe`
   - `python3 skills/cacheforge-ops/ops.py topup --amount 10 --method crypto`

**重要说明（Vault 模式）：**
- Vault 模式仅在请求中包含可获取数据的工具定义（如 `web_fetch` 或 `browser`）时才会虚拟化工具的输出。
- 如果请求中不包含此类工具定义，CacheForge 会以 “no_fetch_tool” 为理由拒绝请求。

## 命令

```bash
# Full setup (interactive)
python3 skills/cacheforge-setup/setup.py provision \
  --email user@example.com \
  --password "..." \
  --invite-code "..." \
  --upstream-kind custom \
  --upstream-base-url https://api.fireworks.ai/inference/v1 \
  --upstream-key fw_...

# Just validate an existing setup
python3 skills/cacheforge-setup/setup.py validate \
  --base-url https://app.anvil-ai.io \
  --api-key cf_...

# Print the OpenClaw snippet (same structure as the CacheForge console)
python3 skills/cacheforge-setup/setup.py openclaw-snippet \
  --base-url https://app.anvil-ai.io \
  --api-key cf_...

# Apply CacheForge provider config into OpenClaw (JSON5-safe; prompts for approval)
python3 skills/cacheforge-setup/setup.py openclaw-apply \
  --base-url https://app.anvil-ai.io \
  --api-key cf_... \
  --set-default
```

## 环境变量

- `CACHEFORGE_BASE_URL` — CacheForge API 的基础 URL（默认：https://app.anvil-ai.io）
- `CACHEFORGE_API_KEY` — 现有的 API 密钥（如果已设置，则无需执行配置步骤）
- `CACHEFORGE_INVITE_CODE` — 仅限邀请模式的注册代码
- `OPENAI_API_KEY`、`OPENROUTER_API_KEY`、`ANTHROPIC_API_KEY`、`FIREWORKS_API_KEY` — 会根据实际情况自动检测上游提供商的 API 密钥
- `UPSTREAM_BASE_URL` — 可选参数，用于覆盖 `provision` 命令中的上游基础 URL

## 设置完成后

配置完成后，请执行以下操作：
```bash
export OPENAI_BASE_URL=https://app.anvil-ai.io/v1
export OPENAI_API_KEY=cf_...  # your CacheForge tenant API key
```

所有兼容 OpenAI 的工具（如 OpenClaw、Claude Code、Cursor 等）都将自动通过 CacheForge 进行请求处理。

如果您更倾向于使用 OpenClaw 的原生配置方式（推荐），请不要将相关配置信息保存在 `openclaw.json` 文件中，而是通过其他方式管理这些配置。

## API 接口规范（当前版本）

此技能使用的 API 接口包括：
- `POST /api/provision`：用于配置和注册 CacheForge
- `GET /v1/account/info`：用于获取账户信息