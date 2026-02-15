---
name: economic-calendar-fetcher
description: 使用 FMP API 获取即将发生的经济事件和数据发布信息。检索预定发布的央行决策、就业报告、通胀数据、GDP 数据以及其他可能影响市场的经济指标，覆盖指定的日期范围（默认为未来 7 天）。以时间顺序生成包含影响评估的 Markdown 报告。
---

# 经济日历获取工具

## 概述

该工具通过 Financial Modeling Prep (FMP) 的经济日历 API 检索即将发生的经济事件和数据发布。它能够获取预定发布的经济指标，包括中央银行的货币政策决策、就业报告、通胀数据（CPI/PPI）、GDP 数据、零售销售数据以及其他可能影响金融市场的事件。

该工具使用 Python 脚本查询 FMP API，并为每个预定事件生成按时间顺序排列的 Markdown 报告，同时附有市场影响评估。

**主要功能：**
- 获取指定日期范围内的经济事件（最长 90 天）
- 支持灵活的 API 密钥配置（环境变量或用户输入）
- 根据影响程度、国家或事件类型进行过滤
- 生成包含影响分析的结构化 Markdown 报告
- 默认查询未来 7 天内的事件，以便快速了解市场动态

**数据来源：**
- FMP 经济日历 API：`https://financialmodelingprep.com/api/v3/economic_calendar`
- 覆盖主要经济体：美国、欧盟、英国、日本、中国、加拿大、澳大利亚
- 事件类型：中央银行决策、就业数据、通胀数据、GDP 数据、贸易数据、房地产数据、调查数据

## 适用场景

当用户需要以下信息时，可以使用该工具：
1. **经济日历查询：**
   - “本周有哪些经济事件？”
   - “请显示未来两周的经济日历”
   - “下一次 FOMC 会议是什么时候？”
   - “下个月将发布哪些重要的经济数据？”
2. **市场事件规划：**
   - “本周市场有哪些值得关注的事件？”
   - “是否有高影响力的经济数据发布？”
   - “下一次就业报告/CPI 报告/GDP 报告是什么时候？”
3. **特定日期范围查询：**
   - “获取 1 月 1 日到 1 月 31 日之间的经济事件”
   - “2025 年第一季度的经济日历有哪些事件？”
4. **国家特定查询：**
   - “显示下周的美国经济数据发布”
   - “欧洲央行的活动安排是什么？”
   - “日本何时发布通胀数据？”

**不适用场景：**
- 过去的经济事件（请使用市场新闻分析工具进行历史分析）
- 企业收益日历（该工具不包含企业收益信息）
- 实时市场数据或实时报价
- 技术分析或图表解读

## 工作流程

按照以下步骤获取和分析经济日历：

### 第 1 步：获取 FMP API 密钥

**检查 API 密钥是否可用：**
1. 首先检查 `FMP_API_KEY` 环境变量是否已设置。
2. 如果未设置，请通过聊天请求用户提供 API 密钥。
3. 如果用户没有 API 密钥，请提供以下指导：
   - 访问 https://financialmodelingprep.com
   - 注册免费账户（每日请求限制为 250 次）
   - 登录 API 控制面板以获取密钥。

**示例用户交互：**
```
User: "Show me economic events for next week"
Assistant: "I'll fetch the economic calendar. Do you have an FMP API key? I can use the FMP_API_KEY environment variable, or you can provide your API key now."
```

### 第 2 步：确定日期范围

**根据用户请求设置合适的日期范围：**
- **默认值（无特定日期）：** 今天起 7 天
- **用户指定日期范围：** 使用确切的日期（验证格式：YYYY-MM-DD）
- **最大范围：** 90 天（FMP API 限制）

**示例：**
- “下周” → 今天起 7 天
- “未来两周” → 今天起 14 天
- “2025 年 1 月” → 2025-01-01 至 2025-01-31
- “2025 年第一季度” → 2025-01-01 至 2025-03-31

**验证日期范围：**
- 确保开始日期 ≤ 结束日期
- 确保范围 ≤ 90 天
- 如果查询的日期在过去，请发出警告

### 第 3 步：执行 API 查询脚本

**使用适当的参数运行 `get_economic_calendar.py` 脚本：**

**基本用法（默认查询 7 天）：**
```bash
python3 /path/to/economic-calendar-fetcher/scripts/get_economic_calendar.py --api-key YOUR_KEY
```

**使用特定日期范围：**
```bash
python3 /path/to/economic-calendar-fetcher/scripts/get_economic_calendar.py \
  --from 2025-01-01 \
  --to 2025-01-31 \
  --api-key YOUR_KEY \
  --format json
```

