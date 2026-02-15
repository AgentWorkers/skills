---
name: vibetrading-global-signals
description: 从 vibetrading-datahub 查询由 AI 生成的交易信号。这些信号是由自主代理根据鲸鱼投资者（大型交易者）的活动、新闻、资金利率以及技术指标进行分析后生成的。
metadata:
  {
    "openclaw":
      {
        "emoji": "📡",
        "requires": { "bins": ["curl", "jq"] }
      }
  }
---

# VibeTrading 全球交易信号

从 vibetrading-datahub 查询由 AI 生成的交易信号。这些信号由自主代理根据鲸鱼投资者（whale investors）的活动、新闻、资金费率以及技术指标进行分析后生成。

## 设置

无需身份验证！该 API 现已开放，无需 API 令牌即可使用。

只需直接运行相应的脚本即可：

## API 端点

### 1. 获取最新信号（多符号）
获取多个符号的最新信号，并按符号进行分组。

**示例用法**：
```bash
# Get latest signals for BTC and ETH, all types
curl 'https://vibetrading.dev/api/v1/signals/latest?symbols=BTC,ETH'

# Get only whale and news signals from last 24h
curl 'https://vibetrading.dev/api/v1/signals/latest?symbols=BTC,ETH,SOL&signal_types=WHALE_ACTIVITY,NEWS_ANALYSIS&hours=24'
```

### 2. 按符号获取信号
获取单个符号的交易信号。

**示例用法**：
```bash
curl 'https://vibetrading.dev/api/v1/signals/BTC?signal_types=TECHNICAL_INDICATOR&limit=5&hours=48'
```

### 3. 按符号和类型获取信号
获取特定符号及其信号类型的交易信号。

**示例用法**：
```bash
curl 'https://vibetrading.dev/api/v1/signals/ETH/FUNDING_RATE?limit=3'
```

## 信号类型

| 信号类型 | 描述 |
|-------------|-------------|
| `WHALE_ACTIVITY` | 鲸鱼投资者钱包活动分析 |
| `NEWS_ANALYSIS` | 加密货币新闻情绪分析 |
| `FUNDING_RATE` | 永续合约资金费率信号 |
| `TECHNICAL_INDICATOR` | 多时间框架的技术分析 |

## 工作流程

### 1. 查询信号
使用提供的脚本查询信号：
- `scripts/get_latest_signals.js` - 获取多个符号的最新信号
- `scripts/get_signals_by_symbol.js` - 获取单个符号的交易信号
- `scripts/get_signals_by_type.js` - 按符号和类型获取信号

### 3. 分析结果
查看信号内容，包括：
- **情绪**：看涨、看跌或中性
- **分析**：详细的 Markdown 分析报告
- **时间戳**：分析执行的日期和时间

### 4. 安排监控
设置定时任务以定期监控信号：
```bash
# Example: Check BTC/ETH signals every hour
0 * * * * /path/to/scripts/get_latest_signals.js BTC,ETH
```

## 脚本
- `scripts/get_latest_signals.js` - 获取多个符号的最新信号
- `scripts/get_signals_by_symbol.js` - 获取单个符号的交易信号
- `scripts/get_signals_by_type.js` - 按符号和类型获取信号

## 示例

### 快速信号检查
```bash
# Check BTC signals
node scripts/get_signals_by_symbol.js BTC

# Check latest BTC and ETH signals
node scripts/get_latest_signals.js BTC,ETH

# Check ETH funding rate signals
node scripts/get_signals_by_type.js ETH FUNDING_RATE
```

### 高级过滤
```bash
# Get whale activity signals from last 48 hours
node scripts/get_latest_signals.js BTC,ETH,SOL WHALE_ACTIVITY 48

# Get multiple signal types
node scripts/get_latest_signals.js BTC "WHALE_ACTIVITY,NEWS_ANALYSIS" 24
```

## 响应格式

所有 API 响应包含：
- `symbols`：查询的符号数组
- `signals`：按符号分组的信号对象
- `metadata`：查询元数据（时间窗口、信号类型等）

每个信号包含以下信息：
- `id`：唯一的信号 ID
- `symbol`：交易符号
- `signal_type`：信号类型
- `author`：生成信号的代理
- `signal_payload`：包含情绪分析和 Markdown 详细内容的信号数据
- `created_at`：信号创建的时间戳

## 与交易策略集成

可以使用这些信号来：
1. **利用 AI 生成的分析来确认交易想法**
2. **从多个维度监控市场情绪**
3. **为特定信号类型设置警报**
4. **结合其他数据进行全面分析**

## 故障排除

**常见问题**：
1. **404 Not Found**：查询参数对应的信号不存在
2. **速率限制**：API 可能存在速率限制，请调整查询频率
3. **网络问题**：检查网络连接

**调试命令**：
```bash
# Test API connectivity
curl 'https://vibetrading.dev/api/v1/signals/latest?symbols=BTC' -v

# Simple ping test
curl -I 'https://vibetrading.dev/api/v1/signals/latest?symbols=BTC'
```

## 注意事项
- 为提高性能，API 响应会被缓存
- 信号的时间戳采用 UTC 格式
- 始终使用其他数据源验证信号信息
- 在任何交易决策中都要采取适当的风险管理措施