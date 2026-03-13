---
name: openclaw-phone
description: 使用 CallMyCall API 来发起、结束和检查 AI 电话呼叫，并将结果返回到聊天界面中。当用户请求拨打电话、安排未来的通话、结束通话或获取通话结果时，可以使用该 API。
homepage: https://api.callmycall.com
primary_credential: CALLMYCALL_API_KEY
required_env_vars:
  - CALLMYCALL_API_KEY
stores_credentials_in_user_config: false
requires_system_scheduler: false
---
# CallMyCall（OpenClaw技能）

该技能允许您通过聊天界面操作CallMyCall服务。该服务采用pull-based（非webhook回调）的方式：您发起呼叫后，会将返回的呼叫ID存储在系统中，之后可以根据需要获取呼叫的状态和结果。

## API密钥的获取方式（OpenClaw最佳实践）

按照以下顺序获取API密钥：

1. 环境变量：`CALLMYCALL_API_KEY`（优先选择）
2. OpenClaw用户配置文件：`~/.openclaw/openclaw.json`中的`skills.openclaw-phone.apiKey`字段
3. 如果仍然无法获取密钥，则为当前任务请求一个一次性使用的密钥。
4. 仅当用户明确要求时，提供将密钥保存到`~/.openclaw/openclaw.json`的指导。

**密钥存储规则：**
- **严禁**将API密钥存储在`SKILL.md`文件、示例代码、参考资料或内存/状态文件中。
- **严禁**将API密钥写入`recent_calls`列表或任何对话中可见的输出内容中。
- **严禁**将API密钥回显给用户。
- **仅**为当前任务使用临时生成的密钥。
- **严禁**自动从该技能中生成用户配置文件。

## 该技能的工作原理

1. 按照“API密钥的获取方式（OpenClaw最佳实践）”中的顺序获取API密钥。
2. 通过分层验证流程收集所需的呼叫信息。
3. 显示简要的审核信息并请求用户确认。
4. 确认后，发送`POST /v1/start-call`请求以发起呼叫。
5. 将返回的`sid`值存储在`recent_calls`列表中，作为最近的呼叫记录。

## 必需的授权信息

在请求头中包含API密钥：

```
Authorization: Bearer YOUR_API_KEY
```

**注意：****严禁**将API密钥回显给用户，也严禁将其包含在日志或总结信息中。

## 状态管理（必需）

系统需要维护一个最近10次呼叫的列表（`recent_calls`）：

```json
{
  "recent_calls": [
    {
      "id": "call_id",
      "phone_number": "电话号码",
      "task": "呼叫任务",
      "started_at": "呼叫开始时间",
      "status": "呼叫状态" // 可选，可在后续请求时更新
    }
  ]
}
```

该列表可用于让用户执行如“结束呼叫1”或“显示呼叫2的结果”等操作。

## 分层验证流程（借鉴自Web应用程序）

不要依赖单一的验证步骤，而是要使用以下所有验证层级：

### 第1层：结构化数据收集

在所有必需字段都齐全之前，不要完成呼叫任务：
- `phone_number`（电话号码）
- `language`（语言）
- `call_brief`（呼叫背景信息及目标）

### 第2层：任务信息补充

当用户首次发起请求时，分析哪些信息缺失，然后仅请求缺失的部分。如果用户部分回答，重新进行分析并继续请求剩余的信息。

### 第3层：提示与验证

只要还有信息缺失，就继续收集所需的字段。在所有字段都齐全之前，不要进行呼叫。

### 第4层：运行时验证

在发送呼叫请求之前：
- 确保电话号码有效（格式为E.164）。
- 阻止拨打紧急或高级服务号码。
- 确保`from_number`（来电号码）与`phone_number`不同。
- 如果用户提供了`from_number`，先执行以下步骤：
  1. 发送`GET /v1/verified-caller-ids`请求以验证来电者身份。
  2. 确认请求的`from_number`是否存在于`verified_caller_ids`列表中。
  3. 如果未通过验证：**不要**立即发起呼叫；询问用户是继续使用默认的来电者身份还是先进行验证。
