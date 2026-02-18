# ClawMeter — 成本跟踪仪表盘

**实时跟踪 OpenClaw API 的使用情况和支出，并提供预算警报。**

---

## 概述

ClawMeter 是一个自托管的成本跟踪仪表盘，它可以监控您的 OpenClaw 会话日志，计算令牌使用量和 API 成本，并提供可定制的预算警报以及实时分析功能。

**适用人群：**
- 希望了解自身 AI 开支情况的用户
- 需要管理 OpenClaw 部署并控制预算的团队
- 基于成本优化模型选择的开发者
- 希望避免意外 API 费用的所有人

---

## 安装

### 先决条件

- OpenClaw 已安装并运行
- Node.js v18+（用于仪表盘服务器）
- OpenClaw 中已启用会话日志记录（默认设置）

### 设置流程

1. **克隆或下载 ClawMeter：**
   ```bash
   cd ~/.openclaw/workspace
   git clone https://github.com/yourusername/clawmeter.git
   cd clawmeter
   ```

2. **安装依赖项：**
   ```bash
   npm install
   ```

3. **进行配置（可选）：**
   ```bash
   cp .env.example .env
   # Edit .env to customize paths, budget limits, or alert settings
   ```

4. **导入现有日志：**
   ```bash
   npm run ingest
   ```

5. **启动仪表盘：**
   ```bash
   npm start
   ```

6. **打开仪表盘：**
   访问 http://localhost:3377

---

## 命令

安装此工具后，您的 OpenClaw 代理可以响应以下命令：

### 支出查询

- **“我今天花了多少钱？”**
  - 显示当天的总支出和预算百分比

- **“我的月支出是多少？”**
  - 显示当前月的总支出和预算状态

- **“显示这周的支出情况”**
  - 总结过去 7 天的支出情况

### 成本分析

- **“哪个模型最昂贵？”**
  - 按模型（Claude、GPT、Gemini 等）划分成本

- **“显示成本最高的会话”**
  - 按总成本列出成本最高的会话

- **“我的平均每日支出是多少？”**
  - 计算过去 30 天的平均每日成本

### 仪表盘与报告

- **“打开我的成本仪表盘”**
  - 提供链接 http://localhost:3377

- **“生成成本报告”**
  - 导出汇总数据（今日/本周/本月/全部时间）

### 数据管理

- **“刷新成本数据”**
  - 手动重新导入会话日志

- **“清除旧的成本数据”**
  - （可选）归档或删除超过 X 天的数据

---

## API 端点

ClawMeter 提供了一个 REST API，代理可以通过该 API 查询数据：

### 摘要统计

```bash
GET http://localhost:3377/api/summary
```

**响应：**
```json
{
  "today": 2.15,
  "week": 8.42,
  "month": 32.76,
  "allTime": 127.89,
  "sessions": 234,
  "messages": 1842,
  "budgetDaily": 5.0,
  "budgetMonthly": 100.0
}
```

### 日度明细

```bash
GET http://localhost:3377/api/daily?days=30
```

**响应：**
```json
[
  {
    "date": "2026-02-14",
    "cost": 2.15,
    "input_tokens": 45820,
    "output_tokens": 12340,
    "messages": 18
  }
]
```

### 会话记录

```bash
GET http://localhost:3377/api/sessions?limit=50&offset=0
```

**响应：**
```json
[
  {
    "id": "abc123",
    "agent": "main",
    "model": "claude-sonnet-4-5",
    "total_cost": 0.842,
    "message_count": 12
  }
]
```

### 模型明细

```bash
GET http://localhost:3377/api/models
```

**响应：**
```json
[
  {
    "model": "claude-sonnet-4-5",
    "provider": "anthropic",
    "total_cost": 45.62,
    "message_count": 324
  }
]
```

### 最高成本会话

```bash
GET http://localhost:3377/api/top-sessions?limit=10
```

### 预算警报

```bash
GET http://localhost:3377/api/alerts
```

### 手动导入数据

```bash
POST http://localhost:3377/api/ingest
```

---

## 配置

### 环境变量

编辑 `.env` 文件以进行自定义配置：

```bash
# Paths
OPENCLAW_AGENTS_DIR=/home/youruser/.openclaw/agents
CLAWMETER_DB=/home/youruser/.openclaw/workspace/clawmeter/data/clawmeter.db

# Server
PORT=3377

# Budgets (USD)
BUDGET_DAILY_LIMIT=5.00
BUDGET_MONTHLY_LIMIT=100.00

# Telegram alerts (optional)
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# Email alerts (optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASS=your_app_password
ALERT_EMAIL_TO=notify@yourdomain.com
```

