---
name: turkey-news
version: 1.0.0
description: "该技能能够通过 RSS 源获取来自土耳其的重要新闻，并对其进行摘要处理。同时，它还支持通过 Cron 任务实现自动通知功能。"
author: dias
tags: [news, turkey, rss, turkish]
---

# 土耳其新闻

本工具会跟踪并汇总土耳其的重要新闻。

## 新闻来源（RSS）

- NTV: https://www.ntv.com.tr/son-dakika.rss
- CNN Türk: https://www.cnnturk.com/feed/rss/all/news
- TRT Haber: https://www.trthaber.com/sondakika.rss
- Sözcü: https://www.sozcu.com.tr/rss/all.xml
- Milliyet: https://www.milliyet.com.tr/rss/rssnew/gundemrss.xml
- Habertürk: https://www.haberturk.com/rss
- Hürriyet: https://www.hurriyet.com.tr/rss/anasayfa
- Sabah: https://www.sabah.com.tr/rss/anasayfa.xml
- Anadolu Ajansı: https://www.aa.com.tr/tr/rss/default?cat=guncel

## 使用方法

### 手动方式
向代理发送指令：“提供土耳其新闻”或“最新新闻是什么？”

### 自动方式（Cron任务）
通过Cron任务每天运行2-3次。代理会获取新闻，进行筛选，并将重要新闻通过Telegram通知用户。

### 脚本
```bash
node scripts/fetch-news.js
```
脚本会生成JSON格式的输出，代理会对这些输出进行解析并添加评论。

## 代理使用说明

1. 运行 `scripts/fetch-news.js` 脚本。
2. 从输出中筛选出过去3小时内的新闻。
3. 选择最重要的5-7条新闻。
4. 为每条新闻撰写简短的土耳其语摘要（标题+1句话）。
5. 通过Telegram将摘要通知指定的用户（例如“Usta”）。