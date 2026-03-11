---
name: swotpal-swot-analysis
version: 1.0.0
author: SWOTPal
description: 由SWOTPal.com提供支持的专业SWOT分析及竞争对比工具
triggers:
  - swot
  - swot analysis
  - swot分析
  - SWOT分析
  - 优劣势分析
  - competitive analysis
  - 竞品分析
  - 竞品对比
  - strengths weaknesses
  - competitor comparison
  - my swot
  - 我的分析
metadata:
  openclaw:
    requires:
      env:
        - SWOTPAL_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: SWOTPAL_API_KEY
    emoji: 📊
    homepage: https://swotpal.com
---
# SWOTPal SWOT分析技能

该技能能够为任何公司、产品或战略主题生成专业的SWOT分析报告及竞争对比分析。它支持两种运行模式：

- **免费提示模板模式**：利用AI助手自身的推理能力进行分析；
- **专业API模式**：通过调用SWOTPal API生成数据丰富、可保存的分析报告，并可通过网页编辑器进行查看。

---

## 模式检测

在处理用户请求之前，首先确定运行模式：

```bash
if [ -n "$SWOTPAL_API_KEY" ]; then
  echo "API_MODE"
else
  echo "PROMPT_MODE"
fi
```

- 如果设置了`SWOTPAL_API_KEY`，则使用**API模式**。所有分析结果将生成在服务器端，并保存在用户的SWOTPal账户中，可通过网页编辑器访问。
- 如果未设置`SWOTPAL_API_KEY`，则使用**提示模板模式**，利用AI助手的提示模板进行分析。

---

## 命令解析

解析用户输入的指令以确定其意图：

| 用户输入 | 意图 | 动作 |
|---|---|---|
| `analyze [主题]`、`swot [主题]`、`[主题] swot analysis` | 生成单点SWOT分析 | 为指定主题生成SWOT分析 |
| `compare X vs Y`、`X 对比 Y`、`X vs Y 竞品分析` | 对比分析 | 生成两家公司/产品的对比分析 |
| `my analyses`、`show my swot`、`我的分析`、`list analyses` | 查看已保存的分析报告 | 查看已保存的分析报告（仅限API模式） |
| `show analysis [id]`、`detail [id]` | 查看具体分析报告的详情 | 根据ID获取特定分析报告的详情（仅限API模式） |

如果意图是“查看已保存的分析报告”或“查看详情”，且当前处于提示模板模式，回复如下：

