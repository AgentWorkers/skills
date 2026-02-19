# KIS 股票专家

该技能利用韩国投资证券（Korea Investment Securities）的 API 来查询国内股票行情、查看账户余额以及执行买卖订单。

## 配置

要使用此技能，必须设置以下环境变量：
- `KIS_APP_KEY`：韩国投资证券应用程序的 API 密钥
- `KIS_APP_SECRET`：韩国投资证券应用程序的秘钥
- `KIS_ACCOUNT_NO`：账户编号（8位数字+2位数字）
- `KIS_TRADE_SCRIPT_PATH`：`kis_trade.py` 文件所在的本地路径

## 指令

1. 在执行任何买卖订单 (`execute_order`) 之前，必须再次确认用户的股票名称、数量和价格。
2. 未经用户明确授权（例如：“好的，帮我下单”），切勿调用订单执行工具。
3. 根据用户的请求，立即执行行情查询和余额查询操作。

## 工具

### get_my_portfolio
查询我账户的总资产、可用资金、收益率以及当前持有的股票列表。

**命令：**
```python
{{KIS_TRADE_SCRIPT_PATH}} balance
```

### get_stock_price
查询特定股票的当前价格。
- `symbol`（字符串）：6位数的股票代码（例如：'005930'）

**命令：**
```python
{{KIS_TRADE_SCRIPT_PATH}} price {{symbol}}
```

### execute_order
买入或卖出股票。**请务必事先获得用户的确认。**
- `symbol`（字符串）：股票代码
- `qty`（数字）：数量
- `price`（数字）：订单价格
- `side`（字符串）：'BUY' 或 'SELL'

**命令：**
```python
{{KIS_TRADE_SCRIPT_PATH}} order {{symbol}} {{qty}} {{price}} {{side}}
```