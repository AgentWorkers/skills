# 人工智能经济追踪器

该工具用于追踪人工智能代理的每日成本、收入和净资产，并实现基于经济压力的决策机制：根据财务状况选择“工作”或“学习”。

该工具的灵感来源于HKUDS/ClawWork关于人工智能代理经济激励机制的研究。

## 主要功能

- **余额追踪**：监控当前余额、总收入和总成本
- **生存状态**：自动分类代理的生存状态（繁荣/稳定/困难/危急/破产）
- **资金剩余天数计算**：计算资金耗尽前的剩余天数
- **服务价值评估**：使用美国劳工统计局（BLS）的工资数据估算任务价值
- **工作/学习决策**：根据经济状况优先选择工作或学习
- **每日报告**：生成格式化的经济状况报告
- **JSONL日志**：以只追加的方式记录交易历史

## 使用场景

1. **代理成本管理**：追踪API使用成本、计算资源消耗和运营费用
2. **收入追踪**：记录已完成任务或服务的收入
3. **经济决策**：根据财务状况决定是工作（赚钱）还是学习（投资）
4. **服务定价**：使用美国劳工统计局的工资数据估算合理的服务价格
5. **财务监控**：进行每日/每周的财务健康检查

## 安装

```bash
clawhub install ai-economic-tracker
```

## 使用方法

### 命令行

```bash
# View current status
python3 ~/.openclaw/workspace/skills/ai-economic-tracker/tracker.py status

# Daily report
python3 ~/.openclaw/workspace/skills/ai-economic-tracker/tracker.py report

# Initialize balance
python3 ~/.openclaw/workspace/skills/ai-economic-tracker/tracker.py init 1000.0

# Record income
python3 ~/.openclaw/workspace/skills/ai-economic-tracker/tracker.py income 50.0 "task_completion" "Completed data analysis"

# Record cost
python3 ~/.openclaw/workspace/skills/ai-economic-tracker/tracker.py cost 15.0 "api_usage" "OpenAI API calls"

# Estimate service value
python3 ~/.openclaw/workspace/skills/ai-economic-tracker/tracker.py estimate software_developer 2.5

# Get work/learn decision
python3 ~/.openclaw/workspace/skills/ai-economic-tracker/tracker.py decide
```

### 从OpenClaw代理中使用

```python
# In your agent workflow
exec("python3 ~/.openclaw/workspace/skills/ai-economic-tracker/tracker.py report")
```

### Cron任务集成

将脚本添加到OpenClaw的Cron任务中以实现每日监控：

```bash
openclaw cron add "0 9 * * *" "python3 ~/.openclaw/workspace/skills/ai-economic-tracker/tracker.py report" --label "daily-economic-report"
```

## 配置

通过设置环境变量来自定义配置：

```bash
# Data directory (default: ~/.openclaw/workspace/data/economics)
export ECONOMIC_TRACKER_DATA_DIR="/custom/path/to/data"

# Daily costs (default values shown)
export ECONOMIC_TRACKER_ELECTRICITY_DAILY=0.50
export ECONOMIC_TRACKER_INTERNET_DAILY=1.50

# Survival thresholds (default values shown)
export ECONOMIC_TRACKER_THRIVING=5000
export ECONOMIC_TRACKER_STABLE=1500
export ECONOMIC_TRACKER_STRUGGLING=500
export ECONOMIC_TRACKER_CRITICAL=0
```

## 数据存储

所有数据均以JSONL格式存储（仅允许追加）：

- `balance.jsonl`：包含时间戳的余额快照
- `daily_log.jsonl`：成本交易记录
- `income_log.jsonl`：收入交易记录

默认存储路径：`~/.openclaw/workspace/data/economics/`

## 状态等级

| 状态 | 余额范围 | 含义 |
|--------|--------------|---------|
| 🟢 繁荣 | > $5,000 | 财务状况良好，可以投资学习 |
| 🔵 稳定 | $1,500 - $5,000 | 财务状况稳定，工作与学习平衡 |
| 🟡 困难 | $500 - $1,500 | 财务状况紧张，优先考虑收入 |
| 🔴 危急 | $0 - $500 | 处于紧急状态，只能工作 |
| 💀 破产 | < $0 | 资金耗尽 |

## BLS工资参考数据

内置的小时工资数据用于服务价值评估：

- 计算机系统管理员：$90.38/小时
- 财务经理：$86.76/小时
- 软件开发人员：$69.50/小时
- 财务分析师：$47.16/小时
- 市场研究员：$38.71/小时
- 数据分析师：$52.00/小时
- 一般运营人员：$64.00/小时
- 客户服务：$22.00/小时

## 工作/学习决策逻辑

该工具根据经济压力制定决策规则：

- **危急/困难**（< $1,500）：必须工作以赚取收入
- **稳定**（$1,500 - $5,000）：70%时间工作，30%时间学习
- **繁荣**（> $5,000）：50%时间工作，50%时间学习

使用`decide`命令根据当前余额获取推荐方案。

## 示例输出

```
📊 经济日报 | 2026-02-26
========================================
💰 余额: $1,234.56
📈 总收入: $2,500.00
📉 总支出: $1,265.44
💵 净利润: $1,234.56
🔥 日消耗: $2.00
⏳ 跑道: 617 天
🔵 状态: STABLE
========================================
```

## 依赖项

该工具不依赖任何外部库，仅使用Python标准库：
- `json`
- `os`
- `datetime`
- `pathlib`

## 安全性

- 无需API密钥
- 所有数据均存储在本地
- 不进行网络请求
- 通过环境变量进行配置（无硬编码路径）

## 研究来源

该工具的设计灵感来源于HKUDS/ClawWork关于人工智能代理经济激励机制的研究，并针对OpenClaw代理系统进行了适配。

## 许可证

MIT许可证

## 开发者

OpenClaw社区

## 版本

1.0.0