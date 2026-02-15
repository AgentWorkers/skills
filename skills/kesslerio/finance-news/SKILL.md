---
name: finance-news
description: "**市场新闻简报（含AI摘要）**  
适用于需要了解股票新闻、市场动态、投资组合表现、晨间/晚间简报、财经头条或价格警报的场景。支持美国/欧洲/日本市场，可通过WhatsApp发送，并提供英文/德文版本。  

**功能特点：**  
- 自动生成新闻摘要（利用AI技术）  
- 支持多市场数据（美国、欧洲、日本）  
- 通过WhatsApp发送通知  
- 提供多种语言版本（英文/德文）  

**适用场景：**  
- 股票投资者  
- 财务分析师  
- 投资顾问  
- 市场研究人员  

**使用说明：**  
- 根据需求选择相关市场数据  
- 设置发送频率（每日/每周）  
- 自定义通知内容（新闻标题、摘要等）  
- 确保接收者收到及时、准确的市场信息  

**示例：**  
- 当客户询问股票市场情况时，可立即发送包含AI摘要的市场新闻简报。  
- 适用于晨间会议或晚间总结，帮助团队快速了解市场动态。  

**优势：**  
- 提高信息传递效率  
- 保证信息准确性  
- 适应不同语言需求  

**注意事项：**  
- 请确保系统已更新至最新版本，以充分利用AI摘要功能。  
- 如需调整通知内容或格式，请联系技术支持。"
---

# 金融新闻技能

该技能提供基于人工智能的市场新闻简报服务，支持自定义语言输出和自动推送功能。

## 首次设置

运行交互式设置向导，配置您的新闻来源、推送渠道和调度时间：

```bash
finance-news setup
```

向导将引导您完成以下步骤：
- 📰 **RSS订阅源：** 启用/禁用《华尔街日报》（WSJ）、《巴伦周刊》（Barron’s）、CNBC、雅虎财经（Yahoo Finance）等新闻源
- 📊 **市场区域：** 选择美国（US）、欧洲（Europe）、日本（Japan）或亚洲（Asia）市场
- 📤 **推送方式：** 配置WhatsApp或Telegram群组
- 🌐 **语言设置：** 设置默认语言（英语/德语）
- ⏰ **调度时间：** 设置早晨或晚上的推送时间

您还可以自定义其他详细设置：

```bash
finance-news setup --section feeds     # Just RSS feeds
finance-news setup --section delivery  # Just delivery channels
finance-news setup --section schedule  # Just cron schedule
finance-news setup --reset             # Reset to defaults
finance-news config                    # Show current config
```

## 快速入门

```bash
# Generate morning briefing
finance-news briefing --morning

# View market overview
finance-news market

# Get news for your portfolio
finance-news portfolio

# Get news for specific stock
finance-news news AAPL
```

## 功能亮点

### 📊 市场覆盖范围
- **美国市场：** 标准普尔500指数（S&P 500）、道琼斯指数（Dow Jones）、纳斯达克指数（NASDAQ）
- **欧洲市场：** 德国DAX指数、法国STOXX 50指数、英国FTSE 100指数
- **日本市场：** 日经225指数（Nikkei 225）

### 📰 新闻来源
- **高级订阅源：** 《华尔街日报》（WSJ）、《巴伦周刊》（提供RSS订阅）
- **免费来源：** CNBC、雅虎财经（Yahoo Finance）、Finnhub
- **投资组合相关新闻：** 来自雅虎财经的特定股票代码的新闻

### 🤖 人工智能分析
- 采用Gemini技术进行新闻分析
- 支持多种语言（英语/德语）
- 简报形式多样：摘要、分析报告或仅显示标题

### 📅 自动推送
- **推送时间：**
  - 早晨：美国市场开盘时间（太平洋时间6:30）
  - 晚上：美国市场收盘时间（太平洋时间13:00）
- **推送方式：** 通过WhatsApp群组发送

## 命令操作

### 生成新闻简报

```bash
# Morning briefing (English is default)
finance-news briefing --morning

# Evening briefing with WhatsApp delivery
finance-news briefing --evening --send --group "Market Briefing"

# German language option
finance-news briefing --morning --lang de

# Analysis style (more detailed)
finance-news briefing --style analysis
```

### 市场数据查询

```bash
# Market overview (indices + top headlines)
finance-news market

# JSON output for processing
finance-news market --json
```

### 投资组合管理

```bash
# List portfolio
finance-news portfolio-list

# Add stock
finance-news portfolio-add NVDA --name "NVIDIA Corporation" --category Tech

# Remove stock
finance-news portfolio-remove TSLA

# Import from CSV
finance-news portfolio-import ~/my_stocks.csv

# Interactive portfolio creation
finance-news portfolio-create
```

### 股票代码相关新闻

```bash
# News for specific stock
finance-news news AAPL
finance-news news TSLA
```

## 配置信息

### 投资组合数据文件格式

文件路径：`~/clawd/skills/finance-news/config/portfolio.csv`

