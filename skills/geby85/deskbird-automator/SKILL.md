---
name: deskbird-automator
description: 该技能通过 Telegram 实现对 Deskbird 的远程控制，同时具备安全的身份验证机制、设备发现功能以及停车位的状态查询与预订功能。当 OpenClaw 代理需要执行 Deskbird 的任务，或需要创建/更新定期的 Cron 任务时，可使用此技能；该技能还支持查询任务执行的频率，并在身份验证过期后自动重新进行身份验证。
---
# Deskbird-Automator

使用此技能可通过本地命令行工具（`scripts/deskbird_tool.py`）安全地操作 Deskbird，并可选择将其设置为定期运行的 Cron 任务。

## 前提条件

- 请在项目目录 `<repo-root>` 中操作。
- 建议使用以下命令行命令：
  - `./scripts/deskbird.sh auth-check`
  - `./scripts/deskbird.sh auth-refresh --format json`
  - `./scripts/deskbird.sh auth-import --stdin --format json`
  - `./scripts/deskbird.sh discovery`
  - `./scripts/deskbird.sh parking-status`
  - `./scripts/deskbird.sh parking-book-first`
  - 新上传后的设置步骤：
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
    - `pip install -r requirements.txt`
    - `python -m playwright install chromium`
    - `chmod +x scripts/deskbird.sh`
- 确保启用安全模式（`DESKBIRD_SAFE_MODE=true`），并禁止发送请求数据流。
- 对于 Telegram 的重新认证，建议仅使用 DevTools 中的复制粘贴功能以及 `auth-import` 命令。
- 不要在聊天中默认推荐使用 `auth-pair-*` 和 `auth-capture` 命令。

## 确定性环境变量路径

- 所有技能调用都应通过 `./scripts/deskbird.sh` 这个包装器来执行。
- 该包装器会自动设置 `--env-file <skill-root>/.env`，以避免因工作目录（CWD）变化导致的认证错误。
- 仅在需要手动调试时，才能明确指定 `--env-file` 的路径。

## 推荐的长期认证方式（基于 Firebase）

- 在技能配置文件（`.env`）中存储一次认证后的以下信息：
  - `DESKBIRD_fireBASE_API_KEY`
  - `DESKBIRD_fireBASE_REFRESH_TOKEN`
  - 之后代理程序可以通过 `auth-refresh` 自动获取新的认证令牌，而无需再次登录。

## 自动化前的必问对话

如果尚未创建相应的 Cron 任务，请按以下顺序询问用户：
1. “是否要创建一个定期运行的 Cron 任务？”
2. 如果用户同意，询问：“周期是多少？默认设置为每天 00:30（欧洲/柏林时间），执行一次，持续 24 小时。”
3. “每次任务的具体操作是什么？”
   - 如果用户不明确，建议提供以下默认选项：
     - “仅发送所有可预订对象的列表”
     - “在满足条件时自动预订停车位”
     - “仅进行监控，不进行预订”
4. 整理用户选择的周期、任务内容，并再次确认用户的决定。

如果用户未指定周期，系统将使用默认设置：每天 00:30（欧洲/柏林时间）。

## 重新认证流程（每次执行 Deskbird 功能前）

在执行 `discovery`、`status` 或 `booking` 操作之前，必须先执行以下步骤：
```bash
./scripts/deskbird.sh auth-check --format json --min-valid-minutes 90
```

根据返回的结果执行以下操作：
- 如果 `requires_reauth=false`，则正常继续执行。
- 如果 `requires_reauth=true`：
  - 如果 `DESKBIRD_fireBASE_API_KEY` 和 `DESKBIRD_fireBASE_REFRESH_TOKEN` 已设置：
    - 首先自动执行 `./scripts/deskbird.sh auth-refresh --format json --min-valid-minutes 90`。
    - 如果操作失败，再请求用户手动重新认证。
  - 如果没有 Firebase 证书，需要询问用户是否现在进行重新认证。
- 手动重新认证的默认方法是使用 Chrome DevTools 中的令牌复制粘贴功能。

## Office 发现功能（必备）

- 在执行任何详细查询（`parking-status`、`parking-check`、`parking-book-first`）之前，必须先执行 `discovery` 操作。
- `--office-id` 是可选参数：命令行会自动通过 `internalWorkspaces` 功能识别当前使用的办公室。
- 仅当存在多个办公室且默认设置不明确时，才需要指定 `--office-name `<NAME_TEILSTRING>`；或者可以在技能配置文件（`.env`）中设置 `DESKBIRD_DEFAULT_OFFICE_ID`。
- 代理程序不应默认询问用户的办公室 ID。

## 通过 DevTools 进行重新认证

当需要重新认证时，引导用户按照以下步骤操作：
1. 在浏览器中打开 `app.deskbird.com` 并使用 SSO 登录。
2. 打开 DevTools（网络选项卡）。
3. 点击 `api.deskbird.com` 发送请求。
4. 复制请求头信息（`Authorization`、`Cookie`、`X-CSRF-Token`、`X-XSRF-Token`）。
5. 将这些信息通过 Telegram 发送给机器人。

收到用户复制的请求头信息后，系统内部应按照以下方式处理：
```bash
cat <<'EOF' | ./scripts/deskbird.sh auth-import --stdin --format json
<PASTED_HEADER_BLOCK_OR_TOKEN>
EOF
```

之后还需再次检查：
```bash
./scripts/deskbird.sh auth-check --format json --min-valid-minutes 90
```

**备用方案**：
- 如果无法通过 DevTools 进行重新认证，提供手动使用 `auth-capture` 的选项。

如果重新认证仍然失败：
- 不允许执行任何预订操作。
- 明确告知用户因认证失败而无法继续执行任务。

## Cron 任务的运行规则

Cron 任务的运行需要具备容错性和谨慎性：
- 不要启动过于频繁的尝试或密集的轮询循环。
- 如果在 Cron 任务执行过程中认证失效，不要盲目继续尝试。
- 应通过 Telegram 发送消息，明确提示用户重新认证的操作步骤，并优雅地结束任务。

## 创建/更新 Cron 任务

建议使用 OpenClaw 的 Cron 功能。如果可用，优先使用 `cron.add`/`cron.update` 命令；如果不行，也可以使用命令行工具：
```bash
openclaw cron add --name "Deskbird Daily" --schedule "30 0 * * *" --prompt "<SESSION_PROMPT>" --announce
```

规则：
- 使用欧洲/柏林时间作为默认时间设置。
- 每个任务仅创建一个唯一的 Cron 任务，避免重复。
- 更新现有任务，而不是创建新的任务副本。

## Cron 任务提示的生成

在生成 Cron 任务提示时，请参考 [references/cron-session-template.md](references/cron-session-template.md) 中的模板，并替换其中的占位符。

## 向用户展示的输出格式

无论任务是手动执行还是通过 Cron 调用，都应提供以下信息：
1. 认证状态（`ok` 或 `reauth_noetig`）
2. 当前检查的内容（日期、区域、对象类型）
3. 重要结果（空闲/已占用/被封锁的状态，以及当前占用的对象）
4. 是否成功进行了预订，以及失败的原因