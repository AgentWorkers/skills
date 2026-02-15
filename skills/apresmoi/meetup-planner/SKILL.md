---
name: meetup-planner
description: 这是一个智能的事件查找工具，它可以根据您的兴趣搜索聚会和活动，跟踪这些活动的进度，并在活动发生前提醒您。
license: MIT
metadata:
  version: 1.0.0
  author: apresmoi
  homepage: https://github.com/apresmoi/meetup-planner
  repository: https://github.com/apresmoi/meetup-planner.git
  bootstrap: BOOTSTRAP.md
  permissions:
    network:
      - eventbrite.com
      - meetup.com
      - luma.co
    filesystem:
      - ~/.openclaw/workspace/meetup-planner/
    cron: daily-searches
---

# 活动规划助手

这是一个智能助手，能帮助您发现、跟踪并不错过任何符合您兴趣的活动。

## 一次性设置

**重要提示**：安装此技能后，代理会自动运行 `BOOTSTRAP.md` 中的引导设置流程。

引导设置流程包括：
1. 检查网页搜索和爬取功能
2. 收集您的活动偏好设置
3. （可选）设置每日自动搜索
4. 创建工作区结构

如果您没有搜索/爬取功能，系统会请求您提供相应的工具。

## 该技能的功能

设置完成后：
1. **每日搜索**：每天早上自动搜索符合您偏好的活动（如启用）
2. **活动发现**：使用可用的搜索和爬取工具在网络上查找活动
3. **活动跟踪**：保存新发现的活动供您查看
4. **智能提醒**：在活动开始前24小时和2小时发送提醒
5. **偏好设置管理**：随时更新您的兴趣和搜索条件

## 首次设置

**首次使用此技能时**，系统会按照 `BOOTSTRAP.md` 的步骤引导您完成设置。

设置过程是**交互式且友好的**：
1. ✅ 检查网页搜索和爬取功能
2. 🎯 通过友好对话了解您的活动偏好
3. ⏰ （可选）设置每日自动搜索
4. 📁 创建具有适当权限的工作区结构

**设置耗时2-3分钟**。如果您没有安装搜索/爬取工具，系统会请求您提供它们。

## 使用方法

### 初始运行
```
Run the meetup-planner skill to begin setup
```

### 日常操作
设置完成后，该技能将：
- 每天早上自动搜索活动
- 将搜索结果保存到 `events.json` 文件中
- 展示新的活动供您查看
- 跟踪您感兴趣的活动

### 发现感兴趣的活动
告诉系统：“我对 [活动名称] 感兴趣”，系统将：
- 将该活动标记为已确认
- 发送注册链接给您
- 设置24小时和2小时前的提醒

### 命令
- `update preferences` - 修改您的活动偏好设置
- `show upcoming` - 显示所有被跟踪的活动
- `remove event [名称]` - 停止跟踪某个活动
- `pause search` - 暂时停止每日搜索
- `resume search` - 恢复每日搜索

## 数据存储

该技能维护以下文件：
- `user-preferences.json` - 您的活动偏好设置
- `events.json` - 所有发现和跟踪的活动
- `event-reminders.json` - 预定的提醒信息

## 技术细节

**所需功能**：
- 网页搜索功能（任何搜索工具或技能）
- 网页爬取/抓取功能（任何抓取工具或技能）

**调度**：
- 使用系统cron作业（或等效工具）进行每日搜索
- 使用定时任务发送活动提醒

## 隐私声明

所有数据仅存储在您的本地机器上。您的偏好设置和跟踪的活动信息不会被发送到任何外部地方，除非是通过配置的API进行新活动的搜索。

## 数据传输与外部API使用

该技能会通过外部网络请求来搜索和抓取活动信息。具体使用的服务取决于您安装的搜索/爬取工具。

**传输的数据**：
- 根据您的偏好设置的搜索查询字符串（例如：“AI meetup San Francisco February 2026”）
- 需要抓取的活动页面的URL
- 您的IP地址（由网络系统自动发送）
- 您使用的搜索/爬取工具所需的任何认证凭据

**不传输的数据**：
- 您的完整偏好设置
- 活动注册状态或历史记录
- 个人备注或修改内容
- 其他被跟踪的活动信息

**数据最小化原则**：
- 仅传输完成任务所需的最必要数据
- 所有凭据均通过HTTPS安全传输
- 不进行任何遥测、分析或使用情况跟踪
- 数据不会被发送到除您配置的搜索/爬取工具之外的任何服务

---

## 代理使用说明

**重要提示**：安装此技能后，请在使用前务必运行 `BOOTSTRAP.md` 中的引导设置流程。

当调用此技能时：

### 第0阶段：检查引导设置状态（务必先运行此步骤）

**在继续其他操作之前**，请检查引导设置是否已完成：

```bash
# Check if bootstrap config exists
cat ~/.openclaw/workspace/meetup-planner/config.json 2>/dev/null
```

**如果文件不存在或 `bootstrapComplete: false`：**
- 通知用户：“👋 欢迎使用活动规划助手！我需要先进行一些设置，这只需要几分钟时间。”
- **按照 `BOOTSTRAP.md` 中的步骤逐步操作**
- 在引导设置完成之前，请勿进入第1/2/3阶段