### 预算警报

ClawMeter 会自动检查支出是否超过配置的阈值，并通过以下方式发送警报：

- **Telegram** — 发送到您的手机
- **Email** — 通过 SMTP 发送

**警报触发条件：**
- 日支出超过 `BUDGET_DAILY_LIMIT`
- 月支出超过 `BUDGET_MONTHLY_LIMIT`

**警报限制：** 每种类型每天最多发送一次警报（防止垃圾邮件）

---

## 代理集成示例

### 示例 1：每日支出检查

**用户：** “我今天花了多少钱？”

**代理响应：**
```
Let me check your spending...

📊 Today's Spend: $2.15
Budget: $5.00 (43% used)

You have $2.85 remaining today.
```

**实现方式：**
```javascript
const res = await fetch('http://localhost:3377/api/summary');
const data = await res.json();
const pct = (data.today / data.budgetDaily * 100).toFixed(0);
return `📊 Today's Spend: $${data.today.toFixed(2)}\nBudget: $${data.budgetDaily.toFixed(2)} (${pct}% used)\n\nYou have $${(data.budgetDaily - data.today).toFixed(2)} remaining today.`;
```

### 示例 2：模型比较

**用户：** “我应该使用哪个模型来节省成本？”

**代理响应：**
```
Based on your usage history:

💰 Cost per 1K messages:
• Claude Haiku 3-5: $0.12
• GPT-4o-mini: $0.18
• Claude Sonnet 4-5: $0.45
• Claude Opus 4: $1.23

Recommendation: Use Haiku for simple tasks, Sonnet for complex work.
```

### 示例 3：预算警告

**代理（主动提醒）：**
```
⚠️ Budget Alert

You've spent $5.52 today, exceeding your $5.00 daily limit.

Top sessions today:
1. Code review task — $2.10
2. Research project — $1.85
3. Email drafting — $0.98

