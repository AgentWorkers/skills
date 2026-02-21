---
name: reddit-spy
description: **Stealth Reddit 智能工具**：允许您在不被封禁的情况下浏览、阅读和分析任何 Reddit 子版块。该工具采用了多层备份机制（OAuth API → Stealth HTTP → 浏览器隐藏模式 → PullPush 归档技术），确保您的访问行为不会被检测到。
---
# Reddit Spy -- 隐秘的子版块情报收集工具

您可以浏览任何目标子版块，阅读完整帖子，分析策略，并提取竞争情报——所有这些操作都不会被 Reddit 封禁。

**入口点：**
```bash
python3 /root/.openclaw/skills/reddit-spy/scripts/reddit_spy.py <command> [options]
```

所有命令都会将输出结果以 JSON 格式写入标准输出（stdout），日志则会被写入标准错误输出（stderr）。

---

## 设置

**Tor（主要使用，已运行中）：**
Tor 可以让您从任何 IP 地址实时访问 Reddit。它作为 systemd 服务运行在这台虚拟专用服务器（VPS）上。
```bash
# Verify Tor is running
systemctl status tor@default

# If stopped, start it
systemctl start tor@default
```

**可选：Reddit OAuth（更可靠）：**
如果您拥有 Reddit API 访问权限，请设置以下环境变量（每分钟 60 次请求限制）：
```bash
export REDDIT_CLIENT_ID="your-app-client-id"
export REDDIT_CLIENT_SECRET="your-app-secret"
export REDDIT_USERNAME="your-reddit-username"
export REDDIT_PASSWORD="your-reddit-password"
```

**可选：代理服务器：**
```bash
export REDDIT_PROXY_URL="http://user:pass@proxy:port"
```

---

## 数据获取流程（按顺序执行）

| 数据获取层 | 方法 | 速度 | 数据类型 | 状态 |
|-------|--------|-------|------|--------|
| 1. OAuth API | Reddit API v2 | 快速 | 实时数据 | 可选（需要 API 密钥） |
| 2. **Tor** | 通过 Tor 出口节点使用 SOCKS5 协议 | 快速 | 实时数据 | **主要数据获取层** |
| 3. 隐秘 HTTP 请求 | 直接访问 old.reddit.com | 快速 | 实时数据 | 但在 VPS 上可能被屏蔽 |
| 4. 浏览器代理 | 使用 Playwright 工具 | 较慢 | 实时数据 | 但在 VPS 上可能被屏蔽 |
| 5. PullPush | 使用 Archive API | 快速 | 历史数据（可能存在延迟） | 始终可用 |

每个命令会按顺序尝试不同的数据获取方式；如果某层无法获取数据，则会自动切换到下一层。各数据获取层的状态会被缓存 1 小时。Tor 会自动更换连接路径（以规避速率限制）。

---

## 命令说明

### `spy` -- 全面子版块情报收集

一次性获取子版块的基本信息、热门帖子及策略分析结果。
```bash
python3 .../reddit_spy.py spy --subreddit IndieHackers --sort top --timeframe week --limit 25
```

| 参数 | 默认值 | 可选值 |
|-------|---------|--------|
| `--subreddit` | （必填） | 子版块名称（不含前缀 "r/"） |
| `--sort` | top | 热门、新帖、最高排名、上升趋势 |
| `--timeframe` | week | 小时、天、周、月、年、全部 |
| `--limit` | 25 | 需分析的帖子数量 |

**返回结果：** 关键指标、获取的帖子数量、内容类型分布、互动模式分析、热门帖子列表及实用建议。

### `deep-read` -- 帖子深度分析

读取帖子的全部内容及所有嵌套评论，并提供相关统计信息。
```bash
python3 .../reddit_spy.py deep-read --url "https://www.reddit.com/r/.../comments/..." --depth 8
```

**返回结果：** 帖子全文、扁平化的评论列表（包含作者、内容、评分、评论深度等信息）以及评论统计数据。

### `bulk-scan` -- 多个子版块批量扫描

一次性扫描多个子版块并进行对比分析。
```bash
python3 .../reddit_spy.py bulk-scan --subreddits "IndieHackers,SaaS,Entrepreneur" --timeframe all --limit 20
```

**返回结果：** 每个子版块的策略分析结果以及子版块间的对比数据（按订阅者和互动量排序）。

### `strategy` -- 策略模式提取

分析哪些内容策略在特定子版块中最有效。
```bash
python3 .../reddit_spy.py strategy --subreddit SaaS --sort top --timeframe month --limit 50
```

**返回结果：** 内容类型排名、互动模式排名、最佳发布时间/日期、热门帖子列表及建议。

### `search` -- 关键词搜索

在指定子版块内搜索特定主题。
```bash
python3 .../reddit_spy.py search --subreddit IndieHackers --query "growth strategy" --sort top --timeframe month
```

### `user-intel` -- 用户资料分析

分析用户在多个子版块中的发布模式。
```bash
python3 .../reddit_spy.py user-intel --username some_user --limit 25
```

**返回结果：** 用户的总帖子数量、子版块使用频率、内容发布模式及互动分析。

### `health-check` -- 数据获取层状态检测

检查当前可用的数据获取层是否正常工作。
```bash
python3 .../reddit_spy.py health-check --test-sub python
```

---

## 情报收集工作流程

### 第一步：状态检查
```bash
python3 .../reddit_spy.py health-check
```
在开始分析之前，先确认所有数据获取层是否正常运行。

### 第二步：批量扫描目标子版块
```bash
python3 .../reddit_spy.py bulk-scan --subreddits "IndieHackers,SaaS,Entrepreneur,Automation" --timeframe week --limit 25
```

### 第三步：深入分析热门帖子
从第一步中筛选出得分较高的帖子，并阅读其全部内容和评论。
```bash
python3 .../reddit_spy.py deep-read --url "https://reddit.com/r/.../comments/..."
```

### 第四步：分析顶级贡献者
```bash
python3 .../reddit_spy.py user-intel --username top_poster
```

### 第五步：查找信息空白点
```bash
python3 .../reddit_spy.py search --subreddit IndieHackers --query "automation" --sort top
```

---

## 战略分析输出

`spy`、`bulk-scan` 和 `strategy` 命令会返回以下信息：

- **内容类型**：问题、教程、技巧、展示、列表、讨论、链接等，每种类型的平均评分和评论数量 |
- **互动模式**：问题类、数字相关、情感类、个人分享、中性类等，附带互动指标 |
- **按小时划分的发布时间**：按平均评分排序的小时段 |
- **按天划分的发布时间**：按平均评分排序的日期 |
- **热门帖子**：评分最高的帖子，包括标题、评分和类型 |
- **建议**：基于分析结果提供的实用建议（最佳内容类型、互动模式、发布时间、推荐日期） |

## 安全性与限制

- **仅读取数据**：不会修改任何帖子、评论、投票或进行其他交互 |
- **速率限制**：每次请求之间有 3-8 秒的延迟 |
- **OAuth**：遵守 Reddit API 的每分钟 60 次请求限制 |
- **PullPush**：使用历史数据，数据可能滞后数周或数月