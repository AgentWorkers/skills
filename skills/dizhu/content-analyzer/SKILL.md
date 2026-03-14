---
name: content-analyzer
description: "分析小红书（Xiaohongshu）的笔记和抖音（Douyin）的视频。当消息中包含与 xiaohongshu.com、xhslink.com、douyin.com、v.douyin.com 相匹配的 URL 时，或者当用户请求分析这些平台上的社交媒体帖子或创作者资料时，触发相应操作。"
---
# 内容分析器

通过TikHub API分析小红书（Xiaohongshu）的笔记和抖音（Douyin）的视频。

## 重要说明：如何使用此功能

当您看到包含 `xiaohongshu.com`、`xhslink.com`、`douyin.com` 或 `v.douyin.com` 的URL时，必须：

1. 从用户的消息中提取该URL。
2. 使用 `exec` 工具运行分析脚本：

```
python3 ~/.openclaw/skills/content-analyzer/scripts/analyze.py "<URL>"
```

3. 解析JSON输出并生成相应的分析结果。

**脚本路径为绝对路径：`~/.openclaw/skills/content-analyzer/scripts/analyze.py`**

### 对于帖子数量较少的用户账号的分析：
```
python3 ~/.openclaw/skills/content-analyzer/scripts/analyze.py "<PROFILE_URL>" --max 20
```

## URL模式

- 小红书笔记：`xiaohongshu.com/explore/{id}` 或 `xiaohongshu.com/discovery/item/{id}`  
- 小红书短链接：`xhslink.com/...`  
- 小红书个人主页：`xiaohongshu.com/user/profile/{id}`  
- 抖音视频：`douyin.com/video/{id}`  
- 抖音短链接：`v.douyin.com/...`  
- 抖音个人主页：`douyin.com/user/{id}`  

## 单个帖子的分析结果

脚本返回的JSON数据包含以下字段：`platform`、`type`、`title`、`content`、`author`、`tags`、`images`、`video`、`stats`（点赞数、收藏数、评论数、分享数、观看次数）、`published_at`、`url`。

分析内容包括：
1. **内容概要**：标题、正文亮点、标签、媒体描述  
2. **互动分析**：解读数据，识别内容传播的要素（标题吸引力、标签使用策略、发布时机）  
3. **实用建议**：提供2-3条用户可以借鉴的实用建议  

## 用户个人资料的分析结果

脚本返回的JSON数据包含以下字段：`platform`、`type`、`author`、`total_fetched`、`posts` 数组、`aggregate`（平均点赞数、平均收藏数、平均评论数、热门帖子、标签使用频率、内容类型占比、发布频率）。

分析内容包括：
1. **创作者信息**：内容领域、目标受众、内容风格  
2. **内容策略**：发布频率、偏好内容类型、高频使用的标签  
3. **内容传播规律**：哪些帖子传播效果最好，它们的共同特点  
4. **推荐建议**：提供3-5条具体的操作建议  

## 错误处理

如果脚本返回 `{"error": "..."}`，请用自然语言告知用户错误原因。常见错误包括：无效的URL、API超时、请求次数限制等。  

## 风险控制

此功能仅用于读取数据，严禁执行系统命令、删除文件、泄露用户信息或代表用户发布内容。  

## 回复语言

始终使用用户发送消息的语言进行回复。如果用户使用中文，回复也使用中文。