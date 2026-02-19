---
name: meeting-coordinator
description: 会议协调的执行调度助理（负责处理电子邮件、日程安排、场地选择及与会确认等工作）。
metadata:
  openclaw:
    emoji: "📅"
    requires:
      bins:
        - gog
        - goplaces
        - python3
      env:
        - GOG_ACCOUNT
        - GOOGLE_PLACES_API_KEY
    primaryEnv: GOG_ACCOUNT
    homepage: https://github.com/voshawn/meeting-coordinator-skill
---
# 会议协调员

作为高精度的执行助理，负责会议安排工作。

## 适用场景

当用户需要以下操作时，请使用此技能：
- 预订新会议
- 重新安排或取消现有会议
- 回复或管理转发的会议安排邮件
- 寻找线下会议的场地
- 发送会议确认邮件或后续通知

## 目标

在保护用户时间和声誉的同时，最小化会议安排的复杂性：
- 快速提供高质量的会议选项
- 避免日历冲突和重复预订
- 确保所有外部沟通信息符合公司风格并获得批准
- 保持完整的会议记录

## 所需信息

### `USER.md` 必须提供：
- 用户的全名
- 用户的电子邮件地址
- 日历ID（可能与电子邮件地址不同）
- 所在时区（IANA格式，例如 `America/New_York`）
- 偏好的会议时间窗口（日期和小时）
- 不同类型会议的默认时长
- 会议期间的出行和缓冲时间偏好
- 场地偏好

### `SOUL.md` 或 `IDENTITY.md` 必须提供：
- 辅助工具的使用规范
- 电子邮件签名模板

### 使用的工具：
- `gog` CLI（具备日历和Gmail访问权限）
- `goplaces` CLI（用于查找场地）
- 本地脚本：
  - `scripts/check-availability.py`
  - `scripts/find-venue.py`

如果缺少所需信息，请在开始操作前提出简洁的澄清问题。

## 运行时和凭证模型

此技能依赖于本地CLI认证和配置文件：
- 必需的二进制文件：`gog`, `goplaces`, `python3`
- 必需的环境变量：
  - `GOG_ACCOUNT`：`gog`使用的代理Gmail账户
  - `GOOGLE_PLACES_API_KEY`：`goplaces`使用的API密钥
- 必需的本地配置目录：
  - `$HOME/.config/gog`
  - `$HOME/.config/goplaces`
- 如果 `GOG_ACCOUNT` 或 `GOOGLE_PLACES_API_KEY` 未设置，请停止操作并请求用户配置凭证。

**凭证处理要求：**
- `gog` 使用与 `GOG_ACCOUNT` 关联的OAuth凭证/令牌。
- `goplaces` 使用 `GOOGLE_PLACES_API_KEY`。
- 不要默认使用任何账户；在运行安排操作前必须确认当前使用的账户。

**操作前的检查（每次会话开始前必须执行）：**
1. 验证账户绑定：`echo "$GOG_ACCOUNT"` 并确认其与代理Gmail账户一致。
2. 验证 `gog` 的认证状态：`gog auth list`。
3. 验证 `goplaces` 的API密钥是否存在：`test -n "$GOOGLE_PLACES_API_KEY"`。
4. 在写入数据之前，先通过读取操作验证目标日历的访问权限。

## 不可协商的规则：
- 在执行以下操作之前，必须获得用户的明确批准：
  - 发送任何邮件
  - 创建、更新或删除任何对第三方可见的日历事件
  - 取消或重新安排已确认的会议
  - 进行或修改预订
  - 移动可能引发冲突的现有事件
- 对于任何修改操作，先展示具体的命令，然后等待用户的明确批准；如果细节发生变化，之前的批准将失效。
- **草稿审核清单：** 在提交草稿请求批准时，必须明确说明并确认：
    1. **收件人：** 收件人名单（To: 和 CC: 列）
    2. **日期和时间：** 提议或确认的日期和时间（明确标注时区）
    3. **地点：** 线下会议的场地名称和完整地址，或远程会议的链接

## 数据完整性要求：
- 严禁伪造参会者的电子邮件地址、地址、预订详情或消息ID。
- 除非用户明确指示，否则不得使用默认日历。
- 始终使用考虑时区的时间戳。
- 在创建/更新/删除操作后，必须记录事件ID。

