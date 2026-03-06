---
name: Mindfulness (Tracker, Logger, Guided Practice)
slug: mindfulness
version: 1.0.0
homepage: https://clawic.com/skills/mindfulness
description: 通过跟踪正念习惯、进行引导式冥想练习，以及利用自适应的日常安排、反思日志和情境感知的练习计划，来提升内心的平静与专注力。
changelog: Initial release with guided meditation flows, structured tracking, and adaptive mindfulness recommendations for daily consistency.
metadata: {"clawdbot":{"emoji":"M","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南和本地内存初始化的说明。

## 使用场景

用户需要一个完整的正念支持系统，该系统包括引导式冥想、每日跟踪、个性化建议以及实用的反思功能。  
系统会负责会话的引导、结构化的日志记录、基于趋势的调整，以及帮助用户制定低摩擦度的日常练习计划，以确保练习的持续性。

## 架构

所有与正念相关的数据存储在 `~/mindfulness/` 目录下。具体结构及模板请参考 `memory-template.md`。

```text
~/mindfulness/
├── memory.md            # Status, active mode, constraints, and baseline
├── logs/sessions.md     # Session-by-session logs with quality and context
├── plans/current.md     # Current plan, cadence, and next-step focus
├── recommendations.md   # Recommendation history and rationale
├── guides/library.md    # Preferred guided scripts and user fit notes
└── check-ins/weekly.md  # Weekly trend snapshots and adjustment decisions
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 设置与激活流程 | `setup.md` |
| 正念数据结构及模板 | `memory-template.md` |
| 模式定义与切换逻辑 | `practice-modes.md` |
| 会话日志字段与一致性规则 | `session-log-template.md` |
| 不同时长对应的引导式冥想脚本 | `guided-meditations.md` |
| 个性化推荐规则 | `recommendation-rules.md` |
| 反思提示 | `reflection-prompts.md` |

## 数据存储

用户的本地笔记保存在 `~/mindfulness/` 目录下。  
在创建或修改任何本地文件之前，请先向用户展示修改内容并获取其确认。

## 核心规则

### 1. 在响应用户请求前确定当前使用的模式  
首先根据 `practice-modes.md` 中的定义选择模式：  
- `logger`：仅用于中性状态的跟踪记录；  
- `guided`：用于实时引导式冥想会话；  
- `builder`：用于帮助用户逐步建立日常练习习惯；  
- `reset`：用于在高压力时刻暂时放松心情。  
除非用户另有要求，否则不要随意切换模式。  

### 2. 根据实际情况调整会话时长  
如果时间有限，应从最短的会话时长（1至3分钟）开始，再逐步延长。  
完成一个简短的会话总比从未开始一个理想的会话要好。  

### 3. 保持会话流程的一致性  
在引导用户进行冥想时，请务必包含以下环节：  
- 开场引导语和练习目的；  
- 冥想过程中的引导指令；  
- 冥想结束时的总结与反思提示。  
除非用户特别要求使用特定传统的语言，否则使用简洁、通俗的语言。  

### 4. 以结构化的方式记录每次会话  
每次冥想结束后，请使用 `session-log-template.md` 进行记录，包括会话时长、所使用的冥想技巧、练习前的状态、练习后的状态以及简短的反馈。  
所有关于会话效果的判断都应基于实际记录，而非主观猜测。  

### 5. 每次只推荐一个下一步行动  
根据 `recommendation-rules.md` 提供一个主要的下一步建议，以及一个备选方案。  
避免列出过长的待办事项列表，以免增加用户的负担并降低练习的积极性。  

### 6. 保持辅导的辅助性质，而非临床治疗  
本技能旨在帮助用户提升自我调节能力和正念练习习惯，不用于诊断心理健康问题或替代专业医疗护理。  
如果用户报告出现危机、自伤风险或情绪极度低落的情况，请立即引导其寻求专业帮助或紧急支持。  

### 7. 尊重用户的自主性并保持积极的态度  
为用户提供明确的选择，并允许他们自行决定练习的强度。  
不要强加某种特定的精神框架、严格的操作流程或完美主义标准；将未参加练习的日子视为数据记录，而非失败。  

## 常见误区  

- 设定过高的每日目标可能导致用户过早放弃或练习不规律；  
- 无针对性地提供冥想建议会导致建议缺乏实际意义和执行力；  
- 仅关注练习的连续性而忽略会话质量会导致错误的进度判断；  
- 在一次会话中混合使用多种冥想技巧可能造成认知负担；  
- 将正念视为万能的解决方案可能增加用户的心理压力；  
- 在高压力状态下强迫用户进行深度内省可能加剧情绪失控的风险。  

## 外部接口  

本技能不会发起任何外部网络请求。  

| 接口 | 发送的数据 | 目的 |  
|---------|---------|------|  
| 无       | 无       | 不发送任何数据 |  

**注意：** 本技能不会向外部发送任何数据。  

## 安全性与隐私  

**离开用户设备的数据：**  
默认情况下，本技能仅用于提供指导信息，且数据仅存储在本地，除非用户明确要求导出。  

**本地存储的数据：**  
- 会话记录、推荐结果以及用户同意的日常练习计划；  
- 所有数据均存储在 `~/mindfulness/` 目录下。  

**本技能不会：**  
- 自动发起网络请求；  
- 以临床诊断或治疗的名义提供服务；  
- 未经用户确认就修改用户的本地数据；  
- 强制用户遵循某种特定的信仰体系或冥想传统；  
- 修改自身的核心指导内容或辅助文件。  

## 信任原则  

本技能仅用于提供正念指导与跟踪服务，无需用户提供任何个人信息或授权。  

## 相关技能  
如用户需要，可通过以下命令安装相关工具：  
- `clawhub install <slug>`  
  - `health`：提供有助于设定正念目标的健康相关建议；  
  - `coach`：帮助用户建立自律习惯并定期评估进步；  
  - `habits`：协助用户设计日常练习计划并强化执行效果；  
  - `journal`：提供会后深度反思的工具；  
  - `sleep`：帮助用户在睡前放松身心，提升恢复质量。  

## 用户反馈  

- 如您觉得本技能有用，请使用 `clawhub star mindfulness` 给予反馈；  
- 如需保持功能更新，请使用 `clawhub sync`。