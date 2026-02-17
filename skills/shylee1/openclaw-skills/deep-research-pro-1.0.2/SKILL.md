---
name: deep-research-pro
version: 1.0.0
description: "多源深度研究代理：能够搜索网络、整合研究结果，并生成带有引用信息的报告。无需使用API密钥。"
homepage: https://github.com/paragshah/deep-research-pro
metadata: {"clawdbot":{"emoji":"🔬","category":"research"}}
---

# 深度研究专业技能 🔬

这是一项强大且独立的深度研究工具，能够从多个网络来源生成详尽且带有引用信息的报告。无需使用任何付费API，仅依赖DuckDuckGo搜索引擎。

## 工作原理

当用户请求对某个主题进行研究时，请按照以下流程操作：

### 第1步：明确研究目标（30秒）

提出1-2个简短的澄清问题：
- “您的目的是什么？是学习、做决策，还是撰写文章？”
- “您希望从哪个具体角度或深度进行研究？”

如果用户回答“只是想研究一下”，则可以直接使用预设的默认设置继续操作。

### 第2步：制定研究计划（在搜索前先思考）

将研究主题分解为3-5个子问题。例如：
- 主题：“人工智能对医疗行业的影响”
  - 当前人工智能在医疗领域的应用有哪些？
  - 已经测量到了哪些临床成果？
  - 面临哪些监管挑战？
  - 哪些公司在这一领域处于领先地位？
  - 市场规模和增长趋势如何？

### 第3步：执行多源搜索

对于每个子问题，运行DDG搜索脚本：

**搜索策略：**
- 为每个子问题使用2-3种不同的关键词组合
- 结合网络搜索和新闻搜索
- 力求获取15-30个独特的来源
- 优先选择学术机构、官方发布的内容、可靠的新闻来源 > 博客 > 论坛

### 第4步：深入阅读关键资料

对于最有价值的网站，获取完整的内容：

```bash
curl -sL "<url>" | python3 -c "
import sys, re
html = sys.stdin.read()
# Strip tags, get text
text = re.sub('<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text).strip()
print(text[:5000])
"
```

仔细阅读3-5个关键来源的内容，不要仅依赖搜索结果中的片段。

### 第5步：整合信息并撰写报告

按照以下结构撰写报告：

```markdown
# [Topic]: Deep Research Report
*Generated: [date] | Sources: [N] | Confidence: [High/Medium/Low]*

## Executive Summary
[3-5 sentence overview of key findings]

## 1. [First Major Theme]
[Findings with inline citations]
- Key point ([Source Name](url))
- Supporting data ([Source Name](url))

## 2. [Second Major Theme]
...

## 3. [Third Major Theme]
...

## Key Takeaways
- [Actionable insight 1]
- [Actionable insight 2]
- [Actionable insight 3]

## Sources
1. [Title](url) — [one-line summary]
2. ...

## Methodology
Searched [N] queries across web and news. Analyzed [M] sources.
Sub-questions investigated: [list]
```

### 第6步：保存和交付结果

保存完整的报告：
```bash
mkdir -p ~/clawd/research/[slug]
# Write report to ~/clawd/research/[slug]/report.md
```

然后按照以下方式交付结果：
- **简短的主题**：将完整报告发布在聊天界面
- **较长的报告**：发布执行摘要和关键要点，并提供完整报告的文件链接

## 质量要求

1. **所有观点都必须有来源支持。** 不允许使用未经证实的信息。
2. **进行交叉验证。** 如果某个观点仅来自一个来源，请标注为“未经验证”。
3. **时效性很重要。** 优先选择过去12个月内的资料。
4. **如实说明不足之处。** 如果某个子问题没有找到可靠的信息，应如实说明。
5. **避免主观臆断。** 如果不清楚某个事实，应注明“数据不足”。

## 使用示例

```
"Research the current state of nuclear fusion energy"
"Deep dive into Rust vs Go for backend services in 2026"
"Research the best strategies for bootstrapping a SaaS business"
"What's happening with the US housing market right now?"
```

## 作为子代理的使用方法

当以子代理的形式运行时，需要提供完整的研究请求和相关背景信息：

```
sessions_spawn(
  task: "Run deep research on [TOPIC]. Follow the deep-research-pro SKILL.md workflow.
  Read /home/clawdbot/clawd/skills/deep-research-pro/SKILL.md first.
  Goal: [user's goal]
  Specific angles: [any specifics]
  Save report to ~/clawd/research/[slug]/report.md
  When done, wake the main session with key findings.",
  label: "research-[slug]",
  model: "opus"
)
```

## 所需资源

- DDG搜索脚本：`/home/clawdbot/clawd/skills/ddg-search/scripts/ddg`
- `curl`（用于获取网页内容）
- 无需API密钥！