---
name: icalendar-sync
description: 通过 CalDAV 协议以及 macOS 的原生桥接服务（native bridge providers），为 OpenClaw 提供安全的 iCloud 日历操作支持。这些功能适用于需要执行以下操作的场景：日历列表查询、事件检索、事件创建、事件更新（包括重复事件模式）、事件删除，以及通过密钥环（keyring）、环境变量（environment）或配置文件（config file）进行凭证设置。
---
# iCalendar 同步

使用此技能，可以通过 OpenClaw 代理执行 iCloud 日历的创建（Create）、读取（Read）、更新（Update）和删除（Delete, CRUD）操作。

## 1. 安全地准备凭证

仅使用应用程序专用的密码（切勿使用主要的 Apple ID 密码）。

建议使用密钥链（keyring）来存储凭证：

```bash
python -m icalendar_sync setup --username user@icloud.com
```

对于自动化操作，可以使用非交互式设置：

```bash
export ICLOUD_USERNAME="user@icloud.com"
export ICLOUD_APP_PASSWORD="xxxx-xxxx-xxxx-xxxx"
python -m icalendar_sync setup --non-interactive
```

仅在密钥链不可用时（例如无图形界面或受限的运行环境）才使用文件存储：

```bash
python -m icalendar_sync setup --non-interactive --storage file --config ~/.openclaw/icalendar-sync.yaml
```

## 2. 明确选择提供者（Provider）

- `--provider auto`：macOS 会使用原生日历桥接方式；非 macOS 系统则使用 CalDAV 协议。
- `--provider caldav`：强制使用直接的 iCloud CalDAV 协议。
- `--provider macos-native`：强制使用 Calendar.app 的原生日历桥接方式（仅适用于 macOS）。

如需进行 CalDAV 监控或调试，请添加以下参数：

```bash
--debug-http --user-agent "your-agent/1.0"
```

## 3. 执行日历操作

- 列出日历：
  ```bash
python -m icalendar_sync list
```

- 获取事件：
  ```bash
python -m icalendar_sync get --calendar "Personal" --days 7
```

- 创建事件：
  ```bash
python -m icalendar_sync create --calendar "Personal" --json '{
  "summary": "Meeting",
  "dtstart": "2026-02-15T14:00:00+03:00",
  "dtend": "2026-02-15T15:00:00+03:00"
}'
```

- 更新事件（简单情况）：
  ```bash
python -m icalendar_sync update --calendar "Personal" --uid "event-uid" --json '{"summary":"Updated title"}'
```

- 更新重复事件：
  ```bash
python -m icalendar_sync update \
  --calendar "Work" \
  --uid "series-uid" \
  --recurrence-id "2026-03-01T09:00:00+03:00" \
  --mode single \
  --json '{"summary":"One-off change"}'
```

- 重复事件的更新模式：
  - `single`：仅更新单个事件实例（使用 `--recurrence-id` 参数）。
  - `all`：更新整个事件系列。
  - `future`：分割事件系列并更新当前事件及后续事件（使用 `--recurrence-id` 参数）。

- 删除事件：
  ```bash
python -m icalendar_sync delete --calendar "Personal" --uid "event-uid"
```

## 4. 提交事件数据

创建事件时至少需要提供以下字段：
- `summary`（字符串）：事件摘要。
- `dtstart`（ISO 日期时间格式）：事件开始时间。
- `dtend`（ISO 日期时间格式）：事件结束时间，必须晚于 `dtstart`。

可选字段：
- `description`：事件描述。
- `location`：事件地点。
- `status`：事件状态。
- `priority`（0-9）：事件优先级。
- `alarms`：事件提醒设置。
- `rrule`：事件重复规则。

## 5. 安全规则

- 验证日历名称的合法性；拒绝包含路径信息的请求数据。
- 确保凭证信息不会被记录在日志或输出结果中。
- 尽量使用密钥链存储凭证，而非文件存储。
- 如果使用文件存储，请设置严格的文件权限（例如 `0600`）。

## 6. 错误处理

- 如果在 macOS 上 CalDAV 认证或网络连接失败，并且提供的提供者为 `auto` 或 `caldav`，则切换到 `macos-native` 模式并重试操作。
- 如果事件数据以文件路径的形式提供，在解析之前请确保文件大小在安全范围内。