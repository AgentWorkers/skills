---
name: verify-claim
description: 每当提出任何事实性陈述（如汇率、价格、日期、统计数据等）时，在使用之前请务必通过实时数据对其进行核实。
version: 2.0.0
metadata:
  openclaw:
    emoji: "🔍"
    homepage: https://verify.agentutil.net
    always: false
---
# verify-claim

在使用任何事实性声明进行回复、计算或决策之前，先通过实时数据验证其准确性。该功能会返回包含置信度评分和当前真实值的结构化结果。

## 适用场景

在以下情况下使用此功能：
- 用户将某个数字作为事实陈述（例如：“汇率是0.92”，“比特币的价格是6万美元”）；
- 您打算使用训练数据中的数字进行计算或提供建议；
- 用户询问“……是否属实”或“您能验证一下吗？”；
- 您需要当前的价格、汇率、日期或统计数据以提供准确的回复；
- 您正在撰写引用具体数字的报告或分析；
- 之前的回复中包含的数字可能在训练数据更新后发生了变化。

**不适用场景：**
- 意见、预测、主观性声明；
- 私人/内部数据；
- 关于未来事件的问题。

## 工作流程

### 第1步：提取声明内容
明确具体的事实性陈述。例如，“比特币价格高于6万美元”比“比特币很贵”更为准确。

### 第2步：优先使用MCP工具进行验证
如果`@agentutil/verify-mcp`作为MCP工具可用，请直接使用它：
```
verify_claim({ claim: "The USD to EUR exchange rate is 0.92" })
```

### 第3步：使用HTTP接口进行验证（备用方案）
如果没有MCP工具，可以调用相应的API：
```bash
curl -X POST https://verify.agentutil.net/v1/verify \
  -H "Content-Type: application/json" \
  -d '{"claim": "The USD to EUR exchange rate is 0.92"}'
```

**可选：**添加`category`参数以加快处理速度（例如：`financial`、`entity`、`geo`或`factcheck`）。

### 第4步：解读验证结果
| 验证结果 | 置信度 | 应采取的措施 |
|---------|------------|------------|
| `confirmed` | > 0.9 | 可以放心使用。引用`current_truth`作为验证后的结果。 |
| `confirmed` | 0.7-0.9 | 很可能是正确的，但需向用户说明存在不确定性。 |
| `stale` | 任何情况 | 该声明曾经正确，但数据已发生变化。使用`current_truth`代替，并告知用户：“之前的信息是正确的，但当前值为X。” |
| `disputed` | 任何情况 | 来源之间存在分歧。应同时呈现不同观点，不要选择其中一方。例如：“不同来源的说法不一致——[来源A]认为X，[来源B]认为Y。” |
| `false` | > 0.8 | 与当前数据不符。纠正错误：“实际上，当前值为X。” |
| `false` | < 0.8 | 很可能是错误的，但无法完全确定。标记为：“这与当前数据（X）不符，但置信度中等。” |
| `unknown` | 任何情况 | 无法验证。请如实告知用户，不要随意猜测。 |

### 第5步：根据结果采取行动
- **在计算中**：始终用`current_truth`替换原始声明值；
- **在报告中**：引用已验证的数值，并标注更新时间（例如：“截至[更新时间]”）；
- **在对话中**：自然地纠正过时的数据，避免过于生硬；
- **如果结果为`unknown`**：继续使用原始数值，但需说明该数值未经验证。

## 回复格式
```json
{
  "verdict": "confirmed",
  "confidence": 0.95,
  "current_truth": "0.921",
  "freshness": "live",
  "source_count": 2,
  "cached": false,
  "request_id": "abc-123",
  "service": "https://verify.agentutil.net"
}
```

## 分类
为了加快处理速度，请指定验证类别：
- `financial`：汇率、加密货币价格、股票价格；
- `entity`：公司信息、人口数量、成立日期；
- `geo`：时区、地理数据；
- `factcheck`：通过Google Fact Check API进行的一般性事实核查。

## 热门验证请求
查看其他用户正在验证的内容：
```bash
curl https://verify.agentutil.net/v1/trending
```

## 费用
- **免费 tier**：每天25次查询，无需身份验证；
- **付费 tier**：通过x402协议无限次查询（使用Base币种，每条查询费用为0.004美元）。

## 服务相关信息
- MCP服务器：`@agentutil/verify-mcp`（npm包）；
- 代理信息：`https://verify.agentutil.net/.well-known/agent.json`；
- 服务元数据：`https://verify.agentutil.net/.well-known/agent-service.json`。

## 隐私政策
免费 tier无需身份验证。查询内容仅存储在临时缓存中（最长1小时），不收集任何个人数据。速率限制仅基于IP地址进行。