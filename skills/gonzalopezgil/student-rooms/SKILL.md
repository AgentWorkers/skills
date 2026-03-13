---
name: student-rooms
description: 搜索、扫描并监控 Yugo 和 Aparto 提供方的学生住宿情况。当用户询问学生住房、房间可用性、学期住宿、预订选项或价格比较时，可使用该工具。该工具覆盖 Yugo（11 个国家，70 多个城市，包括英国、爱尔兰、西班牙、德国、法国、意大利、葡萄牙、奥地利、澳大利亚、美国、阿联酋）和 Aparto（爱尔兰、西班牙、意大利、英国、法国的 14 个城市）。支持按学期筛选、持续监控模式（带警报功能）、预订流程追踪以及多种通知方式（标准输出、Webhook、Telegram、OpenClaw）。该工具可以独立使用（无需 OpenClaw），同时也支持与 OpenClaw 的集成，以实现通知和代理模式下的警报功能。
---
# student-rooms CLI

这是一个多供应商的学生住宿查找和监控工具。它可以查询Yugo和Aparto平台的房间可用性，根据学期和价格进行筛选，并在新房源出现时发送警报。

## 设置

```bash
cd /path/to/student-rooms-cli
source .venv/bin/activate
```

配置文件：`config.yaml`（如果不存在，请从`config.sample.yaml`复制）。主要配置项包括：

```yaml
target:
  country: "Ireland"
  city: "Dublin"
academic_year:
  start_year: 2026
  end_year: 2027
filters:
  max_weekly_price: 350.0
notifications:
  type: "openclaw"  # or stdout | webhook | telegram
  openclaw:
    mode: "message"
    channel: "telegram"
    target: "CHAT_ID"
```

## 命令

所有命令都支持`--provider yugo|aparto|all`（默认值为`all`）以及`--json`选项，用于生成结构化输出。

### discover — 列出房源信息

```bash
python -m student_rooms discover --provider all
python -m student_rooms discover --provider all --json
python -m student_rooms discover --city Barcelona --provider aparto --json
```

返回目标城市的房源名称、地址、位置和URL。

### scan — 单次房源可用性检查

```bash
# Semester 1 rooms (default filter)
python -m student_rooms scan --provider all --json

# All options (full year, semester 2, etc.)
python -m student_rooms scan --all-options --json

# Scan + send notification for top match
python -m student_rooms scan --provider all --notify
```

JSON输出结构：
```json
{
  "matchCount": 5,
  "matches": [
    {
      "provider": "yugo",
      "property": "Residence Name",
      "roomType": "Gold Ensuite",
      "priceWeekly": 310.0,
      "priceLabel": "€310/week",
      "available": true,
      "bookingUrl": "https://...",
      "startDate": "2026-09-01",
      "endDate": "2027-01-31",
      "optionName": "Semester 1",
      "dedupKey": "yugo|slug|gold ensuite|2026-27|Semester 1"
    }
  ]
}
```

### watch — 持续监控

```bash
python -m student_rooms watch --provider all
```

按照配置的间隔（默认为1小时，加上随机延迟）进行扫描。仅对之前未出现的新房源发送警报。会保留已查看过的房源信息，以避免重复警报。

### probe-booking — 深入查询预订流程

```bash
python -m student_rooms probe-booking --provider yugo --residence "Dominick Place" --json
python -m student_rooms probe-booking --provider aparto --residence "Binary Hub" --json
```

返回预订相关信息、可用床位、直接预订链接以及门户网站的重定向URL。支持`--residence`、`--room`、`--tenancy`、`--index`等筛选条件。

### notify — 测试通知功能

```bash
python -m student_rooms notify --message "Test alert 🏠"
```

### test-match — 测试学期匹配逻辑

```bash
python -m student_rooms test-match --from-year 2026 --to-year 2027 --name "Semester 1" --start-date 2026-09-01 --end-date 2027-01-31 --json
```

## 地点覆盖

可以通过CLI参数覆盖配置中的目标地点：

```bash
python -m student_rooms scan --city Barcelona --country Spain --provider all --json
```

## 使用提示

- 建议始终使用`--json`选项以获得结构化输出。
- 使用`scan --json`命令检查当前房源可用性，并解析`matchCount`和`matches`数组。
- 使用`discover --json`命令在扫描前查看可用的房源信息。
- 将`watch`命令作为后台进程进行持续监控。
- 结合`scan --notify`命令在一个命令中触发警报。
- `scan`输出中的`dedupKey`字段用于唯一标识每个房源，便于追踪。

## 与OpenClaw的集成

在配置文件中设置`notifications.type: "openclaw"`。支持两种通知方式：
- **message**：通过`openclaw message send`将警报文本发送到指定频道或目标。
- **agent**：触发OpenClaw代理会话，并将警报信息作为上下文传递。

可选参数：`create_job_on_match: true`用于创建一次性的定时任务以协助预订。

该工具完全可以独立使用；只有在需要`openclaw`通知后端时才需要安装OpenClaw。

## 通知后端

| 后端 | 配置键 | 必需条件 |
|---------|-----------|----------|
| `stdout` | （默认） | 无 |
| `webhook` | `notifications.webhook.url` | 任何HTTP端点（如Discord、Slack、ntfy.sh） |
| `telegram` | `notifications.telegram_bot_token` + `chat_id` | Telegram机器人 |
| `openclaw` | `notifications.openclaw.target` | 已安装OpenClaw CLI |

## 提供商说明

- **Yugo**：通过动态API获取房源信息（国家 → 城市 → 住宿类型 → 房间 → 租赁选项）。支持完整的预订流程查询。
- **Aparto**：从apartostudent.com抓取房源信息，然后查询StarRez平台的房源详情。意大利/西班牙/意大利语地区使用同一个门户；英国使用单独的门户；法国不支持StarRez平台（仅支持房源查询）。