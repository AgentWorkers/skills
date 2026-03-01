---
name: icloud-toolkit
description: >
  统一的 iCloud 集成功能，支持日历、电子邮件和联系人管理。适用场景包括：  
  (1) 创建、查看、搜索或删除日历事件；  
  (2) 阅读、发送或搜索电子邮件；  
  (3) 查找、创建、编辑或删除联系人；  
  (4) 任何涉及 iCloud 日历、电子邮件或联系人的操作。  
  该功能支持时区转换、符合 iCloud 格式的显示，并能自动同步数据（通过 vdirsyncer）。
metadata:
  openclaw:
    emoji: "☁️"
    primaryEnv: "ICLOUD_APP_PASSWORD"
    install: ["brew install vdirsyncer", "brew install khal", "brew install himalaya", "brew install khard"]
    requires:
      bins: ["python3", "himalaya", "khal", "vdirsyncer", "khard"]
---
# iCloud 工具包

这是一个统一的日历、邮件和联系人管理 CLI 工具。通过一个脚本，可以完成所有与 iCloud 相关的操作。

**脚本：** `scripts/icloud.py`  
**配置文件：** `config/config.json`  

## 首次设置  

如果 `config/config.json` 不存在，该工具会输出 `SETUP_REQUIRED` 的提示，而不会执行任何命令。请按照以下两步进行设置：  

### 第一步：配置（收集信息并连接到 iCloud）  

向用户询问以下信息：  
1. **Apple ID**（用于登录 iCloud 的电子邮件地址）  
2. **发送地址**（用于发送邮件的发件地址；通常与 Apple ID 相同，除非用户使用了自定义域名）  
3. **显示名称**（用于邮件中的发件人名称）  
4. **时区**（采用 IANA 格式，例如 `America/New_York`；如果省略，则会自动检测）  

大多数用户使用他们的 Apple ID 进行发送，因此第二步只需询问：“您的发送地址是否与 Apple ID 相同？或者您是否使用了自定义域名？”如果发送地址与 Apple ID 相同，则可以省略 `--apple-id` 参数。只有使用 iCloud 自定义域名（例如 `you@yourdomain.com`）的用户需要单独设置 `--apple-id`。  

密码由 OpenClaw 的 secrets 系统管理，存储在 `$ICLOUD_APP_PASSWORD` 变量中。如果用户尚未设置密码，请告知他们：  
> 您需要一个专门用于 iCloud 应用的密码。请访问 https://appleid.apple.com → 登录 → 安全设置 → 应用专用密码 → 为 “iCloud 工具包” 生成一个新的密码。然后使用以下命令设置密码：  
`/secret set ICLOUD_APP_PASSWORD`  

接下来运行以下命令：  
```bash
# Most users (sending address = Apple ID):
python3 $ICLOUD setup configure --email APPLE_ID --name "USER_NAME" --timezone TIMEZONE

# Custom domain users (sending address differs from Apple ID):
python3 $ICLOUD setup configure --email SENDING_ADDRESS --apple-id APPLE_ID --name "USER_NAME" --timezone TIMEZONE
```  

此命令会生成认证文件，配置 vdirsyncer（用于处理 CalDAV 和 CardDAV 协议），执行发现和同步操作，并将检测到的日历和通讯录信息以 JSON 格式输出。  

### 第二步：完成设置（映射日历和通讯录信息）  

向用户展示第一步中检测到的日历和通讯录内容，询问他们为每个日历和通讯录指定一个友好的名称（例如 “个人日历”、“工作日历” 等），并选择默认设置。  

然后运行以下命令：  
```bash
python3 $ICLOUD setup finalize --email SENDING_ADDRESS --apple-id APPLE_ID --name "USER_NAME" --timezone TIMEZONE \
  --calendars '{"Personal":"uuid-from-discovery","Work":"another-uuid"}' --default Personal \
  --addressbooks '{"Contacts":"uuid-from-discovery"}' --default-addressbook Contacts
```  

