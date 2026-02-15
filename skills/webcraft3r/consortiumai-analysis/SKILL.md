---
name: consortium-ai-analysis
displayName: Consortium AI Analysis
description: 从 Consortium AI 获取最新的 AI 生成的加密货币交易分析结果（买入/卖出/等待），适用于现货交易对。
requirements: TRADING_ANALYSIS_API_KEY.
author: Consortium AI
authorUrl: https://consortiumai.org/
keywords: ["crypto", "trading", "analysis", "BUY", "SELL", "API", "spot", "signals"]
category: trading
---

## 使用说明

该技能提供了对 Consortium AI 生成的交易分析结果的 **按需、只读** 访问权限。它通过调用外部 API 来获取最新的交易决策。该技能不存储数据、不安排任务，也不发送自动通知。

### 运行方式（实现步骤）

在技能目录中，您可以通过以下两种方式调用交易分析 API：
- 通过发送 HTTP 请求（请参阅 API 参考文档）
- 或者运行捆绑好的脚本：

- **获取任意交易对的最新分析结果：**
  `node scripts/trading-analysis.js`
  或 `npm run latest`
- **获取特定代币的最新分析结果：**
  `node scripts/trading-analysis.js <TOKEN>`
  或 `npm run token -- <TOKEN>`
  例如：`node scripts/trading-analysis.js SOL`

运行脚本之前，需要设置 `TRADING_ANALYSIS_API_KEY` 环境变量。如果请求成功，脚本会将 API 响应以 JSON 格式输出到标准输出（stdout）；如果请求失败，则会将错误信息以 JSON 格式输出到标准错误输出（stderr），并退出（返回非零状态码）。

---

## 设置

在使用该技能之前，请将 API 密钥设置为环境变量：

```bash
export TRADING_ANALYSIS_API_KEY=your-secret-api-key
```

