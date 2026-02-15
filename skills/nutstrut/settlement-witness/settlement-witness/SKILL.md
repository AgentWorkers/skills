---
name: settlement-witness
description: "OpenClaw 技能：从公共的 SettlementWitness HTTPS 端点获取 replay-stable 的 PASS/FAIL 结果。该操作是无状态的（stateless）、确定性的（deterministic），并且结果会经过签名处理。"
---

# SettlementWitness（OpenClaw技能）

该技能会调用公开的SettlementWitness HTTPS接口。无需使用任何本地服务。

## 功能说明
当任务完成后，且需要在结算前获取交付证明时，可以调用SettlementWitness来获取一个具有 replay-stability（可重放稳定性）的收据。

SettlementWitness不负责评估任务的质量或解决争议，它仅根据预先定义的规则检查提供的输出是否与任务规范（spec）相匹配。

## 标准接口地址
- POST: https://defaultverifier.com/settlement-witness
- GET: https://defaultverifier.com/manifest

## 必需输入参数
- task_id（字符串）：任务ID
- spec（对象）：任务规范
- output（对象）：任务输出结果

## 示例请求
```json
{
  "task_id": "example-002",
  "spec": { "expected": "foo" },
  "output": { "expected": "foo" }
}
```

## 结果解析
- 如果 `verifier_response.verdict` 的值为 `PASS`，则表示任务已完成且验证通过。
- 如果 `verifier_response.verdict` 的值为 `FAIL`，则表示任务未通过验证，不能自动进行结算。
- `receipt_id` 是用于存储、记录或分享的稳定标识符。

## 安全注意事项
- 请勿在任务规范（spec）或输出结果（output）中包含任何敏感信息（如私钥、API密钥）。
- 请确保任务规范和输出结果尽可能简洁且具有确定性（使用哈希值或唯一标识符更为理想）。

## 安装方法（适用于OpenClaw用户）
将以下文件夹复制到您的OpenClaw技能目录中：
`settlement-witness/SKILL.md`