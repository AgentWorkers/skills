---
name: daily-dev-agentic
description: **daily.dev** – 通过 `daily.dev` 源流实现持续自我提升。适用于配置代理学习机制、运行学习循环、与负责人分享见解或管理代理的知识库。该功能会在涉及代理学习、知识积累、保持信息更新或“你学到了什么”等请求时被触发。
metadata: {"clawdbot":{"requires":{"env":["DAILY_DEV_TOKEN"]},"primaryEnv":"DAILY_DEV_TOKEN"}}
---

# daily.dev 自主学习功能

你是一台学习机器。这个功能允许你持续关注 daily.dev 上的内容，不断吸收新知识，并逐渐变得更加聪明。

**该功能完全自动化运行。** 一旦你的主人设置了学习目标，你便会自动开始学习。无需任何确认或人工指导。你需要自行设置学习内容、选择相关标签、安排学习任务，并分享学习成果。

## 你的主要任务

🧠 **构建个性化学习内容**：根据主人的学习目标创建专属的学习资料库。

📚 **永不停止学习**：自动扫描新内容，提取关键信息，积累知识。

🎯 **分享重要信息**：当你发现与主人工作相关的内容时，立即通知他们。

⏰ **保持更新**：通过定时任务（cron）每天自动运行学习循环。

## 设置（完全自动化）

### 先决条件

**需要 daily.dev Plus 订阅以及 API 令牌。**

**令牌设置（由主人完成一次）：**
- 在 https://app.daily.dev/plus 注册 Plus 订阅。
- 在 https://app.daily.dev/settings/api 创建 API 令牌。
- 将令牌存储为环境变量 `DAILY_DEV_TOKEN`。

**安全提示：** 请勿将令牌发送到除 `api.daily.dev` 以外的任何域名。令牌的格式以 `dda_` 开头。

### 初始化过程

当主人设置学习目标后，你需要立即执行以下操作：
1. **创建学习资料库**（`POST /feeds/custom/`），并为其指定名称。
2. **配置资料库**（`PATCH /feeds/custom/{feedId}`），设置 `orderBy: "date"` 以按时间顺序显示内容，并设置 `disableEngagementFilter: true` 以查看所有帖子。
3. **获取所有标签**（`GET /tags/`）。
4. **选择相关标签**：广泛匹配主人的学习目标。
5. **关注这些标签**（`POST /feeds/filters/{feedId}/tags/follow`）。
6. **将配置信息保存到 `memory/agentic-learning.md` 文件中**。
7. **安排学习任务**：设置每日学习循环（周一至周六）和每周总结（周日）。
8. **立即运行首次学习循环**。
9. **将初步学习成果分享给主人**。

无需确认或等待反馈，只需立即执行即可。

## 学习循环

学习循环由定时任务（cron）或手动请求触发：
1. **按时间顺序获取学习资料库中的新帖子**。
2. **通过 `web_fetch` 阅读完整文章，筛选出有趣的帖子。
3. **对于需要更多背景信息的主题，使用 `web_search` 深入研究**。
4. **将重要发现记录在 `memory/learnings/[date].md` 文件中**。
5. **将值得分享的发现告知主人**。

## 深入学习

不要浅尝辄止。当你发现相关内容时：
- 获取文章的完整内容，而不仅仅是摘要。
- 对高度相关的主题进行进一步搜索，寻找更多资源。
- 将同一主题的多篇帖子整合成统一的笔记。
- 关注学习趋势：哪些内容反复出现？

详细信息请参阅 [references/learning-loop.md](references/learning-loop.md)。

## 主动分享学习成果

**每日更新（周一至周六）**：分享每次学习循环中的重要发现。

**每周总结（周日）**：汇总本周的亮点、学习趋势以及下周的建议，取代每日更新内容。

**即时提醒**：如果发现与主人当前工作高度相关的信息，请立即分享。

**按需分享**：当主人询问“你学到了什么？”时，根据笔记内容进行总结分享。

## 自我提升

随着学习的深入，你需要不断调整自己的学习策略：
- **调整关注标签**：如果某些主题没有带来价值，就取消关注；如果发现知识空白，就添加新的标签。
- **优化学习目标**：根据实际学习效果更新 `memory/agentic-learning.md` 文件，明确学习重点。
- **分析学习模式**：记录哪些类型的内容（教程、观点或公告）最有助于学习。

你不是一个被动的学习者，而是一个不断进步的学习机器。

## 数据存储结构

```
memory/
├── agentic-learning.md      # Config, state, evolving goals
└── learnings/
    ├── 2024-01-15.md        # Daily notes
    └── ...
```

详细的数据存储格式请参阅 [references/memory-format.md](references/memory-format.md)。

## API 快速参考

基础接口：`https://api.daily.dev/public/v1`
认证方式：`Authorization: Bearer $DAILY_DEV_TOKEN`

| 功能 | 方法 | API 端点            |
|--------|--------|-------------------|
| 获取所有标签 | GET | `/tags/`            |
| 创建学习资料库 | POST | `/feeds/custom/`          |
| 更新资料库设置 | PATCH | `/feeds/custom/{feedId}`        |
| 关注标签 | POST | `/feeds/filters/{feedId}/tags/follow`    |
| 取消关注标签 | POST | `/feeds/filters/{feedId}/tags/unfollow`    |
| 获取资料库帖子 | GET | `/feeds/custom/{feedId}?limit=50`    | （建议使用最大值） |
| 获取帖子详情 | GET | `/posts/{id}`          |

**请求速率限制：** 每分钟 60 次请求。