---
name: finviz-crawler
description: 这是一个用于 finviz.com 的持续财务新闻爬虫工具，支持 SQLite 数据存储、文章提取和查询功能。适用于监控金融市场、构建新闻摘要或需要本地财务新闻数据库的场景。该工具可作为后台守护进程（daemon）或 systemd 服务运行。
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---
# finviz-crawler

## 为什么需要这个工具？

📰 **属于自己的金融新闻数据库**：大多数金融工具仅提供一次性查询的API接口。而这个工具会持续运行，将Finviz上的所有标题和文章保存到本地数据库中。你可以随时查询历史数据——没有API使用限制，也不会有任何数据缺失。

🆓 **无需API密钥或订阅**：它直接使用Crawl4AI和RSS协议从finviz.com抓取数据。Bloomberg、Reuters、Yahoo Finance和CNBC的文章都会被自动提取，完全免费。

🤖 **专为AI摘要生成而设计**：该工具输出的文本/JSON格式非常适合大型语言模型（LLM）进行解析。你可以将其与OpenClaw的定时任务结合使用，实现自动化的每日晨报、晚间总结或每周投资报告。

💾 **自动清理**：你可以配置工具自动删除旧文章（无论是从数据库中还是磁盘上）。设置`--expiry-days 30`可保留一个月的历史数据，设置为`0`则永久保存所有数据。

🔄 **守护进程架构**：作为后台服务运行，随OpenClaw的启动/停止而自动启动/停止。设置完成后无需人工干预。支持systemd（Linux）和launchd（macOS）系统。

## 安装

```bash
python3 scripts/install.py
```

该工具支持**macOS、Linux和Windows**系统。安装过程中会安装Python相关包（`crawl4ai`、`feedparser`），配置Playwright浏览器，并创建数据存储目录。

### 手动安装
```bash
pip install crawl4ai feedparser
crawl4ai-setup  # or: python -m playwright install chromium
```

## 使用方法

### 运行爬虫
```bash
# Default: ~/workspace/finviz/, 7-day expiry
python3 scripts/finviz_crawler.py

# Custom paths and settings
python3 scripts/finviz_crawler.py --db /path/to/finviz.db --articles-dir /path/to/articles/

# Keep 30 days of articles
python3 scripts/finviz_crawler.py --expiry-days 30

# Never auto-delete (keep everything)
python3 scripts/finviz_crawler.py --expiry-days 0

# Custom crawl interval (default: 300s)
python3 scripts/finviz_crawler.py --sleep 600
```

### 查询文章
```bash
# Last 24 hours of headlines
python3 scripts/finviz_query.py --hours 24

# Titles only (compact, good for LLM summarization)
python3 scripts/finviz_query.py --hours 12 --titles-only

# With full article content
python3 scripts/finviz_query.py --hours 12 --with-content

# List downloaded articles with content status
python3 scripts/finviz_query.py --list-articles --hours 24

# Database stats
python3 scripts/finviz_query.py --stats
```

### 管理股票代码
```bash
# List all tracked tickers
python3 scripts/finviz_query.py --list-tickers

# Add single ticker (auto-generates keywords from symbol)
python3 scripts/finviz_query.py --add-ticker NVDA

# Add with custom keywords
python3 scripts/finviz_query.py --add-ticker "NVDA:nvidia,jensen huang"

# Add multiple tickers (batch)
python3 scripts/finviz_query.py --add-ticker NVDA TSLA AAPL
python3 scripts/finviz_query.py --add-ticker "NVDA:nvidia,jensen" "TSLA:tesla,elon musk"

# Remove tickers (batch)
python3 scripts/finviz_query.py --remove-ticker NVDA TSLA

# Custom DB path
python3 scripts/finviz_query.py --list-tickers --db /path/to/finviz.db
```

股票代码信息存储在`finviz.db`数据库的`tickers`表中，与文章信息一起保存。爬虫会定期读取该表以确定需要抓取哪些股票代码的相关页面。

