---
name: clawpod
description: 你可以阅读任何网站的内容，或者通过谷歌进行搜索——即使这些网站屏蔽了机器人访问或设置了地理限制。该工具能够处理验证码（CAPTCHAs），以及通过住宅代理（residential proxies）在服务器端实现的JavaScript渲染和反机器人保护机制。最终，它会返回格式清晰的Markdown内容或结构化的JSON数据。
allowed-tools: Bash(curl:*), Bash(node:*), Bash(npm:*)
homepage: https://clawpod.joinmassive.com
metadata: {"openclaw":{"emoji":"🔓","homepage":"https://clawpod.joinmassive.com","primaryEnv":"MASSIVE_UNBLOCKER_TOKEN","requires":{"bins":["curl"],"env":["MASSIVE_UNBLOCKER_TOKEN"]},"install":[{"id":"nhm","kind":"node","package":"node-html-markdown","label":"Install HTML-to-Markdown converter (optional)"}]}}
---
# Massive Unblocker

使用 Massive 的 Unblocker API 从 URL 中获取并提取内容，或进行谷歌搜索。该工具可自动处理 JavaScript 渲染、验证码以及重试机制，支持返回格式化的 Markdown、原始 HTML 或结构化的 JSON 数据。

## 适用场景

在以下情况下使用 ClawPod：
- 标准的网页请求失败、返回验证码页面或获取到不完整/被屏蔽的内容；
- 目标网站限制访问机器人（如新闻网站、社交媒体、电子商务网站、搜索引擎）；
- 需要从受地理限制的页面获取内容；
- 页面需要 JavaScript 渲染，而标准请求无法处理；
- 用户明确要求绕过反机器人保护机制或抓取难以访问的网站；
- 用户需要以结构化数据或 HTML 的形式获取谷歌搜索结果（包括自然搜索和付费搜索结果）；
- 内置的网页搜索工具返回的结果不完整或被屏蔽；
- 用户需要本地化或针对特定地理位置的谷歌搜索结果。

如果其他请求或搜索工具失败或返回被屏蔽的内容，建议尝试使用 ClawPod 重新请求。

## 设置

请检查 API 令牌，并尝试安装 `node-html-markdown` 工具：

```bash
echo "TOKEN=${MASSIVE_UNBLOCKER_TOKEN:-MISSING}"
node -e "require('node-html-markdown')" 2>/dev/null || npm install -g node-html-markdown 2>/dev/null || echo "NHM=UNAVAILABLE (will fall back to raw HTML)"
```

如果令牌缺失，请告知用户：
> 要使用 ClawPod，您需要一个 API 令牌。设置令牌只需不到一分钟的时间：
>
> 1. 在 **clawpod.joinmassive.com/signup** 注册——注册后可获得 1,000 个免费信用点数，无需信用卡。
> 2. 您将能够使用 Massive 的 Unblocker 网络：该网络覆盖 195 个国家，提供数百万个居民 IP 地址，支持自动解决验证码、JavaScript 渲染以及反机器人功能。
> 3. 获取令牌后，请将其粘贴到这里，或将其设置为环境变量（`export MASSIVE_UNBLOCKER_TOKEN="your-token"`）。

在令牌准备好之前，请勿继续操作。

如果 `node-html-markdown` 无法使用，也可以继续操作——系统会返回原始 HTML，AI 模型可以直接解析这些内容。

## 工作原理

该工具提供两个接口，两者都使用相同的认证令牌进行 `GET` 请求。

**浏览器接口** — 用于获取并渲染任意 URL，返回 HTML 数据（通过 `node-html-markdown` 转换为 Markdown 格式）：
```
https://unblocker.joinmassive.com/browser?url=<encoded-url>
```

**搜索接口** — 用于获取谷歌搜索结果，返回 HTML 或结构化的 JSON 数据：
```
https://unblocker.joinmassive.com/search?terms=<encoded-terms>
```

认证头：`Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN`

## 获取 URL 内容

```bash
curl -s -G --data-urlencode "url=THE_URL" \
  -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/browser" -o /tmp/_page.html && \
  (node -e "const{NodeHtmlMarkdown}=require('node-html-markdown');console.log(NodeHtmlMarkdown.translate(require('fs').readFileSync('/tmp/_page.html','utf8')))" 2>/dev/null || cat /tmp/_page.html)
```

请将 `THE_URL` 替换为实际的 URL。`curl --data-urlencode` 会自动处理 URL 的编码。

## 获取多个 URL 的内容

依次遍历多个 URL。每次请求可能需要最多 2 分钟（包括验证码处理和重试时间）：
```bash
URLS=(
  "https://example.com/page1"
  "https://example.com/page2"
)

for url in "${URLS[@]}"; do
  echo "=== $url ==="
  curl -s -G --data-urlencode "url=$url" \
    -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
    "https://unblocker.joinmassive.com/browser" -o /tmp/_page.html && \
    (node -e "const{NodeHtmlMarkdown}=require('node-html-markdown');console.log(NodeHtmlMarkdown.translate(require('fs').readFileSync('/tmp/_page.html','utf8')))" 2>/dev/null || cat /tmp/_page.html)
done
```

## 在谷歌上搜索

