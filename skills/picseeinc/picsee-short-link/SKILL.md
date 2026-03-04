---
name: picsee-short-link
description: 使用 PicSee (pse.is) 来缩短 URL。API 令牌可以存储在 `skills/picsee-short-link/config.json` 文件中（可选）。当用户请求缩短 URL、创建短链接或提及 PicSee 时，可以使用该服务。该服务支持两种模式：未经身份验证的模式（基本缩短功能）和经过身份验证的模式（高级计划用户可享受分析、编辑、搜索以及自定义缩略图等功能）。
metadata:
  {
    "openclaw":
      {
        "emoji": "🔗",
        "configPaths": ["skills/picsee-short-link/config.json"],
        "requires": { "bins": ["curl", "jq"] },
        "externalApis": ["api.pics.ee", "chrome-ext.picsee.tw", "api.qrserver.com", "quickchart.io"],
        "writesPaths": ["/tmp/*.png", "skills/picsee-short-link/config.json"]
      }
  }
---
# PicSee 短链接服务

这是一个快速 URL 缩短工具，支持可选的分析功能。

## 安全性与功能范围

该工具执行以下操作：

**文件操作：**
- 读取/写入 `skills/picsee-short-link/config.json` 文件（以明文形式存储 API 令牌，可选）
- 将 QR 码图片写入 `/tmp/<shortcode>.png` 文件（仅当用户请求时）
- 将分析图表写入 `/tmp/<encodeId>_analytics.png` 文件（仅当用户请求可视化时）

**网络操作：**
- 向 `api.pics.ee` 发送 HTTPS API 请求（需要身份验证）
- 向 `chrome-ext.picsee.tw` 发送 HTTPS API 请求（无需身份验证）
- 向 `api.qrserver.com` 发送 HTTPS API 请求（生成 QR 码，可选）
- 向 `quickchart.io` 发送 HTTPS API 请求（生成图表，可选）

**安全注意事项：**
- API 令牌以明文形式存储在工作区配置文件中（不适用于整个系统）
- 所有 API 请求均使用 HTTPS 协议
- 除了 PicSee API 和用户请求的 QR/图表服务外，不会向第三方发送任何数据
- 令牌不会被记录或传输给其他方

**功能范围：**
- 核心功能是 URL 缩短；分析、QR 码和图表为可选功能，需用户明确请求。

## 快速操作：缩短 URL

**对于 99% 的请求，使用以下流程：**

1. **检查配置**：读取 `skills/picsee-short-link/config.json` 文件
   - 如果文件不存在 → 转到 **首次设置**（见下文）
   - 如果文件存在 → 检查 `status` 字段并继续下一步

2. **调用 API**：
   - **无需身份验证**（无令牌）：
     ```bash
     curl -X POST https://chrome-ext.picsee.tw/v1/links \
       -H "Content-Type: application/json" \
       -d '{"url":"<LONG_URL>","domain":"pse.is","externalId":"openclaw"}'
     ```
   
   - **需要身份验证**（有令牌）：
     ```bash
     # Read token from config.json first
     TOKEN=$(jq -r '.apiToken' ~/.openclaw/workspace/skills/picsee-short-link/config.json)
     
     curl -X POST https://api.pics.ee/v1/links \
       -H "Authorization: Bearer $TOKEN" \
       -H "Content-Type: application/json" \
       -d '{"url":"<LONG_URL>","domain":"pse.is","externalId":"openclaw"}'
     ```
     （令牌存储在 `config.json` 文件的 `apiToken` 字段中）

3. **显示结果**（便于用户复制的代码块）：
   ```text
   https://pse.is/abc123
   ```
   然后询问用户是否需要 QR 码；如果用户未登录，还需询问是否要添加 API 令牌以使用分析/编辑功能。

4. **生成 QR 码**（仅当用户明确请求时）：
   ```bash
   curl -o /tmp/qrcode.png "https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=<SHORT_URL>"
   ```
   然后通过 `message` 工具发送 QR 码图片（路径：`/tmp/qrcode.png`）

**完成。** 除非用户请求，否则无需询问分析功能。

---

## 首次设置（如果配置文件不存在）

**检测**：检查 `skills/picsee-short-link/config.json` 文件是否存在。如果不存在，则表示是首次使用。

**询问用户**（解释功能）：

