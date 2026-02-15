---
name: carddav-contacts
description: 使用 vdirsyncer 和 khard 同步和管理 CardDAV 联系人（来自 Google、iCloud、Nextcloud 等服务）。
metadata: {"clawdbot":{"emoji":"📇","os":["linux"],"requires":{"bins":["vdirsyncer","khard"]},"install":[{"id":"apt","kind":"apt","packages":["vdirsyncer","khard"],"bins":["vdirsyncer","khard"],"label":"Install vdirsyncer + khard via apt"}]}}
---

# CardDAV联系人管理（vdirsyncer + khard）

**vdirsyncer** 将 CardDAV 中的联系人信息同步到本地的 `.vcf` 文件中，**khard** 则通过命令行（CLI）读取并管理这些联系人信息。

## 先进行同步

在查询之前，请务必先完成同步操作，以确保获取到最新的联系人信息：
```bash
vdirsyncer sync
```

## 快速搜索（智能搜索）

如果配置了 `default_action = list`（默认设置），您可以无需使用任何子命令直接进行搜索：
```bash
khard "john"                     # Search for "john" in all fields
khard "pilar"                    # Search for "pilar"
```

## 列出联系人信息并搜索（显式搜索）

当需要使用特定的搜索选项，或者默认的搜索方式不符合您的需求时，可以使用 `list` 命令：
```bash
khard list                       # List all contacts
khard list "john"                # Search explicitly
khard list -a work               # List only from 'work' address book
khard list -p                    # Parsable output (tab-separated)
```

## 查看联系人详情

```bash
khard show "john doe"            # Show details (pretty print)
khard show --format yaml "john"  # Show as YAML (good for editing)
```

## 快速查找字段信息

可以提取特定的联系人信息（非常适合用于数据传输或处理）：
```bash
khard email "john"               # List emails only
khard phone "john"               # List phone numbers only
khard postaddress "john"         # List postal addresses
```

## 管理联系人信息

```bash
khard new                        # Create new contact (interactive editor)
khard edit "john"                # Edit contact (interactive editor)
khard remove "john"              # Delete contact
khard move "john" -a work        # Move to another address book
```

## 配置设置

### 1. 配置 vdirsyncer（位于 `~/.config/vdirsyncer/config` 文件中）

```ini
[pair google_contacts]
a = "google_contacts_remote"
b = "google_contacts_local"
collections = ["from a", "from b"]
conflict_resolution = "a wins"

[storage google_contacts_remote]
type = "carddav"
url = "https://www.googleapis.com/.well-known/carddav"
username = "your@email.com"
password.fetch = ["command", "cat", "~/.config/vdirsyncer/google_app_password"]

[storage google_contacts_local]
type = "filesystem"
path = "~/.local/share/vdirsyncer/contacts/"
fileext = ".vcf"
```

### 2. 配置 khard（位于 `~/.config/khard/khard.conf` 文件中）

请务必将 `default_action` 设置为 `list`，以启用快速搜索功能：
```ini
[addressbooks]
[[google]]
path = ~/.local/share/vdirsyncer/contacts/default/

[general]
default_action = list
editor = vim
merge_editor = vimdiff

[contact table]
display = formatted_name
sort = last_name
```

### 3. 初始化程序

```bash
mkdir -p ~/.local/share/vdirsyncer/contacts
vdirsyncer discover google_contacts
vdirsyncer sync
```