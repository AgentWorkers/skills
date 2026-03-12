---
name: Self-Improving + Proactive Agent
slug: self-improving
version: 1.2.16
homepage: https://clawic.com/skills/self-improving
description: "自我反思 + 自我批评 + 自我学习 + 自我组织能力。该智能体能够评估自身的工作表现，发现错误，并持续进行改进。适用于以下情况：  
(1) 某个命令、工具、API 或操作出现故障时；  
(2) 用户纠正了你的错误或拒绝了你的工作成果；  
(3) 你意识到自己的知识已经过时或不准确；  
(4) 你发现了更优的解决方法；  
(5) 用户明确要求使用该技能来完成当前任务。"
changelog: "Clarifies the setup flow for proactive follow-through and safer installation behavior."
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":[]},"os":["linux","darwin","win32"],"configPaths":["~/self-improving/"],"configPaths.optional":["./AGENTS.md","./SOUL.md","./HEARTBEAT.md"]}}
---
## 使用场景

当用户纠正你的错误或指出问题时；当你完成了重要的工作并希望评估结果时；当你发现自己的输出有改进的空间时；知识应该随着时间的推移而积累，而无需人工维护。

## 架构

内存数据存储在 `~/self-improving/` 目录中，并采用分层存储结构。如果 `~/self-improving/` 目录不存在，请运行 `setup.md` 脚本进行初始化。工作区的设置需要将自优化功能添加到工作区的 AGENTS、SOUL 文件以及 `HEARTBEAT.md` 文件中，相关的维护规则则通过 `heartbeat-rules.md` 文件来管理。

