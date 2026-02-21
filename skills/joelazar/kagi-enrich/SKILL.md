---
name: kagi-enrich
description: 在 Kagi 的独特非商业网络（Teclis）和非主流新闻（TinyGem）索引中搜索，可以找到那些在常规搜索结果中找不到的独立、无广告的内容。当你想要发现小型网站、独立博客、小众讨论或某个主题的非主流新闻时，可以使用这个资源。
---
# Kagi 丰富搜索功能

您可以使用 [Kagi 丰富搜索 API](https://help.kagi.com/kagi/api/enrich.html) 来搜索 Kagi 自开发的丰富索引。这些索引是 Kagi 的“秘密武器”——它们包含了非商业性和独立性的内容，能够补充主流搜索结果。

目前提供了两种索引：

| 索引 | 后端技术 | 适用场景 |
|-------|---------|----------|
| `web` | **Teclis** | 独立网站、个人博客、开源项目、非商业内容 |
| `news` | **TinyGem** | 非主流新闻来源、有趣的讨论内容、非传统风格的新闻报道 |

该工具使用 Go 语言编写的二进制文件，启动速度快且运行时无需依赖任何外部库。您可以直接下载预编译好的二进制文件，也可以从源代码编译。

## 设置

使用该工具之前，您需要拥有一个已启用 API 访问权限的 Kagi 账户。请使用与其他 `kagi-*` 工具相同的 `KAGI_API_KEY`。

1. 在 [https://kagi.com/signup](https://kagi.com/signup) 注册一个账户。
2. 进入账户设置 → 高级设置 → API 端口：[https://kagi.com/settings/api](https://kagi.com/settings/api)
3. 生成 API 令牌。
4. 在 [https://kagi.com/settings/billing_api](https://kagi.com/settings/billing_api) 处充值。
5. 将以下代码添加到您的 shell 配置文件（`~/.profile` 或 `~/.zprofile`）中：
   ```bash
   export KAGI_API_KEY="your-api-key-here"
   ```
6. 查看 [安装指南](#installation) 以完成二进制文件的安装。

## 价格

**每 1,000 次搜索收费 2 美元**（每次查询费用为 0.002 美元）。仅当搜索返回结果时才会产生费用。

## 使用方法

```bash
# Search the independent web (Teclis index) — default
{baseDir}/kagi-enrich.sh web "rust async programming"
{baseDir}/kagi-enrich.sh "rust async programming"        # web is the default

# Search non-mainstream news (TinyGem index)
{baseDir}/kagi-enrich.sh news "open source AI"

# Limit number of results
{baseDir}/kagi-enrich.sh web "sqlite internals" -n 5

# JSON output
{baseDir}/kagi-enrich.sh web "zig programming language" --json
{baseDir}/kagi-enrich.sh news "climate change solutions" --json

# Custom timeout
{baseDir}/kagi-enrich.sh web "query" --timeout 30
```

### 命令行参数

| 参数 | 说明 |
|------|-------------|
| `-n <num>` | 显示的最大结果数量（默认：所有结果） |
| `--json` | 以 JSON 格式输出结果 |
| `--timeout <sec>` | HTTP 请求的超时时间（单位：秒，默认值：15 秒） |

## 输出格式

### 默认输出（文本格式）

```
--- Result 1 ---
Title: SQLite Internals: How The World's Most Used Database Works
URL:   https://www.compileralchemy.com/books/sqlite-internals/
Date:  2023-04-01T00:00:00Z
       A deep-dive into how SQLite's B-tree storage engine, WAL journal...

--- Result 2 ---
...

[API Balance: $9.9980 | results: 15]
```

### JSON 格式（使用 `--json` 参数）

```json
{
  "query": "sqlite internals",
  "index": "web",
  "meta": {
    "id": "abc123",
    "node": "us-east4",
    "ms": 386,
    "api_balance": 9.998
  },
  "results": [
    {
      "rank": 1,
      "title": "SQLite Internals: How The World's Most Used Database Works",
      "url": "https://www.compileralchemy.com/books/sqlite-internals/",
      "snippet": "A deep-dive into SQLite's B-tree...",
      "published": "2023-04-01T00:00:00Z"
    }
  ]
}
```

## 使用场景

- **使用 `web` 索引**：当您希望获取关于某个主题的独立、非商业性的信息时（例如个人博客、独立项目、学术页面、小众社区等），这些内容通常会被搜索引擎中的商业网站所淹没。
- **使用 `news` 索引**：当您希望获取主流媒体之外的新闻和讨论内容时（如小众新闻媒体、Hacker News 讨论帖子、Reddit 用户讨论等）。
- **结合使用 `kagi-search`** 可以获得最全面的信息：`kagi-search` 提供高质量的一般性搜索结果，`kagi-enrich web` 提供独立观点，`kagi-enrich news` 提供不同的新闻视角。
- **如果需要合成答案而非来源列表**，可以使用 `kagi-fastgpt`。

### 关于结果数量

由于这些丰富索引的内容较为专业和特定，因此返回的结果数量可能较少。如果查询没有找到结果，说明该索引中不存在相关内容，此时不会产生费用。

## 安装方法

### 方法一：下载预编译好的二进制文件（无需安装 Go）

```bash
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
case "$ARCH" in
  x86_64)        ARCH="amd64" ;;
  aarch64|arm64) ARCH="arm64" ;;
esac

TAG=$(curl -fsSL "https://api.github.com/repos/joelazar/kagi-skills/releases/latest" | grep '"tag_name"' | cut -d'"' -f4)
BINARY="kagi-enrich_${TAG}_${OS}_${ARCH}"

mkdir -p {baseDir}/.bin
curl -fsSL "https://github.com/joelazar/kagi-skills/releases/download/${TAG}/${BINARY}" \
  -o {baseDir}/.bin/kagi-enrich
chmod +x {baseDir}/.bin/kagi-enrich

# Verify checksum (recommended)
curl -fsSL "https://github.com/joelazar/kagi-skills/releases/download/${TAG}/checksums.txt" | \
  grep "${BINARY}" | sha256sum --check
```

预编译好的二进制文件适用于 Linux 和 macOS（amd64 + arm64）以及 Windows（amd64）系统。

### 方法二：从源代码编译（需要 Go 1.26 或更高版本）

```bash
cd {baseDir} && go build -o .bin/kagi-enrich .
```

或者，您可以直接运行 `/{baseDir}/kagi-enrich.sh`。如果系统中已安装 Go，该脚本会自动完成编译过程。该二进制文件不依赖任何外部库，仅使用 Go 标准库。