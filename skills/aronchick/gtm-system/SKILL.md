# GTM 跟踪系统

这是一个专为 Expanso/Prometheus 设计的 Go-To-Market（市场推广）跟踪系统。

## 所在位置
`/home/daaronch/.openclaw/workspace/gtm-system/`

## CLI 工具
`python3 /home/daaronch/.openclaw/workspace/gtm-system/scripts/gtm.py [命令]`

## 快速命令

### 日常操作
```bash
# Get today's actions and priorities
python3 scripts/gtm.py actions

# Generate digest for Telegram
python3 scripts/gtm.py digest

# View pipeline
python3 scripts/gtm.py pipeline

# List unprocessed signals
python3 scripts/gtm.py signals
```

### 联系人管理
```bash
# Add a contact
python3 scripts/gtm.py add-contact "Name" "email@co.com" --company "Company" --role "CTO"

# List contacts
python3 scripts/gtm.py contacts
```

### 机会管理
```bash
# Create opportunity
python3 scripts/gtm.py add-opp "Company Name" --contact 1 --description "Interested in Bacalhau" --priority 3

# Move stage (awareness → interest → evaluation → negotiation → closed_won/closed_lost)
python3 scripts/gtm.py move-stage 1 evaluation

# Log an interaction
python3 scripts/gtm.py log "Had demo call, very interested" --opp 1
```

### 提醒设置
```bash
# Set a reminder
python3 scripts/gtm.py remind "Send pricing proposal" --opp 1 --date 2024-02-15

# Complete a reminder
python3 scripts/gtm.py complete 1
```

### 爬取数据
```bash
# Run all crawlers (HN, Reddit, GitHub)
python3 scripts/gtm.py crawl

# Run specific crawlers
python3 scripts/gtm.py crawl --sources hn,github

# Mark signal as processed
python3 scripts/gtm.py process-signal 1
```

### 关键词管理
```bash
# Add a tracking keyword
python3 scripts/gtm.py add-keyword "new-keyword" --category domain --weight 1.5
```

## 流程阶段
1. **认知阶段**（Awareness）：客户知道我们的存在
2. **兴趣阶段**（Interest）：表现出兴趣，初步联系
3. **评估阶段**（Evaluation）：积极评估，提供演示或试用
4. **谈判阶段**（Negotiation）：讨论条款和价格
5. **成交阶段**（ClosedWon）：交易成功完成
6. **失败阶段**（ClosedLost）：交易失败

## 数据库位置
`/home/daaronch/.openclaw/workspace/gtm-system/data/gtm.db`（SQLite 数据库）

## 自然语言查询
当用户询问关于 GTM、销售流程或机会的相关信息时，可以使用 CLI 来获取数据并生成摘要：
- “我的销售流程中有哪些机会？” → 运行 `pipeline` 命令
- “今天有需要跟进的事项吗？” → 运行 `actions` 命令
- “添加一个联系人...” → 使用 `add-contact` 命令
- “检查新的销售机会” → 先运行 `crawl` 命令，再运行 `signals` 命令