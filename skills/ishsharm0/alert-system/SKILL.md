# 警报系统

具备可定制触发器的智能监控功能——包括价格警报（股票、加密货币、产品）、事件监控以及通过 Telegram 发送的通知。

## 使用方法
```python
from alert_system.alerts import AlertSystem

system = AlertSystem("<username>")
system.add_alert("price", "BTC", "above", 100000)
triggered = system.check_all()
```

## 主要功能
- 价格警报（通过 yfinance 提供的股票价格数据）
- 网站/事件变化监控
- 可自定义的条件触发器
- 集成 Cron 任务进行定期检查
- 触发条件满足时通过 Telegram 发送通知