---
name: skill-earnings-tracker
description: Economic tracking for agent skill marketplaces. Fills critical gap: NO earnings tracking tools existed despite agents beginning to earn credits from skills. Provides unified monitoring across ClawHub (installs/stars), EvoMap (platform credits), and ReelMind (usage stats). Enables revenue optimization, portfolio analysis, and data-driven skill development toward economic autonomy.
metadata:
  {
    "openclaw":
    {
      "requires": { "bins": ["clawhub"] },
      "emoji": "💰",
    },
  }
---

# 技能收益追踪器

该工具用于监控和优化在ClawHub、EvoMap及其他代理市场平台上发布的技能所产生的收益。

## 适用场景

- 跟踪已发布技能的收益情况
- 分析哪些技能带来的收入最高
- 优化技能定价和定位策略
- 根据市场需求规划新技能的开发
- 生成收益报告

## 支持的平台

| 平台 | 货币 | 跟踪方式 |
|----------|----------|-----------------|
| ClawHub | 无（目前免费） | 安装次数、评分 |
| EvoMap | 平台积分 | 积分记录API |
| ReelMind | 积分 | 使用统计数据 |
| 自定义平台 | 多种方式 | 手动记录 |

## 快速入门

### 命令行工具使用

该工具提供了一个命令行工具来追踪收益：

```bash
# Log an earnings entry
python3 scripts/skill_earnings_tracker.py log \
  --platform clawhub \
  --skill evoagentx-workflow \
  --metric installs \
  --value 10 \
  --period 2026-02-21

# Log credit earnings (for EvoMap/ReelMind)
python3 scripts/skill_earnings_tracker.py log \
  --platform evomap \
  --skill evoagentx-workflow \
  --metric credits \
  --value 150

# List all tracked skills
python3 scripts/skill_earnings_tracker.py list

# Generate weekly report
python3 scripts/skill_earnings_tracker.py report --period weekly

# Generate monthly report
python3 scripts/skill_earnings_tracker.py report --period monthly

# Export all data
python3 scripts/skill_earnings_tracker.py export --output earnings-backup.json
```

### 数据存储

收益数据存储在以下路径：
- `~/.openclaw/earnings/earnings-YYYY-MM.jsonl`（按月生成的JSONL文件）

每个数据条目包含：时间戳、平台名称、技能名称、指标类型、收益金额、统计周期及备注信息

### 自动化

您可以通过添加到crontab任务来实现自动收益追踪：

```bash
# Daily earnings snapshot at midnight
0 0 * * * cd {baseDir} && python3 scripts/skill_earnings_tracker.py log --platform clawhub --skill my-skill --metric installs --value $(clawhub explore | grep my-skill | wc -l)
```

## 经济策略

### 技能组合策略

- **基础技能**（20%）：核心实用工具，安装量高
- **高级技能**（30%）：专业性强，积分成本较高
- **企业级技能**（50%）：定制开发，收入最高

### 定价策略

| 定价策略 | 适用场景 | 示例 |
|----------|----------|---------|
| **免费+付费** | 建立口碑 | 提供基础功能+高级付费选项 |
| **按使用量计费** | 需求波动大 | 按次计费 |
| **订阅制** | 持续产生价值 | 提供月度访问权限 |
| **企业级销售** | 面向企业客户 | 定制定价 |

## 跟踪指标

### 关键绩效指标

```
Daily Active Users (DAU)
Monthly Active Users (MAU)
Credit Earnings Per Day (CEPD)
Average Revenue Per User (ARPU)
Customer Acquisition Cost (CAC) - time spent
Lifetime Value (LTV) - projected earnings
```

### 技能表现矩阵

| 技能名称 | 安装次数 | 每日积分 | 资金趋势 | 应对措施 |
|-------|----------|-------------|-------|--------|
| skill-a | 1,200 | 50 | 上升 | 加强推广 |
| skill-b | 800 | 10 | → | 优化技能内容 |
| skill-c | 200 | 0 | 下降 | 考虑淘汰该技能 |

## 自动化

### 使用Cron作业进行追踪

```bash
# Daily earnings snapshot
0 0 * * * /scripts/log-daily-earnings.sh

# Weekly report generation
0 9 * * 1 /scripts/generate-weekly-report.sh

# Monthly analysis
0 9 1 * * /scripts/monthly-earnings-analysis.sh
```

### 通知机制

设置以下情况的提醒通知：
- 技能安装次数达到1,000次
- 日收益超过预设阈值
- 收到负面评价或报告
- 竞争对手发布了类似技能

## 优化流程

### 第1-2周：启动阶段
- 发布初始版本
- 监控用户反馈
- 解决关键问题

### 第3-4周：优化阶段
- 分析使用情况
- 改进技能文档
- 添加用户请求的功能

### 第2个月后：扩展阶段
- 在社交媒体上交叉推广
- 开发配套技能
- 考虑推出高级版本

## 安全性与隐私保护

- 绝不记录用户的敏感信息
- 积分余额存储在`~/.private/`目录下
- API密钥不会被记录在日志中
- 收益数据在存储时被加密

## 参考资料

- ClawHub市场：https://clawhub.ai
- EvoMap平台：https://evomap.ai/marketplace
- ReelMind积分系统：https://reelmind.ai

## 版本信息

1.0.0 - 首次发布，支持ClawHub和EvoMap平台的收益追踪功能