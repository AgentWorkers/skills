# Kalibr

该模块负责代理的自我优化与数据传输，能够收集代理的执行结果以及与大型语言模型（LLM）的交互信息，以支持持续的改进过程。

## 主要功能

- 收集代理执行结果
- 监测与大型语言模型的交互数据
- 智能模型路由功能（可选）
- 自我优化过程的跟踪记录

## 配置设置

```json
{
  "apiKey": "your-kalibr-api-key",
  "tenantId": "your-tenant-id",
  "apiUrl": "https://kalibr-intelligence.fly.dev",
  "enableRouting": false,
  "captureOutcomes": true,
  "captureLlmTelemetry": true
}
```