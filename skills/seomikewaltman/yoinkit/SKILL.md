---
name: yoinkit
description: 在13个社交平台上搜索、分析并转录内容——包括热门话题、视频字幕、帖子元数据以及跨平台的研究工作流程。
---
# Yoinkit — OpenClaw 技能

Yoinkit 可在 13 个社交平台上搜索、分析并转录内容，包括热门话题、视频字幕、帖子元数据、创作者动态以及跨平台的研究工作流程。

## 平台参考

**在运行命令之前**，请查看 [references/platforms.md](references/platforms.md)，以了解以下信息：
- 哪些平台支持字幕/热门内容/搜索/用户动态功能
- 各平台的特定参数和选项
- 如何处理不支持的操作

## 使用要求

- 需要订阅 Yoinkit 并启用 API 访问权限
- 从 Yoinkit 设置 → OpenClaw 中获取 API 令牌

## 配置

在 OpenClaw 配置文件中设置您的 API 令牌：

```bash
# Via chat command
/config set skills.entries.yoinkit.env.YOINKIT_API_TOKEN="your-token-here"
```

或者编辑 `~/.openclaw/openclaw.json` 文件：

```json
{
  "skills": {
    "entries": {
      "yoinkit": {
        "env": {
          "YOINKIT_API_TOKEN": "your-token-here",
          "YOINKIT_API_URL": "https://yoinkit.ai/api/v1/openclaw"
        }
      }
    }
  }
}
```

> **本地测试：** 将 `YOINKIT_API_URL` 设置为 `http://localhost:8000/api/v1/openclaw`，以便在本地服务器上进行测试。如果未设置，则使用生产环境地址。

## 命令

### `yoinkit transcript <url> [options]`

从视频 URL 中提取字幕。

**支持的平台：** YouTube、TikTok、Instagram、Twitter/X、Facebook

**选项：**
- `--language CODE` — 两位字母的语言代码（仅限 YouTube 和 TikTok）。例如：`en`、`es`、`fr`

```bash
yoinkit transcript https://youtube.com/watch?v=abc123
yoinkit transcript https://youtube.com/watch?v=abc123 --language es
yoinkit transcript https://tiktok.com/@user/video/123
yoinkit transcript https://instagram.com/reel/abc123
```

---

### `yoinkit content <url>`

从社交帖子中获取完整内容及其元数据。

**支持的平台：** YouTube、TikTok、Instagram、Twitter/X、Facebook、LinkedIn、Reddit、Pinterest、Threads、Bluesky、Truth Social、Twitch、Kick

```bash
yoinkit content https://youtube.com/watch?v=abc123
yoinkit content https://twitter.com/user/status/123
yoinkit content https://reddit.com/r/technology/comments/abc
yoinkit content https://bsky.app/profile/user.bsky.social/post/abc
```

---

### `yoinkit search <platform> "<query>" [options]`

在指定平台上搜索内容。不同平台有不同的参数，请使用相应的参数。

**支持的平台：** YouTube、TikTok、Instagram、Reddit、Pinterest

**常见选项：**
- `--sort TYPE` — 对结果进行排序（具体参数因平台而异，详见下文）
- `--time PERIOD` — 按时间过滤结果（具体参数因平台而异，详见下文）
- `--cursor TOKEN` — 上一次请求的分页游标
- `--continuation TOKEN` — YouTube 的分页令牌
- `--page N` — 页码（仅限 Instagram）

**平台特定的排序参数：**
- YouTube：`relevance`、`popular`
- TikTok：`relevance`、`most-liked`、`date-posted`
- Reddit：`relevance`、`new`、`top`、`comment_count`

**平台特定的时间参数：**
- YouTube：`today`、`this_week`、`this_month`、`this_year`
- TikTok：`yesterday`、`this-week`、`this-month`、`last-3-months`、`last-6-months`、`all-time`
- Reddit：`all`、`day`、`week`、`month`、`year`

```bash
yoinkit search youtube "AI tools for creators"
yoinkit search youtube "AI tools" --sort popular --time this_week
yoinkit search tiktok "productivity tips" --sort most-liked
yoinkit search reddit "home automation" --sort top --time month
yoinkit search instagram "fitness motivation" --page 2
yoinkit search pinterest "Italian recipes"
```

---

### `yoinkit trending <platform> [options]`

获取当前的热门内容。

**支持的平台：** YouTube、TikTok

