---
name: kis-trading
description: "使用韩国投资证券（KIS）的Open API进行国内股票交易：包括余额查询、行情查看、买卖订单提交、交易记录查看以及市场行情了解等。"
metadata:
  openclaw:
    emoji: "📈"
    requires:
      bins: ["python3"]
      pip: ["requests"]
    config_keys:
      - KIS_APP_KEY
      - KIS_APP_SECRET
      - KIS_ACCOUNT_NO
      - KIS_BASE_URL
---

# KIS股票交易

通过韩国投资证券（Korea Investment & Securities）的Open API进行国内股票买卖的技能。

## 设置

在`~/.kis-trading/config.ini`配置文件中设置以下参数：

```ini
[KIS]
APP_KEY = your_app_key
APP_SECRET = your_app_secret
ACCOUNT_NO = 12345678-01
BASE_URL = https://openapi.koreainvestment.com:9443
# 모의투자: https://openapivts.koreainvestment.com:29443
```

## 检查配置：

```bash
python3 scripts/setup.py --config ~/.kis-trading/config.ini --check
```

## 查看账户余额

- 显示账户余额
- 显示可用资金
- 显示可购买的股票金额

```bash
python3 scripts/balance.py --config ~/.kis-trading/config.ini
```

## 持有的股票

- 显示持有的股票信息
- 显示我的股票
- 显示股票收益率

```bash
python3 scripts/holdings.py --config ~/.kis-trading/config.ini
```

## 股票行情

- 显示三星电子的当前价格（代码：005930）
- 显示Kakao的股价

```bash
python3 scripts/quote.py --config ~/.kis-trading/config.ini --code 005930
python3 scripts/quote.py --config ~/.kis-trading/config.ini --name 삼성전자
```

## 下单/成交

- 下单购买三星电子10股
- 下单出售Kakao 5股

**⚠️ 请务必在用户确认后执行任何订单！**

## 下单前必须：
1. 向用户展示股票名称、数量和价格，并请求确认
2. 可以使用`--dry-run`选项预览订单内容
3. 确认无误后执行实际订单

## 交易记录

- 显示交易历史
- 显示今天的成交记录
- 显示所有订单的详细信息

```bash
python3 scripts/history.py --config ~/.kis-trading/config.ini
python3 scripts/history.py --config ~/.kis-trading/config.ini --start 20240101 --end 20240131
```

## 市场概况

- 查看市场整体情况
- 显示成交量排名前几位的股票
- 显示KOSPI指数

## 注意事项：
- 在实际投资时，请务必将`BASE_URL`设置为正确的API地址
- 模拟交易和实际交易的TR ID可能不同
- API调用每秒限制为20次（系统会自动控制）
- **严禁**在未经用户确认的情况下执行任何订单