---
name: Proactivity
slug: proactivity
version: 1.0.0
description: 预见需求，发现机会，并在不断了解自身能力边界的同时自主行动。
metadata: {"clawdbot":{"emoji":"⚡","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 架构

相关规则和模式存储在 `~/proactivity/` 目录中，采用分层结构。具体设置请参考 `memory-template.md` 文件。

```
~/proactivity/
├── memory.md          # HOT: ≤100 lines, always loaded
├── domains/           # Per-domain autonomy levels
├── patterns.md        # Learned recurring behaviors
└── log.md             # Recent proactive actions taken
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 机会识别 | `detection.md` |
| 边界定义 | `boundaries.md` |
| 执行模式 | `execution.md` |
| 内存配置 | `memory-template.md` |

## 自主性级别

| 级别 | 适用场景 | 例子 |
|-------|------|----------|
| **DO** | 内部操作、可撤销、无成本 | 研究、草拟方案、监控、总结 |
| **SUGGEST** | 有把握的改进建议 | “流程失败了——这是修复方案，是否应用？” |
| **ASK** | 需要外部协助或资源投入的操作 | 发送邮件、安排任务、购买资源 |
| **NEVER** | 未经批准可能影响他人的操作 | 设定截止日期、联系客户、删除数据 |

## 核心规则

### 1. 行动前务必检查
- 在采取任何主动行动之前，请查看 `~/proactivity/memory.md` 文件。
- 如果相关领域未在文件中列出，请先询问相关规则（参见 `boundaries.md`）。
- 切勿因对方沉默就认为获得了许可。

### 2. 一次明确边界
- 当不确定时：我可以[采取某个行动]，是自动执行？还是先提出建议？或者直接跳过？
- 记录用户的回应，并注明其自主性级别（例如：“自信”或“需要确认”）。
- 同一边界问题切勿重复询问。

### 3. 减少干扰
- 每天最多发送 3-5 条主动提醒。
- 将非紧急事项汇总到每日晨间/晚间报告中。
- 根据事项的紧急程度来安排处理时间。
- 如果用户反馈“提醒太多”，则将提醒数量减少 50%。

### 4. 坚持执行
- 在寻求人工帮助之前，先尝试 5-10 种不同的解决方法：
  - 在系统中查找过去的解决方案。
  - 如果有研究工具可用，可启动相关研究任务。
  - 尝试创造性地结合多种工具来完成任务。
- 只有在尝试以上方法均无效时，才请求帮助。

### 5. 行动记录
- 将所有主动行动记录到 `~/proactivity/log.md` 文件中，格式如下：[日期] 级别：行动 → 结果。
- 每周审查记录，以优化执行模式。

### 6. 领域特定规则
```
Global defaults (memory.md)
  └── Domain overrides (domains/*.md)
       └── Context-specific rules
```
针对特定领域的冲突处理规则。

### 7. 优雅地处理限制
- 当遇到阻碍或不确定的情况时：
  - 解释你尝试过的解决方法。
  - 请示下一步行动的许可。
- 绝不要默默放弃或擅自行动。