Consider switching to a cheaper model or pausing non-urgent tasks.
```

---

## 仪表盘功能

### 概览屏幕

- **今日支出** 以及预算进度条
- **每周和每月总计**
- **历史总支出** 和消息数量
- **预算状态**（绿色/黄色/红色指示器）

### 分析功能

- **每日成本图表**（条形图，支持 7 天/14 天/30 天/90 天视图）
- **模型成本分布**（饼图，显示百分比）
- **按成本排序的最高成本会话**
- **近期活动** 动态显示

### 警报历史

- 查看所有触发的预算警报
- 查看警报的触发时间和原因
- 跟踪随时间变化的支出模式

---

## 使用场景

### 1. 个人预算管理

**场景：** 您希望将 OpenClaw 的成本控制在每月 100 美元以内。

**设置方式：**
- 设置 `BUDGET_MONTHLY_LIMIT=100.00`
- 启用 Telegram 警报
- 每周查看仪表盘

**结果：** 在超出预算前收到通知，相应调整使用情况。

### 2. 团队成本分配

**场景：** 多个团队成员共享一个 OpenClaw 实例。

**设置方式：**
- ClawMeter 按代理/会话记录成本
- 通过 API 导出数据以供报告使用
- 分析哪些代理/项目的成本最高

**结果：** 实现公平的成本分配，发现优化机会。

### 3. 模型选择优化

**场景：** 不确定应使用哪个模型来完成特定任务。

**设置方式：**
- 使用不同模型进行实验
- 在 ClawMeter 仪表盘中比较成本
- 分析每条消息的成本和每个令牌的成本

**结果：** 基于数据做出模型选择，实现成本与质量的平衡。

### 4. 生产环境监控

**场景：** OpenClaw 在生产环境中运行，需要实时监控成本。

**设置方式：**
- ClawMeter 实时导入日志
- 设置严格的预算警报
- 监控仪表盘中的异常情况

---

## 故障排除

### 仪表盘显示 0.00 美元

**原因：** 未找到会话日志或日志尚未导入。

**解决方法：**
1. 确认 `OPENCLAW_AGENTS_DIR` 指向正确的路径
2. 手动运行 `npm run ingest`
3. 检查 `agents/*/sessions/` 目录下是否存在 `.jsonl` 文件

### 自动监控功能未生效

**原因：** 文件监控工具未检测到变化。

**解决方法：**
1. 确保服务器正在运行（运行 `npm start`）
2. 查看终端是否有 `📥 X new events` 的提示信息
3. 检查会话目录的文件权限

### 预算警报未发送

**原因：** 凭据缺失或错误。

**解决方法：**
1. 重新检查 `.env` 文件中的 `TELEGRAM_BOT_TOKEN` 和 `TELEGRAMCHAT_ID`
2. 对于电子邮件，验证 SMTP 设置
3. 检查服务器日志中的错误信息

### 数据库错误

**原因：** 数据库文件损坏或被锁定。

**解决方法：**
1. 停止服务器
2. 备份 `data/clawmeter.db`
3. 删除数据库并重新运行 `npm run ingest`

---

## 高级配置

### 自定义模型定价

如果您使用自定义模型或价格发生变化：

1. 修改 `src/pricing.mjs` 文件
2. 在 `MODEL_PRICING` 对象中添加相应配置：
   ```javascript
   'your-custom-model': {
     input: 2.50,    // per million tokens
     output: 10.00,  // per million tokens
     cacheRead: 0.25,   // optional
     cacheWrite: 3.75   // optional
   }
   ```
3. 重启服务器

### 定时报告

使用 cron 任务安排每日/每周报告：

```bash
# Daily summary at 9 AM
0 9 * * * curl -s http://localhost:3377/api/summary | mail -s "Daily Cost Report" you@example.com
```

### 数据导出

导出原始数据以供外部分析：

```bash
# Export all sessions to CSV
sqlite3 data/clawmeter.db "SELECT * FROM sessions" -csv > sessions.csv
```

### 作为服务运行

创建 systemd 服务以实现持续运行：

```ini
# /etc/systemd/system/clawmeter.service
[Unit]
Description=ClawMeter Cost Tracking Dashboard
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/home/youruser/.openclaw/workspace/clawmeter
ExecStart=/usr/bin/npm start
Restart=always

[Install]
WantedBy=multi-user.target
```

**启用并启动服务：**
```bash
sudo systemctl enable clawmeter
sudo systemctl start clawmeter
```

---

## 安全性考虑

### 仅限本地访问

默认情况下，ClawMeter 绑定到 `localhost:3377`，**不暴露于互联网**。

如需远程访问，请使用 SSH 隧道：
```bash
ssh -L 3377:localhost:3377 your-server
```

### 敏感数据

会话日志可能包含对话内容。ClawMeter：
- 仅存储使用相关的元数据（令牌、成本、时间戳）
- **不** 存储消息内容或提示信息
- 数据库使用本地 SQLite（不进行云同步）

### API 认证

ClawMeter 目前**不支持认证**。在生产环境中，建议采取以下措施：

1. 在反向代理（nginx/caddy）后运行 ClawMeter 并设置认证
2. 使用防火墙规则限制访问
3. 将其部署在私有网络中

---

## 性能

### 资源使用情况

- **CPU：** 耗用极少（基于事件触发的数据导入）
- **RAM：** 约 50-100 MB
- **磁盘：** 每条消息最多占用 1 KB 的存储空间（SQLite 效率很高）
- **网络：** 完全在本地处理

### 可扩展性

ClawMeter 可轻松处理：
- **超过 10 万条消息**
- **多年的历史数据**
- **多个代理**（通过目录结构进行管理）

对于大规模部署（数百万条消息），可以考虑：
- 定期归档数据库
- 使用 PostgreSQL 作为后端（需要修改代码）

---

## 开发计划

**计划中的功能：**

- [ ] 多用户认证
- [ ] 支持大型部署的 PostgreSQL 数据库
- [ ] 数据导出格式（CSV/JSON）
- [ ] 成本预测（预测每月支出）
- [ ] 支持 Slack/Discord 通知
- [ ] 令牌使用情况热图
- [ ] 模型性能监控（延迟、质量）
- [ ] 根据使用情况提供预算建议

---

## 支持方式

- **文档：** [GitHub 项目页面](https://github.com/yourusername/clawmeter)
- **问题反馈：** [GitHub 问题列表](https://github.com/yourusername/clawmeter/issues)
- **社区：** [OpenClaw Discord 频道](https://discord.gg/openclaw)

---

## 许可证

MIT 许可证 — 永久免费且开源。

---

**由 OpenClaw 社区开发**

**跟踪您的支出，优化成本，保持控制。**