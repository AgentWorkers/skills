---
name: Pregnancy (Tracker, Journal, Triage, Visit Prep)
slug: pregnancy
version: 1.0.0
homepage: https://clawic.com/skills/pregnancy
description: 使用灵活的日志记录功能来跟踪孕期日常情况、症状以及临床指标；提供每周的总结报告，并实施以安全为首要原则的分诊机制，以便后续的医疗跟进。
changelog: Initial release with flexible pregnancy tracking modules, clinician-ready weekly summaries, and safety triage guardrails.
metadata: {"clawdbot":{"emoji":"P","requires":{"bins":[]},"os":["darwin","linux","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南和本地数据初始化的说明。

## 使用场景

用户需要一个灵活的孕期追踪工具，用于记录症状、日常活动、用药情况、预约信息、疑问以及需要关注的健康警示信号。该工具能够整理日志数据，确保其具有临床参考价值，并为产前检查提供简洁的总结报告，但不会替代专业的医疗护理。

## 架构

所有数据存储在 `~/pregnancy/` 目录下。具体数据结构及模板请参考 `memory-template.md`。

```text
~/pregnancy/
|-- memory.md                 # Status, context, and active tracking modules
|-- logs/daily-log.md         # Day-by-day entries with timestamps and units
|-- summaries/weekly.md       # Weekly clinical summary and trend notes
|-- summaries/visit-prep.md   # Questions and priorities for the next appointment
|-- alerts/events.md          # Red and amber events with trigger reasons
`-- preferences/thresholds.md # User-specific tracking scope and escalation choices
```

## 快速参考

| 主题 | 对应文件 |
|-------|------|
| 设置与激活流程 | `setup.md` |
| 数据存储结构及模板 | `memory-template.md` |
| 灵活的追踪框架 | `tracking-framework.md` |
| 统计量目录与单位规范 | `metric-catalog.md` |
| 数据质量与验证规则 | `data-quality.md` |
| 红色/琥珀色紧急情况处理规则 | `triage-rules.md` |
| 周报与检查总结模板 | `visit-summary-template.md` |

## 数据存储

所有本地记录都保存在 `~/pregnancy/` 目录下。在创建或修改任何文件之前，请先向用户确认数据存储计划。

## 核心规则

### 1. 在记录数据前明确使用目的
- 确定数据记录的目的（仅用于基本健康追踪、面向临床医生的孕期追踪，或高风险人群的监测支持）；
- 仅启用用户实际需要的功能模块，之后再逐步扩展。

### 2. 保持追踪的灵活性与条理性
- 使用 `tracking-framework.md` 来实现模块化的数据追踪：
  - 包含每日基本数据记录，确保数据连续性；
  - 可选模块包括症状记录、用药记录、预约信息、情绪状态、睡眠情况、营养摄入、胎儿活动情况以及血糖值等；
  - 根据用户需求自定义数据记录内容；
  - 避免强制用户同时使用所有功能模块。

### 3. 保持数据的临床实用性
- 遵循 `metric-catalog.md` 和 `data-quality.md` 中的规定：
  - 必须记录数据的时间戳、单位及记录背景；
  - 将所有数据统一转换为相同的单位系统；
  - 区分观察到的事实与对数据的解读；
  - 对于模糊不清的记录或缺失的背景信息，应要求用户补充说明。

### 4. 生成适合产前检查的总结报告
- 至少每周使用 `visit-summary-template.md` 生成一份简洁的总结报告：
  - 显示数据趋势；
  - 指出超出正常范围或需要关注的情况；
  - 提出医生需要了解的未解决问题；
  - 确保报告内容简明扼要，便于在产前检查中使用。

### 5. 优先处理紧急情况
- 依据 `triage-rules.md` 中的规则来处理红色/琥珀色紧急情况；
- 如出现紧急症状，应立即提供紧急指导；
- 在紧急情况未得到处理前，不要继续常规的追踪与建议。

### 6. 仅限于辅助用途，不替代诊断功能
- 该工具仅用于辅助数据组织和追踪，不用于疾病诊断、开具处方、解读影像检查结果或替代医生的专业判断；
- 对于用药调整或治疗决策，应引导用户咨询其医疗团队。

### 7. 保护用户隐私与自主权
- 仅记录与孕期相关的必要信息；
- 允许用户选择是否详细记录数据，也可随时暂停、简化或删除数据记录；
- 绝不进行隐藏的背景数据追踪。

## 常见问题

- 过早或过度记录数据可能导致用户流失及数据质量不稳定；
- 数据的时间戳或单位信息缺失会导致数据分析失真；
- 将安慰性信息与警示信号混在一起可能导致紧急情况处理延误；
- 将非强制性的用户数据当作临床依据可能导致错误决策；
- 如果总结报告仅包含原始数据，会降低产前检查的实用性；
- 超出功能范围提供治疗建议可能危及用户安全与信任。

## 外部接口

该工具不发送任何外部网络请求。

| 接口 | 发送的数据 | 目的 |
|---------|-----------|---------|
| 无       | 无        | 不发送任何数据 |

## 安全性与隐私保护

**离开用户设备的数据：**
- 默认情况下，该工具不会发送任何数据。除非用户明确要求导出，否则仅提供使用说明和本地数据。

**本地存储的数据：**
- 追踪日志、每周总结报告、警报事件以及用户同意提交的医生问题列表；
- 所有数据均存储在 `~/pregnancy/` 目录下。

**该工具不执行以下操作：**
- 诊断孕期健康状况或提供紧急医疗服务；
- 未经用户同意不会进行网络请求；
- 未经用户确认不会修改任何文件；
- 不会收集与孕期无关的个人信息。

## 信任声明

该工具仅用于孕期追踪和产前检查准备，无需用户提供任何认证信息，也不依赖第三方服务。

## 相关工具

如果用户同意安装，可同时使用以下工具：
- `health`：提供全面的健康规划与长期习惯管理支持；
- `doctor`：帮助用户为医疗咨询和后续跟进做好准备；
- `symptoms`：专注于症状记录与模式分析；
- `nutrition`：根据健康目标制定饮食与补水计划；
- `sleep`：帮助用户建立良好的睡眠习惯，提升能量管理能力。

## 用户反馈

- 如果您觉得该工具有用，请点赞：`clawhub star pregnancy`；
- 如需获取最新更新，请使用：`clawhub sync`。