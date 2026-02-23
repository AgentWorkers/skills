---
name: thrd
description: "为您的人工智能代理提供一个专用的收件箱，并通过 thrd.email 安全地管理电子邮件。该服务支持即时入职流程、收件箱轮询、回复/发送（操作具有幂等性且受策略控制）、冷邮件发送时的“推理证明”机制、人工验证功能以及邮件送达情况的跟踪。此外，该服务不会将 API 密钥保存到磁盘上。"
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
# 第三电子邮件技能（Third Email Skill）

该技能帮助您使用 [thrd.email](https://thrd.email) 为 AI 代理创建并管理一个独立的收件箱，而无需将您的个人收件箱与之关联。

**安全提示**：默认情况下，不要将您的主收件箱连接到 AI 代理；请使用专用的代理收件箱。

## 工作流程

### 同步 OpenAPI 合同（建议在使用工具前执行）
为了避免使用过时的信息，请刷新 OpenAPI 合同并查看 `info.version`：
```bash
python3 scripts/openapi_sync.py
python3 scripts/openapi_sync.py --print-version
```
该操作会利用 HTTP 缓存验证机制（`ETag`/`Last-Modified`），仅在合同内容发生变化时才会重新下载。

### 配置新电子邮件账户
要创建一个新的电子邮件账户，请运行入职脚本：
```bash
python3 scripts/onboard.py --agent-name "My Agent" [--tenant-name "My Company"]
```
该脚本会将新收件箱的相关数据以及一个 **已屏蔽** 的 API 密钥以 JSON 格式输出到标准输出（stdout）。

如果您需要在受信任的终端中获取一次性的原始 API 密钥，请执行以下操作：
```bash
python3 scripts/onboard.py --agent-name "My Agent" --reveal-api-key
```

**安全提示**：**切勿将 API 密钥保存到磁盘上**。请将其存储在运行时的密钥管理器中，并将 `THRD_API_KEY` 设置为环境变量。其他工具也需要 `THRD_API_KEY`，但入职流程不需要。

### 升级计划（计费）
要为您当前的租户启用付费计费，请使用结算脚本：
```bash
python3 scripts/checkout.py <plan_name>
```
可用计划如下：
- `sandbox` → Sandbox Starter（每月 9 欧元，每月发送邮件数量上限从 100 封提升至 2,000 封）
- `limited` → Tier 2
- `verified` → Tier 3

将生成的 Stripe 支付链接转发给您的负责人以完成支付。

### 人工确认（验证）
**Tier 3（已验证的发送功能）** 需要通过 X 进行人工确认：
- 启动确认流程：`POST /v1/claim/x/start`
- 将 `claim_url` 转发给您的负责人。
- 检查状态：`GET /v1/claim/x/status`

### 推理验证（Proof of Reasoning, PoR）
对于 Tier 3 的发送功能，系统可能会要求提供推理验证结果以防止垃圾邮件。
- 如果收到 `428 por_required` 错误，请解决响应中提供的逻辑问题。
- 重新发送请求时需包含 `por_token` 和 `por_answer`。

### 管理电子邮件并跟踪发送状态
有关详细的 API 使用说明（轮询、发送、回复、信任评分以及检查发送状态），请参阅 [references/api.md](references/api.md)。
**注意**：默认情况下，回复操作会采用“回复全部”（reply-all）的方式，保留历史抄送地址，并确保接收者不会从最新的收件人列表中遗漏。
- Tier 2 及更高版本支持通过 `cc[]` 添加抄送地址；在 Tier 1 中，`cc[]` 仅能包含该邮件对话历史中已存在的抄送地址。
**安全提示**：当 Prompt Shield 将收到的邮件标记为高风险时，Tier 2/3 的发送流程可能需要先通过 `POST /v1/security/ack` 创建一个临时性的 `security_ack_token`，然后再执行 `reply`/`send` 操作。
**配额提示**：使用 `GET /v1/usage` 查看每月的使用情况（`used`、`remaining`、`state`、`reset_at`），以避免在运行过程中超出使用限制。

### 唤醒机制（推荐使用）
许多大型语言模型（LLM）运行时无法可靠地维持后台轮询功能。建议尽可能使用唤醒 Webhook：
- 配置 Webhook：`PUT /v1/wake/webhook`
- 查看状态：`GET /v1/wake/webhook`
- 禁用 Webhook：`DELETE /v1/wake/webhook`

THRD 会发送带有签名的 `inbox_pending` 呼点（ping），您的运行时应立即通过 `GET /v1/events` 进行数据拉取并确认接收。

**Webhook 不可用时的备用方案**：
```bash
python3 scripts/poll_daemon.py --cursor-file .thrd_cursor
```
该方案可以在没有公共 Webhook 端点的情况下维持基于轮询的邮件发送功能。

## 工具
- `scripts/onboard.py`：用于快速配置新的电子邮件收件箱。
- `scripts/checkout.py`：生成用于升级的 Stripe 支付链接。
- `scripts/openapi_sync.py`：刷新/缓存最新的 OpenAPI 合同并获取当前 `info.version`。
- `scripts/poll_daemon.py`：为不支持唤醒 Webhook 的运行时提供备用的长时间轮询服务。