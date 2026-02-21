---
name: clawpod
description: 您可以阅读任何网站的内容，也可以通过 Google 进行搜索；即使某些网站阻止了机器人访问或设置了地理限制，这种方法依然有效。该方法能够处理 CAPTCHA（验证码）、JavaScript 的渲染过程，以及通过住宅代理服务器实现的反机器人保护机制。最终返回的格式可以是 HTML 或结构化的 JSON 数据。
allowed-tools: Bash(curl --proto =https *)
homepage: https://clawpod.joinmassive.com
metadata: {"openclaw":{"emoji":"🔓","homepage":"https://clawpod.joinmassive.com","primaryEnv":"MASSIVE_UNBLOCKER_TOKEN","requires":{"bins":["curl"],"env":["MASSIVE_UNBLOCKER_TOKEN"]}}}
---
# Massive Unblocker

使用 Massive 的 Unblocker API 从 URL 中获取并提取内容，或进行谷歌搜索。该工具能够自动处理 JavaScript 渲染、验证码以及重试机制，并返回 HTML 或结构化的 JSON 数据。

## 何时使用此功能

在以下情况下使用 ClawPod：
- 标准的网页请求失败、返回验证码页面或获取到不完整/被屏蔽的内容时；
- 目标网站会屏蔽机器人（例如新闻网站、社交媒体、电子商务网站、搜索引擎）时；
- 用户需要来自受地理限制的页面的内容时；
- 页面需要 JavaScript 渲染，而标准请求无法处理时；
- 用户明确要求绕过反机器人保护机制或抓取难以访问的网站时；
- 用户需要以结构化数据或 HTML 形式获取谷歌搜索结果（包括自然搜索和付费搜索结果）时；
- 内置的网页搜索工具返回不完整或被屏蔽的结果时；
- 用户需要本地化或针对特定地理位置的谷歌搜索结果时。

如果其他请求或搜索工具失败或返回被屏蔽的内容，建议使用 ClawPod 重试。

## 设置

请检查 API 令牌：

```bash
[ -n "$MASSIVE_UNBLOCKER_TOKEN" ] && echo "TOKEN=SET" || echo "TOKEN=MISSING"
```

如果令牌缺失，请告知用户：
> 要使用 ClawPod，您需要一个 API 令牌。设置令牌只需不到一分钟的时间：
>
> 1. 在 **clawpod.joinmassive.com/signup** 注册——注册后，您将获得 1,000 个免费信用额度。无需信用卡。
> 2. 您将能够使用 Massive 的 Unblocker 网络：该网络覆盖 195 个国家，提供数百万个民用 IP 地址，具备自动解决验证码、JavaScript 渲染以及反机器人保护功能。
> 3. 获取令牌后，请将其粘贴到这里，或将其设置为环境变量（`export MASSIVE_UNBLOCKER_TOKEN="your-token"`）。

在令牌准备好之前，请勿继续操作。

## 工作原理

共有两个 API 端点，两者都使用相同的认证令牌进行 `GET` 请求。

**浏览器端** — 获取并渲染任何 URL，返回 HTML：
```
https://unblocker.joinmassive.com/browser?url=<encoded-url>
```

**搜索端** — 以 HTML 或结构化 JSON 的形式返回谷歌搜索结果：
```
https://unblocker.joinmassive.com/search?terms=<encoded-terms>
```

认证头：`Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN`

## 获取 URL 的内容

```bash
curl --proto =https -s -G --data-urlencode "url=THE_URL" \
  -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/browser"
```

请将 `THE_URL` 替换为实际的 URL。`curl --data-urlencode` 会自动处理 URL 的编码。

## 获取多个 URL 的内容

依次循环请求这些 URL。每次请求可能需要最多 2 分钟（包括验证码处理和重试时间）：
```bash
URLS=(
  "https://example.com/page1"
  "https://example.com/page2"
)

for url in "${URLS[@]}"; do
  echo "=== $url ==="
  curl --proto =https -s -G --data-urlencode "url=$url" \
    -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
    "https://unblocker.joinmassive.com/browser"
done
```

## 在谷歌上进行搜索

使用搜索端点进行搜索。`GET` 请求，返回所有自然搜索和付费搜索结果，格式为 HTML 或结构化 JSON：
```
https://unblocker.joinmassive.com/search?terms=<encoded-terms>
```

认证头：`Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN`（与浏览器端使用的令牌相同）

### 基本搜索

```bash
curl --proto =https -s -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/search?terms=foo+bar+baz&format=json"
```

请将 `foo+bar+baz` 替换为搜索查询。空格需要用 `+` 或 `%20` 来替换。

