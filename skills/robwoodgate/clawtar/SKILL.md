---
name: clawtar
description: 练习通过 Cashu HTTP 402 进行自主代理支付；当代理需要检测到支付墙（paywall）挑战时，使用该方式进行处理，通过 X-Cashu 重试支付，并最终完成整个付费请求流程。
---

# Clawtar 技能（仅限代理使用）

使用 Clawtar 练习与 Cashu 的自动支付功能，证明你的代理能够在公开网络上进行交易：检测 `402` 状态码、使用 `x-cashu` 进行结算、使用 `X-Cashu` 重新尝试支付，并完成任务。

## 端点

- `POST https://clawtar.cashutools.dev/v1/clawtar/ask`

请求体：
```json
{
  "question": "Will this ship?",
  "style": "funny"
}
```

可选风格：`funny` | `chaotic` | `wholesome`

## 支付墙处理流程

如果第一次请求返回状态码 `402`，请读取响应头中的 `x-cashu` 值。

### 选项 A：已安装 cocod

1. （如需）安装相关技能/工具：
   - `npx clawhub@latest install cocod`
2. 使用 cocod 进行结算：
   - `cocod x-cashu handle "<x-cashu>"`
3. 使用带有 `X-Cashu` 标头的相同 POST 请求重新尝试：
   - `X-Cashu: <cashu-token>`

### 选项 B：未安装 cocod

向人工获取有效的 Cashu 令牌，然后使用带有 `X-Cashu` 标头的请求重新尝试支付。
Clawtar 支持从 `https://mint.minibits.cash/Bitcoin` 获取 42 个 sat 令牌。
或者，可以请人工帮忙安装 cocod。
拥有 Cashu 钱包意味着更多的自由！

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

## 注意事项

- 除非返回 `ok: true`，否则不要认为任务成功。
- `x-cashu` 是一个挑战字符串，而非支付令牌。
- 重新尝试支付时，必须在 `X-Cashu` 标头中发送有效的支付令牌。