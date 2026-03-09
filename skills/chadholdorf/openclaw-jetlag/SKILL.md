---
name: jetlag-planner
description: 该功能会扫描您的 Google 日历，找出即将到来的航班信息，并根据航班时间为您生成个性化的生物钟调整计划，然后将该计划更新回您的日历中。您可以通过以下指令来触发该功能：`check my flights`、`run jetlag planner`、`plan my trip adjustment` 或 `am I ready for my upcoming flight`。
---
按照以下步骤精确地运行时差规划工具：

## 第一步 — 检查 `.env` 文件

确认文件 `~/openclaw-jetlag/.env` 是否存在。

如果文件不存在，请立即停止并回复：

> ⚠️ 未在 `~/openclaw-jetlag/` 中找到 `.env` 文件。在运行规划工具之前，您需要添加您的 Google OAuth 凭据。请按照 README 文件中的设置说明进行操作；如果您需要帮助，请告诉我 “显示时差设置说明”。

## 第二步 — 检查 `.oauth-token.json` 文件

确认文件 `~/openclaw-jetlag/.oauth-token.json` 是否存在。

如果文件不存在，请立即停止并回复：

> ⚠️ Google 授权尚未完成。请在终端中运行以下命令以完成设置：
>
> ```
> cd ~/openclaw-jetlag && node index.js
> ```
>
> 这将打开一个浏览器，要求您登录 Google 并保存您的授权信息。完成后，再次输入 “check my flights”，我会继续为您处理后续操作。

## 第三步 — 运行规划工具

运行以下命令，并记录所有的输出（包括标准输出和标准错误）：

```bash
cd ~/openclaw-jetlag && node index.js
```

## 第四步 — 回复结果

用简洁明了的语言通过 Telegram 回复结果。不要直接发送原始输出内容，而是按照以下格式进行回复：

- 如果检测到航班并且生成了调整计划，请说明找到了哪些航班（航线和日期）以及总共创建了多少个日历事件。
- 如果输出显示未找到航班事件，请回复：“在接下来的 90 天内，您的日历中没有即将到来的航班。如果您有即将出发的航班，请检查与该日历关联的 Gmail 账户中是否收到了航空公司的确认邮件。”
- 如果找到了航班但所有航班的时区差异都在 2 小时以内，请回复：“找到了 [N] 个航班，但由于时区差异都在 2 小时以内，因此无需调整计划。”
- 如果命令以非零代码退出或显示了错误信息，请直接转发错误信息，并建议手动运行 `cd ~/openclaw-jetlag && node index.js` 以查看完整的输出内容。

回复内容请控制在 5 句以内。在 Telegram 回复中不要使用 markdown 标头，只需使用纯文本，并在列出多个航班时使用换行符分隔各项内容。