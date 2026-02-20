---
name: Self-Improving Agent
slug: self-improving
version: 1.1.0
homepage: https://clawic.com/skills/self-improving
description: 修正本身就是一种改进；这种能够自我优化的记忆系统，无疑是一种强大的工具。
changelog: Added detection triggers, quick queries, memory stats, and example templates for easier setup.
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

当用户纠正你的错误或指出问题时，你需要记住用户的偏好设置、行为模式以及在不同会话中总结出的经验教训。这些知识应该随着时间的推移而不断积累，而无需人工维护。

## 架构

记忆数据存储在 `~/self-improving/` 目录中，并采用分层存储结构。具体配置请参考 `memory-template.md` 文件。

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

| 主题 | 对应文件 |
|-------|------|
| 学习机制 | `learning.md` |
| 安全边界 | `boundaries.md` |
| 扩展规则 | `scaling.md` |
| 内存操作 | `operations.md` |

## 数据存储

所有数据都存储在 `~/self-improving/` 目录中。首次使用时需要创建相关文件：

```bash
mkdir -p ~/self-improving/{projects,domains,archive}
```

## 检测触发条件

当发现以下情况时，系统会自动记录：

**用户纠正** → 记录到 `corrections.md` 文件中，并更新 `memory.md`：
- “不，那不对……”
- “实际上，应该是……”
- “你对……的理解有误……”
- “我更喜欢选择 X，而不是 Y……”
- “请记住我之前说过……”
- “别再做 X 了……”
- “你为什么还一直……”

**用户偏好信号**（如果明确表达） → 记录到 `memory.md` 文件中：
- “我喜欢你……的时候”
- “请总是为我做 X……”
- “永远不要做 Y……”
- “我的风格是……”
- “对于 [项目]，请使用……”

**行为模式**（如果出现 3 次以上） → 进行跟踪并提升其优先级：
- 相同的指令被重复使用 3 次以上
- 长期有效的操作流程
- 用户对某种方法的正面评价

**无需记录的情况**：
- 一次性指令（如“现在就做 X”）
- 与特定上下文相关的指令（如“在这个文件中……”）
- 假设性内容（如“如果……会怎样……”）

## 快速查询

| 用户提问 | 对应操作 |
|-----------|--------|
| “你对 X 了解多少？” | 在所有数据层中搜索相关信息 |
| “你学到了什么？” | 显示 `corrections.md` 中最近的 10 条记录 |
| “显示我的行为模式” | 列出 `memory.md` 中的热门模式 |
| “显示 [项目] 的相关模式” | 加载 `projects/{name}.md` 文件 |
| “暖区存储了哪些内容？” | 列出 `projects/` 和 `domains/` 目录下的文件 |
| “内存统计信息” | 显示各数据层的记录数量 |
| “忘记 X” | 从所有数据层中删除相关内容（请先确认） |
| “导出内存数据” | 将所有文件压缩成 ZIP 格式 |

## 内存统计信息

当用户请求 “内存统计信息” 时，系统会提供如下报告：

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

### 1. 仅从用户纠正中学习
- 仅当用户明确指出错误时才进行记录
- 不要从不言而喻的行为或观察中推断用户的偏好
- 如果连续 3 次收到相同的纠正，需要用户再次确认该偏好

### 2. 分层存储
| 数据层 | 存储位置 | 存储容量限制 | 行为规则 |
|------|----------|------------|----------|
| 热门模式（HOT） | `memory.md` | 不超过 100 行 | 始终加载 |
| 温区模式（WARM） | `projects/`, `domains/` | 每层不超过 200 行 | 根据上下文需求加载 |
| 冷区模式（COLD） | `archive/` | 无容量限制 | 根据查询需求加载 |

### 3. 自动提升/降级规则
- 如果某种行为模式在 7 天内被使用 3 次，提升为热门模式（HOT）
- 如果 30 天内未被使用，降级为温区模式（WARM）
- 如果 90 天内未被使用，归档到冷区模式（COLD）
- 未经用户确认，不得删除任何数据

### 4. 命名空间隔离
- 项目相关的行为模式存储在 `projects/{name}.md` 文件中
- 全局偏好设置存储在热门模式层（`memory.md` 中
- 域相关的内容（代码、写作规范等）存储在 `domains/` 目录下
- 命名空间之间的规则继承顺序：全局 → 域 → 项目

### 5. 冲突解决规则
- 当不同规则之间存在冲突时：
  - 优先采用最具体的规则（项目 > 域 > 全局）
  - 优先采用最近被使用的规则
  - 如果仍不清楚如何处理，询问用户意见

### 6. 数据压缩规则
- 当文件大小超过限制时：
  - 将相似的纠正内容合并为单一规则
  - 将不常用的模式归档
  - 简化冗长的记录内容
  - 保证已确认的偏好设置不被删除

### 7. 透明度原则
- 所有操作都需注明来源（例如：“使用了 X（来自 projects/foo.md:12）”）
- 每周提供总结报告，包括新学到的模式、被降级的模式以及被归档的模式
- 根据用户需求提供完整的数据导出功能（ZIP 格式）

### 8. 安全边界
请参考 `boundaries.md` 文件——严禁存储凭证信息、健康数据或第三方信息

### 9. 优雅的降级机制
当系统达到存储容量上限时：
- 仅加载热门模式（HOT）的数据
- 根据需求加载相关命名空间的数据
- 避免系统无声失败，需向用户说明无法加载的数据

## 使用范围

本技能仅用于：
- 从用户的明确纠正中学习
- 将用户的偏好设置存储在本地文件 `~/self-improving/` 中
- 在激活时读取自身的内存数据

本技能绝不：
- 访问用户的日历、电子邮件或联系人信息
- 发起网络请求
- 读取 `~/self-improving/` 目录之外的文件
- 从不言而喻地推断用户的偏好设置
- 修改自身的 `SKILL.md` 文件

## 相关技能
如果用户同意安装，可以使用以下命令进行扩展：
- `clawhub install <slug>`：
  - `memory`：用于存储代理的长期行为模式
  - `learning`：实现自适应教学和解释功能
  - `decide`：帮助系统自主判断何时需要请求用户帮助
  - `escalate`：指导系统在何时需要请求用户决策

## 用户反馈
- 如果本技能对你有帮助，请使用 `clawhub star self-improving` 给予评价
- 为了保持功能更新，请使用 `clawhub sync` 命令同步数据