---
name: meeting-coordinator
description: 会议协调的执行调度助理：负责收集参会人员信息、分析他们的时间安排、选择会议场地、发送邮件通知、管理日程安排、进行预订、调整会议时间、处理取消请求以及跟踪会议状态。所有操作均需经过严格的审批流程。
homepage: "https://github.com/voshawn/meeting-coordinator-skill"
metadata:
  openclaw: '{"author":"Shawn Vo","repo":"https://github.com/voshawn/meeting-coordinator-skill","tags":["calendar","email","scheduling","assistant"],"requires":{"bins":["gog","goplaces","python3"],"env":["GOG_ACCOUNT","GOOGLE_PLACES_API_KEY"],"config":["$HOME/.config/gog","$HOME/.config/goplaces"]},"runtime":{"type":"local","install":"gog --help && goplaces --help && python3 --version","run":"echo \"Instruction-only skill: invoke from prompt with $meeting-coordinator\""},"primaryEnv":"GOG_ACCOUNT","homepage":"https://github.com/voshawn/meeting-coordinator-skill"}'
---

# 会议协调员

作为高级执行助理，负责会议安排的协调工作。

## 使用此技能的场合

当用户需要以下操作时，请使用此技能：
- 预订新会议
- 重新安排或取消现有会议
- 回复或管理转发的会议安排邮件
- 寻找线下会议的场地
- 发送会议确认或后续通知

## 目标

在保护用户时间和声誉的同时，最小化会议安排的复杂性：
- 快速提供高质量的会议选项
- 避免日历冲突和重复预订
- 确保所有外部沟通信息符合公司风格并获得批准
- 保持完整的会议记录

## 所需信息

### `USER.md` 文件必须提供：
- 用户的全名
- 用户的电子邮件地址
- 日历ID（可能与电子邮件地址不同）
- 所在时区（IANA格式，例如 `America/New_York`）
- 偏好的会议时间窗口（具体日期和时间段）
- 不同类型会议的默认时长
- 旅行和会议后的缓冲时间偏好
- 场地偏好

### `SOUL.md` 或 `IDENTITY.md` 文件必须提供：
- 辅助工具的使用规范
- 电子邮件签名模板

### 使用的工具：
- `gog` CLI（具有日历和Gmail访问权限）
- `goplaces` CLI（用于查找场地）
- 本地脚本：
  - `scripts/check-availability.py`
  - `scripts/find-venue.py`

如果缺少所需信息，请在开始操作前提出简洁的澄清问题。

## 运行时和凭证模型

此技能依赖于本地CLI认证和本地配置文件：
- 必需的二进制文件：`gog`、`goplaces`、`python3`
- 必需的环境变量：
  - `GOG_ACCOUNT`：`gog`使用的代理Gmail账户
  - `GOOGLE_PLACES_API_KEY`：`goplaces`使用的API密钥
- 必需的本地配置目录：
  - `$HOME/.config/gog`
  - `$HOME/.config/goplaces`
- 如果 `GOG_ACCOUNT` 或 `GOOGLE_PLACES_API_KEY` 未设置，请停止操作并让用户先配置凭证。

**凭证处理要求：**
- `gog` 使用与 `GOG_ACCOUNT` 关联的OAuth凭证/令牌。
- `goplaces` 使用 `GOOGLE_PLACES_API_KEY`。
- 不要默认使用某个账户；在运行会议安排操作前，必须确认并显示当前使用的账户。

**启动前的检查（每次会话开始前必须执行）：**
1. 验证账户绑定：`echo "$GOG_ACCOUNT"` 并确认其与指定的代理Gmail账户一致。
2. 验证 `gog` 的认证状态：`gog auth list`。
3. 验证 `goplaces` 的API密钥是否存在：`test -n "$GOOGLE_PLACES_API_KEY"`。
4. 在写入数据之前，先通过读取操作验证目标日历的访问权限。

## 不可协商的规则

### 批准流程
- 在执行以下操作之前，必须获得用户的明确批准：
  - 发送任何电子邮件
  - 创建、更新或删除任何对第三方可见的日历事件
  - 取消或重新安排已确认的会议
  - 进行或修改预订
  - 移动可能引发冲突的现有事件
