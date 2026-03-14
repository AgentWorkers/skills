---
name: mt5-trading-assistant
description: Comprehensive MetaTrader 5 (MT5) trading automation and monitoring skill. Use when users need to connect to MT5 trading platforms, execute trades, monitor accounts, analyze market data, or automate trading strategies. Triggers: MT5, MetaTrader 5, trading automation, forex trading, gold trading (XAUUSD), automated trading, trading bot, MT5 API, execute trade, buy/sell orders, close positions, stop loss/take profit, account monitoring, real-time quotes, K-line data.
---

# MT5交易助手

这是一个专为MetaTrader 5交易平台设计的自动化套件，提供账户监控、交易执行、市场分析和风险管理工具。

## 快速入门

> **重要提示**：此技能包中包含使用了硬编码凭证的示例脚本。在使用前，请务必修改配置信息。

### 先决条件

1. 安装了Python 3.7及以上版本，并且已经安装了`MetaTrader5`相关包：
   ```bash
   pip install MetaTrader5
   ```

2. MT5桌面客户端已启动并登录您的账户。
3. 在MT5中启用了自动交易功能（按F7键或点击工具栏上的交通灯图标）。

### 基本使用示例

#### 检查账户状态
```bash
python scripts/mt5_check.py
```

#### 执行测试交易
```bash
# IMPORTANT: First modify scripts/mt5_buy.py with your account details
python scripts/mt5_buy.py 0.01
```

#### 获取市场快照
```bash
python scripts/mt5_snapshot.py
```

#### 执行交易
```bash
# Buy 0.01 lots at market price
python scripts/mt5_buy.py 0.01

# Sell 0.02 lots at specified price 5040.00
python scripts/mt5_sell.py 0.02 5040.00

# Buy with stop loss and take profit
python scripts/mt5_buy.py 0.01 0 5030 5050
```

#### 平仓
```bash
# Close all script-managed positions
python scripts/mt5_close_all.py

# Close all positions for a symbol
python scripts/mt5_close_all.py all

# Close specific position by ticket
python scripts/mt5_close_all.py 12345678
```

#### 测试K线数据
```bash
python scripts/test_mt5_kline.py
```

## 核心功能

### 1. 账户监控
- 实时跟踪余额和资产净值
- 监控持仓情况并计算盈亏
- 显示保证金和杠杆信息
- 验证连接状态

### 2. 交易执行
- 下单（买入/卖出）
- 平仓（全部或部分）
- 管理止损和止盈
- 支持修改订单

### 3. 市场数据
- 实时买卖报价
- 历史K线数据（M1、M5、H1、D1等时间周期）
- 监控价差
- 计算价格变动

### 4. 风险管理
- 计算持仓规模
- 自动执行止损
- 设置风险百分比限制
- 设置每日损失上限

## 脚本参考

### `mt5_buy.py` - 买入订单执行
```bash
python scripts/mt5_buy.py <volume> [price] [stop_loss] [take_profit]
```
**参数**：
- `volume`：交易量（例如，0.01表示微手）
- `price`：可选的执行价格（0表示市价）
- `stop_loss`：可选的止损价格
- `take_profit`：可选的止盈价格

**示例**：
```bash
# Market buy 0.01 lot
python scripts/mt5_buy.py 0.01

# Limit buy at 5040.00 with SL 5030, TP 5050
python scripts/mt5_buy.py 0.05 5040.00 5030.00 5050.00
```

### `mt5_sell.py` - 卖出订单执行
```bash
python scripts/mt5_sell.py <volume> [price] [stop_loss] [take_profit]
```
**用法**：与`mt5_buy.py`相同，但用于卖出订单。

### `mt5_close_all.py` - 仓位管理
```bash
python scripts/mt5_close_all.py [command]
```
**命令**：
- 无参数：关闭脚本管理的所有仓位（使用魔法数字100001/100002）
- `all`：关闭指定符号的所有仓位
- `<ticket>`：根据订单编号关闭特定仓位

