---
name: earnings-calendar
description: 该技能通过使用 Financial Modeling Prep (FMP) API 来检索美国股票的即将发布的收益公告。当用户请求收益日历数据、想知道未来一周哪些公司会发布收益报告，或者需要每周的收益概览时，可以使用该技能。该技能主要针对市值在 20 亿美元以上（中盘及以上）且具有显著市场影响力的公司，将数据按日期和时间顺序整理成清晰的 Markdown 表格格式。支持多种使用环境（命令行界面、桌面应用、Web 应用），并提供灵活的 API 密钥管理功能。
---

# 营业财报日历

## 概述

该技能通过使用Financial Modeling Prep (FMP) API来检索美国股票的即将发布的财报公告。它主要关注那些市值较大（中盘及以上，超过20亿美元）的公司，因为这些公司的财报可能会对市场产生影响。该技能会生成结构化的Markdown报告，显示接下来一周内哪些公司会发布财报，并按日期和时间进行分组（开盘前、收盘后或未公布时间）。

**主要特点**：
- 使用FMP API获取可靠、结构化的财报数据
- 通过市值（>20亿美元）进行筛选，以关注对市场有重大影响的公司
- 包括每股收益（EPS）和收入估算
- 支持多种环境（命令行界面（CLI）、桌面应用和网页）
- 灵活的API密钥管理
- 按日期、时间和市值进行排序

## 先决条件

### FMP API密钥

该技能需要一个Financial Modeling Prep API密钥。

**获取免费API密钥**：
1. 访问：https://site.financialmodelingprep.com/developer/docs
2. 注册免费账户
3. 即刻获得API密钥
4. 免费 tier：每天250次API调用（足够用于每周的财报日历）

**按环境设置API密钥**：

**Claude代码（CLI）**：
```bash
export FMP_API_KEY="your-api-key-here"
```

**Claude桌面应用**：
在系统中设置环境变量或配置MCP服务器。

**Claude网页**：
在执行技能时会请求API密钥（仅存储在当前会话中）。

## 核心工作流程

### 第1步：获取当前日期并计算目标周

**关键**：始终首先获取准确的当前日期。

- 获取当前日期和时间：
  - 使用系统日期/时间获取今天的日期
  - 注意：“今天的日期”在环境变量（<env>标签）中提供
- 计算目标周：从当前日期起接下来的7天

**日期范围计算**：
```
Current Date: [e.g., November 2, 2025]
Target Week Start: [Current Date + 1 day, e.g., November 3, 2025]
Target Week End: [Current Date + 7 days, e.g., November 9, 2025]
```

**为什么这很重要**：
- 财报日历具有时间敏感性
- “下周”必须根据实际的当前日期来计算
- 为API请求提供准确的日期范围

**将日期格式化为YYYY-MM-DD**以确保与API兼容。

### 第2步：加载FMP API指南

在检索数据之前，先加载详细的FMP API指南：

```
Read: references/fmp_api_guide.md
```

该指南包含：
- FMP API端点结构和参数
- 认证要求
- 市值筛选策略（通过公司概况API）
- 财报时间约定（BMO、AMC、TAS）
- 响应格式和字段描述
- 错误处理策略
- 最佳实践和优化提示

### 第3步：检测和配置API密钥

根据环境检测API密钥的可用性。

**多环境API密钥检测**：

#### 3.1 检查环境变量（CLI/桌面应用）

```bash
if [ ! -z "$FMP_API_KEY" ]; then
  echo "✓ API key found in environment"
  API_KEY=$FMP_API_KEY
fi
```

如果环境变量已设置，则继续执行第4步。

#### 3.2 向用户请求API密钥（桌面应用/网页）

如果未找到环境变量，则使用AskUserQuestion工具：

**问题配置**：
```
Question: "This skill requires an FMP API key to retrieve earnings data. Do you have an FMP API key?"
Header: "API Key"
Options:
  1. "Yes, I'll provide it now" → Proceed to 3.3
  2. "No, get free key" → Show instructions (3.2.1)
  3. "Skip API, use manual entry" → Jump to Step 8 (fallback mode)
```

