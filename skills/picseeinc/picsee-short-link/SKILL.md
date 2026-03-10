---
name: picsee-short-link
description: PicSee 是一个 URL 缩短工具，具备二维码生成、数据分析图表以及通过 CLI（命令行接口）进行链接管理的功能。当用户需要缩短 URL、生成二维码、查看数据分析结果、列出或搜索链接时，可以使用该工具。该工具支持两种模式：无需认证的模式（仅提供基本的 URL 缩短、二维码生成和数据分析图表功能）和需要认证的模式（提供完整的数据分析、链接编辑和搜索功能）。用户数据通过 AES-256-CBC 加密技术进行存储。
license: MIT
compatibility: Requires Node.js >= 18. Network access to api.pics.ee, chrome-ext.picsee.tw, api.qrserver.com, quickchart.io.
metadata:
  author: picsee
  version: "2.0.1"
  emoji: "🔗"
  openclaw-configPaths: "skills/picsee-short-link/config.json"
  openclaw-requires: "node"
  openclaw-writesPaths: "skills/picsee-short-link/config.json, ~/.openclaw/.picsee_token, ~/.openclaw/.picsee_salt, skills/picsee-short-link/tmp/*.png"
---
# PicSee 短链接服务

这是一个用于缩短 URL 的工具，支持 **二维码生成**、**数据分析** 以及通过 **命令行界面 (CLI)** 进行链接管理。该服务可与任何能够执行 shell 命令的代理程序配合使用（例如 OpenClaw、Claude Code、Codex 等）。

---

## 命令行界面 (CLI) 路径

```
node ~/.openclaw/workspace/skills/picsee-short-link/cli/dist/cli.js
```

为简洁起见，以下示例中使用了 `picsee` 作为别名。

---

## 快速参考

### 缩短 URL
```bash
picsee shorten "https://example.com/long-url"
picsee shorten "https://example.com" --slug mylink
picsee shorten "https://example.com" --slug mylink --domain pse.is --title "My Title" --tags seo,marketing
```

### 数据分析
```bash
picsee analytics mylink
```

### 生成数据分析图表
```bash
picsee chart mylink
```
该命令会获取分析数据，并返回一个可视化每日点击次数的图表链接（QuickChart）。

### 生成二维码
```bash
picsee qr "https://pse.is/mylink"
picsee qr "https://pse.is/mylink" --size 500
```

### 列出所有链接
```bash
picsee list
picsee list --limit 10
picsee list --start "2026-03-31T23:59:59" --keyword "campaign"
picsee list --tag seo --starred
```

`--start` 参数可用于从指定时间点开始反向查询（默认为当前时间）。例如：`2026-03-31T23:59:59` 表示从 2026 年 3 月 31 日开始查询。

### 编辑链接
```bash
picsee edit mylink --url "https://new-destination.com"
picsee edit mylink --slug newslug --title "New Title" --tags a,b,c
```
此功能需要高级计划才能使用。

### 删除/恢复链接
```bash
picsee delete mylink
picsee recover mylink
```

### 认证
```bash
picsee auth <token>
picsee auth-status
```
获取 token 的方法：访问 https://picsee.io → 选择头像 → 进入“设置” → “API” → 复制 token。

### 帮助文档
```bash
picsee help
```

---

## 完整参数选项

### `shorten` 命令
| 参数 | 说明 |
|------|-------------|
| `--slug <slug>` | 自定义短链接的 slug（3-90 个字符） |
| `--domain <domain>` | 短链接的域名（默认：`pse.is`） |
| `--title <title>` | 预览链接的标题（高级计划） |
| `--desc <desc>` | 预览链接的描述（高级计划） |
| `--image <url>` | 预览链接的缩略图（高级计划） |
| `--tags t1,t2` | 用逗号分隔的标签（高级计划） |
| `--utm s:m:c:t:n` | UTM 参数（来源、媒介、活动、关键词、内容） |

### `list` 命令
| 参数 | 说明 |
|------|-------------|
| `--start <time>` | 从指定时间点开始反向查询（默认为当前时间） |
| `--limit <n>` | 每页显示的结果数量（1-50，默认为 50） |
| `--keyword <kw>` | 根据标题或描述进行搜索（高级计划，3-30 个字符） |
| `--tag <tag>` | 根据标签进行过滤（高级计划） |
| `--url <url>` | 根据目标 URL 进行过滤 |
| `--slug <slug>` | 根据 slug 进行过滤 |
| `--starred` | 仅显示被标记的链接 |
| `--api-only` | 仅显示通过 API 生成的链接 |
| `--cursor <mapId>` | 分页查询的当前位置 |

### `edit` 命令
| 参数 | 说明 |
|------|-------------|
| `--url <url>` | 新的目标 URL |
| `--slug <slug>` | 新的短链接 slug |
| `--domain <domain>` | 新的域名 |
| `--title <title>` | 新的链接标题 |
| `--desc <desc>` | 新的链接描述 |
| `--image <url>` | 新的链接缩略图 |
| `--tags t1,t2` | 新的标签 |
| `--expire <iso>` | 链接的有效期限（ISO 8601 格式） |

---

## 认证方式

| 认证方式 | API 主机 | 可用功能 |
|------|----------|----------|
| **未认证** | `chrome-ext.picsee.tw` | 仅支持创建短链接 |
| **认证** | `api.pics.ee` | 支持创建短链接、数据分析、查询、编辑和删除链接 |

系统会自动检测：如果 `~/.openclaw/.picsee_token` 文件中存在加密过的 token，则使用认证模式。

---

## 安全性措施

- **Token 加密**：使用 AES-256-CBC 算法进行加密，IV（初始化向量）与密文一起存储。
- **密钥生成**：使用 `SHA-256(random-salt + hostname + "-" + username)` 的公式生成密钥；其中 32 字节的随机盐值仅生成一次并存储在 `~/.openclaw/.picsee_salt` 文件中（设置模式为 `0600`），即使知道主机名和用户名也无法预测密钥。
- **文件权限**：token 和 salt 文件的权限设置为 `0600`。

---

## 代理程序使用说明（后续处理）

### 将二维码下载为图片

执行 `picsee qr` 命令后，可以下载并发送二维码图片：

```bash
mkdir -p ~/.openclaw/workspace/skills/picsee-short-link/tmp
curl -s -o ~/.openclaw/workspace/skills/picsee-short-link/tmp/<ENCODE_ID>_qr.png "<originalQrUrl>"
```

使用 `message` 工具发送图片，路径为：`filePath: "~/.openclaw/workspace/skills/picsee-short-link/tmp/<ENCODE_ID>_qr.png"`。

### 将数据分析图表下载为图片

执行 `picsee chart` 命令后，可以下载并发送图表图片：

```bash
mkdir -p ~/.openclaw/workspace/skills/picsee-short-link/tmp
curl -s -o ~/.openclaw/workspace/skills/picsee-short-link/tmp/<ENCODE_ID>_chart.png "<originalChartUrl>"
```

使用 `message` 工具发送图片，路径为：`filePath: "~/.openclaw/workspace/skills/picsee-short-link/tmp/<ENCODE_ID>_chart.png"`。