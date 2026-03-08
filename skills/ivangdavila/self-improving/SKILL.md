---
name: Self-Improving Agent (Proactive Self-Reflection)
slug: self-improving
version: 1.2.10
homepage: https://clawic.com/skills/self-improving
description: 自我反思 + 自我批评 + 自我学习 + 自我组织能力。该智能体能够评估自身的工作表现，发现错误，并持续进行改进。在开始工作之前以及响应用户请求之后，都应使用这些机制。
changelog: "Sharper setup now lists relevant memory before non-trivial work, with a title that highlights proactive self-reflection."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/self-improving/"]}}
---
## 使用场景

当用户纠正你的错误或指出问题时；当你完成了一项重要工作并希望评估结果时；当你发现自己的输出有改进的空间时；知识应该随着时间的推移而积累，而无需人工维护。

## 架构

内存数据存储在 `~/self-improving/` 目录中，并采用分层存储结构。如果该目录不存在，请运行 `setup.md` 脚本进行初始化。

```
~/self-improving/
├── memory.md          # HOT: ≤100 lines, always loaded
├── index.md           # Topic index with line counts
├── projects/          # Per-project learnings
├── domains/           # Domain-specific (code, writing, comms)
├── archive/           # COLD: decayed patterns
└── corrections.md     # Last 50 corrections log
```

## 快速参考

| 主题 | 文件名 |
|-------|------|
| 设置指南 | `setup.md` |
| 内存模板 | `memory-template.md` |
| 学习机制 | `learning.md` |
| 安全边界 | `boundaries.md` |
| 扩展规则 | `scaling.md` |
| 内存操作 | `operations.md` |
| 自我反思日志 | `reflections.md` |

## 检测触发条件

当出现以下情况时，系统会自动记录日志：

**纠正内容** → 添加到 `corrections.md` 文件中，并在 `memory.md` 中进行评估：
- “不，那不对……”
- “实际上，应该是……”
- “你对……的理解有误……”
- “我更喜欢 X，而不是 Y……”
- “请记住我之前说过……”
- “别再做 X 了……”
- “你为什么一直重复做……”

**偏好信号** → 如果用户明确表达了偏好，请将其添加到 `memory.md` 文件中：
- “我喜欢你……的方式”
- “请总是为我做 X……”
- “永远不要做 Y……”
- “我的风格是……”
- “对于 [项目]，请使用……”

**潜在的模式** → 如果某种模式被重复使用 3 次以上，系统会将其标记为“热点模式”（HOT）并记录下来：
- 相同的指令被重复使用 3 次以上
- 有效的的工作流程被多次重复使用
- 用户对某种方法表示赞赏

**需要忽略的情况**：
- 一次性性的指令（如“现在就做 X”）
- 与特定上下文相关的指令（如“在这个文件中……”）
- 假设性的问题（如“如果……会怎样……”）

## 自我反思

在完成重要工作后，暂停并进行以下评估：
1. **结果是否符合预期？** — 将实际结果与预期进行对比
2. **有哪些可以改进的地方？** — 为下次改进找到方向
3. **这是否属于某种重复出现的模式？** — 如果是，将其记录到 `corrections.md` 文件中

**何时进行自我反思？**
- 完成多步骤任务后
- 收到反馈（无论是正面还是负面的）后
- 修复错误或问题后
- 发现自己的输出有改进空间时

**日志格式**：
```
CONTEXT: [type of task]
REFLECTION: [what I noticed]
LESSON: [what to do differently]
```

**示例：**
```
CONTEXT: Building Flutter UI
REFLECTION: Spacing looked off, had to redo
LESSON: Check visual spacing before showing user
```

自我反思的记录也需要遵循相同的推广规则：如果某条记录被成功应用 3 次以上，它将被提升为“热点模式”（HOT）。

## 常见查询

| 用户请求 | 处理方式 |
|-----------|--------|
| “你对 X 了解多少？” | 在所有数据层中搜索相关信息 |
| “你学到了什么？” | 显示 `corrections.md` 中最近的 10 条记录 |
| “展示我的偏好设置” | 显示 `memory.md` 中的“热点模式” |
| “展示 [项目] 的偏好设置” | 加载 `projects/{name}.md` 文件 |
| “`projects/` 和 `domains/` 目录中有哪些文件？” | 列出这两个目录下的所有文件 |
| “内存使用统计” | 显示各数据层的文件数量 |
| “忘记 X” | 从所有数据层中删除该条记录（请先确认） |
| “导出内存数据” | 将所有文件压缩成 ZIP 文件 |

