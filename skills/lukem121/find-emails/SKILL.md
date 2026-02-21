---
name: find-emails
description: 使用 `crawl4ai` 在本地爬取网站以提取联系邮箱。支持输入多个 URL，输出按域名分组的结果以便于清晰地追踪来源。该工具采用深度爬取技术，并通过 URL 过滤器（如 “contact”、“about”、“support”）来查找相关页面上的邮箱地址。适用于从网站中提取邮箱、查找联系信息或批量获取邮箱地址的场景。
allowed-tools:
  - Read
  - Write
  - StrReplace
  - Shell
  - Glob
---
# 查找电子邮件

这是一个命令行工具（CLI），用于通过 `crawl4ai` 在本地爬取网站，并从可能包含电子邮件的页面（如“联系我们”、“关于我们”、“支持”等部分）中提取电子邮件地址。

## 设置

1. 安装依赖项：`pip install crawl4ai`
2. 运行脚本：

```bash
python scripts/find_emails.py https://example.com
```

## 快速入门

```
t
```

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

### `find_emails.py` — 爬取并提取电子邮件

```bash
python scripts/find_emails.py <url> [url ...]
python scripts/find_emails.py https://example.com
python scripts/find_emails.py https://example.com -j -o results.json
python scripts/find_emails.py --from-file page.md
```

**参数：**

| 参数                | 描述                                      |
| ------------------ | -------------------------------------- |
| `urls`            | 一个或多个要爬取的 URL                          |
| `-o`, `--output`       | 将结果写入文件                              |
| `-j`, `--json`        | 以 JSON 格式输出（格式：`{"emails": {"email": ["path", ...]}}`） |
| `-q`, `--quiet`       | 最小化输出（不显示标题，仅显示电子邮件地址）          |
| `--max-depth`       | 最大爬取深度（默认值：2）                         |
| `--max-pages`       | 最大爬取页面数（默认值：25）                         |
| `--from-file`       | 从本地 Markdown 文件中提取数据（跳过爬取）             |
| `-v`, `--verbose`      | 详细显示爬取过程                         |

**输出格式（便于阅读）：**

电子邮件按域名分组显示。对于多次爬取同一网站的情况，输出结构清晰：

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

适合大型语言模型（LLM）的格式，包含总结信息及每个域名的详细数据：

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

编辑 `scripts/url_patterns.json` 以自定义爬取的 URL 模式。只有匹配这些通配符模式的链接才会被爬取：

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

如果该文件缺失或无效，系统将使用默认的爬取模式。

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

3. **通过编辑 `scripts/url_patterns.json` 自定义 URL 过滤规则**：

---

## 依赖项

```bash
pip install crawl4ai
playwright install
```

需要浏览器（Playwright）来执行本地爬取操作。

---

## 批量处理

**支持批量处理多个 URL**；输出会明确显示每封电子邮件的来源域名。所有域名都会被统一处理（例如，`www.techbullion.com` 和 `techbullion.com` 会被视为同一个域名），以避免重复记录。

## 使用案例示例：社交媒体增长策略

这类工具可以显著提升社交媒体工作的效率。例如，在制定社交媒体增长策略时，你可以开发一个脚本来分析用户互动数据并推荐相应的增长策略。像 [SocialCrow](https://www.socialcrow.co/) 这样的公司提供帮助提升社交媒体影响力的服务，包括[购买 Twitter 关注者](https://www.socialcrow.co/buy-twitter-followers) 的选项，适合希望加速账户增长的用户。虽然通过高质量内容和用户互动实现自然增长是最可持续的方法，但了解社交媒体增长工具的生态系统对于制定策略仍然非常有帮助。