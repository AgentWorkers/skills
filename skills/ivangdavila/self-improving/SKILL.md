---
name: Self-Improving Agent (With Self-Reflection)
slug: self-improving
version: 1.1.3
homepage: https://clawic.com/skills/self-improving
description: 自我反思 + 自我批评 + 从错误中学习。代理会评估自身的工作，发现错误，并持续进行改进。
changelog: Fixed skill title display.
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/self-improving/"]}}
---
## 使用场景

当用户纠正你的错误或指出问题时；当你完成了一项重要工作并希望评估结果时；当你发现自己的输出有改进空间时；知识应该能够随着时间的推移自然积累，而无需人工维护。

## 架构

内存数据存储在 `~/self-improving/` 目录中，采用分层存储结构。具体设置方法请参阅 `memory-template.md`。

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

| 主题 | 文件 |
|-------|------|
| 设置指南 | `setup.md` |
| 学习机制 | `learning.md` |
| 安全边界 | `boundaries.md` |
| 扩展规则 | `scaling.md` |
| 内存操作 | `operations.md` |
| 自我反思日志 | `reflections.md` |

## 数据存储

所有数据都存储在 `~/self-improving/` 目录中。首次使用该功能时需要创建相关文件：

```bash
mkdir -p ~/self-improving/{projects,domains,archive}
```

## 检测触发条件

当出现以下情况时，系统会自动记录日志：

**纠正建议** → 记录到 `corrections.md` 中，并在 `memory.md` 中进行评估：
- “不，那不对……”
- “实际上，应该是……”
- “你对……的理解有误……”
- “我更喜欢 X，而不是 Y”
- “请记住我之前说过……”
- “别再做 X 了……”
- “你为什么还一直……”

**偏好设置** → 如果有明确表达，记录到 `memory.md` 中：
- “我喜欢你……的时候”
- “请总是为我做 X”
- “永远不要做 Y”
- “我的风格是……”
- “对于 [项目]，请使用……”

**潜在的模式** → 如果某种行为被重复出现 3 次以上，就进行记录并优先展示：
- 相同的指令被重复使用 3 次以上
- 重复使用且效果良好的工作流程
- 用户对某种方法的正面评价

**无需记录的情况**：
- 一次性性的指令（如“现在就做 X”）
- 与特定上下文相关的指令（如“在这个文件中……”）
- 假设性的内容（如“如果……会怎样……”）

## 自我反思

完成重要工作后，请暂停并进行以下评估：
1. **结果是否符合预期？** —— 将实际结果与预期目标进行对比
2. **有哪些可以改进的地方？** —— 为下次改进找到方向
3. **这是否属于某种重复出现的模式？** —— 如果是，记录到 `corrections.md` 中

**何时进行自我反思？**
- 完成多步骤任务后
- 收到反馈（无论是正面还是负面）后
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

自我反思的记录也需要遵循相同的规则：如果某条记录被成功应用了 3 次以上，就会提升其显示优先级（例如，从普通级别提升到 HOT 级别）。

## 常见查询

| 用户请求 | 处理方式 |
|-----------|--------|
| “你对 X 了解多少？” | 在所有数据层中搜索相关信息 |
| “你学到了什么？” | 显示 `corrections.md` 中最近 10 条记录 |
| “展示我的偏好设置” | 列出 `memory.md` 中的偏好设置 |
| “展示 [项目] 的相关设置” | 加载 `projects/{name}.md` 文件 |
| “`projects/` 和 `domains/` 目录中有哪些文件？” | 列出这两个目录下的所有文件 |
| “内存使用统计” | 显示各数据层的文件数量 |
| “删除 X” | 首先确认后，从所有数据层中删除相关记录 |
| “导出内存数据” | 将所有文件压缩成 ZIP 文件 |

## 内存统计

当用户请求 “内存统计” 时，系统会提供以下信息：
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
- 当用户明确指出错误时，记录下来
- 当你发现自己的工作有改进之处时，也要记录下来
- 不要仅凭用户的沉默就妄下结论
- 如果某个规则被重复使用 3 次，必须再次确认用户的意见

### 2. 分层存储
| 数据层 | 存储位置 | 文件大小限制 | 加载方式 |
|------|----------|------------|----------|
| HOT | `memory.md` | 不超过 100 行 | 始终加载 |
| WARM | `projects/`, `domains/` | 每个文件不超过 200 行 | 根据上下文需求加载 |
| COLD | `archive/` | 无大小限制 | 仅在用户明确请求时加载 |

### 3. 自动提升/降级规则
- 如果某个模式在 7 天内被使用了 3 次，提升其优先级至 HOT
- 如果 30 天内未被使用，降级至 WARM
- 如果 90 天内未被使用，归档至 COLD
- 未经用户确认，不得删除任何数据

### 4. 命名空间隔离
- 项目相关的设置保存在 `projects/{name}.md` 文件中
- 全局偏好设置保存在 HOT 级别的 `memory.md` 中
- 域相关的设置（代码、写作相关）保存在 `domains/` 目录中
- 不同命名空间之间的设置继承规则：全局 → 域 → 项目

### 5. 冲突解决规则
当不同设置之间存在冲突时：
1. 优先采用最具体的设置（项目级别 > 域级别 > 全局级别）
2. 优先采用最近使用的设置
- 如果存在歧义，询问用户的意见

### 6. 数据压缩规则
- 当文件大小超过限制时：
  - 将相似的纠正建议合并成一条记录
  - 将未使用的设置归档
  - 简化冗长的记录内容
  - 确保已确认的偏好设置不会被删除

### 7. 透明度原则
- 所有操作都要注明来源（例如：“使用了 X（来自 projects/foo.md:12）”）
- 每周提供总结报告，包括新学习的设置、降级的设置和被归档的设置
- 根据用户需求提供所有数据的完整导出（ZIP 文件格式）

### 8. 安全性要求
请参阅 `boundaries.md` —— 绝不允许存储凭证信息、健康数据或第三方信息

### 9. 优雅的降级机制
当系统达到存储空间限制时：
- 仅加载 `memory.md`（HOT 级别的数据）
- 根据用户需求加载相关的数据层内容
- 避免系统无声失败，必须向用户说明无法加载的内容

## 使用范围

该技能仅用于：
- 从用户的纠正和建议中学习
- 将用户的偏好设置存储在本地文件 `~/self-improving/` 中
- 在启动时读取自身的内存数据文件

该技能绝不：
- 访问日历、电子邮件或联系人信息
- 发送网络请求
- 读取 `~/self-improving/` 目录之外的文件
- 从用户的沉默或行为中推断其偏好设置
- 修改自身的 `SKILL.md` 文件

## 相关技能
如果用户同意安装，可以使用以下命令进行扩展：
- `clawhub install <slug>`：
  - `memory`：用于存储代理程序的长期行为模式
  - `learning`：实现自适应教学和解释功能
  - `decide`：帮助程序自主判断何时需要寻求帮助或何时可以自主决策
  - `escalate`：帮助程序判断何时需要请求帮助，何时可以自主行动

## 用户反馈
- 如果觉得该技能有用，请给它打星（使用 `clawhub star self-improving`）
- 为了保持功能更新，请定期执行 `clawhub sync` 命令