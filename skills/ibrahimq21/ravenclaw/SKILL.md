# Ravenclaw操作技能

**类别：** 邮件自动化 / 通信

**描述：** 操作Ravenclaw邮件系统——发送电子邮件、安排邮件发送时间、检查收件箱以及管理邮件工作流程。支持将POP3邮箱中的邮件转发到Discord webhook，并具备定时发送功能。

**维护者：** Ibrahim Qureshi (@ibrahimq21)

**标签：** 邮件、Discord、webhook、自动化、smtp、pop3、定时

---

## 功能

- 通过SMTP立即发送电子邮件
- 安排邮件在未来特定时间发送
- 检查收件箱及未读邮件
- 手动触发邮件检查
- 查看已安排的邮件队列
- 取消已安排的邮件
- 系统健康检查及统计信息

---

## 需求

### 本地设置（直接操作）

**Ravenclaw必须正在运行：**
```bash
# Start Ravenclaw bridge
cd path/to/ravenclaw
python ravenclaw.py

# Default port: 5002
```

**环境变量：**
- `RAVENCLAW_URL`（可选）：Ravenclaw API的自定义URL（默认：`http://localhost:5002`）

### 社区共享

用户使用此技能需满足以下条件：
1. 本地安装了Ravenclaw
2. Ravenclaw正在运行
3. 通过环境变量或`RAVENCLAW_URL`进行配置

---

## 命令

### 发送电子邮件

立即发送一封电子邮件。

**格式：**
```
send email to [recipient] with subject [subject] and body [body]
```

**示例：**
```
send email to manager@company.com with subject "Leave Request" and body "I would like to take leave tomorrow."
```

**参数：**
- `recipient`（必填）：收件人邮箱地址
- `subject`（必填）：邮件主题
- `body`（必填）：邮件内容

**API调用：`POST /send`

---

### 安排电子邮件

安排邮件在指定时间发送。

**格式：**
```
schedule email to [recipient] with subject [subject] and body [body] at [time]
```

**示例：**
```
schedule email to hr@company.com with subject "Leave Application" and body "Requesting leave for next Monday" at "2026-02-23T09:00:00"
```

**参数：**
- `recipient`（必填）：收件人邮箱地址
- `subject`（必填）：邮件主题
- `body`（必填）：邮件内容
- `time`（必填）：ISO-8601时间戳（例如：`2026-02-23T09:00:00`）

**API调用：`POST /schedule`

**提示：**
- 使用格式：`YYYY-MM-DDTHH:MM:SS`
- 时间必须在未来
- 高优先级的邮件会有更多的重试机会

---

### 查看已安排的邮件

查看所有已安排的邮件。

**格式：**
```
list scheduled emails
show scheduled emails
```

**API调用：`GET /schedule/list`

**响应内容：**
- 总邮件数量
- 待发送邮件数量
- 邮件列表（包含状态、发送时间、收件人信息）

---

### 取消已安排的邮件

取消待发送的邮件。

**格式：**
```
cancel scheduled email [id]
```

**示例：**
```
cancel scheduled email sched_20260223100000_0
```

**API调用：`POST /schedule/cancel/<id>`

---

### 检查收件箱

手动检查收件箱。

**格式：**
```
check inbox
check emails
```

**API调用：`POST /check`

**操作：**
- 从POP3服务器获取新邮件
- （如果配置了）将邮件转发到Discord
- 更新收件箱信息

---

### 查看未读邮件

获取未读邮件的列表。

**格式：**
```
show unread emails
get unread
```

**API调用：`GET /unread`

---

### 查看所有邮件

获取收件箱中的所有邮件。

**格式：**
```
show inbox
list emails
```

**API调用：`GET /inbox`

---

### 系统健康检查**

检查Ravenclaw的运行状态。

**格式：**
```
ravenclaw status
ravenclaw health
```

**API调用：`GET /health`

**响应内容：**
- 运行状态
- 账户信息
- 邮件数量
- 域名配置

---

### 统计信息

查看处理统计信息。

**格式：**
```
ravenclaw stats
email statistics
```

**API调用：`GET /stats`

**包含内容：**
- 总邮件数量
- 未读邮件数量
- 待发送的邮件数量
- 允许的域名列表

---

## 配置示例

### 直接操作（当Ravenclaw在本地运行时）

```yaml
# No special config needed
# Uses http://localhost:5002 by default
```

### 自定义URL

```bash
# Set environment variable
export RAVENCLAW_URL="http://your-server:5002"
```

### Ravenclaw .env配置文件

```env
# Required
EMAIL_HOST=mail.yourdomain.com
EMAIL_USERNAME=your@email.com
EMAIL_PASSWORD=yourpassword

# Optional
DOMAIN_FILTER=yourdomain.com
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
BRIDGE_PORT=5002
```

---

## 使用场景

- **留言请求**  
```
schedule email to manager@company.com with subject "Leave Request - March 2-6" and body "Dear Manager,\n\nI would like to request leave..." at "2026-02-16T10:00:00"
```

- **会议提醒**  
```
schedule email to team@company.com with subject "Meeting Tomorrow" and body "Don't forget about the sync meeting at 10 AM" at "2026-02-17T09:00:00"
```

- **自动通知**  
```
send email to alerts@company.com with subject "System Alert" and body "CPU usage exceeded 90%"
```

---

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| 连接失败 | Ravenclaw未运行 | 启动Ravenclaw：`python ravenclaw.py` |
| 域名不允许 | 收件人域名不在过滤列表中 | 更新`.env`文件中的`DOMAIN_FILTER` |
| 发送时间必须在未来 | 安排的时间已经过去 | 使用未来的时间戳 |
| SMTP发送失败 | 邮件服务器错误 | 检查`.env`文件中的凭据 |

---

## 故障排除

**Ravenclaw无响应：**
```bash
# Check if running
curl http://localhost:5002/health

# Start Ravenclaw
cd path/to/ravenclaw
python ravenclaw.py
```

**邮件无法发送：**
- 确认`.env`文件中的SMTP凭据是否正确
- 检查域名是否在`DOMAIN_FILTER`中
- 查看`ravenclaw.log`日志

**已安排的邮件未发送：**
- 确保Ravenclaw正在运行以执行发送任务
- 查看`/schedule/list`以获取邮件状态
- 确保`target_time`格式正确（ISO-8601）

---

## 相关文件

- **SKILL.md** — 本文档
- **skill.yaml** — 技能定义（如需）
- **ops.sh** — 辅助操作脚本（可选）

---

## 集成说明

使用此技能需要：
1. 本地运行Ravenclaw服务器
2. 在`.env`文件中配置SMTP/POP3访问信息
- 确保能够访问`localhost:5002`端口

对于社区共享，用户需要使用自己的Ravenclaw实例及相应的邮箱凭据。

---

## 相关资源

- **Ravenclaw仓库：** https://github.com/ibrahimq21/ravenclaw
- **文档：** 查看Ravenclaw仓库中的`README.md`文件