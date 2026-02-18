---
name: Learn
slug: learn
version: 1.0.2
description: 通过间隔重复和主动回忆来构建和跟踪学习进度，适用于任何领域。
changelog: Fixed data folder to match slug, removed vague cron reference
metadata: {"clawdbot":{"emoji":"🎓","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 数据存储

```
~/learn/
├── topics/              # One folder per topic
│   └── {topic}/
│       ├── concepts.json   # Concepts with SR schedule
│       ├── notes.md        # Study notes
│       └── progress.md     # Mastery tracking
├── reviews/             # Due review queue
│   └── due.json
└── config.json          # Preferences
```

首次使用时执行以下操作：`mkdir -p ~/learn/{topics,reviews}`

## 功能范围

本技能包括：
- ✅ 在 `~/learn/` 目录下创建学习计划
- ✅ 使用间隔重复法来帮助用户记忆概念
- ✅ 生成用于巩固知识的测验
- ✅ 在用户需要复习时提醒他们（复习信息存储在 `~/learn/reviews/` 目录中）
- ❌ 未经允许，严禁访问外部学习平台
- ❌ 严禁将数据存储在 `~/learn/` 目录之外

## 快速参考

| 学习主题 | 对应文件 |
|-------|------|
| 认知原理 | `cognition.md` |
| 间隔重复法（数学学习） | `retention.md` |
| 验证方法 | `verification.md` |

## 核心规则

### 1. 工作流程
```
Goal → Plan → Study → Practice → Verify → Review
```

### 2. 仅采用主动复习方式
严禁被动复习。始终遵循以下步骤：
- 先提出问题，让用户尝试回答
- 然后展示正确答案
- 让用户对自己的回答进行评分（分为“容易”、“良好”、“困难”或“错误”）

### 3. 开始学习新主题的步骤
1. 用户说明他们想要学习的内容
2. 在 `~/learn/topics/{topic/` 目录下创建相应的文件夹
3. 将学习内容分解为具体的概念
4. 将这些概念添加到间隔重复学习队列中

### 4. 间隔重复学习机制
在 `concept.json` 文件中配置如下规则：
```json
{
  "concept_name": {
    "added": "2024-03-15",
    "interval_days": 1,
    "next_review": "2024-03-16",
    "ease_factor": 2.5,
    "reviews": 0
  }
}
```

每次复习后：
- 如果回答正确，增加复习间隔时间（乘以 `ease_factor` 值）
- 如果回答错误，将复习间隔重置为 1 天

### 5. 验证学习成果
在标记某个概念为“已掌握”之前：
- 生成 5 个与该概念相关的问题
- 用户必须答对 4 个或以上问题
- 将复习进度记录在 `progress.md` 文件中（该文件位于对应的主题文件夹内）

### 6. 配置设置
配置文件位于 `~/learn/config.json` 中：
```json
{
  "depth": "standard",
  "learner_type": "practical",
  "daily_review_limit": 20
}
```