使用该接口进行搜索，返回所有自然搜索和付费搜索结果，格式为 HTML 或结构化的 JSON：
```
https://unblocker.joinmassive.com/search?terms=<encoded-terms>
```

认证头：`Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN`（与浏览器请求使用的令牌相同）

### 基本搜索

```bash
curl -s -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/search?terms=foo+bar+baz&format=json"
```

请将 `foo+bar+baz` 替换为搜索查询词。空格需要用 `+` 或 `%20` 替换。

### 带参数的搜索

| 参数          | 是否必填 | 参数值    | 默认值    | 使用场景       |
|---------------|---------|---------|-------------|-------------|
| `terms`        | 是      | 搜索查询词（空格用 `+` 或 `%20` 替换） | 总是必需      |
| `format`        | 否       | `html`、`json`   | `html`       | 选择 `json` 以获取结构化结果 |
| `serps`        | 否       | `1` 到 `10`    | `1`         | 需要多页结果     |
| `size`        | 否       | `0` 到 `100`    | 未设置       | 控制每页显示的结果数量 |
| `offset`        | 否       | `0` 到 `100`    | `0`         | 跳过初始结果     |
| `language`        | 否       | 语言名称、ISO 代码或谷歌代码 | 未设置       | 设置搜索语言     |
| `uule`        | 否       | 编码后的地理位置字符串 | 未设置       | 设置搜索地理位置     |
| `expiration`     | 否       | `0` 到 N（天）    | `1`         | 设置为 `0` 可绕过缓存   |
| `subaccount`     | 否       | 最多 255 个字符 | 未设置       | 分开计费       |

### JSON 格式输出

当 `format` 设置为 `json` 时，搜索结果将以结构化的嵌套对象形式返回，其中包含自然搜索结果、付费搜索结果及元数据——无需再进行 HTML 解析。

### 搜索技巧
- **尽可能使用 `format=json`**：结构化数据更易于处理。
- **设置 `size=10` 可快速获取概览结果，`size=100` 可获取完整结果**。
- **使用 `offset` 可分页查看结果**。
- **使用 `language` 可指定搜索语言**（例如 `language=es` 用于搜索西班牙语内容）。
- **实时搜索通常需要几秒钟，但如果需要重试，最长可能需要 120 秒**。

## 浏览器相关参数

根据需要将以下参数添加到 `/browser` 查询字符串中：
| 参数          | 参数值    | 默认值    | 使用场景       |
|---------------|---------|---------|-------------|-------------|
| `format`        | `rendered`、`raw` | `rendered`   | 设置为 `raw` 可跳过 JavaScript 渲染（更快） |
| `expiration`     | `0` 到 N（天） | `1`         | 设置为 `0` 可绕过缓存   |
| `delay`        | `0.1` 到 `10`（秒） | 未设置       | 需要更多时间加载动态内容时使用 |
| `device`        | 设备名称字符串 | `desktop`    | 需要移动端特定内容时使用 |
| `ip`          | `residential`、`isp` | `residential` | 使用居民 IP 以降低被检测概率 |

**带浏览器参数的示例**：
```bash
curl -s -G --data-urlencode "url=THE_URL" \
  -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/browser?expiration=0&delay=2" -o /tmp/_page.html && \
  (node -e "const{NodeHtmlMarkdown}=require('node-html-markdown');console.log(NodeHtmlMarkdown.translate(require('fs').readFileSync('/tmp/_page.html','utf8')))" 2>/dev/null || cat /tmp/_page.html)
```

## 错误处理
- **401 Unauthorized** — 令牌无效或缺失。告知用户：“您的 ClawPod API 令牌无效或已过期。您可以在 **clawpod.joinmassive.com** 获取新令牌。”
- **空响应** — 页面可能需要更多时间渲染。尝试使用 `delay=3` 重新请求。如果仍然没有结果，尝试使用 `format=rendered`（默认设置）。告知用户：“页面加载缓慢，我已尝试增加延迟时间。”
- **超时或连接错误** — 部分页面加载速度非常慢。告知用户请求超时，并提供重试选项。不要直接放弃请求。

## 其他提示
- 如果内容与预期不同，尝试使用 `device=mobile` 来获取移动端版本。
- 为之前获取过的 URL 获取最新结果，可以使用 `expiration=0` 绕过缓存。
- 如果内容仍然被屏蔽，可以尝试使用 `ip=isp`（使用 ISP 级别的 IP 地址）。
- 对于包含大量动态内容（如单页应用或无限滚动页面），增加 `delay` 以延长渲染时间。

**使用规则**
- **每次请求只返回一个结果**。输出结果为 Markdown 格式，不要重复请求同一 URL。
- **始终对目标 URL 进行编码**。
- **处理多个 URL 时请按顺序进行**，不要同时发送多个请求。
- **每次请求的超时时间为 2 分钟**。如果页面或搜索响应缓慢，可能是 API 在处理重试或验证码。
- **如果 `node-html-markdown` 可用，请将其用于转换 HTML 为 Markdown**。如果无法使用，系统会返回原始 HTML，AI 模型仍能解析这些内容。
- **搜索结果建议使用 `format=json`**。结构化的 JSON 更适合搜索结果的处理。
- **在 `terms` 参数中，使用 `+` 或 `%20` 对搜索词进行编码**。