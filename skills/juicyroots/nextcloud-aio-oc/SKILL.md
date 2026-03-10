---
name: nextcloud-aio-oc (NextCloud AIO OpenClaw)
description: 可靠的 Nextcloud 集成功能，支持笔记、任务、日历、文件及联系人管理（支持 CardDAV 协议的 vCard 数据处理，并具备强大的联系人创建/更新功能）。
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

该技能将 OpenClaw 与 Nextcloud 连接起来，以实现以下功能：
- 访问 Notes API
- 管理 CalDAV 任务和事件
- 操作 WebDAV 文件
- 管理 CardDAV 联系人信息

主要目标：实现稳定、可靠的 Nextcloud 数据读写操作。

该技能已通过以下版本进行验证：
- Nextcloud Hub 25 Autumn (`32.0.6`)
- OpenClaw (`2026.3.2`)

## 必需配置

请设置以下环境变量：
- `NEXTCLOUD_URL`（示例：`https://cloud.example.com`）
- `NEXTCLOUD_USER`
- `NEXTCLOUD_TOKEN`（强烈建议使用应用专用密码）
- `NEXTCLOUD_TIMEZONE`（推荐使用 IANA 时区，例如 `America/Los_Angeles`；用于处理不带时区的日期/时间格式）

## 运行时和元数据规范

本节是确保注册表元数据一致性的关键依据：
- 必需的二进制文件：`node`（Node.js 20 及更高版本）
- 必需的环境变量：`NEXTCLOUD_URL`、`NEXTCLOUD_USER`、`NEXTCLOUD_TOKEN`
- 可选的环境变量：`NEXTCLOUD_TIMEZONE`
- 必需的网络目标：由 `NEXTCLOUD_URL` 指定的主机（以及该主机的正常重定向路径）

如果注册表条目中显示“无需二进制文件”或“无需环境变量”，请将其视为过时的元数据，并在发布前进行修复。

## 预执行审计

在任何新环境中首次运行之前，请完成以下操作：
- 检查随附的脚本清单。
- 确保没有意外的端点或特权系统调用。
- 如果检查未完成，请勿运行该技能。
- 建议优先使用沙箱/容器环境进行验证，并使用最低权限的应用程序凭据。

## 安全性和发布注意事项

- 请勿在 `SKILL.md`、脚本、示例代码、提交信息或变更日志中硬编码凭据。
- 请将敏感信息仅存储在环境变量或本地秘密存储中。
- 为集成使用专用的应用密码；如果密码泄露或共享，请及时更换。
- 请将本地的 `.env` 文件排除在 Git 提交范围之外（参见 `.gitignore`）。
- 在发布之前，快速扫描文件中的敏感信息并删除任何意外出现的敏感内容。

## 随附脚本检查清单（首次使用前）

该技能包含两个脚本：`scripts/nextcloud.js`（用于文本操作）和 `scripts/files_binary.py`（用于二进制文件传输）。在新环境中运行之前，请检查以下内容：
1. 确认运行时要求：
   - `node --version`（必须为 20 及更高版本）
2. 检查外部端点：
   - `rg -n "https?://" scripts/nextcloud.js`
3. 检查敏感功能的使用情况：
   - `rg -n "child_process|spawn\\(|exec\\(|require\\(\"fs\"\\)|require\\('fs'\\)|fs\\." scripts/nextcloud.js`
4. 确认凭据仅通过环境变量传递：
   - `rg -n "NEXTCLOUD_URL|NEXTCLOUD_USER|NEXTCLOUD_TOKEN|NEXTCLOUD_TIMEZONE" scripts/nextcloud.js`
5. 先在低风险模式下运行：
   - 使用专用的低权限 Nextcloud 应用密码
   - 如果可能，请使用非生产数据测试

### 静态审计快照（当前版本）

对 `scripts/nextcloud.js` 的快速检查应显示：
- 配置信息从 `process.env.NEXTCLOUD_URL|USER|TOKEN|TIMEZONE` 中读取。
- 请求路径构建为 `${CONFIG.url}${endpoint}`，并使用 `fetch()` 函数发送请求。
- 代码中未发现明显的 `child_process` 或 `fs` 操作。

对 `scripts/files_binary.py` 的快速检查：
- 配置信息从 `os.environ.get("NEXTCLOUD_URL|USER|TOKEN")` 中读取。
- DAV URL 构建为 `{url}/remote.php/dav/files/{user}/{path}`。
- 仅使用标准库（`urllib`、`base64`、`xml.etree`）；不依赖第三方库。

