---
name: appstore-rating-pulse
description: >
  **功能说明：**  
  实时跟踪并报告任何iOS应用在多个国家的App Store评分情况，数据每日通过Cron任务自动更新。适用于需要监控特定地区（如美国、英国、日本、德国）内应用的评分情况，或定期生成评分报告的用户。也可根据用户需求（如“查看我的应用评分”、“每日跟踪App Store评分”、“为我的应用设置评分监控”或“显示各国的应用评分”）触发相应操作。  
  **主要特性：**  
  1. **实时数据更新**：每日自动从App Store获取最新评分信息。  
  2. **多国家支持**：支持同时监控多个国家的应用评分。  
  3. **自定义报告**：可设置每日自动生成评分报告的频率和格式。  
  4. **便捷查询**：提供直观的界面，方便用户快速查看和应用评分数据。  
  5. **灵活配置**：支持根据用户需求定制监控内容和报告格式。  
  **使用场景：**  
  - 监控特定地区应用的评分变化  
  - 生成定期评分报告  
  - 实时了解应用在全球范围内的表现  
  **适用场景示例：**  
  - 开发者需要及时了解应用在目标市场的表现  
  - 市场分析师需要分析应用在不同地区的用户反馈  
  - 管理人员需要定期评估应用的市场表现  
  **技术细节：**  
  - 通过Cron任务定时从App Store获取数据  
  - 数据存储和查询采用高效的后端服务  
  - 提供API接口，支持自定义数据分析和报表生成  
  **注意事项：**  
  - 请确保您的应用程序已配置正确的App Store审核和发布设置。  
  - 数据传输和存储过程需遵循相关隐私和合规性要求。
---
# App Store 评分统计工具

该工具使用 Apple 的免费 iTunes Lookup API 来获取全球任何国家中 iOS 应用的当前整体评分，无需 API 密钥或付费订阅。

## 设置

使用你的应用列表和目标国家信息编辑 `scripts/fetch-ratings.sh` 文件：

```bash
# Apps: "App Name" "AppStoreID" "CC1,CC2,CC3"
APPS=(
  "My App|1234567890|US,GB,DE"
  "Another App|9876543210|US,JP,KR"
)
```

国家代码遵循 ISO 3166-1 alpha-2 标准（例如：US、GB、JP、KR、DE、FR、RU、ES、CA、AU 等）。

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

评分使用逗号作为小数分隔符。如果某个国家没有评分，则显示 “N/A”。

## 每日定时任务设置

创建一个独立的 cron 任务（sessionTarget: isolated），该任务会运行脚本并将结果通过 announce 功能发送出去：

```
Run bash /path/to/scripts/fetch-ratings.sh and send the output to the user as-is. If all lines show N/A or the script errors, warn that something may be wrong.
```

示例调度时间：`0 12 * * *`（每天中午，根据你的时区）。

## 自定义设置

- 通过编辑 `fetch-ratings.sh` 文件中的 `APPS` 数组来添加或删除应用。
- 通过修改以逗号分隔的国家代码列表来为特定应用添加或删除目标国家。
- 国家名称会自动显示；常见国家会显示其对应的中文名称，其他国家则显示其原始代码。