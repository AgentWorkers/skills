---
name: microsoft-365-graph-openclaw
description: Microsoft 365 Graph for OpenClaw：支持基于Webhook的唤醒机制。通过该工具，可以减少因频繁轮询收件箱而产生的LLM（Large Language Model）使用成本，同时还能通过Microsoft Graph高效管理Outlook邮件、日历、OneDrive以及联系人信息。
version: 0.2.0
license: MIT
homepage: https://github.com/draeden79/microsoft-365-graph-openclaw
repository: https://github.com/draeden79/microsoft-365-graph-openclaw
metadata: {"openclaw":{"homepage":"https://github.com/draeden79/microsoft-365-graph-openclaw","os":["linux","darwin","win32"],"primaryEnv":"OPENCLAW_HOOK_TOKEN","requires":{"bins":["python3","bash","curl"],"env":["OPENCLAW_HOOK_URL","OPENCLAW_HOOK_TOKEN","GRAPH_WEBHOOK_CLIENT_STATE","OPENCLAW_SESSION_KEY"]}}}
security:
  summary: Push-first Graph integration with explicit hook token auth and clientState validation.
  notes:
    - Do not commit state/graph_auth.json or token-bearing logs.
    - Keep hooks token and Graph clientState in protected env storage.
    - Prefer /hooks/wake default to avoid unnecessary isolated agent runs.
---
# Microsoft 365 Graph for OpenClaw 技能

## 1. 快速前提条件
1. 安装了 `requests` 的 Python 3。
2. 默认的认证信息：
   - 客户端 ID（个人账户默认值）：`952d1b34-682e-48ce-9c54-bac5a96cbd42`
   - 租户（个人账户默认值）：`consumers`
   - 默认权限范围：`Mail.ReadWrite`, `Mail.Send`, `Calendars.ReadWrite`, `Files.ReadWrite`, `All Contacts.ReadWrite`, `Offline_access`
   - 对于工作/学校账户，请使用 `--tenant-id organizations`（或租户 GUID）和租户批准的 `--client-id`。
   - 公共默认客户端 ID 用于快速测试。在生产环境中，请使用您自己的应用程序注册信息。
3. 令牌存储在 `state/graph_auth.json` 文件中（git 会忽略该文件）。
4. 推送模式所需的运行时环境变量：
   - `OPENCLAWHOOK_URL`
   - `OPENCLAWHOOK_TOKEN`
   - `GRAPH_WEBHOOK_CLIENT_STATE`
   - `OPENCLAW_SESSION_KEY`

权限配置文件（根据使用场景确定最小权限）详见 `docs/permission-profiles.md`。

## 2. 辅助 OAuth 流程（设备代码）
1. 运行以下命令：
   ```bash
   python scripts/graph_auth.py device-login \
     --client-id 952d1b34-682e-48ce-9c54-bac5a96cbd42 \
     --tenant-id consumers
   ```
2. 脚本会打印出一个 **URL** 和一个 **设备代码**。
3. 打开 `https://microsoft.com/devicelogin`，输入设备代码，并使用目标账户进行授权。
4. 检查和管理认证状态：
   - `python scripts/graph_auth.py status`
   - `python scripts/graph_auth.py refresh`
   - `python scripts/graph_auth.py clear`
5. 其他脚本会调用 `utils.get_access_token()`，在需要时自动刷新令牌。
6. 在 `graph_auth.py` 中禁用了权限范围覆盖；该技能始终使用默认权限范围 `DEFAULT_SCOPES`。

详细参考：[`references/auth.md`](references/auth.md)。

## 3. 邮件操作
- **列出/筛选邮件**：`python scripts/mail_fetch.py --folder Inbox --top 20 --unread`
- **获取特定邮件**：`... --id <messageId> --include-body --mark-read`
- **移动邮件**：在命令中添加 `--move-to <folderId>`
- **发送邮件**（默认启用 `saveToSentItems` 功能）：
  ```bash
  python scripts/mail_send.py \
    --to user@example.com \
    --subject "Update" \
    --body-file replies/thais.html --html \
    --cc teammate@example.com \
    --attachment docs/proposal.pdf
  ```
