---
name: nextcloud-aio-oc (NextCloud AIO OpenClaw)
description: 可靠的 Nextcloud 集成功能，支持笔记、任务、日历、文件和联系人的管理；同时具备 CardDAV 标准的 vCard 处理能力，并支持强大的联系人创建/更新功能。
license: MIT
compatibility: Requires Node.js 20+. Needs network access to Nextcloud instance.
required-binaries:
  - node>=20
required-env-vars:
  - NEXTCLOUD_URL
  - NEXTCLOUD_USER
  - NEXTCLOUD_TOKEN
optional-env-vars:
  - NEXTCLOUD_TIMEZONE
requiredBinaries:
  - node
requiredEnv:
  - NEXTCLOUD_URL
  - NEXTCLOUD_USER
  - NEXTCLOUD_TOKEN
optionalEnv:
  - NEXTCLOUD_TIMEZONE
primaryEnv: NEXTCLOUD_TOKEN
allowed-tools: Bash Read
---
# NextCloud AIO OpenClaw 技能

该技能将 OpenClaw 与 Nextcloud 连接，以支持以下功能：
- Notes API
- CalDAV 任务和事件
- WebDAV 文件
- CardDAV 联系人信息

主要目标：实现稳定、可靠的 Nextcloud 读写操作。

该技能已在以下版本上通过验证：
- Nextcloud Hub 25 Autumn (`32.0.6`)
- OpenClaw (`2026.3.2`)

## 必需配置

设置以下环境变量：
- `NEXTCLOUD_URL`（示例：`https://cloud.example.com`）
- `NEXTCLOUD_USER`
- `NEXTCLOUD_TOKEN`（强烈建议使用应用专用密码）
- `NEXTCLOUD_TIMEZONE`（推荐使用 IANA 时区，例如 `America/Los_Angeles`；用于处理不带时区的日期/时间输入）

## 运行时和元数据契约

本节是确保注册表元数据一致性的关键依据。

- 必需的二进制文件：`node`（Node.js 20+）
- 必需的环境变量：`NEXTCLOUD_URL`、`NEXTCLOUD_USER`、`NEXTCLOUD_TOKEN`
- 可选的环境变量：`NEXTCLOUD_TIMEZONE`
- 必需的网络目标：由 `NEXTCLOUD_URL` 定义的主机（以及该主机的常规重定向路径）

如果注册表条目显示“无需二进制文件”或“无需环境变量”，请将其视为过时的元数据，并在发布前进行修复。

## 预执行审计

在任何新环境中首次运行之前，请完成以下脚本审查流程：
- 确认没有意外的端点或特权系统调用。
- 如果检查不完整，请勿运行该技能。
- 建议优先使用沙箱/容器环境进行验证，并使用最低权限的应用程序凭据。

## 安全性和发布安全

- 请勿在 `SKILL.md`、脚本、示例代码、提交信息或变更日志中硬编码凭据。
- 仅将敏感信息存储在环境变量或本地秘密存储中。
- 为集成使用专用应用密码；如果密码泄露或共享，请及时更新。
- 将本地 `.env` 文件排除在 Git 仓库之外（参见 `.gitignore` 文件）。
- 在发布前，快速扫描文件中是否存在敏感信息，并删除任何意外出现的敏感内容。

## 打包脚本审查清单（首次使用前）

该技能包含名为 `scripts/nextcloud.js` 的可执行 JavaScript 文件。在新环境中运行之前，请执行以下审查：
1. 确认运行时要求：
   - `node --version`（必须为 Node.js 20+）
2. 检查明显的出站端点：
   - `rg -n "https?://" scripts/nextcloud.js`
3. 检查敏感功能的使用情况：
   - `rg -n "child_process|spawn\\(|exec\\(|require\\(\"fs\"\\)|require\\('fs'\\)|fs\\." scripts/nextcloud.js`
4. 确认凭据仅通过环境变量传递：
   - `rg -n "NEXTCLOUD_URL|NEXTCLOUD_USER|NEXTCLOUD_TOKEN|NEXTCLOUD_TIMEZONE" scripts/nextcloud.js`
5. 先以低权限模式运行：
   - 使用专用的 Nextcloud 应用程序密码
   - 尽可能在非生产数据上测试

如果审查结果不令人满意，请在代码得到可信维护者的审核之前不要运行该技能。

### 静态审计快照（当前版本）