**3.2.1 如果用户选择“否，获取免费密钥”**：

提供说明：
```
To get a free FMP API key:

1. Visit: https://site.financialmodelingprep.com/developer/docs
2. Click "Get Free API Key" or "Sign Up"
3. Create account (email + password)
4. Receive API key immediately
5. Free tier includes 250 API calls/day (sufficient for daily use)

Once you have your API key, please select "Yes, I'll provide it now" to continue.
```

#### 3.3 请求API密钥输入

如果用户有API密钥，则请求输入：

**提示**：
```
Please paste your FMP API key below:

(Your API key will only be stored for this conversation session and will be forgotten when the session ends. For regular use, consider setting the FMP_API_KEY environment variable.)
```

**将API密钥存储在会话变量中**：
```
API_KEY = [user_input]
```

**与用户确认**：
```
✓ API key received and stored for this session.

Security Note:
- API key is stored only in current conversation context
- Not saved to disk or persistent storage
- Will be forgotten when session ends
- Do not share this conversation if it contains your API key

Proceeding with earnings data retrieval...
```

### 第4步：通过FMP API检索财报数据

使用Python脚本从FMP API获取财报数据。

**脚本位置**：
```
scripts/fetch_earnings_fmp.py
```

**执行**：

**选项A：使用环境变量（CLI）**：
```bash
python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09
```

**选项B：使用会话API密钥（桌面应用/网页）**：
```bash
python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09 "${API_KEY}"
```

**脚本工作流程**（自动）：
1. 验证API密钥和日期参数
2. 调用FMP财报日历API获取日期范围内的数据
3. 获取公司概况（市值、行业）
4. 筛选市值超过20亿美元的公司
5. 标准化时间（BMO/AMC/TAS）
6. 按日期 → 时间 → 市值降序排序
7. 将结果输出到stdout

**预期输出格式**（JSON）：
```json
[
  {
    "symbol": "AAPL",
    "companyName": "Apple Inc.",
    "date": "2025-11-04",
    "timing": "AMC",
    "marketCap": 3000000000000,
    "marketCapFormatted": "$3.0T",
    "sector": "Technology",
    "industry": "Consumer Electronics",
    "epsEstimated": 1.54,
    "revenueEstimated": 123400000000,
    "fiscalDateEnding": "2025-09-30",
    "exchange": "NASDAQ"
  },
  ...
]
```

**保存到文件**（建议用于报告生成器）：
```bash
python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09 "${API_KEY}" > earnings_data.json
```

**或捕获到变量中**：
```bash
earnings_data=$(python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09 "${API_KEY}")
```

**错误处理**：

如果脚本返回错误：
- **401 Unauthorized**：API密钥无效 → 验证密钥或重新输入
- **429 Rate Limit**：超过每日250次调用 → 等待或升级计划
- **Empty Result**：指定日期范围内没有财报 → 扩大日期范围或在报告中注明
- **Connection Error**：网络问题 → 重试或使用缓存的数据（如果可用）

### 第5步：处理和组织数据

一旦获取到财报数据（JSON格式），对其进行处理和组织：

#### 5.1 解析JSON数据

从脚本输出中加载JSON数据：
```python
import json
earnings_data = json.loads(earnings_json_string)
```

**或如果已保存到文件中**：
```python
with open('earnings_data.json', 'r') as f:
    earnings_data = json.load(f)
```

#### 5.2 验证数据结构**

确认数据包含以下字段：
- ✓ 股票代码
- ✓ 公司名称
- ✓ 日期
- ✓ 时间（BMO/AMC/TAS）
- ✓ 市值
- ✓ 行业

#### 5.3 按日期分组

按日期对所有财报公告进行分组：
- 星期日，[完整日期]（如适用）
- 星期一，[完整日期]
- 星期二，[完整日期]
- 星期三，[完整日期]
- 星期四，[完整日期]
- 星期五，[完整日期]
- 星期六，[完整日期]（如适用）

#### 5.4 按时间子分组

