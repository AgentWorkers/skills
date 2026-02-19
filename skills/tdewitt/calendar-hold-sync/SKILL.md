---
name: calendar-hold-sync
description: 使用 `gog` 将一个或多个源 Google 日历中的事件同步到一个或多个目标日历中，并将这些事件标记为“忙”（Busy）状态。此功能适用于需要防止重复预订、补录旧版日历中的待办事项、进行数据同步以及对日程安排进行安全管理的场景。
---
# 日历事件同步

实现从源Google日历到目标日历的事件同步功能，以防止事件重复预订。

## 依赖项

- 确保`PATH`环境中包含`gog` CLI工具。
- 确保每个用于映射的账户都已配置了OAuth认证。
- 代码中不得硬编码账户邮箱、日历ID或事件ID。

如果`gog`尚未配置，请按照以下步骤进行设置：

1. 运行`gog auth credentials /path/to/client_secret.json`。
2. 运行`gog auth add you@gmail.com --services calendar`。
3. 通过`gog auth list`验证配置是否正确。

只有在特定工作流程中确实需要时，才添加额外的Google服务。

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
      "lookaheadDays": 30, // 提前查看的天数（默认值）
      "allDayMode": "ignore" | "mirror", // 全天模式：忽略或同步
      "overlapPolicy": "skip" | "allow", // 事件重叠策略：跳过或允许
      "hold.summary": "Busy", // 事件状态（默认值）
      "hold.visibility": "private", // 事件可见性（默认值）
      "hold.transparency": "busy", // 事件透明度（默认值）
      "holdnotifications": "none", // 通知设置（默认值）
      "hold.reminders": "none", // 提醒设置（默认值）
      "metadata.format": "SYNCV1", // 元数据格式（默认值）
      "metadata.encoding": "base64url(json)", // 元数据编码方式
      "metadata.fields": ["srcAccount", "srcCalendar", "eventId", "start", "end", "title"], // 元数据字段
      "scheduling.reconcileCron": "", // 调整策略
      "scheduling.daytimeCron": "", // 日间调度时间（可选）
      "scheduling.driftWindowDays": "", // 时间偏移窗口天数（可选）
      "scheduling.watchIntervalSeconds": 20, // 监控间隔秒数（默认值）
      "safety.dryRun": true, // 干运行模式（默认值）
      "safety.maxChangesPerRun": 5, // 每次运行的最大更改次数
      "safetyexcludeIfSummaryMatches": [], // 排除条件（可选）
      "safetyexcludeIfDescriptionPrefix": [], // 排除前缀（可选）
      "gog.listEventsCmd": "", // 事件列表命令（可选）
      "gog.createEventCmd": "", // 创建事件命令（可选）
      "gog.updateEventCmd": "", // 更新事件命令（可选）
      "gog.deleteEventCmd": "", // 删除事件命令（可选）
      "gog.allowCustomCommands": true // 允许自定义命令（必须设置为true才能使用这些命令）
    }
  ]
}
```

## 自定义命令模板安全机制

当启用自定义命令时：

- 仅接受`gog`提供的命令模板。
- 模板通过替换`{account}`和`{calendarId}`等占位符来生成实际命令。
- 生成的命令将作为参数（argv）直接执行，不会进行shell插值。
- 除非完全信任并审核配置文件，否则保持`gog.allowCustomCommands`设置为`false`。

## 元数据编码

在事件同步的`description`字段中存储源日历的链接，格式为：

```
SYNCV1:<base64url(JSON>
```

**JSON字段包括：**

- `srcAccount`：源账户
- `srcCalendar`：源日历
- `eventId`：事件ID
- `start`：事件开始时间
- `end`：事件结束时间
- `title`：事件标题

## 动作流程

对于每个映射配置：

1. 读取当前窗口内的源日历事件。
2. 生成相应的事件同步记录（状态为`private`、`busy`，不发送提醒）。
3. 通过`SYNCV1:`前缀识别已存在的同步记录。
4. 以幂等的方式执行以下操作：
   - 创建缺失的同步记录。
   - 更新已过时的同步记录。
   - 删除不再需要的同步记录。
5. 如果目标日历中有未管理的事件与源日历事件重叠，且配置允许重叠，则不创建新的同步记录。
6. 遵循`maxChangesPerRun`的限制。
7. 执行`dryRun`模式（仅执行一次同步操作）。

## 后补机制

对于不符合`SYNCV1`格式的旧版同步记录，可以通过添加编码后的元数据来升级这些记录。

## 命令接口

- `hold-sync validate-config`：验证配置文件。
- `hold-sync reconcile --mapping <名称>|--all [--dry-run]`：同步所有映射。
- `hold-sync backfill --mapping <名称>|--all [--dry-run]`：补全所有映射的旧记录。
- `hold-sync status --mapping <名称>|--all`：查看所有映射的状态。
- `hold-sync install-cron --mapping <名称>|--all`：为所有映射设置调度任务。
- `hold-sync watch --mapping <名称>|--all [--interval-seconds <n>]`：以指定间隔监控源日历事件。

## 监控频率

监控频率可通过用户配置文件进行设置：

- `scheduling.watchIntervalSeconds`：控制监控间隔。
- `mappings[].lookaheadDays`：控制监控/同步的滚动窗口时长。

**推荐配置值：**

- `watchIntervalSeconds`: 900秒（15分钟）
- `lookaheadDays`: 1天（24小时）

## 工作原理

- 使用基于轮询的监控机制（`hold-sync watch`）以实现快速更新。
- 更新延迟大约等于`watchIntervalSeconds`。
- 该工具为自我托管/操作员执行的自动化工具。

## 已知限制

- 本工具不依赖Webhook或推送订阅；当前采用轮询方式实现同步。
- 即使启用了监控模式，也会定期执行同步任务。

## 需要进行的测试：

- 元数据的编码和解码功能。
- 事件重叠检测的正确性。
- 重复执行同步操作（创建/删除）的正确性。

**来源说明：**

本功能基于以下资源进行开发：
- https://clawhub.ai/steipete/gog
- https://github.com/steipete/gogcli
- https://gogcli.sh/

**针对OpenClaw的注意事项：**

在将数据发布到ClawHub或OpenClaw时，请遵循以下建议：

- 保持文档以指令和命令为中心。
- 明确指出依赖项：用户必须预先配置`gog`工具。
- 优先选择可预测的脚本执行方式，避免使用特定于提供者的API；将CLI作为数据交互的边界。