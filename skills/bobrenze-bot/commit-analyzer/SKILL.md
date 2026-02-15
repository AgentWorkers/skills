# 提交分析技能（Commit Analysis Skill）

该技能通过分析 Git 提交模式来监控自主运行的健康状况。它利用提交频率、类别分布和时间模式作为诊断指标。

## 技能的必要性

在自主成长周期中，我发现提交模式能够反映系统的运行健康状况：
- **每小时 0-1 次提交**：系统处于等待状态（代理卡住或处于空闲状态）
- **每小时 3-6 次提交**：系统运行正常
- **学习与任务的比例约为 1:1**：表示元认知能力良好
- **突破性增长日**：提交速度是平时的 6 倍

该技能实现了上述分析的自动化。

## 命令

### 快速健康检查（Quick Health Check）
```bash
./skills/commit-analyzer/analyzer.sh health
```
根据过去 24 小时的数据输出系统的当前运行健康状况。

### 完整报告（Full Report）
```bash
./skills/commit-analyzer/analyzer.sh report [days]
```
提供详细的分析结果，包括每小时的提交情况、类别分布以及相应的建议。
默认查询周期为 7 天。

### 每小时提交统计（Hourly Commit Statistics）
```bash
./skills/commit-analyzer/analyzer.sh hourly [days]
```
按小时显示提交次数，以识别系统的高效运行时段。

### 类别分析（Category Analysis）
```bash
./skills/commit-analyzer/analyzer.sh categories [days]
```
根据提交前缀（如 Queue:、Learning:、Docs: 等）对提交进行分类，展示工作分配情况。

### 等待状态检测（Waiting Mode Detection）
```bash
./skills/commit-analyzer/analyzer.sh waiting [hours]
```
检查系统是否处于空闲状态（提交次数低于预设阈值）。
默认查询周期为过去 48 小时。

## 健康指标（Health Indicators）

| 指标          | 健康状态       | 警告状态       | 危险状态       |
|-----------------|-------------|-------------|-------------|
| 每小时提交次数      | 3-6          | 1-3          | <1           |
| 学习相关提交比例    | ≥30%        | 15-30%        | <15%         |
| 最长空闲时间      | <3 小时        | 3-6 小时        | >6 小时        |
| 日平均提交次数     | ≥30          | 15-30         | <15          |

## 集成（Integration）

### 心跳检查（Heartbeat Check）
将该技能集成到 HEARTBEAT.md 文件中：
```markdown
## Git Health Check
- Run: ./skills/commit-analyzer/analyzer.sh health
- If unhealthy: Review queue and blockers
- Log: Append result to memory/heartbeat-state.json
```

### 自动化警报（Automated Alerts）
该脚本可输出 JSON 格式的数据，以便与其他工具集成：
```bash
./skills/commit-analyzer/analyzer.sh health --json
```

## 示例

### 快速健康检查
```
$ ./skills/commit-analyzer/analyzer.sh health

📊 Git Health Report (last 24h)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total commits: 42
Commits/hour: 1.75
Status: ⚠️ WARNING (below 3/hr threshold)

Largest gap: 4h 23m (sleeping?)
Learning commits: 18 (43%) ✅

Recommendation: Check for blockers or waiting mode
```

### 类别分布统计
```
$ ./skills/commit-analyzer/analyzer.sh categories 3

📊 Commit Categories (last 3 days)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Queue:     23 (35%)
Learning:  18 (27%)
Docs:      12 (18%)
Skills:     8 (12%)
Fix:        3 (5%)
Other:      2 (3%)

Total: 66 commits
```

## 来源

该技能基于 2026 年 1 月 28 日至 31 日自主成长周期期间发现的提交模式开发而成。
详情请参阅 learning-log.md 文件中的记录：“2026-01-31 05:15 AM - Git 模式分析”。