对 `scripts/nextcloud.js` 进行快速 grep 类型的检查，应确认以下内容：
- 配置信息从 `process.env.NEXTCLOUD_URL|USER|TOKEN|TIMEZONE` 中读取。
- 请求路径格式为 `${CONFIG.url}${endpoint}`，并使用 `fetch()` 方法发送请求。
- 包裹代码中未发现明显的 `child_process` 或 `fs` 操作。

这并非全面的安全审计。每次更新包后都需要重新执行这些检查。

## 运行

```bash
node scripts/nextcloud.js <command> <subcommand> [options]
```

## 命令

### Notes（笔记）
- `notes list`  
- `notes get --id <id>`  
- `notes create --title <title> --content <content> [--category <category>]`  
- `notes edit --id <id> [--title <title>] [--content <content>] [--category <category>]`  
- `notes delete --id <id>`

### Tasks（任务）
- `tasks list [--calendar <calendar-name>]`  
- `tasks create --title <title> --calendar <calendar-name> [--due <iso>] [--priority <0-9>] [--description <text>] [--timezone <IANA>]`  
- `tasks edit --uid <uid> [--calendar <calendar-name> [--title <title>] [--due <iso>] [--priority <0-9>] [--description <text>] [--timezone <IANA>]`  
- `tasks delete --uid <uid> [--calendar <calendar-name>]`  
- `tasks complete --uid <uid> [--calendar <calendar-name>]`

### Calendar Events（日历事件）
- `calendar list [--from <iso>] [--to <iso>]`（默认：未来 7 天）  
- `calendar create --summary <summary> --start <iso-or-date> --end <iso-or-date> [--calendar <calendar-name>] [--description <text>] [--timezone <IANA>] [--all-day]`  
- `calendar edit --uid <uid> [--calendar <calendar-name> [--summary <summary>] [--start <iso-or-date> --end <iso-or-date>] [--description <text>] [--timezone <IANA>] [--all-day]`  
- `calendar delete --uid <uid> [--calendar <calendar-name>]`

**注意**：
- 在许多配置中，`Contact birthdays` 被视为事件日历，但仅支持读取操作。
- 生日信息必须通过 `contacts create/edit --birthday ...` 进行管理，而不能通过 `calendar create/edit` 来修改。
- `calendar list` 会返回事件的 `summary`、`start`、`end` 等信息，有时还会包含 `location` 和 `description`。

### Calendar Discovery（日历发现）
- `calendars list [--type <tasks|events>]`

### Files（文件）
- `files list [--path <path>]`  
- `files search --query <query>`  
- `files get --path <path>`  
- `files upload --path <path> --content <content>`  
- `files delete --path <path>`

### Contacts（联系人）
- `contacts list [--addressbook <name>]`  
- `contacts get --uid <uid> [--addressbook <name>]`  
- `contacts search --query <query> [--addressbook <name>]`  
- `contacts create [--name <full-name>] [--first-name <given>] [--last-name <family>] [--middle-name <middle>] [--prefix <prefix>] [--suffix <suffix>] [--addressbook <name>] [--email <single>] [--emails <csv>] [--phone <single>] [--phones <csv>] [--organization <org>] [--title <title>] [--note <note>] [--birthday <YYYY-MM-DD|YYYYMMDD|--MM-DD|--MMDD>]`  
- `contacts edit --uid <uid> [--addressbook <name>] [--name <full-name>] [--first-name <given>] [--last-name <family>] [--middle-name <middle>] [--prefix <prefix>] [--suffix <suffix>] [--email <single>] [--emails <csv>] [--phone <single>] [--phones <csv>] [--organization <org>] [--title <title>] [--note <note>] [--birthday <YYYY-MM-DD|YYYYMMDD|--MM-DD>]`  
- `contacts delete --uid <uid> [--addressbook <name>]`

### Address Book Discovery（地址簿发现）

## 联系人数据契约（重要）

使用 `fullName` 和 `structuredName` 作为标准名称字段。

联系人输出信息包括：
- `uid`
- `addressBook`
- `fullName`
- `structuredName`（包含：
  - `familyName`
  - `givenName`
  - `additionalNames`
  - `honorificPrefixes`
  - `honorificSuffixes`
- `nameRaw`（仅用于诊断；默认不显示给用户）
- `emails` 数组或 `null`
- `phones` 数组或 `null`
- `organization`, `title`, `note`
- `birthday`（格式化为 `YYYY-MM-DD` 或 `--MM-DD` 以便阅读）
- `birthdayRaw`（原始的 CardDAV 格式）

## 可靠性规则（快速参考）

