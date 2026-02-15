---
name: apple-contacts
description: 从 macOS 的 Contacts.app 中查找联系人信息。该功能可用于将电话号码解析为联系人姓名、查询联系人详情或搜索地址簿中的联系人。
metadata: {"clawdbot":{"emoji":"👤","os":["darwin"]}}
---

# Apple Contacts

通过 AppleScript 查询 Contacts.app 应用程序。

## 快速查找

```bash
# By phone (name only)
osascript -e 'tell application "Contacts" to get name of every person whose value of phones contains "+1XXXXXXXXXX"'

# By name
osascript -e 'tell application "Contacts" to get name of every person whose name contains "John"'

# List all
osascript -e 'tell application "Contacts" to get name of every person'
```

## 完整的联系人信息

⚠️ 请勿使用 `first person whose` — 这个方法存在漏洞。请使用以下模式：

```bash
# By phone
osascript -e 'tell application "Contacts"
  set matches to every person whose value of phones contains "+1XXXXXXXXXX"
  if length of matches > 0 then
    set p to item 1 of matches
    return {name of p, value of phones of p, value of emails of p}
  end if
end tell'

# By name
osascript -e 'tell application "Contacts"
  set matches to every person whose name contains "John"
  if length of matches > 0 then
    set p to item 1 of matches
    return {name of p, value of phones of p, value of emails of p}
  end if
end tell'
```

## 电话查找

⚠️ **必须精确匹配存储的格式**。

| 存储的值 | 搜索的值 | 是否匹配？ |
|--------|--------|--------|
| `+1XXXXXXXXXX` | `+1XXXXXXXXXX` | ✅ |
| `+1XXXXXXXXXX` | `XXXXXXXXXX` | ❌ |

建议先尝试使用 `+1` 前缀进行搜索。如果失败，可以尝试按姓名进行搜索。

## 姓名搜索

- 不区分大小写
- 支持部分匹配（使用 `contains`）
- 精确匹配：请使用 `is` 而不是 `contains`

## 输出结果

输出结果将以逗号分隔的格式显示：`name, phone1, [phone2...], email1, [email2...]`

如果没有找到匹配项，则输出为空（这不是错误）。