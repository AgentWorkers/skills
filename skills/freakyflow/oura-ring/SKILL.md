---
name: oura-ring
description: 该工具每天会将 Oura Ring 手环记录的健康与健身数据同步到 markdown 文件中，包括睡眠质量、身体状态、活动量、心率、压力水平、血氧饱和度（SpO2）以及锻炼数据等信息。
disable-model-invocation: true
metadata:
  openclaw:
    primaryEnv: OURA_TOKEN
    requires:
      bins: ["uv"]
      env: ["OURA_TOKEN"]
    config:
      - id: oura_token
        label: Oura Personal Access Token
        type: secret
        env: OURA_TOKEN
---

# Oura Ring

此技能可将您通过 Oura Ring 收集的每日健康数据同步到可读的 Markdown 文件中。

## 数据同步

同步当天的数据：

```bash
uv run {baseDir}/scripts/sync_oura.py
```

同步特定日期的数据：

```bash
uv run {baseDir}/scripts/sync_oura.py --date 2026-02-07
```

同步过去 N 天的数据：

```bash
uv run {baseDir}/scripts/sync_oura.py --days 7
```

## 查看健康数据

健康数据文件存储在 `{baseDir}/health/YYYY-MM-DD.md` 目录下——每天对应一个文件。

如需了解健康或健身相关情况，请阅读 `{baseDir}/health/` 目录中对应日期的文件。如果请求的日期文件不存在，请先运行该日期的数据同步命令。

## Cron 脚本设置

使用 OpenClaw 的 `cron` 工具，将同步脚本设置为每天早上自动运行，以确保您的健康数据始终保持最新状态。