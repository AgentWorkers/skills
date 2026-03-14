---
name: self-improvement
description: 基于 OpenClaw-RL 研究（arxiv.org/abs/2603.10165）开发的通用代理自我提升技能。该技能能够捕捉用户反馈中的评价信号（+1/-1）以及指导性建议，并据此生成改进方案。
metadata:
  openclaw:
    emoji: 🧬
    homepage: https://adelpro.us.kg
---
# 自我提升技能

该技能使任何代理都能够通过类似PRM（Pull Request Management）的评估机制来学习并改进自身表现。

## 功能概述

- **收集反馈**：存储用户对代理输出的反馈信息。
- **评估反馈**：从用户反馈中提取评分（+1表示正面反馈，-1表示需要改进的地方）。
- **分析反馈**：分析用户提供的指导性建议（hint），找出其中的规律。
- **生成改进方案**：根据分析结果生成具体的改进措施。

## 设计理念（受OpenClaw-RL启发）

参考[OpenClaw-RL论文](https://arxiv.org/abs/2603.10165)：

> “下一个状态的信号同时包含了关于前一个行为的评估信息和指导性建议。”

该系统使用两种类型的信号：
1. **评估信号**：代理的输出是否有效？（二元评分）
2. **指导性信号**：代理应该如何改进？（用户提供的建议）

## 使用方法

### 收集反馈
```
SKILL:self-improvement --feedback "Great!" --job daily-report
SKILL:self-improvement --feedback "Add more stats" --job daily-report
```

### 获取反馈统计信息
```
SKILL:self-improvement --stats daily-report
```

### 生成改进方案
```
SKILL:self-improvement --improve daily-report
```

## 命令参数

| 参数 | 说明 | 示例 |
|-----|-------------|---------|
| `--job` | 任务/作业名称 | `daily-digest`, `weekly-recap` |
| `--feedback` | 用户反馈内容 | `"谢谢！"` 或 `"请添加更多X内容"` |
| `--score` | 手动评分（可选） | `1`, `0`, `-1` |
| `--stats` | 显示反馈统计信息 | `daily-digest` |
| `--improve` | 生成改进方案 | `daily-digest` |
| `--weekly` | 显示每周总结 | （可选） |

## 数据存储路径

数据存储在`memory/learning/agent-feedback.json`文件中：
```json
{
  "jobs": {
    "daily-digest": {
      "evaluations": [
        { "date": "2026-03-14", "score": 1, "hint": null },
        { "date": "2026-03-13", "score": -1, "hint": "add weekly star comparison" }
      ],
      "improvements": [
        { "date": "2026-03-14", "suggestion": "Add weekly star delta", "implemented": false }
      ]
    }
  }
}
```

## 定时任务集成

- **每日**：在上午9:30收集用户反馈。
- **每日**：在上午10:00生成改进方案。
- **每周**：在周六上午9:00生成每周总结。

## 示例工作流程

1. 用户接收每日反馈摘要。
2. 用户给出反馈：“很好！但是能否展示星形图（star trend）的统计结果？”
3. 系统收集反馈：评分=1，建议="展示星形图统计结果"。
4. 第二天，系统生成改进方案：
   - “添加过去7天的星形图对比功能”
   - “用户满意度：75%”
5. 代理自动更新提示语。

## 改进方案格式

改进方案的格式如下：
```
📈 Improvement Suggestions - {job}

Stats: 8 evaluations, avg score: 0.75

Top Hints:
1. "add weekly star changes" (2x)
2. "use table format" (1x)

Suggested Actions:
• Add 7-day star delta to GitHub section
• Use table-image-generator for stats

Status: 1 improvement pending
```

## 手动评估

如果无法获取用户反馈，可以手动对代理的表现进行评估：
```
Evaluate yesterday's output as: good/bad
```

## 相关技能

- **复合工程（Compound Engineering）**：用于深入分析用户会话数据。
- **代理进化器（Agent Evolver）**：该功能的旧称，可参考“自我提升”相关文档。