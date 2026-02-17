---
name: discogs-cli
description: 这是一个 OpenClaw 技能，用于管理用户在 Discogs 上的黑胶唱片收藏。
metadata: {"clawdbot":{"emoji":"Vinyl","requires":{"bins":["go"]}}}
---
# OpenClaw 的 Discogs 收藏管理技能

该技能提供了一个命令行接口，用于与用户在其 Discogs.com 上的唱片收藏进行交互。它专为 OpenClaw 助手设计，采用了类似于 `git` 或 `gog` 的子命令结构。

## 先决条件

该技能是一个 Go 程序，需要安装 Go 工具链。

**安装（Debian/Ubuntu）：**
`sudo apt-get update && sudo apt-get install -y golang-go`

## 一次性设置

首次使用前，必须运行随附的安装脚本。该脚本会编译 Go 可执行文件，并将其放置在技能目录内的指定位置。

1. **运行安装脚本：**
    ```bash
    skills/discogs-cli/install.sh
    ```

2. **配置凭据：**
    该命令会将您的 Discogs 令牌和用户名保存到配置文件（`~/.config/discogs-cli/config.yaml`）中。
    ```bash
    skills/discogs-cli/bin/discogs-cli config set -u "YourUsername" -t "YourSecretToken"
    ```

## 使用方法

所有命令都必须以可执行文件的完整路径作为前缀。

### 下载专辑封面

下载指定专辑的封面，并在聊天界面中显示。

```bash
skills/discogs-cli/bin/discogs-cli release art <release_id>
```

### 列出收藏文件夹

显示所有文件夹及其包含的唱片数量。

```bash
skills/discogs-cli/bin/discogs-cli collection list-folders
```

### 列出文件夹中的唱片

显示特定文件夹内的所有唱片。输出结果为格式化的表格。

```bash
# List all releases from the "All" folder (default)
skills/discogs-cli/bin/discogs-cli collection list

# List all releases from a specific folder by ID
skills/discogs-cli/bin/discogs-cli collection list --folder 8815833
```

## 在 Discogs 数据库中搜索

搜索唱片、艺术家或唱片公司。

```bash
# Search for a release (default type)
skills/discogs-cli/bin/discogs-cli search "Daft Punk - Discovery"

# Search for an artist
skills/discogs-cli/bin/discogs-cli search --type artist "Aphex Twin"
```

## 管理您的愿望清单

管理您的 Discogs 愿望清单。

### 显示愿望清单

显示愿望清单中的所有项目。

```bash
skills/discogs-cli/bin/discogs-cli wantlist list
```

### 将唱片添加到愿望清单

通过唱片 ID 将其添加到愿望清单中。

```bash
skills/discogs-cli/bin/discogs-cli wantlist add 12345
```

### 从愿望清单中删除唱片

通过唱片 ID 从愿望清单中删除唱片。

```bash
skills/discogs-cli/bin/discogs-cli wantlist remove 12345
```

## 缓存和估值命令

这些命令依赖于本地缓存来提高性能。您需要先运行 `sync` 命令来填充缓存。

### 同步收藏详情（耗时）

获取收藏中每个项目的详细信息并构建本地缓存。此命令执行速度较慢，建议在后台运行。请告知用户此操作需要一些时间。

```bash
skills/discogs-cli/bin/discogs-cli collection sync
```

### 获取收藏价值（快速）

读取本地缓存以获取每个项目的预估市场价值及整个收藏的总价值。此命令执行速度较快。如果执行失败，可能是因为缓存未更新，此时需要运行 `sync` 命令。

```bash
skills/discogs-cli/bin/discogs-cli collection value
```

### 获取单张唱片的详细信息（快速）

提供单张唱片的详细信息，包括曲目列表。

```bash
skills/discogs-cli/bin/discogs-cli collection get 35198584
```