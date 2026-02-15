---
name: google-maps-search-api
description: 该技能旨在帮助用户自动从 Google 地图搜索结果中提取商业数据。当用户请求“查找纽约的咖啡店”、“搜索牙科诊所”或“从 Google 地图中提取商业线索”时，代理应主动使用该技能来完成任务。
---

# Google 地图搜索自动化技能

## ✨ 平台兼容性

**✅ 在所有主流 AI 助手上都能稳定且可靠地运行**

| 平台 | 支持情况 | 安装方法 |
|----------|--------|----------------|
| **OpenCode** | ✅ 完全支持 | 将技能文件夹复制到 `~/.opencode/skills/` |
| **Claude Code** | ✅ 完全支持 | 内置技能支持 |
| **Cursor** | ✅ 完全支持 | 复制到 `~/.cursor/skills/` |
| **OpenClaw** | ✅ 完全支持 | 兼容 |

**为什么选择 BrowserAct 技能？**
- 🚀 执行稳定，无崩溃风险
- ⚡ 响应速度快
- 🔧 无需繁琐的配置
- 📦 即插即用
- 💬 专业支持

## 📖 介绍
该技能通过 BrowserAct 的 Google 地图搜索 API 模板提供一站式商业数据收集服务。只需一个命令即可获取结构化商业数据。

## 🔑 API 密钥说明
在运行之前，请检查 `BROWSERACT_API_KEY` 环境变量。如果未设置，请等待用户提供 API 密钥。
**代理应告知用户**：
> “由于您尚未配置 BrowserAct API 密钥，请访问 [BrowserAct 控制台](https://www.browseract.com/reception/integrations) 获取密钥，并在此聊天中提供给我。”

## 🛠️ 输入参数说明
代理应根据用户需求灵活配置以下参数：

1. **KeyWords（搜索关键词）**
   - **类型**：`string`
   - **说明**：用户在 Google 地图上想要搜索的关键词。
   - **示例**：`coffee`、`bakery`、`coworking space`

2. **language（用户界面语言）**
   - **类型**：`string`
   - **说明**：设置用户界面语言和返回文本的语言。
   - **可选值**：`en`、`de`、`fr`、`it`、`es`、`ja`、`zh-CN`、`zh-TW`
   - **默认值**：`en`

3. **country（国家/地区偏好）**
   - **类型**：`string`
   - **说明**：设置搜索结果的国家或地区偏好。
   - **示例**：`us`、`gb`、`ca`、`au`、`de`、`fr`、`es`、`it`、`jp`
   - **默认值**：`us`

4. **max_dates（最大提取数量）**
   - **类型**：`number`
   - **说明**：从搜索结果中提取的最大地点数量。
   - **默认值**：`100`

## 🚀 执行方法（推荐）
代理应通过执行以下独立脚本来实现“一个命令获取结果”的功能：

```bash
# Call example
python ./scripts/google_maps_search_api.py "KeyWords" "language" "country" max_dates
```

## 📊 数据输出说明
脚本成功执行后，会直接解析并打印 API 响应中的结果。结果包括：
- `name`：商家名称
- `full address`：商家地址
- `rating`：平均评分
- `review count`：评论数量
- `price range`：价格范围
- `cuisine type`：商家类别
- `amenity tags`：设施信息（如 Wi-Fi、户外座位）
- `review snippet`：精选的简短评论
- `service options`：服务选项（如“在线订购”、“堂食”）

## ⚠️ 错误处理与重试
在脚本执行过程中，如果出现错误（例如网络波动或任务失败），代理应按照以下逻辑处理：

1. **检查输出内容**：
   - 如果输出中包含 “Invalid authorization”，则说明 API 密钥无效或已过期。**不要重试**，而是引导用户检查并提供正确的 API 密钥。
   - 如果输出中不包含 “Invalid authorization”，但任务执行失败（例如输出以 “Error:” 开头或返回空结果），代理应**自动尝试重新执行**脚本一次。

2. **重试限制**：
   - 自动重试仅允许**一次**。如果第二次尝试仍然失败，则停止重试，并向用户报告具体的错误信息。