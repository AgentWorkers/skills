---
name: picsee-short-link
description: PicSee 提供 URL 缩短服务以及通过 MCP 服务器或 CLI 脚本进行链接管理的功能。当用户需要缩短 URL、查看链接分析数据、列出/搜索链接或提及 PicSee 时，可以使用该服务。该服务支持两种模式：无需认证的模式（仅提供基本的 URL 缩短功能）和需要认证的模式（支持链接分析、编辑和搜索功能）。存储的令牌采用 AES-256-CBC 加密算法进行保护。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔗",
        "configPaths": ["skills/picsee-short-link/config.json"],
        "requires": { "bins": ["node"] },
        "externalApis": ["api.pics.ee", "chrome-ext.picsee.tw", "api.qrserver.com", "quickchart.io"],
        "writesPaths": ["skills/picsee-short-link/config.json", "~/.openclaw/.picsee_token", "/tmp/*.png"]
      }
  }
---
# PicSee短链接服务

这是一个提供URL缩短、分析、搜索和链接管理的工具。支持两种使用方式：

- **MCP服务器**（推荐用于Claude Code、Cursor、OpenClaw的mcporter插件）  
- **CLI脚本**（旧版本，但仍可使用）

---

## MCP服务器

入口文件：`skills/picsee-short-link/mcp-server/dist/index.js`

### 通过mcporter（OpenClaw）注册

```bash
mcporter config add picsee stdio -- node ~/.openclaw/workspace/skills/picsee-short-link/mcp-server/dist/index.js
```

之后可以通过以下方式调用相关工具：
```bash
mcporter call picsee.shorten_url url="https://example.com/long-path"
```

### 通过Claude Code注册

在`.claude/settings.json`文件中配置：
```json
{
  "mcpServers": {
    "picsee": {
      "command": "node",
      "args": ["<absolute-path>/mcp-server/dist/index.js"]
    }
  }
}
```

### MCP工具参考

#### `shorten_url`

用于缩短URL。系统会自动检测认证模式：
- 如果已保存API令牌，则使用带高级功能的`api.pics.ee`接口；
- 否则，使用未经认证的`chrome-ext.picsee.tw`接口。

| 参数 | 类型 | 是否必填 | 说明 |
|---------|-------|---------|-------------------|
| `url`    | string | 是       | 目标URL            |
| `encodeId` | string | 否       | 自定义 slug（3-90个字符）       |
| `domain`  | string | 否       | 短链接域名（默认：`pse.is`）       |
| `title`   | string | 否       | 自定义预览标题（高级计划）       |
| `description` | string | 否       | 自定义预览描述（高级计划）       |
| `imageUrl` | string | 否       | 自定义预览缩略图（高级计划）       |
| `tags`    | string[] | 否       | 标签（用于分类，高级计划）       |
| `utm`    | object | 否       | `{source, medium, campaign, term, content}`（高级计划） |

返回值：`{ success, shortUrl, encodeId, mode }`

---

#### `get_analytics`

用于获取短链接的点击统计信息。需要认证。

| 参数 | 类型 | 是否必填 | 说明 |
|---------|-------|---------|-------------------|
| `encodeId` | string | 是       | 短链接的slug（例如：`pse.is/abc123`）       |

