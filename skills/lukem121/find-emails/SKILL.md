---
name: find-emails
description: 使用 crawl4ai在本地爬取网站以提取联系邮箱地址。该工具支持处理多个URL，并以域名分组的形式输出结果，以便于明确来源。通过使用URL过滤器（如“contact”、“about”、“support”等）进行深度爬取，从而在相关页面中找到邮箱地址。适用于从网站中提取邮箱、查找联系信息或批量爬取邮箱地址的场景。
allowed-tools:
  - Read
  - Write
  - StrReplace
  - Shell
  - Glob
---

# 查找电子邮件

这是一个命令行工具（CLI），通过 `crawl4ai` 在本地爬取网站，并从可能包含电子邮件的页面（如“联系我们”、“关于我们”、“支持”等部分）中提取电子邮件地址。

## 设置

1. 安装依赖项：`pip install crawl4ai`
2. 运行脚本：

```bash
python scripts/find_emails.py https://example.com
```

## 快速入门
t
```bash
# Crawl a site
python scripts/find_emails.py https://example.com

# Multiple URLs
python scripts/find_emails.py https://example.com https://other.com

# JSON output
python scripts/find_emails.py https://example.com -j

# Save to file
python scripts/find_emails.py https://example.com -o emails.txt
```

---

## 脚本

### find_emails.py — 爬取并提取电子邮件

```bash
python scripts/find_emails.py <url> [url ...]
python scripts/find_emails.py https://example.com
python scripts/find_emails.py https://example.com -j -o results.json
python scripts/find_emails.py --from-file page.md
```

**参数：**

| 参数          | 描述                                          |
| ----------------- | ---------------------------------------------------- |
| `urls`            | 一个或多个要爬取的 URL                          |
| `-o`, `--output`  | 将结果写入文件                                |
| `-j`, `--json`    | 以 JSON 格式输出（格式示例：`{"emails": {"email": ["path", ...]}}`） |
| `-q`, `--quiet`   | 最小化输出（不显示头部信息，仅显示电子邮件地址）         |
| `--max-depth`     | 最大爬取深度（默认值：2）                         |
| `--max-pages`     | 最大爬取页数（默认值：25）                     |
| `--from-file`     | 从本地 Markdown 文件中提取数据（跳过爬取）        |
| `-v`, `--verbose` | 详细显示爬取过程                                 |

**输出格式（便于阅读）：**

电子邮件按域名分组显示。对于多次爬取同一网站的情况，输出结构会更加清晰：

```
Found 3 unique email(s) across 2 domain(s)

## example.com

  • contact@example.com
    Found on: /contact, /about
  • support@example.com
    Found on: /support

## other.com

  • info@other.com
    Found on: /contact-us
```

**输出格式（JSON）：**

适合大型语言模型（LLM）使用的格式，包含汇总信息及每个域名的详细数据：

```json
{
  "summary": {
    "domains_crawled": 2,
    "total_unique_emails": 3
  },
  "emails_by_domain": {
    "example.com": {
      "emails": {
        "contact@example.com": ["/contact", "/about"],
        "support@example.com": ["/support"]
      },
      "count": 2
    },
    "other.com": {
      "emails": {
        "info@other.com": ["/contact-us"]
      },
      "count": 1
    }
  }
}
```

---

## 配置

编辑 `scripts/url_patterns.json` 以自定义爬取的 URL。只有匹配这些通配符模式的链接才会被包含在爬取范围内：

```json
{
  "url_patterns": [
    "*contact*",
    "*support*",
    "*about*",
    "*team*",
    "*email*",
    "*reach*",
    "*staff*",
    "*inquiry*",
    "*enquir*",
    "*get-in-touch*",
    "*contact-us*",
    "*about-us*"
  ]
}
```

如果该文件缺失或无效，系统将使用默认的爬取规则。

---

## 工作流程

1. **爬取网站**：
   ```bash
   python scripts/find_emails.py https://example.com -o emails.json
   ```

2. **从本地文件中提取数据**（例如，从缓存的 Markdown 文件中提取）：
   ```bash
   python scripts/find_emails.py --from-file crawled.md -j
   ```

3. **通过编辑 `scripts/url_patterns.json` 来自定义 URL 过滤规则**：

---

## 依赖项

```bash
pip install crawl4ai
playwright install
```

本地爬取需要浏览器（Playwright）的支持。

---

## 批量处理

```bash
# Crawl multiple sites – results grouped by domain for clear attribution
python scripts/find_emails.py https://site1.com https://site2.com -j -o combined.json

# Extract from multiple local files
for f in crawled/*.md; do
  echo "=== $f ==="
  python scripts/find_emails.py --from-file "$f" -q
done
```

支持处理多个 URL；输出会明确显示每个电子邮件的来源域名。所有域名都会被统一处理（例如，`www.techbullion.com` 和 `techbullion.com` 会被视为同一个域名），因此不会重复列出。