### `mt5_check.py` - 账户状态检查
```bash
python scripts/mt5_check.py
```
**输出**：账户信息、持仓情况、市场数据和系统状态。

### `mt5_snapshot.py` - 市场快照
```bash
python scripts/mt5_snapshot.py
```
**输出**：包含账户信息和交易状态的简洁报告。

### `test_mt5_kline.py` - 数据验证
```bash
python scripts/test_mt5_kline.py
```
**用途**：测试MT5的连接和数据获取功能。

## 配置 - 使用前必须修改

⚠️ **安全警告**：示例脚本中使用了硬编码的演示账户凭证。在使用前，请务必将其替换为您的真实账户凭证。

### 配置选项

#### 选项1：直接修改脚本（快速）
直接编辑每个脚本文件中的配置部分：

```python
# In scripts/mt5_buy.py, scripts/mt5_sell.py, etc.
ACCOUNT_CONFIG = {
    "login": YOUR_ACCOUNT_NUMBER,      # CHANGE THIS
    "password": "YOUR_PASSWORD",       # CHANGE THIS  
    "server": "YOUR_SERVER_NAME",      # CHANGE THIS
    "symbol": "YOUR_SYMBOL",           # e.g., "XAUUSD" or "XAUUSDm"
}
```

#### 选项2：使用配置文件（推荐）
1. 根据模板创建`config.py`文件：
   ```bash
   cp references/config_template.py config.py
   ```

2. 编辑`config.py`文件：
   ```python
   MT5_CONFIG = {
       "login": 12345678,              # YOUR MT5 account number
       "password": "your_password",    # YOUR MT5 password
       "server": "YourServer",         # YOUR MT5 server
       "symbol": "XAUUSD",             # Trading symbol
   }
   ```

3. 在脚本中取消注释导入语句：
   ```python
   # Uncomment these lines in each script:
   try:
       from config import MT5_CONFIG
       ACCOUNT_CONFIG.update(MT5_CONFIG)
   except ImportError:
       print("NOTE: config.py not found, using default configuration")
   ```

### 市场经纪商特定设置

#### Exness
```python
MT5_CONFIG = {
    "login": 277528870,
    "password": "your_password",
    "server": "Exness-MT5Trial5",  # Demo server
    "symbol": "XAUUSDm",           # Gold with 'm' suffix
}
```

#### IC Markets
```python
MT5_CONFIG = {
    "login": 12345678,
    "password": "your_password", 
    "server": "ICMarkets-MT5",
    "symbol": "XAUUSD",            # Standard symbol
}
```

## 常见问题及解决方法

### 连接问题
**错误**：`Initialize failed` 或 `Login failed`
**解决方法**：
1. 确保MT5桌面客户端已启动并登录。
2. 检查`config.py`中的账户凭证是否正确。
3. 确认服务器名称与MT5客户端显示的服务器名称一致。
4. 在MT5中启用自动交易功能（按F7键）。

### 交易问题
**错误**：“自动交易被客户端禁用”
**解决方法**：点击MT5工具栏上的自动交易按钮（交通灯图标）。

**错误**：“无效的符号”
**解决方法**：检查MT5客户端中的符号名称，注意符号名称可能带有经纪商特定的后缀。

### 性能问题
**执行缓慢**：减少刷新频率，关闭不需要的图表。
**连接中断**：检查网络稳定性，重启MT5客户端。

## 高级用法

### 自定义策略
通过导入MT5提供的函数来创建自定义交易策略脚本：

```python
import MetaTrader5 as mt5
from config import MT5_CONFIG

def moving_average_strategy():
    """Simple moving average crossover strategy"""
    # Initialize MT5
    mt5.initialize()
    mt5.login(MT5_CONFIG["login"], MT5_CONFIG["password"], server=MT5_CONFIG["server"])
    
    # Get historical data
    rates = mt5.copy_rates_from(MT5_CONFIG["symbol"], mt5.TIMEFRAME_H1, datetime.now(), 100)
    
    # Calculate indicators
    # ... strategy logic ...
    
    # Execute trades
    # ... order execution ...
    
    mt5.shutdown()
```

