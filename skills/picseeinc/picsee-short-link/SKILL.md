---
name: picsee-short-link
description: PicSee 是一个 URL 缩短工具，具备二维码生成、数据分析图表以及通过 MCP 服务器进行链接管理的功能。当用户需要缩短 URL、生成二维码、查看数据分析结果、列出或搜索链接时，可以使用该工具。该工具支持两种模式：无需身份验证的模式（仅提供基本的 URL 缩短、二维码生成和数据分析图表功能）和需要身份验证的模式（提供完整的数据分析、链接编辑和搜索功能）。用户生成的令牌会使用 AES-256-CBC 加密技术进行存储。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔗",
        "configPaths": ["skills/picsee-short-link/config.json"],
        "requires": { "bins": ["node", "mcporter"] },
        "externalApis": ["api.pics.ee", "chrome-ext.picsee.tw", "api.qrserver.com", "quickchart.io"],
        "writesPaths": ["skills/picsee-short-link/config.json", "~/.openclaw/.picsee_token", "/tmp/*.png"]
      }
  }
---
# PicSee短链接服务

这是一个URL缩短工具，支持**二维码生成**、**数据分析**以及通过**Model Context Protocol (MCP)服务器**进行链接管理。它允许AI代理（如Claude Code、Cursor、OpenClaw）通过标准化的工具调用直接使用PicSee的功能。

---

## 首次设置

### OpenClaw

执行以下命令来注册MCP服务器（只需注册一次）：
```bash
mcporter config add picsee stdio -- node ~/.openclaw/workspace/skills/picsee-short-link/mcp-server/dist/index.js
```

验证注册结果：
```bash
mcporter config list | grep picsee
```

### ClawHub

通过ClawHub CLI进行安装：
```bash
clawhub install picsee-short-link
```

MCP服务器的注册过程会自动完成。

---

## 使用方法

### 基本缩短功能
```bash
mcporter call picsee.shorten_url url="https://example.com/long-url"
```

### 使用自定义链接别名
```bash
mcporter call picsee.shorten_url url="https://example.com" encodeId="mylink"
```

### 生成二维码
```bash
mcporter call picsee.generate_qr_code shortUrl="https://pse.is/mylink" size=300
```

### 查看分析数据
```bash
mcporter call picsee.get_analytics encodeId="mylink"
```

### 生成数据分析图表
```bash
mcporter call picsee.generate_analytics_chart \
  dailyClicks='[{"date":"3/1","clicks":45},{"date":"3/2","clicks":67}]' \
  encodeId="mylink"
```

### 列出最近生成的链接
```bash
mcporter call picsee.list_links startTime="2026-03-31T23:59:59" limit=10
```

---

## MCP工具参考

### `shorten_url`

用于缩短URL。系统会自动检测认证模式：如果已存储API密钥，则使用带高级功能的`api.pics.ee`接口；否则使用未经认证的`chrome-ext.picsee.tw`接口。

**参数：**
- `url` (字符串，**必填**): 需要缩短的URL
- `encodeId` (字符串): 自定义链接别名（3-90个字符）
- `domain` (字符串): 短链接的域名（默认：`pse.is`)
- `title` (字符串): 自定义预览标题（高级计划）
- `description` (字符串): 自定义预览描述（高级计划）
- `imageUrl` (字符串): 自定义预览缩略图（高级计划）
- `tags` (字符串[]): 用于组织链接的标签（高级计划）
- `utm` (对象): `{source, medium, campaign, term, content}` (高级计划)

**返回值：`{ success, shortUrl, encodeId, mode }`

---

### `generate_qr_code`

为任意短链接生成二维码。**仅当用户明确请求时使用此功能**。系统会自动通过PicSee生成二维码，并且不会消耗任何配额。

**参数：**
- `shortUrl` (字符串，**必填**): 需要生成二维码的短链接
- `size` (数字): 二维码的尺寸（以像素为单位，100-1000，默认值：300）

**返回值：`{ success, qrCodeUrl, originalQrUrl, shortUrl, size, note }`

**示例：**
```bash
mcporter call picsee.generate_qr_code shortUrl="https://pse.is/mylink" size=300
```

---

### `get_analytics`

用于查看短链接的点击统计数据。**需要认证。**

**参数：**
- `encodeId` (字符串，**必填**): 短链接的别名（例如：`pse.is/abc123`中的`abc123`）

**返回值：`{ success, data: { totalClicks, uniqueClicks, dailyClicks[] } }`

---

### `generate_analytics_chart`

用于生成每日点击趋势的折线图。**仅当用户明确请求时使用此功能**。系统会自动通过PicSee生成图表，并且不会消耗任何配额。

**参数：**
- `dailyClicks` (数组，**必填**): 包含`date, clicks`的对象数组。日期格式为`YYYY-MM-DD`或`MM/DD`
- `encodeId` (字符串): 链接的别名（用于图表标题）

**返回值：`{ success, chartUrl, originalChartUrl, dataPoints, note }`

**示例：**
```bash
mcporter call picsee.generate_analytics_chart \
  dailyClicks='[{"date":"3/1","clicks":45},{"date":"3/2","clicks":67}]' \
  encodeId="mylink"
```

---

### `list_links`

用于列出和搜索链接。**需要认证**。结果按时间倒序返回（最新链接在前）。

