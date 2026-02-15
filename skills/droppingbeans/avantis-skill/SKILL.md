---
name: avantis
description: 在 Avantis（基础版）中执行杠杆交易。支持加密货币、外汇和商品的交易，杠杆倍数最高可达100倍。该系统采用 Python SDK，并实现了与钱包的直接集成。
metadata:
  author: beanbot
  version: "1.0.0"
  requires:
    - Python 3.12+
    - avantis-trader-sdk
    - Wallet: 0x79622Ea91BBbDF860e9b0497E4C297fC52c8CE64
---

# Avantis 杠杆交易

在 Avantis 上执行杠杆交易——这是全球最大的加密货币、外汇、商品和指数衍生品交易平台。

## 快速入门

### 查看持仓
```bash
avantis_venv/bin/python skills/avantis/scripts/positions.py
```

### 开仓
```bash
# 5x long ETH with $10 collateral
avantis_venv/bin/python skills/avantis/scripts/trade.py long ETH 10 5

# 10x short BTC with $20 collateral
avantis_venv/bin/python skills/avantis/scripts/trade.py short BTC 20 10
```

### 平仓
```bash
# Close specific position
avantis_venv/bin/python skills/avantis/scripts/close.py <pair_index> <trade_index>

# Or close all positions for a pair
avantis_venv/bin/python skills/avantis/scripts/close.py ETH
```

## 钱包配置

**主钱包**: `0x79622Ea91BBbDF860e9b0497E4C297fC52c8CE64`
- 私钥: `/home/ubuntu/clawd/MAIN_WALLET.txt`
- 已批准使用的 USDC 数量: 100 USDC
- 燃气（Gas）余额: 0.004500 ETH（约可进行 89 笔交易）

## 支持的市场

### 加密货币（最高杠杆 50 倍）
- ETH/USD, BTC/USD, SOL/USD, LINK/USD
- ARB/USD, OP/USD, AVAX/USD 等

### 外汇（最高杠杆 100 倍）
- EUR/USD, GBP/USD, USD/JPY, AUD/USD
- USD/CAD, USD/CHF, NZD/USD

### 商品（最高杠杆 100 倍）
- 黄金（XAU/USD），白银（XAG/USD）
- 石油（WTI, Brent）

### 指数（最高杠杆 50 倍）
- SPX, NDX, DJI

## 功能

### 杠杆交易
- **多头**: 价格上涨时获利
- **空头**: 价格下跌时获利
- **最低杠杆**: 2 倍
- **最高杠杆**: 加密货币 50 倍，外汇/商品 100 倍

### 风险管理
- **止盈**: 在目标价格自动平仓（最大亏损为初始投资的 500%）
- **止损**: 在达到止损价格时自动平仓
- **保证金调整**: 增加/减少抵押品以调整杠杆
- **部分平仓**: 平仓部分持仓

### 费用说明
- **亏损保护**: 与市场趋势相反的交易中，亏损可享受最高 20% 的回扣
- **正向滑点**: 有助于平衡未平仓头寸的执行效果
- **动态费用**: 根据市场情况收取 0.04-0.1% 的费用

## 常见操作

### 开仓
```python
# Long ETH: 5x leverage, $10 collateral
# Position size: $50 (10 × 5)
python scripts/trade.py long ETH 10 5

# With take profit and stop loss
python scripts/trade.py long ETH 10 5 --tp 3500 --sl 3000
```

### 查看持仓
```python
python scripts/positions.py

# Output:
# 📊 Open positions: 1
#   • LONG 5x | $10 collateral | ETH/USD
#   • Entry: $3200 | Current: $3250
#   • PnL: +$7.81 (+7.81%)
```

### 平仓
```python
# Full close
python scripts/close.py 0 0  # pair_index=0 (ETH), trade_index=0

# Partial close (50%)
python scripts/close.py 0 0 --amount 5
```

### 更新止损/止盈
```python
python scripts/update-tpsl.py 0 0 --tp 3800 --sl 3100
```

## 持仓规模指南

### 最小持仓规模
- **ETH/USD**: 最小持仓约为 $30
- **BTC/USD**: 最小持仓约为 $50
- 计算公式: `抵押品 × 杠杆 ≥ 最小要求`

### 示例
- ❌ $5 × 5x = $25（对于 ETH 来说持仓规模太小）
- ✅ $10 × 5x = $50（适合 ETH）
- ✅ $20 × 2.5x = $50（适合 ETH）

### 推荐的持仓规模
- **从小额开始**: 使用 $10-20 的抵押品进行测试
- **逐步增加**: 在确认策略有效后逐步增加
- **最大风险**: 每笔交易的风险不超过账户资金的 5-10%

## 杠杆指南

### 保守型（2-5x）
- 清仓风险较低
- 盈亏幅度较小
- 适合: 学习阶段或市场波动较大的情况

### 中等型（5-10x）
- 风险与收益平衡
- 常用于加密货币交易
- 适合: 有明确交易方向的投资者

