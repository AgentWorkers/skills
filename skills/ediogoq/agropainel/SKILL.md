# price-monitor

该技能用于查询实时报价（数据始终为最新，无本地缓存）：

- 米西奥纳斯州西德罗兰迪亚地区的豆类（直接收购价格）
- 米西奥纳斯州西德罗兰迪亚地区的玉米（直接收购价格）
- 当前商业美元汇率（数据来源：AwesomeAPI）

## 系统要求
Python 3.9+

## 安装方法
运行以下命令安装所需依赖库：
```
pip install -r requirements.txt
```

## 手动执行方式
直接运行以下Python脚本：
```
python fetch_prices.py
```