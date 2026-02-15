---
name: google-news-api
description: 自动从 Google News 中抓取结构化的新闻数据。当用户请求某个主题的新闻、行业趋势或进行公关监控时，可以使用该功能。该功能会在检测到诸如“查找关于……的新闻”、“跟踪趋势”或“监控公关活动”等关键词时触发。
---

# Google 新闻自动化抓取技能

## ✨ 平台兼容性

**✅ 在所有主要 AI 助手上都能稳定且可靠地运行**

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
该技能利用 BrowserAct 的 Google 新闻 API 模板，提供一站式新闻收集服务。通过一个命令，代理即可获取结构化新闻数据。

## 🔑 API 密钥说明
在运行之前，请检查 `BROWSERACT_API_KEY` 环境变量。如果未设置，请不要执行脚本；请用户从 [BrowserAct 控制台](https://www-browseract.com/reception/integrations) 获取 API 密钥，并在此聊天中提供给我。

**需要向用户发送的消息：**
> “由于您尚未配置 BrowserAct API 密钥，请前往 [BrowserAct 控制台](https://www-browseract.com/reception/integrations) 获取密钥，并在此聊天中提供给我。”

## 🛠️ 输入参数
根据用户需求灵活配置以下参数：

1. **Search_Keywords**  
   - **类型**：`string`  
   - **描述**：在 Google 新闻中搜索的关键词（例如：公司名称、行业术语）。  
   - **示例**：`AI Startup`、`Tesla`、`SpaceX`  

2. **Publish_date**  
   - **类型**：`string`  
   - **描述**：文章的时间范围过滤器。  
   - **选项**：  
     - `any time`：无时间限制  
     - `past hours`：突发新闻  
     - `past 24 hours`：每日监控（推荐）  
     - `past week`：短期趋势  
     - `past year`：长期研究  
   - **默认值**：`past week`  

3. **Datelimit**  
   - **类型**：`number`  
   - **描述**：提取的最大新闻条目数量。  
   - **默认值**：`30`  
   - **建议**：监控使用 10-30 条，研究使用更多条目。

## 🚀 执行（推荐方式）
执行以下脚本以获取结果：

```bash
# Call Example
python .cursor/skills/google-news-api/scripts/google_news_api.py "Keywords" "TimeRange" Count
```

## 📊 数据输出
成功执行后，将返回结构化数据：  
- `headline`：新闻标题  
- `source`：发布者  
- `news_link`：新闻链接  
- `published_time`：发布时间  
- `author`：作者名称（如有提供）

## ⚠️ 错误处理与重试机制  
1. **检查输出**：  
   - 如果输出包含 “Invalid authorization”，则 API 密钥无效。**不要重试**，引导用户提供正确的密钥。  
   - 对于其他错误（例如：“Error:” 或空结果），**自动重试一次**。  

2. **重试限制**：  
   - 最多自动重试 **一次**。如果仍然失败，请停止并向用户报告错误。