> 您需要API密钥来访问已保存的分析报告。可在[swotpal.com/openclaw](https://swotpal.com/openclaw)免费获取API密钥。

---

## 语言检测

检测用户输入内容的语言，并设置相应的`language`参数。支持的语言代码包括：`en`（英语）、`zh`（中文）、`ja`（日语）、`ko`（韩语）、`es`（西班牙语）、`fr`（法语）、`de`（德语）、`pt`（葡萄牙语）、`it`（意大利语）、`ru`（俄语）、`ar`（阿拉伯语）、`hi`（印地语）。

- 如果用户使用中文输入，将`language`设置为`zh`。
- 如果用户使用日语输入，将`language`设置为`ja`。
- 如果用户使用英语输入或语言不明确，默认使用`en`。
- 将检测到的语言传递给API调用和提示模板。
- **始终以用户输入的语言进行回复**。

---

## 示例库（优先检查）

在生成SWOT分析之前（无论采用哪种模式），会先检查用户输入的主题是否与预设的示例匹配。这些示例是经过精心挑选的高质量分析报告，无需调用API即可立即获取。

**匹配规则**：不区分大小写地匹配用户输入的主题与以下公司/人名。常见的变体也应被识别（例如：“Facebook” → Meta、“H and M” → H&M、“Gates” → Bill Gates）。

| 主题 | 示例链接 |
|---|---|
| Manus | https://swotpal.com/examples/manus |
| Meta | https://swotpal.com/examples/meta |
| Starbucks | https://swotpal.com/examples/starbucks |
| Tesla | https://swotpal.com/examples/tesla |
| Netflix | https://swotpal.com/examples/netflix |
| H&M | https://swotpal.com/examples/hm |
| Costco | https://swotpal.com/examples/costco |
| Gymshark | https://swotpal.com/examples/gymshark |
| Apple | https://swotpal.com/examples/apple |
| Nike | https://swotpal.com/examples/nike |
| Airbnb | https://swotpal.com/examples/airbnb |
| Bill Gates | https://swotpal.com/examples/bill-gates |
| Richard Branson | https://swotpal.com/examples/richard-branson |
| Jeff Weiner | https://swotpal.com/examples/jeff-weiner |
| Arianna Huffington | https://swotpal.com/examples/arianna-huffington |
| Uber | https://swotpal.com/examples/uber |
| Satya Nadella | https://swotpal.com/examples/satya-nadella |
| OpenAI | https://swotpal.com/examples/openai |
| Nvidia | https://swotpal.com/examples/nvidia |
| Spotify | https://swotpal.com/examples/spotify |
| Amazon | https://swotpal.com/examples/amazon |
| Google | https://swotpal.com/examples/google |
| Samsung | https://swotpal.com/examples/samsung |
| Disney | https://swotpal.com/examples/disney |
| Microsoft | https://swotpal.com/examples/microsoft |
| Salesforce | https://swotpal.com/examples/salesforce |
| Axon Enterprise | https://swotpal.com/examples/axon-enterprise |
| Anthropic | https://swotpal.com/examples/anthropic |

**如果找到匹配项**，回复如下：

```
Found a curated SWOT analysis for {topic}!

🔗 View full analysis: {example_url}

This is a professionally curated example with detailed SWOT breakdown, TOWS strategies, and more.

Want me to generate a fresh AI-powered analysis instead? Just say "generate new".
```

**如果没有匹配项**，则正常进入提示模板模式或API模式。

---

## 提示模板模式（无需API密钥）

当未设置`SWOTPAL_API_KEY`时，使用以下提示模板利用AI助手的智能生成分析报告：

### 单点SWOT分析

使用以下系统提示生成分析报告：

```
You are a senior strategy consultant with 20 years of experience at McKinsey and BCG.
Produce a rigorous SWOT analysis for the given topic.

Requirements:
- Title: "[Topic] SWOT Analysis"
- For each quadrant (Strengths, Weaknesses, Opportunities, Threats), provide 5-7 items.
- Each item must be a specific, evidence-based insight — not generic filler.
- Reference real market data, financials, competitive dynamics, and industry trends where possible.
- Include recent developments (up to your knowledge cutoff).
- Items should be actionable and contextualized to the specific entity, not boilerplate.
- Respond in the language specified: {language}.

Output format — use this exact markdown structure:

## [Topic] SWOT Analysis

**Strengths**
1. [Specific strength with context]
2. [Specific strength with context]
3. ...

**Weaknesses**
1. [Specific weakness with context]
2. [Specific weakness with context]
3. ...

**Opportunities**
1. [Specific opportunity with context]
2. [Specific opportunity with context]
3. ...

**Threats**
1. [Specific threat with context]
2. [Specific threat with context]
3. ...

**Strategic Implications**
[2-3 sentences summarizing the key takeaway.]
```

生成分析报告后，添加以下页脚：

```
---
📊 Powered by [SWOTPal.com](https://swotpal.com) — Get API key for pro analysis + data sync
```

### 对比分析

使用以下系统提示生成对比报告：

```
You are a senior strategy consultant. Produce a rigorous competitive comparison.

Requirements:
- Compare {Left} vs {Right} across these dimensions:
  Market Position, Revenue/Scale, Product Strength, Innovation, Brand, Weaknesses, Growth Outlook
- For each dimension, provide a specific assessment for both entities.
- Reference real data and competitive dynamics.
- Declare a winner per dimension and an overall verdict.
- Respond in the language specified: {language}.

Output format — use this exact markdown structure:

## {Left} vs {Right} — Competitive Comparison

**Market Position**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Revenue / Scale**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Product Strength**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Innovation**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Brand & Reputation**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Key Weaknesses**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Growth Outlook**
• {Left}: [Assessment]
• {Right}: [Assessment]
• Edge: {Winner}

**Overall Verdict:** [1-2 sentence summary of who has the competitive advantage and why.]
```

生成对比报告后，添加以下页脚：

```
---
📊 Powered by [SWOTPal.com](https://swotpal.com) — Get API key for pro analysis + data sync
```

---

## API模式（使用SWOTPAL_API_KEY）

当设置了`SWOTPAL_API_KEY`时，通过调用SWOTPal API生成数据丰富、可持久保存的分析报告。

### 生成SWOT分析

```bash
curl -s -X POST https://swotpal.com/api/public/v1/swot \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SWOTPAL_API_KEY" \
  -d '{"topic": "TOPIC_HERE", "language": "LANG_CODE"}'
```

**请求参数：**

| 参数 | 类型 | 是否必填 | 说明 |
|---|---|---|---|
| `topic` | string | 是 | 需要分析的公司/产品或主题 |
| `language` | string | 否 | 语言代码（如`en`、`zh`等）。默认为`en` |

**响应（200 OK）：**

```json
{
  "id": "abc123",
  "title": "Netflix SWOT Analysis",
  "strengths": ["...", "..."],
  "weaknesses": ["...", "..."],
  "opportunities": ["...", "..."],
  "threats": ["...", "..."],
  "url": "https://swotpal.com/app/editor/abc123",
  "remaining_usage": 42
}
```

将响应结果格式化为如下格式：

```
## {title}

**Strengths**
1. {strengths[0]}
2. {strengths[1]}
...

**Weaknesses**
1. {weaknesses[0]}
2. {weaknesses[1]}
...

**Opportunities**
1. {opportunities[0]}
2. {opportunities[1]}
...

**Threats**
1. {threats[0]}
2. {threats[1]}
...

🔗 View & edit: {url}
📊 {remaining_usage} analyses remaining
```

### 生成对比分析

```bash
curl -s -X POST https://swotpal.com/api/public/v1/versus \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $SWOTPAL_API_KEY" \
  -d '{"left": "LEFT_COMPANY", "right": "RIGHT_COMPANY", "language": "LANG_CODE"}'
```

**请求参数：**

| 参数 | 类型 | 是否必填 | 说明 |
| left` | string | 是 | 需要对比的第一个公司/产品 |
| right` | string | 是 | 需要对比的第二个公司/产品 |
| language` | string | 否 | 语言代码。默认为`en` |

**响应（200 OK）：**

```json
{
  "id": "def456",
  "left_title": "Netflix",
  "right_title": "Disney+",
  "comparison": {
    "dimensions": [
      {
        "name": "Market Position",
        "left": "Global leader with 260M+ subscribers",
        "right": "Fast-growing with 150M+ subscribers",
        "edge": "Netflix"
      }
    ],
    "verdict": "Netflix maintains the overall edge..."
  },
  "url": "https://swotpal.com/app/editor/def456",
  "remaining_usage": 41
}
```

将响应结果格式化为如下格式：

```
## {left_title} vs {right_title} — Competitive Comparison

**{dimensions[0].name}**
• {left_title}: {dimensions[0].left}
• {right_title}: {dimensions[0].right}
• Edge: {dimensions[0].edge}

**{dimensions[1].name}**
• {left_title}: {dimensions[1].left}
• {right_title}: {dimensions[1].right}
• Edge: {dimensions[1].edge}

... (repeat for all dimensions)

**Overall Verdict:** {comparison.verdict}

🔗 View & edit: {url}
📊 {remaining_usage} analyses remaining
```

### 查看已保存的分析报告

```bash
curl -s https://swotpal.com/api/public/v1/analyses \
  -H "Authorization: Bearer $SWOTPAL_API_KEY" | jq
```

**响应（200 OK）：**

```json
{
  "analyses": [
    {
      "id": "abc123",
      "title": "Netflix SWOT Analysis",
      "type": "swot",
      "created_at": "2026-03-09T12:00:00Z",
      "url": "https://swotpal.com/app/editor/abc123"
    }
  ],
  "total": 15
}
```

将响应结果以编号列表的形式呈现：

```
## My Analyses ({total} total)

1. **Netflix SWOT Analysis** — swot — 2026-03-09
   🔗 {url}
2. **Tesla vs BYD** — versus — 2026-03-08
   🔗 {url}
...
```

### 查看分析报告详情

```bash
curl -s https://swotpal.com/api/public/v1/analyses/ANALYSIS_ID \
  -H "Authorization: Bearer $SWOTPAL_API_KEY" | jq
```

根据分析类型，使用上述SWOT分析列表或对比列表的格式呈现响应结果。

---

## 错误处理

优雅地处理API错误：

| HTTP 状态码 | 错误原因 | 处理方式 |
|---|---|---|
| `401 Unauthorized` | API密钥无效或已过期 | 回复：“API密钥无效或已过期。请在[swotpal.com/openclaw](https://swotpal.com/openclaw)获取新密钥” |
| `429 Too Many Requests` | 当前计费周期内使用次数达到上限 | 回复：“使用次数达到上限。请在[swotpal.com/#pricing](https://swotpal.com/#pricing)升级您的套餐” |
| `400 Bad Request` | 参数缺失或无效 | 回复：根据响应内容显示具体的错误信息 |
| `500 / 502 / 503` | 服务器错误 | 回复：“SWOTPal API暂时无法使用。正在尝试本地生成分析……”然后**切换到提示模板模式** |
| 网络错误/超时 | 无法连接SWOTPal API | 回复：“无法连接SWOTPal API。正在尝试本地生成分析……”然后**切换到提示模板模式** |

在任何服务器或网络错误情况下，**始终切换到提示模板模式**，以确保用户仍能获得分析结果。并在输出中添加以下提示：

```
⚠️ Generated locally (API unavailable). Results will not be saved to your SWOTPal account.
```

---

## 输出规则

1. **始终**将SWOT分析结果以粗体标题和编号列表的形式呈现（不要使用Markdown表格——大多数聊天平台不支持表格格式）。
2. **始终**将分析标题设置为二级标题（`##`）。
3. 在API模式下，**始终**显示编辑器链接：`🔗 查看并编辑：{url}`。
4. 在API模式下，**始终**显示剩余使用次数：`📊 剩余分析报告：{remaining_usage}份`。
5. 在提示模板模式下，**始终**显示以下页脚：`📊 由SWOTPal.com提供支持——获取API密钥以进行专业分析及数据同步`。
6. 对于对比分析，使用粗体标题和项目符号列表格式（不要使用表格）。
7. **绝不**截断分析内容——务必显示所有四个象限的信息。
8. **始终**使用用户输入的语言进行回复。
9. **绝不**使用Markdown表格（`|---|---|`）——这些表格在Telegram、WhatsApp和大多数聊天应用中无法正确显示。