此命令会更新 `config/config.json` 文件（包括用于匹配回复地址的邮件地址信息），生成 khal、himalaya 和 khard 的配置文件，并执行验证操作。`--addressbooks` 和 `--default-addressbook` 参数是可选的，省略这些参数即可跳过联系人设置步骤。  

## 快速参考  
```bash
ICLOUD=~/.openclaw/workspace/skills/icloud-toolkit/scripts/icloud.py

# Calendar
python3 $ICLOUD calendar list                                    # Today
python3 $ICLOUD calendar list --days 7                           # Next 7 days
python3 $ICLOUD calendar list --days 7 --calendar Appointments   # Specific calendar
python3 $ICLOUD calendar search "meeting"                        # Search events
python3 $ICLOUD calendar create <calendar> <date> <start> <end> <title> [--location] [--description]
python3 $ICLOUD calendar create-allday <calendar> <date> <title> [--description]
python3 $ICLOUD calendar delete <uid>                            # Delete by UID
python3 $ICLOUD calendar sync                                    # Manual sync

# Email
python3 $ICLOUD email list                                       # Latest 10
python3 $ICLOUD email list --count 20 --folder Sent              # Sent folder
python3 $ICLOUD email list --unread                              # Unread only
python3 $ICLOUD email read <id> [--folder X]                      # Read email (folder defaults to INBOX)
python3 $ICLOUD email send <to> <subject> <body>                 # Send email
python3 $ICLOUD email reply <id> <body> [--all] [--folder X]     # Reply (From auto-matched to whichever address received the original)
python3 $ICLOUD email search "from Apple" [--folder X]            # Search (folder defaults to INBOX)
python3 $ICLOUD email move <folder> <id> [--source X]             # Move email (source defaults to INBOX)
python3 $ICLOUD email delete <id> [--folder X]                   # Delete email (move to Deleted Messages)

# Folder
python3 $ICLOUD folder purge <folder>                            # Purge all emails from folder

# Contacts
python3 $ICLOUD contact list                                     # All contacts
python3 $ICLOUD contact list --addressbook Contacts --count 20   # Specific book, limit results
python3 $ICLOUD contact show <uid>                               # Show by UID
python3 $ICLOUD contact search "John"                            # Search contacts
python3 $ICLOUD contact create John Doe --email john@example.com --phone +15551234567
python3 $ICLOUD contact create --fn "Acme Corp" --org "Acme Corp"   # Org-only contact
python3 $ICLOUD contact edit <uid> --add-email second@example.com   # Add email to existing
python3 $ICLOUD contact edit <uid> --first Jane --last Smith        # Change name
python3 $ICLOUD contact delete <uid>                             # Delete by UID
python3 $ICLOUD contact sync                                     # Manual sync

# Setup
python3 $ICLOUD setup configure --email X --apple-id X --name X [--timezone X]   # Step 1: connect + discover
python3 $ICLOUD setup finalize --email X --apple-id X --name X --timezone X \
  --calendars '{"Name":"uuid"}' --default Name \
  [--addressbooks '{"Name":"uuid"}' --default-addressbook Name]                  # Step 2: write configs
python3 $ICLOUD setup verify                                        # Run smoke tests
python3 $ICLOUD setup init                                          # Interactive wizard (dev only)
python3 $ICLOUD setup discover-calendars                            # Show calendar mapping
```  

## 日历  

### 创建事件  

事件的时间是 **本地时间**；脚本会根据 `config/config.json` 中的 `timezone` 设置自动转换为 UTC 时间。所有时区都会正确处理夏令时（DST）。  

**内部处理流程：**  
1. 从 iCloud 同步最新数据  
2. 将本地时间转换为 UTC 时间（例如：CST 14:00 → UTC 20:00）  
3. 生成带有 UTC 时间戳的 .ics 文件（不使用 VTIMEZONE 标签，以避免 iCloud 将事件误判为全天事件）  
4. 将生成的 .ics 文件写入正确的日历目录  
5. 将更改推送到 iCloud  

### 列出事件  

### 搜索事件  

### 删除事件  

可以从 khal 的列表输出或创建事件的确认信息中获取事件的 UID。  

### 日历名称  

