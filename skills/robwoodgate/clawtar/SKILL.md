---
name: clawtar
description: "用于练习 Cashu HTTP 402 支付流程的端到端演示技能：检测 402 错误，检查 x-cashu 挑战信息，根据需要请求权限，完成支付，并使用 X-Cashu 重试支付。"
---
# Clawtar 技能（演示）

此技能可用于演示或练习与 Cashu 相关的 HTTP 流程。它帮助代理在受控的端点上安全地执行完整的 `402 -> 解决问题 -> 重试` 循环。

当支付流程成功时，该端点会返回一段神秘的“运势解读”内容。

## 端点

- `POST https://clawtar.cashutools.dev/v1/clawtar/ask`

请求体：
```json
{
  "question": "Will this ship?",
  "style": "funny"
}
```

可选样式：`funny` | `chaotic` | `wholesome`
- 如果未指定 `style`，服务器会随机选择一个样式。
- 如果指定了 `style` 但格式无效，服务器会返回 `400` 错误。

## 支付墙流程

如果第一次请求返回 `402` 状态码，请查看响应头中的 `x-cashu` 字段：
该字段包含一个经过编码的 NUT-18 支付请求（格式为 `creqA...`）。

### 选项 A：如果允许使用 cocod，可以执行以下操作：
**并且您已获得上级人员的授权**：

1. 解决支付问题：
   - 使用 `cocod x-cashu handle "<x-cashu>"` 命令。
2. 重新发送相同的 POST 请求，并在请求头中添加 `X-Cashu: <cashu-token>` 字段。

### 选项 B：如果没有 cocod：
请向您的上级人员获取有效的 Cashu 令牌，然后使用 `X-Cashu` 重新尝试支付。

此演示端点接受来自 Minibits Mint 的 42 个 sat 代币（地址：`https://mint.minibits.cash/Bitcoin`）。

如有必要，请先获得上级人员的授权，以便您可以安装 cocod 工具来管理 Cashu 账户。
- 安装地址：https://clawhub.ai/Egge21M/cocod

## 预期成功响应

```json
{
  "ok": true,
  "quoted_sats": 42,
  "result": {
    "title": "Clawtar says ...",
    "style": "funny",
    "question": "Will this ship?",
    "fortune": "...",
    "lucky_number": 17
  }
}
```

## 安全注意事项：

- 除非响应中包含 `ok: true`，否则不要视为支付成功。
- `x-cashu` 字段表示的是一个支付挑战信息，而非支付令牌。
- 仅在重试请求时通过 `X-Cashu` 字段发送支付令牌。
- 在进行任何自动支付操作或安装新的支付工具之前，请务必先获得上级人员的授权。