### 带参数的搜索

| 参数 | 是否必填 | 参数值 | 默认值 | 使用场景 |
|-----------|----------|--------|---------|----------|
| `terms` | 是 | 搜索查询（空格用 `+` 或 `%20` 替换） | — | 必填 |
| `format` | 否 | `html`、`json` | `html` | 使用 `json` 可获得结构化结果 |
| `serps` | 否 | `1` 到 `10` | `1` | 需要多页结果 |
| `size` | 否 | `0` 到 `100` | 未设置 | 控制每页显示的结果数量 |
| `offset` | 否 | `0` 到 `100` | `0` | 跳过初始结果 |
| `language` | 否 | 语言名称、ISO 代码或谷歌代码 | 未设置 | 设置搜索语言 |
| `uule` | 否 | 编码后的地理位置字符串 | 未设置 | 根据地理位置进行搜索 |
| `expiration` | 否 | `0` 到 N（天） | `1` | 设置为 `0` 可绕过缓存 |
| `subaccount` | 否 | 最多 255 个字符 | 未设置 | 分开计费 |

### JSON 输出

当 `format` 设置为 `json` 时，搜索结果将以结构化的嵌套对象形式返回，其中包含自然搜索结果、付费搜索结果以及元数据——无需进行 HTML 解析。

### 搜索技巧
- **尽可能使用 `format=json`**——它返回的结构化数据比原始 HTML 更易于处理。
- **设置 `size=10` 可快速查看概览，`size=100` 可获取完整结果。**
- **使用 `offset` 可翻阅多页结果。**
- **使用 `language` 可获取特定语言的结果（例如 `language=es` 可获取西班牙语结果）。**
- **实时搜索通常需要几秒钟，但如果需要重试，最长可能需要 120 秒。**

## 浏览器参数

根据需要将以下参数添加到 `/browser` 查询字符串中：

| 参数 | 参数值 | 默认值 | 使用场景 |
|-----------|--------|---------|----------|
| `format` | `rendered`、`raw` | `rendered` | 使用 `raw` 可跳过 JavaScript 渲染（速度更快） |
| `expiration` | `0` 到 N（天） | `1` | 设置为 `0` 可绕过缓存 |
| `delay` | `0.1` 到 `10`（秒） | 无 | 如果页面需要更多时间加载动态内容，请设置此参数 |
| `device` | 设备名称字符串 | `desktop` | 需要针对移动设备的特定内容 |
| `ip` | `residential`、`isp` | `residential` | 使用民用 IP 可降低被检测到的概率 |

**带浏览器参数的示例：**

```bash
curl --proto =https -s -G --data-urlencode "url=THE_URL" \
  -H "Authorization: Bearer $MASSIVE_UNBLOCKER_TOKEN" \
  "https://unblocker.joinmassive.com/browser?expiration=0&delay=2"
```

## 错误处理
- **401 Unauthorized** — 令牌无效或缺失。告知用户：“您的 ClawPod API 令牌似乎无效或已过期。您可以在 **clawpod.joinmassive.com** 获取新的令牌。”
- **空响应** — 页面可能需要更多时间来渲染。尝试使用 `delay=3` 重试。如果仍然没有响应，尝试使用 `format=rendered`（默认设置）。告知用户：“页面加载缓慢——我已经增加了延迟时间。”
- **超时或连接错误** — 有些页面加载非常慢。告知用户请求超时，并提供重试选项。不要直接失败。

## 提示
- 如果内容与预期不同，可以尝试使用 `device=mobile` 来获取移动设备版本的内容。
- 如果需要获取之前请求过的 URL 的最新结果，可以使用 `expiration=0` 来绕过缓存。
- 如果内容仍然被屏蔽，可以尝试使用 `ip=isp`（使用 ISP 级别的 IP 地址）。
- 如果页面包含大量动态内容（如单页应用程序或无限滚动页面），可以增加 `delay` 以延长渲染时间。

## 规则
- **每次请求只返回一个结果**。结果会直接包含在输出中，不要重复请求相同的 URL。
- **始终对目标 URL 进行 URL 编码。**
- **处理多个 URL 时请依次进行请求，不要并行请求。**
- **每次请求的超时时间为 2 分钟**。如果页面或搜索响应缓慢，可能是由于 API 处理重试或验证码的原因。
- **搜索结果建议使用 `format=json`。** 对于搜索结果，结构化 JSON 比 HTML 更适合处理。
- **在 `terms` 参数中，使用 `+` 或 `%20` 替换空格来对搜索词进行编码。**