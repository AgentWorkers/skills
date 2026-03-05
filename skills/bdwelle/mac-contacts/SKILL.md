---
name: mac-contacts
description: 用于读取和管理 macOS 联系人信息的命令行工具（CNContactStore）。支持通过姓名、电子邮件、电话号码、城市或国家进行搜索；可以查看联系人的所有信息（包括其所属的列表）；支持创建和更新联系人信息（包括姓名、组织名称、电话号码、电子邮件和邮寄地址）；支持删除联系人；同时支持管理联系人所属的群组（列表）。适用于需要在 macOS 上查找、添加、编辑、删除或整理联系人信息的情况，或者在需要获取联系人的电话号码、电子邮件、地址或其所属列表时使用该工具。
compatibility: >
  Requires macOS with Contacts access granted to Terminal/your agent host.
  Requires Python 3, pyobjc-framework-Contacts, and PyYAML
  (pip install pyobjc-framework-Contacts pyyaml).
metadata:
  author: bdwelle
---
# mac-contacts

macOS 的 Contacts 命令行工具（CLI）基于 `CNContactStore` 进行操作。所有读取操作都会使用统一的联系人视图（合并了 iCloud、本地和 Exchange 的联系人数据）。所有写入操作都是原子的（即要么全部成功，要么全部失败），通过 `CNSaveRequest` 完成。在处理 iCloud 支持的群组时，由于 `CNSaveRequest.removeMember_fromGroup_` 方法会静默地返回空操作（无实际效果），因此需要使用 `osascript` 来实现群组成员的移除操作。

## 依赖项

```bash
pip install pyobjc-framework-Contacts
```

```bash
pip install pyyaml
```

首次运行时，系统会提示您是否允许终端（或您的代理主机）访问联系人信息。您也可以通过 **系统设置 → 隐私与安全 → 联系人** 来设置访问权限。

## 使用方法

```bash
python3 skill://mac-contacts/scripts/mac-contacts.py <subcommand> [options]
```

以下所有示例中，`mac-contacts` 都是该命令的简写形式。

---

## 子命令

### search

搜索联系人。通过位置参数查询，可以在 **姓名、单位、备注、电子邮件、电话号码**（电话号码会进行规范化处理）和 **邮政地址** 字段中进行搜索。可以使用特定的标志来限制搜索范围。

```
search [QUERY]
       [--list LIST]
       [--email EMAIL]
       [--phone PHONE]
       [--city CITY]
       [--country COUNTRY]
```

| 标志 | 描述 |
|------|-------------|
| `QUERY` | 在所有字段中进行全面搜索。电话号码会进行模糊匹配（查询的数字必须出现在联系人的电话号码中；至少需要 4 位数字才能匹配）。 |
| `--list LIST` | 仅返回属于指定列表/群的联系人。 |
| `--email EMAIL` | 按电子邮件地址进行匹配（使用 CNContact 的原生电子邮件匹配函数，效率较高）。 |
| `--phone PHONE` | 按电话号码进行匹配；在比较前会去除非数字字符。至少需要 4 位数字。 |
| `--city CITY` | 按邮政地址中的城市进行匹配。 |
| `--country COUNTRY` | 按邮政地址中的国家进行匹配。 |

**示例：**

```bash
# Comprehensive — finds by name, org, email, phone, address
mac-contacts search "John"
mac-contacts search "john@example.com"   # auto-matches email
mac-contacts search "415-555"            # auto-matches phone (≥4 digits)
mac-contacts search "San Francisco"      # auto-matches city

# Explicit field targeting
mac-contacts search --email "john@acme.com"
mac-contacts search --phone "415"        # error: fewer than 4 digits
mac-contacts search --phone "4155551234"
mac-contacts search --city "London"
mac-contacts search --country "Germany"

# Filter to list members
mac-contacts search --list "Work"
```

输出每个联系人的详细信息：姓名、单位、电话号码、电子邮件地址、邮政地址等。

---

### show

显示联系人的所有可用信息，包括其所属的列表。

```
show NAME
```

输出内容包括：全名（包括前缀/中间名/后缀）、昵称、单位、职位、部门、电话号码、电子邮件地址、邮政地址、社交媒体链接、生日、日期、备注（如果可读的话）以及该联系人所属的列表。

```bash
mac-contacts show "Jane Doe"
mac-contacts show "Apple"        # matches any contact whose name contains "Apple"
```

> **注意：** 如果有多个联系人匹配相同的姓名，只会显示第一个结果。

---

### create