## 日历创建规则：
- 线下会议：在 `--location` 参数中包含完整的街道地址。
- 线上会议：使用 `--meet` 生成Google Meet链接，并将 `--location` 参数留空。
- 同一事件不得同时包含物理地址和虚拟链接。
- 旅行和缓冲时间段的事件为私密事件，不包含参会者信息。
- **重要提示：** 确保所有旅行和缓冲时间段标记为 **Busy**（不可用），以屏蔽这些时间段。在 `gog` CLI 中使用 `--transparency busy` 标志。

## 沟通方式：
- 先起草邮件，然后获取批准，再发送。
- 在发送会议安排邮件时抄送用户。
- 如果存在邮件讨论线程，请在讨论中回复。
- 保持与 `SOUL.md`/`IDENTITY.md` 中规定的语气和签名一致。
- 使用 `gog gmail send --body-html` 以HTML格式发送邮件。
- 在邮件中显示时间时区时，使用标准的美国时间标签（`ET`, `CT`, `MT`, `PT`），而不是IANA时区ID。
- 如果对方位于不同的时区，需在同一行显示两个时间（例如：`3:00 PM ET / 12:00 PM PT`）。

## 标准会议记录文件：
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
- `calendar_event_ids_active`（当前活动的日历事件ID列表）：
  - `tentative`（暂定的）
  - `main`（最终选择的）
  - `travel_to`（出行目的地）
  - `buffer_post`（缓冲时间）
  - `travel_home`（回家路线）
- `calendar_event_ids_deleted`（已删除的日历事件ID列表）
- `venue`（场地名称和完整地址，适用于线下会议）
- `reservation`（预订状态，例如 `none` | `details/confirmation_code` | `phone-needed` | `walk-in`）
- `thread_context`（邮件主题和讨论线程ID）
- `created_at`（创建时间）
- `updated_at`（更新时间）
- `activity_log`（仅用于追加）

**状态生命周期：**
`intake` -> `awaiting-human-approval` -> `awaiting-counterparty` -> `confirmed` -> `completed`
**其他终端状态：`cancelled`, `closed-no-response`

**允许的转换：**
- `intake` -> `awaiting-human-approval` | `cancelled`
- `awaiting-human-approval` -> `awaiting-counterparty` | `cancelled`
- `awaiting-counterparty` -> `confirmed` | `awaiting-human-approval` | `closed-no-response` | `cancelled`
- `confirmed` -> `completed` | `awaiting-human-approval` | `cancelled`
- `completed` | `cancelled` | `closed-no-response` -> 达到保留期限后可归档

**条目模板：**
使用以下结构来记录每个会议：

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

### 编辑规则（严格遵循）：
1. 通过 `meeting_id` 查找现有条目；如果不存在，则创建新条目。
2. 仅更新相关内容，不得重写、重新排序或删除无关条目。
3. 每次更新时，更新 `updated_at` 并添加一行 `Activity Log`。
4. 日历删除后，不得删除事件ID。
5. 当事件被删除或取消时，将其ID从 `calendar_event_ids_active` 移至 `calendar_event_ids_deleted`，并记录时间戳和原因。
6. 在 `in-progress.md` 中保留终端状态下的条目，直到达到归档条件。

**保留和清理政策（14天规则）：**
保留规则基于 `updated_at`：
- 仅当满足以下两个条件时，才从 `in-progress.md` 中删除条目：
  - 状态为 `completed` | `cancelled` | `closed-no-response`
  - `updated_at` 至少14天前
- 必须将条目移动到 `memory/scheduling/archive.md`，而不是直接删除。
- 非终端状态的条目无论时间多久都不会自动删除。
- 如果非终端状态的条目超过14天未更新，请询问用户处理方式；不要自动关闭或删除。

**标准工作流程：**
1. **信息收集：**
  - 收集会议参与者、目的、会议类型、截止日期/紧急性、地点等相关信息。
  - 在继续之前，确认以下信息是否缺失：
    - 对方电子邮件地址
    - 偏好的日期范围
    - 会议类型（线上或线下）
  - 仅当用户未指定时，才使用 `USER.md` 中的默认值。

2. **场地搜索：**
  - 根据会议类型确定会议时长（根据请求或 `USER.md` 中的默认值）。
  - 在指定的时间窗口内检查多个候选日期。

```bash
python3 scripts/check-availability.py \
  --calendar <calendar_id> \
  --date YYYY-MM-DD \
  --duration <minutes> \
  --start-hour <0-23> \
  --end-hour <1-24> \
  --tz <iana_timezone>
```

