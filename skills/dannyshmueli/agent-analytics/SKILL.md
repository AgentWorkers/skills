---
name: agent-analytics
description: 为任何网站添加轻量级、注重隐私的分析跟踪功能。可以跟踪页面浏览量和自定义事件，并通过 CLI 或 API 查询数据。当用户想要了解项目是否仍在运行以及是否正在发展时，可以使用该功能。
version: 2.4.0
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
# Agent Analytics — 为任何网站添加跟踪功能

您可以使用 Agent Analytics 为网站添加分析跟踪功能。Agent Analytics 是一个专为开发者设计的轻量级平台，适用于那些发布大量项目并希望其 AI 代理能够监控这些项目的开发者。

## 设计理念

Agent Analytics 并非 Mixpanel。不要跟踪所有数据，只需跟踪那些能够回答“这个项目是否还有活力并正在发展？”的问题。对于一个典型的网站来说，除了自动记录的页面浏览量之外，最多只需跟踪 3-5 个自定义事件。

## 首次设置

**获取 API 密钥：** 在 [agentanalytics.sh](https://agentanalytics.sh) 注册，并从仪表板生成一个密钥。或者，您也可以从 [GitHub](https://github.com/Agent-Analytics/agent-analytics) 下载开源版本进行自行托管。

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

`create` 命令会返回一个 **项目写入令牌**（project write token）——请在下面的代码片段中将其作为 `data-token` 使用。这个令牌与您的 API 密钥（用于读取/查询数据）是不同的。

## 第一步：添加跟踪代码片段

在 `</body>` 之前添加以下代码：

```html
<script src="https://api.agentanalytics.sh/tracker.js"
  data-project="PROJECT_NAME"
  data-token="PROJECT_WRITE_TOKEN"></script>
```

这段代码会自动跟踪包含路径（path）、引用来源（referrer）、浏览器类型（browser）、操作系统（OS）、设备类型（device）、屏幕尺寸（screen size）以及 UTM 参数（UTM params）的 `page_view` 事件。您无需手动添加自定义的 `page_view` 事件。

> **安全提示：** 项目写入令牌（`aat_*`）是公开且安全的，可以安全地嵌入到客户端 HTML 中。它只能将事件写入到特定的项目中，具有速率限制（免费用户每分钟 10 次请求，付费用户每分钟 1,000 次请求），并且可以从仪表板撤销。它无法读取数据——读取数据需要使用单独的 API 密钥（`aak_*`）。

## 第二步：查看现有事件（已有的项目）

如果已经启用了跟踪功能，请检查哪些事件和属性键正在被使用，以便在新添加事件时保持名称的一致性：

```bash
npx @agent-analytics/cli properties-received PROJECT_NAME
```

这段代码会显示每种事件类型使用的属性键（例如 `cta_click → id`、`signup → method`）。在添加新事件之前，请确保名称一致。

## 第三步：为重要操作添加自定义事件

在需要跟踪用户行为的元素上使用 `onclick` 事件处理程序：

```html
<a href="..." onclick="window.aa?.track('EVENT_NAME', {id: 'ELEMENT_ID'})">
```

`?.` 运算符可以确保在跟踪器尚未加载时不会引发错误。

### 80% 的 SaaS 网站都需要的标准事件

选择适用于您网站的事件类型。大多数网站需要 2-4 个标准事件：

| 事件 | 触发条件 | 属性 |
|-------|-------------|------------|
| `cta_click` | 用户点击呼叫行动按钮（CTA button） | `id`（按钮的 ID） |
| `signup` | 用户创建账户 | `method`（注册方式：github/google/email） |
| `login` | 用户登录 | `method` |
| `feature_used` | 用户使用了核心功能 | `feature`（使用的功能） |
| `checkout` | 用户开始支付流程 | `plan`（套餐类型：free/pro 等） |
| `error` | 发生了明显错误 | `message`, `page` |

### 应该跟踪哪些作为 `cta_click` 的事件

- 表示用户有转化意图的按钮，例如 “开始使用” / “注册” / “免费试用” 按钮 |
- “升级” / “购买” 等购买呼吁按钮 |
- 导航到注册页面或仪表板的链接 |
- 针对开源项目的 “在 GitHub 上查看” / “星标” 按钮 |

### 不应该跟踪的内容
- 所有的链接或按钮（信息量太大，不易分析） |
- 滚动深度（无法直接操作） |
- 表单字段的交互（过于详细） |
- 底部链接（数据量较少）

### 属性命名规则
- 使用蛇形命名法（snake_case），例如 `hero_get_started` 而不是 `heroGetStarted` |
- `id` 属性用于唯一标识元素，应简洁且具有描述性 |
- 将 ID 命名为 `section_action`，例如 `hero_signup`、`pricing_pro`、`nav_dashboard` |
- 不需要对 `page_view` 已经捕获的数据进行编码（如路径、引用来源、浏览器类型等）。

## 第二步（高级）：运行 A/B 实验

A/B 实验可以帮助您测试页面元素的哪种变体更有效。整个实验过程由 API 驱动，无需使用仪表板界面。

### 创建实验

```bash
npx @agent-analytics/cli experiments create my-site \
  --name signup_cta --variants control,new_cta --goal signup
```

或者通过 API 进行设置：

```bash
curl -X POST "https://api.agentanalytics.sh/experiments" \
  -H "X-API-Key: $AGENT_ANALYTICS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"project":"my-site","name":"signup_cta","variants":["control","new_cta"],"goal_event":"signup"}'
```

### 在代码中实现实验变体

```js
// tracker.js loads config automatically. Use aa.experiment() to get the assigned variant:
var variant = window.aa?.experiment('signup_cta', ['control', 'new_cta']);

if (variant === 'new_cta') {
  document.querySelector('.cta').textContent = 'Start Free Trial';
} else {
  document.querySelector('.cta').textContent = 'Sign Up';
}
```

关键点：
- `aa.experiment()` 是确定性的——同一用户总是会被分配到相同的实验变体 |
- 每个会话只会自动记录一次曝光事件（exposure event） |
- 即使配置端点尚未加载，内联的 `['control', 'new_cta']` 也会生效 |
- 按照常规方式跟踪目标事件：`window.aa?.track('signup', {method: 'github'})`

### 查看实验结果

```bash
npx @agent-analytics/cli experiments get exp_abc123
```

实验结果会返回贝叶斯概率 `probability_best`、转化提升量（lift）以及推荐方案（recommendation）。通常每个实验变体需要大约 100 次曝光才能获得有意义的结果。

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
- 使用蛇形命名法为实验命名，例如 `signup_cta`、`pricing_layout`、`hero_copy` |
- 除非流量非常大，否则使用两个变体（A/B）——更多的变体需要更多的数据 |
- 设置一个明确的 `goal_event`，该事件应与业务目标相关联（例如 `signup`、`purchase`，而不是简单的 `page_view`） |
- 在选择最佳方案之前，让实验持续运行直到 `sufficient_data: true` |
- 实验完成后执行 `experiments complete <id> --winner new_cta` 命令来结束实验。

## 立即进行测试

添加跟踪功能后，立即验证其是否正常工作：

```bash
# Option A: Browser console on your site:
window.aa.track('test_event', {source: 'manual_test'})

# Option B: Click around, then check:
npx @agent-analytics/cli events PROJECT_NAME

# Events appear within seconds.
```

## 查询数据

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
- `--days <N>` — 回顾时间窗口（默认值：7 天；适用于 `stats` 和 `events`） |
- `--limit <N>` — 返回的最大行数（默认值：100） |
- `--since <date>` — 时间截止日期（仅适用于 `properties-received`） |
- `--period <P>` — 对比周期：`1d`、`7d`、`14d`、`30d`、`90d`（仅适用于 `insights`） |
- `--property <key>` — 按属性键进行分组（`breakdown` 需要此参数） |
- `--event <name>` — 按事件名称过滤结果（`breakdown` 需要此参数） |
- `--type <T>` — 页面类型：`entry`、`exit`、`both`（仅适用于 `pages`，默认值：`entry`）

### 分析 API 端点

这些端点返回预先计算好的数据汇总结果——直接使用这些结果，无需在客户端重新计算。所有请求都需要包含 `X-API-Key` 标头或 `?key=` 参数。

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

## 根据需求选择合适的端点

根据用户的问题选择相应的 API 端点：

| 用户问题 | 应使用的 API 端点 | 原因 |
|-----------|------|-----|
| “我的网站表现如何？” | `insights` + `breakdown` + `pages` | 一次性获取完整的每周数据 |
| “有人访问我的网站吗？” | `insights --period 7d` | 快速判断网站是否还有活力 |
| “我的热门页面有哪些？” | `breakdown --property path --event page_view` | 按用户数量排序的热门页面列表 |
| “我的流量来自哪里？” | `breakdown --property referrer --event page_view` | 流量来源 |
| “哪个登录页面的效果最好？” | `pages --type entry` | 每个页面的跳出率和会话深度 |
| “我应该什么时候发布内容？” | `heatmap` | 查找流量较低或高峰时段 |
| “给我所有项目的总结” | 先调用 `projects`，然后对每个项目调用 `insights` | 多项目概览 |

对于任何关于网站表现的问题，**始终先调用 `insights` 端点**——这是最实用的端点。

## 不仅仅是查询数据，还要进行分析

不要仅仅返回原始数据，要对其进行解读。以下是如何将每个 API 端点的返回结果转化为有用的信息。

### `/insights` — 综合分析结果

API 返回的指标包括 `current`、`previous`、`change`、`change_pct` 和 `trend` 字段。

**解读方法：**
- `change_pct > 10` → 表示网站正在增长，应予以正面反馈 |
- `change_pct` 在 -10 到 10 之间 → 表示网站表现稳定 |
- `change_pct < -10` → 表示网站表现下降，建议进一步调查 |
- 比较 `currentbounce_rate` 和 `previousbounce_rate` 的变化情况，判断网站是否有所改善 |
- 将 `avg_duration` 从毫秒转换为秒：`Math.round(value / 1000)` |
- 如果上一个周期的所有数据均为 0，则表示这是一个新项目，没有之前的数据可供对比 |

**示例输出：**
```
This week vs last: 173 events (+22%), 98 users (+18%).
Bounce rate: 87% (up from 82% — getting worse).
Average session: 24s. Trend: growing.
```

### `/breakdown` — 数据排名

API 返回按数量降序排列的 `values: [{ value, count, unique_users }]`。

**解读方法：**
- 只显示前 3-5 个数据即可；避免显示全部数据 |
- 同时显示 `unique_users`，因为 2 个用户产生的 100 个事件与 80 个用户产生的 100 个事件可能有很大差异 |
- 使用 `total_with_property / total_events` 来了解数据覆盖范围，例如 “155 次页面浏览中有 155 次包含了特定路径” |
- 对于引用来源，将结果分为 “direct”（直接访问）和其他类型：

**示例输出：**
```
Top pages: / (98 views, 75 users), /pricing (33 views, 25 users), /docs (19 views, 4 users).
The /docs page has high repeat visits (19 views, 4 users) — power users.
```

### `/pages` — 页面分析

API 返回 `entry_pages: [{ page, sessions, bounces, bounce_rate, avg_duration, avg_events }]`。

**解读方法：**
- `bounce_rate` > 0.7 → 表示页面跳出率较高，需要改进 |
- `bounce_rate` < 0.3 → 表示页面表现良好 |
- 将 `avg_duration` 从毫秒转换为秒；如果小于 10 秒则表示用户体验不佳，大于 60 秒则表示用户体验良好 |
- `avg_events` 表示每个页面的平均会话时长；1.0 表示用户几乎立即离开页面，3.0 或以上表示用户互动良好 |
- 比较不同页面的转化效果，例如：“您的定价页面的转化率是首页的 3 倍”

**示例输出：**
```
Best landing page: /pricing — 14% bounce, 62s avg session, 4.1 pages/visit.
Worst: /blog/launch — 52% bounce, 18s avg. Consider a stronger CTA above the fold.
```

### `/sessions/distribution` — 用户行为分析

API 返回 `distribution: [{ bucket, sessions, pct }]`、`engagedpct` 和 `median_bucket`。

**解读方法：**
- `engagedpct` 是关键指标，表示会话时长大于 30 秒的用户比例 |
- `engagedpct` < 10% → 表示大部分用户立即离开页面，需要优化首屏体验 |
- `engagedpct` 在 10% 到 30% 之间表示用户互动适中 |
- `engagedpct` > 30% 表示用户互动良好 |
- 如果 80% 以上的用户属于 “0s” 组，说明网站存在严重的跳出率问题 |
- 如果不同时间段的用户分布均匀，说明用户体验良好 |

**示例输出：**
```
88% of sessions bounce instantly (0s). Only 6% stay longer than 30s.
The few who do engage stay 3-10 minutes — the content works, but first impressions don't.
```

### `/heatmap` — 时间分布分析

API 返回 `heatmap: [{ day, day_name, hour, events, users }]`、`peak`、`busiest_day`、`busiest_hour`。

**解读方法：**
- `peak` 表示流量最大的时间段；请注意时间是以 UTC 为基准的 |
- `busiest_day` 表示用户活跃的最高峰时段 |
- `busiest_hour` 表示用户在线的最高峰时间 |
- 在流量较低的时间段（如周日凌晨 3 点 UTC）发布内容 |
- 通过比较工作日与周末的流量分布，可以判断用户群体是 B2B 还是 B2C：

**示例输出：**
```
Peak: Friday at 11 PM UTC (35 events, 33 users). Busiest day overall: Sunday.
Traffic is heaviest on weekends — your audience browses on personal time.
Deploy on weekday mornings for minimal disruption.
```

### 周期性数据分析（同时调用三个 API）

同时调用 `insights`、`breakdown --property path --event page_view` 和 `pages --type entry`，然后将结果整合到一个响应中：

```
Weekly Report — my-site (Feb 8–15 vs Feb 1–8)
Events: 1,200 (+22% ↑)  Users: 450 (+18% ↑)  Bounce: 42% (improved from 48%)
Top pages: /home (523), /pricing (187), /docs (94)
Best landing: /pricing — 14% bounce, 62s avg. Worst: /blog — 52% bounce.
Trend: Growing.
```

### 多项目概览

首先调用 `projects` 获取所有项目的列表，然后对每个项目分别调用 `insights --period 7d`，每个项目显示一行结果：

```
my-site         142 views (+23% ↑)  12 signups   healthy
side-project     38 views (-8% ↓)    0 signups   quiet
api-docs          0 views (—)        —            ⚠ inactive since Feb 1
```

使用箭头符号表示数据变化：`↑` 表示上升，`↓` 表示下降，`—` 表示数据持平。标记出需要关注的问题。

### 异常检测

主动发现异常情况，不要等到被询问才处理：
- **突然增长**：任何指标超过上一个周期的 2 倍 → “出现异常增长，检查引用来源” |
- **急剧下降**：任何指标低于上一个周期的 50% → “出现显著下降，需要调查” |
- **无流量项目**：`page_view` 事件数量为零 → “⚠ 未检测到任何流量” |
- **错误**：如果在指定时间段内出现错误事件，请显示 `message` 属性的内容 |

### 可视化结果

在向 Slack、Discord 或 Telegram 等消息平台报告数据时，纯文本表格可能难以阅读。可以使用以下工具进行数据可视化：
- **`table-image-generator` — 将统计数据渲染为清晰的表格图像 |
- **`chart-image` — 从分析数据生成折线图、条形图、面积图或饼图 |

## Agent Analytics 的功能限制

- **没有内置仪表板** — 网站的跟踪功能就是您的仪表板 |
- **不提供用户管理或计费功能** |
- **不支持复杂的渠道分析或群体分析** |
- **不存储个人身份信息（PII）** — 为保护用户隐私，系统不会记录或保留 IP 地址 |

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