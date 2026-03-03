---
name: Anxiety (Tracker, Trigger Map, Coping Planner)
slug: anxiety
version: 1.0.0
homepage: https://clawic.com/skills/anxiety
description: 通过专为治疗准备的日志记录，追踪焦虑发作的频率、触发因素、相关想法以及应对策略；定期进行周度趋势分析，并设置以“安全第一”为原则的紧急求助提示。
changelog: Initial release with therapist-aligned anxiety tracking, trigger mapping, coping playbooks, and graded exposure planning support.
metadata: {"clawdbot":{"emoji":"A","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南和本地内存初始化的说明。

## 使用场景

用户希望记录焦虑症状、恐慌发作、担忧情绪的演变过程、回避行为以及应对措施的效果。该工具会生成对治疗具有临床价值的日志，通过结构化的计划帮助减轻焦虑，并在出现安全风险时立即采取应对措施。

## 架构

所有数据存储在 `~/anxiety/` 目录下。具体结构及模板请参阅 `memory-template.md`。

```text
~/anxiety/
├── memory.md                 # Status, mode, baseline, and active priorities
├── logs/events.md            # Episode-level anxiety event logs
├── logs/thought-records.md   # CBT-style thought records for reframing
├── plans/current.md          # Active coping and exposure plan
├── triggers.md               # Trigger map and safety behavior patterns
├── exposures.md              # Exposure ladder and session outcomes
└── reviews/weekly.md         # Weekly trend review and plan decisions
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 设置与激活流程 | `setup.md` |
| 数据存储结构与模板 | `memory-template.md` |
| 目标模式与切换逻辑 | `tracking-modes.md` |
| 焦虑事件记录格式 | `event-log-template.md` |
| 思维记录流程 | `thought-record.md` |
| 根据焦虑程度选择应对策略 | `regulation-playbook.md` |
| 分级暴露训练计划 | `exposure-ladder.md` |
| 周期性回顾与决策规则 | `weekly-review.md` |
| 紧急情况处理规则 | `triage-rules.md` |

## 数据存储

所有本地记录都保存在 `~/anxiety/` 目录下。在创建或修改任何文件之前，请先向用户确认操作内容。

## 核心规则

### 1. 干预前先设定目标模式
请从 `tracking-modes.md` 中选择目标模式：
- `track`：仅用于观察，不强制要求行为改变；
- `reduce`：逐步降低焦虑强度和频率；
- `recover`：用于事件后的情绪稳定及防止复发。
如果用户仅要求进行跟踪，切勿强制实施降低焦虑强度或暴露训练。

### 2. 详细记录与治疗相关的事件
使用 `event-log-template.md` 记录每个重要的焦虑事件。至少需要记录事件发生的时间、背景信息、触发因素、身体症状、焦虑程度、用户行为以及事件后的简要结果。不要记录无法后续分析的模糊信息。

### 3. 区分事件记录与认知分析
使用 `logs/events.md` 记录事件本身，使用 `logs/thought-records.md` 进行事件的分析与解读。仅在用户需要重新审视思维模式或分析行为模式时使用 `thought-record.md`。切勿在同一条记录中混合原始观察结果与分析结论。

### 4. 明确记录回避行为与安全行为
详细记录用户的回避行为以及他们为获得暂时安全感所采取的措施。利用这些数据来制定 `exposure-ladder.md` 中的暴露训练计划。如果回避行为严重影响了日常生活功能，请明确指出问题并提出具体的改进步骤。

### 5. 根据焦虑程度选择合适的应对策略
使用 `regulation-playbook.md` 根据焦虑程度选择合适的应对策略：
- 低焦虑程度：防止情况恶化，维持正常生活功能；
- 中等焦虑程度：降低生理反应，缩小注意力范围；
- 高焦虑程度：优先确保安全，立即提供支持。
未经用户同意，切勿推荐通用的应对策略。

### 6. 仅在用户同意的情况下使用分级暴露训练
当用户希望长期减轻焦虑时，可以使用 `exposure-ladder.md` 制定逐步的暴露训练计划。每一步都应设置明确的目标、重复次数以及恢复时间。切勿默认采用高强度的暴露训练。

### 7. 立即处理高风险信号
一旦出现严重症状、自伤念头、物质滥用危机或医疗紧急情况，请立即参照 `triage-rules.md` 采取行动。遇到紧急情况时，应优先提供紧急援助，暂停常规辅导服务。该工具主要用于跟踪和行为改变计划，不用于诊断或紧急治疗。

## 常见错误

- 仅记录“感到焦虑”而未提供具体背景信息 → 无法发现可操作的应对模式；
- 第一天记录过多信息 → 会导致用户疲劳并放弃使用该工具；
- 将所有焦虑事件同等对待 → 会导致错误的干预措施；
- 忽略回避行为的记录 → 会使暴露训练计划失效；
- 在急性恐慌发作期间尝试思维重构 → 效果不佳且可能引发用户反感；
- 提出过高的暴露目标 → 可能导致用户抗拒或回避行为加剧；
- 使用专业医学术语 → 违反了工具的安全使用原则。

## 外部接口

该工具不发送任何外部网络请求。

| 接口 | 发送的数据 | 目的 |
|----------|-----------|---------|
| 无 | 无 | 该工具不发送任何数据 |

## 安全性与隐私

**离开用户设备的数据**：
- 默认情况下，该工具不会发送任何数据。除非用户明确要求导出，否则仅用于内部使用。

**本地存储的数据**：
- 焦虑日志、思维记录、触发因素、暴露训练结果以及用户同意的每周回顾内容，均存储在 `~/anxiety/` 目录下。

**该工具不执行以下操作**：
- 诊断精神疾病或医疗状况；
- 未经用户同意进行网络请求；
- 未经用户确认直接修改本地数据；
- 强制用户执行暴露训练任务；
- 修改工具的核心指令或辅助文件。

## 信任声明

该工具仅用于提供焦虑跟踪与应对支持，无需用户提供任何个人信息。无需任何认证信息，也不涉及第三方服务的访问。

## 相关工具

用户可根据需求安装以下扩展功能：
- `therapist`：提供支持性的治疗对话引导；
- `psychologist`：提供结构化的行为与认知指导；
- `mindfulness`：帮助用户培养正念与专注力；
- `journal`：支持用户进行反思性写作与行为模式记录；
- `sleep`：帮助用户改善睡眠质量以缓解焦虑。

## 反馈方式

- 如对该工具有帮助，请使用 `clawhub star anxiety` 给予反馈；
- 如需更新工具信息，请使用 `clawhub sync` 功能。