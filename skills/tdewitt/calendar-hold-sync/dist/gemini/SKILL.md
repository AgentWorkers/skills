---
name: calendar-hold-sync
description: 使用 gog 将一个或多个源 Google 日历中的事件同步到一个或多个目标日历中，将这些事件设置为私有的“忙碌中”（Busy Hold）状态。此功能适用于需要防止重复预订、补录旧的日程安排、进行数据同步或确保日程安排安全性的场景。
---
# 日历事件同步

实现从源Google日历到目标日历的事件同步功能，以防止重复预订。

## 依赖项

- 确保`PATH`环境中包含`gog` CLI工具。
- 确保每个用于映射的账户都已配置用户OAuth认证。
- 代码中不得硬编码账户邮箱、日历ID或事件ID。

如果`gog`未配置，请按照以下步骤进行设置：

1. 运行`gog auth credentials /path/to/client_secret.json`。
2. 运行`gog auth add you@gmail.com --services calendar`。
3. 通过`gog auth list`验证配置是否正确。

只有在其他工作流程中确实需要时，才添加额外的Google服务。

**官方`gog`参考链接：**

- 主页：https://gogcli.sh/
- 仓库：https://github.com/steipete/gogcli

## 配置文件格式

使用用户提供的JSON配置文件，格式如下：

```json
{
  "mappings": [
    {
      "name": "示例映射名称",
      "targetAccount": "目标账户",
      "targetCalendarId": "目标日历ID" (默认为"primary"),
      "sources": [
        {
          "account": "源账户",
          "calendarId": "源日历ID"
        }
      ],
      "lookaheadDays": 30, // 提前查看天数（默认值）
      "allDayMode": "ignore" | "mirror", // 全天显示模式
      "overlapPolicy": "skip" | "allow", // 事件重叠策略
      "hold.summary": "Busy", // 事件状态（默认值）
      "hold.visibility": "private", // 事件可见性（默认值）
      "hold.transparency": "busy", // 事件透明度（默认值）
      "holdnotifications": "none", // 通知设置（默认值）
      "hold.reminders": "none", // 提醒设置（默认值）
      "metadata.format": "SYNCV1", // 元数据格式
      "metadata.encoding": "base64url(json)", // 元数据编码方式
      "metadata.fields": [
        "srcAccount", "srcCalendar", "eventId", "start", "end", "title"
      ],
      "scheduling.reconcileCron": "", // 同步调度规则
      "scheduling.daytimeCron": "", // 日间调度规则（可选）
      "scheduling.driftWindowDays": "", // 事件漂移窗口天数（可选）
      "scheduling.watchIntervalSeconds": 20, // 监控间隔秒数（默认值）
      "safety.dryRun": true, // 干运行模式（默认值）
      "safety.maxChangesPerRun": 5, // 每次运行最大更改次数
      "safetyexcludeIfSummaryMatches": [], // 排除条件（可选）
      "safety.excludeIfDescriptionPrefix": [], // 排除条件（可选）
      "gog.listEventsCmd": "", // 查看事件命令（可选）
      "gog.createEventCmd": "", // 创建事件命令（可选）
      "gog.updateEventCmd": "", // 更新事件命令（可选）
      "gog.deleteEventCmd": "", // 删除事件命令（可选）
      "gog.allowCustomCommands": true // 允许自定义命令（必须设置为true）
    }
  ]
}
```

## 自定义命令模板安全机制

启用自定义命令时：

- 仅接受`gog`提供的命令模板。
- 模板中的占位符（如`{account}`和`{calendarId}`会被替换为实际值。
- 执行后的命令将以参数形式传递（不进行shell插值）。
- 除非完全信任并审核配置文件，否则保持`gog.allowCustomCommands`设置为`false`。

## 元数据编码

在事件描述中存储源日历的链接，格式为：

```json
"SYNCV1:<base64url(JSON>"
```

**JSON字段：**

- `srcAccount`：源账户
- `srcCalendar`：源日历
- `eventId`：事件ID
- `start`：事件开始时间
- `end`：事件结束时间
- `title`：事件标题

## 行为逻辑

对于每个映射规则：

1. 读取当前窗口内的源日历事件。
2. 生成相应的目标日历事件（状态为`private`，显示为`busy`，不发送提醒）。
3. 通过`SYNCV1:`前缀识别已存在的事件。
4. 以幂等方式执行以下操作：
   - 创建缺失的事件。
   - 更新已漂移的事件。
   - 删除过时的事件。
5. 如果事件重叠策略设置为`skip`，则不创建重复的事件。
6. 遵循`maxChangesPerRun`的限制。
7. 保持`dryRun`模式（仅执行必要的操作）。

## 回补机制

对于不符合`SYNCV1`格式的旧事件，通过添加编码后的元数据来更新它们。

## 命令接口

- `hold-sync validate-config`：验证配置文件
- `hold-sync reconcile --mapping <名称>|--all [--dry-run]`：同步事件
- `hold-sync backfill --mapping <名称>|--all [--dry-run]`：回补旧事件
- `hold-sync status --mapping <名称>|--all`：查看同步状态
- `hold-sync install-cron --mapping <名称>|--all`：设置同步任务
- `hold-sync watch --mapping <名称>|--all [--interval-seconds <n>]`：设置监控间隔

## 监控频率

监控频率可通过用户配置进行设置：

- `scheduling.watchIntervalSeconds`：控制监控间隔（默认为900秒，即15分钟）
- `mappings[].lookaheadDays`：控制事件检查的滚动周期（默认为24小时）

## 工作原理

- 采用基于轮询的监控机制（`hold-sync watch`）以实现快速更新。
- 更新延迟大约等于`watchIntervalSeconds`。
- 该功能为自托管/操作员执行的自动化流程。

## 已知限制

- 本功能不依赖Webhook或推送订阅；当前采用轮询方式进行同步。
- 即使启用了监控模式，也会定期执行同步任务。

## 需要测试的内容：

- 元数据的编码和解码功能
- 事件重叠检测的正确性
- 事件更新的幂等性（即多次执行不会产生重复结果）

**来源说明：**

本功能基于以下资源进行开发：
- https://clawhub.ai/steipete/gog
- https://github.com/steipete/gogcli
- https://gogcli.sh/

## （针对Gemini工作流的特别说明：）

- 明确列出所有要求和限制条件。
- 命令和结果的输出采用结构化格式。
- 保持事件同步和回补操作的一致性。