在每次写入操作时，请遵循以下规则以防止数据损坏和混淆：
1. **身份和命名**：
   - 从不从 URL 中推断 `UID`；始终使用 `payload` 中提供的 `uid`。
   - 对用户显示的名称使用 `fullName` 和 `structuredName`；`nameRaw` 仅用于诊断目的。
2. **联系人和生日信息的完整性**：
   - 生日输入格式：`YYYY-MM-DD`、`YYYYMMDD`、`--MM-DD`、`--MM-DD`。
   - 不要在 `BDAY` 后添加分号。
   - 生日信息应通过 `contacts create/edit --birthday ...` 进行管理；切勿直接修改日历条目中的生日信息。
3. **保持意图的一致性**：
   - 仅修改用户明确请求的字段。
   - 要清除某个字段，请传递空值。
   - 尊重用户指定的 `--addressbook`；否则使用默认值或询问用户。
4. **日历和任务的验证**：
   - 在发送数据前验证日期/时间格式；对于定时事件，确保 `end > start`。
   - 对 ICS 文本字段（如 `SUMMARY`、`DESCRIPTION`）进行转义处理。
   - 验证任务的优先级范围（`0..9`）。
   - 对于不带时区的日期时间输入，使用 `--timezone` 或 `NEXTCLOUD_TIMEZONE`。
   - 对于全天事件，使用 `VALUE=DATE` 的格式。
5. **功能和安全性检查**：
   - 不要假设列出的日历都可以写入。
   - 将 `Contact birthdays` 视为只读/系统日历。
   - 如果不存在可写的日历，应说明无法修改相关事件。
   - 有些日历包含多个组件（`VEVENT` 和 `VTODO`），请确保它们同时支持事件和任务操作。
6. **文件操作的验证**：
   - 对于 `files upload/get/delete` 操作，要求提供非空的文件路径。
   - 对 CardDAV/WebDAV 操作中的 XML 过滤/搜索值进行转义处理。
   - 在执行创建、编辑、完成或删除操作后，通过后续的读取/列表操作进行验证。
   - 如果操作失败，尝试在 0.5 秒、1 秒、2 秒后重新尝试。

## Nextcloud/CardDAV 的已知行为

- 服务器/客户端可能在写入/读取时协商或规范化 vCard 版本（`3.0` 对 `4.0`）和内容。
- 在有效的联系人信息中，`FN` 和 `N` 字段都必须出现。
- `BDAY` 的错误通常是由于输入格式不正确（例如分隔符错误）导致的，而非服务器不稳定。
- 折叠的 vCard 行在解析前需要展开。

## 错误处理映射（快速参考）

- `HTTP 403`（在 `calendar create/edit/delete` 操作中）：可能是日历只读或权限问题；切换到可写的事件日历。
- `HTTP 501`（在 `files search` 操作中）：WebDAV `SEARCH` 不受支持；回退到递归的 `PROPFIND` 和客户端过滤。
- `HTTP 415`（在任务/事件更新操作中）：ICS 格式错误；规范化格式后重新尝试。
- 联系人信息写入成功但 UI 仍未更新：在报告错误前先尝试重新验证。

## 代理行为：默认日历选择

当用户创建任务/事件时，如果没有指定日历：
1. 运行 `calendars list --type tasks` 或 `calendars list --type events`。
2. 过滤掉可能只读的日历（如 `Contact birthdays`、`Holidays`、包含 `read only` 或 `readonly` 的日历）。
3. 如果至少存在一个可写的日历，询问用户是否要选择该日历。
4. 将选定的日历存储在内存中。
5. 如果没有可写的事件日历，说明无法修改事件，并建议用户在 Nextcloud 日历中创建可写的日历。

内存键：
- `default_task_calendar`
- `default_event_calendar`

## 代理行为：默认地址簿选择

当用户创建联系人时，如果没有指定地址簿：
1. 运行 `addressbooks list`。
2. 询问用户是否要选择地址簿。
3. 将选定的地址簿存储在内存中。

内存键：
- `default_addressbook`

## 代理行为规则（简要说明）

这些规则是执行操作的快捷方式。上述的可靠性和安全性规则仍然适用。

### Contacts（联系人）和 Birthdays（生日）

1. 确定使用的地址簿（`--addressbook` 或内存中保存的默认值）。
2. 在创建/编辑联系人信息时，仅传递用户请求的字段；如果用户希望清除某些字段，使用空值。
3. 使用 `--name` 传递全名；对于包含多个名称的情况，使用 `structuredName` 格式。
4. 将多个电子邮件/电话号码以 CSV 格式传递。
5. 生日信息的修改始终通过 `contacts create/edit --birthday ...` 进行，切勿通过日历操作进行。

