---
name: supalytics
description: 使用 Supalytics CLI 查询网站分析数据。当用户需要查看页面浏览量、访问者数量、热门页面、流量来源、引用来源、国家/地区、收入指标、转化率、用户转化路径、事件信息或实时访问者数量时，可以使用该工具。
metadata: {"openclaw":{"emoji":"📊","requires":{"bins":["supalytics"]},"homepage":"https://supalytics.co"}}
---

# Supalytics CLI

从 [Supalytics](https://supalytics.co) 查询网站分析数据——简单、快速且符合 GDPR 规范的分析工具，支持收入归因功能。

## 安装

**需要 [Bun](https://bun.sh) 运行时环境**（不支持 Node.js）：

```bash
# Install Bun first
curl -fsSL https://bun.sh/install | bash
export PATH="$HOME/.bun/bin:$PATH"

# Install Supalytics CLI
bun add -g @supalytics/cli
```

## 认证

### 注意：在代理环境中使用 OAuth 时可能出现的问题

`supalytics login` 命令使用 OAuth 设备流进行认证，这需要在浏览器中完成用户交互。但在代理环境（如 OpenClaw）中，认证过程可能会在完成之前被中断。

**针对 OpenClaw 的解决方案：** 使用 `background: true` 模式：

```javascript
await exec({
  command: 'supalytics login',
  background: true,
  yieldMs: 2000  // Wait 2s to capture the verification URL
});
```

代理程序应：
1. 在后台运行登录流程
2. 将验证 URL 显示给用户
3. 等待用户完成浏览器中的授权操作
4. 定期检查后台会话以确认认证是否完成

### 快速设置

```bash
supalytics init    # Opens browser, creates site, shows tracking snippet
```

### 手动设置

```bash
supalytics login        # Opens browser for OAuth
supalytics sites add    # Create a new site
```

## 命令

### 快速统计信息

```bash
supalytics stats              # Last 30 days (default)
supalytics stats today        # Today only
supalytics stats yesterday    # Yesterday
supalytics stats week         # This week
supalytics stats month        # This month
supalytics stats 7d           # Last 7 days
supalytics stats --all        # Include breakdowns (pages, referrers, countries, etc.)
```

### 实时访问者数量

```bash
supalytics realtime           # Current visitors on site
supalytics realtime --watch   # Auto-refresh every 30s
```

### 数据趋势（时间序列）

```bash
supalytics trend              # Daily visitor trend with bar chart
supalytics trend --period 7d  # Last 7 days
supalytics trend --compact    # Sparkline only
```

### 数据细分

```bash
supalytics pages              # Top pages by visitors
supalytics referrers          # Top referrers
supalytics countries          # Traffic by country
```

### 事件记录

```bash
supalytics events                          # List all custom events
supalytics events signup                   # Properties for specific event
supalytics events signup --property plan   # Breakdown by property value
```

### 自定义查询

`query` 命令是最灵活的查询工具：

```bash
# Top pages with revenue
supalytics query -d page -m visitors,revenue

# Traffic by country and device
supalytics query -d country,device -m visitors

# Blog traffic from US only
supalytics query -d page -f "page:contains:/blog" -f "country:is:US"

# Hourly breakdown
supalytics query -d hour -m visitors -p 7d

# UTM campaign performance
supalytics query -d utm_source,utm_campaign -m visitors,revenue

# Sort by revenue descending
supalytics query -d page --sort revenue:desc

# Pages visited by users who signed up
supalytics query -d page -f "event:is:signup"

# Filter by event property
supalytics query -d country -f "event_property:is:plan:premium"
```

**可用的指标：** `visitors`（访问者数量）、`pageviews`（页面浏览量）、`bounce_rate`（跳出率）、`avg_session_duration`（平均会话时长）、`revenue`（收入）、`conversions`（转化次数）、`conversion_rate`（转化率）

**可用的维度：** `page`（页面）、`referrer`（引用来源）、`country`（国家）、`region`（地区）、`city`（城市）、`browser`（浏览器类型）、`os`（操作系统）、`device`（设备类型）、`date`（日期）、`hour`（小时）、`event`（事件类型）、`utm_source`（UTM 源）、`utm_medium`（UTM 渠道）、`utm_campaign`（UTM 活动）、`utm_term`（UTM 术语）、`utm_content`（UTM 内容）

### 网站管理

```bash
supalytics sites                              # List all sites
supalytics sites add example.com              # Create site
supalytics sites update my-site -d example.com  # Update domain
supalytics default example.com                # Set default site
supalytics remove example.com                 # Remove site
```

## 全局选项

所有分析命令都支持以下选项：

| 选项          | 描述                                      |
|-----------------|-------------------------------------------|
| `-s, --site <domain>`   | 查询特定网站（否则使用默认网站）                        |
| `-p, --period <period>` | 时间周期：`7d`、`14d`、`30d`、`90d`、`12mo`、`all`              |
| `--start <date>`     | 开始日期（格式：YYYY-MM-DD）                         |
| `--end <date>`     | 结束日期（格式：YYYY-MM-DD）                         |
| `-f, --filter <filter>`   | 过滤条件：`field:operator:value`                    |
| `--json`       | 输出原始 JSON 数据（用于程序化处理）                     |
| `--no-revenue`    | 不显示收入相关指标                         |
| `-t, --test`     | 查询本地主机/测试数据                         |

## 过滤语法

格式：`field:operator:value`

**操作符：** `is`、`is_not`、`contains`、`not_contains`、`starts_with`

**示例：**
```bash
-f "country:is:US"
-f "page:contains:/blog"
-f "device:is:mobile"
-f "referrer:is:twitter.com"
-f "utm_source:is:newsletter"
-f "event:is:signup"
-f "event_property:is:plan:premium"
```

## 输出格式

- **人类可读格式（默认）**：带有颜色区分的格式化表格
- **JSON 格式 (`--json`)**：原始 JSON 数据，适用于程序化处理

```bash
supalytics stats --json | jq '.data[0].metrics.visitors'
supalytics query -d page -m visitors --json
```

## 使用案例示例

### “我的网站表现如何？”
```bash
supalytics stats
```

### “我的主要流量来源是什么？”
```bash
supalytics referrers
# or with revenue
supalytics query -d referrer -m visitors,revenue
```

### “哪些页面产生的收入最多？”
```bash
supalytics query -d page -m revenue --sort revenue:desc
```

### “我的新闻邮件活动效果如何？”
```bash
supalytics query -d utm_campaign -f "utm_source:is:newsletter" -m visitors,conversions,revenue
```

### “现在有哪些人在访问我的网站？”
```bash
supalytics realtime
```

### “显示本周的访问者趋势”
```bash
supalytics trend --period 7d
```

## 故障排除

| 问题                | 解决方案                                      |
|------------------|-------------------------------------------|
| 命令未找到：`supalytics`     | 确保已安装 Bun，并且 `~/.bun/bin` 在系统路径中；或创建符号链接       |
| 未指定网站            | 运行 `supalytics default <domain>` 以使用默认网站           |
| 未经授权            | 运行 `supalytics login` 重新认证                         |
| 未返回数据            | 检查网站是否已启用跟踪功能；尝试使用 `-t` 命令进行测试           |

### OpenClaw / 守护进程使用

Bun 安装后，其可执行文件位于 `~/.bun/bin`，但该路径可能不在 OpenClaw 等守护进程的系统路径中。安装完成后，需要创建符号链接将 `~/.bun/bin` 添加到系统路径中：

```bash
sudo ln -sf ~/.bun/bin/bun /usr/local/bin/bun
sudo ln -sf ~/.bun/bin/supalytics /usr/local/bin/supalytics
```