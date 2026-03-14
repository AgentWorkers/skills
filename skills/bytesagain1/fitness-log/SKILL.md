---
name: fitness-log
description: "**健身日志**  
——记录锻炼情况与进步的实用工具。  
这是一个专为个人日常使用设计的工具，用于跟踪和管理您的健康与锻炼计划。  
在需要记录锻炼数据或查看健身进展时，可随时使用该工具。"
runtime: python3
license: MIT
---
# 健身日志

健身日志 —— 跟踪你的锻炼记录和进步情况

## 为什么需要这个工具？

- 专为个人日常使用设计
- 无需任何外部依赖或账户
- 数据存储在本地，保护你的隐私
- 命令简单，但功能强大

## 命令列表

- `log` — <类型> <时长> [备注]  记录锻炼类型（如跑步、健身房锻炼、瑜伽、游泳、骑自行车）
- `weight` — <公斤>          记录体重
- `today` —                今天的活动记录
- `week` —                周度总结
- `history` — [数量]          锻炼历史记录（默认显示10条）
- `stats` —                总体统计数据
- `streak` —                连续锻炼天数记录
- `plan` — <目标>          生成锻炼计划
- `progress` —            体重变化图表
- `personal-best` —          个人最佳记录
- `export` — [格式]          导出数据（csv/json格式）
- `info` —                工具版本信息

## 快速入门

```bash
fitness_log.sh help
```

> **注意**：这是BytesAgain团队独立开发的工具，与任何第三方项目无关，也未基于任何第三方项目进行衍生。

---
由BytesAgain提供支持 | bytesagain.com | hello@bytesagain.com