---
name: kalshi
description: 只读的 Kalshi 预测市场集成功能：可用于查看市场行情、检查投资组合持仓、分析预测机会以及寻找高收益/高确定性的交易机会。该功能会在 Kalshi、预测市场、事件合约或交易建议触发时自动启动。
---

# Kalshi 预测市场

提供与 Kalshi 预测市场 API 的只读集成功能。

## 功能

- **浏览市场**：按类别列出活跃的事件和市场
- **市场分析**：获取价格、成交量和订单簿深度信息
- **投资组合视图**：查看持仓和盈亏情况（需要 API 密钥）
- **交易建议**：寻找高确定性、高回报的投资机会

## 设置

安装依赖项：
```bash
pip install requests cryptography
```

（如需访问投资组合信息（需要 RSA 密钥）：

1. 访问 [kalshi.com/account/profile](https://kalshi.com/account/profile)
2. 创建新的 API 密钥 → 保存 **密钥 ID** 并下载 **私钥**
3. 存储凭据：
```bash
mkdir -p ~/.kalshi
mv ~/Downloads/your-key-file.txt ~/.kalshi/private_key.pem
chmod 600 ~/.kalshi/private_key.pem
```

4. 创建 `~/.kalshi/credentials.json` 文件：
```json
{
  "api_key_id": "your-key-id-here",
  "private_key_path": "~/.kalshi/private_key.pem"
}
```

或运行交互式设置程序：
```bash
python scripts/kalshi_portfolio.py setup
```

## 脚本

### 市场数据（无需认证）

```bash
# List trending markets
python scripts/kalshi_markets.py trending

# Search markets by query
python scripts/kalshi_markets.py search "bitcoin"

# Get specific market details
python scripts/kalshi_markets.py market TICKER

# Find high-value opportunities
python scripts/kalshi_markets.py opportunities
```

### 投资组合（需要认证）

```bash
# View positions
python scripts/kalshi_portfolio.py positions

# View balance
python scripts/kalshi_portfolio.py balance

# Trade history
python scripts/kalshi_portfolio.py history
```

## 机会分析

`opportunities` 命令可用于识别以下特征的市场：
- **高确定性**：价格 ≥85¢ 或 ≤15¢（表示置信度超过 85%）
- **具有较高回报潜力**：潜在回报率 ≥10%
- **流动性充足**：订单簿深度足以支持合理的持仓规模

计算公式：`预期价值 = 概率 * 回报率 - (1 - 概率) * 成本`

一个好的投资机会应满足：`预期价值 / 成本 > 0.1`（即预期回报率超过 10%）

## 分类

Kalshi 的市场涵盖以下领域：
- 政治与选举
- 经济（美联储利率、通货膨胀、GDP）
- 天气与气候
- 金融（股票价格、加密货币）
- 娱乐与体育
- 科学与技术

## API 参考

详细端点信息请参阅 `references/api.md`。

## 重要说明

- 该功能仅支持读取数据，不支持交易执行
- 公共端点无需认证
- 访问投资组合/余额信息需要 API 凭据
- 市场交易以美分为单位（100¢ = $1）
- 所有时间均以 UTC 为准