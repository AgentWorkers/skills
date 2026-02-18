---
name: calendar-hold-sync
description: 使用 gog 将一个或多个源 Google 日历中的事件同步到一个或多个目标日历中，将其设置为私有的“忙碌中”（Busy hold）状态。此功能适用于需要防止重复预订、补录旧版日历中的待办事项、进行时间差异调整（drift reconcile），或确保日历数据的安全同步的场景。
---
# 日历事件同步功能

该功能实现将源Google日历中的事件同步到目标日历中，以防止重复预订。

## 必需依赖项

- 确保`PATH`环境中包含`gog` CLI工具。
- 确保每个用于映射的账户都已配置了OAuth认证。
- 请勿在代码中硬编码账户邮箱、日历ID或事件ID。

如果`gog`尚未配置，请按照以下步骤进行设置：

1. 运行`gog auth credentials /path/to/client_secret.json`以获取认证信息。
2. 运行`gog auth add you@gmail.com --services calendar`以添加Google日历服务。
3. 使用`gog auth list`验证日历服务是否已成功添加。

只有在其他工作流程中确实需要时，才添加额外的Google服务。

**官方`gog`资源链接：**

- 主页：https://gogcli.sh/
- 仓库：https://github.com/steipete/gogcli

## 配置文件格式

使用用户提供的JSON配置文件，文件结构如下：

```json
{
  "mappings": [
    {
      "name": "示例映射名称",
      "targetAccount": "目标账户邮箱",
      "targetCalendarId": "目标日历ID" (默认为"primary"),
      "sources": [
        {
          "account": "源账户邮箱",
          "calendarId": "源日历ID"
        }
      ],
      "lookaheadDays": 30, // 提前查看的天数（默认值）
      "allDayMode": "ignore" | "mirror", // 全天显示模式（默认为"ignore")
      "overlapPolicy": "skip" | "allow", // 事件重叠处理策略（默认为"skip")
      "hold.summary": "Busy", // 事件状态（默认为"Busy")
      "hold.visibility": "private", // 事件可见性（默认为"private")
      "hold.transparency": "busy", // 事件透明度（默认为"busy")
      "holdNotifications": "none", // 通知设置（默认为"none")
      "hold.reminders": "none", // 提醒设置（默认为"none")
      "metadata.format": "SYNCV1", // 元数据格式（默认为"SYNCV1")
      "metadata.encoding": "base64url(json)", // 元数据编码方式（默认为"base64url(json)")
      "metadata.fields": [
        "srcAccount", "srcCalendar", "eventId", "start", "end", "title"
      ],
      "scheduling.reconcileCron": ..., // 调整策略
      "scheduling.daytimeCron": ..., // 日间调度策略（可选）
      "scheduling.driftWindowDays": ..., // 事件漂移窗口天数（可选）
      "scheduling.watchIntervalSeconds": 20, // 监控间隔秒数（默认值）
      "safety.dryRun": ..., // 安全策略（可选）
      "safety.maxChangesPerRun": ..., // 每次运行的最大更改次数
      "safetyexcludeIfSummaryMatches": ..., // 排除条件（可选）
      "safety.excludeIfDescriptionPrefix": ..., // 排除条件（可选）
      "gog.listEventsCmd|createEventCmd|updateEventCmd|deleteEventCmd": ..., // gog命令模板（可选）
      "gog.allowCustomCommands": true // 是否允许自定义命令（必须设置为true才能使用自定义命令）
    }
  ]
}
```

## 自定义命令模板安全机制

启用自定义命令时：

- 仅接受`gog`提供的命令模板。
- 模板中的占位符（如`{account}`和`{calendarId}`会被替换为实际值。
- 执行后的命令将以参数形式传递（不进行shell插值）。
- 除非完全信任并审核配置文件，否则请保持`gog.allowCustomCommands`设置为`false`。

## 元数据编码

在事件描述中存储源日历的链接，格式为：

```
SYNCV1:<base64url(JSON>
```

**JSON字段包括：**

- `srcAccount`：源账户邮箱
- `srcCalendar`：源日历ID
- `eventId`：事件ID
- `start`：事件开始时间
- `end`：事件结束时间
- `title`：事件标题

## 功能行为

对于每个映射配置：

1. 读取当前窗口内的源日历事件。
2. 生成相应的目标日历事件（状态为“private”，不显示提醒）。
3. 通过前缀`SYNCV1:`识别已存在的同步事件。
4. 以幂等方式执行以下操作：
   - 创建缺失的事件。
   - 更新已发生漂移的事件。
   - 删除过时的事件。
5. 如果目标日历中有未管理的事件与源日历事件重叠，且配置为`skip`策略，则不创建新的同步事件。
6. 遵循`maxChangesPerRun`限制。
7. 保证每次运行不会超过`dryRun`设定的最大更改次数。

## 后补机制

当存在唯一匹配的源日历事件但目标日历缺少同步数据时，会通过添加编码后的元数据来补全这些数据。

## 命令接口

- `hold-sync validate-config`：验证配置文件。
- `hold-sync reconcile --mapping <name>|--all [--dry-run]`：同步事件（全量/增量）
- `hold-sync backfill --mapping <name>|--all [--dry-run]`：补全数据（全量/增量）
- `hold-sync status --mapping <name>|--all`：查询状态
- `hold-sync install-cron --mapping <name>|--all`：设置调度任务
- `hold-sync watch --mapping <name>|--all [--interval-seconds <n>]`：启动监控任务（间隔秒数）

## 监控频率

监控频率可通过用户配置进行设置：

- `scheduling.watchIntervalSeconds`：控制监控间隔。
- `mappings[].lookaheadDays`：控制滚动监控/同步的窗口时长。

**推荐配置值：**

- `watchIntervalSeconds`: 900秒（15分钟）
- `lookaheadDays`: 1天（24小时）

## 工作原理

- 采用基于轮询的监控机制（`hold-sync watch`）以实现快速更新。
- 更新延迟大约等于`watchIntervalSeconds`。
- 该功能为自托管/操作员执行的自动化脚本。

## 注意事项

- 本功能不依赖Webhook或推送订阅；当前采用轮询方式同步数据。
- 即使启用了监控模式，也会定期执行同步任务。

## 需要测试的内容：

- 元数据的编码和解码功能。
- 事件重叠检测的正确性。
- 重复执行同步操作（创建/删除）的行为是否符合预期。

**来源说明：**

该功能基于以下资源进行开发：
- https://clawhub.ai/steipete/gog
- https://github.com/steipete/gogcli
- https://gogcli.sh/

**针对OpenClaw的说明：**

在将数据发布到ClawHub或OpenClaw时，请使用以下配置方式：

- 保持说明以实现细节和命令操作为中心。
- 明确指出依赖项：用户必须预先配置`gog`工具。
- 优先选择可预测的脚本执行方式，避免使用特定于提供者的API；将CLI作为数据交互的边界。