3. **冲突处理：**
  - **硬冲突**：多个参会者的承诺或不可更改的承诺
  **软冲突**：可以调整的个人或工作安排
  - 未经明确批准，不得调整冲突时间。

4. **场地搜索（仅适用于线下会议）：**
```bash
python3 scripts/find-venue.py \
  --location "Neighborhood, City" \
  --type coffee|lunch|dinner \
  --min-rating <optional>
```

- 生成2-3个合适的场地选项。
- 在使用场地信息之前，验证其完整地址。
- 根据交通便利性和用户偏好进行筛选。

5. **生成审批材料：**
  - 提供一个简洁的选项列表，包括：
    - 带有时区标签的日期和时间（`ET`, `CT`, `MT`, `PT`）
    - 当对方时区不同时，显示双重时间（例如：`3:00 PM ET / 12:00 PM PT`）
    - 会议时长
    - 场地名称和完整地址（适用于线下会议）
    - 旅行和缓冲时间的影响
    - 已知的冲突情况以及需要调整的事项
  - 在用户批准之前，不得联系对方。

6. **创建暂定安排：**
  - 为每个被批准的选项创建一个暂定安排。
  - 使用颜色 `8` 标记暂定安排。
  - 立即记录每个暂定安排的ID。

```bash
gog calendar create <calendar_id> \
  --summary "HOLD: <Counterparty Name> (<Option Label>)" \
  --from "YYYY-MM-DDTHH:MM:SS<offset>" \
  --to "YYYY-MM-DDTHH:MM:SS<offset>" \
  --event-color 8
```

7. **发送邮件：**
  - 使用 `references/email-templates.md` 中的模板。
  - 先起草邮件请求批准。
  - 获得批准后，发送邮件并将邮件和线程ID记录在跟踪文件中。
  - 发送邮件时使用 `--body-html`。

8. **处理对方回复：**
  - 如果对方接受安排，进入确认流程。
  - 如果对方提出新的安排建议，重新检查场地可用性并再次征求用户批准。
  - 如果对方拒绝且没有其他建议，询问用户是否需要发送新的安排建议。
  - 如果对方在2个工作日内未回复，询问是否需要发送后续通知。

9. **确认会议：**
  - 删除未使用的暂定安排。

```bash
gog calendar delete <calendar_id> <event_id> --force
```

**记录删除的暂定安排：**
  - 在 `calendar_event_ids_deleted` 中记录每个被删除的暂定安排的ID、时间戳和原因。
  - 不要删除会议条目。
  - 创建最终的会议条目（适用于线下会议）。

10. **重新安排会议：**
    - 获取用户的明确批准。
    - 按照步骤2-4重新生成新的会议安排。
    - 发送确认邮件。
    - 确认后，更新或重新创建会议条目，并将过时的条目ID移至 `calendar_event_ids_deleted`。
    - 不要删除 `in-progress.md` 中的会议条目。
    - 更新预订信息和跟踪记录。

11. **取消会议：**
    - 获取用户的明确批准。
    - 取消或删除所有相关事件。
    - 如有必要，取消预订。
    - 发送取消邮件，并在跟踪记录中标记状态为 `cancelled` 和原因。
    - 将取消的条目保留在 `in-progress.md` 中，直到达到14天的保留期限，然后归档。

12. **会议前一天：**
    - 对于线下或高风险的会议，起草确认邮件。
    - 获取批准并发送邮件。
    - 重新核实预订详情（如有必要）。

**命令使用说明：**
- 建议使用带有明确UTC偏移量的绝对时间戳（例如 `-05:00`, `-08:00` 等）。
- 务必阅读命令输出并记录创建/更新的事件ID。
- 如果命令失败，报告错误并请求下一步指示；不要自行猜测。
- 内部计算和API调用使用IANA时区；在邮件中显示时区时使用 `ET`/`CT`/`MT`/`PT` 标签。

**邮件模板参考：**
使用 `references/email-templates.md` 来生成：
- 初始提案邮件
- 邀请确认邮件
- 会议前一天确认邮件
- 重新安排和取消邮件
- 未回复时的提醒邮件

**质量标准：**
在完成任何会议安排任务之前，务必验证：
- 每次发送邮件前都记录用户的批准信息
- 日历中没有冲突
- 与对方的沟通简洁、准确且时区信息清晰
- 跟踪文件中更新了状态、事件ID和时间戳
- `in-progress.md` 中没有删除非终端状态的条目