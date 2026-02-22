---
name: allstock-data
description: 通过腾讯金融API查询A股和美股数据。适用于用户需要实时或历史股票报价、指数、ETF价格或中国/美国市场的市场数据的情况。
---
# 中国股票数据

查询A股和美股实时市场数据。

## A股数据查询

### 基本URL
```
http://qt.gtimg.cn/q=<股票代码>
```

### 股票代码规则

| 市场 | 代码前缀 | 示例 |
|--------|-------------|--------- |
| 上交所主板 | sh600xxx | sh600560 |
| 上交所科创板 | sh688xxx | sh688xxx |
| 深交所主板 | sz000xxx | sz000001（平安银行） |
| 深交所创业板 | sz300xxx | sz300xxx |
| 深交所ETF | sz159xxx | sz159326 |

### 指数代码

| 指数 | 代码 | |
|-------|------| |
| 上证综合指数 | sh000001 | |
| 深证成分指数 | sz399001 | |
| 创业板指数 | sz399006 | |
| STAR 50指数 | sz399987 | |
| CSI 300指数 | sh000300 |

### 查询示例

**单只股票：**
```
http://qt.gtimg.cn/q=sh600089
```

**多只股票（用逗号分隔）：**
```
http://qt.gtimg.cn/q=sh600089,sh600560,sz399001
```

### 返回数据格式

返回的数据为准JSON格式，字段之间用`~`分隔：

```
v_sh600089="1~TEB~600089~28.75~28.92~28.63~1999256~...~-0.17~-0.59~..."
```

**关键字段说明：**

| 指数 | 含义 | |
|-------|---------| |
| 0 | 市场代码 | |
| 1 | 股票名称 | |
| 2 | 股票代码 | |
| 3 | 当前价格 | |
| 4 | 开盘价 | |
| 5 | 最低价 | |
| 6 | 最高价 | |
| 30 | 涨跌幅 | |
| 31 | 涨跌幅百分比 | |

**注意**：API会直接返回涨跌幅百分比字段（索引31），请直接使用该字段，无需自行计算。

## 美股数据查询

腾讯财经API对美股的支持有限。可以使用以下替代方案：

### 方案1：Yahoo Finance（推荐）

```bash
curl -s "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
```

### 方案2：Alpha Vantage（需要API密钥）

```bash
curl -s "https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey=YOUR_KEY"
```

### 常见美股指数代码

| 指数 | Yahoo代码 | |
|-------|------------| |
| 道琼斯指数 | ^DJI | |
| 纳斯达克指数 | ^IXIC | |
| 标普500指数 | ^GSPC | |

## 数据解析示例

### Python - 解析腾讯财经数据

```python
import re
import urllib.request

def get_stock_data(code):
    url = f"http://qt.gtimg.cn/q={code}"
    with urllib.request.urlopen(url) as response:
        data = response.read().decode('gbk')

    # 提取数据
    match = re.search(r'="([^"]+)"', data)
    if not match:
        return None

    fields = match.group(1).split '~')

    return {
        'name': fields[1],
        'code': fields[2],
        'price': float(fields[3]),
        'open': float(fields[4]),
        'high': float(fields[5]),
        'low': float(fields[6]),
        'change': float(fields[30]),
        'change_pct': float(fields[31]),
    }

# 使用示例
data = get_stock_data('sh600089')
print(f"{data['name']}: {data['price']} ({data['change_pct']}%")
```

### 使用web_fetch工具

```python
# 获取多只股票数据
url = "http://qt.gtimg.cn/q=sh600001,sh600089,sz399001"
# 使用web_fetch工具获取数据，然后进行解析
```

## 注意事项：

1. **编码**：腾讯财经返回的数据为GBK编码，请正确解码。
2. **涨跌幅百分比**：使用API返回的字段（索引31），避免手动计算。
3. **数据延迟**：实时数据可能存在15分钟的延迟。
4. **请求频率**：避免频繁请求，建议批量查询。
5. **错误处理**：无效的代码会返回`v_pv_none_match="1"`，请检查响应内容。