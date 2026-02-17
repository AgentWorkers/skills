---
name: thrd
description: "为您的人工智能代理提供一个专用的收件箱，并通过 thrd.email 安全地管理电子邮件。该服务包括即时入职支持、收件箱轮询、回复/发送功能（具有幂等性和策略控制）、针对冷发送邮件的“推理证明”机制、人工验证功能以及邮件送达情况的跟踪。此外，该服务不会将 API 密钥保存到磁盘上。"
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

该技能帮助您使用 [thrd.email](https://thrd.email) 为 AI 代理创建并管理一个独立的收件箱，而无需将您的个人收件箱与之关联。

**默认安全设置**：切勿将您的主收件箱连接到代理上；请使用专用的代理收件箱。

## 工作流程

### 同步 OpenAPI 合同（建议在使用工具前执行）
为了避免使用过时的信息，请刷新 OpenAPI 合同并查看 `info.version`：
```bash
python3 scripts/openapi_sync.py
python3 scripts/openapi_sync.py --print-version
```
此操作会利用 HTTP 缓存验证机制（`ETag`/`Last-Modified`），仅在合同内容发生变化时才会重新下载。

### 配置新的电子邮件账户
要创建新的电子邮件账户，请运行入职脚本：
```bash
python3 scripts/onboard.py --agent-name "My Agent" [--tenant-name "My Company"]
```
该脚本会将包含 `api_key` 和新收件箱地址的 JSON 数据输出到标准输出（stdout）。请将 `api_key` 视为敏感信息，切勿将其保存到文件中。

**安全提示**：**切勿将您的 API 密钥写入文件**。请将其存储在运行时的秘密管理器中，并将 `THRD_API_KEY` 设置为环境变量。（其他工具需要 `THRD_API_KEY`；但入职流程不需要。）

### 升级计划（计费）
要为您当前的租户启用付费计费，请使用结算脚本：
```bash
python3 scripts/checkout.py <plan_name>
```
可选的升级计划如下：
- `sandbox` -> Sandbox Starter（每月 9 欧元，每月发送邮件数量上限从 100 封提升至 2,000 封）
- `limited` -> Tier 2
- `verified` -> Tier 3

将生成的 Stripe 支付链接转发给您的负责人以完成支付。

### 人工确认（验证）
**Tier 3（已验证的发送行为）** 需要通过 X 进行人工确认：
- 启动确认流程：`POST /v1/claim/x/start`
- 将 `claim_url` 转发给您的负责人。
- 查看状态：`GET /v1/claim/x/status`

### 推理证明（Proof of Reasoning, PoR）
对于 Tier 3 的发送行为，系统可能会要求您解决逻辑问题以防止垃圾邮件。
- 如果收到 `428 por_required` 错误，请解决响应中提供的逻辑问题。
- 重新发送请求，并附带 `por_token` 和 `por_answer`。

### 管理电子邮件并跟踪发送状态
有关详细的 API 使用方法（轮询、发送、回复、信任评分以及检查发送状态），请参阅 [references/api.md](references/api.md)。
**注意**：默认情况下，回复操作会采用“回复全部”（reply-all）的方式，这样可以保留历史抄送信息，并确保所有参与者都不会被遗漏。在 Tier 2 及更高版本中，您可以使用 `cc[]` 参数添加抄送地址；在 Tier 1 中，`cc[]` 仅允许包含该邮件对话历史中已存在的抄送地址。

**安全提示**：当 Prompt Shield 将收到的邮件标记为高风险时，Tier 2/3 级别的操作可能需要先通过 `POST /v1/security/ack` 创建一个临时性的 `security_ack_token`，然后再执行 `reply` 或 `send` 操作。

### 配置唤醒机制（推荐使用）
许多大型语言模型（LLM）运行时无法可靠地持续执行后台轮询。请尽可能使用唤醒 Webhook：
- 配置 Webhook：`PUT /v1/wake/webhook`
- 查看状态：`GET /v1/wake/webhook`
- 禁用 Webhook：`DELETE /v1/wake/webhook`

THRD 会发送带有签名信息的 `inbox_pending` 呼叫；您的运行时应立即通过 `GET /v1/events` 获取最新信息并作出响应。

**Webhook 不可用时的备用方案**：
```bash
python3 scripts/poll_daemon.py --cursor-file .thrd_cursor --on-events "echo inbound-ready"
```
该方案可以在没有公共 Webhook 端点的情况下仍保持邮件的正常发送。
**安全提示**：`--on-events` 参数以安全的方式运行（不支持 shell 命令，如 `;`、`&&`、管道操作或重定向）。

## 相关工具
- `scripts/onboard.py`：用于快速配置新的电子邮件账户。
- `scripts/checkout.py`：生成用于升级的 Stripe 支付链接。
- `scripts/openapi_sync.py`：刷新/缓存最新的 OpenAPI 合同并获取当前版本信息。
- `scripts/poll_daemon.py`：适用于没有唤醒 Webhook 功能的运行时的备用轮询守护进程。