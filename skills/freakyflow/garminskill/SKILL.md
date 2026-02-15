---
name: garmin-connect
version: 1.2.0
description: 该工具每天会将来自 Garmin Connect 的健康与健身数据同步到 markdown 文件中，包括睡眠、活动量、心率、压力水平、身体电量、心率变异性（HRV）、血氧饱和度（SpO2）以及体重等数据。
homepage: https://github.com/freakyflow/garminskill
metadata: {"clawdbot":{"emoji":"💪","requires":{"bins":["uv"]},"install":[{"id":"uv","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv via Homebrew"}]}}
---

# Garmin Connect

该技能可将您从 Garmin Connect 获取的日常健康数据同步到可读的 Markdown 文件中。

## 设置

在首次同步之前，需要进行身份验证。此操作只需执行一次，因为生成的令牌会在本地缓存大约一年时间。

如果同步命令出现“未找到缓存令牌”的错误，请提示用户在终端中运行设置命令：

```bash
uv run {baseDir}/scripts/sync_garmin.py --setup --email you@example.com
```

密码会通过 `getpass` 函数以交互式方式获取，不会显示在屏幕上，也不会存储在 shell 历史记录中或作为命令参数传递。成功后，用户会看到“成功！令牌已缓存到 ~/.garminconnect” 的提示。之后，所有同步操作都将使用缓存的令牌，无需再次输入凭据。

请勿在聊天中询问用户的密码，也切勿通过命令行参数或标准输入（stdin）传递密码，因为这些方式可能导致凭据泄露。

## 同步数据

- 同步当天的数据：  
  ```bash
uv run {baseDir}/scripts/sync_garmin.py
```

- 同步特定日期的数据：  
  ```bash
uv run {baseDir}/scripts/sync_garmin.py --date 2026-02-07
```

- 同步过去 N 天的数据：  
  ```bash
uv run {baseDir}/scripts/sync_garmin.py --days 7
```

## 查看健康数据

健康数据文件存储在 `{baseDir}/health/YYYY-MM-DD.md` 目录下，每天对应一个文件。

要查询健康或健身相关信息，请读取 `{baseDir}/health/` 目录中对应日期的文件。如果请求的日期对应的文件不存在，请先运行同步命令。

## 依赖项

该技能使用 [uv](https://docs.astral.sh/uv/) 来执行同步脚本。`uv` 是 Astral 开发的一个快速 Python 包管理器，它能够读取内联脚本元数据（PEP 723 标准），并自动在隔离环境中安装所需的依赖项（`garminconnect`、`cloudscraper`），无需手动执行 `pip install` 操作。

## 凭据

Garmin Connect 不提供公共的 OAuth API，因此需要使用一次性的电子邮件/密码登录方式。在设置过程中，密码仅用于获取 OAuth 令牌，之后会被丢弃。令牌会缓存在 `~/.garminconnect/` 目录中，有效期约为一年。运行时只需使用缓存的令牌，无需再次输入电子邮件或密码。如果令牌过期，请重新运行设置命令。

## Cron 安排

使用 OpenClaw 的 `cron` 工具将同步脚本设置为每天早晨自动运行，以确保您的健康数据始终保持最新状态。此过程不需要任何环境变量或额外凭据，因为同步操作会使用之前设置时缓存的令牌。