---
name: show-booking
description: 根据电子邮件或粘贴的房源信息来预订房产看房服务，具体包括提取房源数据、安排外拨电话任务、协调协助看房的代理人、创建日历邀请以及回复确认信息。此功能适用于用户请求预订一个或多个房产的看房服务时，或需要协调客户偏好的看房时间时；同时也可用于自动化办公电话流程，替代手动登录BrokerBay的操作。
---
# 显示预订信息

## 概述

执行一个端到端的工作流程来处理预订请求：
1. 从自由格式的提示或电子邮件文本中解析用户输入的信息。
2. 为每个房源生成相应的通话任务。
3. 将通话执行任务交给 `tour-booking` 子代理处理。
4. 根据确认的预约时间生成日历邀请文件。
5. 返回一个简洁的确认总结。

## 输入信息

在发起外拨电话之前，需要收集以下字段：
- 客户的全名。
- 房源信息（地址、房源 ID（如有）、办公室电话、办公室/代理名称（如有）。
- 客户偏好的时间窗口和时区。
- 预订限制（如特殊要求、入住人数、最低通知时间）。
- 确认通知的接收方式（电子邮件/SMS）。

如果某个房源缺少电话号码，请将其标记为“已阻止”，并不要为该房源发起通话。

## 工作流程

### 1) 解析用户输入

运行以下代码块：

```bash
python3 scripts/intake_request.py --input-file /path/to/intake.txt --output /tmp/showing-intake.json
```

或者直接传递文本输入：

```bash
python3 scripts/intake_request.py --input-text "Book showings for ..." --output /tmp/showing-intake.json
```

### 2) 构建通话队列

运行以下代码块：

```bash
python3 scripts/orchestrate_showings.py --intake /tmp/showing-intake.json --output /tmp/showing-plan.json
```

此步骤会生成以下结果：
- `call_queue`：包含已获取电话号码的房源列表。
- `blocked`：缺少必要信息的房源列表。
- `calendar_candidates`：待确认通话后用于生成邀请的房源记录。

### 3) 将通话任务委托给 `tour-booking`

对于 `call_queue` 中的每个房源，使用以下命令调用 `tour-booking/scripts/place_outbound_call.py`：
- 房源元数据。
- 客户信息。
- 回电说明。

如果未批准进行实际通话，请使用 `--dry-run` 选项运行该脚本，并返回生成的通话数据。

### 4) 为已确认的预约创建邀请

当房源确认了具体的时间后，执行以下操作：

```bash
python3 scripts/create_invite_ics.py \
  --input /tmp/confirmed-showings.json \
  --output-dir /tmp/showing-invites
```

脚本会为每个已确认的预约生成一个 `.ics` 文件。该文件可以导入到 Google 日历中，或者直接作为附件发送给客户。

### 5) 返回状态信息

报告以下内容：
- 已确认的预约信息（包括时间、地址和邀请文件路径）。
- 待处理的回电任务。
- 被标记为“已阻止”的房源及其缺失的信息。
- 尝试拨打的电话总数以及成功/失败的次数。

## 规范要求

- 明确说明呼叫方是代表经纪公司/房地产代理的人工智能助手。
- 遵守当地的电话营销和同意要求。
- 保留完整的审计记录：包括请求数据、通话结果、预订结果以及时间戳。
- 在通话结果明确表示预约已确认之前，切勿声称预约已经成功。