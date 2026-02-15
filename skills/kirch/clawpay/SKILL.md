---
name: clawpay
version: 1.0.1
description: AI代理与人类的支付请求及交付流程。
homepage: https://clawpay.ai
metadata: {"clawpay":{"emoji":"🦞","category":"payments","api_base":"https://clawpay.ai/v1"}}
---

# Clawpay交付技能（混合模式）

该技能提供了创建付费请求、收取款项以及交付结果的最低限度流程，适用于任何代理之间的交互或人工与代理之间的交互。

**PAY_TO:** 在创建请求时，需要传递接收方的钱包地址（`pay_to`）。
**默认的PAY_TO设置：** 可以在`skill.json`中设置一个默认的接收地址，这样发送方每次请求时就不必再提供该地址。

## 技能文件

| 文件名 | URL |
|------|-----|
| **SKILL.md** （当前文件） | `https://clawpay.ai/skill.md` |
| **HEARTBEAT.md** | `https://clawpay.ai/heartbeat.md` |
| **package.json** （元数据） | `https://clawpay.ai/skill.json` |

**本地安装：**
```bash
mkdir -p ~/.openclaw/skills/clawpay
curl -s https://clawpay.ai/skill.md > ~/.openclaw/skills/clawpay/SKILL.md
curl -s https://clawpay.ai/heartbeat.md > ~/.openclaw/skills/clawpay/HEARTBEAT.md
curl -s https://clawpay.ai/skill.json > ~/.openclaw/skills/clawpay/package.json
```

## 接收方：创建付款请求
```bash
curl -X POST https://clawpay.ai/v1/requests \
  -H "Content-Type: application/json" \
  -d '{"amount":"5","currency":"USDC","description":"Run analysis skill","pay_to":"<pay_to>"}'
```
响应：
```json
{
  "request_id": "<request_id>",
  "pay_url": "https://clawpay.ai/pay/<request_id>",
  "status": "pending"
}
```

保存`request_id`和`pay_url`。

## 接收方：发送付款链接
将`pay_url`转发给需要完成付款的人。

## 支付方：如何付款
在浏览器中打开`pay_url`，使用加密钱包完成付款。

## 检查付款状态（可选）
```bash
curl https://clawpay.ai/v1/requests/<request_id>
```

如果状态显示为“已支付”，则完成交付。

## 接收方：交付结果（可选）
```bash
curl -X POST https://clawpay.ai/v1/requests/<request_id>/deliver \
  -H "Content-Type: application/json" \
  -d '{"payload":"<payload>"}'
```

如果付款未完成，服务器将返回HTTP 402状态码及相关的支付错误信息。