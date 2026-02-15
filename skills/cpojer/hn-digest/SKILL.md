---
name: hn-digest
description: "根据用户请求，获取并发送 Hacker News 的首页帖子。当用户输入 “hn”、“pull HN” 或 “hn 10”，或者指定某个主题（如 “hn health”、“hn hacking” 或 “hn tech”）时，系统会发送 N 条帖子（默认为 5 条）。每条帖子以标题和链接的形式单独发送。系统会自动过滤掉与加密货币相关的帖子。"
---

# HN 摘要

## 命令格式

将以 `hn` 开头的用户消息解析为获取 Hacker News 首页摘要的请求。

支持的命令格式：
- `hn` → 默认显示 5 条帖子
- `hn <n>` → 显示 `n` 条帖子
- `hn <topic>` → 按主题筛选/优先显示相关帖子
- `hn <n> <topic>` → 同时显示 `n` 条按主题筛选的帖子
- 如果用户在查看部分帖子后再次请求更多内容（例如：“再显示 10–15 条”），视为偏移量请求，并使用 `--offset` 参数（例如：`offset 10`，显示第 11–20 条帖子）

支持的主题：
- `tech` （默认）
- `health`
- `hacking`
- `life` / `lifehacks`

## 输出要求：
- **不要** 添加任何额外的评论、前言或结尾文字。
- 将结果以 **单独的消息** 的形式发送。
- 每条帖子的格式必须如下：
  - 第一行：帖子标题
  - 第二行：`<发布时间> · <评论数量>`（例如：`45分钟前`、`6小时前`、`3天前`）
  - 第三行：Hacker News 帖子的链接（`https://news.ycombinator.com/item?id=...`）
- 在所有帖子信息之后，发送 **一条最终的消息**，该消息包含生成的图片。
- 如果聊天平台要求媒体内容包含非空文本，使用简短的标题（例如：`.`）。

## 执行流程：
1. 从用户消息中提取 `n` 和 `topic` 参数。
2. 获取并排序帖子：
   - 运行命令：`node skills/hn-digest/scripts/hn.mjs --count <n> --offset <offset> --topic <topic> --format json`
   - 默认的 `offset` 值为 0，除非用户之前请求了更多内容。
3. 以所需的 3 行格式将结果发送为 **多条单独的消息**。
4. 然后使用 `Nano Banana` 工具根据刚刚获取的帖子内容生成一张图片：
   - 使用 `skills/hn-digest/scripts/mood_prompt.mjs` 根据 JSON 数据生成提示信息。
   - 在图片中加入 3–4 个与帖子主题相关的趣味元素（不包含文字或 logo）。
   - 运行命令：`skills/hn-digest/scripts/generate_mood_nano_banana.sh ./tmp/hn-mood/hn-mood.png <topic> <n> <offset>` 生成并附加图片。
   - 将生成的图片作为另一条消息发送。

**异常处理**：
- 如果获取或排序帖子的过程失败，或者没有找到任何帖子：
  - 使用浏览器访问 `https://news.ycombinator.com/`，手动选择 N 条与技术相关的非加密类帖子，并以相同的 3 行格式发送。
- 即使如此，也要生成一张图片（保持 “Hacker News 技术深度报道”的氛围），并在图片中加入与 “香蕉” 相关的趣味元素。