```
~/self-improving/
├── memory.md          # HOT: ≤100 lines, always loaded
├── index.md           # Topic index with line counts
├── heartbeat-state.md # Heartbeat state: last run, reviewed change, action notes
├── projects/          # Per-project learnings
├── domains/           # Domain-specific (code, writing, comms)
├── archive/           # COLD: decayed patterns
└── corrections.md     # Last 50 corrections log
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 设置指南 | `setup.md` |
| 心跳状态模板 | `heartbeat-state.md` |
| 内存模板 | `memory-template.md` |
| 工作区心跳信息 | `HEARTBEAT.md` |
| 心跳规则 | `heartbeat-rules.md` |
| 学习机制 | `learning.md` |
| 安全边界 | `boundaries.md` |
| 扩展规则 | `scaling.md` |
| 内存操作 | `operations.md` |
| 自我反思日志 | `reflections.md` |
| OpenClaw 心跳种子文件 | `openclaw-heartbeat.md` |

## 要求

- 无需任何凭证  
- 无需额外的二进制文件  
- 安装 `Proactivity` 技能可能需要网络访问权限  

## 学习信号

当出现以下情况时，系统会自动记录日志：  

**纠正信息** → 添加到 `corrections.md` 文件中，并在 `memory.md` 中进行评估：  
- “不，那不对...”  
- “实际上应该是...”  
- “你对……的理解有误...”  
- “我更喜欢 X，而不是 Y...”  
- “请记住我之前说过……”  
- “别再做 X 了...”  
- “你为什么一直……”  

**偏好信号**（如果用户明确表达） → 添加到 `memory.md` 文件中：  
- “我喜欢你……的方式”  
- “请总是为我做 X”  
- “永远不要做 Y”  
- “我的风格是……”  
- “对于 [项目]，请使用……”  

**需要记录的模式**：  
- 同一指令被重复 3 次以上  
- 重复出现且效果良好的工作流程  
- 用户对某种方法的正面评价  

**无需记录的情况**：  
- 一次性指令（如“现在就做 X”）  
- 与特定上下文相关的指令  
- 假设性的问题（如“如果……会怎样”）  

## 自我反思  

完成重要任务后，请暂停并进行以下评估：  
1. **结果是否符合预期？** —— 将实际结果与预期目标进行对比  
2. **有哪些可以改进的地方？** —— 为下次改进找到方向  
3. **这是否属于某种重复出现的模式？** —— 如果是，记录到 `corrections.md` 文件中  

**何时进行自我反思？**  
- 完成多步骤任务后  
- 收到反馈（正面或负面）后  
- 修复错误或问题后  
- 发现自己的输出有改进的空间时  

**日志格式：**  
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

自我反思的记录同样遵循“三次应用后提升”的规则：如果某条记录被成功应用三次，就会提升到 “HOT” 状态。  

## 常见问题及解决方法  

| 常见问题 | 原因 | 解决方法 |  
|------|--------------|-------------|  
| 从用户的沉默中推断用户意图 | 可能导致错误规则 | 等待用户的明确纠正或重复出现的情况后再进行判断 |  
| 提升模式的速度过快 | 会导致 HOT 区域内存混乱 | 新学到的内容应在被多次验证后再正式记录 |  
| 阅读所有命名空间中的内容 | 会浪费处理效率 | 仅加载 HOT 区域的内容以及最相关的文件 |  
- 通过删除来压缩数据 | 会丢失信任记录和历史信息 | 应合并、总结数据或降低模式的优先级 |  

## 核心规则  

### 1. 从用户的纠正和自我反思中学习  
- 当用户明确指出错误时，记录下来  
- 当你发现自己的工作有改进时，也记录下来  
- 切勿仅凭用户的沉默就下结论  
- 如果某条规则被重复出现三次，应请求用户确认后再将其正式记录  

### 2. 分层存储  
| 存储层级 | 存储位置 | 文件大小限制 | 处理方式 |  
|------|----------|------------|----------|  
| HOT | `memory.md` | 不超过 100 行 | 始终加载 |  
| WARM | `projects/`, `domains/` | 每个文件夹不超过 200 行 | 根据上下文需要加载 |  
| COLD | `archive/` | 无限制 | 仅在需要时加载 |  

### 3. 自动提升/降级规则  
- 如果某条模式在 7 天内被使用了 3 次，提升到 HOT 状态  
- 如果 30 天内未被使用，降级到 WARM 状态  
- 如果 90 天内未被使用，归档到 COLD 状态  
- 未经用户确认，切勿删除任何模式  

### 4. 命名空间隔离  
- 项目相关的模式保存在 `projects/{name}.md` 文件中  
- 全局偏好设置保存在 HOT 区域（`memory.md`）  
- 域名相关的模式（代码、写作相关）保存在 `domains/` 文件中  
- 命名空间间的规则继承顺序：全局 → 域名 → 项目  

### 5. 冲突解决规则  
- 当不同模式之间存在冲突时：  
  - 优先采用最具体的规则（项目 > 域名 > 全局）  
  - 优先采用最近使用的规则  
  - 如果仍不确定，询问用户的意见  

### 6. 数据压缩  
- 当文件大小超过限制时：  
  - 将相似的纠正信息合并成一条规则  
  - 将未使用的模式归档  
  - 对冗长的记录进行总结  
  - 绝不删除已确认的偏好设置  

### 7. 透明度原则  
- 所有操作都应注明来源（例如：“使用的是来自 `projects/foo.md:12` 的规则”）  
- 提供每周的总结报告（包括已学习的模式、降级的规则和被归档的规则）  
- 可根据需求导出所有数据（格式为 ZIP 文件）  

### 8. 安全性要求  
- 严禁存储凭证、健康数据或第三方信息（详见 `boundaries.md`）  

### 9. 优雅的降级机制  
- 当存储空间达到上限时：  
  - 仅加载 `memory.md`（HOT 区域的内容）  
  - 根据需求加载相关命名空间的内容  
- 绝不默默地失败——必须告知用户哪些内容无法加载  

## 技能范围  

该技能仅用于：  
- 从用户的纠正和自我反思中学习  
- 将用户的偏好设置保存在本地文件 `~/self-improving/` 中  
- 当工作区启用心跳功能时，维护 `~/self-improving/heartbeat-state.md` 文件中的状态信息  
- 在启动时读取自身的内存数据  

**该技能绝不会：**  
- 访问日历、电子邮件或联系人信息  
- 发送网络请求  
- 读取 `~/self-improving/` 目录之外的文件  
- 仅凭用户的沉默或观察来推断用户的偏好设置  
- 在清理数据时随意删除或修改自身的设置文件  
- 修改自身的 `SKILL.md` 文件  

## 数据存储方式  

所有数据存储在 `~/self-improving/` 目录中：  
- `memory.md`：保存 HOT 状态下的规则和已确认的偏好设置  
- `corrections.md`：保存用户的纠正信息及可重复使用的学习内容  
- `projects/` 和 `domains/`：保存特定项目或域名的模式  
- `archive/`：保存过时或不再使用的模式  
- `heartbeat-state.md`：保存用于维护的标记信息  

## 相关技能  
用户可安装以下扩展技能（通过 `clawhub install <slug>` 命令）：  
- `memory`：用于存储长期使用的模式  
- `learning`：实现自适应的教学和解释功能  
- `decide`：帮助判断何时需要寻求帮助或自主决策  
- `escalate`：帮助判断何时需要请求帮助或自主行动  

## 反馈方式  
- 如果觉得本技能有用，请给予反馈（使用 `clawhub star self-improving`）  
- 保持更新：通过 `clawhub sync` 功能获取最新信息