**使用环境变量（无需 `--api-key`）：**
```bash
export FMP_API_KEY=your_key_here
python3 /path/to/economic-calendar-fetcher/scripts/get_economic_calendar.py \
  --from 2025-01-01 \
  --to 2025-01-07
```

**脚本参数：**
- `--from`：开始日期（YYYY-MM-DD） - 默认：今天
- `--to`：结束日期（YYYY-MM-DD） - 默认：今天起 7 天
- `--api-key`：FMP API 密钥（如果设置了 `FMP_API_KEY` 环境变量，则可选）
- `--format`：输出格式（json 或 text） - 默认：json
- `--output`：输出文件路径（可选，默认：stdout）

**错误处理：**
- API 密钥无效 → 请用户验证密钥
- 超过请求频率限制（429） → 建议等待或升级 FMP 订阅等级
- 网络错误 → 采用指数退避策略重试
- 日期格式无效 → 提供正确的格式示例

### 第 4 步：解析和过滤事件

**处理脚本返回的 JSON 数据：**
1. **解析事件信息：** 从 API 响应中提取所有事件。
2. **应用用户指定的过滤条件：**
   - 影响程度：“高”、“中”、“低”
   - 国家：“美国”、“欧盟”、“日本”、“中国”等
   - 事件类型：FOMC、CPI、就业、GDP 等
   - 货币：“USD”、“EUR”、“JPY”等

**过滤示例：**
- “仅显示高影响力事件” → 过滤条件：`impact == "High`
- “仅显示美国事件” → 过滤条件：`country == "US"`
- “中央银行决策” → 在事件名称中搜索 “Rate”、“Policy”、“FOMC”、“ECB”、“BOJ”

**事件数据结构：**
```json
{
  "date": "2025-01-15 14:30:00",
  "country": "US",
  "event": "Consumer Price Index (CPI) YoY",
  "currency": "USD",
  "previous": 2.6,
  "estimate": 2.7,
  "actual": null,
  "change": null,
  "impact": "High",
  "changePercentage": null
}
```

### 第 5 步：评估市场影响

**评估每个事件的市场影响：**

**影响程度分类（根据 FMP 的划分）：**
- **高影响力：** 对市场有重大影响的事件
  - FOMC 利率决策、欧洲央行/日本央行的政策会议
  - 非农就业数据（NFP）、CPI、GDP
  - 通常会导致市场波动幅度在 0.5% 以上
- **中等影响力：** 有显著影响但波动较小
  - 零售销售、工业生产数据
  - 采购经理指数（PMI）、消费者信心指数
  - 房地产数据、耐用品订单
- **低影响力：** 影响较小的指标
  - 周度失业申请数据（除非数值极端）
  - 地区制造业调查数据
  - 小型拍卖结果

**其他影响因素：**
1. **当前市场敏感度：**
   - 高通胀环境 → CPI/PPI 的重要性增加
   - 经济衰退担忧 → 就业数据更为关键
   - 利率下调预期 → 中央银行会议至关重要
2. **意外可能性：**
   - 实际数据与预期值的差异
   - 预期变化较大 → 关注度较高
   - 公众预期不确定性 → 影响潜力较大
3. **事件关联性：**
   - 同一天内有多个相关事件 → 影响叠加
   - 例如：CPI、零售销售数据加上美联储讲话 → 影响极大
4. **未来影响：**
   - 该事件是否会影响未来的中央银行决策？
   - 这是初步数据还是最终数据？
   - 这些数据是否会进行修正？

### 第 6 步：生成输出报告

**创建结构化的 Markdown 报告，包含以下部分：**

**报告标题：**
```markdown
# Economic Calendar
**Period:** [Start Date] to [End Date]
**Report Generated:** [Timestamp]
**Total Events:** [Count]
**High Impact Events:** [Count]
```

**事件列表（按时间顺序）：**

为每个事件提供详细信息：
```markdown
## [Date] - [Day of Week]

### [Event Name] ([Impact Level])
- **Country:** [Country Code] ([Currency])
- **Time:** [HH:MM UTC]
- **Previous:** [Value]
- **Estimate:** [Consensus Forecast]
- **Impact Assessment:** [Your analysis]

**Market Implications:**
[2-3 sentences on why this matters, what markets watch for, typical reaction patterns]

---
```

