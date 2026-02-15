---
name: scraper
description: 从 Notion、DocSend、PDF 文件以及其他来源抓取文档，并将其转换为本地 PDF 文件。适用于用户需要下载、归档或将网页文档转换为 PDF 格式的情况。支持对受保护文档的认证流程，并通过用户配置文件实现会话持久化。返回已下载 PDF 文件的本地路径。
---

# docs-scraper

这是一个命令行工具（CLI），通过浏览器自动化从各种来源抓取文档，并将它们转换为本地PDF文件。

## 安装

```bash
npm install -g docs-scraper
```

## 快速入门

将任何文档URL抓取为PDF文件：

```bash
docs-scraper scrape https://example.com/document
```

生成的PDF文件将保存在本地路径：`~/.docs-scraper/output/1706123456-abc123.pdf`

## 基本使用方法

- **使用守护进程进行抓取**（推荐，可保持浏览器会话活跃）：
```bash
docs-scraper scrape <url>
```

- **使用指定配置文件进行抓取**（适用于需要身份验证的网站）：
```bash
docs-scraper scrape <url> -p <profile-name>
```

- **使用预填充的数据进行抓取**（例如，用于DocSend服务的数据）：
```bash
docs-scraper scrape <url> -D email=user@example.com
```

- **直接模式**（一次性抓取，不使用守护进程）：
```bash
docs-scraper scrape <url> --no-daemon
```

## 身份验证流程

当文档需要身份验证（登录、电子邮件验证或密码输入）时：

1. 初始抓取会返回一个作业ID：
   ```bash
   docs-scraper scrape https://docsend.com/view/xxx
   # Output: Scrape blocked
   #         Job ID: abc123
   ```

2. 使用正确的凭证重新尝试抓取：
   ```bash
   docs-scraper update abc123 -D email=user@example.com
   # or with password
   docs-scraper update abc123 -D email=user@example.com -D password=1234
   ```

## 配置文件管理

配置文件用于存储身份验证所需的会话cookie。

```bash
docs-scraper profiles list     # List saved profiles
docs-scraper profiles clear    # Clear all profiles
docs-scraper scrape <url> -p myprofile  # Use a profile
```

## 守护进程管理

守护进程会保持浏览器实例的活跃状态，以加快抓取速度。

```bash
docs-scraper daemon status     # Check status
docs-scraper daemon start      # Start manually
docs-scraper daemon stop       # Stop daemon
```

注意：运行抓取命令时，守护进程会自动启动。

## 清理

抓取到的PDF文件存储在`~/.docs-scraper/output/`目录下。守护进程会自动删除超过1小时的旧文件。

- 手动清理文件：
```bash
docs-scraper cleanup                    # Delete all PDFs
docs-scraper cleanup --older-than 1h    # Delete PDFs older than 1 hour
```

## 作业管理

```bash
docs-scraper jobs list         # List blocked jobs awaiting auth
```

## 支持的来源类型

- **直接PDF链接**：直接下载PDF文件
- **Notion页面**：将Notion页面内容导出为PDF
- **DocSend文档**：处理DocSend平台的文档
- **LLM备用抓取器**：使用Claude API抓取其他网页内容

---

## 抓取器参考

每个抓取器都支持特定的`-D`参数来指定数据字段。请根据URL类型选择合适的参数。

### DirectPdfScraper

- **支持的URL格式**：以`.pdf`结尾的URL
- **需要提供的数据字段**：无（直接下载PDF文件）
- **示例**：
```bash
docs-scraper scrape https://example.com/document.pdf
```

---

### DocsendScraper

- **支持的URL格式**：`docsend.com/view/*`、`docsend.com/v/*`及其子域名（例如`org-a.docsend.com`）
- **URL模式**：
  - 文档：`https://docsend.com/view/{id}` 或 `https://docsend.com/v/{id}`
  - 文件夹：`https://docsend.com/view/s/{id}`
  - 子域名：`https://{subdomain}.docsend.com/view/{id>`
- **需要提供的数据字段**：
  | 字段 | 类型 | 说明 |
  |-------|------|-------------|
  | `email` | email | 访问文档所需的电子邮件地址 |
  | `password` | 密码 | 保护文档所需的密码 |
  | `name` | text | （针对需要NDA协议的文档）您的姓名 |
