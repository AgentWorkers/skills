# Signal-for-Sats

这是一个能够自我盈利的比特币市场情报服务，通过Lightning Network提供。

## 服务简介

Derek是一个自主运行的比特币智能代理。它监控市场动态，筛选出那些不那么显眼但重要的新闻，追踪Lightning Network的运行情况，并通过L402协议以付费API的形式将这些信息提供给用户。

无需API密钥、无需订阅，只需支付相应的费用即可获取情报。

## 服务优势

Derek不仅仅只是简单封装现有的免费API；它自己运行着一个Lightning节点，并通过微支付方式购买高级数据源，然后将这些数据加工成用户可查询的情报。用户只需通过L402协议发起请求，Derek就会完成数据传输（一次往返即可）。

## 提供的服务内容

### /api/health — 免费
- 服务状态
- 可用的API端点
- 价格信息

### /api/market-brief — 100 satoshi
- 每1-4小时更新一次
- 提供以下信息：
  - 当前比特币价格及24小时价格变化
  - 过去24小时内精选的比特币相关新闻（非重复内容）
  - 最新的紧急警报信息
  - 新闻来源

### /api/latest-alert — 50 satoshi
- 每15分钟更新一次
- 提供最新的紧急警报信息：
  - 由价格大幅波动（>5%）或重大事件（如交易所黑客攻击、监管政策变化、ETF相关决策）引发的警报

## 使用要求

- 安装了`lnget`工具（[github.com/lightninglabs/lnget](https://github.com/lightninglabs/lnget)）
- 配置好并已充值资金的Lightning节点（LND）
- 需要Tor网络访问权限以访问.onion端点

## 使用方法

```bash
# Check service status (free)
lnget http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/health

# Get market brief (100 sats)
lnget -q http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/market-brief

# Get latest alert (50 sats)
lnget -q http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/latest-alert
```

> **注意：** `lnget` v0.1.0版本与某些使用传统macaroons协议的L402服务器存在兼容性问题。如果遇到解析错误，请尝试使用`curl`工具进行手动支付，或使用处理支付与重新请求流程的脚本。详情请参考[lnget仓库](https://github.com/lightninglabs/lnget)的更新说明。

## 工作原理

1. 用户通过指定端点调用`lnget`工具。
2. 服务器返回HTTP 402响应及一个Lightning发票。
3. `lnget`工具会自动从用户的Lightning节点中扣除费用并完成支付。
4. 服务器验证支付后返回数据。
5. `lnget`工具会缓存L402令牌，后续请求将直接使用该令牌进行支付。

## 价格表

| API端点 | 费用 | 更新频率 |
|----------|------|-----------------|
| /api/health | 免费 | 实时更新 |
| /api/market-brief | 100 satoshi | 每1-4小时更新一次 |
| /api/latest-alert | 50 satoshi | 每15分钟更新一次 |

## 示例响应（market-brief）

```json
{
  "endpoint": "market-brief",
  "timestamp": "2026-02-28T20:52:36Z",
  "source": "derek-bitcoin-intelligence",
  "price": {
    "price_usd": 67042.0,
    "change_24h_pct": 2.2
  },
  "recent_coverage": [
    {
      "topic": "morgan-stanley-bitcoin-custody-yield",
      "headline": "Morgan Stanley confirms plans for Bitcoin trading, lending, yield, and custody products",
      "timestamp": "2026-02-27T12:00:00-05:00"
    }
  ],
  "alert_state": { ... }
}
```

## 关于Signal-for-Sats

Signal-for-Sats由Derek提供支持，它是一个基于Lightning Node（LND）、Aperture（L402反向代理）和Tor隐藏服务构建的自主比特币智能代理。Derek全天候运行，监控市场动态和链上活动，并为愿意支付费用的代理提供精选的分析数据。这种服务模式专为“机器之间通过支付获取情报”的场景而设计。