### 配置参数

| 参数 | CLI命令 | 环境变量 | 默认值 |
|---------|----------|---------|---------|
| 数据库路径 | `--db` | — | `~/workspace/finviz/finviz.db` |
| 文章存储目录 | `--articles-dir` | — | `~/workspace/finviz/articles/` |
| 爬取间隔 | `--sleep` | — | `300`（5分钟） |
| 文章过期时间 | `--expiry-days` | `FINVIZ_EXPIRY_DAYS` | 7天 |
| 时区 | — | `FINVIZ_TZ` 或 `TZ` | 系统默认时区 |

## 💬 聊天命令（通过OpenClaw代理）

安装此工具后，你可以通过以下命令在OpenClaw中快速查询相关信息：

| 命令 | 功能 |
|---------|--------|
| `/finviz list` | 显示被跟踪的股票代码 |
| `/finviz add NVDA, TSLA` | 添加股票代码到跟踪列表 |
| `/finviz remove NVDA` | 从跟踪列表中移除股票代码 |
| `/finviz stats` | 显示文章/股票代码的数量 |
| `/finviz help` | 显示可用命令 |

这些命令通过`finviz_query.py` CLI脚本在OpenClaw中执行。

## 📱 PrivateApp仪表盘

我们提供了一个配套的移动仪表盘：[PrivateApp](https://github.com/camopel/PrivateApp)。这是一个专为个人服务器设计的PWA（Progressive Web Application）仪表盘。

**Finviz**应用程序提供以下功能：  
- 带时间范围筛选功能的新闻浏览界面（12小时/24小时/一周）  
- 可根据股票代码筛选新闻  
- 根据需求生成由大型语言模型生成的摘要  

安装PrivateApp后，Finviz仪表盘即可直接使用，无需额外配置。

## 架构说明

**爬虫守护进程（`finviz_crawler.py`）：**
- 每5分钟从finviz.com/news.ashx抓取新闻标题  
- 通过Crawl4AI（Playwright）或RSS协议获取文章内容（对于需要付费访问的网站）  
- 通过检测机器人/付费墙来过滤无效内容  
- 对每个域名实施访问频率限制，并轮换用户代理  
- 使用SHA-256哈希值去除重复文章  
- 可配置文章的自动过期机制  
- 在接收到SIGTERM/SIGINT信号时自动关闭程序  

**查询工具（`finviz_query.py`）：**
- 仅使用SQLite进行只读查询（不涉及HTTP请求，仅依赖标准库）  
- 支持按时间范围筛选数据，并可导出文章标题或全部内容  
- 专为大型语言模型的摘要生成流程设计  

## 作为服务运行（可选）

### 在Linux系统中使用systemd
```ini
[Unit]
Description=Finviz News Crawler

[Service]
ExecStart=python3 /path/to/scripts/finviz_crawler.py --expiry-days 30
Restart=on-failure
RestartSec=30

[Install]
WantedBy=default.target
```

### 在macOS系统中使用launchd
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key><string>com.finviz.crawler</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>/path/to/scripts/finviz_crawler.py</string>
        <string>--expiry-days</string>
        <string>30</string>
    </array>
    <key>RunAtLoad</key><true/>
    <key>KeepAlive</key><true/>
</dict>
</plist>
```

## 数据存储结构
```
~/workspace/finviz/
├── finviz.db          # SQLite: articles + tickers (single DB)
├── articles/          # Full article content as .md files
│   ├── market/        # General market headlines
│   ├── nvda/          # Per-ticker articles
│   └── tsla/
└── summaries/         # LLM summary cache (.json)
```

## 定时任务集成

你可以将此工具与OpenClaw的定时任务结合使用，实现自动化的数据处理：  
```
Schedule: 0 6 * * * (6 AM daily)
Task: Query last 24h → LLM summarize → deliver to Matrix/Telegram/Discord
```