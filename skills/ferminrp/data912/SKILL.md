---
name: data912-market-data
description: >
  **Query Data912市场数据端点**  
  用于查询阿根廷和美国金融工具的相关市场数据。适用于以下场景：  
  - 用户请求MEP/CCL报价；  
  - 需要查看阿根廷市场的实时行情（股票、期权、债券、公司债务等）；  
  - 需要获取美国的行情数据（美国存托凭证（ADRs）、股票等）；  
  - 需要按股票代码获取美国的OHLC（开高收低）历史数据；  
  - 需要查询美国的期权链信息；  
  - 需要了解波动率或风险指标。  
  **使用场景示例：**  
  - 当用户提到“Data912”、“MEP”、“CCL”、“期权链”、“历史数据”、“OHLC”、“隐含波动率”、“历史波动率”或“波动率百分位数”时，可使用该功能；  
  - 该功能可提供基于API的市场数据快照。
---
# Data912 市场数据

通过 Data912 的公开市场 API，可以查询阿根廷和美国的市场数据快照、历史价格走势以及交易结束（EOD）后的衍生品分析信息。

## API 概述

- **基础 URL**: `https://data912.com`
- **认证**: 无需认证（公开 API）
- **数据格式**: JSON 格式
- **数据说明**: Data912 将此 API 定义为用于教育或娱乐目的的数据，明确表示数据并非实时数据。
- **缓存说明**: 服务器元数据显示数据大约会通过 Cloudflare 进行 2 小时的缓存。

## 端点分组

### 1. 实时市场面板

- `/live/mep`（美元 MEP）
- `/live/ccl`（美元 CCL）
- `/live/arg_stocks`（阿根廷股票）
- `/live/arg_options`（阿根廷期权）
- `/live/arg_cedears`（阿根廷期货）
- `/live/arg_notes`（阿根廷公司信息）
- `/live/arg_corp`（阿根廷企业）
- `/live/arg_bonds`（阿根廷债券）
- `/live/usa_adrs`（美国地址）
- `/live/usa_stocks`（美国股票）

示例：

```bash
curl -s "https://data912.com/live/arg_stocks" | jq '.[0:5]'
```

### 2. 历史价格走势（OHLC）

- `/historical/stocks/{ticker}`（股票历史价格）
- `/historical/cedears/{ticker}`（期货历史价格）
- `/historical/bonds/{ticker}`（债券历史价格）

示例：

```bash
curl -s "https://data912.com/historical/stocks/GGAL" | jq '.[0:10]'
```

### 3. 交易结束后的衍生品分析

- `/eod/volatilities/{ticker}`（期权波动率）
- `/eod/option_chain/{ticker}`（期权链数据）

示例：

```bash
curl -s "https://data912.com/eod/volatilities/AAPL" | jq '.'
curl -s "https://data912.com/eod/option_chain/AAPL" | jq '.[0:10]'
```

### 本技能不支持的功能

- 请勿使用 `/contact` 端点。本技能仅专注于市场数据的检索与解析。

## 关键字段

### 面板字段（`/live/*`）

- `symbol`: 金融工具的代码/符号
- `px_bid`, `q_bid`: 卖价和买卖量
- `px_ask`, `q_ask`: 买价和买卖量
- `c`: 类似收盘价的交易价格
- `pct_change`: 百分比变化
- `v`: 成交量
- `q_op`: 交易操作次数（如有提供）

### 历史数据字段（`/historical/*/{ticker}`）

- `date`: 日期字符串
- `o`, `h`, `l`, `c`: 开盘价、最高价、最低价、收盘价
- `v`: 成交量
- `dr`: 日收益率
- `sa`: 来源提供的其他数值指标

### 波动率指标（`/eod/volatilities/{ticker}`）

- 波动率期限结构：`iv_s_term`, `iv_m_term`, `iv_l_term`
- 波动率百分位数：`iv_*_percentile`
- 高波动率期限结构：`hv_s_term`, `hv_m_term`, `hv_l_term`
- 高波动率百分位数：`hv_*_percentile`
- 相对价值比率：`iv_hv_*_ratio`, `iv_fair_iv_ratio`
- 公平价值参考：`fair_iv`, `fair_iv_percentile`

### 期权链字段（`/eod/option_chain/{ticker}`）

- 合同信息：`opex`, `s_symbol`, `type`, `k`
- 市场数据：`bid`, `ask`, `c`, `oi`
- 期权希腊字母：`delta`, `gamma`, `theta`, `vega`, `rho`
- 估值/概率：`fair_value`, `fair_iv`, `itm_prob`, `intrinsic`, `otm`
- 期限信息：`r_days`, `r_tdays`, `hv_2m`, `hv_1yr`

## 工作流程

1. **确定需求**并选择对应的端点组：
   - 实时市场数据快照 -> `/live/*`
   - 时间序列数据 -> `/historical/*/{ticker}`
   - 期权/风险分析 -> `/eod/*/{ticker}`
2. **验证输入内容**：
   - 对于历史数据/交易结束后的数据，需要提供股票代码。
   - 如果代码缺失，请在查询前要求用户提供。
3. **使用 `curl -s` 获取数据**，然后使用 `jq` 进行解析。
4. **处理空数组**：
   - 如果响应结果为空数组，返回提示：“当前该端点/代码暂无数据。”
5. **提供可操作的总结**：
   - 首先提供简短的快照信息。
   - 然后包含用户请求的相关详细数据。
6. **明确数据用途**：
   - 提醒用户这些数据仅用于教育或参考目的，非实时数据。
   - 避免将结果作为交易建议使用。

## 错误处理

- **429 请求过多**：
  - 大多数市场端点的请求频率限制为每分钟 120 次。
  - 稍作延迟后重新尝试；避免连续多次请求。
- **422 验证错误**：
  - 通常是由于路径输入无效或缺失（例如代码格式错误）。
  - 重新检查代码和端点后再尝试。
- **网络/超时错误**：
  - 重试几次（例如，延迟后重试 2 次）。
  - 如果仍然失败，返回明确的错误信息及尝试的端点。

## 结果展示

向用户展示结果时：

- 首先提供简洁的快照信息（哪些指标发生了变化、变化的方向和幅度）。
- 对于面板数据，比较买卖价、收盘价及百分比变化。
- 对于历史数据，总结价格趋势和显著波动。
- 对于波动率/期权数据，突出显示百分位数和波动率与高波动率之间的关系。
- 明确指出数据为教育/参考用途，不提供财务建议。

## OpenAPI 规范

完整的 API 架构和端点定义请参见 [references/openapi-spec.json](references/openapi-spec.json)。