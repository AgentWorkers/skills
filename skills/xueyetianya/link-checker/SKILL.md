# link-checker

这是一个用于检测失效链接的工具，它会爬取网页并检查所有超链接是否存在HTTP错误（如404“未找到”）、重定向（如301/302）、超时或连接失败等问题。工具会生成详细的报告，其中包含状态码、响应时间和链接地址等信息。支持递归爬取（可控制深度）、域名过滤以及多种输出格式。该工具基于Python3的urllib库开发，无需依赖任何外部库。对于网站维护、SEO优化和质量控制来说，这是一个非常实用的工具。

由BytesAgain提供支持 | bytesagain.com | hello@bytesagain.com

## 命令

| 命令 | 描述 |
|---------|-------------|
| `check <url>` | 检查单个页面上的所有链接 |
| `crawl <url>` | 递归爬取并检查所有链接 |
| `report <url>` | 生成完整的HTML报告 |
| `broken <url>` | 仅显示失效的链接 |
| `redirects <url>` | 仅显示被重定向的链接 |
| `external <url>` | 仅检查外部链接 |
| `internal <url>` | 仅检查内部链接 |
| `batch <file>` | 批量检查多个页面上的链接 |
| `summary <url>` | 快速生成链接统计摘要 |

## 选项

- `--depth <n>` | 递归爬取的深度（默认值：1） |
- `--timeout <seconds>` | 每个链接的请求超时时间（默认值：10秒） |
- `--format text|json|csv|html` | 输出格式（默认值：text） |
- `--output <file>` | 将报告保存到文件 |
- `--concurrent <n>` | 同时进行的检查任务数量（默认值：5） |
- `--internal-only` | 仅检查内部链接 |
- `--external-only` | 仅检查外部链接 |
- `--exclude <pattern>` | 排除匹配指定模式的URL |
- `--verbose` | 显示所有链接（包括正常的链接） |
- `--quiet` | 仅显示失效的链接 |
- `--user-agent <string>` | 自定义User-Agent头信息 |

## 示例

```bash
# Check all links on a page
bash scripts/main.sh check https://example.com

# Find only broken links
bash scripts/main.sh broken https://example.com --format json

# Recursive crawl with depth limit
bash scripts/main.sh crawl https://example.com --depth 2 --internal-only

# Generate HTML report
bash scripts/main.sh report https://example.com --output link-report.html

# Check external links only with custom timeout
bash scripts/main.sh external https://example.com --timeout 15

# Quick summary
bash scripts/main.sh summary https://example.com
```

## 状态分类

| 分类 | 状态码 | 描述 |
|----------|-------------|-------------|
| ✅ 正常 | 200, 204 | 链接可用 |
| 🔄 重定向 | 301, 302, 307, 308 | 链接已被重定向 |
| ❌ 失效 | 404, 410 | 链接已失效 |
| ⚠️ 错误 | 403, 500, 502, 503 | 服务器错误 |
| ⏱️ 超时 | — | 连接超时 |
| 🚫 失败 | — | 连接失败或DNS解析失败 |