```csv
symbol,name,category,notes
AAPL,Apple Inc.,Tech,Core holding
NVDA,NVIDIA Corporation,Tech,AI play
MSFT,Microsoft Corporation,Tech,
```

### 新闻来源配置

文件路径：`~/clawd/skills/finance-news/config/config.json`  
（旧版本备用路径：`config/sources.json`）
- 包括《华尔街日报》（WSJ）、《巴伦周刊》（Barron’s）、CNBC、雅虎财经的RSS订阅源信息  
- 各地区的市场指数数据  
- 语言设置  

## 定时任务管理

### 通过OpenClaw进行配置

```bash
# Add morning briefing cron job
openclaw cron add --schedule "30 6 * * 1-5" \
  --timezone "America/Los_Angeles" \
  --command "bash ~/clawd/skills/finance-news/cron/morning.sh"

# Add evening briefing cron job
openclaw cron add --schedule "0 13 * * 1-5" \
  --timezone "America/Los_Angeles" \
  --command "bash ~/clawd/skills/finance-news/cron/evening.sh"
```

### 手动设置（crontab）

```cron
# Morning briefing (6:30 AM PT, weekdays)
30 6 * * 1-5 bash ~/clawd/skills/finance-news/cron/morning.sh

# Evening briefing (1:00 PM PT, weekdays)
0 13 * * 1-5 bash ~/clawd/skills/finance-news/cron/evening.sh
```

## 示例输出内容

```markdown
🌅 **Börsen-Morgen-Briefing**
Dienstag, 21. Januar 2026 | 06:30 Uhr

📊 **Märkte**
• S&P 500: 5.234 (+0,3%)
• DAX: 16.890 (-0,1%)
• Nikkei: 35.678 (+0,5%)

📈 **Dein Portfolio**
• AAPL $256 (+1,2%) — iPhone-Verkäufe übertreffen Erwartungen
• NVDA $512 (+3,4%) — KI-Chip-Nachfrage steigt

🔥 **Top Stories**
• [WSJ] Fed signalisiert mögliche Zinssenkung im März
• [CNBC] Tech-Sektor führt Rally an

🤖 **Analyse**
Der S&P zeigt Stärke. Dein Portfolio profitiert von NVDA's 
Momentum. Fed-Kommentare könnten Volatilität auslösen.
```

## 集成方式

### 与OpenBB集成

该技能可与其他工具集成，例如OpenBB：
```bash
# Get detailed quote, then news
openbb-quote AAPL && finance-news news AAPL
```

### 与OpenClaw Agent集成
当用户询问以下问题时，OpenClaw Agent会自动使用该技能提供相关信息：
- “市场当前情况如何？”
- “我的投资组合的最新新闻”
- “生成早晨新闻简报”
- “苹果公司（AAPL）的最新动态是什么？”

### 与Lobster集成

您可以通过[Lobster](https://github.com/openclaw/lobster)工作流引擎来调度和优化新闻推送流程：

```bash
# Run with approval before WhatsApp send
lobster "workflows.run --file workflows/briefing.yaml"

# With custom args
lobster "workflows.run --file workflows/briefing.yaml --args-json '{\"time\":\"evening\",\"lang\":\"en\"}'"
```

详细文档请参阅`workflows/README.md`。

## 相关文件

```
skills/finance-news/
├── SKILL.md              # This documentation
├── Dockerfile            # NixOS-compatible container
├── config/
│   ├── portfolio.csv     # Your watchlist
│   ├── config.json       # RSS/API/language configuration
│   ├── alerts.json       # Price target alerts
│   └── manual_earnings.json  # Earnings calendar overrides
├── scripts/
│   ├── finance-news      # Main CLI
│   ├── briefing.py       # Briefing generator
│   ├── fetch_news.py     # News aggregator
│   ├── portfolio.py      # Portfolio CRUD
│   ├── summarize.py      # AI summarization
│   ├── alerts.py         # Price alert management
│   ├── earnings.py       # Earnings calendar
│   ├── ranking.py        # Headline ranking
│   └── stocks.py         # Stock management
├── workflows/
│   ├── briefing.yaml     # Lobster workflow with approval gate
│   └── README.md         # Workflow documentation
├── cron/
│   ├── morning.sh        # Morning cron (Docker-based)
│   └── evening.sh        # Evening cron (Docker-based)
└── cache/                # 15-minute news cache
```

## 所需依赖库/工具

- Python 3.10及以上版本  
- `feedparser`（用于解析RSS数据）：`pip install feedparser`  
- Gemini CLI：`brew install gemini-cli`  
- OpenBB（用于获取股票报价）  
- OpenClaw消息传递工具（用于通过WhatsApp发送通知）

## 常见问题解决方法

### Gemini无法正常使用
- 检查网络连接是否正常  
- 《华尔街日报》/《巴伦周刊》的部分内容可能需要订阅才能访问  
- 免费新闻源（CNBC、雅虎财经）通常可以正常使用  

### WhatsApp推送失败
- 确认WhatsApp群组存在且机器人具有访问权限  
- 查看`openclaw doctor`工具以获取WhatsApp推送状态信息