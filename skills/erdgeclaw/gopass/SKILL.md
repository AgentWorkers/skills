---
name: gopass
description: "使用 gopass（团队密码管理器）来存储、检索、列出和管理密码。当用户需要保存凭据、查找密码、生成新密码、管理密码条目或与 gopass 密码存储系统进行交互时，可以使用该工具。涵盖 CRUD 操作（创建、读取、更新、删除）、密码生成、一次性密码（TOTP）的生成、密码接收者的设置、存储系统的挂载以及剪贴板操作等功能。"
---

# gopass 技能

gopass 是一款专为团队设计的 CLI 密码管理工具，基于 GPG 和 Git 技术构建。

## 先决条件

- 已安装 `gopass` 可执行文件
- 拥有有效的 GPG 密钥（gopass 使用 GPG 进行加密）
- 已完成存储初始化（通过 `gopass init` 或 `gopass setup` 命令）

## 常用操作

### 列出密码
```bash
gopass ls
gopass ls -f          # flat list
```

### 查看密码
```bash
gopass show path/to/secret           # full entry (password + metadata)
gopass show -o path/to/secret        # password only
gopass show -c path/to/secret        # copy to clipboard
gopass show path/to/secret key       # show specific field
```

### 创建/更新密码
```bash
gopass insert path/to/secret         # interactive
gopass edit path/to/secret           # open in $EDITOR
echo "mypassword" | gopass insert -f path/to/secret   # non-interactive
```

在首行下方添加键值对形式的密码元数据：
```
mysecretpassword
username: erdGecrawl
url: https://github.com
notes: Created 2026-01-31
```

### 生成新密码
```bash
gopass generate path/to/secret 24           # 24-char password
gopass generate -s path/to/secret 32        # with symbols
gopass generate --xkcd path/to/secret 4     # passphrase (4 words)
```

### 删除密码
```bash
gopass rm path/to/secret
gopass rm -r path/to/folder          # recursive
```

### 移动/复制密码
```bash
gopass mv old/path new/path
gopass cp source/path dest/path
```

### 搜索密码
```bash
gopass find github                   # search entry names
gopass grep "username"               # search entry contents
```

## 存储管理

### 初始化存储
```bash
gopass setup                         # guided first-time setup
gopass init <gpg-id>                 # init with specific GPG key
```

### 挂载子存储
```bash
gopass mounts add work /path/to/work-store
gopass mounts remove work
gopass mounts                        # list mounts
```

### 同步（git push/pull）
```bash
gopass sync
```

### 设置团队访问权限
```bash
gopass recipients                    # list
gopass recipients add <gpg-id>
gopass recipients remove <gpg-id>
```

## TOTP（一次性密码）
```bash
gopass otp path/to/secret            # show current TOTP code
```
将 TOTP URI 以 `totp: otpauth://totp/...` 的格式存储在密码条目中。

## 非交互式使用技巧

- 使用 `echo "pw" | gopass insert -f path` 进行批量密码添加
- 使用 `gopass show -o path` 输出仅包含密码的内容（便于机器读取）
- 使用 `gopass show -f path` 可以抑制警告信息
- 设置 `GOPASS_NO_NOTIFY=true` 可以关闭桌面通知
- 使用 `gopass --yes` 可以自动确认操作提示