这并非全面的安全审计。每次更新代码后，请重新执行这些检查。

## 运行脚本

```bash
node scripts/nextcloud.js <command> <subcommand> [options]
```

## 命令

### Notes（笔记）
- `notes list`：列出所有笔记
- `notes get --id <id>`：根据 ID 获取笔记内容
- `notes create --title <title> --content <content> [--category <category>]`：创建新笔记
- `notes edit --id <id> [--title <title>] [--content <content>] [--category <category>]`：编辑笔记内容
- `notes delete --id <id>`：删除笔记

### Tasks（任务）
- `tasks list [--calendar <calendar-name>]`：列出所有任务
- `tasks create --title <title> --calendar <calendar-name> --due <iso> [--priority <0-9>] [--description <text>] [--timezone <IANA>]`：创建新任务
- `tasks edit --uid <uid> [--calendar <calendar-name> --title <title> --due <iso> [--priority <0-9>] [--description <text>] [--timezone <IANA>]`：编辑任务
- `tasks delete --uid <uid> [--calendar <calendar-name>]`：删除任务
- `tasks complete --uid <uid> [--calendar <calendar-name>]`：完成任务

### Calendar（日历）
- `calendar list [--from <iso>] [--to <iso>]`：列出所有日历事件（默认范围：未来 7 天）
- `calendar create --summary <summary> --start <iso-or-date> --end <iso-or-date> --calendar <calendar-name> --description <text> [--timezone <IANA>] --all-day`：创建新日历事件
- `calendar edit --uid <uid> [--calendar <calendar-name> --summary <summary> --start <iso-or-date> --end <iso-or-date> --description <text> [--timezone <IANA>] --all-day`：编辑日历事件
- `calendar delete --uid <uid> [--calendar <calendar-name>]`：删除日历事件

**注意**：
- 在许多配置中，联系人生日信息会显示在日历事件中，但仅支持读取。
- 生日信息应通过 `contacts create/edit --birthday ...` 进行管理，而不能通过日历操作创建/编辑。
- `calendar list` 返回事件的 `summary`、`start`、`end` 等字段；如果存在，还可能包含 `location` 和 `description`。

### Calendar Discovery（日历发现）
- `calendars list [--type <tasks|events>]`：列出所有日历类型（任务或事件）

### Files（文件）
- `files list [--path <path>]`：列出所有文件
- `files search --query <query>`：根据文件名或路径查询文件
- `files get --path <path>`：获取文件内容
- `files upload --path <path> --content <content>`：上传文件
- `files delete --path <path>`：删除文件

### Files（二进制文件）——支持 ODT、DOCX、PDF、图片等格式

`nextcloud.js` 将文件内容作为文本字符串处理，因此无法正确处理二进制文件。对于二进制文件，请使用配套的 Python 脚本 `scripts/files_binary.py`：

```bash
python3 scripts/files_binary.py download <nc_path> <local_path>
python3 scripts/files_binary.py upload   <local_path> <nc_path>
python3 scripts/files_binary.py exists   <nc_path>
python3 scripts/files_binary.py list     [<nc_path>]
```

该脚本使用相同的 `NEXTCLOUD_URL`、`NEXTCLOUD_USER`、`NEXTCLOUD_TOKEN` 环境变量。它会根据文件扩展名自动检测文件类型（ODT、DOCX、XLSX、PDF、PNG、JPG 等）。

**使用建议**：
- **纯文本文件（.md、.txt、.csv）**：使用 `node scripts/nextcloud.js files get/upload`
- **二进制文件（.odt、.docx、.pdf、图片）**：使用 `python3 scripts/files_binary.py download/upload`

### Contacts（联系人）
- `contacts list [--addressbook <name>]`：列出所有联系人
- `contacts get --uid <uid> [--addressbook <name>]`：获取联系人信息
- `contacts search --query <query> [--addressbook <name>]`：搜索联系人
- `contacts create [--name <full-name>] ...`：创建新联系人
- `contacts edit --uid <uid> ...`：编辑联系人信息
- `contacts delete --uid <uid> ...`：删除联系人

### Address Book（地址簿）
- `addressbooks list`：列出所有地址簿

**联系人数据规范（重要说明）**

