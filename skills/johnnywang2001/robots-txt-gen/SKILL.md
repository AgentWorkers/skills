---
name: robots-txt-gen
description: 生成、验证并分析网站的 robots.txt 文件。适用于以下场景：从头开始创建 robots.txt 文件、验证现有的 robots.txt 语法、检查某个 URL 是否被 robots.txt 规则允许或禁止访问，以及为常见的开发框架（如 WordPress、Next.js、Django、Rails）生成相应的 robots.txt 文件。此外，该工具还可用于审核爬虫指令或调试搜索引擎索引相关问题。
---
# robots-txt-gen

从命令行生成、验证和测试 robots.txt 文件。

## 快速入门

```bash
# Generate a robots.txt for a platform
python3 scripts/robots_txt_gen.py generate --preset nextjs --sitemap https://example.com/sitemap.xml

# Validate an existing robots.txt
python3 scripts/robots_txt_gen.py validate --file robots.txt

# Validate a remote robots.txt
python3 scripts/robots_txt_gen.py validate --url https://example.com/robots.txt

# Test if a URL is allowed for a user-agent
python3 scripts/robots_txt_gen.py test --file robots.txt --url /admin/dashboard --agent Googlebot

# Generate with custom rules
python3 scripts/robots_txt_gen.py generate --allow "/" --disallow "/admin" --disallow "/api" --disallow "/private" --sitemap https://example.com/sitemap.xml --agent "*"
```

## 命令

### `generate`
使用自定义规则或平台预设创建 robots.txt 文件。

选项：
- `--preset <name>` — 使用平台预设：`wordpress`、`nextjs`、`django`、`rails`、`laravel`、`static`、`spa`、`ecommerce`
- `--agent <name>` — 用户代理（默认：`*`）。可重复设置多个用户代理。
- `--allow <path>` — 允许访问的路径。可重复设置。
- `--disallow <path>` — 禁止访问的路径。可重复设置。
- `--sitemap <url>` — 网站地图 URL。可重复设置。
- `--crawl-delay <seconds>` — 爬取延迟时间（以秒为单位）。
- `--block-ai` — 添加规则以阻止常见的 AI 爬虫（如 GPTBot、ChatGPT-User、CCBot、Google-Extended、anthropic-ai 等）。
- `--output <file>` — 将结果写入指定文件，而不是输出到标准输出。

### `validate`
检查 robots.txt 文件的语法错误和最佳实践警告。

选项：
- `--file <path>` — 需要验证的本地文件路径。
- `--url <url>` — 需要获取并验证的远程 robots.txt 文件 URL。

### `test`
测试给定用户代理是否被允许访问或禁止访问特定的 URL 路径。

选项：
- `--file <path>` — 用于测试的 robots.txt 文件。
- `--url <path>` — 需要测试的 URL 路径（例如：`/admin/login`）。
- `--agent <name>` — 用于测试的用户代理（默认：`Googlebot`）。

## 平台预设

| 预设 | 禁止访问的路径 | 备注 |
|--------|---------------|-------|
| `wordpress` | `/wp-admin/`, `/wp-includes/`, 查询参数 | 允许访问 `/wp-admin/admin-ajax.php` |
| `nextjs` | `/_next/static/`, `/api/`, `/.next/` | Next.js 的标准路径 |
| `django` | `/admin/`, `/static/admin/`, `/media/private/` | Django 的管理页面和私有媒体文件 |
| `rails` | `/admin/`, `/assets/`, `/tmp/` | Rails 的常用路径 |
| `laravel` | `/admin/`, `/storage/`, `/vendor/` | Laravel 的常用路径 |
| `static` | 不阻止任何访问 | 允许所有访问，并包含网站地图 |
| `spa` | `/api/`, `/assets/` | 单页应用（SPA）的常见路径 |
| `ecommerce` | `/cart/`, `/checkout/`, `/account/`, `/search?` | 防止爬取用户会话相关页面 |

## AI 爬虫阻止

`--block-ai` 标志用于添加规则，以阻止以下常见的 AI 爬虫：
- GPTBot、ChatGPT-User（OpenAI）
- Google-Extended（Google AI）
- CCBot（Common Crawl）
- anthropic-ai（Anthropic）
- Bytespider（ByteDance）
- ClaudeBot（Anthropic）
- FacebookBot（Meta）