**如果文件存在且 `bootstrapComplete: true`：**
- 根据用户的请求进入相应的阶段：
  - “立即搜索” → 进入第2阶段（每日搜索）
  - “显示即将举行的活动” → 进入第3阶段（活动确认与跟踪）
  - “更新偏好设置” → 重新运行偏好设置收集流程
  - 无特定请求 → 询问：“您想做什么？我可以搜索活动、显示即将举行的活动或更新您的偏好设置。”

### 第1阶段：设置

**所有设置均由 `BOOTSTRAP.md` 处理。详见上述第0阶段。**

### 第2阶段：每日搜索

1. **加载偏好设置**：
   - 读取 `~/.openclaw/workspace/meetup-planner/user-preferences.json`
   - 解析用户的兴趣、位置、偏好的活动类型等

2. **搜索活动**：
   - 使用您可用的搜索工具搜索符合偏好设置的活动
   - 搜索查询示例：
     - “[主题] 活动 {地点} {当前月份}”
     - “[主题] 会议 {地点} 即将举行”
     - “[主题] 研讨会 {地点}”
   - 进行多次搜索，涵盖用户的所有兴趣主题

3. **提取活动详情**：
   - 对于每个符合条件的搜索结果，使用您可用的抓取工具提取活动页面的信息
   - 提取：活动名称、日期、时间、地点、描述、注册链接
   - 可参考的网站包括：Eventbrite、Meetup.com、Luma等

4. **过滤和保存**：
   - 从 `~/.openclaw/workspace/meetup-planner/events.json` 中加载现有活动
   - 过滤掉重复项和不符合条件的活动
   - 将新活动添加到文件中
   - 为每个活动添加以下信息：`{id, name, date, time, location, url, description, cost, added_date, status: "new"`

5. **展示给用户**：
   - 以美观的格式展示新活动详情
   - 询问：“我找到了X个符合您兴趣的新活动。您想了解它们吗？”
   - 可以逐一展示活动详情，或以列表形式展示
   - 对每个活动询问用户是否感兴趣

### 第3阶段：活动确认与跟踪

1. **当用户表示感兴趣时**：
   - 在 `events.json` 中将活动状态更新为“感兴趣”
   - 提供注册链接：“这是注册链接：{url}”
   - 询问：“您注册后请告诉我！”

2. **当用户确认注册时**：
   - 在 `events.json` 中将活动状态更新为“已注册”
   - 在 `~/.openclaw/workspace/meetup-planner/reminders.json` 中设置提醒：
     ```json
     {
       "event_id": "abc123",
       "event_name": "...",
       "reminders": [
         {"time": "24_hours_before", "sent": false},
         {"time": "2_hours_before", "sent": false}
       ]
     }
     ```
   - 确认：“太好了！我会在活动开始前24小时和2小时提醒您。”

### 第4阶段：提醒系统

1. **检查提醒是否到期**（每小时检查一次）：
   - 加载 `~/.openclaw/workspace/meetup-planner/reminders.json`
   - 检查当前时间与活动时间
   - 如果距离活动还有24-25小时且24小时提醒未发送：
     - 通知用户：“提醒：[活动名称] 明天在{时间}举行！地点：{地点}”
     - 标记24小时提醒已发送
   - 如果距离活动还有2-3小时且2小时提醒未发送：
     - 通知用户：“注意！[活动名称] 将在2小时后开始！请做好准备！”
     - 标记2小时提醒已发送

2. **活动结束后**：
   - 将活动状态更新为“已结束”
   - 可选询问：“[活动名称] 体验如何？您想让我帮忙寻找类似的活动吗？”

### 第5阶段：持续操作

支持以下用户命令：
- **“update preferences”** / **“change preferences”**：重新运行偏好设置收集流程
- **“show upcoming”**：显示所有状态为“感兴趣”或“已注册”的活动
- **“show new events”**：显示状态为“新”的未查看活动
- **“remove event [名称]**：停止跟踪某个活动
- **“pause search”**：暂停每日自动搜索（更新配置）
- **“resume search”**：恢复每日自动搜索
- **“search now”**：立即执行搜索
- **“list past events”**：显示已发生的活动

## 错误处理

- **如果技能安装失败**：提供手动操作指南和GitHub链接
- **如果API密钥无效**：请求用户验证并提供新的密钥
- **如果搜索没有结果**：尝试使用更宽泛的搜索词或建议其他主题
- **如果cron设置失败**：在用户请求时提供手动搜索选项
- **如果活动抓取失败**：仅显示搜索结果链接
- **始终保护数据**：未经备份，不得覆盖 `events.json` 或 `preferences.json`

## 文件结构
```
~/.openclaw/workspace/meetup-planner/
├── user-preferences.json    # Human's event preferences
├── events.json              # All discovered and tracked events
├── reminders.json           # Scheduled reminders
├── config.json              # Skill configuration (cron schedule, etc.)
└── backups/                 # Automatic backups of data files
```