返回值：`{ success, data: { totalClicks, uniqueClicks, dailyClicks[] } ``

---

#### `list_links`

用于列出和搜索链接。需要认证。结果按时间倒序返回（最新条目在前）。

| 参数 | 类型 | 是否必填 | 说明 |
|---------|-------|---------|-------------------|
| `startTime` | string | 是       | 从指定时间点开始查询（格式：`YYYY-MM-DDTHH:MM:SS`，例如：`2026-03-31T23:59:59`） |
| `limit` | number | 否       | 每页显示的结果数量（1-50，默认50）     |
| `isAPI` | boolean | 否       | 仅显示API生成的链接       |
| `isStar` | boolean | 否       | 仅显示星标链接       |
| `prevMapId` | string | 否       | 分页游标（用于查询更早的链接）     |
| `externalId` | string | 否       | 按外部ID过滤链接       |
| `keyword` | string | 否       | 按标题/描述搜索（高级计划，3-30个字符） |
| `tag`    | string | 否       | 按标签过滤链接（高级计划）       |
| `url`    | string | 否       | 按目标URL过滤链接       |
| `encodeId` | string | 否       | 按slug过滤链接       |
| `authorId` | string | 否       | 按作者ID过滤链接       |
| `utm`    | object | 否       | `{source, medium, campaign, term, content}`（高级计划） |

返回值：`{ success, data: [{ encodeId, domain, url, title, totalClicks, uniqueClicks, createTime, tags, utm }] }`

**常见错误**：使用月份的第一天作为查询起点（例如`2026-03-01`）会导致错过该月的大部分数据。请始终使用该月的最后一天。

---

#### `edit_link`

用于编辑现有的短链接。需要认证，并且必须使用高级计划。仅允许修改以下字段：

| 参数 | 类型 | 是否必填 | 说明 |
|---------|-------|---------|-------------------|
| `originalEncodeId` | string | 是       | 需要编辑的链接的slug       |
| `url`    | string | 否       | 新的目标URL           |
| `encodeId` | string | 否       | 新的自定义slug         |
| `domain`  | string | 否       | 新的域名           |
| `title`   | string | 否       | 新的预览标题         |
| `description` | string | 否       | 新的预览描述         |
| `imageUrl` | string | 否       | 新的预览缩略图         |
| `tags`    | string[] | 否       | 新的标签             |
| `fbPixel` | string | 否       | Facebook像素ID         |
| `gTag`    | string | 否       | Google标签管理器ID         |
| `utm`    | object | 否       | 新的UTM参数         |
| `expireTime` | string | 否       | 链接过期时间（ISO 8601格式）     |

返回值：`{ success, message }`

---

#### `delete_link`

用于删除或恢复短链接。需要认证。

| 参数 | 类型 | 是否必填 | 说明 |
|---------|-------|---------|-------------------|
| `encodeId` | string | 是       | 短链接的slug           |
| `action` | string | 否       | `"delete"`（默认）或 `"recover"`（恢复）     |

返回值：`{ success, message }`

---

#### `setup_auth`

用于存储和验证PicSee API令牌。令牌使用AES-256-CBC加密算法（密钥由主机名和用户名生成，使用SHA-256哈希值）并保存在`~/.openclaw/.picsee_token`文件中。

| 参数 | 类型 | 是否必填 | 说明 |-------------------|
| `token` | string | 是       | PicSee API令牌           |

返回值：`{ success, plan, quota, usage, message }`

令牌获取地址：<https://picsee.io/> → 设置 → API → 复制令牌

---

## CLI脚本（旧版本）

所有脚本位于`skills/picsee-short-link/scripts/`目录下。输出格式为JSON，无需MCP服务器即可独立使用。

| 脚本 | 功能 | 使用方法         |
|--------|-------------|-------------------------|
| `shorten.mjs` | 缩短URL       | `node shorten.mjs "<URL>"`         |
| `analytics.mjs` | 获取链接统计     | `node analytics.mjs "<ENCODE_ID>"`         |
| `list.mjs` | 列出/搜索链接     | `node list.mjs "<START_TIME>" [LIMIT] [--flags]`     |
| `edit.mjs` | 编辑链接       | `node edit.mjs "<ENCODE_ID>" "<NEW_URL>"`     |
| `delete.mjs` | 删除/恢复链接     | `node delete.mjs "<ENCODE_ID>" [delete|recover]`     |
| `auth.mjs` | 存储令牌       | `node auth.mjs "<TOKEN>"`         |
| `setup.mjs` | 设置未认证模式     | `node setup.mjs`         |

关于`list.mjs`的进阶参数，可以使用`node list.mjs --help`查看详细信息。

---

## 认证模式

| 认证模式 | API地址 | 支持的功能         |
|---------|-------------|-------------------------|
| **未认证** | `chrome-ext.picsee.tw` | 仅支持创建短链接         |
| **认证** | `api.pics.ee` | 支持创建、分析、列表、搜索、编辑和删除链接     |

系统会自动检测`~/.openclaw/.picsee_token`文件中是否存在加密令牌；如果存在，则使用认证模式。否则使用未认证模式。

`config.json`文件用于保存用户选择的认证模式：
```json
{ "mode": "authenticated", "setupDate": "2026-03-04" }
```

---

## 安全性

- **令牌加密**：使用AES-256-CBC算法加密，IV（初始化向量）与密文一起存储（格式：`iv_hex:ciphertext_hex`）。
- **密钥生成**：使用`SHA-256hostname + "-" + username`生成密钥（每台机器独立生成，无共享密钥）。
- **文件权限**：令牌文件权限设置为`0600`，防止未经授权的访问。
- **不存储明文令牌**。
- **MCP服务器和CLI脚本兼容**（使用相同的密钥管理库和文件路径）。

---

## 错误处理

| 错误情况 | 处理方式         |
|---------|-------------------------|
| 未提供令牌且需要认证 | “需要使用PicSee API令牌进行认证。请执行`setup_auth`操作。” |
| 使用非高级计划尝试编辑链接 | “编辑功能需要高级计划。请创建新链接。” |
| 令牌无效 | “令牌无效。请访问https://picsee.io/ → 设置 → API获取新令牌。” |

---

## OpenClaw代理脚本

这些脚本并非MCP服务器的工具，而是代理在接收到上述工具的结果后执行的后续操作。可以使用`exec`命令来运行相应的curl命令。

### 二维码生成

当用户请求生成二维码时：

```bash
curl -s -o /tmp/<ENCODE_ID>_qr.png "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=https://pse.is/<ENCODE_ID>"
```

通过`message`工具发送文件`"/tmp/<ENCODE_ID>_qr.png"`。仅当用户明确请求时生成二维码。

### 分析图表

在调用`get_analytics`后，如果用户需要查看每日点击量图表：

1. 从响应中提取`dailyClicks`数组。
2. 使用这些数据生成图表文件（格式：`/tmp/<ENCODE_ID>_chart.png`）。

通过`message`工具发送该文件。仅当用户请求可视化图表时生成，不会在每次分析请求时自动生成。