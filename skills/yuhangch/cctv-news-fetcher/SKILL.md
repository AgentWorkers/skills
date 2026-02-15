---
name: cctv-news-fetcher
description: 从 CCTV 新闻联播（Xinwen Lianbo）中获取并解析指定日期的新闻摘要。
user-invocable: true
---

# CCTV新闻获取器

此技能可帮助您获取指定日期的CCTV新闻节目的摘要标题和内容。

## 使用方法

您可以向代理发送以下指令：
- “获取20250210日的CCTV新闻”
- “给我昨天的重要新闻”

## 指令说明

当用户请求特定日期的新闻时：
1. 日期格式应为`YYYYMMDD`。如果用户输入“昨天”或“今天”，系统会自动根据当前本地时间计算相应的日期。
2. 使用`bun`或`node`在`{baseDir}/scripts/news_crawler.js`脚本中执行该任务。命令格式为：`bun {baseDir}/scripts/news_crawler.js <YYYYMMDD>`
3. 解析JSON格式的输出结果，并为用户提供摘要。如果可能的话，根据新闻标题将新闻分为“国内”和“国际”两类进行展示；否则，仅列出重要新闻。

## 配置要求

此技能依赖于`node-html-parser`插件。请确保环境中已安装`bun`插件。