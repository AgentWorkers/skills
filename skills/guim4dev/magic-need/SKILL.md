---
name: magic-need
description: 在任务执行过程中，该技能用于收集AI代理所需工具和数据的信息。当代理发现需要某个不存在的工具、API或数据源时，该技能会提供一个命令行界面（CLI）来记录这些需求。这些需求会自动被分类，并可定期进行审查，以制定集成计划。适用于代理发现某些资源不可用的情况，例如：“我需要X API才能顺利完成这项任务”、“如果我能访问Y日志，就能进行进一步分析”、“一个能够执行Z操作的工具在这里会非常有用”。
---
# magic-need

这个功能可以帮助您记录人工智能（AI）代理所需的功能或资源，让代理为您规划产品需求。

## 概述

当AI代理在执行任务时遇到数据或工具不足的障碍时，该功能允许代理准确记录其缺失的内容。随着时间的推移，这些记录会形成一个按优先级排序的集成和功能开发路线图。

该功能的灵感来源于Sonarly的`magic_fetch`概念——为代理提供一个“无实际功能的工具”，让它告诉您真正需要什么。

## 使用方法

### 作为代理（在任务执行过程中）

当您发现需要某些资源但当前没有时：

```bash
# Option 1: Use the CLI directly
node ~/.openclaw/skills/magic-need/scripts/cli.js "API for recent deploys of service X"

# Option 2: Use via shell exec
exec({
  command: 'node ~/.openclaw/skills/magic-need/scripts/cli.js "CPU metrics for upstream service"'
})
```

命令行界面（CLI）会：
1. 将需求保存到`~/.magic-need/needs.json`文件中。
2. 自动对需求进行分类（集成、可观测性、DevOps、认证、数据库、存储等）。
3. 返回包含需求ID的确认信息。

### 作为人类（审核需求）

```bash
# List all needs
node scripts/cli.js list

# Generate a report (grouped by category)
node scripts/cli.js report

# Archive resolved needs
node scripts/cli.js clear
```

## 自动分类

需求会根据描述中的关键词自动分类：

| 分类 | 关键词 | 需求示例 |
|----------|----------|--------------|
| `集成` | api, endpoint | “用于获取用户数据的API” |
| `可观测性` | metric, log, monitor | “过去一小时的错误日志” |
| `DevOps` | deploy, pipeline, ci | “服务X的最新部署情况” |
| `认证` | user, auth, login, permission | “服务Y的认证令牌” |
| `数据库` | database, db, query, schema | “查询活跃用户信息” |
| `存储` | file, storage, upload, s3 | “将文件上传到云存储” |
| `其他` | （默认） | 其他需求 |

## 数据格式

需求以JSON格式存储在`~/.magic-need/needs.json`文件中：

```json
[
  {
    "id": "j8ldlr",
    "description": "API for recent deploys",
    "createdAt": "2026-03-07T18:09:18.123Z",
    "status": "pending",
    "category": "integration"
  }
]
```

## 报告格式

`report`命令会生成格式化的报告：

```
🪄 **Magic Need Report** — 4 pending

🔌 **INTEGRATION** (2)
  • API for recent deploys of auth-service
  • Feature flags toggled recently

📊 **OBSERVABILITY** (1)
  • CPU metrics for upstream database

📝 **GENERAL** (1)
  • Tool to visualize data flow
```

## 最佳实践

### 正确的需求描述

请具体说明您的需求：
- ✅ “过去2小时内服务X的部署所需的API接口”
- ✅ “上游认证服务Pod的CPU和内存指标”
- ✅ “api-gateway在过去24小时内更改的功能开关”
- ✅ “按受影响用户群体分类的Sentry错误”

### 错误的需求描述

避免使用模糊的描述：
- ❌ “需要更多数据”
- ❌ “没有工具就无法完成”
- ❌ “如果有日志会更好”

### 集成路线图

定期查看生成的报告，以便：
1. 发现规律（哪些类别的需求最多？）
2. 确定优先级（哪些需求阻碍了任务的进展？）
3. 先开发最具影响力的工具。

## CLI参考

完整实现代码请参见`scripts/cli.js`。

### 命令

| 命令 | 描述 |
|---------|-------------|
| `cli.js "description"` | 注册一个新的需求 |
| `cli.js list` | 列出所有需求 |
| `cli.js report` | 生成格式化的报告 |
| `cli.js clear` | 归档待处理的需求 |

## 定时任务集成

要接收每日报告，请设置一个定时任务：

```bash
# Daily at 10 PM
0 22 * * * node ~/.openclaw/skills/magic-need/scripts/cli.js report | your-notification-script
```

或者使用OpenClaw的定时任务系统将报告发送到Discord频道。