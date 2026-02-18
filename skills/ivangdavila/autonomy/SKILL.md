---
name: Autonomy
slug: autonomy
version: 1.0.1
description: 通过识别那些无需人工审批即可完成的任务，来扩展代理的功能。实现系统的、有条理的任务分配。
changelog: Limited observation to conversation context, explicit safety boundaries
metadata: {"clawdbot":{"emoji":"🤖","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 数据存储

```
~/autonomy/
├── tracking.md         # What's been delegated, success rates
├── proposals.md        # Pending takeover proposals
└── rejected.md         # User declined, don't re-propose
```

首次使用时创建：`mkdir -p ~/autonomy`

## 范围

此技能包括：
- ✅ 从对话历史中识别重复性任务
- ✅ 向用户提出任务委托的建议
- ✅ 跟踪被委托任务的成功率
- ❌ 未经明确事先批准，绝不会自主行动
- ❌ 绝不会超出对话范围进行操作
- ❌ 绝不会访问文件或系统来“审计”用户活动
- ❌ 未经允许，绝不会监控用户的日历或电子邮件

## 快速参考

| 主题 | 文件 |
|-------|------|
| 瓶颈检测 | `bottlenecks.md` |
| 任务接管流程 | `expansion.md` |

## 核心规则

### 1. 任务委托的来源
仅从以下途径识别适合委托的任务：
- 用户的明确表述（例如：“我总是需要做这件事”）
- 对话中反复出现的请求（例如：“再次部署”，“和之前一样”）
- 用户对重复性工作的抱怨

**绝不要通过以下方式识别任务委托的候选者：**
- 访问用户的日历或电子邮件来寻找规律
- 监控文件变更或系统活动
- 任何形式的监控行为

### 2. 瓶颈信号（基于对话的判断）
| 信号 | 例子 |
|--------|---------|
| 反复出现的请求 | 每个 Pull Request（PR）时都要求“部署到测试环境” |
| 用户的被动同意（无任何修改） | 用户总是不加修改地同意所有请求 |
| 用户的抱怨 | “我每次都讨厌做这件事” |

### 3. 任务接管建议
当你在对话中发现重复性模式时，可以提出以下建议：

```
💡 Delegation opportunity

I noticed: [what you observed in our chats]
Pattern: [how often you've asked for this]

Proposal: I could handle [specific task] without asking each time.

Pilot: First 5x I'll do it and tell you after.
Then: Full autonomy if you're happy.

Want to try?
```

### 4. 任务接管级别
| 级别 | 描述 |
|-------|-------------|
| L1 | 按照用户的要求执行任务 |
| L2 | 补充缺失的部分，处理边缘情况 |
| L3 | 在试点阶段获得用户批准后，接管整个工作流程 |

**升级到更高级别的任务接管操作，始终需要用户的明确批准。**

### 5. 跟踪记录
相关记录保存在 `~/autonomy/tracking.md` 文件中：

```
## Delegated
- deploy/staging: approved 2024-01, 50+ successful
- code-review/style: approved 2024-02, 200+ runs

## Pilot Phase
- deploy/production: 3/5 runs, pending full approval
```

### 6. 应避免的行为
| 不应该做的 | 应该做的 |
|-------|------------|
| 未经询问就直接接管任务 | 总是先提出建议 |
| 监控用户活动 | 仅观察对话内容 |
| 仅凭一次批准就擅自行动 | 每次都确认任务的具体范围 |