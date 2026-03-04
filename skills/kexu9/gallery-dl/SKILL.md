---
name: gallery-dl
description: Download image galleries and collections from 100+ sites. Use when: (1) Downloading from Reddit, Twitter, Instagram, Pixiv, Danbooru, (2) Batch downloading image galleries, (3) Archiving artist portfolios, (4) Downloading from specific tags or users.
version: 1.1.0
changelog: "v1.1.0: Added reasoning framework, decision tree, troubleshooting, self-checks"
metadata:
  openclaw:
    requires:
      bins:
        - python3
    emoji: "🖼️"
    category: "utility"
    homepage: https://github.com/mikf/gallery-dl
---

# gallery-dl

该工具可以从100多个网站下载图片库和图片集合。

## 该功能的使用场景

当用户需要从Reddit、Twitter、Instagram、Pixiv、Danbooru或其他支持该功能的网站下载图片时，该功能会被激活。

## 工作流程

| 步骤 | 操作 | 原因 |
|------|--------|-----|
| 1 | **安装** | 通过pip安装gallery-dl工具 |
| 2 | **身份验证** | 如有必要，配置身份验证信息 |
| 3 | **确定网站及URL类型** | 识别目标网站及其URL格式 |
| 4 | **下载图片** | 根据用户设置下载图片 |
| 5 | **组织文件** | 将下载的图片保存到指定文件夹 |

---

## 安装

```bash
pip install gallery-dl
```

---

## 支持的网站列表

Reddit、Twitter/X、Instagram、Tumblr、Pixiv、Danbooru、Gelbooru、Furbooru、ArtStation、DeviantArt、Flickr、Newgrounds、HBO、TikTok、YouTube等，共计100多个网站。

完整列表：https://github.com/mikf/gallery-dl#supported-services

---

## 基本用法

### 命令格式

```bash
gallery-dl "URL" [options]
```

### 使用示例

```bash
# Download from Reddit
gallery-dl "https://www.reddit.com/r/wallpapers/"

# Download to specific folder
gallery-dl "URL" -D /path/to/folder

# Download specific user's posts
gallery-dl "https://twitter.com/username/media"

# Download from Pixiv artist
gallery-dl "https://www.pixiv.net/users/12345"

# Download from Danbooru tags
gallery-dl "https://danbooru.donmai.us/posts?tags=cat"
```

---

## 参数说明

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `-D, --directory PATH` | 下载路径 | ./gallery-dl |
| `-f, --filename FORMAT` | 文件名模板 | {id}.{extension} |
| `--range RANGE` | 下载范围（例如：1-10） | all |
| `--limit N` | 下载数量限制 | 无限制 |
| `--username USER` | 登录用户名 | - |
| `--password PASS` | 登录密码 | - |
| `--netrc` | 使用.netrc文件进行身份验证 | false |

---

## 文件名模板示例

```bash
# Default (id.extension)
gallery-dl "URL" -f "{id}.{extension}"

# By date (YYYY/id.extension)
gallery-dl "URL" -f "{date:%Y}/{id}.{extension}"

# By site (site/id.extension)
gallery-dl "URL" -f "{domain}/{id}.{extension}"

# Original filename
gallery-dl "URL" -f "/O"
```

---

## 身份验证方式

许多网站需要用户登录才能下载图片。以下是三种常见的身份验证方法：

### 1. 命令行登录

```bash
gallery-dl "URL" --username USER --password PASS
```

### 2. 使用.netrc文件

在用户主目录下创建`.netrc`文件：

```
machine twitter.com
login username
password password
```

### 3. 使用配置文件（config.json）

在用户主目录下创建`.config/gallery-dl/config.json`文件：

```json
{
    "extractor": {
        "twitter": {
            "username": "user",
            "password": "pass"
        },
        "pixiv": {
            "username": "user", 
            "password": "pass"
        }
    }
}
```

---

## 常见问题及解决方法

### 问题：“gallery-dl: 命令未找到”

- **原因**：未安装gallery-dl工具。
- **解决方法**：运行 `pip install gallery-dl`。

### 问题：“HTTP Error 401: Unauthorized”

- **原因**：需要登录。
- **解决方法**：配置身份验证信息（使用`--username`和`--password`参数，或通过`.netrc`文件）。

### 问题：“HTTP Error 403: Forbidden”

- **原因**：可能受到下载速率限制或访问了受保护的内容。
- **解决方法**：等待一段时间后重试，或检查用户名和密码是否正确。

### 问题：“没有找到图片”

- **原因**：提供的URL错误或该网站不支持图片下载。
- **解决方法**：确认URL是否正确。

### 问题：“权限不足”

- **原因**：没有写入文件的权限。
- **解决方法**：检查目标文件夹的权限，或使用`-D`参数指定可写入的目录。

---

## 自我检查

- [ ] gallery-dl是否已安装：`gallery-dl --version`
- [ ] 提供的URL是否正确。
- [ ] 对于需要登录的网站，是否已配置身份验证信息。
- [ ] 输出文件夹是否存在且具有写入权限。
- [ ] 是否遵守了下载速率限制（避免频繁下载）。

---

## 快速参考

| 功能 | 命令示例 |
|------|---------|
| 下载Reddit图片 | `gallery-dl "https://www.reddit.com/r/sub/"` |
| 下载Twitter图片 | `gallery-dl "https://twitter.com/user/media"` |
| 下载Pixiv图片 | `gallery-dl "https://www.pixiv.net/users/12345"` |
| 将图片下载到指定文件夹 | `gallery-dl "URL" -D ./folder` |
| 限制下载数量 | `gallery-dl "URL" --limit 10` |
| 自定义文件名 | `gallery-dl "URL" -f "{id}.{extension}"` |

---