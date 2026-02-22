---
name: Six Thinking Hats
slug: six-thinking-hats
version: 1.0.0
homepage: https://clawic.com/skills/six-thinking-hats
description: 使用结构化的并行思维方法，从六个角度分析决策。
metadata: {"clawdbot":{"emoji":"🎩","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 设置

如果 `~/six-thinking-hats/` 不存在，或者系统提示设置未完成，请先阅读 `setup.md` 文件。

## 适用场景

当用户需要彻底分析某个决策、问题或想法时，可以使用 De Bono 的“六顶思考帽”方法来系统地从各个角度进行探索。

## 架构

相关数据存储在 `~/six-thinking-hats/` 目录下。具体结构请参考 `memory-template.md` 文件。

```
~/six-thinking-hats/
├── memory.md       # Preferences + past analyses
└── archive/        # Completed analyses
```

## 快速参考

| 项目 | 文件      |
|------|---------|
| 设置流程 | setup.md   |
| 记忆模板 | memory-template.md |
| 各种思考帽的详细信息 | hats.md   |

## 六顶思考帽

| 思考帽 | 重点关注 | 关键问题       |
|-------|-----------|-------------|
| 白色帽   | 事实、数据    | 我们知道了什么？还缺少哪些数据？ |
| 红色帽   | 情感、直觉    | 我对这件事有什么感受？我的直觉是什么？ |
| 黑色帽   | 风险、问题    | 可能会出现什么问题？为什么会失败？ |
| 黄色帽   | 益处、价值    | 有哪些优势？最佳情况是什么？ |
| 绿色帽   | 创造力、替代方案 | 还有哪些可能性？新的想法？ |
| 蓝色帽   | 过程、控制    | 下一步该做什么？总结一下？ |

## 核心规则

### 1. 一次只使用一种思考帽
- 每个时刻只使用一种思考帽
- 在切换思考帽之前，先完成当前视角下的分析
- 明确地宣布思考帽的转换

### 2. 顺序很重要
决策的标准流程如下：
1. **蓝色帽** — 明确问题
2. **白色帽** — 收集事实
3. **绿色帽** — 生成备选方案
4. **黄色帽** — 评估每个方案的好处
5. **黑色帽** — 评估每个方案的风险
6. **红色帽** — 进行直觉判断
7. **蓝色帽** — 做出结论并做出决策

### 3. 并行进行思考
- 所有人都朝着同一个方向思考
- 不允许争论或辩护
- 每种思考帽都有充分的时间被考虑

### 4. 红色帽的发言应简短
- 只表达情感，无需解释原因
- 发言时间不超过 30 秒
- 例如：“我感到兴奋”，而不是“我感到兴奋是因为……”

### 5. 黑色帽并非表示消极
- 它代表批判性思考，而非消极情绪
- 用于识别需要解决的问题，而非直接否定某个方案
- 应与黄色帽结合使用以保持平衡

### 6. 绿色帽要产生多种方案
- 至少生成 3 个替代方案
- 在绿色帽阶段不进行评判
- 优先考虑数量而非质量

### 7. 蓝色帽负责整个过程
- 开始和结束整个讨论
- 总结每种思考帽得出的结果
- 做出最终决策

## 输出格式

在分析决策时，输出内容应按照以下结构组织：

```markdown
## Analysis: [Topic]

### Blue Hat: Framing
[Problem statement, scope, goal]

### White Hat: Facts
[Known data, missing information, sources]

### Green Hat: Options
1. [Option A]
2. [Option B]
3. [Option C]

### Yellow Hat: Benefits
| Option | Benefits |
|--------|----------|
| A | [benefits] |
| B | [benefits] |
| C | [benefits] |

### Black Hat: Risks
| Option | Risks |
|--------|-------|
| A | [risks] |
| B | [risks] |
| C | [risks] |

### Red Hat: Gut Check
[Brief emotional response to each option]

### Blue Hat: Conclusion
[Summary, recommendation, next steps]
```

## 常见误区
- 混淆不同思考帽的用途 → 会导致分析混乱，遗漏关键视角
- 跳过红色帽的环节 → 会忽略可能被逻辑忽略的直觉
- 只使用黑色帽而不结合黄色帽 → 决策结果可能显得消极，导致好的方案被放弃
- 只使用绿色帽而不设定限制 → 不切实际的方案会浪费时间
- 最后没有使用蓝色帽 → 分析结果缺乏可执行的结论

## 相关技能
如果用户需要，可以使用以下命令安装相关工具：
- `clawhub install <slug>`：安装 `decide`（决策框架）、`brainstorm`（创意生成工具）和 `first-principles-thinking`（基础分析工具）

## 反馈建议
- 如果觉得本文档有用，请点赞：`clawhub star six-thinking-hats`
- 保持更新：`clawhub sync`