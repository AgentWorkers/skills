---
name: serper
description: 通过 Serper API 进行专业搜索（新闻、地点、地图、评论、学者信息、专利）以及批量数据抓取。
---

# Serper Search

## 使用方法
```bash
serperV search -q "Apple Inc" -t search --tbs qdr:h --page 3
serperV scrape -u "https://site1.com, https://site2.com"
```

- **搜索类型**：`search`、`places`、`maps`、`news`、`shopping`、`scholar`、`patents`。
- **时间范围（`--tbs`）**：`qdr:h`（小时）、`qdr:d`（天）、`qdr:w`（周）、`qdr:m`（月）、`qdr:y`（年）。
- **参数**：
  - `-q` / `--query`：搜索查询（默认启用自动补全功能）。
  - `-u` / `--url`：一个或多个网址（用逗号分隔）。
  - `-t` / `--type`：搜索端点（默认为 `search`）。
  - `-l` / `--limit`：显示结果的数量。
  - `-g` / `--gl`：国家代码。
  - `-h` / `--hl`：语言代码。
  - `-p` / `--page`：指定的结果页面。

## 安装方法
1. `npm install -g @vinitngr/serper-v --force`
2. `serperV auth <api_key>`