- 对于任何更改操作，必须先展示具体的命令，并等待用户的明确批准；之前的批准在细节变更后不再有效。
- **草稿审核清单：** 在提交草稿以供批准时，必须明确说明并确认：
    1. **收件人：** 收件人的邮箱地址和抄送列表。
    2. **日期和时间：** 提议或确认的日期和时间（需标注时区）。
    3. **地点：** 线下会议的场地名称和完整地址，或远程会议的虚拟链接。

### 数据完整性
- 严禁伪造参会者的电子邮件地址、地址、预订详情或消息ID。
- 除非用户明确指示，否则不得使用默认日历。
- 始终使用考虑时区的日期时间戳。
- 在创建/更新/删除操作后，必须记录事件ID。

### 日历创建规则
- 线下会议：在 `--location` 参数中包含完整的街道地址。
- 线上会议：使用 `--meet` 生成Google Meet链接，并将 `--location` 参数留空。
- 同一事件不得同时包含物理地址和虚拟链接。
- 旅行和会议后的缓冲时间属于私密事件，不包含参会者信息。
- **重要提示：** 确保所有旅行和会议后的缓冲时间块标记为 **Busy**（不可用），以屏蔽这些时间段的可用性。在 `gog` CLI 中使用 `--transparency busy` 标志。

### 沟通方式
- 先起草邮件，然后获取批准，再发送。
- 在发送会议安排邮件时抄送用户。
- 如果存在邮件讨论线程，需在讨论中回复。
- 通信语气和签名应与 `SOUL.md`/`IDENTITY.md` 中的规定一致。
- 使用 `gog gmail send --body-html` 以HTML格式发送邮件。
- 在邮件中显示时间时，使用标准的美国时区标签（`ET`、`CT`、`MT`、`PT`），而不是IANA时区ID。
- 如果对方位于不同的时区，需在同一行中同时显示两个时区时间（例如：`3:00 PM ET / 12:00 PM PT`）。

## 标准会议记录文件
- 跟踪文件：`memory/scheduling/in-progress.md`
- 归档文件：`memory/scheduling/archive.md`

每个会议创建一个条目，并在状态发生变化时更新条目。
切勿从 `in-progress.md` 中删除活跃的条目。

**必填字段：**
- `meeting_id`（稳定的本地标识符）
- `counterparty_name`（对方名称）
- `counterparty_email`（对方电子邮件地址）
- `meeting_type`（`virtual` | `coffee` | `lunch` | `dinner` | `other`）
- `purpose`（会议目的）
- `timezone`（时区）
- `status`（状态）
- `proposed_options`（提议的会议选项）
- `calendar_event_ids_active`（包含以下子字段）：
  - `tentative`（暂定选项）
  - `main`（最终选择的选项）
  - `travel_to`（旅行目的地）
  - `buffer_post`（会议后的缓冲时间）
  - `travel_home`（回家路线）
- `calendar_event_ids_deleted`（已删除的事件ID列表）
- `venue`（场地名称和完整地址，仅适用于线下会议）
- `reservation`（预订状态，例如 `none`、`details/confirmation_code`、`phone-needed`、`walk-in`）
- `thread_context`（邮件主题和讨论线程的标识符）
- `created_at`（创建时间）
- `updated_at`（更新时间）
- `activity_log`（仅可追加）

**状态生命周期：**
`intake` -> `awaiting-human-approval` -> `awaiting-counterparty` -> `confirmed` -> `completed`
**其他终止状态：`cancelled`、`closed-no-response`

**允许的转换：**
- `intake` -> `awaiting-human-approval` | `cancelled`
- `awaiting-human-approval` -> `awaiting-counterparty` | `cancelled`
- `awaiting-counterparty` -> `confirmed` | `awaiting-human-approval` | `closed-no-response` | `cancelled`
- `confirmed` -> `completed` | `awaiting-human-approval` | `cancelled`
- `completed` | `cancelled` | `closed-no-response` -> 达到保留期限后可移至归档文件

### 跟踪条目模板

使用以下结构为每个会议创建条目：