> “您是否愿意提供 PicSee API 令牌以启用高级功能？（是/否）”
> 
> **使用令牌（需要身份验证）后，您可以：**
> - 查看链接分析和每日点击统计
> - 列出您的短链接（可按日期范围筛选）
> - 搜索短链接
> - 编辑链接（更改目标 URL）—— **仅限高级计划**
> - 自定义缩略图/标题—— **仅限高级计划**
> 
> **无需令牌（无需身份验证）时，您可以：**
> - 创建基本的短链接（无分析功能）
> 
> **获取 API 令牌的方法：**
> 访问 https://picsee.io/ → 点击右上角的头像 → 设置 → API → 复制令牌”

**如果用户选择“是”：**

1. 等待 API 令牌（字符串格式，例如 `abc123def456...`）

2. 创建 `skills/picsee-short-link/config.json` 文件：
   ```json
   {
     "status": "authenticated",
     "apiToken": "<user_token>",
     "setupDate": "YYYY-MM-DD"
   }
   ```

3. 通过调用 API 检查令牌的有效性：
   ```bash
   TOKEN=$(jq -r '.apiToken' ~/.openclaw/workspace/skills/picsee-short-link/config.json)
   curl -X GET https://api.pics.ee/v2/my/api/status \
     -H "Authorization: Bearer $TOKEN"
   ```

4. 向用户显示其使用的计划等级（免费/基础/高级）及配额信息。

**如果用户选择“否”：**

1. 创建 `skills/picsee-short-link/config.json` 文件：
   ```json
   {
     "status": "unauthenticated",
     "setupDate": "YYYY-MM-DD"
   }
   ```

2. 解释：“您可以在无需身份验证的情况下创建短链接。如需后续使用分析/编辑功能，请随时告诉我。”

---

## 高级功能（仅限已认证用户）

### 查看链接分析

从短链接中提取 `encodeId`（例如 `pse.is/abc123` → `abc123`），然后：

```bash
TOKEN=$(jq -r '.apiToken' ~/.openclaw/workspace/skills/picsee-short-link/config.json)
curl -X GET "https://api.pics.ee/v1/links/<ENCODE_ID>/overview?dailyClicks=true" \
  -H "Authorization: Bearer $TOKEN"
```

**返回的信息包括：**
- `totalClicks`（总点击次数）
- `uniqueClicks`（唯一点击次数）
- `dailyClicks` 数组（包含日期和点击次数）

**生成图表**（如果用户请求可视化）：

1. 使用 jq 从 API 响应中提取每日点击数据
2. 使用图表配置生成 QuickChart URL（折线图，显示总点击次数/唯一点击次数随时间的变化）
3. 下载图表图片

**示例：**
```bash
# After getting API response, parse data and generate chart
ENCODE_ID="abc123"
TOKEN=$(jq -r '.apiToken' ~/.openclaw/workspace/skills/picsee-short-link/config.json)

# Fetch analytics
RESPONSE=$(curl -s -X GET "https://api.pics.ee/v1/links/$ENCODE_ID/overview?dailyClicks=true" \
  -H "Authorization: Bearer $TOKEN")

# Parse dates and clicks (example - adjust based on actual response structure)
DATES=$(echo "$RESPONSE" | jq -r '.data.dailyClicks[].date' | jq -R -s -c 'split("\n")[:-1]')
TOTAL=$(echo "$RESPONSE" | jq -r '.data.dailyClicks[].totalClicks' | jq -s -c '.')
UNIQUE=$(echo "$RESPONSE" | jq -r '.data.dailyClicks[].uniqueClicks' | jq -s -c '.')

# Build QuickChart config (URL-encoded JSON)
CHART_CONFIG=$(cat <<EOF | jq -R -s -c '@uri'
{
  "type": "line",
  "data": {
    "labels": $DATES,
    "datasets": [
      {
        "label": "Total Clicks",
        "data": $TOTAL,
        "borderColor": "rgb(75, 192, 192)",
        "fill": false
      },
      {
        "label": "Unique Clicks",
        "data": $UNIQUE,
        "borderColor": "rgb(255, 99, 132)",
        "fill": false
      }
    ]
  },
  "options": {
    "title": {
      "display": true,
      "text": "Link Analytics - $ENCODE_ID"
    },
    "scales": {
      "yAxes": [{
        "ticks": {
          "beginAtZero": true
        }
      }]
    }
  }
}
EOF
)

# Download chart
curl -o "/tmp/${ENCODE_ID}_analytics.png" "https://quickchart.io/chart?c=$CHART_CONFIG"
```

