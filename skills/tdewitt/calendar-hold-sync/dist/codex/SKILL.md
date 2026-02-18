---
name: calendar-hold-sync
description: 使用 gog 将一个或多个源 Google 日历中的事件同步到一个或多个目标日历中，将其设置为私有的“忙碌中”（Busy Hold）状态。此功能适用于需要防止重复预订、填补旧的日程安排、进行数据同步或确保日程安全的情况。
---
# 日历事件同步

实现从源Google日历到目标日历的事件同步功能，以防止重复预订。

## 依赖项

- 确保`PATH`环境中包含`gog` CLI工具。
- 确保每个用于同步的账户都已配置了OAuth认证。
- 代码中不得硬编码账户邮箱、日历ID或事件ID。

如果`gog`尚未配置，请按照以下步骤进行设置：

1. 运行`gog auth credentials /path/to/client_secret.json`。
2. 运行`gog auth add you@gmail.com --services calendar`。
3. 通过`gog auth list`验证设置是否成功。

只有在确实需要其他Google服务时，才将其添加到配置中。

**官方`gog`文档链接：**

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
      "overlapPolicy": "skip" | "allow", // 事件重叠处理策略
      "hold.summary": "Busy", // 事件状态（默认值）
      "hold.visibility": "private", // 事件可见性（默认值）
      "hold.transparency": "busy", // 事件透明度（默认值）
      "holdnotifications": "none", // 通知设置（默认值）
      "hold.reminders": "none", // 提醒设置（默认值）
      "metadata.format": "SYNCV1", // 元数据格式
      "metadata.encoding": "base64url(json)", // 元数据编码方式
      "metadata-fields": [
        "srcAccount", "srcCalendar", "eventId", "start", "end", "title"
      ],
      "scheduling.reconcileCron": "自定义调度规则",
      "scheduling.daytimeCron": "可选的日间调度规则",
      "scheduling.driftWindowDays": "可选的延迟更新天数",
      "scheduling.watchIntervalSeconds": 20, // 监控间隔秒数（默认值）
      "safety.dryRun": "是否进行模拟运行",
      "safety.maxChangesPerRun": "每次运行的最大更改次数",
      "safety.excludeIfSummaryMatches": ["排除条件", ...], // 排除条件
      "safety.excludeIfDescriptionPrefix": ["排除前缀", ...], // 排除前缀
      "gog.listEventsCmd | createEventCmd | updateEventCmd | deleteEventCmd": ["gog相关命令", ...], // 可覆盖的命令
      "gog.allowCustomCommands": true // 是否允许自定义命令（必须设置为true）
    }
  ]
}
```

## 自定义命令安全机制

当启用自定义命令时：

- 仅接受`gog`提供的命令模板。
- 模板通过替换`{account}`和`{calendarId}`等占位符来生成实际命令。
- 生成的命令将以参数形式执行（不进行shell解析）。
- 除非完全信任并审核配置文件，否则保持`gog.allowCustomCommands`设置为`false`。

## 元数据编码

在事件描述中存储源日历的链接，格式为：

```json
SYNCV1:<base64url(JSON>
```

**JSON字段包括：**
- `srcAccount`：源账户
- `srcCalendar`：源日历ID
- `eventId`：事件ID
- `start`：事件开始时间
- `end`：事件结束时间
- `title`：事件标题

## 功能流程

对于每个映射配置：

1. 读取当前窗口内的源日历事件。
2. 生成相应的目标日历事件（状态为`private`、`busy`，不发送提醒）。
3. 通过`SYNCV1:`前缀识别已存在的同步事件。
4. 以幂等方式执行以下操作：
   - 创建缺失的事件。
   - 更新过期的事件。
   - 删除不再需要的事件。
5. 如果目标日历中有未管理的事件与源日历事件重叠，且配置允许重叠，则不创建新的同步事件。
6. 遵循`maxChangesPerRun`的限制。
7. 确保执行`dryRun`（模拟运行）。

## 回补机制

对于不符合`SYNCV1`格式的旧事件，通过添加编码后的元数据来更新这些事件。

## 命令接口

- `hold-sync validate-config`：验证配置文件。
- `hold-sync reconcile --mapping <名称>|--all [--dry-run]`：同步事件（全量/模拟运行）
- `hold-sync backfill --mapping <名称>|--all [--dry-run]`：回补旧事件（全量/模拟运行）
- `hold-sync status --mapping <名称>|--all`：查询同步状态
- `hold-sync install-cron --mapping <名称>|--all`：设置同步任务
- `hold-sync watch --mapping <名称>|--all [--interval-seconds <n>]`：启动监控任务（间隔秒数）

## 监控频率

监控频率可通过用户配置进行设置：

- `scheduling.watchIntervalSeconds`：控制监控间隔。
- `mappings[].lookaheadDays`：控制事件检查的滚动周期。

**推荐配置值：**
- `watchIntervalSeconds`: 900秒（15分钟）
- `lookaheadDays`: 1天（24小时）

## 工作原理

- 采用基于轮询的监控机制（`hold-sync watch`）以实现快速更新。
- 更新延迟大约等于`watchIntervalSeconds`。
- 该工具为自托管/手动运行的自动化系统。

## 已知限制

- 不假设存在Webhook或推送订阅功能；当前采用轮询方式同步。
- 即使启用了监控模式，也会定期执行同步任务。

## 需要进行的测试：

- 元数据的编码和解码功能。
- 事件重叠检测的正确性。
- 重复执行（幂等）的同步操作。

**来源说明：**

配置流程参考：
- https://clawhub.ai/steipete/gog
- https://github.com/steipete/gogcli
- https://gogcli.sh/

**开发注意事项：**

- 修改配置后请运行验证测试。
- 建议直接更新配置文件，避免使用冗长的说明文本。
- 确保工具调用具有确定性且可重复执行。