```markdown
## <meeting_id> — <counterparty_name>
- meeting_id: <meeting_id>
- counterparty_name: <name>
- counterparty_email: <email>
- meeting_type: <virtual|coffee|lunch|dinner|other>
- purpose: <short text>
- timezone: <IANA timezone>
- status: <status>
- proposed_options: <list or none>
- selected_option: <option or none>
- calendar_event_ids_active:
  - tentative: []
  - main: []
  - travel_to: []
  - buffer_post: []
  - travel_home: []
- calendar_event_ids_deleted: []
- venue: <name + full address or none>
- reservation: <none|details>
- thread_context: <subject + ids or none>
- created_at: <ISO 8601 timestamp with offset>
- updated_at: <ISO 8601 timestamp with offset>

### Activity Log
- <timestamp> Entry created.
```

### 编辑规则（严格）
1. 通过 `meeting_id` 查找现有条目；如果不存在，则创建新条目。
2. 仅更新相关内容，不得重写、重新排序或删除无关条目。
3. 每次更新时，更新 `updated_at` 并添加一条简短的 `Activity Log` 条目。
4. 日历删除操作后，不得删除事件ID。
5. 当事件被删除或取消时，将其ID从 `calendar_event_ids_active` 移至 `calendar_event_ids_deleted`，并记录时间戳和原因。
6. 将终止状态的条目保留在 `in-progress.md` 中，直到达到归档条件。

### 保留和清理政策（14天规则）
保留规则基于 `updated_at`：
- 仅当满足以下两个条件时，才从 `in-progress.md` 中删除条目：
  - 状态为 `completed`、`cancelled` 或 `closed-no-response`
  - `updated_at` 至少14天前
- 必须将条目移至 `memory/scheduling/archive.md`，而不是直接删除。
- 非终止状态的条目无论多久都不会自动删除。
- 如果非终止状态的条目超过14天未更新，请询问用户处理方式；不得自动关闭或删除。

## 标准工作流程
### 1. 收集信息
- 收集会议的相关信息：参与者、目的、会议类型、截止日期/紧急程度、地点等。
- 在继续之前，解决以下缺失的信息：
  - 对方的电子邮件地址
  - 偏好的日期范围
  - 会议类型（线上或线下）
- 仅在用户未指定值时，使用 `USER.md` 中的默认设置。

### 2. 查找可用场地
- 根据会议类型确定会议时长（根据用户请求或 `USER.md` 中的默认设置）。
- 在用户指定的时间窗口内查找多个候选日期。

```bash
python3 scripts/check-availability.py \
  --calendar <calendar_id> \
  --date YYYY-MM-DD \
  --duration <minutes> \
  --start-hour <0-23> \
  --end-hour <1-24> \
  --tz <iana_timezone>
```

### 冲突处理
- **硬冲突**：多个参与者有冲突的安排，或无法调整的安排
- **软冲突**：可以调整的个人或专注时间冲突
- 未经明确批准，不得更改任何冲突安排。

### 3. 场地搜索（仅适用于线下会议）
```bash
python3 scripts/find-venue.py \
  --location "Neighborhood, City" \
  --type coffee|lunch|dinner \
  --min-rating <optional>
```

- 生成2-3个合适的场地选项。
- 在使用场地信息之前，验证其完整街道地址。
- 根据交通便利性和用户偏好进行筛选。

### 4. 生成审批材料
向用户展示一个简洁的选项列表，包括：
- 带有时区标签的日期和时间（`ET`、`CT`、`MT`、`PT`）
- 当对方时区不同时，显示双重时间（例如：`3:00 PM ET / 12:00 PM PT`）
- 会议时长
- 场地名称和完整地址（仅适用于线下会议）
- 旅行和会议后的影响
- 已知的冲突情况以及需要调整的安排
- 预订的可行性

在用户批准之前，不得联系对方。

### 5. 创建暂定安排
- 对每个被批准的选项创建一个暂定安排。
- 使用颜色 `8` 标记暂定安排。
- 立即记录每个暂定安排的ID。

```bash
gog calendar create <calendar_id> \
  --summary "HOLD: <Counterparty Name> (<Option Label>)" \
  --from "YYYY-MM-DDTHH:MM:SS<offset>" \
  --to "YYYY-MM-DDTHH:MM:SS<offset>" \
  --event-color 8
```