- 仅在您明确不希望邮件保存到已发送邮件文件夹时使用 `--no-save-copy` 选项。

更多示例和筛选条件：[`references/mail.md`](references/mail.md)。

## 4. 日历操作
- **列出指定日期范围内的事件**：
  ```bash
  python scripts/calendar_sync.py list \
    --start 2026-03-03T00:00Z --end 2026-03-05T23:59Z --top 50
  ```
- **创建团队会议或现场活动**：使用 `create` 命令；如果需要添加团队会议链接，请添加 `--online` 选项。
- 对于个人 Microsoft 账户（`tenant=consumers`），通过 Graph 创建的团队会议可能不会返回链接；请先在 Outlook/Teams 中创建会议，然后根据需要将链接添加到事件正文。
- **根据 JSON 输出中的 `event_id` 更新/取消事件**。

完整示例：[`references/calendar.md`](references/calendar.md)。

## 5. OneDrive / 文件操作
- **列出文件夹/文件**：`python scripts/drive_ops.py list --path /`
- **上传文件**：`... upload --local notes/briefing.docx --remote /Clients/briefing.docx`
- **下载文件**：`... download --remote /Clients/briefing.docx --local /tmp/briefing.docx`
- **移动/共享文件链接**：使用 `move` 和 `share` 命令。
- 脚本可以解析本地化文件夹别名（例如 `Documents` 和 `Documentos`）。

更多详细信息：[`references/drive.md`](references/drive.md)。

## 6. 联系人操作
- **列出/搜索联系人**：`python scripts/contacts_ops.py list --top 20`
- **创建联系人**：`... create --given-name Jane --surname Doe --email jane.doe@example.com`
- **更新/删除联系人**：`... update <contactId> ...` / `... delete <contactId>`
- 联系人是默认权限范围的一部分，支持作为一级工作流程进行操作。

更多详细信息：[`references/contacts.md`](references/contacts.md)。

## 7. 邮件推送模式（Webhook 适配器）
- **适配器服务器**（包括 Graph 协议交互、`clientState` 验证和任务队列处理）：
  ```bash
  python scripts/mail_webhook_adapter.py serve \
    --host 0.0.0.0 --port 8789 --path /graph/mail \
    --client-state "$GRAPH_WEBHOOK_CLIENT_STATE"
  ```
- **订阅生命周期管理**（`create/status/renew/delete/list`）：
  ```bash
  python scripts/mail_subscriptions.py create \
    --notification-url "https://graph-hook.example.com/graph/mail" \
    --client-state "$GRAPH_WEBHOOK_CLIENT_STATE" \
    --minutes 4200
  ```
  - 默认资源是 `me/messages`（推荐使用，以获得更好的推送覆盖范围）。仅在高级或特定场景下使用 `--resource` 选项进行覆盖。
- **异步工作进程**（用于去重处理和发送通知给 OpenClaw 的 `/hooks/wake`）：
  ```bash
  python scripts/mail_webhook_worker.py loop \
    --session-key "$OPENCLAW_SESSION_KEY" \
    --hook-url "$OPENCLAW_HOOK_URL" \
    --hook-token "$OPENCLAW_HOOK_TOKEN"
  ```
  - 默认模式是 `wake`（`/hooks/wake`, `mode=now`）。仅在需要针对每条邮件发送详细信息时使用 `--hook-action agent` 选项。
- 工作进程队列文件：
  - `state/mail_webhook_queue.jsonl`
  - `state/mail_webhook_dedupe.json`
- **自动化的 EC2 配置**（使用 Caddy 和 systemd 管理）：
  ```bash
  sudo bash scripts/setup_mail_webhook_ec2.sh \
    --domain graphhook.example.com \
    --hook-url http://127.0.0.1:18789/hooks/wake \
    --hook-token "<OPENCLAW_HOOK_TOKEN>" \
    --session-key "hook:graph-mail" \
    --client-state "<GRAPH_WEBHOOK_CLIENT_STATE>" \
    --repo-root "$(pwd)"
  ```
  - 使用 `--dry-run` 选项预览所有特权操作，确保没有错误后再应用更改。
