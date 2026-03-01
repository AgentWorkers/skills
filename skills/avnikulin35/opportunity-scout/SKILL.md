---
name: opportunity-scout
description: 通过在 Twitter、网页、Reddit 和 Product Hunt 上搜索未被满足的需求和痛点，可以在任何细分市场中找到有利可图的商业机会。对每个机会从“需求（Demand）”、“竞争情况（Competition）”、“可行性（Feasibility）”和“盈利模式（Monetization）”四个方面进行评分（每个方面 1-5 分，总分最高 20 分），生成一份包含可操作建议的排名报告。该工具可用于寻找商业创意、市场机会或解决“我应该开发什么产品”这类问题。同时，它也可用于市场研究、细分市场分析、机会挖掘以及新产品的竞争分析等场景。
---
# AI 机会探索器 (AI Opportunity Scout)

发现人们的需求 → 评估你是否能够满足这些需求 → 决定这个项目是否值得开发。

## 快速入门

当用户指定了一个具体的领域（例如：“AI 代理”、“加密货币交易”、“SaaS 工具”）时：

1. 运行下面的探索流程。
2. 使用 `scripts/scout.py` 对每个发现的结果进行评分。
3. 提交排名后的报告。

## 探索流程

### 第一步：收集数据（使用内置工具）

根据用户指定的领域，执行以下搜索操作：

**Twitter**（通过 exec 命令）：
```bash
bird search "[niche] need OR wish OR looking for OR frustrated" --limit 20
bird search "[niche] tool OR plugin OR solution" --limit 20
```

**网络**（通过 web_search 工具）：
- `"[领域] 2026 年的痛点"`
- `"[领域] 人们需要的工具"`
- `"site:reddit.com [领域] 需要/希望/正在寻找..."`
- `"site:producthunt.com [领域]"`

**ClawHub**（如果领域与 AI/代理相关）：
```bash
clawdhub search "[niche keyword]"
```

### 第二步：识别机会

从原始数据中筛选出具有潜力的机会。每个机会都代表一个尚未被满足的具体需求，这些需求有可能成为产品开发的起点。注意以下线索：

- 反复出现的问题或请求（同一问题被提及 3 次以上）；
- 现有产品与用户需求之间的差距；
- 现有解决方案存在的问题（价格过高、过于复杂或缺少关键功能）；
- 尚无成熟解决方案的新兴趋势。

### 第三步：对每个机会进行评分

运行评分脚本：
```bash
python3 scripts/scout.py score --input opportunities.json --output report.md
```

或者根据以下标准手动评分（每个标准 1-5 分）：

| 标准 | 5（最佳） | 3（中等） | 1（最差） |
|---------|---------|---------|---------|
| **需求** | 50 人以上提出需求 | 10-20 次提及 | 1-2 次提及 |
| **竞争情况** | 无解决方案 | 有解决方案但存在缺陷 | 市场已饱和 |
| **可行性** | 1-2 天内可以开发出 MVP | 1-2 周 | 需要数月时间 |
| **盈利潜力** | 有人愿意为类似产品付费 | 可以采用免费模式 | 难以盈利 |

**评分总分解读**：
- **16-20 分**：🔥 立即开发！
- **12-15 分**：👍 有很好的机会，值得尝试；
- **8-11 分**：🤔 需要观察，暂无紧迫性；
- **4-7 分**：❌ 可以跳过。

详细的评分示例请参见 `references/scoring-guide.md`。

### 第四步：生成报告

将搜索结果格式化为报告：
```
# Opportunity Scout: [Niche] — [Date]

## 🏆 Top 3 Opportunities

### 1. [Name] (Score: X/20)
- **Problem:** [What people need]
- **Evidence:** [Links/quotes from research]
- **Scores:** D:[X] C:[X] F:[X] M:[X]
- **Action:** [What to build, how long, how to monetize]

### 2. [Name] (Score: X/20)
...

## All Findings

| # | Opportunity | D | C | F | M | Total | Verdict |
|---|------------|---|---|---|---|-------|---------|
| 1 | ... | | | | | | |

## Recommendation
[Which to build first and why]
```

## 深度探索模式

- `--depth quick`：2 次 Twitter 搜索 + 2 次网络搜索。快速扫描，约 2 分钟完成。
- `--depth normal`：4 次 Twitter 搜索 + 4 次网络搜索 + 使用 ClawHub。标准模式，约 5 分钟完成。
- `--depth deep`：6 次 Twitter 搜索 + 8 次网络搜索 + 使用 ClawHub + 深入分析 Reddit 上的相关内容。全面扫描，约 10 分钟完成。

## 提示：

- 重点关注那些人们愿意付费解决的问题，而不仅仅是他们抱怨的问题；
- “我希望……” 或 “有人知道……的工具吗？” 这类表述是强烈的需求信号；
- 检查现有解决方案是否已被弃用或维护不当——这样的解决方案容易被替代；
- 加密货币/金融领域的机会虽然盈利潜力高，但竞争也激烈；
- 更具体的领域定位（例如：“牙医用的 AI 代理”通常比 “通用 AI 代理” 更有开发价值。