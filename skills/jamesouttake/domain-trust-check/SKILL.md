---
name: domain-trust-check
description: "**URL安全扫描器与域名信誉检查工具**  
**使用场景：**  
- 在访问网站前检查URL的安全性；  
- 扫描电子邮件或消息中的链接；  
- 验证域名是否存在钓鱼、恶意软件或诈骗行为。  
**不适用场景：**  
- 用于提交恶意域名以获取奖励（请使用outtake-bounty-network）。"
metadata: { "openclaw": { "emoji": "🛡️", "requires": { "env": ["OUTTAKE_API_KEY"], "bins": ["curl"] }, "primaryEnv": "OUTTAKE_API_KEY", "homepage": "https://outtake.ai" } }
---
# 域名信任检查

在访问或推荐任何网址之前，请先检查其是否存在网络钓鱼、恶意软件、品牌滥用或诈骗行为。该功能由 [Outtake](https://outtake.ai) 的 Trust API 提供支持。

## 快速入门

> **已经注册了吗？** 如果 `OUTTAKE_API_KEY` 已设置完毕，请直接跳至 curl 命令部分。无需重新注册。

```bash
curl -s -X POST https://app.outtake.ai/api/v1/trust/check \
  -H "Authorization: Bearer $OUTTAKE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://suspicious-site.com"}'
# → {"data": {"url": "...", "verdict": "malicious", "confidence": 0.92, "safe_to_visit": "unsafe", "recommended_action": "block", ...}}
```

## 注册

只需完成一次设置，同一 API 密钥即可用于所有 Outtake 功能。

```bash
curl -s -X POST https://app.outtake.ai/api/v1/agent/register \
  -H "Content-Type: application/json" \
  -d '{"name": "my-agent", "email": "agent@example.com"}'
```

保存返回的 `api_key`——该密钥仅显示一次：

```bash
export OUTTAKE_API_KEY="outtake_..."
```

| 状态 | 含义 |
|---|---|
| 409 | 电子邮件地址已注册——请使用现有的密钥 |
| 429 | 每小时注册次数限制（5 次） |

可选字段：`wallet_address`（以太坊地址，用于奖励支付）、`agent_framework`（例如 "langchain"）。

## 解读结果

| 结果 | 是否安全 | 应采取的行动 |
|---|---|---|
| `malicious` | 不安全 | **禁止访问**。立即警告用户。 |
| `suspicious` | 安全或不确定 | **警告** 用户。如果判断为“不安全”，则视为恶意网站。 |
| `safe` | 安全 | 可以安全访问。 |
| `unknown` | 数据缺失 | 请谨慎操作。 |

**可信度评分：** `1.0` 表示人工审核；`0.7–0.99` 表示机器学习分类；`0.0` 表示数据缺失。

## 批量检查

使用 `POST /trust/check-batch` 命令一次检查最多 50 个网址：

```bash
curl -s -X POST https://app.outtake.ai/api/v1/trust/check-batch \
  -H "Authorization: Bearer $OUTTAKE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://link1.com", "https://link2.com"]}'
```

在检查多个网址时，建议使用批量处理方式以减少网络请求次数。如果请求中包含超过 50 个网址，系统会返回 `400` 错误代码。

## 相关功能

- **[outtake-bounty-network](https://clawhub.ai/skill/outtake-bounty-network)** — 每验证一个恶意域名，可赚取 5 美元 USDC。先使用该功能进行扫描，再提交确认的恶意网址。使用相同的 API 密钥。

## 技术支持

如有任何问题或反馈，请发送电子邮件至 [trust-check@outtake.ai](mailto:trust-check@outtake.ai)。