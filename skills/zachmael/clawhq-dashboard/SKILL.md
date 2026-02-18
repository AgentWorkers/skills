# ClawHQ 仪表盘连接器

该插件负责将代理的状态、心跳信息以及任务完成情况报告到您的 ClawHQ 仪表盘。

## 必备条件

必须设置以下环境变量：
- `CLAWHQ_API_KEY` — 您的 ClawHQ API 密钥（可在“设置” → “API 密钥”中生成）

## 功能行为

### 会话开始时
报告当前任务的状态为“正在运行”：

**Windows（PowerShell）：**
```powershell
$headers = @{ "Authorization" = "Bearer $env:CLAWHQ_API_KEY"; "Content-Type" = "application/json" }
$body = @{ agent = "<agent_name>"; status = "working"; task = "<current task summary>" } | ConvertTo-Json
Invoke-RestMethod -Uri "https://app.clawhq.co/api/agents/report" -Method Post -Headers $headers -Body $body
```

**Mac/Linux（curl）：**
```bash
curl -s -X POST "https://app.clawhq.co/api/agents/report" \
  -H "Authorization: Bearer $CLAWHQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent":"<agent_name>","status":"working","task":"<current task summary>"}'
```

### 会话结束时
报告当前任务的状态为“空闲”：

**Windows：**
```powershell
$headers = @{ "Authorization" = "Bearer $env:CLAWHQ_API_KEY"; "Content-Type" = "application/json" }
$body = @{ agent = "<agent_name>"; status = "idle" } | ConvertTo-Json
Invoke-RestMethod -Uri "https://app.clawhq.co/api/agents/report" -Method Post -Headers $headers -Body $body
```

**Mac/Linux：**
```bash
curl -s -X POST "https://app.clawhq.co/api/agents/report" \
  -H "Authorization: Bearer $CLAWHQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"agent":"<agent_name>","status":"idle"}'
```

### 发送心跳信号
发送心跳信号以保持仪表盘数据的实时性。使用上述命令，并将 `status` 参数设置为 `heartbeat`。

## 注意事项
- 所有 API 调用都应采用“一次性执行”的方式（即调用后不再进行后续操作），请使用 `try/catch` 语句来处理可能的错误，以防错误导致代理程序阻塞。
- 请将 `<agent_name>` 替换为代理的名称（例如：“Eros”或“Atlas”）。
- 当首次报告时，API 会自动创建相应的代理；无需在仪表盘中进行任何额外设置。