请使用 `fullName` 和 `structuredName` 作为标准名称字段。联系人输出包含以下字段：
- `uid`
- `addressBook`
- `fullName`
- `structuredName`（包含 `familyName`、`givenName`、`additionalNames`、`honorificPrefixes`、`honorificSuffixes`）
- `nameRaw`（仅用于诊断；默认不显示给用户）
- `emails`（数组或 `null`）
- `phones`（数组或 `null`）
- `organization`、`title`、`note`
- `birthday`（格式化为 `YYYY-MM-DD` 或 `--MM-DD` 以便阅读）
- `birthdayRaw`（原始的 CardDAV 格式）

## 可靠性规则（快速参考）

在每次写入操作时，请遵循以下规则以避免数据损坏或混淆：
1. **身份和命名**：切勿从 URL 推断 `UID`，始终使用 `uid` 参数。
- 对用户显示的名称使用 `fullName` 和 `structuredName`；`nameRaw` 仅用于诊断。
2. **联系人和生日信息的完整性**：
  - 生日输入格式：`YYYY-MM-DD`、`YYYYMMDD`、`--MM-DD`、`--MM-DD`。
  - 不要在 `BDAY` 后添加分号。
  - 生日信息应通过 `contacts create/edit --birthday ...` 进行管理；切勿直接编辑日历事件中的生日字段。
3. **更新操作**：仅修改用户明确请求的字段。
- 要清除字段值，请传递空值。
- 请尊重用户指定的 `--addressbook` 参数；否则使用默认值或询问用户。
4. **日历和任务的验证**：在发送数据前验证日期/时间格式；确保 `end` 大于 `start`。
- 对 ICS 文本字段进行转义处理。
- 验证任务优先级范围（`0..9`）。
- 对于不带时区的日期时间，使用 `--timezone` 或 `NEXTCLOUD_TIMEZONE`。
- 对于全天事件，使用 `VALUE=DATE` 的格式。

## 行为规范和安全性注意事项
- 不要假设所有列出的日历都可以写入。
- 将联系人生日信息视为只读/系统日历。
- 如果不存在可写入的日历事件，请说明无法执行相关操作。
- 有些日历包含多个组件（`VEVENT` 和 `VTODO`），请确保它们同时支持事件和任务操作。
- 对于文件操作（上传/下载/删除），必须提供非空的文件路径。
- 对于 CardDAV/WebDAV 操作，对输入数据进行转义处理。
- 在执行创建、编辑、完成、删除操作后，进行后续验证。
- 如果操作失败，请在 0.5 秒、1 秒、2 秒后重试。

## Nextcloud/CardDAV 的已知行为
- 服务器/客户端可能会协商或规范化 vCard 版本（`3.0` 对 `4.0`）和内容。
- 在有效的联系人信息中，`FN` 和 `N` 字段必须各出现一次。
- `BDAY` 错误通常是由于输入格式不正确造成的（例如分隔符错误），而非服务器故障。
- 折叠的 vCard 行在解析前需要展开。

## 错误处理规则
- `HTTP 403`（在创建/编辑/删除日历事件时）：可能是只读日历或权限问题；切换到可写入的事件日历。
- `HTTP 501`（在文件搜索时）：WebDAV `SEARCH` 不受支持；回退到递归 `PROPFIND` 和客户端过滤。
- `HTTP 415`（在更新任务/事件时）：ICS 格式错误；规范化格式后重试。
- 联系人信息写入成功但 UI 仍显示旧数据：在报告错误前执行验证重试。

## 代理行为：默认日历选择
- 当用户创建任务/事件时，如果没有指定日历：
  1. 运行 `calendars list --type tasks` 或 `calendars list --type events`。
  2. 过滤掉只读日历（例如联系人生日日历、节假日日历）。
  3. 如果存在可写入的日历，询问用户是否将其设置为默认日历。
  4. 将默认日历存储在内存中。
  5. 如果没有可写入的事件日历，说明无法执行相关操作，并建议用户在 Nextcloud 日历中创建日历。

## 代理行为：默认地址簿选择
- 当用户创建联系人时，如果没有指定地址簿：
  1. 运行 `addressbooks list`。
  2. 询问用户是否将其设置为默认地址簿。
  3. 将默认地址簿存储在内存中。

## 代理行为简明指南
这些指南是执行操作的快捷方式。上述可靠性规则仍然适用。

