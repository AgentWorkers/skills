---
name: usage-export
version: 1.0.0
description: 将 OpenClaw 的使用数据导出为 CSV 格式，以便用于 Power BI 等分析工具。数据按活动类型、模型和渠道进行每小时汇总。
homepage: https://clawdhub.com/skills/usage-export
metadata: {"openclaw":{"emoji":"📊","category":"analytics","requires":{"bins":["python3"]}}}
---

# 使用数据导出

您可以将 OpenClaw 的使用数据导出为 CSV 文件，以便在 Power BI、Excel 或任何 BI 工具中进行分析。

## 功能介绍

- 扫描会话 JSONL 文件以获取使用数据
- 按 **小时** 和 **活动类型** 进行数据聚合
- 每天生成一个 CSV 文件
- 记录令牌使用情况、成本以及工具使用情况
- 包括主会话和子代理会话的数据

## 输出格式

CSV 文件会被保存在 `~/.clawdbot/exports/usage/YYYY-MM-DD.csv` 目录下：

```csv
timestamp_hour,date,hour,session_key,channel,model,provider,activity_type,request_count,input_tokens,output_tokens,cache_read_tokens,cache_write_tokens,total_tokens,cost_usd
2026-01-30T05:00:00Z,2026-01-30,5,agent:main:main,signal,claude-opus-4-5,anthropic,chat,3,24,892,14209,500,15625,0.12
2026-01-30T05:00:00Z,2026-01-30,5,agent:main:main,signal,claude-opus-4-5,anthropic,tool:exec,8,80,450,0,0,530,0.02
```

**有关列的详细定义，请参阅 [SCHEMA.md](SCHEMA.md)。**

## 安装

```bash
# Via ClawdHub
clawdhub install usage-export

# Or manually
mkdir -p ~/.openclaw/skills/usage-export
# Copy SKILL.md, SCHEMA.md, and scripts/ folder
```

## 使用方法

### 手动导出

```bash
# Export today's data
python3 {baseDir}/scripts/export.py --today

# Export specific date
python3 {baseDir}/scripts/export.py --date 2026-01-29

# Export date range
python3 {baseDir}/scripts/export.py --from 2026-01-01 --to 2026-01-31
```

### Cron 任务设置（推荐）

为了确保数据更新及时，建议使用 Cron 任务每小时执行一次导出操作：

```bash
# System crontab
0 * * * * python3 ~/.openclaw/skills/usage-export/scripts/export.py --today
```

或者通过 OpenClaw 的配置文件来设置导出任务：

```json
{
  "cron": {
    "jobs": [{
      "name": "usage-export",
      "schedule": { "kind": "cron", "expr": "0 * * * *" },
      "payload": { 
        "kind": "systemEvent", 
        "text": "Run usage export: python3 ~/.openclaw/skills/usage-export/scripts/export.py --today --quiet" 
      },
      "sessionTarget": "main"
    }]
  }
}
```

## 与 Power BI 的集成

1. 在 Power BI 中选择 **“获取数据”** → **文本/CSV**  
2. 指定路径为 `~/.clawdbot/exports/usage/`  
3. 使用文件夹源合并这些文件  
4. 然后您可以构建自己的数据仪表板！

### 建议的可视化图表类型

- **每日成本趋势**：按日期显示的折线图  
- **模型使用情况**：按模型显示的饼图  
- **活动热力图**：小时与活动类型的矩阵图  
- **渠道使用情况对比**：按渠道显示的条形图  
- **工具使用排名**：按请求次数排名前十的工具  

## 配置选项

环境变量（可选）：

| 变量          | 默认值       | 说明                          |
|----------------|------------|---------------------------------------------|
| `USAGE_EXPORT_DIR` | `~/.clawdbot/exports/usage` | 输出目录                          |
| `USAGE_EXPORT_SESSIONS` | `~/.clawdbot/agents` | 会话数据目录                          |

## 注意事项

- 所有时间戳均采用 UTC 格式  
- 成本列是基于配置的定价信息估算得出的（详情请参阅 SCHEMA.md）  
- 缓存的令牌数据仅适用于 Anthropic；其他服务提供商可能显示为 0  
- 新会话会在下一次导出时自动被收录到结果文件中