---
name: Report
description: 您可以配置自定义的定期报告，这些报告具有灵活的调度安排、数据来源和交付格式。
---

## 该功能的用途

您可以设置任意数量的报告，这些报告会按照您指定的频率自动运行，并以您希望的格式呈现。

**示例：**
- 每周的自由职业收入总结 → 每周一通过 Telegram 发送
- 每日的健康检查报告 → 以提示信息和日志的形式呈现
- 每月的项目进度报告 → 在每月1日生成 PDF 文件
- 实时警报 → 当达到预设阈值时触发

---

## 快速参考

| 任务 | 相关文件 |
|------|------|
| 报告配置方案 | `schema.md` |
| 输出格式（聊天、PDF、HTML、JSON） | `formats.md` |
| 交付渠道和调度方式 | `delivery.md` |
| 数据收集方法 | `data-input.md` |
| 警报和阈值规则 | `alerts.md` |
| 报告示例 | `examples.md` |

---

## 创建报告

用户需要指定他们想要跟踪的信息。系统会收集以下信息：
- **报告名称** — 用于标识报告的简短名称
- **指标** — 需要包含的数据
- **调度时间** — 报告生成的频率（每日、每周、每月或按需）
- **格式** — 报告的呈现方式（聊天消息、PDF 文件或 HTML 页面）
- **交付方式** — 报告的发送目的地（Telegram、文件或电子邮件）
- **警报设置** — 可选的阈值，用于触发通知

系统会根据用户提供的信息，在 `~/reports/{name}/config.md` 文件中生成相应的配置文件。

---

## 报告存储

```
~/reports/
├── index.md                    # List of all reports
├── {name}/
│   ├── config.md               # Report configuration
│   ├── data.jsonl              # Historical data
│   ├── latest.json             # Most recent values
│   └── generated/              # Past reports (PDF, HTML)
```

---

## 调度选项

| 频率 | Cron 表达式 | 说明 |
|---------|-----------------|---------|
| 每日 | `0 9 * * *` | 每天上午9点 |
| 每周 | `0 9 * * 1` | 每周一上午9点 |
| 每两周 | `0 9 * * 1/2` | 每隔一周的周一 |
| 每月 | `0 9 1 * *` | 每月1日 |
| 每季度 | `0 9 1 1,4,7,10 *` | 1月/4月/7月/10月 |
| 按需 | - | 用户请求时生成 |

**注意：** 一份报告可以设置多种调度方式：
- 快速更新：每日通过聊天消息发送
- 完整报告：每周生成 PDF 文件

---

## 数据输入

报告的数据来源包括：
- **手动输入** — 用户手动提供数据
- **系统提示** — 系统在指定时间询问用户数据
- **API** — 如果有相应的访问权限，系统会自动从 API 获取数据
- **计算生成** — 数据基于其他指标计算得出

详细信息请参阅 `data-input.md`。

---

## 格式选项

| 格式 | 适用场景 |
|--------|----------|
| 聊天消息 | 适用于快速更新和发送警报 |
| PDF | 适用于正式报告和共享 |
| HTML | 适用于详细分析和存档 |
| JSON | 适用于数据导出和系统集成 |

相关模板请参阅 `formats.md`。

---

## 示例交互流程

**设置报告：**
```
User: "I want a weekly report of my consulting hours and revenue"
Agent: Creates ~/reports/consulting/config.md
       Schedules: Every Monday 9am
       Prompts: Sunday evening for data
```

**每周报告的生成流程：**
```
Sunday 8pm — Agent: "Time for your consulting update. Hours? Revenue?"
User: "32 hours, $4,800"
Agent: "✓ Logged. Report generates tomorrow 9am."

Monday 9am — Agent sends:
📊 Consulting Report — Week 7
• Hours: 32h (↑4h vs last week)
• Revenue: $4,800 (↑$600)
• Effective rate: $150/hr
```

---

## 报告管理

```
"List my reports" → Shows all configured reports
"Pause health report" → Stops generation temporarily
"Change consulting to biweekly" → Updates schedule
"Delete old-project report" → Removes config and data
"Run consulting report now" → Generates on-demand
```

---

### 正在运行的报告
（此处应列出所有已配置的报告列表）

### 交付偏好设置
（此处应列出默认的交付格式和渠道）

### 调度概览
（此处应说明每份报告的具体运行时间）