### 积极型（10-50x）
- 清仓风险较高
- 潜在盈亏幅度较大
- 适合: 短期 scalping 交易或设置紧密的止损

### 极端型（50-100x）
- 清仓风险极高
- 仅适用于外汇/商品交易
- 适合: 经验丰富的交易者

## 费用与成本

### 交易费用
- **开仓费**: 持仓规模的 0.04-0.1%（动态计算）
- **平仓费**: 持仓规模的 0.04-0.1%
- **示例**: $50 的持仓 × 0.08% = $0.04 的费用

### 执行费用
- **费用**: 每笔交易约 $0.10-0.30（以 ETH 计）
- **包含**: 基础网络的燃气费用
- **自动计算**: 由 SDK 处理

### 保证金费用
- **每日费用**: 持仓规模的 0.02-0.05%
- **示例**: $50 的持仓 × 0.03% = 每日 $0.015
- **扣除方式**: 在平仓或调整保证金时扣除

## 风险提示

⚠️ **清算风险**: 如果亏损超过抵押品，持仓将被清算
- 杠杆越高，清算速度越快
- 请定期监控持仓情况

⚠️ **市场风险**: 加密货币/外汇市场波动较大
- 价格可能迅速下跌
- 请使用止损机制

⚠️ **费用影响**: 小额持仓会支付更高的费用
- 保证金费用每日累计
- 请将费用因素纳入利润计算中

## 最佳实践

### 交易前
1. **检查余额**: 确保有足够的 USDC 和燃气
2. **观察市场**: 关注当前价格和波动情况
3. **评估风险**: 了解最大可能的亏损
4. **设置止损**: 使用止损机制

### 交易中
1. **定期监控持仓**: 尤其对高杠杆持仓
2. **根据市场情况调整**: 根据市场变化更新止盈/止损
3. **逐步平仓**: 考虑部分平仓以锁定利润
4. **关注费用**: 保证金费用每日累计

### 交易后
1. **回顾交易表现**: 分析哪些策略有效，哪些无效
2. **调整策略**: 根据交易结果调整持仓规模和杠杆
3. **记录经验**: 将这些经验纳入持续学习的流程中

## 常见问题

### “BELOW_MIN_POS” 错误
- 持仓规模过小
- 解决方案: 增加抵押品或杠杆

### “Price Feed Down”（错误代码 503）
- Avantis 系统故障
- 解决方案: 等待 5-10 分钟后重试

### “余额不足”
- USDC 或燃气不足
- 解决方案: 向钱包充值

### 交易失败
- 通常是由于审批或余额问题
- 解决方案: 检查账户余额，必要时重新提交交易请求

## 高级功能

### 限价单
```python
# Open long at specific price
python scripts/trade.py long ETH 10 5 --limit 3000
```

### 保证金调整
```python
# Add $5 collateral (reduces leverage)
python scripts/update-margin.py 0 0 --deposit 5

# Remove $3 collateral (increases leverage)
python scripts/update-margin.py 0 0 --withdraw 3
```

### 市场研究
```python
# Get current price + analysis
python scripts/market-info.py ETH

# Compare multiple assets
python scripts/market-info.py ETH BTC SOL
```

## 与其他工具的集成

### Bankr（可选）
- 可使用 Bankr 进行市场研究
- 使用 Avantis 进行实际交易
- 目前建议分开使用（使用不同的钱包）

### 持续学习
- 在 `instincts/crypto/` 目录中记录成功的交易策略
- 记录有效的杠杆设置
- 记录入场/出场模式

### 战略性回顾
- 在平仓后进行总结
- 在关键节点评估交易表现
- 根据结果调整交易策略

## 资源

- **平台**: https://avantisfi.com
- **SDK 文档**: https://sdk.avantisfi.com
- **交易指南**: https://docs.avantisfi.com
- **Discord**: https://discord.gg/avantis

## 脚本参考

所有脚本位于 `skills/avantis/scripts/` 目录下：
- `positions.py` - 查看持仓
- `trade.py` - 开新仓
- `close.py` - 平仓（全部或部分）
- `update-tpsl.py` - 更新止盈/止损
- `update-margin.py` - 增加/减少抵押品
- `market-info.py` - 获取市场数据
- `balance.py` - 检查钱包余额

## 安装说明

SDK 已安装在 `/home/ubuntu/clawd/avantis_venv/` 目录下：
```bash
# Activate venv (if needed for manual testing)
source /home/ubuntu/clawd/avantis_venv/bin/activate

# Check installation
python -c "from avantis_trader_sdk import TraderClient; print('✓ SDK ready')"
```

## 安全检查清单

每次交易前请务必：
- [ ] 检查钱包余额（USDC 和燃气）
- [ ] 确认杠杆设置合适
- [ ] 设置止损
- [ ] 确保持仓规模符合最低要求
- [ ] 了解最大亏损情况
- [ ] 制定退出计划

---

**⚠️ 重要提示**: 杠杆交易风险较高。请从小额开始，使用止损机制，切勿冒险投入超出您能承受的损失。