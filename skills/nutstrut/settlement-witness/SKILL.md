---
name: settlement-witness
description: "OpenClaw 技能：从 SettlementWitness 获取 replay-stable 收据（已签名的 SAR v0.1 版本）。该操作是无状态的（stateless），且具有确定性（deterministic）。"
---
# SettlementWitness（OpenClaw技能）

使用SettlementWitness生成一个可用于任务结算的、具有重放稳定性的收据（SAR v0.1）。

## 推荐使用方式（MCP）
POST https://defaultverifier.com/mcp

健康检查：
GET https://defaultverifier.com/mcp-healthz

MCP端点会返回完整的SettlementWitness收据JSON数据。

## 直接的REST接口替代方式
POST https://defaultverifier.com/settlement-witness
GET https://defaultverifier.com/settlement-witness  （返回JSON格式的帮助信息）

## 立即运行（复制/粘贴）

### Linux/macOS
```bash
curl -sS https://defaultverifier.com/settlement-witness \
  -H "Content-Type: application/json" \
  -d '{"task_id":"example-001","spec":{"expected":"foo"},"output":{"expected":"foo"}}'
```

### Windows PowerShell（重要提示）
PowerShell中会将`curl`别名为`Invoke-WebRequest`，这可能会导致“422 Invalid JSON”错误。
请使用`curl.exe`并传递文件形式的请求数据：

```powershell
@'
{"task_id":"example-001","spec":{"expected":"foo"},"output":{"expected":"foo"}}
'@ | Out-File -Encoding ascii -NoNewline body.json

curl.exe -X POST https://defaultverifier.com/settlement-witness `
  -H "Content-Type: application/json" `
  --data-binary "@body.json"
```

## 重要提示：安装/下载操作本身不会执行任何操作
许多客户端仅会执行发现操作（例如`tools/list`）。
要生成收据，必须触发实际的工具运行（MCP中的`tools/call`命令来执行`settlement_witness`）或发送上述REST请求。

## 必需输入参数
- task_id（字符串）
- spec（对象）
- output（对象）

## 示例REST请求
{
  "task_id": "example-002",
  "spec": { "expected": "foo" },
  "output": { "expected": "foo" }
}

## 请求结果解析
- PASS → 验证完成
- FAIL → 不自动进行结算
- INDETERMINATE → 重试或升级处理
- receipt_id → 稳定的收据标识符
- reason_code → 失败原因（例如：SPEC_MISMATCH）

## 安全注意事项
- 请勿在spec或output参数中传输任何敏感信息。
- 请确保spec和output的内容是确定的、可预测的。