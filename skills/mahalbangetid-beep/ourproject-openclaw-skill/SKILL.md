---
name: ourproject
description: 直接通过您的 OpenClaw 代理来管理 ourproject.app 工作空间中的各项内容：项目、任务、财务信息、客户关系管理（CRM）等。
---
# OurProject OpenClaw 技能 🦞

将您的 [ourproject.app](https://ourproject.app) 账户连接到 OpenClaw 代理。您可以通过自然语言对话来查询项目、任务、财务信息、账单、客户信息以及接收通知。

## 设置

### 1. 获取 API 密钥

1. 登录到 [ourproject.app](https://ourproject.app)
2. 转到 **集成 → API 密钥**
3. 点击 **“生成 API 密钥”**
4. 复制密钥（密钥以 `op_` 开头）——该密钥仅显示一次！

### 2. 配置技能

运行设置脚本：

```bash
node scripts/setup.js
```

脚本会请求您的 API 密钥并验证连接。

如需重新测试，请运行：

```bash
node scripts/test.js
```

### 3. 完成！

现在您可以向 OpenClaw 代理询问以下内容：
- “我当前有哪些项目？”
- “今天有哪些任务需要完成？”
- “显示即将到期的账单”
- “给我一份每日总结”
- “我的财务状况如何？”
- “有哪些未读的通知？”

## 可用的命令

### 快速命令

| 命令 | 功能 |
|---------|-------------|
| `node scripts/summary.js` | 生成每日总结 |
| `node scripts/projects.js` | 列出所有项目 |
| `node scripts/tasks.js` | 列出待办任务 |
| `node scripts/deadlines.js [天数]` | 显示有截止日期的任务（默认：3 天） |
| `node scripts/bills.js [天数]` | 显示即将到期的账单（默认：7 天） |
| `node scripts/finance.js` | 查看财务概览 |
| `node scripts/notifications.js` | 显示未读通知的数量 |
| `node scripts/test.js` | 测试 API 连接 |

### API 查询（高级）

```bash
node scripts/api.js GET /projects
node scripts/api.js GET /tasks
node scripts/api.js GET /finance/dashboard
node scripts/api.js GET /crm/analytics/overview
node scripts/api.js POST /notes '{"title":"From OpenClaw","content":"Hello!"}'
```

## 您可以访问哪些数据？

| 模块 | 端点 | 所需权限 |
|--------|-----------|-------------|
| 项目 | 列出项目、查看详细信息 | `read` |
| 任务 | 列出任务、查看状态和截止日期 | `read` |
| 备注 | 列出、创建、更新备注 | `read`, `write` |
| 财务 | 查看财务概览、账户信息、交易记录 | `read` |
| 账单 | 列出账单、显示即将到期的账单 | `read` |
| 客户关系管理 (CRM) | 查看仪表板、客户信息、提醒 | `read` |
| 通知 | 查看通知数量、列出通知内容 | `read` |
| 资产 | 查看资产信息 | `read` |

## 对话示例

当用户询问他们的工作情况时，使用相应的脚本：

- “我的项目进展如何？” → `node scripts/projects.js`
- “有哪些账单即将到期？” → `node scripts/bills.js`
- “今天有哪些任务需要完成？” → `node scripts/deadlines.js 1`
- “给我今天的总结” → `node scripts/summary.js`
- “我目前的余额是多少？” → `node scripts/finance.js`
- “有哪些未读的通知？” → `node scripts/notifications.js`

## 故障排除

- **“API 密钥无效”** → 使用新的密钥重新运行 `node scripts/setup.js`
- **“连接错误”** → 确保 [ourproject.app] 可以正常访问
- **“权限错误”** → 生成具有所需权限的新 API 密钥

## 链接

- 网站：[ourproject.app](https://ourproject.app)