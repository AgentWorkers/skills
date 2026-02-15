---
name: xanlens-audit
description: **AI代理的GEO审计API**  
该API用于检查AI代理在ChatGPT、Perplexity、Gemini等平台上的品牌曝光度。  
使用x402支付方式，费用为0.99美元（USDC）。  
无需API密钥即可使用。
version: 2.0.0
---

# XanLens 审计服务

该服务用于检测品牌在人工智能搜索引擎中的可见度，并提供详细的优化报告（包括 GEO（生成式引擎优化）评分）。

## 快速入门

```bash
# Agent request → returns 402 with payment instructions
curl -X POST https://xanlens.xyz/api/v1/audit \
  -H "Content-Type: application/json" \
  -d '{"brand": "BRAND_NAME", "industry": "INDUSTRY"}'

# Pay 0.99 USDC on Base, then retry with tx hash
curl -X POST https://xanlens.xyz/api/v1/audit \
  -H "Content-Type: application/json" \
  -H "X-Payment-Tx: 0xYOUR_TX_HASH" \
  -d '{"brand": "BRAND_NAME", "industry": "INDUSTRY"}'
```

## 参数

| 参数 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| brand | string | 是 | 品牌或公司名称 |
| website | string | 否 | 需要分析的网站 URL |
| industry | string | 否 | 行业或领域（默认值："general"） |
| competitors | string[] | 否 | 最多可输入 5 个竞争对手的名称 |

## 响应结果

优化报告（JSON 格式）：
- `overall_score`（0-100 分）及对应的等级（用字母表示）
- 各搜索引擎的评分（如 Gemini、Perplexity 等）
- 分类统计结果（发现、品牌展示、对比等）
- 网站分析报告（包括结构标记、元标签等信息）
- 可操作的优化建议（具体改进措施）

## 支付方式

- **价格：** 每次审计费用为 0.99 美元（USDC）
- **网络：** Base（链 ID：8453）
- **协议：** x402
- **钱包地址：** `0xB33FF8b810670dFe8117E5936a1d5581A05f350D`
- **无需 API 密钥** — 每次查询单独付费，无需注册账户

## 支付流程

1. 向 `/api/v1/audit` 发送 POST 请求，接收包含支付详情的 402 响应
2. 将 0.99 美元（USDC）转账至 Base 链上的指定钱包
3. 重新发送请求，并在请求头中添加 `X-Payment-Tx: <tx_hash>` 以标识支付记录
4. 接收完整的审计报告

## MCP 工具

XanLens 审计服务也可作为 MCP（管理控制平台）工具使用：

```json
{
  "xanlens": {
    "url": "https://xanlens.xyz/api/mcp"
  }
}
```

使用方式：`xanlens_audit(brand, website?, industry?)`

## 相关链接

- 官网：https://xanlens.xyz
- API 文档：https://xanlens.xyz/api-docs
- MCP 端点：https://xanlens.xyz/api/mcp
- ClawHub 集成：xanlens-audit