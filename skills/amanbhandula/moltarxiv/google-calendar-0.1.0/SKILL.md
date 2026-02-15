---
name: google-calendar
description: 通过 Google Calendar API 与 Google 日历进行交互：列出即将发生的事件、创建新事件、更新或删除事件。当您需要从 OpenClaw 以编程方式访问您的日历时，请使用此技能。
---

# Google 日历技能

## 概述
该技能提供了对 Google 日历 REST API 的简单封装。它允许你执行以下操作：
- **列出** 即将发生的事件（可选地根据时间范围或查询条件进行筛选）
- **添加** 新事件，包括事件标题、开始/结束时间、描述、地点和参与者信息
- **根据事件 ID 更新** 现有事件
- **根据事件 ID 删除** 事件

该技能使用 Python 编写（文件名为 `scripts/google_calendar.py`），运行该技能之前需要设置以下环境变量（你可以使用 `openclaw secret set` 工具安全地存储这些变量）：
```
GOOGLE_CLIENT_ID=…
GOOGLE_CLIENT_SECRET=…
GOOGLE_REFRESH_TOKEN=…   # obtained after OAuth consent
GOOGLE_CALENDAR_ID=primary   # or the ID of a specific calendar
```
首次运行该技能时，可能需要执行 OAuth 流程以获取刷新令牌——请参阅下面的 **设置** 部分。

## 命令
```
google-calendar list [--from <ISO> --to <ISO> --max <N>]
google-calendar add   --title <title> [--start <ISO> --end <ISO>]
                     [--desc <description> --location <loc> --attendees <email1,email2>]
google-calendar update --event-id <id> [--title <title> ... other fields]
google-calendar delete --event-id <id>
```
所有命令都会将返回的 JSON 数据输出到标准输出（stdout）中。错误信息会被输出到标准错误（stderr）中，并导致非零的退出代码。

## 设置步骤
1. **创建一个 Google Cloud 项目** 并启用 *Google 日历 API*。
2. **创建 OAuth 凭据**（选择 *桌面应用* 类型）。请记录下 `client_id` 和 `client_secret`。
3. 运行辅助脚本以获取刷新令牌：
   ```bash
   GOOGLE_CLIENT_ID=… GOOGLE_CLIENT_SECRET=… python3 -m google_calendar.auth
   ```
   该脚本会打开浏览器（或显示一个你可以在其他地方打开的 URL），请求你授权访问。授权成功后，系统会显示刷新令牌，请将其复制下来。
4. 安全地存储这些凭据：
   ```bash
   openclaw secret set GOOGLE_CLIENT_ID <value>
   openclaw secret set GOOGLE_CLIENT_SECRET <value>
   openclaw secret set GOOGLE_REFRESH_TOKEN <value>
   openclaw secret set GOOGLE_CALENDAR_ID primary   # optional
   ```
5. 安装一次所需的 Python 包：
   ```bash
   pip install --user google-auth google-auth-oauthlib google-api-python-client
   ```

## 工作原理（简要说明）
脚本从环境变量中读取凭据，使用刷新令牌重新获取访问令牌，然后创建一个服务对象（`service = build('calendar', 'v3', credentials=creds)`），并调用相应的 API 方法。

## 参考资料
- Google 日历 API 文档：https://developers.google.com/calendar/api/v3/reference
- 安装应用的 OAuth 2.0 协议：https://developers.google.com/identity/protocols/oauth2/native-app

---

**注意：** 该技能不需要图形用户界面（GUI），完全通过 HTTP 请求进行操作，因此非常适合用于无头服务器（headless servers）。