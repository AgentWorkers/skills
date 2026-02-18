---
name: content-research
description: 研究热门话题，并为特定平台生成相关内容。触发条件包括：“research [topic]”（研究[主题]）、“what's new in [topic]”（[主题]的最新动态）、“content for [platform]”（[平台]的相关内容）、“create posts about [topic]”（创建关于[主题]的帖子）。支持Reddit、X/Twitter、Discord、LinkedIn等平台，并为每个平台提供多种内容创作方向。
---
# 内容研究

工作流程分为两个阶段：**研究** → **创作**

---

## 第一阶段：研究

**触发条件：`research [主题]`，`[主题] 的最新动态`

### 1. 搜索

使用网络搜索工具查找最新新闻：
```
web_search(query="[topic] news", freshness="pw")
```

**搜索模式：**
- 新闻：`[主题] 新闻`
- Reddit：`site:reddit.com [主题]`
- X/Twitter：`site:x.com [主题]`

### 2. 获取文章内容

提取文章内容：
```
web_fetch(url="[URL]", maxChars=8000)
```

### 3. 筛选

- **7天时间限制** — 忽略过期的内容
- 跳过介绍性文章（如“什么是X”）
- 跳过价格预测或技术分析类内容
- 优先选择：产品发布、合作伙伴关系、更新、行业动态、重要里程碑等

### 4. 呈现结果
```markdown
## [Topic] Research — [Date]

1. **[Headline]** - [Source] - [X days ago]
   [2-3 sentence summary]
   
2. **[Headline]** - [Source] - [X days ago]
   [2-3 sentence summary]

[up to 5 items, newest first]
```

---

## 第二阶段：内容创作

**触发条件：`为[平台]创建内容`，`为Reddit创建内容`

### 平台格式要求

#### Reddit
- 标题要吸引人（避免使用标题党）
- 2-4段对话式的文字
- 包含文章链接
- 文章结尾处提供讨论提示

**创作角度：**
1. **新闻报道** — 直截了当的报道
2. **讨论** — “你怎么看……”
3. **分析** — 你对事件影响的看法
4. **简单解释** — 用简单的语言解释复杂内容
5. **反向观点** — 从不同角度进行讨论

#### X/Twitter
- 字数不超过280个字符（或一条推文）
- 第一行要吸引读者的注意力
- 使用换行符提高可读性

**创作角度：**
1. **突发新闻** — 只呈现事实，强调紧迫性
2. **热点观点** — 引发讨论的观点
3. **多条推文** — 分享详细内容
4. **评论回应** — 对公告进行评论
5. **幽默内容** — 以幽默的方式分享

#### Discord
- 使用项目符号列表（避免使用表格）
- 链接需用`<https://...>`格式显示
- 使用粗体或大写字母来强调重点

**创作角度：**
1. **提醒** — 简短的信息+链接
2. **总结** — 关键要点
3. **讨论** — 邀请用户发表意见
4. **详细解释** — 分享详细内容
5. **幽默内容** — 与社区互动

#### LinkedIn
- 保持专业的语气
- 开篇提供见解
- 3-5段简短的文字
- 文章结尾处提出问题

**创作角度：**
1. **行业洞察** — 事件对行业的影响
2. **经验教训** — 从事件中得到的启示
3. **预测** — 事件的发展趋势
4. **职业影响** — 事件对职业发展的影响
5. **案例研究** — 深入分析事件案例

---

## 品牌风格（可选）

对于品牌相关的内容，可以创建一个`brand-config.md`文件来规定品牌风格和内容创作指南：

```markdown
# Brand: [Name]

## Voice
- [Tone descriptor]
- [Communication style]

## Avoid
- [Things not to say]

## Include
- [Required elements]
```

在创作品牌相关内容时，请参考该文件以确保风格的一致性。

---

## 示例流程
```
User: research defi

Agent: [Returns 5 findings from past 7 days]

User: 2 for reddit

Agent: [5 Reddit angles for finding #2]

User: angle 3

Agent: [Ready-to-post content]
```