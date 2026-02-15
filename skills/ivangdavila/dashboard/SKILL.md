---
name: Dashboard
slug: dashboard
description: 您可以利用本地托管功能、可视化质量保证（QA）流程以及可脚本化的自动化工具，从任何数据源构建自定义仪表板。
---

## 使用场景

当用户需要从任何数据源（如API、数据库、物联网传感器或业务指标）中提取数据并可视化时，可以使用该工具。系统会先在本地生成Web仪表板，并在交付前进行数据验证。

## 核心原则：**脚本化优先 > 定时检查（Heartbeat）**

所有能够通过自动化方式完成的任务，都应优先使用脚本化方式；只有在以下情况下才需要人工干预：
- 初始设置和连接
- 错误调试
- 设计或布局的调整
- 新数据源的添加

**数据获取应通过cron脚本完成，而非依赖代理程序的定时检查（Heartbeat）**。使用代理程序成本较高，而脚本则更加经济高效。

## 架构设计

```
~/dashboards/
├── registry.json           # Port assignments, project metadata, health status
├── scripts/                # Cron-able fetch scripts (agent generates, system runs)
│   └── fetch-{project}.sh  # curl + jq → data.json
├── {project}/
│   ├── config.json         # Layout, widgets, refresh intervals
│   ├── data.json           # Current data (updated by script, read by dashboard)
│   ├── index.html          # Static dashboard, reads data.json
│   └── .cache/             # Historical data, gitignored
```

## 可视化质量保证流程（必须遵循）

**在未完成数据验证之前，切勿交付任何仪表板。**请务必遵循以下流程：

```
1. Generate HTML
2. Open in browser → take screenshot
3. Check against criteria:
   □ No text overlapping
   □ Readable font sizes (≥14px for body, ≥24px for KPIs)
   □ Consistent spacing (8px grid)
   □ Good contrast (WCAG AA minimum)
   □ Charts have labels/legends
   □ Loading/error states visible
   □ Dark mode working (if enabled)
4. If ANY issue → fix → repeat from 2
5. Only after 3 passes with no issues → deliver
```

## 美学设计原则（确保用户体验）

| 设计元素 | 推荐的默认设置 |
|---------|--------------|
| 颜色 | 使用Tailwind CSS的Slate配色方案，并添加一种强调色 |
| 背景颜色 | 深色：`#0f172a`；浅色：`#f8fafc` |
| 文本颜色 | 深色：`#e2e8f0`；浅色：`#1e293b` |
| 字体间距 | 保持4px的倍数（推荐16px、24px或32px） |
| 角落处理 | 所有角落都应用8px的圆角效果 |
| 图表类型 | 仅使用ECharts或Chart.js，避免混合使用 |
| 字体 | 使用系统自带的字体，禁止使用自定义字体 |
| KPI展示方式 | 数字显示尺寸为48-72px，标签位于下方（14px），并添加表示数据变化的图标 |

## 数据源管理策略

针对不同类型的数据源（SaaS、DevOps、物联网、金融、内容创作等），具体策略请参见`sources.md`文件。

| 使用场景 | 数据源获取方式 | 所需的Token费用 |
|----------|----------|------------|
| 提供SDK/REST接口的API | 使用`curl`和`jq`命令将数据提取到`data.json`文件中 | 无需支付Token费用（通过cron脚本自动执行） |
| 提供Webhook接口的API | 当数据更新时，通过Webhook触发`data.json`文件的更新 | 无需支付Token费用 |
| 无API但提供嵌入功能的平台 | 在仪表板中嵌入第三方组件（如Stripe、Google Analytics插件） | 无需支付Token费用 |
| 既无API也无嵌入功能的平台 | 通过截图方式获取数据并显示在仪表板上 | 可能需要使用代理程序（偶尔） |
| 仅支持数据导出 | 用户提供CSV文件，系统自动读取并显示在仪表板上 | 无需支付Token费用 |
| 需要通过电子邮件接收报告 | 系统解析邮件内容以提取数据 | 需要使用代理程序（负责邮件解析）

**原则：**优先考虑使用脚本化方式获取数据；只有在无法使用脚本化方法时，才采用截图或数据抓取的方式。

## 无API情况下的数据获取策略

对于那些没有提供API的服务（例如某些分析工具或内部系统），可以采取以下方法：

```bash
# Cron runs daily at 6am
# 1. Open headless browser
# 2. Login (credentials from Keychain)
# 3. Navigate to chart
# 4. Screenshot specific element (not full page)
# 5. Save to ~/dashboards/{project}/screenshots/{date}.png
# 6. Dashboard shows latest screenshot with timestamp
```

**使用限制：**
- 每个服务每天最多允许抓取1-2张截图（遵守服务条款）。
- 对于提供API的服务，禁止使用截图方式。
- 必须在截图上显示“最后更新时间：X”。

## API集成规则

- **速率限制**：根据`daily_limit`除以`widgets`再除以`hours_active`来计算每小时的请求次数。
- 如果请求频率超过限制，应降低请求频率或直接报错。
- 需要实时监控每个API的剩余使用额度。

**错误处理机制：**
- 如果连续三次请求失败，系统将自动停止请求。
- 对于过时的数据，会在显示时添加提示信息（例如：“数据更新时间为2小时前 ⚠️”）。
- 仪表板上的数据永远不会显示为空，始终会提供默认的替代内容。

**身份验证：**
- 请将API凭证存储在Keychain中，切勿直接写入配置文件中。
- 主动刷新Token（在Token过期前）。
- 支持多个账户（例如`stripe_personal`和`stripe_work`）。

## 安全性检查清单

在交付任何仪表板之前，请确保满足以下安全要求：
- [ ] API凭证存储在Keychain中，而非配置文件中。
- [ ] 仪表板默认不监听`127.0.0.1`端口。
- 仪表板中不包含任何个人身份信息（如电子邮件地址或姓名）。
- 日志中不记录Token或收入数据。
- 如果日志中包含敏感信息，必须对日志进行加密处理。
- 如果需要局域网访问，使用基于生成的临时密码进行基本身份验证。

## 可扩展性设计

对于需要管理大量仪表板的用户，可以采用以下扩展方案：

```json
// registry.json
{
  "projects": {
    "stripe-revenue": {
      "port": 3001,
      "sources": ["stripe"],
      "lastUpdate": "2026-02-13T10:00:00Z",
      "status": "healthy"
    },
    "home-assistant": {
      "port": 3002,
      "sources": ["hass"],
      "lastUpdate": "2026-02-13T10:05:00Z", 
      "status": "healthy"
    }
  },
  "nextPort": 3003,
  "globalPalette": "slate-blue"  // Shared colors across dashboards
}
```

**元仪表板（Meta-Dashboard）：**生成`~/dashboards/index.html`文件，用于展示所有仪表板的运行状态。

## 法律合规性注意事项

- **官方提供的REST API**：使用官方文档中规定的接口，确保安全。
- **官方提供的嵌入组件**：如Stripe、Google Analytics等第三方组件，可安全使用。
- **公开数据抓取**：需谨慎操作，遵守相关服务条款（如robots.txt文件的规定）。
- **个人账户的截图**：仅限个人使用，需遵守服务条款。
- **未公开的API**：避免使用，以免引发技术问题或违反服务条款。
- **需要登录后才能进行数据抓取**：通常这种行为是被禁止的。

**原则：**如果需要反向工程某个系统的接口，必须让用户了解可能带来的风险。