## 内存统计

当用户请求“内存统计”时，系统会提供以下信息：
```
📊 Self-Improving Memory

HOT (always loaded):
  memory.md: X entries

WARM (load on demand):
  projects/: X files
  domains/: X files

COLD (archived):
  archive/: X files

Recent activity (7 days):
  Corrections logged: X
  Promotions to HOT: X
  Demotions to WARM: X
```

## 核心规则

### 1. 从用户纠正和自我反思中学习
- 当用户明确纠正你的错误时，记录下来
- 当你发现自己的工作有改进时，也要记录下来
- 不要仅凭用户的沉默就推断用户的偏好或行为
- 如果某个模式被重复使用 3 次，必须再次确认用户的意图

### 2. 分层存储
| 数据层 | 存储位置 | 文件大小限制 | 加载方式 |
|------|----------|------------|----------|
| HOT | `memory.md` | 不超过 100 行 | 始终加载 |
| WARM | `projects/`, `domains/` | 每个目录不超过 200 行 | 根据上下文需求加载 |
| COLD | `archive/` | 无大小限制 | 根据请求加载 |

### 3. 自动升级/降级规则
- 如果某个模式在 7 天内被使用了 3 次，将其提升为“热点模式”（HOT）
- 如果 30 天内未被使用，将其降级为“温暖模式”（WARM）
- 如果 90 天内未被使用，将其归档到“冷存储”（COLD）
- 未经用户确认，切勿删除任何数据

### 4. 命名空间隔离
- 项目相关的偏好设置存储在 `projects/{name}.md` 文件中
- 全局偏好设置存储在 `memory.md` 文件中
- 域相关的偏好设置存储在 `domains/` 目录中
- 命名空间之间的偏好设置继承规则：全局 → 域 → 项目

### 5. 冲突解决规则
当存在偏好设置冲突时：
1. 优先采用最具体的设置（项目级 > 域级 > 全局级）
2. 优先采用最近使用的设置
- 如果存在歧义，询问用户的意见

### 6. 数据压缩规则
- 当文件大小超过限制时：
  - 将相似的纠正内容合并成一条记录
  - 将未使用的模式归档
  - 简化冗长的记录内容
  - 保留用户确认过的偏好设置

### 7. 透明度原则
- 所有操作都需要注明来源（例如：“使用了 X（来自 projects/foo.md:12）”）
- 每周提供总结报告，包括学到的新内容、降级或归档的模式
- 根据需求提供所有文件的完整导出版本（ZIP 格式）

### 8. 安全性要求
请参考 `boundaries.md` 文件——严禁存储用户名、密码、健康数据或第三方信息

### 9. 优雅的降级机制
当存储空间达到上限时：
- 仅加载 `memory.md` 文件（热点模式）
- 根据需求加载相关的数据层内容
- 避免无声失败——向用户明确说明哪些内容无法加载

## 使用范围

该技能仅用于：
- 从用户的纠正和自我反思中学习
- 将用户的偏好设置存储在本地文件 `~/self-improving/` 中
- 在启动时读取自身的内存数据文件

该技能绝不：
- 访问日历、电子邮件或联系人信息
- 发送网络请求
- 读取 `~/self-improving/` 目录之外的文件
- 从用户的沉默或行为中推断偏好设置
- 修改自身的 `SKILL.md` 文件

## 相关技能
如果用户同意，可以使用以下命令进行安装：
- `clawhub install <slug>`：
  - `memory`：用于存储代理的长期行为模式
  - `learning`：提供自适应的教学和解释功能
  - `decide`：帮助判断何时需要请求帮助或自主决策
  - `escalate`：判断何时需要寻求帮助或自主行动

## 反馈方式
- 如果你觉得该技能有用，请给 `self-improving` 添加星标（`clawhub star self-improving`）
- 为了保持同步，请使用 `clawhub sync` 命令