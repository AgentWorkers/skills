---
name: vitavault
description: 导入并查询 VitaVault 的健康数据导出文件（格式为 JSON 或 CSV，数据来源于 iOS 应用程序）。当用户询问他们的健康数据、实验室检测结果、用药情况、睡眠趋势、心率、步数、体重、营养状况，或需要健康状况摘要以用于晨间汇报时，可以使用此功能。此外，在设置 VitaVault 数据导入、查询健康趋势，或为人工智能分析准备健康数据背景信息时，该功能也同样适用。
---
# VitaVault 健康数据技能

该技能用于导入从 VitaVault iOS 应用程序导出的健康数据，并使其能够被您的 AI 代理查询。

## 功能概述

VitaVault 会将苹果健康数据（共 48 种类型）以 JSON 或 CSV 格式从您的 iPhone 导出。该技能会：

1. 将导出的文件导入到 `~/vitavault/data/` 目录中。
2. 将健康记录解析为可查询的格式。
3. 汇总健康指标，以便进行简报和分析。
4. 分析数据随时间的变化趋势（如睡眠时间、步数、心率、体重、实验室检测结果等）。

## 快速入门

```bash
# 1. Import a VitaVault export (JSON or CSV)
python3 scripts/import.py ~/Downloads/vitavault-export.json

# 2. Get today's health summary
python3 scripts/summary.py

# 3. Query specific metrics
python3 scripts/query.py --type heartRate --days 7
python3 scripts/query.py --type sleepAnalysis --days 30
python3 scripts/query.py --type bodyMass --days 90

# 4. Get a prompt-ready health context block (for morning briefings)
python3 scripts/briefing.py
```

## 数据导入

VitaVault 以两种格式导出健康数据：

- **JSON**（推荐用于 AI 使用）：
```bash
python3 scripts/import.py ~/Downloads/vitavault-export.json
python3 scripts/import.py ~/Downloads/vitavault-export.json --tag "feb-2026"
```

- **CSV**：
```bash
python3 scripts/import.py ~/Downloads/vitavault-export.csv
```

导入后的文件会被标准化并存储在 `~/vitavault/data/` 目录中。每次导入操作都会添加时间戳，最新的导入文件会被创建为 `~/vitavault/data/latest.json` 的符号链接。

如果有多个导入文件，系统会合并这些文件：新数据会覆盖旧数据（通过记录 ID 进行匹配）。

### 获取导出文件的方法

您可以通过以下方式从 iPhone 获取健康数据文件：
- 通过 **AirDrop** 将文件传输到 Mac，然后使用 `scp` 命令将其复制到服务器。
- 通过 **iCloud Drive** 或 **Files** 应用程序共享文件并下载。
- 通过电子邮件将导出文件发送给自己。
- 直接将文件共享到任何云存储服务中。

## 数据查询

查询结果默认为人类可读的格式。如果您需要结构化的数据输出，可以使用 `--json` 参数。

## 数据汇总

```bash
# Full health summary (all available metrics, last 24h)
python3 scripts/summary.py

# Week summary
python3 scripts/summary.py --days 7

# JSON output for piping
python3 scripts/summary.py --json
```

## 与晨间简报系统的集成

该技能可以直接与 OpenClaw 的晨间简报定时任务集成。

## 支持的数据类型

请参阅 `references/data-types.md` 文件，以获取 VitaVault 导出的 48 种健康指标的完整列表，这些指标按类别（活动、身体状况、生命体征、睡眠、营养、心理健康）进行了分类。

## 数据格式

请参阅 `references/schema.md` 文件，了解 VitaVault 的 JSON 导出格式（包括健康记录格式、元数据结构及版本 2.0 的规范）。

## 文件结构

```
~/vitavault/
├── data/
│   ├── latest.json          → symlink to most recent import
│   ├── 2026-02-19T06-30.json
│   └── 2026-02-18T18-00.json
└── config.json              → preferences (units, default days, etc.)
```