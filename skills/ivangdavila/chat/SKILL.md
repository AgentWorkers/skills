---
name: Chat
slug: chat
version: 1.1.0
description: 根据用户的明确反馈来了解他们的沟通偏好，并据此调整沟通的语气、格式和风格。
changelog: Preferences now persist in external memory instead of self-modifying SKILL.md
metadata: {"clawdbot":{"emoji":"💬","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 数据存储

```
~/chat/
├── memory.md       # Confirmed preferences (≤50 lines)
├── experiments.md  # Testing patterns (not yet confirmed)
└── rejected.md     # User said no, don't re-propose
```

首次使用时创建：`mkdir -p ~/chat`

## 功能范围

该功能：
- ✅ 从用户的明确反馈中学习用户的偏好设置
- ✅ 将偏好设置存储在 `~/chat/memory.md` 文件中
- ✅ 根据存储的偏好设置调整沟通方式
- ❌ 绝不修改 `SKILL.md` 文件
- ❌ 绝不通过用户的沉默或行为进行推断
- ❌ 绝不存储用户的敏感个人信息

## 快速参考

| 主题 | 文件名 |
|-------|------|
| 偏好设置的相关信息 | `dimensions.md` |
| 确认标准 | `criteria.md` |

## 核心规则

### 1. 仅从用户的明确反馈中学习偏好设置
- 用户必须明确表达自己的偏好或提出反对意见
- 例如：“我更喜欢 X” 或 “不要做 Y” 是有效的反馈信号
- 沉默或没有抱怨并不表示用户的意见
- 绝不能仅凭观察来推断用户的偏好

### 2. 三次确认机制
| 阶段 | 存储位置 | 执行操作 |
|-------|----------|--------|
| 测试阶段 | `experiments.md` | 观察用户的行为 1-2 次 |
| 确认阶段 | （询问用户） | 在用户重复该行为 3 次后，再次确认 |
| 确认偏好 | `memory.md` | 用户同意该偏好设置 |
| 拒绝偏好 | `rejected.md` | 用户拒绝该偏好设置 |

### 3. 紧凑的存储格式
在 `memory.md` 文件中，每个偏好设置仅占用一行：

```
- Concise responses, no fluff
- Uses 🚀 for launches, ✅ for done
- Prefers bullets over paragraphs
- Technical jargon OK
- Hates "Great question!" openers
```

### 4. 冲突解决规则
- 最新的明确偏好设置优先生效
- 如果偏好设置存在歧义，需询问用户
- 未经用户明确指示，绝不要覆盖已确认的偏好设置

### 5. 透明度原则
- 在使用偏好设置时需注明来源：“使用的是来自 `~/chat/memory.md` 的内容”
- 根据用户要求，可展示 `memory.md` 的全部内容
- 如果用户要求删除某个偏好设置，该设置将从所有相关文件中删除