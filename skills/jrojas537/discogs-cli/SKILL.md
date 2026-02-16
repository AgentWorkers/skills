---
name: discogs-cli
description: 在 Discogs 上管理用户的黑胶唱片收藏。可以使用它来列出收藏中的唱片或文件夹。
metadata: {"clawdbot":{"emoji":"Vinyl","requires":{"bins":["go"]}}}
---
# Discogs 收藏管理器

该工具提供了一个命令行接口，用于与用户在 Discogs.com 上的唱片收藏进行交互。它采用了类似于 `git` 或 `gog` 的子命令结构。

## 前提条件

该工具是一个 Go 语言编写的程序，因此需要安装并编译 Go 工具链。

**安装（Debian/Ubuntu）：**
```
sudo apt-get update && sudo apt-get install -y golang-go
```

## 首次使用前的设置

在首次使用之前，您需要编译该工具，确保生成的二进制文件位于系统的 PATH 环境变量中，并配置您的登录凭据。

1. **编译工具：**
   进入工具所在的 `scripts` 目录，然后运行 Go 编译命令。
   ```bash
    cd <path_to_skill>/scripts && go build -o discogs-cli .
    ```

2. **安装工具：**
   将编译后的 `discogs-cli` 二进制文件移动到系统的 PATH 环境变量下的某个位置（例如 `/usr/local/bin`）。

3. **配置凭据：**
   该命令会将您的 Discogs 凭据（Token 和用户名）保存到配置文件 `~/.config/discogs-cli/config.yaml` 中。
   ```bash
    discogs-cli config set -u "YourUsername" -t "YourSecretToken"
    ```

## 使用方法

一旦二进制文件被编译并添加到系统的 PATH 环境变量中，您就可以运行以下命令：

### 下载专辑封面图片

下载指定专辑的封面图片，并在聊天界面中显示它。
```bash
discogs-cli release art <release_id>
```

### 列出收藏文件夹

显示所有文件夹及其包含的唱片数量。
```bash
discogs-cli collection list-folders
```

### 列出文件夹中的唱片

显示特定文件夹内的所有唱片，输出结果为格式化的表格。
```bash
# List all releases from the "All" folder (default)
discogs-cli collection list

# List all releases from a specific folder by ID
discogs-cli collection list --folder 8815833
```

## 在 Discogs 数据库中搜索

搜索唱片、艺术家或唱片厂牌。

```bash
# Search for a release (default type)
discogs-cli search "Daft Punk - Discovery"

# Search for an artist
discogs-cli search --type artist "Aphex Twin"
```

## 管理您的愿望清单

- **列出愿望清单：** 显示您愿望清单中的所有项目。
  ```bash
discogs-cli wantlist list
```

- **将唱片添加到愿望清单：** 根据唱片 ID 将其添加到愿望清单中。
  ```bash
discogs-cli wantlist add 12345
```

- **从愿望清单中删除唱片：** 根据唱片 ID 从愿望清单中删除唱片。
  ```bash
discogs-cli wantlist remove 12345
```

## 缓存与估值相关命令

这些命令依赖于本地缓存来提高性能。用户需要先运行 `sync` 命令来更新缓存。

### 同步收藏详情（耗时）

获取收藏中每首唱片的详细信息并构建本地缓存。此命令执行速度较慢，建议在后台运行。请告知用户此操作可能需要一些时间。
```bash
discogs-cli collection sync
```

### 获取收藏价值（快速）

读取本地缓存以获取每首唱片的预估市场价值以及整个收藏的总价值。此命令执行速度较快。如果执行失败，可能是因为缓存未更新，用户需要再次运行 `sync` 命令。
```bash
discogs-cli collection value
```

### 查看单张唱片的详细信息（快速）

提供单张唱片的详细信息，包括曲目列表。
```bash
discogs-cli collection get 35198584
```