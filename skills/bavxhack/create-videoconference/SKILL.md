---
name: meetling-default
description: 默认的视频会议通过 Meetling 进行。即时通话始终使用 `/m/` 会议室，并通过 Claw 的默认方式发送相关数据。预定好的会议会提供会议链接以及电子邮件邀请模板。安全联系人的信息会直接加载（不会使用环境变量控制的文件路径）。
version: 1.3.0
metadata:
  openclaw:
    requires:
      bins:
        - node
      env:
        - MEETLING_INSTANT_THRESHOLD_MINUTES
        - SKILL_LANGUAGE_DEFAULT
---
# Meetling 默认设置（视频会议）——安全版

## 固定的 Meetling 主机地址
该技能始终使用以下地址：
https://app.meetling.de

任何环境变量都无法更改此基础 URL。

## 安全性：联系人加载
- 联系人信息仅从 `./contacts.json`（当前工作目录）中加载。
- 任何环境变量都无法覆盖该文件路径。
- 该技能不会显示联系人文件的路径。

如果 `contacts.json` 不存在或格式不正确，技能会使用空的数据集，并将接收者标记为“未解析”。

## 行为方式

### 即时会议/临时会议（始终使用 `/m/` 路径）
在满足以下任意条件时触发：
- 文本中包含 “now / right now / asap / immediately”；
- 或包含德语对应的表达式 “jetzt / jetzt gleich / sofort / gleich”；
- 或 `start_time` 在 `MEETLING_INSTANT_THRESHOLD_MINUTES` 分钟内；
- 或参与者已确定，但未提供 `start_time`。

返回结果：
- `url`: https://app.meetling.de/m/<slug>`；
- `share`: 包含消息内容以及已解析的接收者信息的链接（适用于您的 Claw 应用发送路径）。

### 预约会议
如果 `start_time` 在未来超过 `MEETLING_INSTANT_THRESHOLD_MINUTES` 分钟之后：
- 返回包含邮件主题和正文的 `emailInvite`，以及 Meetling 会议的链接。

注意：该技能不负责自动创建 Meetling 会议界面或发送会议邀请（这些功能需要使用官方 API 或成熟的 UI 自动化工具来实现）。