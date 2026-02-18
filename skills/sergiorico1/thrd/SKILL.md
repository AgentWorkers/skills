---
name: thrd
description: "为您的人工智能代理提供一个专用的收件箱，并通过 thrd.email 安全地管理电子邮件。该服务包括即时入职引导、收件箱轮询、回复/发送（操作具有幂等性且受策略控制）、冷邮件发送时的“推理证明”功能、人工验证请求以及邮件送达情况的跟踪。此外，该服务不会将 API 密钥存储在磁盘上。"
metadata:
  {
    "openclaw":
      {
        "emoji": "📧",
        "requires": { "bins": ["python3"], "env": ["THRD_API_KEY"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "exec",
              "command": "pip install -r requirements.txt",
              "label": "Install Python dependencies",
            },
          ],
      },
  }
---
# 第三项电子邮件技能

此技能可帮助您使用 [thrd.email](https://thrd.email) 为 AI 代理创建并管理一个独立的收件箱，而无需将您的个人收件箱与之关联。

**默认安全设置**：切勿将您的主收件箱连接到代理；请使用专用的代理收件箱。

## 工作流程

### 同步 OpenAPI 合同（建议在使用工具前执行）
为避免使用过时的信息，请刷新 OpenAPI 合同并查看 `info.version`：
```bash
python3 scripts/openapi_sync.py
python3 scripts/openapi_sync.py --print-version
```
该操作会利用 HTTP 缓存验证机制（`ETag`/`Last-Modified`），仅在合同内容发生变化时才会重新下载。

### 配置新的电子邮件账户
要创建新的电子邮件账户，请运行入职脚本：
```bash
python3 scripts/onboard.py --agent-name "My Agent" [--tenant-name "My Company"]
```
该脚本会将包含 `api_key` 和新收件箱地址的 JSON 数据输出到标准输出（stdout）。请将 `api_key` 视为机密信息。

**安全提示**：**切勿将您的 API 密钥保存到磁盘上**。请将其存储在运行时的秘密管理器中，并将 `THRD_API_KEY` 设置为环境变量。（其他工具需要 `THRD_API_KEY`；入职流程不需要。）

### 升级计划（计费）
要为您当前的租户启用付费计费，请使用结算脚本：
```bash
python3 scripts/checkout.py <plan_name>
```
升级选项包括：
- `sandbox` -> Sandbox Starter（每月 9 欧元，每月发送邮件数量上限从 100 封提升至 2,000 封）
- `limited` -> Tier 2
- `verified` -> Tier 3

将生成的 Stripe 支付链接转发给您的负责人以完成支付。

### 人工验证（身份确认）
**Tier 3（已验证的发送功能）** 需要通过 X 进行人工身份验证：
- 启动验证流程：`POST /v1/claim/x/start`
- 将 `claim_url` 转发给您的负责人。
- 查看验证状态：`GET /v1/claim/x/status`

### 推理验证（Proof of Reasoning, PoR）
对于 **Tier 3** 的发送功能，系统可能会要求您解决逻辑挑战以防止垃圾邮件。
- 如果收到 `428 por_required` 错误，请按照响应中的提示解决逻辑问题。
- 重新发送请求时请附上 `por_token` 和 `por_answer`。

### 管理电子邮件并跟踪发送状态
有关详细的 API 使用方法（轮询、发送、回复、信任评分以及检查发送状态），请参阅 [references/api.md](references/api.md)。
**注意**：默认情况下，回复操作会采用“回复全部”（reply-all）的方式，这样可以保留历史抄送信息，并确保所有接收者都能收到邮件。
- **Tier 2** 及更高版本支持通过 `cc[]` 添加抄送地址；**Tier 1** 中，`cc[]` 仅能包含该邮件对话历史中已存在的抄送地址。
**安全提示**：当 Prompt Shield 将收到的邮件标记为高风险时，**Tier 2/3** 的发送流程可能需要在发送邮件前创建一个临时性的 `security_ack_token`（`POST /v1/security/ack`）。
**配额提示**：使用 `GET /v1/usage` 命令监控每月的使用情况（`used`、`remaining`、`state`、`reset_at`），以避免在运行过程中超出配额限制。

### 唤醒机制（推荐使用）
许多大型语言模型（LLM）的运行时无法可靠地维持后台轮询功能。建议尽可能使用唤醒 Webhook：
- 配置 Webhook：`PUT /v1/wake/webhook`
- 查看状态：`GET /v1/wake/webhook`
- 禁用 Webhook：`DELETE /v1/wake/webhook`

THRD 会发送签名的 `inbox_pending` 响应，您的运行时应立即通过 `GET /v1/events` 获取最新信息并进行确认。

**Webhook 不可用时的备用方案**：
```bash
python3 scripts/poll_daemon.py --cursor-file .thrd_cursor --on-events "echo inbound-ready"
```
该方案可以在没有公共 Webhook 的情况下维持邮件的正常发送功能。

**心跳机制（适用于 OpenClaw 及类似运行时）**：
- 如果您的运行时具有心跳调度器（例如每 30 分钟一次），请在每次心跳时检查收件箱状态。
- 在每次心跳时，使用保存的游标调用 `GET /v1/events`，处理返回的事件，然后通过 `POST /v1/events/ack` 更新游标。
- 30 分钟的间隔作为最低限度的备用方案；但对于需要 OTP 或账户验证的流程，建议使用更短的心跳间隔（1-5 分钟）。
- 这种轮询方式不会发送电子邮件，也不会消耗 THRD 的月度发送配额。

## 相关工具
- `scripts/onboard.py`：用于快速配置新的电子邮件账户。
- `scripts/checkout.py`：生成用于升级的 Stripe 支付链接。
- `scripts/openapi_sync.py`：刷新/缓存最新的 OpenAPI 合同并获取当前版本信息。
- `scripts/poll_daemon.py`：适用于没有唤醒 Webhook 功能的运行时的长时间轮询守护进程。