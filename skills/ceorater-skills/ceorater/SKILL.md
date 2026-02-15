---
name: ceorater
description: "获取标准普尔500指数公司的机构级CEO绩效分析数据。这些分析包括专有评分指标：CEORaterScore（综合评分）、AlphaScore（市场超额表现评分）、RevenueCAGRScore（收入增长率评分）和CompScore（薪酬效率评分）。基础数据涵盖总股票回报（TSR）与标准普尔500指数（SPY）的对比情况、年均回报率、CEO的总薪酬（来自代理文件的最新财年数据），以及经任期调整后的收入增长率（Revenue CAGR）。每条记录包含CEO姓名、公司名称、股票代码、所属行业、业务领域以及任职日期。目前覆盖517位CEO的数据，每日更新。这些信息对于投资研究、尽职调查以及高管薪酬分析非常有用。"
homepage: https://www.ceorater.com
disable-model-invocation: true
requires:
  env:
    - CEORATER_API_KEY
primaryEnv: CEORATER_API_KEY
triggers: ["CEO performance", "CEORater", "CEO score", "CEO rating", "executive performance", "CEO compensation", "AlphaScore", "CompScore", "TSR", "total stock return"]
metadata: {"openclaw":{"requires":{"env":["CEORATER_API_KEY"]},"primaryEnv":"CEORATER_API_KEY","homepage":"https://www.ceorater.com"},"pricing":{"model":"subscription","individual":"$99/month per user for research and analysis","enterprise":"Contact sales@ceorater.com for proprietary model integration, AI/ML training, or product development"},"provider":{"name":"CEORater","url":"https://www.ceorater.com","support":"support@ceorater.com","sales":"sales@ceorater.com"}}
---
# CEORater技能

通过CEORater API查询标准普尔500指数成分股及美国主要上市公司的CEO绩效数据。

## 先决条件

1. 在 [https://www.ceorater.com/api-docs.html](https://www.ceorater.com/api-docs.html) 获取API密钥（每位用户每月费用为99美元）。
2. 设置环境变量：`CEORATER_API_KEY=zpka_your_key_here`。

**许可说明：** 自助服务API访问仅允许个人进行研究和分析。如需将CEORater数据集成到公司自有模型中、用于人工智能/机器学习训练或产品开发，需签订企业协议——请联系 sales@ceorater.com。

## 可用指标

| 指标          | 范围        | 描述                                      |
|---------------|------------|-----------------------------------------|
| CEORaterScore    | 0-100       | CEO综合效能评分                        |
| AlphaScore     | 0-100       | 相对于市场基准的绩效表现                    |
| RevenueCAGRScore | 0-100       | 考虑任期因素后的收入增长率百分比                |
| CompScore      | A-F         | 薪酬效率等级                            |
| TSR During Tenure | %          | CEO任期内的总股票回报率                    |
| TSR vs. S&P 500   | %          | 相对于标准普尔500指数（SPY）的绩效表现            |
| CEO Compensation | $M          | 最新代理文件中记录的CEO总薪酬                |
| Revenue CAGR    | %          | 考虑任期因素后的复合年收入增长率                |

## API接口

### 按股票代码查询公司
```bash
curl -H "Authorization: Bearer $CEORATER_API_KEY" \
  "https://api.ceorater.com/v1/company/AAPL?format=raw"
```

### 搜索公司
```bash
curl -H "Authorization: Bearer $CEORATER_API_KEY" \
  "https://api.ceorater.com/v1/search?q=technology&format=raw"
```

### 列出所有公司
```bash
curl -H "Authorization: Bearer $CEORATER_API_KEY" \
  "https://api.ceorater.com/v1/companies?limit=100&format=raw"
```

## 使用说明

当用户需要查询CEO绩效、评级或高管薪酬时：

1. **单家公司查询：** 使用 `/v1/company/{ticker}` 接口。
2. **行业/领域分析：** 使用 `/v1/search?q={query}` 接口。
3. **批量数据查询：** 使用 `/v1/companies?limit=N` 接口。
   对于用于计算的数值型数据，始终使用 `format=raw` 格式。

### 示例查询

- “苹果公司的CEORaterScore是多少？” → GET /v1/company/AAPL
- “显示科技行业的CEO们” → GET /v1/search?q=technology
- “哪些CEO的评级最高？” → GET /v1/companies, sort by ceoraterScore
- “比较蒂姆·库克和萨蒂亚·纳德拉的绩效” → GET /v1/company/AAPL 和 /v1/company/MSFT

## 响应格式（原始数据）

```json
{
  "companyName": "Apple Inc.",
  "ticker": "AAPL",
  "sector": "Technology",
  "industry": "Computer Manufacturing",
  "ceo": "Tim Cook",
  "founderCEO": false,
  "ceoraterScore": 87,
  "alphaScore": 93.5,
  "revenueCagrScore": 75.2,
  "revenueCagr": 0.042,
  "compScore": "C",
  "tsrMultiple": 22.23,
  "tenureYears": 14.4,
  "avgAnnualTsrRatio": 1.55,
  "compPer1PctTsrMM": 0.482,
  "tsrVsSpyRatio": 15.64,
  "avgAnnualVsSpyRatio": 1.09,
  "compensationMM": 74.6
}
```

## 错误处理

| 代码          | 含义                                      |
|--------------|-----------------------------------------|
| 401          | API密钥缺失或无效                        |
| 404          | 未找到股票代码                            |
| 400          | 请求参数错误                            |

## 辅助脚本

为方便使用，请运行 `[baseDir]/scripts/ceorater.sh` 脚本：

```bash
# Get single company
{baseDir}/scripts/ceorater.sh get AAPL

# Search
{baseDir}/scripts/ceorater.sh search "healthcare"

# List top N
{baseDir}/scripts/ceorater.sh list 20
```

## 数据覆盖范围

- 截至2026年2月，涵盖517位CEO的数据，包括所有标准普尔500指数成分股。
- 数据每日在美国市场收盘后更新（通常为东部标准时间下午6:30）。
- 响应结果可缓存最多24小时。

## 更多信息

- 文档：[https://www.ceorater.com/api-docs.html](https://www.ceorater.com/api-docs.html)
- 代理信息：[https://www.ceorater.com/.well-known/agent.json](https://www.ceorater.com/.well-known/agent.json)
- 技术支持：support@ceorater.com
- 企业销售咨询：sales@ceorater.com