---
name: ms-outlook-teams-assistant
description: "在 Windows 机器上，无需依赖网页版，即可跟踪并提醒用户关于 Microsoft Outlook 电子邮件以及（可选的）Microsoft Teams 消息的状态。适用于以下场景：  
1. 监控用户的收件箱/被提及信息，并通过 Telegram/Teams 发送提醒，直到用户处理完毕；  
2. 根据现有的 Outlook 对话记录，起草简短、礼貌且不使用专业术语的电子邮件回复；  
3. 显示过去 N 天内的待办事项（默认为 7 天）。  
该功能通过 Outlook 桌面应用程序的自动化脚本（COM 接口）实现；如果配置了 Microsoft Graph，也可用于 Teams。"
---

# MS Outlook + Teams Assistant（优先支持桌面端）

## 该工具的功能

- **Outlook桌面端的提醒功能**：查找过去7天内可能需要回复的消息，并持续发送提醒，直到用户处理完毕。
- **电子邮件回复草稿生成**：根据用户设定的语气规则（对话式、简洁明了、礼貌用语；使用简单英语；避免冗余表达；不使用破折号）生成回复草稿。
- **Teams聊天消息跟踪**（可选）：如果已配置Microsoft Graph且符合租户政策，该工具会跟踪需要回复的Teams聊天消息，并发送相应的提醒。

## 安全设置

- **禁止**自动发送电子邮件或Teams消息。
- **回复草稿**：生成后保存在Outlook中，或复制到Telegram中供用户审核。
- **提醒方式**：默认通过Telegram发送；只有在用户明确启用时才会通过Teams发送提醒。

## 设置（只需一次）

### A）Outlook桌面端自动化（推荐）

1. 确保已安装并登录Outlook桌面版。
2. 安装Python依赖库（执行此操作前请先确认系统是否支持）：
   - `pip install pywin32`
3. 创建配置文件：
   - 将`references/config.example.json`复制到`references/config.json`，并根据实际需求进行修改。
   **注意**：如果配置文件中包含个人身份信息，请勿提交到版本控制系统中。

### B）通过Microsoft Graph集成Teams功能（可选）

仅适用于能够创建Entra ID应用程序并授予相应权限的情况：

- 将`references/config.example.json`复制到`references/config.json`，并填写`teams.tenantId`、`teams.clientId`和`teams.scopes`。
- 然后运行`scripts/teams_scan.py`以完成设备代码登录流程。
详细步骤请参阅`references/teams-graph-setup.md`。

## 核心工作流程

### 1）扫描并发送提醒（Outlook）

使用`scripts/scan_outlook.py`脚本。

### 1b）扫描Teams聊天记录（通过Microsoft Graph）

使用`scripts/teams_scan.py`脚本。

**参数**：
- `--days 7`（默认值：7天）

首次运行时，系统会提示输入设备代码以完成登录。

**参数**：
- `--days 7`（默认值）
- `--mode report|telegram`（默认值：report）
- `--max-items 200`（默认值：200条消息）

**筛选规则**（可在配置文件中修改）：
- 仅扫描过去N天内的消息
- 排除来自明显广播源的消息
- 优先显示用户被提及的消息（不仅包括抄送）或主题/正文包含明确请求的消息
- 优先显示用户尚未回复的消息（尽力识别）

**输出结果**：
- 显示需要处理的消息列表，包含消息主题、发送者、接收时间以及标记原因。

**后续操作**：
- 如果选择了`--mode telegram`，系统会发送一条包含详细信息的提醒消息。

### 2）处理消息（标记为已处理或设置提醒）

该工具使用本地状态文件来避免重复提醒：

- **标记为已处理**：将消息的`internetMessageId`（或备用信息：主题+时间戳）添加到已处理消息列表中。
- **设置提醒**：为消息设置`snoozeUntil`时间戳（用于延迟提醒）。

可以使用`scripts/state.py`脚本进行操作（或直接修改配置文件中的时间戳）。

### 3）生成电子邮件回复草稿（Outlook）

使用`scripts/draft_reply.py`脚本。

### 4）生成提醒信息（不发送）

首先使用`scripts/scan_all.py`更新缓存的数据，然后使用`scripts/remind.py`生成适合发送到Telegram的提醒信息（实际不发送）。

**适用场景**：
- 单个Teams聊天记录：当`needsReply`为`true`时发送提醒。
- 团组聊天记录：当`mentionedMe`为`true`且`needsReply`为`true`时发送提醒。
- Outlook消息：对于被标记为需要处理的消息发送提醒。

如果输出结果不为空，该工具会将提醒信息发送到Telegram。

**输入参数**：
- 可以提供消息的`EntryID`，或通过主题和最近的时间范围进行搜索。

**处理方式**：
- 尽量提取完整的聊天记录和相关元数据。
- 生成两种格式的回复草稿：
  - **简洁版**（2–5句话）
  - **详细版**（5–10句话）
- 回复草稿的语气规则遵循`references/writing-style.md`文件中的规定。

**输出结果**：
- 将草稿内容打印到控制台。
- 如果设置了`--create-draft`选项，还会在Outlook中生成回复草稿（但不会实际发送）。

## 需要用户提供更多信息时

仅询问无法自行判断的内容：
- 需要回复的电子邮件地址（主题/发送者/回复时间）
- 用户的意图（同意/拒绝/请求信息/确认时间）
- 任何特殊要求（截止日期、附件、收件人名称等）

请尽量减少提问数量（每次最多3个问题）。