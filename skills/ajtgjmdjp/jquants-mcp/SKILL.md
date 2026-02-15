---
name: jquants-mcp
description: "通过 J-Quants API 访问 JPX 股票市场数据——可以搜索股票、获取东京证券交易所上市公司的每日开盘价（Open）、最高价（High）、最低价（Low）、收盘价（Close）和成交量（Volume，OHLCV），以及财务摘要和收益日历。"
metadata: {"openclaw":{"emoji":"💹","requires":{"bins":["jquants-mcp"],"env":["JQUANTS_MAIL_ADDRESS","JQUANTS_PASSWORD"]},"install":[{"id":"uv","kind":"uv","package":"jquants-mcp","bins":["jquants-mcp"],"label":"Install jquants-mcp (uv)"}]}}
---

# J-Quants: JPX股票市场数据

通过官方的J-Quants API，您可以获取东京证券交易所（TSE）上市股票的数据。您可以搜索股票、获取每日的开盘价（OHLCV）、收盘价、最高价、最低价以及成交量，还可以查看财务摘要和盈利公告日程。

**重要提示：** 该工具仅供个人使用。根据J-Quants的服务条款，禁止任何形式的数据再分发。详情请参阅：https://jpx-jquants.com/termsofservice

## 使用场景

- 通过股票代码或公司名称搜索TSE上市的股票
- 获取任意股票的每日OHLCV价格数据
- 查看财务摘要（收入、利润、每股收益EPS、净资产收益率ROE）
- 查看即将发布的盈利公告日期
- 比较不同公司的财务指标

## 命令

### 搜索股票
```bash
# By stock code
jquants-mcp search 7203

# By company name (Japanese)
jquants-mcp search トヨタ

# JSON output
jquants-mcp search ソニー --json-output
```

### 获取股票价格
```bash
# Default: last 30 days
jquants-mcp price 7203

# With date range
jquants-mcp price 7203 --start-date 2024-01-01 --end-date 2024-12-31

# JSON output
jquants-mcp price 7203 --json-output
```

### 获取财务数据
```bash
jquants-mcp financials 7203
jquants-mcp financials 6758 --json-output
```

### 获取盈利公告日程
```bash
# Default: next 30 days
jquants-mcp calendar

# With date range
jquants-mcp calendar --start-date 2024-04-01 --end-date 2024-06-30
```

### 测试连接
```bash
jquants-mcp test
```

## 工作流程

1. `jquants-mcp search <company>` → 查找股票代码
2. `jquants-mcp price <code>` → 获取价格历史记录
3. `jquants-mcp financials <code>` → 获取财务数据
4. `jquants-mcp calendar` → 查看盈利公告日期

## 设置要求

- 需要设置`JQUANTS_MAIL_ADDRESS`和`JQUANTS_PASSWORD`环境变量
- 可免费注册账户：https://jpx-jquants.com/
- 使用Python包进行安装：`pip install jquants-mcp` 或 `uv tool install jquants-mcp`

## 服务条款

使用本工具即表示您同意J-Quants的服务条款。数据仅限个人使用，禁止任何形式的数据再分发。