---
name: agent-analytics
description: 为任何网站添加轻量级、注重隐私的 Analytics 跟踪功能。可以跟踪页面浏览量和自定义事件，并通过 CLI 或 API 查询数据。当用户想要了解项目是否仍在运行并持续发展时，可以使用该功能。
version: 2.1.0
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

Agent Analytics 并非 Mixpanel。不要跟踪所有数据，只需跟踪那些能够回答“这个项目是否还活跃并正在发展？”的问题。对于一个典型的网站来说，除了自动记录的页面浏览量之外，最多只需要跟踪 3-5 个自定义事件。

## 首次设置

**获取 API 密钥：** 在 [agentanalytics.sh](https://agentanalytics.sh) 注册，并从控制面板生成一个密钥。或者，您也可以从 [GitHub](https://github.com/Agent-Analytics/agent-analytics) 下载开源版本进行自托管。

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

`create` 命令会返回一个“项目写入令牌”（project write token），请在下面的代码片段中将其用作 `data-token`。这个令牌与您的 API 密钥（用于读取/查询数据）是分开使用的。

## 第一步：添加跟踪代码片段

在 `</body>` 之前添加以下代码：

```html
<script src="https://api.agentanalytics.sh/tracker.js"
  data-project="PROJECT_NAME"
  data-token="PROJECT_WRITE_TOKEN"></script>
```

这段代码会自动跟踪包含路径（path）、引用来源（referrer）、浏览器类型（browser）、操作系统（OS）、设备类型（device）、屏幕尺寸（screen size）以及 UTM 参数（UTM params）的 `page_view` 事件。您无需额外添加自定义的 `page_view` 事件。

> **安全提示：** 项目写入令牌（`aat_*`）是公开且安全的，可以直接嵌入到客户端 HTML 中。它只能用于向特定项目写入数据，具有速率限制（免费用户每分钟 10 次请求，付费用户每分钟 1,000 次请求），并且可以通过控制面板进行撤销。它无法读取数据——读取数据需要使用单独的 API 密钥（`aak_*`）。

## 第二步：查看已有的事件（已有的项目）

如果跟踪功能已经启用，请查看当前使用了哪些事件及其对应的属性键，以确保新添加的事件与现有系统的命名规则一致：

```bash
npx @agent-analytics/cli properties-received PROJECT_NAME
```

这段代码会显示每种事件类型使用的属性键（例如：`cta_click → id`、`signup → method`）。在添加新事件之前，请确保新事件的命名与现有系统保持一致。

## 第三步：为重要操作添加自定义事件

在需要跟踪用户行为的元素上使用 `onclick` 事件处理程序：

```html
<a href="..." onclick="window.aa?.track('EVENT_NAME', {id: 'ELEMENT_ID'})">
```

`?.` 运算符可以确保在跟踪器尚未加载时不会引发错误。

### 80% 的 SaaS 网站都会使用的标准事件

根据实际需求选择合适的事件类型。大多数网站需要跟踪 2-4 种事件：

| 事件类型 | 触发条件 | 属性键       |
|---------|-----------|------------|
| `cta_click` | 用户点击呼叫行动按钮 | `id`        |
| `signup` | 用户创建账户    | `method`      |
| `login` | 用户登录      | `method`      |
| `feature_used` | 用户使用核心功能 | `feature`      |
| `checkout` | 用户开始支付流程 | `plan`       |
| `error` | 发生明显错误    | `message`, `page`    |

### 应该跟踪哪些事件（以 `cta_click` 为例）：

- 表示用户有转化意向的按钮，如“开始使用”/“注册”/“免费试用”按钮
- “升级”/“购买”等购买引导按钮
- 导航到注册页面或仪表板的链接
- 针对开源项目的“在 GitHub 上查看”/“收藏”按钮

### 不应该跟踪的内容：
- 所有的链接或按钮（信息量过大）
- 页面滚动深度（无法直接操作）
- 表单字段的交互（过于详细）
- 底部链接（数据价值较低）

### 属性命名规则：
- 使用蛇形命名法（snake_case），例如 `hero_get_started` 而不是 `heroGetStarted`
- `id` 属性用于唯一标识元素，应简短且具有描述性
- 将相关属性命名为 `section_action`，例如 `hero_signup`、`pricing_pro`、`nav_dashboard`
- 不需要对 `page_view` 已经捕获的数据（如路径、引用来源、浏览器类型）进行重新编码

## 第四步：立即进行测试

添加跟踪代码后，请立即验证其是否正常工作：

```bash
# Option A: Browser console on your site:
window.aa.track('test_event', {source: 'manual_test'})

# Option B: Click around, then check:
npx @agent-analytics/cli events PROJECT_NAME

# Events appear within seconds.
```

## 数据查询

### 命令行工具参考

```bash
# List all your projects (do this first)
npx @agent-analytics/cli projects

# Aggregated stats for a project
npx @agent-analytics/cli stats my-site --days 7

# Recent events (raw log)
npx @agent-analytics/cli events my-site --days 30 --limit 50

# What property keys exist per event type?
npx @agent-analytics/cli properties-received my-site --since 2025-01-01

# Direct API (for agents without npx):
curl "https://api.agentanalytics.sh/stats?project=my-site&days=7" \
  -H "X-API-Key: $AGENT_ANALYTICS_API_KEY"
```

**常用参数**（适用于 `stats`、`events` 和 `properties-received`）：
- `--days <N>` — 查看时间范围（默认：7 天）
- `--limit <N>` — 返回的最大事件数量（默认：100 个，仅限 `events`）
- `--since <date>` — 时间截止日期（仅限 `properties-received`）

## 不仅仅是查询数据，还要进行分析

您可以使用这些工具对数据进行分析，而不仅仅是展示原始数值。从数据中提取有价值的洞察。

### 周期性比较

通过比较两个时间窗口来发现趋势。命令行工具不会自动进行数据计算，您需要手动完成：

```bash
# Pull this week and last week
npx @agent-analytics/cli stats my-site --days 7    # → current period
npx @agent-analytics/cli stats my-site --days 14   # → includes previous period

# Subtract: (14-day total - 7-day total) = previous 7-day total
# Then: ((current - previous) / previous) * 100 = % change
```

使用 `--days 1` 和 `--days 2` 来比较不同时间段的数据，以观察趋势变化。

### 计算衍生指标

在获得原始数据后，请计算以下指标：
- **转化率**：`cta_click` 数量 / `page_view` 数量 × 100%
- **日均值**：`总事件数 / 天数`
- **同比增长**：`(当前周期 - 上一周期) / 上一周期 × 100`
- **每个会话中的事件数**：`总事件数 / 唯一会话数`

### 异常检测

主动发现异常情况，不要等到有人提出问题：
- **异常增长**：任何指标超过日均值的 2 倍
- **急剧下降**：任何指标低于日均值的 50%
- **错误**：最近时间段内的错误事件
- **停滞项目**：之前活跃的项目突然没有 `page_view` 事件

发现异常时，请说明具体是什么情况、何时开始出现异常，并尽可能提供可能的原因。

### 报告格式

在报告项目数据时，请使用以下格式：每个项目占一行，便于阅读：

```
my-site       142 views (+23% ↑)  12 signups   healthy
side-project   38 views (-8% ↓)    0 signups   quiet
api-docs        0 views (—)        —            ⚠ inactive since Feb 1
```

使用趋势箭头表示数据变化：`↑` 表示增长，`↓` 表示下降，`—` 表示持平。对需要关注的情况进行标记。

### 数据可视化

在向 Slack、Discord 或 Telegram 等消息平台报告时，原始文本表格可能难以阅读。请使用以下工具将数据可视化：
- `table-image-generator` — 将统计数据渲染为清晰的表格图片
- `chart-image` — 从分析数据生成折线图、条形图、面积图或饼图

**注意：** 不要将原始 ASCII 表格直接发送到消息平台，应生成图片形式的数据。

## Agent Analytics 的限制：
- 不提供仪表板功能——您的代理本身就充当了仪表板
- 不支持用户管理或计费功能
- 不支持复杂的漏斗分析或群体分析
- 不存储个人身份信息（PII）——设计上注重保护用户隐私

## 示例：
- 带有价格信息的登录页面
- 具有身份验证功能的 SaaS 应用程序

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