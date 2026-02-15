# OpenClaw-Finnhub  
这是一个利用Finnhub API获取实时股票报价和财务数据的OpenClaw技能（plugin）。  

## 系统要求  
- Python 3.11或更高版本  
- 需要安装Finnhub的Python包：`pip3 install finnhub-python`  
- 需要Finnhub的API密钥（[获取方式：访问官网](https://finnhub.io)），并将其设置到环境变量`finnhub_api_key`中  

## 脚本使用方法及功能  
**脚本路径：`./scripts/app.py`**  

### 1. 获取美国股票的实时报价数据  
示例：`python3 ./scripts/app.py 1 NVDA`  
输出结果：  
`当前价格：$185.61，涨跌幅度：$-5.52（-2.8881%），最高价格：$190.3，最低价格：$184.88`