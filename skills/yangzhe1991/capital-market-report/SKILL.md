---
name: capital-market-report
description: 生成高影响力、基于市场异常现象和谣言的报告。重点关注具有实际操作价值的商业信号、打破市场预期的新闻，以及深入的逻辑分析，而非简单的指数数据解读。通过本地扫描工具收集中国及全球金融媒体的信息、Reddit和Twitter上的内容。系统采用严格的市场隔离规则，以避免信息来源的混淆，并要求提供真实的新闻来源URL。
---
# 资本市场报告（高信号异常版）

该技能基于“绝对影响阈值”生成前瞻性的商业推论报告。它摒弃了传统的宏观经济指标分析方法（例如“纳斯达克下跌1%”），转而深入挖掘国内外论坛、新闻和社交媒体中的信息，以识别供应链异常和收益爆发点，尤其是那些存在巨大预期差距的情况。

## 核心理念（绝对影响阈值）

1. **零常规数据**：不再报告常规的市场数据（如指数点位或每日百分比变化），完全专注于商业领域中的重大异常事件。
2. **动态判断**：取消“必须包含3-5个事件”的机械性规则。如果当天只有2个事件符合阈值，就报告这2个事件；如果有8个重大全球供应链相关新闻，就全部报告。
3. **聚焦重点资产，涵盖全球领导者**：在深入分析特定目标资产（如中国存托凭证、A/HK科技股、人工智能/消费/电动汽车供应链）的同时，绝不能忽略全球科技巨头的战略转折点（如“七大巨头”或核心全球人工智能企业）。

## 执行流程与工具链

### 第一步：启动基础数据抓取工具

您需要运行以下信息抓取工具：

**1. 中国财经核心新闻抓取工具**（抓取Cailianshe、华尔街CN、新浪财经等国内媒体来源的数据）：
```bash
uv run scripts/news-processor.py
```

**2. 海外异常与谣言监测工具**（监控Reddit WSB、CoinGecko、Yahoo Finance上的动态以及谷歌新闻中的谣言）：
*（注意：需要安装`stock-analysis`技能才能使用该工具）*
```bash
uv run ~/.openclaw/skills/stock-analysis/scripts/hot_scanner.py
uv run ~/.openclaw/skills/stock-analysis/scripts/rumor_scanner.py
```

### 第二步：筛选“预期差距”

从抓取到的结果中，仅保留符合“绝对影响阈值”的新闻：
- 极其显著的收益逆转或订单激增（例如，某巨头的净利润骤降或订单量激增）。
- 全球供应链层面的产品延误或技术突破（例如，基础模型的发布延迟）。
- 数十亿美元的并购传闻或大量散户投资者的集中行动。

### 第三步：强制来源验证

如果抓取脚本仅返回新闻标题或门户网站首页，**必须使用`web_search`工具**来查找新闻文章的原始URL。
- **重要提示**：不要使用域名首页（例如`https://finance.yahoo.com/`）或搜索引擎结果页面作为来源链接，必须找到文章的实际发布页面。

### 第四步：逻辑推论与本地化

对选定的事件进行严格的逻辑推论：
- **市场范围界定**：明确异常事件发生的“国家/市场”。例如，美国国内机票价格的上涨只能被推断为对美国航空公司和美国在线旅行平台的利好消息；**绝对不能**将其直接应用于中国公司（如Trip.com）。
- 如果事件对海外巨头造成冲击（例如，本田遭受重大亏损），必须验证这一事件对其全球竞争对手的影响是否成立。
- **语言本地化**：尽管该技能的描述使用英语，但生成的最终报告必须使用用户的主要交流语言（例如，如果用户使用中文，报告必须用中文撰写）。

## 报告输出格式

报告必须简洁明了，以推论为核心：

```markdown
📊 **Capital Market Absolute Impact Report | YYYY-MM-DD HH:MM**

⚠️ **Core Anomaly Alerts (Potential Expectation Gaps & Strategic Inflection Points)**

- **[Category/Theme] Core Event Title (Marked with Country/Market)**
  **Source & Link**: News Source Name ([Read Original](Real_Article_URL))
  **Core**: A single sentence highlighting the crux of the anomaly.
  **Rigorous Deduction**: 1-2 sentences pointing out the bullish/bearish impact and specific stock tickers or supply chains. The logic must be airtight.

- **[Category/Theme] Core Event Title (Marked with Country/Market)**
  **Source & Link**: News Source Name ([Read Original](Real_Article_URL))
  **Core**: ...
  **Rigorous Deduction**: ...
```