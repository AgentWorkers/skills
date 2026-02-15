---
name: Study
description: 安排学习课程，管理学习资料，为考试做准备，并跟踪学习进度，以取得学业上的成功。
metadata: {"clawdbot":{"emoji":"📚","os":["linux","darwin"]}}
---

## 设置

首次使用时，请创建工作区：
```bash
./scripts/init-workspace.sh ~/study
```

## 工作流程

```
Plan Semester → Weekly Schedule → Daily Sessions → Review → Exam Prep
```

**规则：**
- 会话的输出（总结、闪卡）必须由学生自己创建——人工智能仅提供辅助工具，不生成内容。
- 每次会话都必须强制进行主动回忆（详见 `techniques.md`）。
- 根据学科类型调整学习策略（详见 `subjects.md`）。
- 记录截止日期和考试时间（详见 `scripts/`）。

## 配置

在 `config.json` 中设置：
- `level`：`high-school` | `undergraduate` | `graduate`
- `subjects`：`[{ name, type, exam_date, weekly_hours }]`
- `technique`：`pomodoro` | `timeblock` | `flexible`

## 脚本（强制执行）

| 脚本 | 用途 |
|--------|---------|
| `init-workspace.sh` | 创建学习工作区 |
| `add-subject.sh` | 添加带有考试日期的学科 |
| `session.sh` | 启动定时学习会话 |
| `plan-week.sh` | 生成每周学习计划 |
| `exam-prep.sh` | 创建考试准备计划 |
| `progress.sh` | 显示各科目的完成情况 |
| `deadlines.sh` | 列出即将到来的截止日期 |

参考资料：`techniques.md`（学习方法）、`materials.md`（内容类型）、`exams.md`（考试准备）、`planning.md`（时间管理）、`subjects.md`（学科策略）、`assessments.md`（评估方式）。  
相关脚本：`scripts/init-workspace.sh`、`scripts/add-subject.sh`、`scripts/session.sh`、`scripts/plan-week.sh`、`scripts/exam-prep.sh`、`scripts/progress.sh`、`scripts/deadlines.sh`。

---

### 学科偏好
<!-- 每个学科的学习风格 |

### 考试历史
<!-- 过去的考试表现记录 |

---
*空白部分请根据实际情况填写。*