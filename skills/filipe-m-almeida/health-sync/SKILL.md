---
name: health-sync
description: 分析来自 Oura、Withings、Hevy、Strava、WHOOP 和 Eight Sleep 的同步健康数据。
read_when:
  - User asks for health-sync setup, auth, sync, or provider status
  - User asks about sleep, recovery, training, activity, your health, or cross-provider trends
---
# 健康数据同步分析功能

## 目的

该功能专门用于分析用户来自以下健康数据提供商的健康数据：

- Oura
- Withings
- Hevy
- Strava
- WHOOP
- Eight Sleep

其主要目标是帮助用户了解数据趋势，比较不同提供商提供的健康数据，并从中获取有用的信息。

## 使用场景

当用户提出以下问题时，可使用该功能：

- 我昨晚的睡眠情况如何？
- 我上次的锻炼效果如何？
- 一年以来我的静息心率有什么变化？
- 我的恢复情况、睡眠质量和训练表现有哪些趋势？
- 我应该关注哪些有用的信息或下一步该做什么？

## 设置与认证

关于初始设置或认证流程，请参考：

- `references/setup.md`

请勿在此重复设置说明。该功能应将设置细节引用至相应的参考文档。

## 数据结构说明

为正确理解数据结构并执行查询，请阅读各数据提供商的参考文档：

- `references/oura.md`
- `references/withings.md`
- `references/hevy.md`
- `references/strava.md`
- `references/whoop.md`
- `references/eightsleep.md`

## 数据更新规则（强制要求）

在进行任何分析之前，务必运行以下命令：

```bash
health-sync sync
```

如果同步失败，请明确报告故障情况；只有在用户明确同意使用可能已过时的数据时，才能继续进行分析。

## 分析流程

1. 首先运行 `health-sync sync` 命令。
2. 确定用户的问题以及相关的提供商/数据资源。
3. 在编写 SQL 语句之前，先阅读相应提供商的数据结构说明。
4. 根据需要查询 `records`、`sync_state` 和 `sync_runs` 等数据。
5. 生成清晰、易于理解的答案，并提供具体的数字和日期信息。
6. 强调有意义的趋势，并提供实用的指导建议。
7. 如果数据质量或覆盖范围有限，请明确告知用户。

## 输出格式

- 语言简洁明了，内容实用。
- 重点在于数据的有效解读，而不仅仅是原始数据的展示。
- 将各项指标与可操作的洞察结果（如睡眠质量、恢复情况、训练效果等）联系起来。
- 仅在必要时提出进一步的问题，以提高分析的准确性。