---
name: freshrss
description: 从自托管的FreshRSS实例中查询标题和文章。当用户请求RSS新闻、最新标题、订阅源更新或希望从其FreshRSS阅读器中浏览文章时，可以使用此功能。支持按类别、时间范围和数量进行过滤。
---

# FreshRSS

通过兼容 Google Reader 的 API，从自托管的 FreshRSS 服务器中查询新闻标题。

## 设置

请设置以下环境变量：

```bash
export FRESHRSS_URL="https://your-freshrss-instance.com"
export FRESHRSS_USER="your-username"
export FRESHRSS_API_PASSWORD="your-api-password"
```

API 密码可以在 FreshRSS 的 “设置” → “个人资料” → “API 管理” 中进行设置。

## 命令

### 获取最新新闻标题

```bash
{baseDir}/scripts/freshrss.sh headlines --count 10
```

### 获取过去 N 小时的新闻标题

```bash
{baseDir}/scripts/freshrss.sh headlines --hours 2
```

### 获取特定类别的新闻标题

```bash
{baseDir}/scripts/freshrss.sh headlines --category "Technology" --count 15
```

### 仅获取未读的新闻标题

```bash
{baseDir}/scripts/freshrss.sh headlines --unread --count 20
```

### 组合过滤条件

```bash
{baseDir}/scripts/freshrss.sh headlines --category "News" --hours 4 --count 10 --unread
```

### 列出所有类别

```bash
{baseDir}/scripts/freshrss.sh categories
```

### 列出所有新闻源

```bash
{baseDir}/scripts/freshrss.sh feeds
```

## 输出

新闻标题的格式如下：
```
[date] [source] Title
  URL
  Categories: cat1, cat2
```

## 注意事项

- 如果未指定数量，默认显示 20 条新闻标题。
- 时间过滤使用 `--hours` 参数来指定相对时间范围（例如：过去 2 小时）。
- 类别名称区分大小写，必须与 FreshRSS 中的类别名称完全匹配。
- 使用 `categories` 命令可以查看可用的类别名称。