如需获取 API 密钥，请联系 [Consortium AI]（X 平台）：[https://x.com/Consortium.AI]。

---

## API 参考文档

**后端 API 基本地址：** `https://api.consortiumai.org`

**端点：** `GET https://api.consortiumai.org/api/trading-analysis`
该端点返回最新的交易分析结果（不包括借贷相关数据）。支持通过基础代币进行筛选。

### 认证

仅需要 API 密钥（不支持 JWT）。密钥的传递方式如下：
- **在请求头中添加：** `x-api-key: <TRADING_ANALYSIS_API_KEY>`
- **在请求头中添加：** `Authorization: Bearer <TRADING_ANALYSIS_API_KEY>`

如果密钥缺失或无效，服务器将返回 **401** 状态码，并在响应体中显示：`{"success": false, "message": "API 密钥无效或缺失"}`。

### 查询参数

| 参数          | 类型       | 是否必填 | 说明                                      |
|---------------|-----------|---------|-----------------------------------------|
| `token`        | string     | 否        | 基础代币符号。设置该参数后，将返回以该代币开头的交易对的最新分析结果（例如：SOL → SOL_USDT, SOL_USD）。示例：SOL, ETH, JUP, BTC。 |
| （未设置 `token` 时） | 获取所有交易对的最新分析结果。 |
| （设置 `token` 时） | 获取指定基础代币的最新分析结果。代币名称会进行规范化处理（去除空白字符并转换为大写）。 |

### 成功响应（状态码 200）

响应体包含交易相关的详细信息。示例：

```json
{
  "data": {
    "id": "...",
    "createdAt": "2026-02-09T14:00:00.000Z",
    "trading": {
      "action": "BUY",
      "pair": "SOL_USDT",
      "shouldExecute": true,
      "confidence": "HIGH",
      "setupScore": 78,
      "reasoning": {
        "marketCondition": "...",
        "technicalAnalysis": "...",
        "riskAssessment": "...",
        "pairSelection": "...",
        "comparativeAnalysis": { ... },
        "sentimentAndNews": { ... }
      },
      "tradeSummary": "Dual-model: BUY SOL_USDT (score: 78) – ...",
      "currentPositionsAnalysis": []
    }
  }
}
```

- `data.trading.action` – 买入（BUY）、卖出（SELL）或等待（WAIT）操作。
- `data.trading.pair` – 例如：SOL_USDT。
- `data.trading.confidence`、`data.trading.setupScore`、`data.trading.reasoning`、`data.trading.tradeSummary` – 可用于向用户展示分析结果。

### 错误响应

| 状态码 | 发生情况 | 响应体（示例）                          |
|---------|-----------|-----------------------------------------|
| **401** | API 密钥缺失或错误   | `{ "success": false, "message": "API 密钥无效或缺失" }`         |
| **404** | 数据库中无相关分析结果 | `{ "data": { "success": false, "message": "未找到交易分析结果" }`         |
| **500** | 服务器/数据库错误   | `{ "data": { "success": false, "message": "无法获取最新交易分析结果", "error": "..." }` |

### 示例请求

```http
GET https://api.consortiumai.org/api/trading-analysis
x-api-key: <TRADING_ANALYSIS_API_KEY>
```

```http
GET https://api.consortiumai.org/api/trading-analysis?token=SOL
x-api-key: <TRADING_ANALYSIS_API_KEY>
```

```bash
# Latest overall
curl -H "x-api-key: $TRADING_ANALYSIS_API_KEY" "https://api.consortiumai.org/api/trading-analysis"

# Latest for SOL
curl -H "x-api-key: $TRADING_ANALYSIS_API_KEY" "https://api.consortiumai.org/api/trading-analysis?token=SOL"
```

---

## 行为总结

| 情况                        | 结果                                      |
|---------------------------|-----------------------------------------|
| API 密钥有效，未设置 `token`，数据库中至少有一条交易记录 | **200** – 返回任意交易对的最新分析结果。            |
| API 密钥有效，`token` 为 SOL，数据库中存在以 SOL_ 开头的交易记录 | **200** – 返回 SOL 的最新交易分析结果。            |
| API 密钥有效，`token` 为 XYZ，但数据库中不存在以 XYZ_ 开头的交易记录 | **404** – “未找到代币 XYZ 的交易分析结果”。            |
| API 密钥无效                   | **401** – “API 密钥无效或缺失”。                        |

响应结果中最多包含一条交易记录（按创建时间排序的最新记录），且仅包含交易相关数据，不包含借贷相关信息。

---

## 可用功能

### `getLatestTradingAnalysis()`

**功能**：  
获取最新的交易分析结果（不区分交易对）。

**预期行为：**
- 向 `https://api.consortiumai.org/api/trading-analysis` 发送 GET 请求。
- 使用 `x-api-key: <TRADING_ANALYSIS_API_KEY>` 或 `Authorization: Bearer <TRADING_ANALYSIS_API_KEY>` 进行认证。
- 返回最新的交易决策（按创建时间排序）。

**使用场景：**
- 用户请求最新的市场分析信息时。
- 未指定具体的交易代币时。

**返回内容：**
- 交易对（例如：BTC_USDT）
- 交易操作（买入、卖出或等待）
- 信心水平
- 交易总结
- 详细的分析理由（包括技术分析、市场趋势、风险评估及市场情绪）

---

### `getTradingAnalysisByToken(token)`

**功能**：  
获取特定基础代币的最新交易分析结果。

**参数：**
- `token`（字符串）：基础代币符号（例如：BTC、ETH、SOL、JUP）

**预期行为：**
- 对代币名称进行规范化处理（去除空白字符并转换为大写）。
- 向 `https://api.consortiumai.org/api/trading-analysis?token=<TOKEN>` 发送 GET 请求。
- 使用 `x-api-key` 或 `Authorization: Bearer <TRADING_ANALYSIS_API_KEY>` 进行认证。
- API 会匹配所有以该代币为基础的交易对，并返回最新的交易决策。

**使用场景：**
- 用户询问特定代币的交易情况时。
- 用户需要获取特定代币的交易建议时。

**返回内容：**
- 该代币的交易对
- 交易操作（买入、卖出或等待）
- 信心水平
- 交易总结
- 详细的分析理由