在每个日期内创建三个子部分：
1. **开盘前（BMO）**
2. **收盘后（AMC）**
3. **未公布时间（TAS）**

数据已经按时间排序，因此保持此顺序。

#### 5.5 在每个时间组内

公司已经按市值降序排序（脚本输出）：
- 巨型股（>2000亿美元）排在最前面
- 大型股（100亿至200亿美元）排在第二位
- 中型股（20亿至100亿美元）排在第三位

这种排序确保了最具市场影响力的公司排在最前面。

#### 5.6 计算汇总统计信息

计算：
- **总公司数量**：数据集中的所有公司数量
- **巨型股/大型股数量**：市值≥100亿美元的公司数量
- **中型股数量**：市值在20亿至100亿美元之间的公司数量
- **峰值日**：财报公告最多的星期几
- **行业分布**：按行业统计（科技、医疗保健、金融等）
- **市值最高的5家公司**：市值最高的5家公司

### 第6步：生成Markdown报告

使用报告生成脚本从JSON数据创建格式化的Markdown报告。

**脚本位置**：
```
scripts/generate_report.py
```

**执行**：

**选项A：输出到stdout**：
```bash
python scripts/generate_report.py earnings_data.json
```

**选项B：保存到文件**：
```bash
python scripts/generate_report.py earnings_data.json earnings_calendar_2025-11-02.md
```

**脚本的作用**：
1. 从JSON文件中加载财报数据
2. 按日期和时间（BMO/AMC/TAS）进行分组
3. 在每个组内按市值排序
4. 计算汇总统计信息
5. 生成格式化的Markdown报告
6. 输出到stdout或保存到文件

脚本自动处理所有格式化工作，包括：
- 正确的Markdown表格结构
- 日期分组和星期名称
- 市值排序
- EPS和收入格式化
- 汇总统计信息的计算

**报告结构**：
```markdown
# Upcoming Earnings Calendar - Week of [START_DATE] to [END_DATE]

**Report Generated**: [Current Date]
**Data Source**: FMP API (Mid-cap and above, >$2B market cap)
**Coverage Period**: Next 7 days
**Total Companies**: [COUNT]

---

## Executive Summary

- **Total Companies Reporting**: [TOTAL_COUNT]
- **Mega/Large Cap (>$10B)**: [LARGE_CAP_COUNT]
- **Mid Cap ($2B-$10B)**: [MID_CAP_COUNT]
- **Peak Day**: [DAY_WITH_MOST_EARNINGS]

---

## [Day Name], [Full Date]

### Before Market Open (BMO)

| Ticker | Company | Market Cap | Sector | EPS Est. | Revenue Est. |
|--------|---------|------------|--------|----------|--------------|
| [TICKER] | [COMPANY] | [MCAP] | [SECTOR] | [EPS] | [REV] |

### After Market Close (AMC)

| Ticker | Company | Market Cap | Sector | EPS Est. | Revenue Est. |
|--------|---------|------------|--------|----------|--------------|
| [TICKER] | [COMPANY] | [MCAP] | [SECTOR] | [EPS] | [REV] |

### Time Not Announced (TAS)

| Ticker | Company | Market Cap | Sector | EPS Est. | Revenue Est. |
|--------|---------|------------|--------|----------|--------------|
| [TICKER] | [COMPANY] | [MCAP] | [SECTOR] | [EPS] | [REV] |

---

[Repeat for each day of week]

---

## Key Observations

### Highest Market Cap Companies This Week
1. [COMPANY] ([TICKER]) - [MCAP] - [DATE] [TIME]
2. [COMPANY] ([TICKER]) - [MCAP] - [DATE] [TIME]
3. [COMPANY] ([TICKER]) - [MCAP] - [DATE] [TIME]

### Sector Distribution
- **Technology**: [COUNT] companies
- **Healthcare**: [COUNT] companies
- **Financial**: [COUNT] companies
- **Consumer**: [COUNT] companies
- **Other**: [COUNT] companies

### Trading Considerations
- **Days with Heavy Volume**: [DATES with multiple large-cap earnings]
- **Pre-Market Focus**: [BMO companies that may move markets]
- **After-Hours Focus**: [AMC companies that may move markets]

---

## Timing Reference

- **BMO (Before Market Open)**: Announcements typically around 6:00-8:00 AM ET before market opens at 9:30 AM ET
- **AMC (After Market Close)**: Announcements typically around 4:00-5:00 PM ET after market closes at 4:00 PM ET
- **TAS (Time Not Announced)**: Specific time not yet disclosed - monitor company investor relations

---

## Data Notes

- **Market Cap Categories**:
  - Mega Cap: >$200B
  - Large Cap: $10B-$200B
  - Mid Cap: $2B-$10B

- **Filter Criteria**: This report includes companies with market cap $2B and above (mid-cap+) with earnings scheduled for the next week.

- **Data Source**: Financial Modeling Prep (FMP) API

- **Data Freshness**: Earnings dates and times can change. Verify critical dates through company investor relations websites for the most current information.

- **EPS and Revenue Estimates**: Analyst consensus estimates from FMP API. Actual results will be reported on earnings date.

---

## Additional Resources

- **FMP API Documentation**: https://site.financialmodelingprep.com/developer/docs
- **Seeking Alpha Calendar**: https://seekingalpha.com/earnings/earnings-calendar
- **Yahoo Finance Calendar**: https://finance.yahoo.com/calendar/earnings

---

*Report generated using FMP Earnings Calendar API with mid-cap+ filter (>$2B market cap). Data current as of report generation time. Always verify earnings dates through official company sources.*
```

