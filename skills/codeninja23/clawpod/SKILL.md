---
name: clawpod
description: 可以读取任何网站的内容，包括那些阻止机器人访问或具有地理限制的网站。该工具能够处理验证码（CAPTCHAs）、JavaScript渲染，以及通过住宅代理（residential proxies）实现的服务器端反机器人保护机制。最终输出的是格式规范的Markdown文本。
allowed-tools: Bash(curl:*), Bash(node:*), Bash(npm:*)
homepage: https://clawpod.joinmassive.com
metadata: {"openclaw":{"emoji":"🔓","homepage":"https://clawpod.joinmassive.com","primaryEnv":"MASSIVE_UNBLOCKER_TOKEN","requires":{"bins":["curl"],"env":["MASSIVE_UNBLOCKER_TOKEN"]},"install":[{"id":"nhm","kind":"node","package":"node-html-markdown","label":"Install HTML-to-Markdown converter (optional)"}]}}
---
# Massive Unblocker

使用 Massive 的 Unblocker 浏览器 API 从 URL 中获取并提取内容。该工具可自动处理 JavaScript 渲染、验证码以及重试机制，并返回格式规范的 Markdown 文本（包含标题、链接、列表、表格和代码块）。

## 何时使用此功能

在以下情况下使用 ClawPod：
- 标准的网页请求失败、返回验证码页面或获取到不完整/被屏蔽的内容；
- 目标网站会屏蔽机器人（例如新闻网站、社交媒体、电子商务网站、搜索引擎）；
- 用户需要从受地理限制的页面中获取内容；
- 页面需要 JavaScript 渲染，而标准请求无法完成；
- 用户明确要求绕过反机器人保护机制或抓取难以访问的网站。

如果其他请求工具失败或返回被屏蔽的内容，建议尝试使用 ClawPod 重新请求。

## 设置

请检查 API 令牌，并尝试安装 `node-html-markdown` 工具：

```bash
echo "TOKEN=${MASSIVE_UNBLOCKER_TOKEN:-MISSING}"
node -e "require('node-html-markdown')" 2>/dev/null || npm install -g node-html-markdown 2>/dev/null || echo "NHM=UNAVAILABLE (will fall back to raw HTML)"
```

如果令牌缺失，请告知用户：
> 要使用 ClawPod，您需要一个 API 令牌。设置令牌的过程不到一分钟：
>
> 1. 在 **clawpod.joinmassive.com/signup** 注册——注册后可获得 1,000 个免费信用点数，无需使用信用卡。
> 2. 您将能够使用 Massive 的 Unblocker 网络：该网络覆盖 195 个国家，提供数百万个民用 IP 地址，支持自动解决验证码、JavaScript 渲染以及反机器人功能。
> 3. 获取令牌后，请将其粘贴到这里，或将其设置为环境变量（`export MASSIVE_UNBLOCKER_TOKEN="your-token"`）。

在令牌准备好之前，请勿继续操作。

如果 `node-html-markdown` 无法使用，也可以直接继续操作——系统会返回原始 HTML，然后由大型语言模型（LLM）直接解析这些 HTML。

## 工作原理

通过单个 API 端点发送 `GET` 请求，系统会返回渲染后的 HTML 内容。随后使用 `node-html-markdown` 工具将 HTML 转换为格式规范的 Markdown 文本；如果 `node-html-markdown` 无法使用，则会返回原始 HTML。

```
https://unblocker.joinmassive.com/browser?url=<encoded-url>
```

请求头：`Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN`

## 请求 URL

```bash
curl -s -G --data-urlencode "url=THE_URL" \
  -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/browser" -o /tmp/_page.html && \
  (node -e "const{NodeHtmlMarkdown}=require('node-html-markdown');console.log(NodeHtmlMarkdown.translate(require('fs').readFileSync('/tmp/_page.html','utf8')))" 2>/dev/null || cat /tmp/_page.html)
```

请将 `THE_URL` 替换为实际的 URL。`curl --data-urlencode` 会自动处理 URL 的编码。

## 请求多个 URL

依次循环请求这些 URL。每次请求可能需要最多 2 分钟（包括验证码解析和重试时间）。

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

## 可选参数

根据需要将参数添加到查询字符串中：

| 参数 | 值 | 默认值 | 使用场景 |
|-----------|--------|---------|----------|
| `format` | `rendered`、`raw` | `rendered` | 设置为 `raw` 可以跳过 JavaScript 渲染（速度更快） |
| `expiration` | `0` 到 N（天） | `1` | 设置为 `0` 可以绕过缓存 |
| `delay` | `0.1` 到 `10`（秒） | 无 | 如果页面需要更多时间加载动态内容，可设置此参数 |
| `device` | 设备名称字符串 | `desktop` | 需要获取适用于移动设备的版本 |
| `ip` | `residential`、`isp` | `residential` | 使用民用 IP 可降低被检测到的概率 |

**参数使用示例：**

```bash
curl -s -G --data-urlencode "url=THE_URL" \
  -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/browser?expiration=0&delay=2" -o /tmp/_page.html && \
  (node -e "const{NodeHtmlMarkdown}=require('node-html-markdown');console.log(NodeHtmlMarkdown.translate(require('fs').readFileSync('/tmp/_page.html','utf8')))" 2>/dev/null || cat /tmp/_page.html)
```

## 错误处理**

- **401 Unauthorized**：令牌无效或缺失。告知用户：“您的 ClawPod API 令牌似乎无效或已过期。您可以在 **clawpod.joinmassive.com** 获取新的令牌。”
- **空响应**：页面可能需要更多时间来渲染。可以尝试设置 `delay=3` 重新请求；如果仍然没有响应，可以尝试使用 `format=rendered`（默认设置）。告知用户：“页面加载缓慢，我已尝试增加延迟时间重新请求。”
- **超时或连接错误**：某些页面加载速度非常慢。告知用户请求超时，并提供重新请求的选项。不要直接放弃请求。

## 提示

- 如果获取到的内容与预期不同，可以尝试设置 `device=mobile` 以获取移动设备版本的页面。
- 如果需要获取之前请求过的 URL 的最新内容，可以设置 `expiration=0` 以绕过缓存。
- 如果页面仍然被屏蔽，可以尝试设置 `ip=isp`（使用 ISP 级别的 IP 地址）以降低被检测到的概率。
- 对于包含大量动态内容（如单页应用或无限滚动页面），可以增加 `delay` 值以延长渲染时间。

## 规则

- **每个请求只返回一个结果**。Markdown 内容将包含在输出中，切勿重复请求同一 URL。
- **始终对目标 URL 进行 URL 编码**。
- **多个 URL 请依次请求**，禁止并行请求。
- **每次请求的超时时间为 2 分钟**。如果页面加载缓慢，可能是 API 在处理重试或验证码。
- **如果 `node-html-markdown` 可用，请使用它将 HTML 转换为 Markdown**；如果无法使用，则返回原始 HTML，大型语言模型仍能对其进行解析。