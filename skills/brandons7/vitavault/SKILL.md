---
name: vitavault
description: VitaVault iOS 应用集成：能够分析从 Apple Health 导出的数据（格式为 JSON、CSV 或适合 AI 处理的文本格式），并与您的 AI 代理协同工作。该应用适用于所有 iPhone 设备，无需使用 Mac。用户可以扫描实验室检测结果、记录用药情况、查看健康趋势，并获得由 AI 提供的洞察和建议。
license: Apache-2.0
compatibility: Any OpenClaw agent. Pairs with VitaVault iOS app (free on App Store).
metadata:
  category: health
  platforms: ios
  author: BrandonS7
---
# VitaVault - 您的健康数据解析工具

这是一个专为处理来自 [VitaVault](https://vitavault.io) 的健康数据导出文件而设计的 AI 代理技能。

> **无需 Mac 设备。** VitaVault 是一款免费的 iOS 应用程序，可自动将您的 Apple Health 数据同步到您的 AI 代理。您可以从 [TestFlight](https://testflight.apple.com/join/A4G27HBt)（测试版）或 App Store（即将推出）中安装它。

## 与 OpenClaw 的自动同步

每当您打开 VitaVault 应用程序时，它都会自动将健康数据同步到云端。您的 OpenClaw 代理可以随时查询这些数据。

### 设置

将您的同步令牌设置为环境变量：
```bash
export VITAVAULT_SYNC_TOKEN="your-token-here"
```

### 查询脚本

```bash
# Get latest health snapshot
python3 scripts/query.py summary

# Get raw JSON
python3 scripts/query.py latest

# Get past week
python3 scripts/query.py week

# Get specific date range
python3 scripts/query.py range 2026-02-01 2026-02-28
```

### API 端点（用于自定义集成）

所有 API 端点都需要添加 `Authorization: Bearer <token>` 标头。

| 方法 | 路径 | 描述 |
|--------|------|-------------|
| GET | `/v1/health/latest` | 最新的健康数据快照 |
| GET | `/v1/health/range?start=YYYY-MM-DD&end=YYYY-MM-DD` | 指定日期范围内的健康数据 |
| GET | `/v1/status` | API 健康检查（无需身份验证） |

基础 URL：`https://vitavault-api.brandon-f00.workers.dev`

## 什么是 VitaVault？

VitaVault 是一款以用户隐私为首要考虑的 iOS 健康应用程序，它具备以下功能：
- 从 Apple Health 中读取 48 种以上的健康数据类型（步数、睡眠质量、心率、心率变异性、血氧饱和度、体重等）
- 使用人工智能分析实验室检测结果，并以通俗易懂的方式解释这些结果
- 通过智能提醒功能跟踪用药情况
- 生成就诊前的准备报告
- 支持三种数据导出格式：JSON、CSV 和适合 AI 分析的纯文本格式
- 所有数据均存储在设备上，不会上传到任何服务器

## 何时使用此技能

- 用户分享了 VitaVault 的健康数据导出文件（JSON、CSV 或适合 AI 分析的纯文本格式）
- 用户询问自己的 Apple Health 数据情况
- 用户需要健康趋势分析或健康建议
- 用户需要了解实验室检测结果或用药记录
- 用户需要为就诊做准备

## 如何使用 VitaVault 导出数据

### 适合 AI 分析的格式（纯文本）
这是最简单的格式，已预先格式化，可直接用于 AI 分析。用户可以从 VitaVault 中导出数据并直接粘贴使用。

示例：
```
HEALTH SUMMARY - Last 7 Days

Steps: 43,133 total (6,162/day avg)
Sleep: 6h 42m last night, 7.1h weekly avg
Heart Rate: 72 bpm avg, 62 bpm resting
HRV: 30ms avg
Blood Oxygen: 97% avg
Weight: 185.4 lbs
Active Calories: 4,645 total (616/day avg)
Exercise: 142 min total
```

### JSON 格式
结构化数据，适用于程序化分析：
```json
{
  "exportDate": "2026-02-17T12:00:00Z",
  "period": "7d",
  "metrics": {
    "steps": { "total": 43133, "dailyAverage": 5719, "unit": "steps" },
    "sleep": { "lastNight": 6.7, "weeklyAverage": 7.1, "unit": "hours" },
    "heartRate": { "average": 72, "resting": 62, "unit": "bpm" },
    "hrv": { "average": 30, "unit": "ms" },
    "bloodOxygen": { "average": 97, "unit": "%" },
    "weight": { "latest": 185.4, "unit": "lbs" },
    "activeCalories": { "dailyAverage": 542, "unit": "kcal" }
  }
}
```

### CSV 格式
每天记录一条数据，可在 Excel 或 Sheets 中查看：
```csv
date,steps,sleep_hours,resting_hr,hrv_ms,weight_lbs,calories
2026-02-17,8012,6.7,62,28,185.4,642
2026-02-16,5891,7.2,61,33,185.2,589
```

## 分析提示

当用户分享 VitaVault 数据时，您可以：
1. **进行趋势分析** - 发现睡眠、活动量和心率等方面的变化模式
2. **标记风险指标** - 识别异常指标（如心率变异性低、睡眠质量差、静息心率偏高）
3. **提供健康建议** - 根据数据提出可行的健康改善措施
4. **生成就诊准备报告** - 为医疗预约生成总结报告
5. **解释实验室检测结果** - 将实验室检测值与健康指标联系起来进行解读
6. **帮助设定健康目标** - 将当前指标与用户设定的目标进行对比

## 示例对话

用户：“这是我的 VitaVault 数据导出文件，我应该关注哪些方面呢？”

良好的回应方式：
1. 表示已收到数据
2. 强调 2-3 个关键观察结果（正面或需要关注的方面）
3. 提出 3 个具体的、可操作的改进建议
4. 表示可以进一步深入分析任何特定指标

## 隐私声明

VitaVault 所有健康数据都在设备上进行处理。数据导出完全由用户主动发起。当用户将数据分享给 AI 代理时，请告知他们这是他们的选择，并且数据将由 AI 服务提供商进行处理。

## 链接

- **应用程序**：[VitaVault 测试版](https://testflight.apple.com/join/A4G27HBt)
- **官方网站**：[vitavault.io](https://vitavault.io)
- **开发者文档**：[vitavault.io/developers](https://vitavault.io/developers/)
- **隐私政策**：[vitavault.io/privacy](https://vitavault.io/privacy/)