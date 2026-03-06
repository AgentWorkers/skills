---
name: zoom-meeting
description: >
  如何使用 Zoom REST API 创建、检索、列出和删除 Zoom 会议。  
  每当用户提到 Zoom 会议、需要安排会议、获取会议详情或请求管理 Zoom 通话时（即使他们没有明确要求使用“Zoom 会议相关功能”），都可以使用此技能。该技能支持自然语言请求和结构化的 JSON 命令。请始终以人类可读的形式回复结果（不要使用 JSON 格式）。
---
# Zoom会议管理技能

该技能支持通过Zoom REST API对Zoom会议进行程序化管理，包括创建、检索、列出和删除会议。

## 使用场景

当用户需要执行以下操作时，可以使用该技能：
- 创建或安排Zoom会议
- 获取会议详情（如加入链接、密码等）
- 查看所有即将召开的会议
- 取消或删除会议
- 在执行与会议相关的操作时提及“Zoom”

## 认证

该技能通过Zoom的服务器间OAuth机制自动处理认证。

**凭证存储位置：** `~/.openclaw/credentials/zoom.json`

**所需凭证：**
```json
{
  "account_id": "YOUR_ACCOUNT_ID",
  "client_id": "YOUR_CLIENT_ID",
  "client_secret": "YOUR_CLIENT_SECRET"
}
```

该技能会自动获取并刷新访问令牌。

## 支持的操作

### 1. create_meeting
创建一个新的Zoom会议。

**参数：**
- `topic`（必填）：会议主题/标题
- `start_time`（可选）：ISO 8601格式的日期/时间。默认值：当前时间
- `duration`（可选）：会议时长（以分钟为单位）。默认值：40分钟
- `timezone`（可选）：时区。默认值：`Asia/Almaty`

**JSON示例：**
```json
{
  "action": "create_meeting",
  "topic": "Daily Standup",
  "start_time": "2026-03-10T10:00:00",
  "duration": 30,
  "timezone": "Asia/Almaty"
}
```

### 2. get_meeting
检索现有会议的详细信息。

**参数：**
- `meeting_id`（必填）：Zoom会议ID

**JSON示例：**
```json
{
  "action": "get_meeting",
  "meeting_id": "123456789"
}
```

### 3. list_meetings
获取用户所有的会议列表。

**参数：**
- `user_id`（可选）：用户ID。默认值：`me`

**JSON示例：**
```json
{
  "action": "list_meetings"
}
```

### 4. delete_meeting
删除一个Zoom会议。

**参数：**
- `meeting_id`（必填）：Zoom会议ID

**JSON示例：**
```json
{
  "action": "delete_meeting",
  "meeting_id": "123456789"
}
```

## 使用示例

### 自然语言交互

**用户：** “明天上午10点创建一个名为‘Architecture Review’的Zoom会议。”
**操作步骤：**
1. 解析用户输入的自然语言，提取所需参数。
2. 将“明天上午10点”转换为ISO 8601格式。
3. 使用提取的参数调用`create_meeting`函数。
4. 返回易于理解的响应。

**用户：** “会议123456789的加入链接是什么？”
**操作步骤：**
1. 使用会议ID调用`get_meeting`函数。
2. 从响应中获取加入链接并返回给用户。

**用户：** “显示我所有即将召开的Zoom会议。”
**操作步骤：**
1. 调用`list_meetings`函数。
2. 将结果格式化为易于阅读的列表并返回给用户。

**用户：** “删除会议987654321。”
**操作步骤：**
1. 使用会议ID调用`delete_meeting`函数。
2. 确认会议已成功删除。

### 结构化JSON输入

用户也可以直接通过JSON格式发送命令：

```json
{
  "action": "create_meeting",
  "topic": "Sprint Planning",
  "start_time": "2026-03-11T14:00:00",
  "duration": 60
}
```

## 参数验证

如果用户提供的会议创建信息不完整，可以询问补充信息：

**用户：** “创建一个Zoom会议。”
**系统回应：** “请问会议的主题是什么？”
**用户：** “团队同步。”
**系统回应：** “会议应该什么时候开始？”
**用户：** “明天下午2点。”
**系统回应：** “会议时长是多少？（默认：40分钟）”

系统会使用收集到的参数和默认值来创建会议。

## 输出格式

始终返回**易于理解的文本**（而非JSON格式）：

**create_meeting**的示例输出：
```
✅ Meeting created!

📋 Topic: Daily Standup
🆔 Meeting ID: 123456789
🔗 Join: https://zoom.us/j/123456789
🔑 Password: 983421
⏰ Start: 2026-03-10T10:00:00
⏱ Duration: 30 min
🌍 Timezone: Asia/Almaty
```

## 错误处理

优雅地处理错误，并以易于理解的格式返回错误信息：

- **认证失败：**
```
Error: Failed to obtain access token. Check credentials in ~/.openclaw/credentials/zoom.json
```

- **无效的会议ID：**
```
Error: Meeting 123456789 does not exist or you don't have permission to access it
```

- **API错误：**
```
Error: Zoom API returned error 429: Rate Limited
```

## 实现方式

该技能通过`scripts/zoom_api.py`脚本与Zoom API进行交互。该脚本负责：
- 从文件中加载凭证
- 生成和刷新OAuth令牌
- 向Zoom API发起HTTP请求
- 解析响应并处理错误

**主要API接口：**
- 创建会议：`POST /users/me/meetings`
- 获取会议信息：`GET /meetings/{meetingId}`
- 列出会议：`GET /users/me/meetings`
- 删除会议：`DELETE /meetings/{meetingId}`

## 默认值

| 参数          | 默认值         |
|---------------|--------------|
| start_time     | 当前时间        |
| duration      | 40分钟        |
| timezone       | Asia/Almaty       |

## 会议创建规则
- 会议总是创建在`/users/me`路径下（针对已认证的用户）
- 确保不会创建重复的会议（每个请求都会创建一个新的会议）
- 所有会议均为预定会议（类型为2）

## 参考文件

- `references/zoom_api_reference.md` - 详细的API文档、接口说明和错误代码

## 设计原则

- **简洁性**：响应简洁明了
- **一致性**：相同的输入总是产生相同的输出结构
- **易于AI代理解析**：响应格式符合AI代理的解析要求
- **安全处理凭证**：绝不将凭证暴露在日志或输出中
- **人类可读的输出**：始终返回易于理解的文本（而非JSON）
- **本地时间显示**：会议时间以指定时区显示（而非UTC）

## 依赖库

- `requests`：用于发送HTTP请求到Zoom API
- `pytz`：用于时区转换（自动安装）