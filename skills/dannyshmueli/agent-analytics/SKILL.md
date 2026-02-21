---
name: agent-analytics
description: "开源的、以代理（agent）为中心的无头（headless）分析平台，内置A/B测试功能。可通过API为任何网站添加跟踪功能、运行实验、查看结果并优化转化率。该平台还提供了一套增长策略（growth playbook），帮助您的代理了解如何实现业务增长，而不仅仅是知道需要跟踪哪些数据。"
version: 2.6.0
author: dannyshmueli
repository: https://github.com/Agent-Analytics/agent-analytics-cli
homepage: https://agentanalytics.sh
tags:
  - analytics
  - tracking
  - web
  - events
metadata: {"openclaw":{"requires":{"env":["AGENT_ANALYTICS_API_KEY"],"anyBins":["npx"]},"primaryEnv":"AGENT_ANALYTICS_API_KEY"}}
---
# 代理分析 — 为任何网站添加跟踪功能

您可以使用 Agent Analytics 来添加分析跟踪功能。Agent Analytics 是一个为开发人员设计的轻量级平台，适用于那些发布大量项目并希望其 AI 代理能够监控这些项目的团队。

## 设计理念

Agent Analytics 并非 Mixpanel。不要跟踪所有数据，只需跟踪那些能够回答以下问题的信息：“这个项目是否还活跃并正在发展？”对于一个典型的网站来说，除了自动记录的页面浏览量外，最多只需要跟踪 3-5 个自定义事件。

## 首次设置

