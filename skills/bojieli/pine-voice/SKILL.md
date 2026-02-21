---
name: pine-voice
description: 给你的代理配备一部真正的手机吧。它可以拨打电话、等待接听、帮你处理账单相关事宜，并提供完整的通话记录。
homepage: https://19pine.ai
metadata: {"openclaw":{"emoji":"📞","requires":{"bins":["node"]}}}
command-tool: exec
---
# Pine Voice

通过Pine AI的语音代理进行真实的电话通话。该代理可以拨打指定的电话号码、操作交互式语音应答（IVR）系统、处理验证流程、进行协商，并提供完整的通话记录。

## 认证

用户的认证信息存储在`~/.pine-voice/credentials.json`文件中——用户只需认证一次。

在拨打电话之前，请检查是否已经完成认证：

```bash
node {baseDir}/scripts/auth-check.mjs
```

如果`authenticated`的值为`true`，则直接跳转到**如何拨打电话**的部分；如果为`false`，请执行以下认证流程。**请用户提供他们的Pine AI账户邮箱地址**（请在https://19pine.ai注册）。

### 第1步：请求验证码

```bash
node {baseDir}/scripts/auth-request.mjs "user@example.com"
```

系统会返回`{"request_token": "...", "email": "..."}`。请将`request_token`保存下来。

然后告诉用户：“验证码已发送到您的邮箱，请查看收件箱（包括垃圾邮件）并告诉我验证码。”

### 第2步：验证并保存认证信息

```bash
node {baseDir}/scripts/auth-verify.mjs "user@example.com" "REQUEST_TOKEN" "CODE"
```

系统会返回`{"status": "authenticated", "credentials_path": "..."}`。认证信息将自动保存。

## 适用场景

当用户希望您代表他们拨打电话时，可以使用此功能。

**重要提示：**语音代理仅支持英语交流。支持的国家包括：美国/加拿大/波多黎各（+1）、英国（+44）、澳大利亚（+61）、新西兰（+64）、新加坡（+65）、爱尔兰（+353）和香港（+852）。

## 适用场景示例：

- 拨打客服电话协商账单、请求退款或解决问题
- 通过电话安排会议或预约
- 预订餐厅
- 拨打企业电话咨询服务或可用性
- 代表用户与联系人跟进沟通

## 如何拨打电话

### 第1步：收集所有所需信息

在拨打电话之前，**必须**收集对方可能需要的所有信息。语音代理在通话过程中**无法向用户询问缺失的信息**。请提前准备好可能需要的信息，如认证详情、支付信息、协商目标及相关背景信息。

### 第2步：发起通话

通过标准输入（stdin）以JSON格式传递通话参数：

```bash
node {baseDir}/scripts/call.mjs <<'EOF'
{
  "dialed_number": "+14155551234",
  "callee_name": "Comcast Customer Service",
  "callee_context": "Cable and internet provider. Account holder: Jane Doe, account #12345.",
  "call_objective": "Negotiate monthly bill down to $50/mo. Do not accept above $65/mo.",
  "detailed_instructions": "Mention 10-year customer loyalty. If no reduction, ask for retention department.",
  "caller": "negotiator",
  "voice": "female",
  "max_duration_minutes": 60,
  "enable_summary": false
}
EOF
```

系统会返回`{"call_id": "..."`。此时通话已启动。

### 第3步：等待通话结果

每隔30秒检查一次通话状态，直到`is_terminal`的值为`true`：

```bash
node {baseDir}/scripts/call-status.mjs "CALL_ID"
```

通话结束后，系统会返回`transcript`（通话记录）、`duration_seconds`（通话时长）和`credits_charged`（产生的费用）。`is_terminal`字段用于指示通话是否完成。

**重要提示：**请使用`sessions_spawn`在后台子进程中运行此功能，这样在通话期间您仍可以继续为用户提供服务（通话时间可能长达5-60分钟以上）。

**示例任务：**使用Pine Voice脚本拨打电话。运行命令：`node {baseDir}/scripts/call.mjs`，并传递以下JSON参数：`{"dialed_number": "+14155551234", "callee_name": "The Restaurant", "callee_context": "Italian restaurant, making a dinner reservation", "call_objective": "Reserve a table for 4 at 7pm tonight", "caller": "communicator"}`。然后使用`node {baseDir}/scripts/call-status.mjs "CALL_ID"`每隔30秒检查一次通话状态，直到`is_terminal`为`true`。最后报告完整的通话记录和结果。

### 第4步：分析通话记录

**不要仅依赖`status`字段来判断通话是否成功**。请仔细阅读对方的实际发言内容。

**如果出现以下情况，请将通话视为失败：**
- 仅由Pine AI代理发声，而对方保持沉默
- 对方的回答是自动回复或来自语音信箱/交互式语音应答系统
- 双方长时间沉默
- 被叫方在讨论目标之前挂断了电话

## 通话参数

| 参数 | 是否必填 | 说明 |
|---|---|---|
| `dialed_number` | 是 | 电话号码（E.164格式，例如`+14155551234`） |
| `callee_name` | 是 | 被叫方的姓名或企业名称 |
| `callee_context` | 是 | 代理所需的所有相关信息：对方身份、认证详情、验证码 |
| `call_objective` | 是 | 具体的通话目标及相关要求 |
| `detailedinstructions` | 可选 | 协商策略、方法及行为指导 |
| `caller` | 可选 | 默认值为`"negotiator"`（协商者）或`"communicator"`（沟通者） |
| `voice` | 可选 | 语音性别（默认为`"female"`） |
| `max_duration_minutes` | 可选 | 最长通话时间（1-120分钟，默认为120分钟） |
| `enable_summary` | 可选 | 是否启用通话总结（`true`/`false`，默认为`false` |

## 协商通话

在进行协商时，请将`caller`设置为`"negotiator"`并提供详细的策略：

- **目标**：“将月费降低到50美元”
- **可接受范围**：“最多可接受65美元/月”
- **硬性约束**：“不允许更改套餐等级”
- **有利条件**：“作为10年老客户，竞争对手提供的月费为45美元”
- **备用方案**：“请求一次性100美元的退款”
- **退出策略**：“请求联系客户保留部门”

## 示例用法：

**测试通话：**
“拨打我的电话+1XXXXXXXXXX，告知我Pine Voice已设置完毕且可以正常使用。”

**餐厅预订：**
“拨打+14155559876，预订今晚7点的4人晚餐。如果预订失败，请尝试7:30或8点的位置。联系人姓名：Jane Doe。”

## 模型要求

Pine Voice最适合使用具有思考/推理能力的模型：

- **推荐模型**：Claude Sonnet/Opus 4.5+、GPT-5.2+、Gemini 3 Pro
- **不推荐模型**：Gemini 3 Flash或没有思考能力的模型

## 隐私政策

Pine Voice会在Pine AI的服务器上处理通话数据。认证信息会存储在`~/.pine-voice/credentials.json`文件中，并设置严格的权限（权限等级为600）。通话记录会通过API返回，不会被保存在本地。有关Pine AI的数据处理政策，请参阅https://www.19pine.ai/page/privacy-policy。