- **示例**：
```bash
# Pre-fill email for DocSend
docs-scraper scrape https://docsend.com/view/abc123 -D email=user@example.com

# With password protection
docs-scraper scrape https://docsend.com/view/abc123 -D email=user@example.com -D password=secret123

# With NDA name requirement
docs-scraper scrape https://docsend.com/view/abc123 -D email=user@example.com -D name="John Doe"

# Retry blocked job
docs-scraper update abc123 -D email=user@example.com -D password=secret123
```

**注意**：
  - DocSend可能需要提供电子邮件、密码或姓名中的任意组合
  - 文件夹内容会被抓取为包含文档链接的PDF文件
  - 提供姓名后，抓取器会自动勾选NDA协议相关的复选框

---

### NotionScraper

- **支持的URL格式**：`notion.so/*`、`*.notion.site/*`
- **需要提供的数据字段**：
  | 字段 | 类型 | 说明 |
  |-------|------|-------------|
  | `email` | Notion账户的电子邮件地址 |
  | `password` | Notion账户的密码 |
- **示例**：
```bash
# Public page (no auth needed)
docs-scraper scrape https://notion.so/Public-Page-abc123

# Private page with login
docs-scraper scrape https://notion.so/Private-Page-abc123 \
  -D email=user@example.com -D password=mypassword

# Custom domain
docs-scraper scrape https://docs.company.notion.site/Page-abc123
```

**注意**：
  - 公开的Notion页面无需身份验证
  - 生成PDF文件前会自动展开可折叠的内容块
  - 使用会话配置文件来保持登录状态

---

### LlmFallbackScraper

- **支持的URL格式**：其他抓取器无法处理的URL
- **数据字段**：由Claude API动态生成
  LLM抓取器会分析页面HTML内容，检测以下内容：
  - 登录表单（动态提取字段名称）
  - Cookie广告（自动关闭）
  - 可展开的内容（自动展开）
  - CAPTCHA验证码（标记为无法访问）
  - 广告墙（标记为无法访问）
- **常见的动态字段**：
  | 字段 | 类型 | 说明 |
  |-------|------|-------------|
  | `email` | （如果存在）登录所需的电子邮件地址 |
  | `password` | （如果存在）登录所需的密码 |
  | `username` | （如果使用用户名登录）用户名 |
- **示例**：
```bash
# Generic webpage (no auth)
docs-scraper scrape https://example.com/article

# Webpage requiring login
docs-scraper scrape https://members.example.com/article \
  -D email=user@example.com -D password=secret

# When blocked, check the job for required fields
docs-scraper jobs list
# Then retry with the fields the scraper detected
docs-scraper update abc123 -D username=myuser -D password=secret
```

**注意**：
  - 需要设置`ANTHROPIC_API_KEY`环境变量
  - 字段名称会根据页面上的实际表单字段提取
  - 允许最多2次登录尝试，超过次数后将失败
  - CAPTCHA验证码需要手动处理

## 数据字段总结

| 抓取器 | email | password | name | 其他字段 |
|---------|-------|----------|------|-------|
| DirectPdf | - | - | - | - |
| DocSend | ✓ | ✓ | ✓ | - |
| Notion | ✓ | ✓ | - | - |
| LLM Fallback | ✓* | ✓* | - | 动态生成* |

*某些字段会根据页面内容动态生成*

## 环境配置（可选）

仅适用于LLM备用抓取器：

```bash
export ANTHROPIC_API_KEY=your_key
```

**可选的浏览器设置**：
```bash
export BROWSER_HEADLESS=true   # Set false for debugging
```

## 常用操作

- **归档Notion页面**：
```bash
docs-scraper scrape https://notion.so/My-Page-abc123
```

- **下载受保护的DocSend文档**：
```bash
docs-scraper scrape https://docsend.com/view/xxx
# If blocked:
docs-scraper update <job-id> -D email=user@example.com -D password=1234
```

- **使用配置文件批量抓取**：
```bash
docs-scraper scrape https://site.com/doc1 -p mysite
docs-scraper scrape https://site.com/doc2 -p mysite
```

## 抓取结果

- **成功**：生成的PDF文件路径（例如：`~/.docs-scraper/output/1706123456-abc123.pdf`）
- **失败**：显示作业ID及所需的认证信息

## 故障排除

- **超时**：执行`docs-scraper daemon stop`并重新启动守护进程
- **身份验证失败**：查看`docs-scraper jobs list`以查看待处理的作业
- **磁盘空间不足**：执行`docs-scraper cleanup`以清除旧PDF文件