### Tasks（任务）

1. 在创建任务时确定使用的日历。
2. 在写入之前验证任务的开始时间和优先级（`0..9`）。
3. 在创建/编辑/完成/删除操作后，通过列表/获取功能进行验证。

### Calendar Events（日历事件）

1. 确定可写的日历；将 `Contact birthdays` 和系统日历视为只读。
2. 验证事件的开始时间和结束时间；确保 `end > start`。
3. 对于不带时区的日期时间，使用 `--timezone` 或 `NEXTCLOUD_TIMEZONE`。
4. 对于全天事件，使用 `--all-day` 格式。

### Appointment Briefing 工作流程（高优先级）

当用户询问约会详情或“今天的约会是什么”时：
1. 根据 `NEXTCLOUD_TIMEZONE` 确定“今天”的时间范围。
2. 运行 `calendar list --from <start-of-day-iso> --to <end-of-day-iso>`。
3. 根据用户输入的关键词（如 `dermatology`、`doctor`、`provider name`）筛选事件。
4. 对于选中的事件，显示事件的摘要、时间范围、地点和描述。
5. 如果有多个匹配项，询问用户是否需要进一步确认。
6. 如果没有匹配项，明确告知用户今天没有找到结果，并建议用户明天或下一周查看。
7. 提供适合短信/聊天的简洁文本信息。

### Files（文件）

1. 对于文件操作，需要提供明确的文件路径。
2. 使用固定的测试路径进行临时文件验证。
3. 读取上传后的文件内容，然后删除临时文件。
4. 对于大量文件，先进行基于路径的筛选，以减少负载。

### Notes（笔记）

1. 创建笔记时需要提供明确的标题和内容。
2. 创建/编辑后，根据 ID 读取笔记内容。
3. 验证完成后删除临时笔记文件。

## 内部测试协议

在实时环境中验证该技能时：
1. 对联系人信息进行创建、获取、编辑、再次获取（可选删除）操作。
2. 对笔记进行创建、获取、编辑、再次获取、删除操作。
3. 对文件进行上传、获取、搜索、列表、删除操作。
4. 对任务进行创建、列表/定位、编辑、完成、删除操作。

在所有测试数据上添加唯一的时间戳后缀，并在用户未要求保留的情况下删除所有临时文件。
测试时使用最低权限的凭据，并监控输出流量；过程仅与 `NEXTCLOUD_URL` 通信。

### 日历异常处理

- 如果不存在可写的日历，将日历修改操作标记为故意跳过（环境限制），但仍执行 `calendar list` 操作。
- 不要将此视为技能失败，而是视为服务器功能/权限限制。

## 持久性规则（请记住这些规则）

以下规则需要长期应用：
1. 生日信息属于联系人字段：使用 `contacts create/edit --birthday ...` 进行操作；切勿直接修改 `Contact birthdays`。
2. 对于全天事件，始终使用 `calendar create/edit --all-day` 和日期格式（避免使用包含时间范围的格式）。
3. 对于不带时区的日期时间，使用 `--timezone` 或 `NEXTCLOUD_TIMEZONE`；如果时区未知，请询问用户。
4. 对于可写的事件，优先使用用户指定的日历；如果遇到 403 错误，可能是权限问题。
5. 在确认最终结果之前，通过读取/列表操作验证事件/联系人的修改情况。
6. 保持全天事件的正确编码格式（`VALUE=DATE`）；除非用户明确要求，否则避免创建重复的事件。

## 故障排除指南

- 如果生日信息已更新，但在 Nextcloud UI 中仍未显示：
  - 立即运行 `contacts get --uid ...`。
  - 如果 API 中的信息正确，建议稍等片刻后再刷新 UI。
  - 在重试一段时间后再次检查。

- `contacts get` 和 `contacts search` 的结果暂时不一致：
  - 优先尝试重新验证，然后信任最新的结果。
- 如果创建联系人信息时持续失败：
  - 运行 `calendars list --type events`，确认是否存在至少一个可写的非系统日历。
  - 如果只有生日/系统日历，说明存在限制，并停止修改操作。

## 输出格式

所有命令返回 JSON 格式的结果：
- 成功：```json
{
  "status": "success",
  "data": {}
}
```
- 错误：```json
{
  "status": "error",
  "message": "Error description"
}
```