---
name: allstock-data
description: >
  **中国A股、港股及美股市场的股票数据查询功能**  
  该功能默认使用腾讯财经的HTTP API（轻量级接口，无需安装），同时支持通过adata SDK获取更全面的数据。支持实时行情、K线历史数据、订单簿分析等功能。
---
# 股票数据查询

系统支持两种数据源。**默认使用的是腾讯金融HTTP API：**

1. **腾讯金融HTTP API（默认）** — 无需安装，无需代理
2. **adata SDK（可选）** — 提供更全面的数据，但需要安装，并可能需要使用代理

---

## 1. 腾讯金融HTTP API（默认）

### 1.1 中国A股实时行情

**接口地址：**
```bash
http://qt.gtimg.cn/q=<股票代码>
```

**股票代码格式：**

| 市场 | 代码前缀 | 示例 |
|--------|-------------|---------|
| 上交所主板 | sh600xxx | sh600519（茅台） |
| 星创板 | sh688xxx | sh688111 |
| 深交所主板 | sz000xxx | sz000001（平安银行） |
| 创业板（GEM） | sz300xxx | sz300033 |
| ETF | sz159xxx | sz159919 |

**指数代码：**

| 指数 | 代码 |
|-------|------|
| 上证综合指数 | sh000001 |
| 深证成分指数 | sz399001 |
| 创业板指数 | sz399006 |
| 星创板50指数 | sz399987 |
| 中证300指数 | sh000300 |

**示例：**
```bash
# 单只股票
curl -s "http://qt.gtimg.cn/q=sh600519"

# 多只股票
curl -s "http://qt.gtimg.cn/q=sh600519,sh000001,sz399001"
```

**响应字段：**
```json
v_sh600519="1~贵州茅台~600519~1460.00~1466.21~1466.99~14146~6374~7772~..."
          ~  名称    ~  代码  ~  开盘价  ~  最高价  ~  最低价  ~  成交量
```

| 指数 | 字段 |
|-------|-------|
| 0 | 市场代码 |
| 1 | 股票名称 |
| 2 | 股票代码 |
| 3 | 当前价格 |
| 4 | 开盘价 |
| 5 | 最低价 |
| 6 | 最高价 |
| 30 | 价格变化 |
| 31 | 变动百分比 |
```

---

### 1.2 香港股票实时行情

**接口地址：**
```bash
http://qt.gtimg.cn/q=hk<股票代码>
```

**示例：**
```bash
# 腾讯控股
curl -s "http://qt.gtimg.cn/q=hk00700"

# 阿里巴巴
curl -s "http://qt.gtimg.cn/q=hk09988"
```

---

### 1.3 美国股票实时行情

**接口地址：**
```bash
http://qt.gtimg.cn/q=us<股票代码>
```

**示例：**
```bash
# 苹果
curl -s "http://qt.gtimg.cn/q=usAAPL"

# 特斯拉
curl -s "http://qt.gtimg.cn/q=usTSLA"

# 英伟达
curl -s "http://qt.gtimg.cn/q=usNVDA"
```

---

### 1.4 K线历史数据

**接口地址：**
```bash
https://web.ifzq.gtimg.cn/appstock/app/fqkline/get
```

**参数：**
| 参数 | 描述 |
|-----------|-------------|
| `_var` | 变量名称，例如 `kline_dayqfq` |
| `param` | 股票代码、K线类型、开始日期、结束日期、数据数量、调整类型 |

**K线类型：** `day` / `week` / `month`

**调整类型：** `qfqa`（向前调整）/ `qfq`（向后调整）/ `empty`（未调整）

**示例：**
```bash
# 茅台股票（过去10天的K线，向前调整）
curl -s "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_dayqfq&param=sh600519,day,,,10,qfqa"

# 平安银行股票（过去5周的K线）
curl -s "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_weekqfq&param=sz000001,week,,,5,qfqa"

# 创业板指数（过去3个月的K线）
curl -s "https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?_var=kline_monthqfq&param=sz399006,month,,,3,qfqa"
```

**响应格式：**
```json
{"day": ["2026-02-27", "1466.99", "1461.19", "1476.21", "1456.01", "13534"], ...]
                日期       开盘价      收盘价      最高价       最低价      成交量
```

---

### 1.5 订单簿分析

**接口地址：**
```bash
http://qt.gtimg.cn/q=s_pk<股票代码>
```

**示例：**
```bash
curl -s "http://qt.gtimg.cn/q=s_pksh600519"
```

**返回内容：** 内部交易与外部交易的买卖量比例

---

## 2. adata SDK（可选）

adata是一个开源的A股量化数据库，提供更全面的数据。需要安装，并可能需要使用代理。

### 安装

```bash
pip install adata
```

### 代理设置（如需使用代理）

```python
import adata
adata.proxy(is_proxy=True, ip='你的代理IP:端口')
```

### 功能列表

| 功能 | 描述 |
|---------|-------------|
| 股票基本信息 | 所有A股代码、股本、行业分类 |
| K线数据 | 日/周/月数据，可进行向前/向后调整 |
| 实时行情 | 批量实时报价 |
| 二级订单簿 | 卖买深度数据 |
| 资金流向 | 单只股票的资金流向分析 |
| 主题板块 | 主题板块数据 |
| 指数数据 | 主要指数行情 |
| ETF数据 | ETF报价 |

### 使用示例

```python
import adata

# 获取所有A股股票代码
df = adata.stock.info.all_code()

# 获取K线数据
df = adata.stock.market.get_market(
    stock_code='000001',
    k_type=1,           # 1=日线，2=周线，3=月线
    start_date='2024-01-01',
    adjust_type=1        # 0=未调整，1=向前调整，2=向后调整
)

# 实时行情
df = adata.stock.market.list_market_current(
    code_list=['000001', '600519']
```

---

## 3. 使用场景指南

| 场景 | 推荐数据源 |
|----------|--------------------|
| 快速查询单只股票价格 | 腾讯金融API |
| K线历史数据 | 腾讯金融API |
| 批量报价查询 | 腾讯金融API |
| 资金流向数据 | adata SDK |
| 完整财务报表 | adata SDK |
| 主题/板块分析 | adata SDK |
| 二级订单簿 | 腾讯金融API或adata SDK |

---

## 4. 重要说明

1. **编码格式**：腾讯金融API返回的文本为GBK编码，请进行解码处理。
2. **价格变化百分比**：使用API提供的字段（索引31）进行计算，切勿手动计算。
3. **数据延迟**：实时数据可能存在最多15分钟的延迟。
4. **请求频率**：避免频繁请求，尽可能使用批量查询。
5. **错误处理**：无效的股票代码会返回 `v_pv_none_match="1"`。