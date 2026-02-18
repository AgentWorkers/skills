---
name: newsboat
description: OpenClaw AI代理技能：通过Newsboat读取和管理RSS/Atom订阅源。
homepage: https://github.com/ianwu-ca-778/openclaw-skills-newsboat
license: MIT
metadata:
  {
    "openclaw":
      { 
        "emoji": "📰",
        "requires": { "bins": ["newsboat", "sqlite3", "pandoc"] }
      }
  }
---
# Newsboat

本指南介绍了如何使用 Newsboat（一款命令行 RSS/Atom 订阅源阅读器）来阅读和管理 RSS/Atom 订阅源。

## 安装

### Debian/Ubuntu

```bash
sudo apt update
sudo apt install newsboat sqlite3 pandoc
```

### macOS

```bash
brew install newsboat sqlite3 pandoc
```

### 其他操作系统

请在互联网上搜索“在 [您的操作系统] 上安装 Newsboat”，以获取具体的安装说明。

## 文件目录
- 配置文件：`~/.newsboat/config`
- 订阅源地址：`~/.newsboat/urls`
- 缓存文件：`~/.newsboat/cache.db`

如果 Newsboat 未添加到系统的 PATH 环境变量中，请使用相应的操作系统搜索工具来找到其文件路径。

## 列出所有订阅源

```bash
cat ~/.newsboat/urls
```

### 示例输出
```
$ cat ~/.newsboat/urls
https://604now.com/rss/
```

## 添加订阅源

```bash
echo "https://example.com/feed.xml" >> ~/.newsboat/urls
```

## 删除订阅源

```bash
sed -i.bak '/https:\/\/example.com\/feed.xml/d' ~/.newsboat/urls
```

此操作会删除指定的订阅源地址，并生成一个名为 `urls.bak` 的备份文件。

## 刷新所有订阅源

```bash
newsboat -x reload
```

## 阅读文章

您可以使用 `sqlite3` 从 Newsboat 的缓存中检索文章内容，并通过 `pandoc` 将 HTML 格式转换为纯文本格式。

`rss_item` 表的结构如下：
```sql
CREATE TABLE rss_item (
	id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
	,guid VARCHAR(64) NOT NULL
	,title VARCHAR(1024) NOT NULL
	,author VARCHAR(1024) NOT NULL
	,url VARCHAR(1024) NOT NULL
	,feedurl VARCHAR(1024) NOT NULL
	,pubDate INTEGER NOT NULL
	,content VARCHAR(65535) NOT NULL
	,unread INTEGER (1) NOT NULL
	,enclosure_url VARCHAR(1024)
	,enclosure_type VARCHAR(1024)
	,enqueued INTEGER (1) NOT NULL DEFAULT 0
	,flags VARCHAR(52)
	,deleted INTEGER (1) NOT NULL DEFAULT 0
	,base VARCHAR(128) NOT NULL DEFAULT ""
	,content_mime_type VARCHAR(255) NOT NULL DEFAULT ""
	,enclosure_description VARCHAR(1024) NOT NULL DEFAULT ""
	,enclosure_description_mime_type VARCHAR(128) NOT NULL DEFAULT ""
);
```

### 阅读最新文章

```bash
sqlite3 -noheader ~/.newsboat/cache.db \
"SELECT 'title = ' || title || '\nurl   = ' || url || '\ndate  = ' || datetime(pubDate, 'unixepoch', 'localtime') || '\n\n' || content 
 FROM rss_item ORDER BY pubDate DESC LIMIT 1;" | \
pandoc -f html-native_divs-native_spans -t plain --strip-comments
```

### 示例输出
```
$ sqlite3 -noheader ~/.newsboat/cache.db \
"SELECT 'title = ' || title || '\nurl   = ' || url || '\ndate  = ' || datetime(pubDate, 'unixepoch', 'localtime') || '\n\n' || content 
 FROM rss_item ORDER BY pubDate DESC LIMIT 1;" | \
pandoc -f html-native_divs-native_spans -t plain --strip-comments

title = 90+ Tri-Cities Restaurants Are Dropping Exclusive Deals And
Menus For A Full Month\nurl =
https://604now.com/taste-of-the-tri-cities-february-march-2026/\ndate =
2026-02-13 16:36:10\n\n

Taste of the Tri-Cities returns for another delicious year, treating
everyone across Metro Vancouver to the amazing culinary delights that
the Coquitlam, Port Coquitlam, and Port Moody has to offer. For a whole
month, from February 15 to March 15, you can take part in one of the
tastiest annual festivals in the Lower Mainland.
```