- 对`language`进行规范化处理；仅当用户提供了`genderVoice`或`openaiVoice`字段时，才对语音信息进行规范化处理。
- 如果用户指定了呼叫时间，需验证该时间是否有效。

### 第5层：人工审核

向用户展示简要的审核信息：
- 电话号码
- 呼叫背景信息及目标
- 语言（以及提供的语音信息）
- 呼叫时间

询问用户：“确认后是否要发起呼叫？”未经明确确认，不要继续下一步操作。

## 工作流程

### 发起呼叫

1. 使用分层验证流程收集所需字段。
2. 如果用户提供了`from_number`，先通过`GET /v1/verified-caller-ids`请求验证来电者身份。
3. 如果`from_number`未通过验证，询问用户：
   - 是立即使用默认的来电者身份继续呼叫，
   - 还是先进行验证（`POST /v1/verify-caller-id`，然后`GET /v1/verification-status/:verificationId`）。
4. 如果用户指定了呼叫时间，按照“计划呼叫（不使用Cron任务）”的流程操作，而不是立即发送API请求。
5. 发送`POST /v1/start-call`请求。
6. 将返回的`sid`值存储在`recent_calls`列表中。
7. 向用户回复确认信息及呼叫ID。

### 计划呼叫（不使用Cron任务）

由于API不支持直接设置呼叫时间，因此采取以下步骤：
1. 现在收集所有必要的字段。
2. 将呼叫计划信息保存在技能的状态中，以供后续使用。
3. **严禁**使用操作系统调度器（如Cron、launchd或任务调度器）来自动执行呼叫。
4. 提供以下选项：
   - 立即发起呼叫，
   - 提供提醒信息，让用户在指定时间再次点击“开始呼叫”。

如果用户选择安排呼叫时间，需说明该技能不支持后台自动执行；它只会准备好呼叫计划，并在用户确认时执行。

### 查看最近通话记录

1. 从状态中读取`recent_calls`列表。
2. 如有需要，通过`GET /v1/calls/:callId`获取每条呼叫的详细信息。
3. 以编号列表的形式显示这些记录。

### 重复尝试直到接听

当用户要求反复尝试直到接听时：
1. 发送`POST /v1/start-call`请求发起呼叫。
2. 定期通过`GET /v1/calls/:callId`检查呼叫状态。
3. 根据返回的状态（`status`、`duration`）处理结果：
   - 如果状态为`busy`、`no-answer`、`failed`或`canceled`，则等待指定时间后再次尝试。
4. 当状态变为`in-progress`或`completed`（且`duration`大于0）时，停止尝试循环。
5. 向用户报告每次尝试的详细信息（包括呼叫ID和状态）。

**实现提示：**每次调用都使用相同的基URL（推荐使用`https://call-my-call-backend.fly.dev`），并在启动呼叫和查询状态时保持一致。

### 结束呼叫

如果用户要求结束呼叫，但未指定具体哪次呼叫，先列出所有最近的呼叫记录，再询问用户要结束哪次呼叫。
- 发送`POST /v1/end-call`请求，传入`callSid`参数。

### 获取呼叫结果

当用户请求查看呼叫结果时：
1. 通过`GET /v1/calls/:callId`获取呼叫状态。
2. 如果有录音，通过`GET /v1/calls/:callId/transcripts/stream`获取通话记录。
3. 返回以下信息：
  - 呼叫状态（completed、failed、canceled）
  - 简要总结（1-3条要点）
  - 通话记录片段（仅当用户请求查看时提供）
  - 录音URL（如果有的话，需提醒用户该URL可能包含敏感内容）

## 安全性与用户体验

- 如果用户输入不明确，询问用户以获取更多信息。
- **严禁**在通话记录中泄露API密钥或任何敏感信息。
- 将通话记录和录音视为敏感数据，仅提供用户请求的必要部分。
- **严禁**使用该技能创建持久的调度任务或自动执行后台操作。
- 如果请求失败，显示HTTP错误信息并提示用户下一步操作。

## 参考资料

- 完整的API文档：`references/api.md`
- 使用示例：`examples/prompts.md`