---
name: whalecli
description: 这是一个专为ETH和BTC区块链设计的、基于代理（agent）的“鲸鱼钱包追踪器”（whale wallet tracker）。该工具能够追踪大型加密货币钱包的动向，分析“鲸鱼用户”（whale users）的交易行为，检测资金积累/分配的模式，并实时发送警报。它还与FearHarvester和Simmer预测市场集成，形成一个完整的信号→投注（signal→bet）工作流程。适用场景包括：用户询问关于“鲸鱼用户”活动的相关信息、追踪链上的交易信号、分析大额钱包的移动情况、研究智能资金（smart money）的流动趋势，以及在利用链上数据进行加密货币交易或投注前的预验证过程。
---
# WhaleWatch CLI — 代理技能

用于追踪加密货币大鳄（“whales”）的交易活动，实现从链上数据信号到代理分析、再到预测市场投注的完整流程。

## 安装

```bash
uv pip install whalecli
```

## 快速入门

```bash
# Initialize config (creates ~/.config/whalecli/config.toml)
whalecli config init

# Set API key (free tier: 5 req/sec)
whalecli config set api.etherscan_api_key YOUR_KEY

# Add a whale wallet
whalecli wallet add 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --label "vitalik.eth" --chain ETH

# Scan all wallets (last 24h)
whalecli scan --format json

# Stream real-time alerts (JSONL, one event per line)
whalecli stream --chain ETH --interval 60
```

## 使用场景

**常用查询语句：**
- “大鳄们正在做什么？”
- “检查ETH/BTC上的大鳄活动”
- “大鳄是在积累资产还是分散资产？”
- “是否有大型钱包的交易活动？”
- “链上的数据信号是什么？”
- “运行一次大鳄交易分析”

**自动触发机制（无需用户输入）：**
- 在市场活跃时段（每60分钟）自动执行一次扫描（通过心跳机制）
- 在进行Simmer/Polymarket投注前，进行大鳄活动检测
- 当恐惧/贪婪指数超过预设阈值时，自动触发检测

## CLI命令

### `whalecli scan` — 一次性大鳄交易分析

```bash
whalecli scan --chain ETH --hours 4 --threshold 70 --format json
```

**输出格式（JSON）：**
```json
{
  "scan_id": "scan_20260222_103015_a1b2",
  "chain": "ETH",
  "window_hours": 4,
  "wallets": [
    {
      "address": "0xd8dA...",
      "label": "vitalik.eth",
      "score": 82,
      "direction": "accumulating",
      "score_breakdown": {
        "net_flow": 35,
        "velocity": 20,
        "correlation": 15,
        "exchange_flow": 12
      },
      "net_flow_usd": 15000000,
      "tx_count": 12
    }
  ],
  "summary": {
    "total_wallets": 5,
    "accumulating": 3,
    "distributing": 1,
    "neutral": 1,
    "avg_score": 65
  },
  "alerts_triggered": 2
}
```

### `whalecli stream` — 实时JSONL数据流

```bash
whalecli stream --chain ETH --interval 60 --threshold 70
```

事件记录（每条记录为一个JSON对象）：
- `stream_start`：数据流开始
- `whale_alert`：检测到大鳄交易信号
- `whale_activity`：检测到大鳄活动（低于预设阈值）
- `heartbeat`：定期系统检查
- `stream_end`：数据流结束

### `whalecli wallet` — 管理被监控的钱包

```bash
whalecli wallet add 0x... --label "whale1" --chain ETH
whalecli wallet list --format json
whalecli wallet remove 0x...
whalecli wallet import wallets.csv
```

### `whalecli alert` — 配置警报规则

```bash
whalecli alert set --score 75 --webhook https://example.com/hook
whalecli alert set --threshold 1000000 --window 1h
whalecli alert list --format json
```

### `whalecli report` — 历史数据分析

```bash
whalecli report --wallet 0x... --days 30 --format json
```

### `whalecli config` — 配置管理

```bash
whalecli config init
whalecli config set api.etherscan_api_key YOUR_KEY
whalecli config show
```

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 成功（检测到警报或扫描完成） |
| 1 | 未检测到警报（扫描执行但未发现异常） |
| 2 | API错误（请求频率限制、密钥无效） |
| 3 | 网络错误（超时、连接失败） |
| 4 | 数据错误（地址无效、钱包未找到） |

## 评分算法

采用四维评分系统（0–100分）：

- **净流量（0–40分）**：基于USD净流量，采用log10缩放，并考虑钱包使用时间
- **活跃度（0–25分）**：当前交易活动与30天基线的对比（log2比率）
- **相关性（0–20分）**：其他钱包的交易方向一致性（至少需要2个参考钱包）
- **交易所流量（0–15分）**：通过CEX地址注册表验证交易方向

**评分解读：**
- 80–100分：强烈的大鳄交易信号（高置信度）
- 60–79分：中等活跃度（值得关注）
- 40–59分：低活跃度（可忽略）
- 0–39分：活动极少（可忽略）

## 代理集成方案

```python
import subprocess, json

def whale_scan(chain="ETH", hours=4, threshold=70):
    """Run whale scan and return parsed results."""
    result = subprocess.run(
        ["whalecli", "scan", "--chain", chain,
         "--hours", str(hours), "--threshold", str(threshold),
         "--format", "json"],
        capture_output=True, text=True, timeout=30
    )
    if result.returncode == 2:
        raise RuntimeError(f"API error: {result.stderr}")
    if not result.stdout.strip():
        return {"wallets": [], "alerts_triggered": 0}
    return json.loads(result.stdout)

# Example: pre-bet whale check
scan = whale_scan(chain="ETH", hours=4)
if scan["summary"]["accumulating"] > scan["summary"]["distributing"]:
    print("Whales accumulating — bullish signal")
```

## 与FearHarvester的集成

实现恐惧/贪婪指数与大鳄交易信号的联动，用于指导Simmer/Polymarket投注策略

```python
# 1. Get F&G value
fg_value = get_fear_greed_index()  # e.g., 8 (Extreme Fear)

# 2. Check whale confirmation
scan = whale_scan(chain="ETH", hours=4)
whales_accumulating = scan["summary"]["accumulating"] > scan["summary"]["distributing"]

# 3. If fear + whales accumulating → strong contrarian signal
if fg_value <= 20 and whales_accumulating:
    # Place bet on recovery market
    place_simmer_bet(market="btc_recovery", side="yes", amount=15)
```

## 支持的区块链平台

- **ETH**：Etherscan API（免费 tier：每秒5次请求）
- **BTC**：Mempool.space（主要数据源）+ Blockchain.info（备用数据源）
- **HL**：Hyperliquid平台的永久性交易记录与持仓信息

## 链接

- **PyPI仓库：** https://pypi.org/project/whalecli/
- **GitHub仓库：** https://github.com/clawinfra/whalecli
- **问题报告：** https://github.com/clawinfra/whalecli/issues