**示例事件条目：**
```markdown
## 2025-01-15 - Wednesday

### Consumer Price Index (CPI) YoY (High Impact)
- **Country:** US (USD)
- **Time:** 14:30 UTC (8:30 AM ET)
- **Previous:** 2.6%
- **Estimate:** 2.7%
- **Impact Assessment:** Very High - Core inflation metric for Fed policy decisions

**Market Implications:**
CPI reading above estimate (>2.7%) likely strengthens hawkish Fed expectations, potentially pressuring equities and supporting USD. Reading at or below 2.7% could reinforce disinflation narrative and support risk assets. Options market pricing 1.2% S&P 500 move on release day.

---
```

**总结部分：**

在报告末尾添加分析性总结：
```markdown
## Key Takeaways

**Highest Impact Days:**
- [Date]: [Events] - [Combined impact rationale]
- [Date]: [Events] - [Combined impact rationale]

**Central Bank Activity:**
- [Summary of any scheduled Fed/ECB/BOJ meetings or speeches]

**Major Data Releases:**
- Employment: [NFP, Unemployment Rate dates]
- Inflation: [CPI, PPI dates]
- Growth: [GDP, Retail Sales dates]

**Market Positioning Considerations:**
[2-3 bullets on how traders might position around these events]

**Risk Events:**
[Highlight any particularly high-uncertainty or surprise-potential events]
```

**过滤说明：**

如果用户指定了特定过滤条件，请在顶部注明：
```markdown
**Filters Applied:**
- Impact Level: High only
- Country: US
- Events shown: [X] of [Y] total events in date range
```

**输出格式：**
- 主要输出形式：保存到磁盘的 Markdown 文件
- 文件名格式：`economic_calendar_[开始日期]_到_[结束日期].md`
- 也在聊天中向用户显示报告摘要

## 输出格式规范

**文件命名规则：**
```
economic_calendar_2025-01-01_to_2025-01-31.md
economic_calendar_2025-01-15_to_2025-01-21.md  (weekly)
economic_calendar_high_impact_2025-01.md  (with filters)
```

**Markdown 结构要求：**
1. **时间顺序：** 按日期和时间排序（最早的事件排在最前面）
2. **影响程度标记：** 使用 (High Impact)、(Medium Impact)、(Low Impact) 标签
3. **时区说明：** 始终注明 UTC，并为美国事件提供 ET/PT 转换
4. **数据完整性：** 包含所有可用字段（过去的数据显示为 “N/A” 或 “无估计值”）
5. **空值处理：** 对空值显示 “N/A” 或 “无估计”
6. **影响评估：** 每个高/中等影响力的事件都必须附有市场影响分析

**表格格式选项（用于展示大量事件）：**
```markdown
| Date/Time (UTC) | Event | Country | Impact | Previous | Estimate | Assessment |
|-----------------|-------|---------|--------|----------|----------|------------|
| 01-15 14:30 | CPI YoY | US | High | 2.6% | 2.7% | Core inflation metric |
```

**语言：** 所有报告均使用英语

## 资源

**Python 脚本：**
- `scripts/get_economic_calendar.py`：主要的 API 查询脚本，具有命令行界面

**参考文档：**
- `references/fmp_api_documentation.md`：完整的 FMP 经济日历 API 参考文档
  - 认证和 API 密钥管理
  - 请求参数和日期格式
  - 响应字段定义
  - 请求频率限制和错误处理
  - 缓存和效率的最佳实践

**API 详情：**
- 端点：`https://financialmodelingprep.com/api/v3/economic_calendar`
- 认证：需要 API 密钥（免费 tier：每日 250 次请求）
- 最大日期范围：每次请求 90 天
- 响应格式：事件对象的 JSON 数组
- 请求频率限制：每秒 5 次（免费 tier）
- 事件覆盖范围：主要经济体（美国、欧盟、英国、日本、中国、加拿大、澳大利亚、瑞士）
- 事件类别：货币政策、就业数据、通胀数据、GDP 数据、贸易数据、房地产数据、调查数据
- 更新频率：实时更新（事件按计划添加/更新）
- 历史数据：提供过去事件的实际数据

**使用提示：**
1. 缓存结果以减少 API 调用次数（一旦事件确定后，通常不会更改）
- 为最佳效率，建议查询 7-30 天内的数据
- 不要查询超过 6 个月后的数据（数据较少，可能具有不确定性）
- 每天刷新缓存以获取即将发生的事件
- 对于实时事件监控，建议使用较短的时间范围（1-7 天）
- 错误处理：**
  - API 密钥错误：提供获取免费密钥的指导
  - 请求频率限制：采用指数退避策略重试
  - 网络故障：如有缓存数据，则优雅降级
  - 日期格式错误：提供正确的格式提示