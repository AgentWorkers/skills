---
name: google-ads-manager
description: >
  **Google Ads活动管理**  
  当用户需要查看统计数据、调整预算，或者启用或禁用Google广告中的活动时，可以使用此技能。该技能支持通过Google Ads API来执行相关操作。
---
# Google Ads Manager

这是一个用于管理Google上下文广告的工具。

## 功能
1. **监控**：获取广告活动列表及其当前指标（展示次数、点击次数、点击率、花费）。
2. **管理**：更改广告活动的状态（启用/暂停）并更新每日预算。
3. **报告**：生成指定时间段内的基本报告。

## 配置
运行该工具需要`google-ads.yaml`配置文件或环境变量中的配置信息。
配置文件应位于以下路径：`~/.google-ads.yaml`或项目根目录下。

## 使用脚本
主要的交互接口是通过Python脚本`scripts/google_ads_tool.py`实现的。

### 命令示例
- 获取广告活动列表：`python3 scripts/google_ads_tool.py list`
- 更改预算：`python3 scripts/google_ads_tool.py update-budget --id <ID> --amount <VALUE>`
- 暂停广告活动：`python3 scripts/google_ads_tool.py update-status --id <ID> --status PAUSED`

## 代理使用说明
收到处理广告的请求时，请按照以下步骤操作：
1. 确认配置文件是否存在。
2. 使用`google_ads_tool.py`执行相应的操作。
3. 如果用户没有特别说明，务必在执行任何关键操作（如更改预算或暂停广告活动）之前先获得用户的确认。