| 名称            | 用途                          |  
|-----------------|--------------------------------|  
| Social          | 社交活动、家人、朋友                |  
| Reminders       | 提醒事项                        |  
| Appointments     | 工作/专业预约                    |  
| General         | 默认分类                        |  

## 同步  

读取数据前和写入数据前后，系统会自动执行同步操作。也可以手动执行同步：  
```bash
python3 $ICLOUD calendar sync
```  

## 邮件  

### 列出邮件  

### 阅读邮件  

### 发送邮件  

**默认发件地址：**  
邮件是从 `config/config.json` 中的 `account_email` 字段发送的，而不是用于 IMAP/SMTP 认证的 iCloud 登录地址。这两个地址通常是不同的——因为 iCloud 允许用户在使用 Apple ID 登录时使用自定义域名发送邮件。在向用户预览邮件草稿时，务必显示正确的发件地址（即 `account_email` 中的地址）。  

**重要提示：**  
在代表用户发送邮件之前，务必先获得用户的许可。  

### 搜索邮件  

使用 himalaya 的查询语法（参数按位置顺序传递）：  
```bash
python3 $ICLOUD email search "from Apple"
python3 $ICLOUD email search "subject invoice"
python3 $ICLOUD email search "after 2026-02-01"
python3 $ICLOUD email search "from Apple and after 2026-01-01"
python3 $ICLOUD email search "from Apple" --folder "Sent Messages"   # Search non-INBOX folder
```  

### 移动邮件  

**注意：** 参数顺序为 `<文件夹> <ID>`（先输入文件夹名称，再输入邮件 ID）。如果未指定 `--source` 参数，系统会默认使用 INBOX 作为源文件夹。  

iCloud 的文件夹结构包括：INBOX、Sent Messages（已发送邮件）、Drafts（草稿）、Deleted Messages（已删除邮件）、Junk（垃圾邮件）、Archive（存档文件）。  

### 删除邮件  

### 文件夹操作  

### 清空文件夹  

会永久删除文件夹中的所有邮件。文件夹本身不会被删除，但文件夹内容会被清空。  

**注意：** 此操作是非交互式的（不会显示确认提示），因此在执行前请务必获得用户的确认。  

## 联系人  

### 列出联系人  

### 显示联系人信息  

### 搜索联系人  

### 创建联系人  

**内部处理流程：**  
1. 从 iCloud 同步最新联系人信息（如果同步失败，则终止操作）  
2. 生成符合 vCard 3.0 标准的联系人卡片文件（包含 UUID）  
3. 将生成的 `.vcf` 文件写入通讯录目录  
4. 将更改推送到 iCloud  

### 编辑联系人  

**无损编辑：**  
在编辑联系人信息时，Apple 特定的属性（如 X-ABLabel、X-APPLE-*、PHOTO 等）会被保留。编辑操作只会修改用户指定的字段，并将修改后的文件保存回原路径（同时保持 vdirsyncer 的文件名映射规则）。  

### 删除联系人  

### 获取联系人 ID  

可以从联系人列表的输出结果或创建联系人的确认信息中获取联系人 ID。  

### 同步  

读取数据前和写入数据前后，系统会自动执行同步操作。也可以手动执行同步：  
```bash
python3 $ICLOUD contact sync
```  

## 其他注意事项：  
- **时区设置：** 在 `config/config.json` 中设置正确的时区（例如 `America/New_York`、`Europe/London`）。所有输入的时间都是本地时间，脚本会自动进行夏令时调整。  
- **同步机制：** 在读取数据前和写入数据前后会自动执行同步，无需手动操作。  
- **配置文件：** `config/config.json` 包含日历名称、通讯录名称、文件路径和时区设置。  
- **密码管理：** 使用 `config/auth` 中存储的密码进行身份验证，该密码同时被 himalaya、vdirsyncer 和 khard 共享。  
- **自我测试：** 使用 `python3 $ICLOUD --test` 命令可以验证 UTC 转换、.ics 文件生成和 vCard 文件的解析功能。  
- **首次设置：** 请参考上面的 “首次设置” 部分。