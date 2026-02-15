---
name: x-monitor
description: 监控特定的X（Twitter）账号，并按照可配置的时间表展示值得关注的推文。该工具能够筛选出与技术和趋势相关的高价值内容，同时排除那些具有煽动性或政治性质的推文。适用于用户需要管理自己的X账号列表、进行手动检查或更新筛选规则的情况。
---

# X Monitor

这是一个自动化监控Twitter/X平台的工具，具备智能过滤功能，能够筛选出具有高价值的内容。

## 设置

### 1. X API凭据

将您的X API凭据保存到`~/.openclaw/workspace/x-monitor/credentials.json`文件中：

```json
{
  "bearer_token": "YOUR_BEARER_TOKEN_HERE"
}
```

### 2. 需要监控的账号

在`~/.openclaw/workspace/x-monitor/handles.json`文件中配置需要监控的账号：

```json
{
  "handles": [
    "naval",
    "paul_graham",
    "balajis",
    "vitalikbuterin"
  ]
}
```

**提示：**为避免超出API配额限制，建议最多配置10-20个账号。

### 3. 时间表配置

在`~/.openclaw/workspace/skills/x-monitor/config/schedule.json`文件中配置检查频率：

```json
{
  "timezone": "America/Los_Angeles",
  "check_times": ["08:00", "12:00", "16:00", "20:00"],
  "enabled": true
}
```

**可选参数：**
- `timezone`：IANA时区字符串（例如："America/New_York"、"Europe/London"、"Asia/Tokyo")
- `check_times`：每天检查的时间点数组（例如：`["09:00", "18:00"]`表示每天检查两次）
- `enabled`：设置为`false`可暂停定时检查

**常见时间表示例：**
- 每天4次：`["08:00", "12:00", "16:00", "20:00"]`
- 每天3次：`["09:00", "14:00", "20:00"]`
- 每天2次：`["09:00", "18:00"]`
- 每天1次：`["09:00"]`

### 4. 设置Cron作业

配置完时间表后，需要通过以下命令让代理创建Cron作业：
- `set up x monitor cron jobs`：根据`schedule.json`文件创建Cron作业
- `update x monitor schedule`：修改`schedule.json`后更新Cron作业

### 5. 重要内容筛选标准

编辑`~/.openclaw/workspace/x-monitor/noteworthy-criteria.md`文件以自定义筛选规则。

## 定期报告

报告会在`config/schedule.json`中指定的时间生成。每份报告包含：
1. **执行摘要**：重要内容的概览
2. **筛选后的推文**：按时间顺序排列的推文列表，包含作者、内容和相关指标

## 命令

**管理账号：**
- `add @username to x monitor`：添加一个新的账号到监控列表
- `remove @username from x monitor`：从监控列表中移除一个账号
- `show x monitor handles`：显示当前被监控的账号列表

**手动检查：**
- `check x now`：立即生成报告

**时间表管理：**
- `show x monitor schedule`：显示当前的时间表配置
- `set x monitor to check at 9am and 6pm`：将检查时间设置为上午9点和下午6点
- `set x monitor timezone to America/New_York`：更新时区设置
- `set up x monitor cron jobs`：根据`schedule.json`文件创建或更新Cron作业

**更新筛选标准：**
- `show noteworthy criteria`：显示当前的筛选规则
- `update noteworthy criteria`：允许用户编辑筛选规则

## 什么是重要内容（默认标准）：

**包含的内容：**
- 关于技术趋势、人工智能、加密货币、产品设计的见解
- 个人在开发或发布过程中的第一手经验
- 新颖的框架、隐喻或思维模型
- 基于数据的观察结果，并附有具体示例
- 反传统但论据充分的观点

**排除的内容：**
- 政治性的煽动性内容或党派性言论
- 通用的励志语录
- 仅用于提高互动量的内容

## API详细信息

该工具使用X API v2的`tweets/search/recent`端点：
- 每个账号每次检查的最大返回结果数量：10条
- 可获取的字段：`created_at`、`public_metrics`、`author_id`、`lang`
- 通过`author_id`可以获取用户的完整信息
- 查询模式：`from:{handle}`

## 数据存储位置：
- **凭据**：`~/.openclaw/workspace/x-monitor/credentials.json`
- **账号信息**：`~/.openclaw/workspace/x-monitor/handles.json`
- **时间表设置**：`~/.openclaw/workspace/skills/x-monitor/config/schedule.json`
- **筛选标准**：`~/.openclaw/workspace/x-monitor/noteworthy-criteria.md`
- **上次检查记录**：`~/.openclaw/workspace/x-monitor/last-check.json`（用于记录检查时间）

## Cron作业设置

在设置Cron作业时，代理会执行以下操作：
1. 从`config/schedule.json`中读取时区和时间信息
2. 使用`agentTurn`负载创建相应的Cron作业
3. 每个作业会执行以下步骤：获取推文 → 筛选重要内容 → 生成报告

**以美国洛杉矶时间为例的Cron表达式示例：**
```json
{
  "schedule": { "kind": "cron", "expr": "0 8 * * *", "tz": "America/Los_Angeles" },
  "payload": { "kind": "agentTurn", "message": "Run x-monitor check and report noteworthy tweets" }
}
```

## 错误处理机制：**
- 遇到速率限制时：暂时停止请求并记录警告信息
- 如果账号信息无效：跳过该账号并继续处理其他账号
- 如果API出现错误：记录错误信息并继续处理剩余的账号