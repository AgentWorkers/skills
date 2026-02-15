---
name: kalshi-trader
description: 查询Kalshi预测市场的相关信息——包括联邦利率（Fed rates）、国内生产总值（GDP）、消费者价格指数（CPI）、经济数据，以及各类受监管的事件合约（regulated event contracts）。
homepage: https://kalshi.com
user-invocable: true
metadata: {"moltbot":{"emoji":"🏛️","requires":{}}}
---

# Kalshi Trader

查询 Kalshi——这个受美国商品期货交易委员会（CFTC）监管的预测市场，提供关于经济、政治和事件的预测合约服务。

## 关于 Kalshi

Kalshi 是美国首个获得 CFTC 批准的合法、受监管的预测市场。它提供以下类型的事件合约：
- 美联储利率决策
- 国内生产总值（GDP）和经济指标
- 通货膨胀（CPI）数据
- 政治事件
- 天气和自然灾害事件

## 命令

### 美联储市场
```bash
python3 {baseDir}/scripts/kalshi.py fed [limit]
```
获取美联储利率预测市场的数据（KXFED 系列）。

### 经济市场
```bash
python3 {baseDir}/scripts/kalshi.py economics [limit]
```
获取 GDP、CPI 及其他经济指标的相关市场数据。

### 热门市场
```bash
python3 {baseDir}/scripts/kalshi.py trending [limit]
```
获取交易量较大的热门市场数据。

### 搜索市场
```bash
python3 {baseDir}/scripts/kalshi.py search "<query>" [limit]
```
根据关键词搜索相关市场。

### 获取所有市场系列
```bash
python3 {baseDir}/scripts/kalshi.py series
```
列出所有可用的市场系列。

## 输出格式

查询结果包括：
- 市场名称/问题
- “YES”价格（表示预测概率）
- 交易量
- 市场代码
- 市场状态（开放/关闭）

## 主要市场系列

| 系列 | 描述 |
|--------|-------------|
| KXFED | 美联储利率决策 |
| KXGDP | 美国 GDP 预测 |
| KXCPI | 消费者价格指数（CPI）/通货膨胀 |
| KXBTC | 比特币价格区间 |

## 使用示例

**用户**：“美联储的利率预测是什么？”
**助手**：我将从 Kalshi 获取美联储利率预测市场的相关数据。

```bash
python3 {baseDir}/scripts/kalshi.py fed
```

**用户**：“搜索与通货膨胀相关的市场”
**助手**：我正在 Kalshi 中搜索与通货膨胀相关的市场数据。

```bash
python3 {baseDir}/scripts/kalshi.py search "inflation"
```

## API 信息

- **基础 URL**：`https://api.elections.kalshi.com/trade-api/v2`
- **认证**：读取操作无需认证
- **请求限制**：遵循标准的 API 请求限制
- **文档**：https://docs.kalshi.com

## 注意事项

- 该工具仅支持读取数据（交易操作需要 API 密钥）
- 价格以小数形式显示（0.75 表示 75% 的概率）
- 交易量表示合约的总数
- 市场最终结果为 $1.00（表示“YES”）或 $0.00（表示“NO”）
- 该市场受美国监管，仅限美国居民使用