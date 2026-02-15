---
name: yahoo-finance-forex
description: 从 Yahoo Finance 获取主要货币对（EUR/USD、GBP/USD、USD/JPY 等）的实时外汇新闻和市场数据。分析市场情绪，并提供交易相关的背景信息。
homepage: https://github.com/nazimboudeffa/openclaw-yahoo-finance-forex
metadata:
  openclaw:
    emoji: "💱"
    requires:
      bins: ["python3"]
    install:
      - id: pip
        kind: pip
        packages: ["yfinance>=0.2.40"]
        label: "Install yfinance"
---

# Yahoo Finance FOREX

使用 Yahoo Finance 的数据来分析主要的外汇货币对：包括新闻、市场数据以及情绪分析。

## 何时使用此功能

- 当用户询问外汇货币对（如 EUR/USD、GBP/USD、USD/JPY 等）时
- 当用户需要最新的外汇新闻或市场情绪分析时
- 当用户需要进行货币交易的基本面分析时
- 当用户询问“EUR/USD 的情况如何？”或类似问题时

## 支持的外汇货币对

**7 个主要货币对：**
- EUR/USD （欧元兑美元）
- GBP/USD （英镑兑美元）
- USD/JPY （美元兑日元）
- USD/CHF （美元兑瑞士法郎）
- AUD/USD （澳元兑美元）
- USD/CAD （美元兑加元）
- NZD/USD （新西兰元兑美元）

## 快速入门

### 获取外汇新闻

```bash
python3 scripts/fetch_forex_news.py EURUSD --limit 10
```

**输出：**
```json
{
  "pair": "EURUSD",
  "current_rate": 1.10250,
  "change_pct": 0.136,
  "news": [
    {
      "title": "ECB maintains hawkish stance on rates",
      "published": "2026-02-02 14:30:00",
      "publisher": "Reuters"
    }
  ],
  "sentiment": {
    "pair_sentiment": 3,
    "recommendation": "BUY"
  }
}
```

## 工作流程

### 1. 用户询问外汇相关内容

**用户：**“EUR/USD 的情况如何？”

**你的操作：**
1. 运行命令：`python3 scripts/fetch_forex_news.py EURUSD --limit 8`
2. 解析 JSON 格式的输出结果
3. 分析市场情绪和新闻
4. 提供以下信息：
   - 当前汇率及变化百分比
   - 主要新闻标题
   - 情绪分析（看涨/看跌）
   - 交易背景（如有支持/阻力位）

### 2. 分析市场情绪

脚本会根据关键词自动计算市场情绪：

**看涨关键词：**增强、上涨、鹰派立场、加息、经济增长
**看跌关键词：**疲软、下跌、鸽派立场、降息、经济衰退

**情绪评分：**
- 正面（> 2）：对该货币对持看涨态度
- 负面（< -2）：对该货币对持看跌态度
- 接近零：中性态度

### 3. 提供交易背景信息

务必包括以下内容：
- **基本面情况**：各国中央银行（如 ECB、Fed、BoJ 等）的货币政策
- **新闻影响**：最新新闻对该货币对的影响
- **技术分析**：当前价格与支持/阻力位的关系

## 脚本参考

### fetch_forex_news.py

**使用方法：**
```bash
python3 scripts/fetch_forex_news.py <PAIR> [--limit N]
```

**参数：**
- `<PAIR>`：货币对（EURUSD、GBPUSD、USDJPY、USDCHF、AUDUSD、USDCAD、NZDUSD）
- `--limit N`：要获取的新闻文章数量（默认值：10，最大值：50）

**输出字段：**
- `pair`：货币对代码
- `current_rate`：当前汇率
- `change_pct`：24 小时内的百分比变化
- `news[]`：新闻文章数组
  - `title`：文章标题
  - `published`：文章发布时间
  - `publisher`：新闻来源
  - `link`：文章链接（可选）
  - `sentiment`：情绪分析结果
  - `pair_sentiment`：情绪评分（-10 到 +10）
  - `recommendation`：买入/卖出/持有建议

## 示例

### 获取 EUR/USD 的分析结果

```bash
python3 scripts/fetch_forex_news.py EURUSD --limit 5
```

### 获取 GBP/USD 的新闻列表

```bash
python3 scripts/fetch_forex_news.py GBPUSD --limit 8
```

## 中央银行的关注点

在分析外汇货币对时，请考虑以下中央银行的影响：
- **EUR/USD**：欧洲央行（ECB）与美联储（Fed）
- **GBP/USD**：英格兰银行（BoE）与美联储（Fed）
- **USD/JPY**：美联储（Fed）与日本央行（BoJ）
- **USD/CHF**：美联储（Fed）与瑞士国家银行（SNB）
- **AUD/USD**：澳大利亚储备银行（RBA）与美联储（Fed）
- **USD/CAD**：美联储（Fed）与加拿大央行（BoC）
- **NZD/USD**：新西兰储备银行（RBNZ）与美联储（Fed）

## 最佳实践

1. **在进行分析之前，务必先获取新闻**  
2. **查看情绪评分**以了解市场倾向  
3. **阅读新闻标题**以识别关键影响因素  
4. **考虑基本面因素**（利率、经济数据、地缘政治）  
5. **提供全面的分析**——同时考虑看涨和看跌因素  
6. **提及风险因素**（波动性、即将发生的事件、技术支撑位/阻力位）

## 参考文件

请查看 `/references` 目录中的文件：
- `api-examples.md`：详细的用法示例  
- `forex-pairs.md`：包含所有可用货币对的完整参考信息  
- `sentiment-guide.md`：情绪分析的方法论说明  

## 限制因素

- 新闻数据可能存在轻微延迟（1-5 分钟）  
- 情绪分析基于关键词，而非深度自然语言处理（NLP）  
- 历史数据仅限于最近 7-14 天内的新闻  
- 不提供实时行情数据（仅提供定期更新）

## 故障排除

**脚本无法运行：**
- 确保已安装 Python 3.7 及更高版本  
- 安装 yfinance 库：`pip install yfinance>=0.2.40`

**未返回新闻：**
- 检查网络连接  
- 确认输入的货币对代码正确  
- 尝试其他货币对或减少新闻获取数量  

**汇率数据缺失：**
- Yahoo Finance API 可能暂时不可用  
- 请稍后再次尝试  

## 技术支持

如有问题或需要帮助，请访问：
- GitHub 仓库：https://github.com/nazimboudeffa/openclaw-yahoo-finance-forex  
- 通过 GitHub Issues 报告问题