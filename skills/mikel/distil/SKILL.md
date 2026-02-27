---
name: distil
description: 将网页内容提取为纯净的 Markdown 格式，并通过 distil.net 代理服务器进行网络搜索。
version: 2.0.1
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins:
        - "curl"
      env:
        - "DISTIL_API_KEY"
    primaryEnv: "DISTIL_API_KEY"
---
# Distil Skill

该工具为代理提供了易于发现且一致的使用方式——无需手动构建URL，也无需记忆请求头或API密钥。Distil能够将网页内容转换为简洁的Markdown格式，从而为大型语言模型（LLM）节省60%–80%的处理所需资源。

## 设置

1. 从https://distil.net获取免费的API密钥（需通过电子邮件验证）；或使用您已有的API密钥。
2. 设置`DISTIL_API_KEY`环境变量。
3. （可选）设置`DISTIL_PROXY_URL`（默认值为`https://proxy.distil.net`，适用于自托管环境）。

## 命令

```bash
# Fetch any URL as clean Markdown
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/https://example.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY"

# Search the web and get results as Markdown
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/search?q=best+practices+for+Go+error+handling" \
  -H "X-Distil-Key: $DISTIL_API_KEY" \
  -H "Accept: text/markdown"

# Take a screenshot of a web page and return it as an image
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/screenshot/https://example.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY" > screenshot.png

# Render a web page (such as a single page javascript app) before trying to extract markdown
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/render/https://example.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY"

# Fetch a URL and return its raw content bypassing any attempt to render markdown
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/raw/https://example.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY"

# Fetch a URL and return its content without using the cache
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/nocache/https://example.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY"
```

## 参数

| 环境变量 | 默认值 | 说明 |
|---------------------|---------|-------------|
| `DISTIL_API_KEY` | （无，但必需） | API密钥 |
| `DISTIL_PROXY_URL` | `https://proxy.distil.net` | 代理基础URL（自托管环境可自定义） |

## 输出结果

- 响应结果会直接输出到标准输出（stdout）。
- 如果出现HTTP错误（非2xx状态码），系统会附带错误信息返回。

## 示例

```bash
# Research a topic
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/search?q=OpenClaw+agent+framework" \
  -H "X-Distil-Key: $DISTIL_API_KEY" \
  -H "Accept: text/markdown"

# Read documentation
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/https://docs.github.com/en/rest" \
  -H "X-Distil-Key: $DISTIL_API_KEY"

# Force fresh fetch (bypass cache)
curl -s "${DISTIL_PROXY_URL:-https://proxy.distil.net}/nocache/https://news.ycombinator.com" \
  -H "X-Distil-Key: $DISTIL_API_KEY"
```

## 备用方案——直接使用curl

如果您更喜欢直接调用代理服务，可以参考以下示例：

```bash
# Fetch a page
curl -s "https://proxy.distil.net/https://example.com" \
  -H "X-Distil-Key: YOUR_API_KEY"

# Search the web
curl -s "https://proxy.distil.net/search?q=your+query" \
  -H "X-Distil-Key: YOUR_API_KEY" \
  -H "Accept: text/markdown"
```

## 注意事项

所有以Markdown格式返回的响应都会显示Distil在转换过程中节省了多少原始数据（即多少“令牌”）。这样您就能实时了解转换的效率。Distil生成的Markdown内容经过优化，去除了不必要的HTML代码和冗余内容，仅保留您所需的信息。与原始HTML相比，这种方式可以节省60%–80%的处理资源，从而显著提升大型语言模型的处理效率。

如果您用完了令牌，Distil会直接返回原始HTML内容，这样即使超出令牌限制，您仍然可以访问相关信息。不过在这种情况下，系统会在网页中插入一条提示信息，告诉您如何解决令牌不足的问题。