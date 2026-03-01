---
name: pt-site
description: 从基于NexusPHP的PT网站搜索并下载种子文件，然后将其添加到qBittorrent中。适用于用户需要搜索特定的PT网站、下载种子文件或在私有跟踪器上查找种子的情况。
---
# PT网站 - 基于NexusPHP的种子文件搜索与下载

在基于NexusPHP的私有种子源上搜索种子文件，下载`.torrent`文件，并将其添加到qBittorrent中。

## 设置

凭据：`~/.clawdbot/credentials/pt-site/sites.json`

```json
{
  "sites": {
    "mySite": {
      "url": "https://pt.example.com",
      "cookie": "c_secure_uid=xxx; c_secure_pass=xxx"
    }
  }
}
```

## 使用方法

### 1. 搜索种子文件

```bash
# Search using browser or web_fetch
browser action=open targetUrl="https://pt.example.com/torrents.php?search=keyword&search_type=0"
```

或者，如果可用的话，可以使用该网站的搜索API。

### 2. 解析搜索结果

NexusPHP的种子页面通常包含以下内容：
- 一个名为`torrents`的表格
- 列：`#`, `Type`, `Title`, `Download`, `Size`, `Seeders`, `Leechers`, `Complete`
- 下载链接：`download.php?id=<id>` 或 `download.php?id=<id>&passkey=<passkey>`

需要提取的信息包括：
- 种子文件ID
- 下载链接（可能需要使用passkey）
- 文件标题、大小、种子数量/下载者数量

### 3. 下载种子文件

```bash
# Download with curl, include Cookie header
curl -L -o /tmp/torrent.torrent "https://pt.example.com/download.php?id=123" \
  -H "Cookie: c_secure_uid=xxx; c_secure_pass=xxx"
```

### 4. 将种子文件添加到qBittorrent

可以使用qbittorrent工具来完成此操作：
```bash
# Add downloaded torrent
./scripts/qbit-api.sh add-file /tmp/torrent.torrent --category "PT"
```

或者，也可以通过磁链（magnet link）或直接URL来下载：

```bash
./scripts/qbit-api.sh add "magnet:?xt=..." --category "PT"
```

## 工作流程

1. **询问用户**需要搜索的PT网站及关键词。
2. **从`sites.json`中加载凭据**。
3. 通过浏览器或直接访问URL进行搜索。
4. **显示搜索结果**（包括文件标题、大小、种子数量、下载者数量）。
5. **用户选择**要下载的种子文件。
6. **下载`.torrent`文件**。
7. **使用qbittorrent工具**将下载的种子文件添加到qBittorrent中。

## 注意事项

- 许多基于NexusPHP的种子网站需要使用passkey才能下载文件——可能需要从用户配置文件中获取passkey。
- 请遵守网站规则，不要发送大量请求（避免造成服务器负担）。
- 将下载的种子文件保存在`/tmp/`目录下，并使用唯一的文件名以避免文件冲突。