### 风险管理集成
```python
from config import MT5_CONFIG

def calculate_position_size(risk_percent=0.02, stop_loss_pips=20):
    """Calculate position size based on risk"""
    account = mt5.account_info()
    risk_amount = account.balance * risk_percent
    
    # Get point value
    symbol_info = mt5.symbol_info(MT5_CONFIG["symbol"])
    point_value = symbol_info.trade_tick_value
    
    # Calculate lot size
    risk_per_pip = risk_amount / stop_loss_pips
    lot_size = risk_per_pip / point_value
    
    return min(lot_size, MT5_CONFIG.get("max_lot_size", 1.0))
```

### 监控仪表盘
创建简单的监控脚本：

```python
#!/usr/bin/env python3
"""
MT5 Trading Dashboard
Refreshes every 10 seconds with account status
"""

import time
from datetime import datetime
import MetaTrader5 as mt5
from config import MT5_CONFIG

def dashboard():
    while True:
        # Clear screen
        print("\n" * 50)
        
        # Get current time
        print(f"MT5 Dashboard - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Get account data
        mt5.initialize()
        mt5.login(MT5_CONFIG["login"], MT5_CONFIG["password"], server=MT5_CONFIG["server"])
        
        # Display data
        account = mt5.account_info()
        if account:
            print(f"Account: {account.login} | Equity: ${account.equity:.2f}")
            print(f"Balance: ${account.balance:.2f} | Margin: ${account.margin:.2f}")
        
        # Get positions
        positions = mt5.positions_get(symbol=MT5_CONFIG["symbol"])
        if positions:
            print(f"\nPositions: {len(positions)}")
            for pos in positions:
                pnl = "+" if pos.profit > 0 else ""
                print(f"  {pos.ticket}: {pos.symbol} {pos.volume} lots | P&L: {pnl}${pos.profit:.2f}")
        
        mt5.shutdown()
        
        print("\n" + "=" * 60)
        print("Next update in 10 seconds (Ctrl+C to stop)")
        
        time.sleep(10)

if __name__ == "__main__":
    try:
        dashboard()
    except KeyboardInterrupt:
        print("\nDashboard stopped")
```

## 安全最佳实践

1. **切勿硬编码密码** - 使用`config.py`文件或环境变量来存储密码。
2. **在生产环境中使用环境变量**：
   ```python
   import os
   MT5_CONFIG = {
       "login": os.getenv("MT5_LOGIN"),
       "password": os.getenv("MT5_PASSWORD"),
       "server": os.getenv("MT5_SERVER"),
   }
   ```
3. **设置文件权限**：`chmod 600 config.py`
4. **将配置文件添加到`.gitignore`文件中**：`echo "config.py" >> .gitignore`
5. **定期更换密码**：每30-90天更改一次密码。

## 资源

### 参考文件
- `references/config_template.py` - 配置模板
- `references/setup_guide.md` - 完整的设置指南

### 外部资源
- [MetaTrader5 Python文档](https://www.mql5.com/en/docs/integration/python_metatrader5)
- [MT5 API参考](https://www.mql5.com/en/docs constants/structures)
- [Exness API指南](https://exness.com/developers/)
- [IC Markets API](https://www.icmarkets.com/development-api/)

## 支持

如遇到问题，请参考以下步骤：
1. 查看`references/setup_guide.md`以获取故障排除建议。
2. 确保MT5客户端已启动且自动交易功能已启用。
3. 使用`python scripts/test_mt5_kline.py`测试连接是否正常。
4. 检查`config.py`中的账户凭证是否正确。

常见解决方案：
- 重启MT5客户端。
- 重新启用自动交易功能（按F7键）。
- 检查网络连接。
- 确认经纪商服务器是否正常运行。