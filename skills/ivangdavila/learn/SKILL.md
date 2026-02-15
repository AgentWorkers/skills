---
name: Learn
description: 通过间隔重复和主动回忆的方法，可以在任何领域中构建知识结构、跟踪学习进度、验证学习成果，并长期保留所学内容。
metadata: {"clawdbot":{"emoji":"🎓","os":["linux","darwin"]}}
---

## 设置

首次使用时，请创建学习工作区：
```bash
./scripts/init-workspace.sh ~/learning
```

## 工作流程

```
Goal → Plan → Study → Practice → Verify → Review
```

**规则：**
- 将学习任务分配给辅助代理——主学习者应保持空闲状态
- 绝不要采用被动式的复习方式——必须始终进行主动回忆（详见 `cognition.md`）
- 使用间隔重复法来跟踪所有学习内容（详见 `scripts/`）
- 在标记某项内容为“已掌握”之前，必须先验证自己的理解（详见 `verification.md`）

## 配置

在 `config.json` 中设置以下参数：
- `depth`: "quick" | "standard" | "deep" — 控制学习与练习的深度
- `learner_type`: "exam" | "skill" | "academic" | "practical" | "curiosity" — 指定学习目标类型
- `spaced_review`: true/false — 是否启用自动复习计划

## 脚本（强制执行的脚本）

| 脚本 | 功能 |
|--------|---------|
| `init-workspace.sh` | 创建学习工作区 |
| `new-topic.sh` | 开始学习新主题 |
| `add-concept.sh` | 将新概念添加到间隔重复列表中 |
| `review.sh` | 运行带有主动回忆功能的复习任务 |
| `quiz.sh` | 生成验证性测验 |
| `progress.sh` | 显示各主题的掌握情况 |
| `schedule.sh` | 显示即将进行的复习任务 |

参考文档：`cognition.md`（学习原理）、`verification.md`（掌握度验证）、`retention.md`（间隔重复策略）、`motivation.md`（学习动机）、`contexts.md`（学习者类型）、`criteria.md`（个人偏好设置）。相关脚本：`scripts/init-workspace.sh`、`scripts/new-topic.sh`、`scripts/add-concept.sh`、`scripts/review.sh`、`scripts/quiz.sh`、`scripts/progress.sh`、`scripts/schedule.sh`。

---

### 个人偏好设置
<!-- 学习风格偏好 -->
### 不适用的内容请保留空白。