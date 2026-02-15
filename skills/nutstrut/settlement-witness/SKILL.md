---
name: settlement-witness
description: "OpenClaw 技能：从 SettlementWitness 生成确定性的、带有签名的 SAR v0.1 收据。该功能是无状态的（即不保留会话状态），且具有确定性（即每次调用都能产生相同的结果）。"
---

# SettlementWitness（OpenClaw技能）

使用SettlementWitness生成用于代理结算的确定性收据（SAR v0.1）。

## 推荐使用方式（MCP - 首选）
POST https://defaultverifier.com/mcp  
健康检查：GET https://defaultverifier.com/mcp-healthz  

工具名称：settlement_witness（位于tools/call目录下）  

MCP端点会直接返回SettlementWitness收据的JSON格式数据。这是推荐的集成方式。  

## 直接使用REST接口的替代方案  
POST https://defaultverifier.com/settlement-witness （推荐，无需在路径末尾添加斜杠）  
POST https://defaultverifier.com/settlement-witness/ （ également accepté；会重定向）  
GET https://defaultverifier.com/settlement-witness （返回JSON格式的帮助信息）  

## 验证规范  
规范文档：https://defaultverifier.com/spec/sar-v0.1  
公钥：https://defaultverifier.com/.well-known/sar-keys.json  

## 必需输入参数  
- task_id（字符串）  
- spec（对象）  
- output（对象）  

## 示例REST请求  
```json
{
  "task_id": "example-002",
  "spec": { "expected": "foo" },
  "output": { "expected": "foo" }
}
```

## 结果解释  
- PASS：验证成功  
- FAIL：无法自动完成结算  
- INDETERMINATE：需要重试或升级处理  
- receipt_id：收据的唯一标识符  
- reason_code：失败的具体原因（例如：SPEC_MISMATCH）  

## 安全提示  
- 请勿在spec或output参数中传输任何敏感信息。  
- 确保spec和output的数据具有确定性（即每次请求产生的结果都应相同）。