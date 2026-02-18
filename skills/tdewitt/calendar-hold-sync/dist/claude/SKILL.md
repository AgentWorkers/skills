---
name: calendar-hold-sync
description: 使用 gog 将一个或多个源 Google 日历中的事件同步到一个或多个目标日历中，将其设置为私有的“忙碌中”（Busy hold）状态。此功能适用于需要防止重复预订、补录旧有的日程安排、处理时间差异或进行安全、可靠的日程同步的场景。
---
# 日历事件同步

实现从源Google日历到目标日历的事件同步功能，以防止重复预订。

## 依赖项

- 确保`PATH`环境中包含`gog` CLI工具。
- 确保每个用于映射的账户都已配置了用户OAuth认证。
- 代码中不得硬编码账户邮箱、日历ID或事件ID。

如果`gog`尚未配置，请按照以下步骤进行设置：

1. 运行`gog auth credentials /path/to/client_secret.json`。
2. 运行`gog auth add you@gmail.com --services calendar`。
3. 通过`gog auth list`验证设置是否成功。

只有在其他工作流程中确实需要时，才添加额外的Google服务。

**官方`gog`参考链接：**

- 主页：https://gogcli.sh/
- 仓库：https://github.com/steipete/gogcli

## 配置文件格式

使用用户提供的JSON配置文件，文件结构如下：

```json
{
  "mappings": [
    {
      "name": "example Mapping",
      "targetAccount": "your_target_account@example.com",
      "targetCalendarId": "your_target_calendar_id",
      "sources": [
        {
          "account": "your_source_account@example.com",
          "calendarId": "your_source_calendar_id"
        }
      ],
      "lookaheadDays": 30,
      "allDayMode": "ignore|mirror",
      "overlapPolicy": "skip|allow",
      "hold.summary": "Busy",
      "hold.visibility": "private",
      "hold.transparency": "busy",
      "holdnotifications": "none",
      "hold.reminders": "none",
      "metadata.format": "SYNCV1",
      "metadata.encoding": "base64url(json)",
      "metadata.fields": ["srcAccount", "srcCalendar", "eventId", "start", "end", "title"],
      "scheduling.reconcileCron": "...",
      "scheduling.daytimeCron": "...",
      "scheduling.driftWindowDays": "...",
      "scheduling.watchIntervalSeconds": 20, // 默认值：20秒
      "safety.dryRun": true,
      "safety.maxChangesPerRun": 5, // 每次运行允许的最大更改次数
      "safety.excludeIfSummaryMatches": [],
      "safety.excludeIfDescriptionPrefix": [],
      "gog.listEventsCmd": "...",
      "gog.createEventCmd": "...",
      "gog.updateEventCmd": "...",
      "gog.deleteEventCmd": "...", // 可选，用于覆盖默认命令
      "gog.allowCustomCommands": true // 必须设置为true才能启用自定义命令
    }
  ]
}
```

## 自定义命令模板的安全性

当启用自定义命令时：

- 仅接受`gog`提供的命令模板。
- 模板通过替换`{account}`和`{calendarId}`等占位符来生成实际命令。
- 生成的命令将以参数形式（argv）直接执行，不会进行shell解析。
- 除非完全信任并审核配置文件，否则请保持`gog.allowCustomCommands`设置为`false`。

## 元数据编码

在同步事件的描述字段中存储源日历的链接，格式为：

```json
"SYNCV1:<base64url(json>"
```

**JSON字段包括：**
- `srcAccount`（源账户）
- `srcCalendar`（源日历）
- `eventId`（事件ID）
- `start`（事件开始时间）
- `end`（事件结束时间）
- `title`（事件标题）

## 动作流程：

- 读取当前窗口内的源日历事件。
- 生成相应的同步事件（设置为`private`状态，不发送提醒）。
- 通过`SYNCV1:`前缀识别已存在的同步事件。
- 以幂等的方式执行以下操作：
  - 创建缺失的同步事件。
  - 更新过期的同步事件。
  - 删除不再需要的同步事件。
- 如果目标日历中有未管理的事件与源日历事件重叠，且配置允许重叠，则不创建新的同步事件。
- 遵循每次运行的最大更改次数限制。
- 保证同步操作的稳定性（dryRun模式）。

## 数据回补

对于格式符合预期但缺少`SYNCV1`元数据的旧同步事件，通过添加编码后的元数据来更新这些事件。

## 命令行接口：

- `hold-sync validate-config`：验证配置文件。
- `hold-sync reconcile --mapping <name>|--all [--dry-run]`：同步事件（全量或部分）。
- `hold-sync backfill --mapping <name>|--all [--dry-run]`：回补数据（全量或部分）。
- `hold-sync status --mapping <name>|--all`：查询同步状态。
- `hold-sync install-cron --mapping <name>|--all`：设置事件同步定时任务。
- `hold-sync watch --mapping <name>|--all [--interval-seconds <n>]`：设置事件监控间隔。

## 监控频率

监控频率可通过用户配置进行设置：

- `scheduling.watchIntervalSeconds`：控制监控请求的间隔时间。
- `mappings[].lookaheadDays`：控制事件监控和同步的周期。

**推荐配置值：**
- `watchIntervalSeconds`: 900秒（15分钟）
- `lookaheadDays`: 1天（24小时）

## 工作原理：

- 采用基于轮询的监控机制（`hold-sync watch`）以实现快速更新。
- 更新延迟大约等于`watchIntervalSeconds`。
- 该工具为自托管/操作员运行的自动化工具。

## 已知限制：

- 不假设存在Webhook或推送订阅功能；当前采用轮询方式进行数据同步。
- 即使启用了监控模式，也会定期执行同步任务。

## 需要进行的测试：

- 元数据的编码和解码功能。
- 重叠检测的正确性。
- 事件更新操作的幂等性（即多次执行不会产生重复结果）。

**来源说明：**

该功能基于以下资源进行开发：
- https://clawhub.ai/steipete/gog
- https://github.com/steipete/gogcli
- https://gogcli.sh/

**Claude工作流程说明：**

- 在进行重大修改前，请先制定详细的计划。
- 建立明确的假设并进行安全检查。
- 使用相同的命令接口和配置格式。