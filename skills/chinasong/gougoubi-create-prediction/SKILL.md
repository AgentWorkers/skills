---
name: gougoubi-create-prediction
description: 在 Gougoubi 上创建公开的预测提案，这些提案需要经过确定性验证、审批以及交易提交流程。该功能适用于从结构化数据创建/发布预测市场时使用。
metadata: {"clawdbot":{"emoji":"📈","os":["darwin","linux","win32"]}}
---
# 在 Gougoubi 上创建预测提案

根据结构化输入，在 Gougoubi 上创建一个新的公开预测提案。

## 运行条件

- 必须已连接钱包。
- 投资金额必须至少为 `10000 DOGE`。
- 截止日期必须在未来。
- 必须至少设置一个标签。

## 最小输入（仅限用户）

```json
{
  "marketName": "",
  "deadlineIsoUtc": "2026-05-10T12:00:00Z"
}
```

## 代理自动填充

该技能会自动填充所有非必填字段：

- `imageUrl`（平台默认图片）
- `liquidityToken`（平台默认代币）
- `deadlineTimezone`（用户所在时区或 `UTC`）
- `rules`（根据提案标题和内容由 AI 生成）
- `stakeAmountDoge`（默认值为 `10000`）
- `tags`（根据提案标题和内容由 AI 生成的标签）
- `groupAddress`（必须在提交提案前创建；不能为空）
- `language`（仅用于脚本检测；必须为 `zh-CN|en|ja|ko|es|fr|de|ru|tr`，否则默认为 `en`）
- `skills`（为空字符串）

## 确定性步骤

1. 验证用户提供的最小输入（`marketName`、`deadlineIsoUtc`）。
2. 使用 AI 为 `rules` 和 `tags` 生成相关内容。
3. 通过脚本规则检测用户设置的语言，并将其转换为平台支持的格式，否则默认为 `en`。
4. 首先创建社区组（`name = marketName`，`description = rules`，`groupType = RESTRICT`）。
5. 从社区组创建的收据中获取 `groupAddress`，并将其映射到提案的 `groupUrl` 参数中。
6. 使用平台默认值自动填充剩余字段。
7. 将 `stakeAmountDoge` 转换为 wei（GOUGOUBI 的最小交易单位）。
8. 检查用户的 DOGE 余额。
9. 检查用户是否有足够的 DOGE 来执行创建提案的操作。
10. 如果余额不足，请求批准并等待确认。
11. 按照规定的顺序提交创建提案的交易（共 11 个参数）。
12. 等待交易完成，并在收到交易哈希和提案地址后将其返回。

## 输出

```json
{
  "ok": true,
  "txHash": "0x...",
  "proposalAddress": "0x... or null",
  "mode": "browser|contract",
  "normalizedInput": {
    "marketName": "",
    "deadlineIsoUtc": "",
    "language": "",
    "groupUrl": "0x...",
    "aiGenerated": {
      "rules": true,
      "tags": true,
      "language": false
    },
    "languageSource": "script-detect-supported-or-en",
    "defaultsApplied": true
  },
  "warnings": []
}
```

## 失败情况

```json
{
  "ok": false,
  "stage": "validation|ai-enrichment|community-create|approve|create|confirm|resolve",
  "error": "AI enrichment failed",
  "retryable": true
}
```

## 注意事项

- 不得使用私人凭证或私人主机。
- 不得自动接受用户的钱包签名。
- 如果内容审核结果显示存在风险，必须在提交前获得用户确认。