4. 通过 `message` 工具发送图表图片（路径：`/tmp/<encodeId>_analytics.png`）

---

### 列出最近创建的链接

```bash
TOKEN=$(jq -r '.apiToken' ~/.openclaw/workspace/skills/picsee-short-link/config.json)
curl -X POST "https://api.pics.ee/v2/links/overview?isAPI=false&limit=50&startTime=<ISO8601_DATE>" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

**日期格式**：`YYYY-MM-DDTHH:MM:SS`（不包含时区后缀）

**⚠️ 重要提示：startTime 参数的使用**

`startTime` 参数会反向筛选结果，仅返回在指定日期或之前创建的链接（按时间顺序从新到旧显示）。

**示例：**

- **查询 2025 年 12 月的数据**：
  - 使用：`startTime=2025-12-31T23:59:59`（当月的最后一天）
  - 这将返回 12 月 1 日至 31 日的所有链接

- **查询特定月份的数据**：
  - 使用该月份的 **最后一天** 的时间戳：`2025-12-31T23:59:59`
  - 例如：12 月 → `2025-12-31T23:59:59`
  - 1 月 → `2026-01-31T23:59:59`

- **查询特定日期范围的数据**：
  - 使用 `startTime` 指定范围的结束日期
  - 结合 `limit` 参数控制返回的结果数量
  - 如需查看更早的数据，可调整 `limit` 值

**常见错误**：使用月份的 **第一天** 会导致遗漏该月份的数据。

---

### 检查用户计划等级

```bash
TOKEN=$(jq -r '.apiToken' ~/.openclaw/workspace/skills/picsee-short-link/config.json)
curl -X GET https://api.pics.ee/v2/my/api/status \
  -H "Authorization: Bearer $TOKEN"
```

**计划等级**：`"free"`、`"basic"`、`"advanced"`

**功能限制**：
- **免费/基础计划**：创建链接、查看分析结果、列出链接
- **高级计划**：编辑链接、自定义缩略图/标题、添加 UTM 参数、跟踪像素

---

### 编辑短链接（仅限高级计划）

```bash
TOKEN=$(jq -r '.apiToken' ~/.openclaw/workspace/skills/picsee-short-link/config.json)
curl -X PUT https://api.pics.ee/v2/links/<ENCODE_ID> \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"url":"<NEW_DESTINATION_URL>"}'
```

**如果用户未使用高级计划**：阻止编辑并建议用户创建新链接。

---

### 删除短链接

```bash
TOKEN=$(jq -r '.apiToken' ~/.openclaw/workspace/skills/picsee-short-link/config.json)
curl -X POST https://api.pics.ee/v2/links/<ENCODE_ID>/delete \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"value":"delete"}'
```

（可以使用 `recover` 命令恢复链接）

---

## 操作模式总结

| 操作模式 | 基础 URL | 是否需要身份验证 | 可用功能 |
|------|----------|---------------|----------|
| **无需身份验证** | `chrome-ext.picsee.tw` | 否 | 仅能创建链接 |
| **需要身份验证** | `api.pics.ee` | 是 | 可创建链接、查看分析结果、列出链接、编辑链接（取决于计划等级） |

**默认设置**：无需身份验证（最快，无需额外设置）。

---

## 输出规范

- **短链接**：始终使用代码块格式以便用户复制
- **语言**：所有响应内容均使用用户的语言
- **避免使用专业术语**：在面向用户的消息中避免使用“API call”、“endpoint”或“JSON”
- **图表**：使用英文标签，采用专业样式，图表保存在 `/tmp/` 目录中，并通过 `message` 工具发送

---

## 快速参考

- **令牌位置**：`skills/picsee-short-link/config.json` 文件中的 `apiToken` 字段
- **配置文件位置**：`skills/picsee-short-link/config.json`
- **默认域名**：`pse.is`
- **外部链接格式**：始终使用 `openclaw`

---

## 错误处理**

- **无需身份验证但用户请求分析功能**：回复：“此功能需要登录。请提供您的 PicSee API 令牌。”
- **用户使用非高级计划但尝试编辑链接**：回复：“编辑链接需要高级计划。您可以创建新的链接。”
- **令牌无效**：回复：“API 令牌无效。请访问 https://picsee.io/ → 设置 → API 重新获取令牌。”