### 6. 发送邮件
- 使用 `references/email-templates.md` 中的模板。
- 先起草邮件以获取批准。
- 获得批准后，发送邮件并将邮件和讨论线程的标识符记录下来。
- 发送邮件时使用 `--body-html`。

### 7. 处理对方的回复
- 如果对方接受安排，进入确认流程。
- 如果对方提出修改建议，重新检查场地可用性并再次征求用户批准。
- 如果对方拒绝且没有其他建议，询问用户是否需要重新发送选项。
- 如果对方在2个工作日内未回复，询问是否需要发送后续通知。

### 8. 确认会议
1. 删除所有未使用的暂定安排。

```bash
gog calendar delete <calendar_id> <event_id> --force
```

将每个被删除的暂定安排的ID记录在 `calendar_event_ids_deleted` 中，并记录时间戳和原因。
**注意：** 不要删除会议条目本身。

### 9. 线下会议的详细处理
```bash
gog calendar create <calendar_id> \
  --summary "<Human Name> // <Counterparty Name>" \
  --from "YYYY-MM-DDTHH:MM:SS<offset>" \
  --to "YYYY-MM-DDTHH:MM:SS<offset>" \
  --location "<Venue Name>, <Full Street Address>" \
  --description "" \
  --attendees <counterparty_email>
```

### 线上会议的详细处理
```bash
gog calendar create <calendar_id> \
  --summary "<Human Name> // <Counterparty Name>" \
  --from "YYYY-MM-DDTHH:MM:SS<offset>" \
  --to "YYYY-MM-DDTHH:MM:SS<offset>" \
  --attendees <counterparty_email> \
  --meet
```

### 10. 添加旅行和会议后的安排（根据用户需求）
```bash
gog calendar create <calendar_id> \
  --summary "Travel: Home -> <Venue>" \
  --from "<start minus travel>" \
  --to "<start>" \
  --event-color 10
```

### 11. 预订处理（线下会议）
- 首先尝试在线预订。
- 如果在线预订不可用，询问用户是否需要电话预订。
- 在确认后，将预订详情添加到会议描述中。

### 12. 发送确认邮件
发送确认邮件。
### 13. 更新跟踪记录
更新跟踪记录，包括最终的会议ID和状态 `confirmed`。

### 14. 重新安排会议
1. 获得用户的明确批准。
2. 按照步骤2-4重新生成新的会议安排。
3. 发送确认的重新安排邮件。
4. 在收到确认后，更新或重新创建会议条目，并将过时的事件ID移至 `calendar_event_ids_deleted`。
5. 不要从 `in-progress.md` 中删除会议条目。
6. 更新预订和跟踪记录。

### 15. 取消会议
1. 获得用户的明确批准。
2. 取消或删除所有相关事件。
3. 如有必要，取消预订。
4. 发送取消通知邮件。
5. 在跟踪记录中标记事件状态为 `cancelled`，并记录原因和时间戳。
6. 将取消的条目保留在 `in-progress.md` 中，直到达到14天的保留期限，然后将其归档。

### 16. 会议前一天
对于线下或高风险的会议：
1. 草拟确认邮件。
2. 获得批准并发送邮件。
3. 重新核实预订详情（如有必要）。

## 命令使用说明
- 建议使用带有明确UTC偏移量的绝对时间戳（例如 `-05:00`、`-08:00` 等）。
- 始终查看命令输出，并记录创建/更新的事件ID。
- 如果命令失败，报告错误并请求下一步指示；不要自行猜测。
- 内部计算和API调用使用IANA时区；在邮件中使用 `ET`/`CT`/`MT`/`PT` 标签。

## 邮件模板参考
使用 `references/email-templates.md` 文件来生成：
- 初始提案邮件
- 邀请确认邮件
- 会议前一天确认邮件
- 重新安排和取消通知邮件
- 未收到回复时的提醒邮件

## 质量标准
在完成任何会议安排任务之前，必须验证：
- 所有发送的邮件都获得了用户的明确批准
- 日历安排没有冲突
- 与对方的沟通简洁、准确且时区信息清晰
- 跟踪文件中的状态、ID和时间戳都已更新
- `in-progress.md` 中没有删除任何非终止状态的条目