**获取 API 密钥：** 在 [agentanalytics.sh](https://agentanalytics.sh) 注册，并从仪表板上生成一个密钥。或者，您也可以从 [GitHub](https://github.com/Agent-Analytics/agent-analytics) 下载开源版本进行自托管。

如果项目尚未启用跟踪功能：

```bash
# 1. Login (one time — uses your API key)
npx @agent-analytics/cli login --token aak_YOUR_API_KEY

# 2. Create the project (returns a project write token)
npx @agent-analytics/cli create my-site --domain https://mysite.com

# 3. Add the snippet (Step 1 below) using the returned token
# 4. Deploy, click around, verify:
npx @agent-analytics/cli events my-site
```

`create` 命令会返回一个 **项目写入令牌**（project write token）——请在下面的代码片段中使用它作为 `data-token`。这个令牌与您的 API 密钥（用于读取/查询数据）是分开的。

## 第一步：添加跟踪代码片段

在 `</body>` 之前添加以下代码：

```html
<script src="https://api.agentanalytics.sh/tracker.js"
  data-project="PROJECT_NAME"
  data-token="PROJECT_WRITE_TOKEN"></script>
```

这段代码会自动跟踪包含路径（path）、引用来源（referrer）、浏览器类型（browser）、操作系统（OS）、设备类型（device）、屏幕尺寸（screen size）和 UTM 参数的 `page_view` 事件。您无需手动添加自定义的 `page_view` 事件。

> **安全提示：** 项目写入令牌（`aat_*`）是公开且安全的，可以嵌入到客户端 HTML 中。它只能将事件写入到特定的项目中，具有速率限制（免费用户每分钟 10 次请求，付费用户每分钟 1,000 次请求），并且可以从仪表板上撤销。它无法读取数据——读取数据需要使用单独的 API 密钥（`aak_*`）。

## 第二步：查看已有的事件（对于已有的项目）

如果已经启用了跟踪功能，请检查当前使用了哪些事件和属性键，以确保名称一致：

```bash
npx @agent-analytics/cli properties-received PROJECT_NAME
```

这段代码会显示每种事件类型使用的属性键（例如 `cta_click → id`、`signup → method`）。在添加新事件之前，请确保名称与现有事件一致。

## 第三步：为重要操作添加自定义事件

在需要跟踪的用户交互元素上使用 `onclick` 事件处理器：

```html
<a href="..." onclick="window.aa?.track('EVENT_NAME', {id: 'ELEMENT_ID'})">
```

`?.` 运算符可以确保在跟踪器尚未加载时不会引发错误。

### 80% 的 SaaS 网站都需要的标准事件

根据实际需求选择相应的事件。大多数网站需要 2-4 个标准事件：

| 事件 | 触发条件 | 属性 |
|-------|-------------|------------|
| `cta_click` | 用户点击呼叫行动按钮 | `id`（点击的按钮） |
| `signup` | 用户创建账户 | `method`（注册方式：github/google/email） |
| `login` | 用户返回并登录 | `method` |
| `feature_used` | 用户使用了某个核心功能 | `feature`（使用的是哪个功能） |
| `checkout` | 用户开始支付流程 | `plan`（购买计划） |
| `error` | 发生了明显的错误 | `message`, `page` |

### 应该跟踪哪些作为 `cta_click` 的事件

只有那些表明用户有转化意图的按钮才需要跟踪：
- “开始使用”/“注册”/“免费试用”按钮
- “升级”/“购买”/价格相关的内容
- 主导航链接到注册页面或仪表板
- “在 GitHub 上查看”/“星标”（针对开源项目）

### 不应该跟踪什么
- 所有的链接或按钮（信息量太大，容易造成干扰）
- 滚动深度（无法直接操作）
- 表单字段的交互（过于详细）
- 底部链接（信号较弱）

### 属性命名规则
- 使用蛇形命名法（snake_case）：例如 `hero_get_started` 而不是 `heroGetStarted`
- `id` 属性用于唯一标识元素：简洁且具有描述性
- 将 ID 命名为 `section_action`，例如 `heroSignup`、`pricing_pro`、`nav_dashboard`
- 不需要对 `page_view` 已经捕获的数据进行编码

## 第二步（进阶）：运行 A/B 实验（针对付费用户）

A/B 实验可以帮助您测试页面元素的哪个变体更有效。整个实验过程由 API 驱动，无需使用仪表板界面。

### 创建实验

```bash
npx @agent-analytics/cli experiments create my-site \
  --name signup_cta --variants control,new_cta --goal signup
```

或者通过 API 进行操作：

```bash
curl -X POST "https://api.agentanalytics.sh/experiments" \
  -H "X-API-Key: $AGENT_ANALYTICS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project":"my-site","name":"signup_cta","variants":["control","new_cta"],"goal_event":"signup"}'
```

### 实现变体（推荐使用声明式方法）

最简单的方法是使用 HTML 属性。无需编写自定义 JavaScript 代码。

**1. 在 `<head>` 标签中添加防闪烁代码**，以防止控制内容闪烁：

```html
<style>.aa-loading [data-aa-experiment]{visibility:hidden!important}</style>
<script>document.documentElement.classList.add('aa-loading');
setTimeout(function(){document.documentElement.classList.remove('aa-loading')},3000)</script>
```

**2. 用 `data-aa-experiment` 标记需要测试的元素，并通过 `data-aa-variant-{key}` 提供不同版本的元素内容**：

```html
<!-- Original content = control. Variant "new_cta" swaps the text. -->
<h1 data-aa-experiment="signup_cta" data-aa-variant-new_cta="Start Free Trial">
  Sign Up
</h1>

<!-- Multiple elements in the same experiment get the same variant -->
<h1 data-aa-experiment="hero_test" data-aa-variant-b="New Headline">Old Headline</h1>
<p data-aa-experiment="hero_test" data-aa-variant-b="New subtext">Old subtext</p>

<!-- Multi-variant -->
<h1 data-aa-experiment="cta_test"
    data-aa-variant-b="Try it free"
    data-aa-variant-c="Get started now">
  Sign up today
</h1>
```

关键点：
- 原始元素内容是测试对象，因此不需要添加额外的属性
- 变体键使用小写，因为 HTML 属性不区分大小写
- 防闪烁功能只会隐藏参与实验的元素（而不会影响整个页面），并且有 3 秒的延迟效果
- `tracker.js` 在应用变体后会移除 `aa-loading` 类
- 每个会话都会自动记录一次 `exposure` 事件
- 如需正常跟踪目标事件，请使用 `window.aa?.track('signup', {method: 'github'})`

### 实现变体（针对复杂情况，使用编程方式）

对于无法通过简单文本替换来展示的动态内容或逻辑，可以使用 JavaScript API：

```js
var variant = window.aa?.experiment('signup_cta', ['control', 'new_cta']);

if (variant === 'new_cta') {
  document.querySelector('.cta').textContent = 'Start Free Trial';
} else {
  document.querySelector('.cta').textContent = 'Sign Up';
}
```

关键点：
- `aa.experiment()` 确保每个用户总是看到相同的变体
- 即使配置端点尚未加载，内联的 `['control', 'new_cta']` 也能正常工作

### 检查实验结果

```bash
npx @agent-analytics/cli experiments get exp_abc123
```

实验结果会返回贝叶斯概率 `probability_best`、效果提升量 `lift` 和推荐方案 `recommendation`。系统通常需要每个变体大约 100 次展示才能得出有意义的结果。

### 管理实验

```bash
# Pause (stops assigning new users)
npx @agent-analytics/cli experiments pause exp_abc123

# Resume
npx @agent-analytics/cli experiments resume exp_abc123

# Complete with a winner
npx @agent-analytics/cli experiments complete exp_abc123 --winner new_cta

# Delete
npx @agent-analytics/cli experiments delete exp_abc123
```

### 最佳实践
- 使用蛇形命名法为实验命名：例如 `signup_cta`、`pricing_layout`、`hero_copy`
- 除非流量非常大，否则至少使用两个变体（A/B 测试）
- 设置一个明确的 `goal_event`，将其与业务目标对应起来（例如 `signup`、`purchase`，而不是简单的 `page_view`）
- 在确定最佳方案之前，让实验持续运行，直到 `sufficient_data: true`
- 实验完成后，使用 `experiments complete <id> --winner new_cta` 完成实验

## 第三步：立即进行测试

添加跟踪功能后，立即验证其是否正常工作：

```bash
# Option A: Browser console on your site:
window.aa.track('test_event', {source: 'manual_test'})

# Option B: Click around, then check:
npx @agent-analytics/cli events PROJECT_NAME

# Events appear within seconds.
```

## 数据查询

### 命令行参考

```bash
# List all your projects (do this first)
npx @agent-analytics/cli projects

# Aggregated stats for a project
npx @agent-analytics/cli stats my-site --days 7

# Recent events (raw log)
npx @agent-analytics/cli events my-site --days 30 --limit 50

# What property keys exist per event type?
npx @agent-analytics/cli properties-received my-site --since 2025-01-01

# Period-over-period comparison (this week vs last week)
npx @agent-analytics/cli insights my-site --period 7d

# Top pages, referrers, UTM sources (any property key)
npx @agent-analytics/cli breakdown my-site --property path --event page_view --limit 10

# Landing page performance
npx @agent-analytics/cli pages my-site --type entry

# Session engagement histogram
npx @agent-analytics/cli sessions-dist my-site

# Traffic patterns by day & hour
npx @agent-analytics/cli heatmap my-site

# A/B experiments (pro only)
npx @agent-analytics/cli experiments list my-site
npx @agent-analytics/cli experiments create my-site --name signup_cta --variants control,new_cta --goal signup
npx @agent-analytics/cli experiments get exp_abc123
npx @agent-analytics/cli experiments complete exp_abc123 --winner new_cta
```

**常用参数：**
- `--days <N>` — 回顾时间窗口（默认值：7 天；适用于 `stats` 和 `events`）
- `--limit <N>` — 返回的最大行数（默认值：100 行）
- `--since <date>` — 时间截止日期（仅适用于 `properties-received`）
- `--period <P>` — 对比周期：`1d`、`7d`、`14d`、`30d`、`90d`（仅适用于 `insights`）
- `--property <key>` — 按属性键分组（`breakdown` 需要此参数）
- `--event <name>` — 按事件名称过滤（`breakdown` 需要此参数）
- `--type <T>` — 页面类型：`entry`、`exit`、`both`（仅适用于 `pages`，默认值：`entry`）

### 分析 API 端点

这些端点返回预先计算好的聚合数据——直接使用这些数据，无需在客户端下载原始事件并自行计算。所有请求都需要包含 `X-API-Key` 标头或 `?key=` 参数。

```bash
# Period-over-period comparison (replaces manual 2x /stats calls)
# period: 1d, 7d, 14d, 30d, or 90d
curl "https://api.agentanalytics.sh/insights?project=my-site&period=7d" \
  -H "X-API-Key: $AGENT_ANALYTICS_API_KEY"
# → { metrics: { total_events: { current, previous, change, change_pct }, ... }, trend }

# Property value breakdown (top pages, referrers, UTM sources, etc.)
curl "https://api.agentanalytics.sh/breakdown?project=my-site&property=path&event=page_view&limit=10" \
  -H "X-API-Key: $AGENT_ANALYTICS_API_KEY"
# → { values: [{ value: "/home", count: 523, unique_users: 312 }, ...] }

# Entry & exit page performance
# type: entry, exit, or both
curl "https://api.agentanalytics.sh/pages?project=my-site&type=entry" \
  -H "X-API-Key: $AGENT_ANALYTICS_API_KEY"
# → { entry_pages: [{ page, sessions, bounces, bounce_rate, avg_duration, avg_events }] }

# Session duration distribution (engagement histogram)
curl "https://api.agentanalytics.sh/sessions/distribution?project=my-site" \
  -H "X-API-Key: $AGENT_ANALYTICS_API_KEY"
# → { distribution: [{ bucket: "0s", sessions, pct }, ...], engaged_pct, median_bucket }

# Traffic heatmap (peak hours & busiest days)
curl "https://api.agentanalytics.sh/heatmap?project=my-site&since=2025-01-01" \
  -H "X-API-Key: $AGENT_ANALYTICS_API_KEY"
# → { heatmap: [{ day, day_name, hour, events, users }], peak, busiest_day, busiest_hour }
```

## 根据问题选择合适的端点

根据用户的问题选择相应的 API 端点：

| 用户问题 | 应使用的 API 端点 | 原因 |
|-----------|------|-----|
| “我的网站表现如何？” | `insights` + `breakdown` + `pages` | 一次性获取全面的每周数据 |
| “有人访问我的网站吗？” | `insights --period 7d` | 快速检查网站是否还活跃 |
| “我的热门页面有哪些？” | `breakdown --property path --event page_view` | 按用户唯一性排序的热门页面列表 |
| “我的流量来自哪里？” | `breakdown --property referrer --event page_view` | 查看流量来源 |
| “哪个登录页面效果最好？” | `pages --type entry` | 分析各页面的跳出率和会话深度 |
| “我应该什么时候发布内容？” | `heatmap` | 找出流量较低或高峰时段 |
| “给我所有项目的总结” | 先调用 `projects`，然后针对每个项目调用 `insights` | 查看多项目概览 |

对于任何关于“X 状态如何”的问题，**始终先调用 `insights`——这是最实用的端点**。

## 分析数据，而不仅仅是查询结果

不要仅仅返回原始数字，要对其进行解读。以下是如何将每个 API 端点的返回结果转化为有用的信息。

### `/insights` — 综合指标

API 返回的指标包括 `current`、`previous`、`change`、`change_pct` 和 `trend` 字段。

**解读方法：**
- `change_pct > 10` → 表示“项目正在增长”，应予以正面强调
- `change_pct` 在 -10 到 10 之间 → 表示“稳定”，说明项目表现稳定
- `change_pct < -10` → 表示“项目正在下降”，需要进一步调查
- `bounce_rate` 的变化：比较当前值和上一个周期的值，判断是“改善”还是“恶化”
- `avg_duration`：将毫秒转换为秒：`Math.round(value / 1000)`
- 如果上一个周期的所有值都为 0，则说明“这是新项目，没有之前的数据可供比较”

**示例输出：**
```
This week vs last: 173 events (+22%), 98 users (+18%).
Bounce rate: 87% (up from 82% — getting worse).
Average session: 24s. Trend: growing.
```

### `/breakdown` — 数据排名

API 返回按 `count` 降序排列的 `values: [{ value, count, unique_users }]`。

**解读方法：**
- 只显示前 3-5 个最高值的排名即可，无需显示全部数据
- 同时展示 `unique_users`——来自 2 个用户的 100 个事件与来自 80 个用户的 100 个事件是有区别的
- 使用 `total_with_property / total_events` 来了解数据覆盖范围：例如“155 次页面浏览中有 155 次包含了特定路径”

**示例输出：**
```
Top pages: / (98 views, 75 users), /pricing (33 views, 25 users), /docs (19 views, 4 users).
The /docs page has high repeat visits (19 views, 4 users) — power users.
```

### `/pages` — 登录页面质量

API 返回 `entry_pages: [{ page, sessions, bounces, bounce_rate, avg_duration, avg_events }]`。

**解读方法：**
- `bounce_rate` > 0.7 → 表示“跳出率较高，需要优化页面”
- `bounce_rate` < 0.3 → 表示“登录页面效果良好”
- `avg_duration`：将毫秒转换为秒；如果小于 10 秒则说明页面体验不佳，大于 60 秒则说明体验良好
- `avg_events`：表示每个页面的平均会话时长；1.0 表示用户几乎立即离开页面，大于 3 表示用户参与度较高

**示例输出：**
```
Best landing page: /pricing — 14% bounce, 62s avg session, 4.1 pages/visit.
Worst: /blog/launch — 52% bounce, 18s avg. Consider a stronger CTA above the fold.
```

### `/sessions/distribution` — 用户互动情况

API 返回 `distribution: [{ bucket, sessions, pct }]`、`engagedpct` 和 `median_bucket`。

**解读方法：**
- `engaged pct` 是关键指标，表示会话时长超过 30 秒的用户占比
- `engaged pct` < 10% → 表示“大多数用户立即离开页面，需要优化首屏体验”
- `engaged pct` 在 10% 到 30% 之间表示“用户参与度中等”
- `engaged pct` > 30% 表示“用户参与度较高”
- 如果 80% 以上的会话都属于“0s”区间，说明网站的跳出率较高

**示例输出：**
```
88% of sessions bounce instantly (0s). Only 6% stay longer than 30s.
The few who do engage stay 3-10 minutes — the content works, but first impressions don't.
```

### `/heatmap` — 时间分布

API 返回 `heatmap: [{ day, day_name, hour, events, users }]`、`peak`、`busiest_day`、`busiest_hour`。

**解读方法：**
- `peak` 表示流量最高的时间段，同时注意时间是以 UTC 为单位的
- `busiest_day` 表示“在这个时间发布博客文章或新产品”
- `busiest_hour` 表示“这个时间段用户活跃度最高”
- 通过 `busiest_hour` 可以判断用户是在工作日还是周末访问网站

**示例输出：**
```
Peak: Friday at 11 PM UTC (35 events, 33 users). Busiest day overall: Sunday.
Traffic is heaviest on weekends — your audience browses on personal time.
Deploy on weekday mornings for minimal disruption.
```

### 周度数据汇总（同时调用三个 API）

同时调用 `insights`、`breakdown --property path --event page_view` 和 `pages --type entry`，然后将结果整合到一个响应中：

```
Weekly Report — my-site (Feb 8–15 vs Feb 1–8)
Events: 1,200 (+22% ↑)  Users: 450 (+18% ↑)  Bounce: 42% (improved from 48%)
Top pages: /home (523), /pricing (187), /docs (94)
Best landing: /pricing — 14% bounce, 62s avg. Worst: /blog — 52% bounce.
Trend: Growing.
```

### 多项目概览

首先调用 `projects` 获取所有项目列表，然后对每个项目分别调用 `insights --period 7d`。

```
my-site         142 views (+23% ↑)  12 signups   healthy
side-project     38 views (-8% ↓)    0 signups   quiet
api-docs          0 views (—)        —            ⚠ inactive since Feb 1
```

使用箭头符号表示数据变化：`↑` 表示增长，`↓` 表示下降，`—` 表示持平。标记出需要关注的异常情况。

### 异常检测

主动发现异常情况，不要等到有人提问：
- **突发增长**：任何指标比上一个周期增长超过 2 倍 → “异常增长，需要检查流量来源”
- **急剧下降**：任何指标比上一个周期下降超过 50% → “显著下降，需要调查”
- **无流量项目**：如果某个项目的 `page_view` 事件数量为 0 → “⚠ 该项目没有流量”
- **错误**：如果在指定时间内出现错误事件，请显示 `message` 属性的内容

### 可视化结果

在向 Slack、Discord 或 Telegram 等消息平台报告数据时，纯文本表格难以阅读。可以使用以下工具辅助可视化：
- **`table-image-generator` — 将统计数据渲染为清晰的表格图片
- **`chart-image` — 从分析数据生成折线图、条形图或饼图

## 成长策略 — 不仅仅是跟踪数据

跟踪数据只是第一步。真正的增长来自于一个可重复的系统：明确的信息传递、有针对性的内容分发、持续的数据跟踪、快速的实验验证以及不断的学习。以下是使用 Agent Analytics 实现这些策略的方法。

### 原则 1：确保信息传递清晰

最有效的转化手段是信息传递。如果用户访问网站后需要费力才能理解产品的价值，那么他们很可能会离开。

**您的代理应该做什么：**
- 立即在首页标题上设置 A/B 实验：`experiments create PROJECT --name hero_headline --variants control,b,c --goal cta_click`
- 测试 2-3 个不同的标题版本，以不同的方式传达相同的信息
- 使用声明式 HTML：`data-aa-experiment="hero_headline" data-aa-variant-b="New headline"`
- 在每个变体吸引约 500 名用户后检查实验结果：`experiments get EXP_ID`
- 选定最佳版本后，接着测试副标题或呼叫行动按钮（cta）

**规则：** 在测试信息传递上花费的时间要比添加新功能更多。即使产品本身很优秀，如果用户无法在短时间内理解其价值，也无法实现转化。

### 原则 2：只跟踪能推动决策的数据，而不是所有数据

不要像 Mixpanel 那样跟踪所有数据，只需跟踪那些能够回答“这个项目是否还活跃并正在发展，我接下来应该做什么？”的问题。

**需要跟踪的关键事件（选择 3-5 个）：**
| 事件 | 它能告诉您什么 |
|-------|-------------------|
| `cta_click`（附带 `id`） | 哪些按钮能推动用户采取行动 |
| `signup` | 用户是否完成了注册？转化率是多少？ |
| `feature_used`（附带 `feature`） | 用户在使用功能后是否感受到了价值？ |
| `checkout` | 是否产生了收入？ |

**代理设置跟踪功能的步骤：**
1. 观察网站，确定最重要的用户行为
2. 为这些特定行为添加跟踪功能
3. 通过 `events PROJECT` 确认数据是否正常传输
4. 设置每周检查：`insights PROJECT --period 7d`

**避免的做法：** 不要跟踪滚动深度、鼠标悬停、所有链接点击或表单字段的交互。过多的数据会干扰分析结果。

### 原则 3：找到用户转化的瞬间

转化并不发生在支付环节，而是在用户意识到产品能解决他们问题的那一刻。

**如何找到这个瞬间：**
1. 跟踪关键功能的交互情况：`feature_used` 和具体的功能名称
2. 使用 `breakdown --property feature --event feature_used` 来查看哪些功能与用户留存率相关
3. 检查 `sessions-dist` — 如果大多数会话的 `bounce_rate` 为 0，说明登录页面有问题；如果会话时长较长但注册率低，说明激活路径有问题
4. 使用 `pages --type entry` — 比较不同登录页面的跳出率，找出最有效的页面

**需要优化的方面：**
- 用户首次获得价值所需的时间
- 用户在哪个环节遇到障碍
- 用户是如何发现产品的价值的

### 原则 4：专注一个渠道，持续优化

不要试图同时覆盖所有渠道，而是选择一个主要的获取渠道并深入挖掘。

**Agent Analytics 的支持方式：**
- `breakdown --property referrer --event page_view` — 查看流量实际来自哪里
- `breakdown --property utm_source` — 跟踪流量来源
- `insights --period 7d` — 每周比较不同渠道的流量增长情况
- 为每个渠道创建不同的登录页面版本（例如 `/reddit/`、`/hn/`），然后与 `pages --type entry` 进行对比

**渠道优化步骤：**
1. 每周检查流量来源的分布情况
- 找出流量最高、跳出率最低的渠道
- 针对这个渠道优化内容，并在该渠道的登录页面上进行实验
- 忽略效果不佳的渠道，专注于优化重点渠道

### 原则 5：自主的持续优化循环

Agent Analytics 的独特之处在于它能够实现完整的优化循环：

```
Track → Analyze → Experiment → Ship winner → Repeat
```

**优化循环的实际操作：**
1. **跟踪**：在呼叫行动按钮（CTA）和关键操作上设置跟踪
2. **分析**：每周使用 `insights`、`breakdown` 和 `pages` 获取数据并生成报告
3. **假设**：例如“首页标题的跳出率为 87%”，然后测试一个更清晰的信息传递方式
4. **实验**：`experiments create PROJECT --name hero_v2 --variants control,b --goal cta_click`
5. **监控**：在收集到足够的数据后，使用 `experiments get EXP_ID` 来检查实验结果
6. **实施**：`experiments complete EXP_ID --winner b` 并部署最佳版本
7. **重复**：针对下一个效果较差的元素开始新的实验

**优先测试的方面（按影响程度排序）：**
- 首页标题 — 对跳出率的影响最大
- 呼叫行动按钮的文本 — 直接影响转化率
- 社交证明/信任信号 — 影响用户的注册意愿
- 价格展示方式 — 影响收入
- 用户引导流程 — 影响用户的参与度

**实验频率：** 根据流量情况，每次进行 1-2 次实验。如果流量非常低（每天不到 1000 名用户），则可以减少实验频率。

### 主动监控增长情况

不要等到用户提出问题才采取行动。如果您的代理设置了自动监控机制，应主动发现以下情况：
- **流量激增**：任何指标比上一个周期增长超过 2 倍 → “流量突然增加，需要检查流量来源”
- **流量骤降**：任何指标比上一个周期下降超过 50% → “流量显著下降，需要调查”
- **项目无活跃用户**：如果某个项目的 `page_view` 事件数量为 0 → “⚠ 该项目没有用户访问”
- **错误**：如果在指定时间内出现错误事件，显示错误信息

## 本技能的功能限制

- Agent Analytics 不提供仪表板功能
- 不支持用户管理和计费
- 不提供复杂的渠道分析或用户群体分析
- 不存储个人身份信息（PII）——设计上严格保护用户隐私

## 示例

### 带有价格信息的登录页面

```html
<!-- Hero CTAs -->
<a href="/signup" onclick="window.aa?.track('cta_click',{id:'hero_get_started'})">
  Get Started Free
</a>
<a href="#pricing" onclick="window.aa?.track('cta_click',{id:'hero_see_pricing'})">
  See Pricing →
</a>

<!-- Pricing CTAs -->
<a href="/signup?plan=free" onclick="window.aa?.track('cta_click',{id:'pricing_free'})">
  Try Free
</a>
<a href="/signup?plan=pro" onclick="window.aa?.track('cta_click',{id:'pricing_pro'})">
  Get Started →
</a>
```

### 具有身份验证功能的 SaaS 应用

```js
// After successful signup
window.aa?.track('signup', {method: 'github'});

// When user does the main thing your app does
window.aa?.track('feature_used', {feature: 'create_project'});

// On checkout page
window.aa?.track('checkout', {plan: 'pro'});

// In error handler
window.aa?.track('error', {message: err.message, page: location.pathname});
```