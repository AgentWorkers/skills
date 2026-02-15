---
name: Family Todo Manager
description: **支持多用户管理的家庭待办事项列表**
---

# 家庭待办事项管理器

这是一个轻量级的、支持多用户的待办事项管理工具，适用于任何家庭，由 Node.js 和 JSON 技术构建。

## 主要功能
- 📝 **自然语言添加任务**：支持通过自然语言添加任务，例如：“明天去买牛奶”。
- 👥 **多用户支持**：支持管理员（您）、家庭成员以及合作伙伴共同管理待办事项。
- ⏰ **Cron 任务调度**：可与 OpenClaw 的 Cron 服务集成，用于每日任务提醒。
- 💾 **JSON 数据存储**：采用简单的文件存储方式（`memory/todo.json`），便于备份。
- 🆔 **唯一时间戳标识**：每个任务都有一个唯一的时间戳标识，按时间顺序排列。

## 安装方法
1. 将 `todo.js` 文件放入您的技能文件夹中（例如：`skills/family-todo/todo.js`）。
2. 确保 `memory/todo.json` 文件存在（如果文件不存在，脚本会自动创建它）。
3. **配置用户信息**：编辑 `todo.js` 文件以设置您的用户 ID（具体操作方法见下文）。

## 配置方法
打开 `todo.js` 文件，修改文件顶部的 `USERS` 常量：

```javascript
const USERS = {
  'Mark': 'YOUR_TELEGRAM_ID_HERE', // e.g., '123456789'
  'Jane': 'PARTNER_TELEGRAM_ID_HERE', // e.g., '987654321'
  'Shared':  'GROUP_ID' // Family shared tasks
};
```

## 使用方法
### 添加任务
- `node todo.js add "Buy milk" "Mark"` （添加任务：“明天去买牛奶”，关联用户：Mark）
- `node todo.js add "Walk the dog" "Susie"` （添加任务：“遛狗”，关联用户：Susie）

### 查看任务列表
- `node todo.js list` （显示所有待办任务）
- `node todo.js list Mark` （仅显示用户 Mark 的待办任务）
- `node todo.js list "Family"` （显示所有家庭成员的待办任务）

### 完成任务
- `node todo.js done <ID>` 或 `node todo.js done "Buy milk"` （标记任务为已完成）

### 日常任务提醒（Cron）
- `node todo.js brief` （早上提醒）
- `node todo.js review` （晚上回顾当天的待办事项）

## 许可证
MIT 许可证