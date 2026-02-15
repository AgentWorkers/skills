---
name: visibleai-audit
description: **AI代理的GEO审计API**  
用于检查ChatGPT、Perplexity、Gemini等平台上的品牌曝光度。  
使用x402支付0.99美元（USDC），无需API密钥。
version: 1.1.0
---

# VisibleAI Audit

该服务用于检测品牌在人工智能搜索引擎中的可见度，并提供详细的优化报告（包括GEO（生成式引擎优化）评分）。

## 快速入门

```bash
# Agent request → returns 402 with payment instructions
curl -X POST https://visibleai.space/api/v1/audit \
  -H "Content-Type: application/json" \
  -d '{"brand": "BRAND_NAME", "industry": "INDUSTRY"}'

# Pay 0.99 USDC on Base, then retry with tx hash
curl -X POST https://visibleai.space/api/v1/audit \
  -H "Content-Type: application/json" \
  -H "X-Payment-Tx: 0xYOUR_TX_HASH" \
  -d '{"brand": "BRAND_NAME", "industry": "INDUSTRY"}'
```

## 参数

| 参数 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| brand | string | 是 | 品牌或公司名称 |
| website | string | 否 | 需要分析的网站URL |
| industry | string | 否 | 行业或领域（默认值：“general”） |
| competitors | string[] | 否 | 最多可输入5个竞争对手的名称 |

## 响应结果

优化报告（JSON格式）：
- **整体评分**（0-100分）及对应的等级（如“A”或“B”等）
- 各搜索引擎的评分（如Gemini、Perplexity等）
- 分类统计结果（发现、品牌展示、对比等）
- 网站分析信息（如结构标记、元标签等）
- 可操作的**优化建议**——具体的改进措施以提高可见度

## 支付方式

- **价格：** 每次审计费用为0.99美元（USDC）
- **网络：** Base（链ID：8453）
- **协议：** x402
- **钱包地址：** `0xB33FF8b810670dFe8117E5936a1d5581A05f350D`
- **无需API密钥**——按查询次数付费，无需注册账户

## 支付流程

1. 向 `/api/v1/audit` 发送POST请求，接收包含支付详情的402响应。
2. 将0.99美元（USDC）转账至Base链上的指定钱包。
3. 重新发送请求，并在请求头中添加 `X-Payment-Tx: <tx_hash>` 字段。
4. 接收完整的审计报告。

## MCP工具

该服务也可作为MCP（Management Console）工具使用：

```json
{
  "visibleai": {
    "url": "https://visibleai.space/api/mcp"
  }
}
```

使用方式：`visibleai_audit(brand, website?, industry?)`

## 相关链接

- 官网：https://visibleai.space
- API文档：https://visibleai.space/api-docs
- MCP管理界面：https://visibleai.space/api/mcp
- ClawHub集成：visibleai-audit