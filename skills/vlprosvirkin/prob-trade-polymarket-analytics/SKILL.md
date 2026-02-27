---
name: probtrade
version: 2.0.4
description: "Polymarket 预测市场：提供数据分析、交易功能、热门市场信息、价格走势、顶尖交易者信息以及市场搜索服务。由 prob.trade 技术支持。"
homepage: https://app.prob.trade
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["python3"],"env":["PROBTRADE_API_KEY","PROBTRADE_API_SECRET"],"config":["~/.openclaw/skills/probtrade/config.yaml"]},"emoji":"📊","install":[{"id":"python3","kind":"brew","formula":"python@3","bins":["python3"],"label":"Install Python 3","os":["darwin","linux"]}]}}
---
# prob.trade — Polymarket 分析与交易

您可以通过 [prob.trade](https://app.prob.trade) 获取实时的预测市场情报，并在 Polymarket 上进行交易。您可以浏览热门市场、查看价格走势、了解顶级交易者的交易情况，以及下达交易订单。

## 设置（所有命令均需执行）

所有命令均需要一个 prob.trade API 密钥。请在 `~/.openclaw/skills/probtrade/config.yaml` 文件中配置该密钥：
```yaml
api_key: "ptk_live_..."
api_secret: "pts_..."
```
您可以在 [https://app.prob.trade](https://app.prob.trade) 的“设置” → “API 密钥” 中生成密钥。需要注册免费账户。

## 分析命令

使用以下脚本查询 prob.trade 的公共 API：

### 市场概览
快速了解预测市场的整体情况：
```bash
python3 {baseDir}/scripts/probtrade.py overview
```
返回内容：市场统计数据、热门市场前十名、价格变动情况以及最新推出的市场。

### 热门市场
查看当前交易最活跃的市场：
```bash
python3 {baseDir}/scripts/probtrade.py hot [--limit N]
```

### 价格变动较大的市场
查看过去 24 小时内价格变动最大的市场：
```bash
python3 {baseDir}/scripts/probtrade.py breaking [--limit N]
```

### 新市场
最近创建的预测市场：
```bash
python3 {baseDir}/scripts/probtrade.py new [--limit N] [--days N]
```

### 搜索市场
根据特定主题查找相关市场：
```bash
python3 {baseDir}/scripts/probtrade.py search "Trump" [--limit N]
```

### 市场详情
通过市场条件 ID 获取特定市场的详细信息：
```bash
python3 {baseDir}/scripts/probtrade.py market <condition_id>
```

### 市场统计
市场分类统计及总体市场数量：
```bash
python3 {baseDir}/scripts/probtrade.py stats
```

### 顶级交易者
查看盈利最多的预测市场交易者：
```bash
python3 {baseDir}/scripts/probtrade.py traders [--limit N] [--sort pnl|roi|volume|winRate] [--period all|30d|7d|24h]
```

## 交易命令

使用上述配置的 API 密钥在 Polymarket 上进行交易：

### 下单
```bash
python3 {baseDir}/scripts/probtrade.py order --market <condition_id> --side BUY --outcome Yes --type LIMIT --price 0.55 --amount 10
```

### 取消订单
```bash
python3 {baseDir}/scripts/probtrade.py cancel --order-id <orderId>
```

### 查看持仓
```bash
python3 {baseDir}/scripts/probtrade.py positions
```

### 查看余额
```bash
python3 {baseDir}/scripts/probtrade.py balance
```

### 查看未成交订单
```bash
python3 {baseDir}/scripts/probtrade.py orders
```

**安全提示**：API 密钥不会离开您的设备，仅会发送 HMAC 签名。系统中没有用于提款/转账的接口。

## 输出格式

所有命令的输出均为结构化的 JSON 格式，便于 AI 系统解析。主要字段包括：

- **condition_id**：唯一的市场标识符（用于在 Polymarket 上进行交易）
- **question**：预测市场的相关问题
- **tokens**：“是/否”选项的当前价格
- **volume_24hr**：过去 24 小时的交易量
- **liquidity**：可用的交易流动性
- **end_date_iso**：市场结果揭晓的时间

## 链接

- 仪表盘：https://app.prob.trade
- 市场页面：`https://app.prob.trade/markets/{condition_id}`
- 交易者个人资料：`https://app.prob.trade/traders/{address}`
- 公共 API：https://api(prob.trade)/api/public/overview
- 交易 API 文档：https://prob.trade/docs/public-api
- ClawHub：https://clawhub.ai/vlprosvirkin/prob-trade-polymarket-analytics