### 联系人和生日信息处理
- 确定地址簿（使用 `--addressbook` 参数或默认值）。
- 在创建/编辑联系人信息时，仅传递用户请求的字段；如果需要清除字段，请使用空值。
- 使用 `--name` 参数传递全名；使用 `structuredName` 参数处理包含多个名称的情况。
- 将多个电子邮件/电话号码作为 CSV 格式传递。
- 生日信息的修改始终通过 `contacts create/edit --birthday ...` 进行，切勿通过日历操作。

### 任务处理
- 如果未指定日历，自动确定日历。
- 在写入前验证任务的开始时间和优先级（`0..9`）。
- 创建/编辑/完成/删除操作后，通过列表功能进行验证。

### 日历事件处理
- 确定可写入的日历；将联系人生日日历视为只读日历。
- 验证 `start`/`end` 时间；确保 `end` 大于 `start`。
- 对于不带时区的日期时间，使用 `--timezone` 或 `NEXTCLOUD_TIMEZONE`。
- 对于全天事件，使用 `--all-day` 格式。

### 预约详情处理（高优先级）
- 当用户询问预约详情或地址时：
  1. 根据 `NEXTCLOUD_TIMEZONE` 确定“今天”的时间范围。
  2. 运行 `calendar list --from <start-of-day-iso> --to <end-of-day-iso>`。
  3. 根据用户输入的关键词（例如“皮肤科”、“医生”、“提供者名称”）过滤事件。
  4. 显示事件的摘要、时间范围、地点和关键信息。
  5. 如果有多个匹配项，询问用户具体需求。
  6. 如果没有匹配项，明确告知用户今天没有预约，并建议用户明天或下一周查看。
  7. 提供适合短信/聊天的简洁文本信息。

### 文件操作
- 对于文件操作，必须提供明确的文件路径。
- `files get/upload/delete` 接受相对路径或通过搜索返回的完整 DAV 链接。
- 对于二进制文件（ODT、DOCX、PDF、图片），使用 `python3 scripts/files_binary.py`；切勿通过 `nextcloud.js files upload` 传递二进制内容。
- 使用固定的测试路径进行临时文件操作。
- 上传文件后删除临时文件。
- 使用用户输入的查询语句进行文件搜索；系统会自动优化查询结果。
- 对于大量文件，先使用精确的路径进行搜索，以减少负载。

### 笔记操作
- 创建笔记时需要提供明确的标题和内容。
- 创建/编辑后，根据 ID 查阅笔记内容。
- 删除临时测试笔记。

## 内部测试协议
在真实环境中测试该技能时：
- 执行以下操作：创建/获取/编辑/删除联系人信息、创建/获取/编辑笔记、上传/获取/删除文件、创建/列出/查找/删除任务、创建/列出/查找/编辑日历。
- 为所有测试数据添加唯一的时间戳后缀，并在用户未请求的情况下删除临时文件。
- 使用最低权限的凭据进行测试，并监控输出流量；过程仅与 `NEXTCLOUD_URL` 通信。

**日历异常处理**：
- 如果不存在可写入的日历事件，请将日历操作标记为故意跳过（环境限制），但仍执行 `calendar list` 操作。
- 不要将此视为技能失败，而是视为服务器功能/权限限制。

## 持久性规则
请将以下规则保存在内存中：
- 生日信息属于联系人字段：使用 `contacts create/edit --birthday ...` 进行操作；切勿直接修改联系人生日信息。
- 对于全天事件，始终使用 `calendar create/edit --all-day` 和日期格式（避免使用包含时间范围的格式）。
- 对于不带时区的日期时间，使用 `--timezone` 或 `NEXTCLOUD_TIMEZONE`；如果时区未知，请询问用户。
- 对于可写入的事件日历，优先使用用户指定的日历；如果遇到 403 错误，说明可能是只读/权限问题。
- 在确认最终结果前，通过列表功能验证事件/联系人的写入操作。

## 故障排除指南
- 如果生日信息已更新但在 Nextcloud UI 中未显示：
  - 立即运行 `contacts get --uid ...`。
  - 如果 API 中的信息正确，建议用户稍等片刻后再刷新 UI。
  - 在重试一段时间后再次检查。

- `contacts get` 和 `contacts search` 的结果不一致：
  - 优先进行重试，然后使用最新的一致结果。
- 在等待期间不要创建重复的联系人记录。

- 如果任务创建失败：
  - 运行 `calendars list --type events` 并确认存在至少一个可写入的日历。
  - 如果只有只读日历，说明存在限制，停止尝试创建操作。

## 输出格式
所有命令返回 JSON 格式：
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