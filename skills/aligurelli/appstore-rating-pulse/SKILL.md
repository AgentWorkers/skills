---
name: appstore-rating-pulse
description: 监控任何iOS应用在多个国家的App Store评分情况。通过Apple提供的免费iTunes Lookup API实时获取应用的整体评分（无需API密钥）。可以设置每日定时报告，或获取即时评分数据。该功能支持以下操作：跟踪应用评分、查看App Store评分、生成每日评分报告，以及展示多国应用的评分情况。
---
# AppStore评分监测工具

该工具利用Apple提供的免费iTunes Lookup API，实时获取全球各国iOS应用的总体评分——无需API密钥或付费订阅。

## 设置

使用您的应用列表和目标地区信息，编辑`scripts/fetch-ratings.sh`脚本：

```bash
# Apps: "App Name" "AppStoreID" "CC1,CC2,CC3"
APPS=(
  "My App|1234567890|US,GB,DE"
  "Another App|9876543210|US,JP,KR"
)
```

国家代码遵循ISO 3166-1 alpha-2标准（例如：US、GB、JP、KR、DE、FR、RU、ES、CA、AU等）。

## 手动运行

```bash
bash /path/to/skills/public/appstore-rating-pulse/scripts/fetch-ratings.sh
```

## 输出格式

```
overall rating for My App(1234567890) 19.02.2026 - 4,72 - USA
overall rating for My App(1234567890) 19.02.2026 - 4,10 - UK
overall rating for My App(1234567890) 19.02.2026 - N/A - GERMANY
```

评分使用逗号（`,`）作为小数分隔符。如果某个国家没有评分，则显示“N/A”。

## 日常定时任务设置

创建一个独立的Cron作业（sessionTarget: isolated），该作业会运行脚本并将结果通过announce工具输出：

```
Run bash /path/to/scripts/fetch-ratings.sh and send the output to the user as-is. If all lines show N/A or the script errors, warn that something may be wrong.
```

示例调度时间：`0 12 * * *`（每天中午12点，根据您的时区）。

## 自定义功能

- 通过修改`fetch-ratings.sh`中的`APPS`数组来添加/删除应用。
- 通过修改以逗号分隔的国家代码列表来为特定应用添加/删除目标国家。
- 国家名称的显示是自动处理的：常见国家名称会被转换成中文显示，其他国家则保留原始代码形式。