**参数：**
- `startTime` (字符串，**必填**): 查询的起始时间。格式为`YYYY-MM-DDTHH:MM:SS`（例如：`2026-03-31T23:59:59`表示2026年3月31日）
- `limit` (数字): 每页显示的链接数量（1-50，默认值：50）
- `isAPI` (布尔值): 仅过滤API生成的链接
- `isStar` (布尔值): 仅过滤星标链接
- `prevMapId` (字符串): 分页游标——用于过滤早于该ID的链接
- `externalId` (字符串): 通过外部ID进行过滤
- `keyword` (字符串): 通过标题/描述进行搜索（高级功能，3-30个字符）
- `tag` (字符串): 通过标签进行过滤（高级功能）
- `url` (字符串): 通过目标URL进行过滤
- `encodeId` (字符串): 通过链接别名进行过滤
- `authorId` (字符串): 通过作者ID进行过滤

**返回值：`{ success, data: [{ encodeId, domain, url, title, totalClicks, uniqueClicks, createTime, tags, utm }] }`

**常见错误：** 使用月份的第一天作为起始时间（例如`2026-03-01`）会导致错过该月的大部分数据。请始终使用该月的最后一天。**

---

### `edit_link`

用于编辑现有的短链接。**需要认证且需使用高级计划**。仅包括需要修改的字段。

**参数：**
- `originalEncodeId` (字符串，**必填**): 需要编辑的链接的当前别名
- `url` (字符串): 新的目标URL
- `encodeId` (字符串): 新的链接别名
- `domain` (字符串): 新的域名
- `title` (字符串): 新的预览标题
- `description` (字符串): 新的预览描述
- `imageUrl` (字符串): 新的预览缩略图
- `tags` (字符串[]): 新的标签
- `fbPixel` (字符串): Meta Pixel ID
- `gTag` (字符串): Google Tag Manager ID
- `utm` (对象): 新的UTM参数
- `expireTime` (字符串): 链接的有效期限（ISO 8601格式）

**返回值：`{ success, message }`

---

### `delete_link`

用于删除或恢复短链接。**需要认证。**

**参数：**
- `encodeId` (字符串，**必填**): 短链接的别名
- `action` (字符串): `"delete"`（默认）或`"recover"`（恢复）

**返回值：`{ success, message }`

---

### `setup_auth`

用于存储和验证PicSee API密钥。密钥使用AES-256-CBC算法进行加密（加密密钥为机器特定的组合：主机名 + 用户名 → SHA-256），并保存在`~/.openclaw/.picsee_token`文件中。

**参数：**
- `token` (字符串，**必填**): PicSee API密钥

**返回值：`{ success, plan, quota, usage, message }`

**获取密钥的途径：** https://picsee.io/ → 设置 → API → 复制密钥

---

## 认证模式

| 认证模式 | API主机 | 支持的功能 |
|------|----------|----------|
| **未经认证** | `chrome-ext.picsee.tw` | 仅支持创建短链接 |
| **已认证** | `api.pics.ee` | 支持创建、数据分析、列表查看、搜索和编辑链接 |

**自动检测：** 如果`~/.openclaw/.picsee_token`文件中存在加密密钥，则使用已认证模式；否则使用未经认证的模式。

`config.json`文件用于记录用户的认证模式偏好设置：
```json
{ "mode": "authenticated", "setupDate": "2026-03-04" }
```

---

## 安全性

- **密钥加密**：使用AES-256-CBC算法进行加密，IV（初始化向量）与密文一起存储（格式：`iv_hex:ciphertext_hex`）
- **密钥生成**：使用`SHA-256hostname + "-" + username`的方式生成密钥（基于机器特定信息，无共享密钥）
- **文件权限**：对密钥文件设置权限为`0600`
- **不存储明文形式的密钥**

---

## 错误处理

| 错误情况 | 返回信息 |
|----------|----------|
| 未提供密钥且需要认证 | “此操作需要认证。请使用`setup_auth`函数获取PicSee API密钥。” |
| 使用非高级计划尝试编辑链接 | “编辑链接需要高级计划。请创建一个新的链接。” |
| 无效的密钥 | “密钥无效。请访问https://picsee.io/ → 设置 → API获取新的密钥。” |

---

## 代理脚本示例（OpenClaw）

这些脚本不属于MCP工具，而是代理在从上述工具获取结果后执行的后续操作。使用`exec`命令来执行相应的curl请求。

### 二维码生成

**在成功缩短URL后**，主动询问用户：“您是否需要为这个短链接生成二维码？”

如果用户同意，生成二维码：

```bash
curl -s -o /tmp/<ENCODE_ID>_qr.png "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://pse.is/<ENCODE_ID>"
```

通过`message`工具发送二维码文件，文件路径为`"/tmp/<ENCODE_ID>_qr.png"`。

### 数据分析图表

**在调用`get_analytics`并显示点击统计数据后**，主动询问用户：“您是否希望查看每日点击量的图表？”

如果用户同意，生成图表：

1. 从响应中提取`dailyClicks`数组
2. 使用这些数据生成图表文件：

```bash
# Example with 3 data points — construct dynamically from actual dailyClicks
curl -s -o /tmp/<ENCODE_ID>_chart.png "https://quickchart.io/chart?w=600&h=300&c=\
{type:'line',data:{labels:['3/1','3/2','3/3'],datasets:[{label:'Clicks',data:[45,67,23],borderColor:'rgb(59,130,246)',fill:false}]}}"
```

通过`message`工具发送图表文件，文件路径为`"/tmp/<ENCODE_ID>_chart.png"`。