创建一个新的联系人。除了 `--first-name` 之外的所有标志都是可选的。

```
create --first-name NAME
       [--last-name NAME]
       [--organization ORG]
       [--email EMAIL]     (repeatable)
       [--phone PHONE]     (repeatable)
       [--street STREET]
       [--city CITY]
       [--state STATE]
       [--zip ZIP]
       [--country COUNTRY]
       [--url URL]         (repeatable)
       [--birthday DATE]
```

```bash
mac-contacts create --first-name "Jane" --last-name "Doe" \
    --organization "Acme" \
    --email "jane@acme.com" --email "jane.personal@gmail.com" \
    --phone "415-555-0100" \
    --street "123 Main St" --city "San Francisco" \
    --state "CA" --zip "94102" --country "United States" \
    --url "https://jane.acme.com" \
    --birthday "1985-03-22"
```

> **注意：** `--note` 标志被故意省略了。因为编写联系人备注需要 `com.apple.developercontacts.notes` 权限，而基于终端的工具通常没有这个权限。

> **`--birthday` 格式：** `YYYY-MM-DD` 表示完整日期（例如 `1985-03-22`），或者 `--MM-DD` 表示月份/日期（不包含年份，例如 `--03-22`）。

---

### update

更新现有联系人的信息。电话号码和电子邮件地址的值会追加到现有值上（而不会被替换）。如果提供了邮政地址相关的标志，会添加新的邮政地址信息。

```
update NAME
       [--organization ORG]
       [--email EMAIL]     (repeatable, appends)
       [--phone PHONE]     (repeatable, appends)
       [--street STREET]
       [--city CITY]
       [--state STATE]
       [--zip ZIP]
       [--country COUNTRY]
       [--url URL]         (repeatable, appends)
       [--birthday DATE]   (replaces existing)
```

```bash
mac-contacts update "Jane Doe" --phone "415-555-0199"
mac-contacts update "Jane Doe" --organization "New Corp" --city "Oakland"
mac-contacts update "Jane Doe" --birthday "1985-03-22"
mac-contacts update "Jane Doe" --url "https://jane.dev"
```

---

### delete

删除一个联系人。除非指定了 `--force` 标志，否则会提示用户确认。

```
delete NAME [--force]
```

```bash
mac-contacts delete "Jane Doe"           # prompts y/N
mac-contacts delete "Jane Doe" --force   # no prompt
```

---

### add_to_list

将一个联系人添加到指定的列表（CNGroup）中。如果列表不存在，会先创建该列表。

```
add_to_list NAME LIST
```

```bash
mac-contacts add_to_list "Jane Doe" "Work"
```

---

### remove_from_list

从指定的列表中删除一个联系人。

```
remove_from_list NAME LIST
```

```bash
mac-contacts remove_from_list "Jane Doe" "Work"
```

> **实现说明：** 由于 `CNSaveRequest.removeMember_fromGroup_` 在处理 iCloud 支持的群组时会静默地返回空操作，因此需要使用 `osascript` 来实现成员移除功能。

---

### list_groups

列出存储中的所有联系人组（列表）。

```
list_groups
```

```bash
mac-contacts list_groups
```

---

## 输出格式

- `search`、`show` 和 `list_groups` 命令的输出格式为 YAML（需要 `pyyaml` 解析工具）。
  `search` 和 `list_groups` 返回一个 YAML 列表；`show` 返回一个单独的 YAML 对象。
  可以使用 `python3 -c "import sys,yaml; print(yaml.safe_load(sys.stdin))` 或 `yq` 来解析输出。
- 成功消息以 `Success:` 开头。
- 错误消息以 `Error:` 或 `[FATAL]` 开头。
- 如果没有找到结果，`search` 和 `list_groups` 命令的退出代码为 1。
- 其他命令在遇到错误时也会以代码 1 结束。

## 已知的限制

- **备注（写入）：** 设置联系人备注需要 `com.apple.developercontacts.notes` 权限。因此，`create` 和 `update` 命令不提供 `--note` 标志。现有的联系人备注可以通过 `show` 命令查看。
- **`update` 命令不会替换原有数据：** 电话号码、电子邮件地址和邮政地址的值只会被追加，而不会被替换。如果要修改这些值，需要删除联系人并重新创建，或者通过 Contacts.app 进行编辑。
- **`show` 命令的姓名匹配方式：** 使用 `CNContactPredicateForContactsMatchingName_` 函数在姓名字段中匹配子字符串。如果存在歧义，会返回第一个匹配的结果。