**选项：**
- `--type TYPE` — 仅限 TikTok：`trending`（默认）、`popular` 或 `hashtags`
- `--country CODE` — 仅限 TikTok：两位字母的国家代码（默认：US）
- `--period DAYS` — TikTok 的热门内容/标签筛选时间：`7`、`30` 或 `120`
- `--page N` — TikTok 的热门内容/标签筛选页码
- `--order TYPE` — 仅限 TikTok：`hot`、`like`、`comment`、`repost`

**注意：** YouTube 的热门内容查询不接受参数，它会返回当前最受欢迎的视频。

```bash
yoinkit trending youtube
yoinkit trending tiktok
yoinkit trending tiktok --type popular --country US --period 7 --order like
yoinkit trending tiktok --type hashtags --period 30
```

---

### `yoinkit feed <platform> <handle> [options]`

获取用户的最新帖子/视频。

**支持的平台：** YouTube、TikTok、Instagram、Twitter/X、Facebook、Threads、Bluesky、Truth Social

**选项：**
- `--type posts|reels|videos` — 内容类型（Instagram、Facebook）。默认值：`posts`
- `--sort latest|popular` — 排序方式（仅限 YouTube）
- `--cursor TOKEN` — 分页游标

```bash
yoinkit feed youtube MrBeast
yoinkit feed youtube @mkbhd --sort latest
yoinkit feed tiktok garyvee
yoinkit feed instagram ali-abdaal --type reels
yoinkit feed twitter elonmusk
yoinkit feed threads zuck
yoinkit feed bluesky user.bsky.social
```

**注意：** 该命令可以处理带有 `@` 前缀或没有 `@` 前缀的用户名。

---

### `yoinkit research "<topic>" [options]`

自动化研究工作流程——结合多个平台的搜索和热门内容信息。

**选项：**
- `--platforms LIST` — 以逗号分隔的平台列表（默认值：youtube,tiktok）
- `--transcripts` — 从热门搜索结果中同时获取字幕

```bash
yoinkit research "home automation"
yoinkit research "AI tools" --platforms youtube,tiktok,reddit
yoinkit research "productivity" --transcripts
```

**功能说明：**
1. 在每个平台上搜索指定主题
2. 从支持的平台中获取热门内容
3. （可选）从热门视频结果中提取字幕
4. 返回合并后的 JSON 结果以供分析

---

## 自然语言交互

您无需使用精确的命令语法。AI 模型会自动将自然语言请求转换为相应的命令：

> “TikTok 上现在什么内容最热门？”
→ `yoinkit trending tiktok`

> “从这个 YouTube 视频中提取字幕：[url]”
→ `yoinkit transcript <url>`

> “查找本周关于智能家居的热门 Reddit 帖子”
→ `yoinkit search reddit "home automation" --sort top --time week`

> “MrBeast 这周发布了什么内容？”
→ `yoinkit feed youtube MrBeast`

> “查看 @garyvee 的最新 TikTok 视频”
→ `yoinkit feed tiktok garyvee`

> “研究创作者们如何使用 AI 工具”
→ `yoinkit research "AI tools" --platforms youtube,tiktok,reddit`

---

## API 基础地址

所有请求均通过您的 Yoinkit 订阅服务进行。

```
https://yoinkit.ai/api/v1/openclaw
```

---

## 输出格式

Yoinkit 的标识符图片位于 `assets/yoinkit-logo.png`（200x200 像素，透明背景，渐变图标）。  
当平台支持图片/媒体内容时，会在结果的首条信息中显示该标识符。  

在向用户展示 Yoinkit 结果时，请遵循以下格式：
- 在输出前加上 **🟣 Yoinkit** 作为标题或标签
- 将视频/帖子结果以卡片形式展示：标题、观看次数/互动次数、发布日期、链接
- 突出显示关键元数据（观看次数、点赞数、发布日期），避免显示原始 JSON 数据
- 对于字幕结果，先提供简短的摘要，如需完整内容再提供全文
- 对于热门内容结果，以编号列表的形式展示，并附带平台信息和互动数据
- 对于研究结果，按平台分类并添加清晰的标题
- 在页面底部添加提示：**由 Yoinkit 提供支持 · yoinkit.ai**

---

## 技术支持

- 问题报告：https://github.com/seomikewaltman/yoinkit-openclaw-skill/issues
- Yoinkit 官网：https://yoinkit.ai