- **一步设置流程（步骤 2..6）**：
  ```bash
  sudo bash scripts/run_mail_webhook_e2e_setup.sh \
    --domain graphhook.example.com \
    --hook-token "<OPENCLAW_HOOK_TOKEN>" \
    --hook-url "http://127.0.0.1:18789/hooks/wake" \
    --session-key "hook:graph-mail" \
    --test-email "tar.alitar@outlook.com"
  ```
  - 使用 `--dry-run` 选项进行无变更的测试（不修改 `/etc` 文件、不使用 `systemctl`、不创建订阅、不发送邮件）。
  - 设置完成后，输出会显示 `READY_FOR_PUSH: YES`。
- **将 OpenClaw 钩子配置包含在自动化脚本中**：
  ```bash
  sudo bash scripts/run_mail_webhook_e2e_setup.sh \
    --domain graphhook.example.com \
    --hook-token "<OPENCLAW_HOOK_TOKEN>" \
    --configure-openclaw-hooks \
    --openclaw-config "/home/ubuntu/.openclaw/openclaw.json" \
    --openclaw-service-name "auto" \
    --openclaw-hooks-path "/hooks" \
    --openclaw-allow-request-session-key true \
    --test-email "tar.alitar@outlook.com"
  ```
- **最小化输入的测试**：
  ```bash
  sudo bash scripts/run_mail_webhook_smoke_tests.sh \
    --domain graphhook.example.com \
    --create-subscription \
    --test-email tar.alitar@outlook.com
  ```
  - 所有关键检查通过后，输出会显示 `READY_FOR_PUSH`。
- 完整的设置和运行脚本：[`references/mail_webhook_adapter.md`](references/mail_webhook_adapter.md)。

## 8. 特权操作限制
核心的 Graph 脚本（`graph_auth.py`, `mail_fetch.py`, `mail_send.py`, `calendar_sync.py`, `drive_ops.py`, `contacts_ops.py`）没有执行权限。

以下设置脚本具有执行权限，执行前需手动审核：
- `scripts/setup_mail_webhook_ec2.sh`
- `scripts/run_mail_webhook_e2e_setup.sh`

这些脚本在未使用 `--dry-run` 选项时可以执行以下操作：
- 修改 `/etc/default/graph-mail-webhook`
- 修改 `/etc/caddy/Caddyfile`
- 创建或重启 `/etc/systemd/system/*.service` 和 `*.timer` 服务
- 选择性地更新 OpenClaw 配置并重启相关服务

推荐的安全操作顺序：
1. 先使用 `--dry-run` 选项运行脚本。
2. 检查脚本执行的操作和目标文件。
3. 先在非生产环境中进行测试。
4. 经过批准后才能在生产环境中应用这些脚本。

## 9. 日志记录和规范
- 每个脚本都会在 `state/graph_ops.log` 文件中记录一条包含时间戳、操作内容和关键参数的 JSON 数据。
- 令牌和日志文件严禁被提交到版本控制系统。
- 命令假设从仓库根目录执行。如果在其他位置运行，请相应调整路径。

## 10. 故障排除
| 错误症状 | 处理方法 |
| --- | --- |
| 401/invalid_grant | 运行 `graph_auth.py refresh`；如果失败，请运行 `clear` 并重新登录设备。 |
| 403/AccessDenied | 权限范围不足或许可/政策问题。使用所需的权限范围重新登录设备。 |
| 429/Throttled | 脚本会尝试多次重试；等待几秒后再试。 |
| `requests.exceptions.SSLError` | 检查本地系统日期和时间设置以及 TLS 信任链是否正确。 |

该技能通过 Microsoft Graph 提供基于 OAuth 的邮件、日历、文件和联系人管理功能，以及基于推送的自动化邮件处理服务。