**格式化最佳实践**：
- 使用Markdown表格进行清晰展示
- 如需要，用粗体显示重要公司名称（巨型股）
- 以人类可读的格式显示市值（例如$3.0T、$150B、$5.2B）——已由脚本格式化
- 按日期和时间逻辑分组
- 在顶部添加摘要部分以便快速查看
- 如果有，包括EPS和收入估算

### 第7步：质量保证

在最终确定报告之前，进行验证：

**数据质量检查**：
1. ✓ 所有日期都在目标周内（接下来的7天）
2. ✓ 所有公司的市值值都存在
3. ✓ 每家公司的时间都已指定（BMO/AMC/TAS）
4. ✓ 每个组内的公司都按市值排序
5. ✓ 汇总统计信息准确
6. ✓ 明确报告生成日期
7. ✓ 如果有，包括EPS和收入估算

**完整性检查**：
1. ✓ 包括目标周内的所有日期（即使没有财报）
2. ✓ 不遗漏任何主要公司（如有需要，可对外部来源进行验证）
3. ✓ 包括行业信息（如果有的话）
4. ✓ 包含时间参考部分
5. ✓ 显示数据来源（FMP API）

**格式检查**：
1. ✓ Markdown表格格式正确
2. ✓ 日期格式一致
3. ✓ 市值使用一致的单位（B表示十亿，T表示万亿）
4. ✓ 所有部分都遵循模板结构
5. ✓ 没有保留占位符文本（[PLACEHOLDER]）
6. ✓ EPS和收入估算格式正确

### 第8步：保存和交付报告

使用适当的文件名保存生成的报告：

**文件名约定**：
```
earnings_calendar_[YYYY-MM-DD].md
```

示例：`earnings_calendar_2025-11-02.md`

文件名中的日期代表报告生成日期，而不是财报周。

**交付**：
- 将Markdown文件保存到工作目录
- 通知用户报告已生成
- 提供关键发现的简要总结（例如：“下周有45家公司发布财报，其中苹果公司和微软公司在周一）

**示例总结**：
```
✓ Earnings calendar report generated: earnings_calendar_2025-11-02.md

Summary for week of November 3-9, 2025:
- 45 companies reporting earnings
- 28 large/mega-cap, 17 mid-cap
- Peak day: Thursday (15 companies)
- Notable: Apple (Mon AMC), Microsoft (Tue AMC), Tesla (Wed AMC)

Top 5 by market cap:
1. Apple - $3.0T (Mon AMC)
2. Microsoft - $2.8T (Tue AMC)
3. Alphabet - $1.8T (Thu AMC)
4. Amazon - $1.6T (Fri AMC)
5. Tesla - $800B (Wed AMC)
```

