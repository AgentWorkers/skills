---
name: Heartbeat
slug: heartbeat
version: 1.0.1
homepage: https://clawic.com/skills/heartbeat
description: 设计更优秀的 OpenClaw HEARTBEAT.md 文件，实现自适应的节奏控制、安全检查功能以及基于 Cron 表达式的任务调度机制，以确保任务能够按照精确的时间表执行。
changelog: "Refined heartbeat guidance with a production template, QA checklist, and cron handoff rules for safer proactive monitoring."
metadata: {"clawdbot":{"emoji":"💓","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
# 心跳检测（Heartbeat Monitoring）💓

为 OpenClaw 代理构建可靠的心跳检测机制，避免不必要的检查、信号丢失或成本过高。

## 设置（Setup）

首次使用时，请按照 `setup.md` 的说明来配置时区、活跃时间、精度要求以及风险容忍度。

## 使用场景（When to Use）

当用户需要改进 OpenClaw 中的心跳检测功能时，代理会审计当前的心跳检测行为，设计更安全的检测方案，并根据实际工作流程调整检测间隔。

该机制适用于自适应监控、主动检查以及结合 cron 任务的混合心跳检测策略。

## 架构（Architecture）

所有心跳检测相关数据存储在 `~/heartbeat/` 目录下。具体结构与字段信息请参考 `memory-template.md`。

```text
~/heartbeat/
├── memory.md              # Preferences, cadence profile, and last tuning decisions
├── drafts/                # Candidate heartbeat variants
└── snapshots/             # Previous heartbeat versions for rollback
```

## 快速参考（Quick Reference）

| 主题 | 文件 |
|-------|------|
| 设置指南 | `setup.md` |
| 内存模型 | `memory-template.md` |
| 生产环境心跳检测模板 | `heartbeat-template.md` |
| 实用案例 | `use-cases.md` |
| 间隔策略参考 | `intervals.md` |
| 触发策略参考 | `triggers.md` |
| 发布前的验证清单 | `qa-checklist.md` |
| 参考资料来源 | `sources.md` |

## 核心规则（Core Rules）

### 1. 在开始编写代码前明确检测范围
首先定义一个核心任务目标以及需要监控的信号（1-3 个）。
如果检测范围较广，应将其分为明确的几个部分（如“关键信号”、“重要信号”和“可选信号”），并仅自动化前两个部分的检测。

### 2. 严格规范输出结果
如果未发现任何需要处理的问题，心跳检测结果必须返回 `HEARTBEAT_OK`。
避免在空循环中生成不必要的输出，以防止系统出现异常行为并降低检测成本。

### 3. 根据时区和活跃时间调整检测频率
从 OpenClaw 的默认设置开始，根据实际情况进行调整：在活跃时间段内使用较短的检测间隔，在非活跃时间段使用较长的间隔。
务必在心跳检测文件中明确标注时区和活跃时间，避免在用户睡眠时触发检测。

### 4. 使用 cron 定时任务进行精确调度，使用心跳检测机制进行动态调整
如果任务需要在固定时间执行，应使用 cron 定时任务；如果任务需要根据环境变化或事件概率进行响应，则应使用心跳检测机制。

### 5. 为高成本操作添加限制
采用两阶段检测策略：先进行低成本的预检查，只有在达到阈值时才执行高成本的操作。
除非用户明确同意，否则不要在每次心跳检测时调用付费 API。

### 6. 定义升级和冷却机制
每个警报条件都必须有触发阈值、升级路径和冷却时间。
没有升级路径意味着不会触发警报；没有冷却机制可能导致频繁的警报。

### 7. 通过模拟测试进行验证并保留回滚方案
在最终发布前，至少使用 `qa-checklist.md` 中的验证清单进行一次模拟测试。
保留上一次心跳检测的记录，以便用户可以快速回滚到之前的配置。

## 常见问题（Common Traps）

- 每次循环都检查所有内容 → 会导致大量 API 调用和资源浪费，同时降低信号质量。
- 将心跳检测用于固定时间（如 09:00）的任务 → 可能导致检测结果不准确。
- 心跳检测配置中未设置时区 → 通知会在错误的本地时间发送。
- 未设置活跃时间过滤机制 → 可能在用户睡眠时触发检测，导致用户疲劳。
- 没有 `HEARTBEAT_OK` 的默认返回值 → 会导致无意义的循环操作。
- 警报没有冷却机制 → 在异常情况下可能导致重复升级。

## 安全性与隐私（Security & Privacy）

所有数据均存储在本地：
- 心跳检测的配置信息和调整记录保存在 `~/heartbeat/` 目录下。
- 心跳检测相关的草稿文件和备份文件也保存在同一目录。

**注意：**  
- 该技能默认不要求用户提供凭证。
- 未经用户许可，不会触发外部 API。
- 不会修改与心跳检测无关的文件。

## 相关技能（Related Skills）
如果用户需要，可以使用以下命令进行安装：
- `clawhub install <slug>`：安装相关工具。
- `schedule`：用于安排重复性工作流程。
- `monitoring`：监控策略和警报设计。
- `alerts`：警报路由和升级管理。
- `workflow`：多步骤工作流程编排。
- `copilot`：具有可控自主性的辅助工具。

## 反馈建议：
- 如果觉得本文档有用，请给它打星（`clawhub star heartbeat`）。
- 保持更新：`clawhub sync`。