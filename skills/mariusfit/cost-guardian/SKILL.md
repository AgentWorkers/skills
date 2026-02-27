# cost-guardian — 人工智能与基础设施成本追踪工具

该工具用于追踪、分析并优化您的人工智能代理及基础设施的运行总成本，提供预算警报、支出预测以及具体的优化建议。

## 命令

### 初始化
```bash
python scripts/cost-guardian.py init
```
在 `~/.openclaw/workspace/costs/` 目录下创建配置文件和数据库。

### 记录成本支出
```bash
# Track API spend
python scripts/cost-guardian.py track --provider openai --amount 12.50 --currency USD --period monthly --category api

# Track infrastructure cost
python scripts/cost-guardian.py track --provider hetzner --amount 5.00 --currency EUR --period monthly --category hosting

# Track one-time cost
python scripts/cost-guardian.py track --provider cloudflare --amount 10.00 --currency USD --period once --category domain

# Track electricity
python scripts/cost-guardian.py track --provider electricity --amount 15.00 --currency EUR --period monthly --category power
```

### 从网关日志中扫描令牌使用情况
```bash
# Scan recent gateway logs for token consumption per model
python scripts/cost-guardian.py scan-tokens

# Scan specific days
python scripts/cost-guardian.py scan-tokens --days 7
```

### 设置预算
```bash
# Monthly budget
python scripts/cost-guardian.py budget --monthly 50.00 --currency EUR

# Budget with alert threshold (alert at 80%)
python scripts/cost-guardian.py budget --monthly 50.00 --alert-pct 80
```

### 成本报告
```bash
# Current month report
python scripts/cost-guardian.py report

# Weekly report
python scripts/cost-guardian.py report --period week

# JSON output
python scripts/cost-guardian.py report --json

# Specific month
python scripts/cost-guardian.py report --month 2026-02
```

### 优化建议
```bash
# Get optimization suggestions
python scripts/cost-guardian.py optimize

# JSON output
python scripts/cost-guardian.py optimize --json
```

### 预测支出
```bash
# Forecast next 3 months
python scripts/cost-guardian.py forecast

# Forecast next N months
python scripts/cost-guardian.py forecast --months 6

# JSON output
python scripts/cost-guardian.py forecast --json
```

### 管理订阅服务
```bash
# Add a subscription
python scripts/cost-guardian.py sub add --name "OpenRouter" --amount 20.00 --currency USD --cycle monthly --renews 2026-03-15 --category api

# List subscriptions
python scripts/cost-guardian.py sub list

# Remove a subscription
python scripts/cost-guardian.py sub remove --name "OpenRouter"

# Check upcoming renewals
python scripts/cost-guardian.py sub upcoming --days 14
```

### 状态仪表盘
```bash
# Quick status overview
python scripts/cost-guardian.py status

# JSON output  
python scripts/cost-guardian.py status --json
```

## 分类

- `api` — 人工智能模型 API 使用费用（如 OpenAI、Anthropic、OpenRouter 等）
- `hosting` — VPS 服务、云服务、域名、DNS
- `power` — 家用实验室的电力费用
- `subscription` — SaaS 订阅费用
- `hardware` — 一次性硬件购置费用
- `other` — 其他所有费用

## 输出格式

所有命令支持以下输出格式：
- **人类可读格式**（默认）—— 带颜色的终端输出
- **JSON 格式**（`--json`）—— 适用于程序化处理的结构化数据

## Cron 任务集成

您可以将以下 Cron 任务添加到 OpenClaw 中以实现自动成本追踪：
- 每日：`scan-tokens` 命令用于监控 API 使用情况
- 每周：`report --period week` 命令生成费用汇总报告
- 每月：`report` 命令 + `forecast` 命令进行全面分析
- 按需：`optimize` 命令用于降低成本

## 数据存储

所有数据存储在 `~/.openclaw/workspace/costs/` 目录下：
- `config.json` — 预算设置和偏好配置
- `costs.db` — SQLite 数据库（包含成本记录和订阅信息）

## 无依赖项

该工具完全基于 Python 3 标准库开发，无需安装任何第三方库（如 pip）。依赖的库包括 sqlite3、json、datetime 和 pathlib。