## 备用模式（第8步的替代方案）：手动输入数据

如果API访问不可用或用户选择跳过API：

**提供手动输入的说明**：

```
Since FMP API is not available, you can manually gather earnings data:

1. Visit Finviz: https://finviz.com/screener.ashx?v=111&f=cap_midover%2Cearningsdate_nextweek
2. Or Yahoo Finance: https://finance.yahoo.com/calendar/earnings
3. Note down companies reporting next week

Please provide the following information for each company:
- Ticker symbol
- Company name
- Earnings date
- Timing (BMO/AMC/TAS)
- Market cap (approximate)
- Sector

I will format this into the standard earnings calendar report.
```

**处理手动输入**：
1. 解析用户提供的财报数据
2. 按日期、时间和市值进行组织
3. 使用相同的模板生成报告
4. 在报告中注明：“数据来源：手动输入”

## 使用案例和示例

### 使用案例1：每周回顾（主要使用案例）

**用户请求**：“获取下周的财报日历”

**工作流程**：
1. 获取当前日期（例如，2025年11月2日）
2. 计算目标周（2025年11月3日至9日）
3. 加载FMP API指南
4. 检测/请求API密钥
5. 获取财报数据：
   ```bash
   python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09 > earnings_data.json
   ```
6. 生成Markdown报告：
   ```bash
   python scripts/generate_report.py earnings_data.json earnings_calendar_2025-11-02.md
   ```
7. 向用户提供摘要

**完整的一句话**：
```bash
python scripts/fetch_earnings_fmp.py 2025-11-03 2025-11-09 > earnings_data.json && \
python scripts/generate_report.py earnings_data.json earnings_calendar_2025-11-02.md
```

### 使用案例2：关注特定日期

**用户请求**：“周一有哪些财报？”

**工作流程**：
1. 获取当前日期并确定下一个周一（例如，2025年11月4日）
2. 获取完整周的数据（与使用案例1相同）
3. 生成完整报告，但突出显示周一的部分
4. 提供周一财报的口头总结

### 使用案例3：关注巨型股

**用户请求**：“显示下周市值超过100亿美元公司的财报”

**工作流程**：
1. 获取完整的财报数据（脚本已经筛选出市值超过20亿美元的公司）
2. 按常规处理和组织数据
3. 在生成报告时，在顶部添加“巨型股重点”部分
4. 在表格中筛选出市值超过100亿美元的公司
5. 注意：附录中仍包含完整数据以供参考

### 使用案例4：特定行业

**用户请求**：“下周有哪些科技公司的财报？”

**工作流程**：
1. 获取完整的财报数据
2. 按常规处理和组织数据
3. 按行业（例如“科技”）筛选结果
4. 生成专注于科技行业的报告
5. 注意：模板结构保持不变；内容经过筛选

## 故障排除

### 问题：API密钥无法使用

**解决方案**：
- 验证API密钥是否正确（小心复制粘贴）
- 检查API密钥是否有效（登录FMP仪表板）
- 确保密钥前后没有额外的空格
- 尝试从FMP仪表板获取新的API密钥

### 问题：脚本返回空结果

**解决方案**：
- 确认日期范围在未来（不是过去的日期）
- 检查日期格式是否为YYYY-MM-DD
- 尝试更宽的日期范围（例如，14天而不是7天）
- 确认该公司确实在该周发布了财报日期

### 问题：缺少主要公司

**解决方案**：
- 公司可能尚未公布财报日期
- 有些公司会在最后一天（提前1-2天）公布日期
- 与公司的投资者关系网站进行交叉核对
- 市值可能降至20亿美元的阈值以下

### 问题：达到速率限制（429错误）

**解决方案**：
- 免费 tier：每天250次调用
- 每份每周报告大约使用3-5次API调用
- 检查是否有其他工具/脚本正在使用相同的API密钥
- 等待24小时以重置速率限制
- 如果需要，考虑升级到付费tier

