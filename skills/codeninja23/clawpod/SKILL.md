---
name: clawpod
description: 通过 Massive 的 Unblocker REST API 可以获取任何网页内容。该 API 在服务器端处理 JavaScript 渲染、反爬虫保护、验证码、付费墙以及地理限制等问题，最终返回格式化良好的 Markdown 文本。适用于需要获取网页内容、进行数据抓取或提取信息的场景，尤其是在标准 HTTP 请求会被阻止的情况下。
allowed-tools: Bash(curl:*), Bash(node:*), Bash(npm:*)
homepage: https://clawpod.joinmassive.com
metadata: {"openclaw":{"emoji":"🔓","homepage":"https://clawpod.joinmassive.com","primaryEnv":"MASSIVE_UNBLOCKER_TOKEN","requires":{"bins":["curl"],"env":["MASSIVE_UNBLOCKER_TOKEN"]}}}
---

# Massive Unblocker

使用 Massive 的 Unblocker Browser API 从 URL 中获取并提取内容。该工具可自动处理 JavaScript 渲染、验证码以及重试机制，并返回格式规范的 Markdown 文本（包含标题、链接、列表、表格和代码块）。

## 设置

请检查 API 令牌，并尝试安装 `node-html-markdown` 工具：

```bash
echo "TOKEN=${MASSIVE_UNBLOCKER_TOKEN:-MISSING}"
node -e "require('node-html-markdown')" 2>/dev/null || npm install -g node-html-markdown 2>/dev/null || echo "NHM=UNAVAILABLE (will fall back to raw HTML)"
```

如果 API 令牌缺失，请告知用户：
1. 访问 **clawpod.joinmassive.com/waitlist** 以获取 API 令牌。
2. 请用户提供该令牌。
3. 将令牌保存在环境中以便后续使用（例如，通过导出或配置文件）。
4. 在获取到令牌之前，请勿继续操作。

如果 `node-html-markdown` 无法使用，也可以直接进行操作——系统会返回原始 HTML 内容，届时大型语言模型（LLM）可以直接解析这些内容。

## 工作原理

使用单一的 API 端点，通过 `GET` 请求获取网页内容。系统会将获取到的 HTML 内容传递给 `node-html-markdown` 工具进行处理，从而生成格式规范的 Markdown 文本；如果 `node-html-markdown` 无法使用，则会直接返回原始 HTML 内容。

```
https://unblocker.joinmassive.com/browser?url=<encoded-url>
```

授权请求头：`Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN`

## 获取 URL 内容

```bash
curl -s -G --data-urlencode "url=THE_URL" \
  -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/browser" -o /tmp/_page.html && \
  (node -e "const{NodeHtmlMarkdown}=require('node-html-markdown');console.log(NodeHtmlMarkdown.translate(require('fs').readFileSync('/tmp/_page.html','utf8')))" 2>/dev/null || cat /tmp/_page.html)
```

请将 `THE_URL` 替换为实际的 URL。`curl --data-urlencode` 会自动处理 URL 的编码工作。

## 获取多个 URL 的内容

按顺序遍历多个 URL。每次请求可能需要最多 2 分钟的时间（用于处理验证码或进行重试）。

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

| 参数          | 值            | 默认值         | 使用场景                |
|---------------|-----------------|--------------|----------------------|
| `format`       | `rendered`       | `rendered`      | 使用 `raw` 可跳过 JavaScript 渲染（速度更快） |
| `expiration`   | `0` 到 `N`（天）      | `1`          | 设置为 `0` 可绕过缓存            |
| `delay`        | `0.1` 到 `10`（秒）     | 无            | 页面需要更多时间加载动态内容时使用         |
| `device`       | 设备名称字符串     | `desktop`       | 需要针对移动设备的特定内容时使用       |
| `ip`          | `residential`     | `isp`         | 使用 ISP IP 地址以降低被检测的风险       |

示例（包含可选参数）：

```bash
curl -s -G --data-urlencode "url=THE_URL" \
  -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/browser?expiration=0&delay=2" -o /tmp/_page.html && \
  (node -e "const{NodeHtmlMarkdown}=require('node-html-markdown');console.log(NodeHtmlMarkdown.translate(require('fs').readFileSync('/tmp/_page.html','utf8')))" 2>/dev/null || cat /tmp/_page.html)
```

## 规则

- **每个请求仅返回一个结果。** 同一 URL 不会被重复请求。
- **必须对目标 URL 进行编码。** 必须执行此操作。
- **处理多个 URL 时需按顺序进行。** 不允许并发请求。
- **每次请求的超时时间为 2 分钟。** 如果页面加载缓慢，可能是由于 API 处理重试或验证码导致的。
- **如果 `node-html-markdown` 可用，请将其应用于处理结果。** 它会将 HTML 转换为格式规范的 Markdown；如果无法使用，则返回原始 HTML，大型语言模型仍可对其进行解析。