---
slug: "n8n-pto-pipeline"
display_name: "N8N Pto Pipeline"
description: "创建一个 n8n 工作流，用于通过 Telegram 机器人将每日任务从 PTO 工程师分配给工头，并实现任务状态报告的功能。"
---

# n8n PTO-Foreman 工作流程（PTO-Foreman Pipeline）

## 商业案例（Business Case）

### 问题描述（Problem Statement）
建筑行业的日常工作计划包括：
- 由项目负责人（PTO，即工程团队）手动将任务分配给现场工作人员
- 任务分配采用纸质文件或电话方式
- 缺乏对任务完成情况的系统化跟踪
- 报告和状态更新延迟

### 解决方案（Solution）
通过自动化 n8n 工作流程，将 Google Sheets 中的任务列表与 Telegram 机器人连接起来，实现实时任务分配和状态收集。

### 商业价值（Business Value）
- **实时分配**：任务会在每天早上 8:00 自动发送给相关人员
- **数字化跟踪**：所有任务和状态信息集中在一个表格中
- **以移动设备为主**：现场工作人员可以使用熟悉的 Telegram 界面
- **无需安装应用程序**：任何支持 Telegram 的手机均可使用该系统

## 技术实现（Technical Implementation）

### 架构（Architecture）
```
┌─────────────────┐    ┌─────────────┐    ┌─────────────────┐
│  Google Sheets  │───>│  n8n        │───>│  Telegram Bot   │
│  (Task List)    │    │  Pipeline   │    │  (To Foreman)   │
└─────────────────┘    └─────────────┘    └─────────────────┘
        ▲                     │                    │
        │                     │                    ▼
        │              ┌──────┴──────┐      ┌───────────┐
        └──────────────│   Status    │<─────│  Foreman  │
                       │   Update    │      │  Response │
                       └─────────────┘      └───────────┘
```

### n8n 工作流程组件（n8n Pipeline Components）

#### 1. 早晨触发器（Morning Trigger，8:00 AM）```json
{
  "nodes": [
    {
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "parameters": {
        "rule": {
          "interval": [
            {"field": "hours", "hoursInterval": 24}
          ]
        },
        "triggerTimes": {"item": [{"hour": 8, "minute": 0}]}
      }
    }
  ]
}
```

#### 2. 从 Google Sheets 获取任务（Get Tasks from Google Sheets）```json
{
  "name": "Get Today Tasks",
  "type": "n8n-nodes-base.googleSheets",
  "parameters": {
    "operation": "read",
    "sheetId": "YOUR_SHEET_ID",
    "range": "Tasks!A:F",
    "options": {}
  }
}
```

#### 3. 按照现场工作人员筛选任务（Filter Tasks by Foreman）```javascript
// Filter tasks for specific foreman based on chat_id
const chatId = $node["Telegram Trigger"].json["message"]["chat"]["id"];
const tasks = $input.all();

return tasks.filter(task =>
  task.json.foreman_chat_id === chatId.toString()
);
```

#### 4. 格式化任务并通过 Telegram 发送（Format and Send via Telegram）```javascript
// Format task message
const tasks = $input.all();
let message = "📋 *Задачи на сегодня:*\n\n";

tasks.forEach((task, index) => {
  message += `*${index + 1}. ${task.json.task_name}*\n`;
  message += `   📍 Участок: ${task.json.location}\n`;
  message += `   ⏰ Срок: ${task.json.deadline}\n`;
  message += `   📝 ${task.json.description}\n\n`;
});

message += "\n_Ответьте на это сообщение статусом:_\n";
message += "✅ выполнил\n❌ не выполнил + причина";

return [{json: {message}}];
```

#### 5. 状态更新处理（Status Update Handler）```javascript
// Parse foreman response and update status
const message = $node["Telegram Trigger"].json["message"]["text"];
const replyTo = $node["Telegram Trigger"].json["message"]["reply_to_message"];

let status = "в работе";
let comment = "";

if (message.toLowerCase().includes("выполнил")) {
  status = "выполнено";
} else if (message.toLowerCase().includes("не выполнил")) {
  status = "не выполнено";
  comment = message.replace(/не выполнил/i, "").trim();
}

return [{
  json: {
    task_id: replyTo.message_id,
    status: status,
    comment: comment,
    updated_at: new Date().toISOString()
  }
}];
```

### Google Sheets 的数据结构（Google Sheets Structure）

**任务表（Tasks Sheet）：**
| 列名 | 描述 |
|--------|-------------|
| task_id | 任务唯一标识符 |
| task_name | 任务名称 |
| description | 任务详细说明 |
| location | 工作地点 |
| deadline | 截止日期/时间 |
| foreman_chat_id | 被分配任务的现场工作人员的 Telegram 聊天 ID |
| status | 当前状态 |
| comment | 现场工作人员的备注 |

**现场工作人员表（Foremen Sheet）：**
| 列名 | 描述 |
|--------|-------------|
| name | 现场工作人员姓名 |
| chat_id | 现场工作人员的 Telegram 聊天 ID |
| registered_at | 注册时间戳 |

### Telegram 机器人的设置（Telegram Bot Setup）
1. 通过 @BotFather 创建机器人
2. 获取机器人令牌
3. 在 n8n 中配置 Webhook
4. 本地测试时，可以使用 n8n tunnel：
```bash
npx n8n --tunnel
```

## 使用流程（Usage Flow）

### 对于项目负责人（PTO 工程师）：
1. 打开 Google Sheets 中的任务列表
2. 添加任务并指定相应的现场工作人员
3. 系统会在每天早上 8:00 自动发送任务

### 对于现场工作人员：
1. 通过 Telegram 机器人接收任务
2. 回复消息以更新任务状态
3. 系统会自动更新 Google Sheets 中的任务状态

### 对于项目经理：
1. 在 Google Sheets 中查看实时任务状态
2. 从历史数据中生成报告
3. 分析不同现场工作人员或工作地点的完成任务率

## 部署选项（Deployment Options）

### 本地环境（测试）（Local Environment, for Testing）```bash
npx n8n --tunnel
```

### 云服务器（生产环境）（Cloud VPS, for Production）
- Hostinger n8n：每月费用约 5 美元
- Amvera Cloud：每月费用约 170 卢布
- timeweb：每月费用约 590 卢布

## 可扩展功能（Extensions）：
- 支持为已完成的任务添加照片附件
- 与 PostgreSQL 数据库集成以支持复杂查询
- 发送提醒通知
- 生成每日/每周报告
- 与项目管理系统连接

## 资源（Resources）
- **来源**：DDC Telegram 社区讨论
- **模板**：可在 DDC 的 GitHub 仓库中获取