### 问题：脚本执行错误

**解决方案**：
- 验证是否安装了Python 3：`python3 --version`
- 安装requests库：`pip install requests`
- 检查脚本是否有执行权限：`chmod +x fetch_earnings_fmp.py`
- 显式使用python3运行：`python3 fetch_earnings_fmp.py ...`

## 最佳实践

### 应该做的
✓ 在任何数据检索之前，始终先获取当前日期
✓ 使用FMP API作为主要数据来源以确保可靠性
✓ 将API密钥存储在环境变量中，以便在CLI中使用
✓ 按市值排序，以优先显示高影响力公司
✓ 按日期和时间分组，以便逻辑清晰
✓ 包括摘要统计信息以便快速查看
✓ 在报告页脚中注明数据来源
✓ 使用清晰的Markdown表格以便阅读
✓ 提供时间参考部分以便清晰
✓ 注意数据的新鲜度和可能的变化
✓ 如果有，包括EPS和收入估算

### 不应该做的
✗ 不要在不根据当前日期计算的情况下假设“下周”
✗ 不要省略时间信息（BMO/AMC/TAS）
✗ 不要在报告中混合日期格式（保持一致）
✗ 除非特别要求，否则不要包括微型股/小型股
✗ 不要忘记按市值在各个部分内进行排序
✗ 不要在对话或报告中分享API密钥
✗ 不要包括当前周或过去日期的财报
✗ 不要在没有质量保证检查的情况下生成报告
✗ 不要将API密钥提交到版本控制系统中

## 安全注意事项

### API密钥安全

**重要提醒**：
1. ✓ 使用免费tier API密钥进行测试
2. ✓ 定期轮换密钥
3. ✓ 不要在对话中分享包含API密钥的内容
4. ✓ 将API密钥设置为CLI的环境变量
5. ✓ 在聊天中提供的密钥仅限当前会话使用（会话结束后即被遗忘）
6. ✗ 永远不要将API密钥提交到Git仓库
7. ✗ 永远不要在生产环境中使用API密钥访问敏感数据

**最佳实践**：
对于Claude Code（CLI），始终使用环境变量：
```bash
# Add to ~/.zshrc or ~/.bashrc
export FMP_API_KEY="your-key-here"
```

对于Claude网页，需要注意：
- 在聊天中输入的API密钥是临时的
- 仅存储在聊天上下文中
- 不会保存到磁盘
- 会话结束后即被遗忘

## 资源

**FMP API**：
- 主要文档：https://site.financialmodelingprep.com/developer/docs
- 获取API密钥：https://site.financialmodelingprep.com/developer/docs
- 财报日历API：https://site.financialmodelingprep.com/developer/docs/earnings-calendar-api
- 公司概况API：https://site.financialmodelingprep.com/developer/docs/companies-key-metrics-api
- 定价/速率限制：https://site.financialmodelingprep.com/developer/docs/pricing

**补充资源**（用于验证）：
- Seeking Alpha：https://seekingalpha.com/earnings/earnings-calendar
- Yahoo Finance：https://finance.yahoo.com/calendar/earnings
- MarketWatch：https://www.marketwatch.com/tools/earnings-calendar

**技能资源**：
- FMP API指南：`references/fmp_api_guide.md`
- Python脚本：`scripts/fetch_earnings_fmp.py`
- 报告模板：`assets/earnings_report_template.md`

---

## 总结

该技能提供了一种可靠的、基于API的方法来生成美国股票的每周财报日历。通过使用FMP API，它可以确保数据结构化且准确，并提供额外的信息，如EPS/收入估算。多环境支持使其适用于CLI、桌面应用和网页，而备用模式则确保在没有API访问的情况下也能正常工作。

**关键工作流程**：日期计算 → API密钥设置 → API数据检索 → 数据处理 → 报告生成 → 质量保证 → 交付

**输出**：清晰、组织良好的Markdown报告，其中财报按日期/时间/市值分组，包括汇总统计信息和交易注意事项。