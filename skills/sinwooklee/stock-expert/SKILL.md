# KIS交易技能

## 工具

### get_my_portfolio
查询我的账户余额和持有的股票列表。
**命令:**
python C:/Users/nembi/.openclaw/scripts/kis_trade.py balance

### get_stock_price
查询特定股票的当前价格。
- `symbol` (string): 6位股票代码
**命令:**
python C:/Users/nembi/.openclaw/scripts/kis_trade.py price {{symbol}}

### execute_order
买入或卖出股票。（注意：此命令会实际执行交易。）
- `symbol` (string): 股票代码
- `qty` (number): 数量
- `price` (number): 价格（0表示以市价成交，具体价格可能根据API设置有所不同）
- `side` (string): 'BUY' 或 'SELL'
**命令:**
python C:/Users/nembi/.openclaw/scripts/kis_trade.py order {{symbol}} {{qty}} {{price}} {{side}}