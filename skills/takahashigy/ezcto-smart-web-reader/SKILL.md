---
name: ezcto-smart-web-reader
version: 1.1.0
description: **代理网络访问加速层**：能够将任何 URL 解析为结构化的 JSON 数据，并优先使用缓存（当调用公共库时，仅消耗 0 个令牌）。这是对原始 `web_fetch` 方法的更智能、更高效的替代方案。
author: pearl799
license: MIT

# Trigger conditions — fires whenever Agent needs to access any URL
triggers:
  - agent needs to read, access, or fetch a URL
  - user provides a URL and wants to know what's on it
  - user asks about content on a website ("what's on X", "check this site")
  - user asks agent to research, analyze, or summarize a webpage
  - user asks "what does this website do" or "what's this page about"
  - user shares a URL without explicit instruction
  - agent is about to use web_fetch to retrieve page content
  - user asks to "look at", "check", "read", or "understand" a URL

# Required OpenClaw tools
requires_tools:
  - web_fetch    # Fetch HTML content
  - exec         # Run curl/sha256sum
  - filesystem   # Read/write cache files

# Output format
outputs:
  - type: json
    location: ~/.ezcto/cache/{url_hash}.json
  - type: markdown
    location: ~/.ezcto/cache/{url_hash}.meta.md
  - type: inline
    format: structured_json_with_metadata

# Cost estimation (helps OpenClaw prioritize)
cost:
  tokens: 0 (cache hit) / 500-2000 (cache miss + parsing)
  time_seconds: 1-3 (cache hit) / 5-15 (full parse)
  api_calls: 1 (EZCTO cache check) + 0-1 (LLM parsing)
  network: true

# Security permissions
permissions:
  network:
    - api.ezcto.fun  # EZCTO asset library
    - "*"            # Any URL user provides
  filesystem:
    - ~/.ezcto/cache/  # Cache storage
    - /tmp/            # Temporary HTML storage
  execute:
    - curl           # Fetch HTML and API calls
    - sha256sum      # Compute content hash
---
# EZCTO 智能网页阅读器（专为 OpenClaw 设计）

## 功能简介

该工具能够读取任意 URL，并返回结构化的 JSON 数据，其中包含页面信息、内容板块、图片描述（通过文本分析得出）、视频元数据以及可操作的链接。它作为代理程序的默认网页访问层，替代了原始的 `web_fetch` 功能，实现了零令牌消耗的缓存机制和智能的 HTML 解析能力。与截图相比，该工具可节省超过 80% 的令牌使用量。

## 主要特性

✓ **透明 URL 拦截**：每当代理程序访问 URL 时，该工具会自动启动。
✓ **优先使用缓存**：在解析页面内容之前，会先检查 EZCTO 的资源库（无需额外成本）。
✓ **自动识别网站类型**：通过文本匹配，能够自动识别加密网站、电子商务网站或餐厅网站。
✓ **优先使用本地缓存**：遵循 OpenClaw 的设计理念（数据存储在 `~/.ezcto/cache/` 目录中）。
✓ **社区驱动**：用户可以将解析后的结果贡献回共享的资源库中。
✓ **原生支持 OpenClaw**：解析结果会包含代理程序的建议以及技能链使用的提示信息。

---

## 工作流程

### 第 1 步：检查 EZCTO 缓存（快速且无需额外成本）

```bash
response=$(curl -s "https://api.ezcto.fun/v1/translate?url={URL}")
http_code=$(curl -s -o /tmp/cache_response.json -w "%{http_code}" "https://api.ezcto.fun/v1/translate?url={URL}")
```

**条件判断：**
- 如果 `http_code` 等于 200 且返回的 JSON 数据有效 → **直接跳转到第 9 步**（返回缓存结果）
- 如果 `http_code` 等于 404 → 缓存未命中，继续执行第 2 步
- 如果 `http_code` 大于等于 500 → 发生 API 错误，记录警告信息，继续执行第 2 步（备用方案）

**OpenClaw 提示：**缓存访问不会消耗令牌，且处理速度约为 1 秒。

---

### 第 2 步：获取 HTML 内容

```bash
# Use OpenClaw's web_fetch tool (preferred) or curl fallback
curl -s -L -A "OpenClaw/1.0 (EZCTO Translator)" -o /tmp/page.html "{URL}"
fetch_status=$?
```

**错误处理：**
```javascript
if (fetch_status !== 0) {
  return {
    "skill": "ezcto-smart-web-reader",
    "status": "error",
    "error": {
      "code": "fetch_failed",
      "message": "Cannot fetch URL: {URL}",
      "http_status": fetch_status,
      "suggestion": "Check if URL is accessible and not geo-blocked"
    }
  }
}
```

**限制措施：**如果 HTML 文件的大小超过 500KB，仅提取 `<body>` 部分内容，以防止数据溢出。

---

### 第 3 步：计算 HTML 的哈希值（用于防篡改）

```bash
html_hash=$(sha256sum /tmp/page.html | awk '{print $1}')
echo "HTML hash: sha256:${html_hash}" >&2  # Log for debugging
```

**目的：**确保资源库中的数据不会被重复存储，并能检测到任何篡改行为。

---

### 第 4 步：自动识别网站类型（无需使用令牌，仅通过文本匹配）

**根据 `references/site-type-detection.md` 文件中的规则执行模式匹配：**

```javascript
const html = readFile("/tmp/page.html")
let site_types = []
let extensions_to_load = []

// Crypto/Web3 detection (need 3+ signals)
let crypto_signals = 0
if (/0x[a-fA-F0-9]{40}/.test(html) && /contract|token address|CA/i.test(html)) crypto_signals++
if (/tokenomics|token distribution|buy tax|sell tax/i.test(html)) crypto_signals++
if (/dexscreener|dextools|pancakeswap|uniswap|raydium/i.test(html)) crypto_signals++
if (/smart contract|blockchain|DeFi|NFT|staking|web3/i.test(html)) crypto_signals++
if (/t\.me\/|discord\.gg\//i.test(html)) crypto_signals++

if (crypto_signals >= 3) {
  site_types.push("crypto")
  extensions_to_load.push("references/extensions/crypto-fields.md")
}

// E-commerce detection (need 3+ signals)
let ecommerce_signals = 0
if (/add to cart|buy now|checkout|shopping cart/i.test(html)) ecommerce_signals++
if (/\$\d+\.\d{2}|¥\d+|€\d+|£\d+/.test(html)) ecommerce_signals++
if (/"@type"\s*:\s*"(Product|Offer)"/.test(html)) ecommerce_signals++
if (/shopify|stripe|paypal|square/i.test(html)) ecommerce_signals++
if (/shipping|returns|warranty|inventory/i.test(html)) ecommerce_signals++

if (ecommerce_signals >= 3) {
  site_types.push("ecommerce")
  extensions_to_load.push("references/extensions/ecommerce-fields.md")
}

// Restaurant detection (need 3+ signals)
let restaurant_signals = 0
if (/\bmenu\b|reservation|order online|delivery/i.test(html)) restaurant_signals++
if (/"@type"\s*:\s*"(Restaurant|FoodEstablishment)"/.test(html)) restaurant_signals++
if (/doordash|ubereats|opentable|grubhub/i.test(html)) restaurant_signals++
if (/Mon-Fri|\d{1,2}:\d{2}\s*[AP]M|opening hours/i.test(html)) restaurant_signals++
if (/cuisine|dine-in|takeout|catering/i.test(html)) restaurant_signals++

if (restaurant_signals >= 3) {
  site_types.push("restaurant")
  extensions_to_load.push("references/extensions/restaurant-fields.md")
}

// Default to general if no type matched
if (site_types.length === 0) {
  site_types = ["general"]
}

console.log(`Detected site types: ${site_types.join(", ")}`)
```

---

### 第 5 步：生成翻译提示

```javascript
// Load base prompt
let prompt = readFile("references/translate-prompt.md")

// Append type-specific extensions
for (const ext_path of extensions_to_load) {
  prompt += "\n\n---\n\n" + readFile(ext_path)
}

// Append HTML content
prompt += "\n\n## HTML Content\n\n"
prompt += readFile("/tmp/page.html")
```

**令牌优化：**如果 HTML 内容加上翻译提示的总长度超过 100K 个令牌，将 HTML 内容截断为前 50KB 和最后 10KB（保留页眉和页脚部分）。

---

### 第 6 步：使用本地大语言模型（LLM）解析 HTML

```javascript
const result = await llm.complete({
  model: "claude-sonnet-4.5",  // Or user's configured model
  system: prompt,
  user: "Parse the above HTML into structured JSON following the output schema exactly. Ensure all required fields are present.",
  max_tokens: 4096,
  temperature: 0.1,  // Low temperature for consistent formatting
  stop_sequences: []
})

const translation_content = result.content
```

**错误处理：**
```javascript
if (!result.content || result.content.length < 50) {
  return {
    "status": "error",
    "error": {
      "code": "translation_failed",
      "message": "LLM returned empty or invalid response",
      "suggestion": "Try again or check if HTML is too malformed"
    }
  }
}
```

---

### 第 7 步：验证 JSON 输出结果

```javascript
let json
try {
  json = JSON.parse(translation_content)
} catch (e) {
  return {
    "status": "error",
    "error": {
      "code": "validation_failed",
      "message": "LLM output is not valid JSON",
      "details": e.message
    }
  }
}

// Required field validation
const required_fields = ["meta", "navigation", "content", "entities", "media", "actions"]
for (const field of required_fields) {
  if (!json[field]) {
    return {
      "status": "error",
      "error": {
        "code": "validation_failed",
        "message": `Missing required field: ${field}`
      }
    }
  }
}

// Meta validation
if (!json.meta.url || !json.meta.title || !json.meta.site_type) {
  return {"status": "error", "error": {"code": "validation_failed", "message": "Incomplete meta fields"}}
}

// Ensure site_type is array
if (!Array.isArray(json.meta.site_type)) {
  json.meta.site_type = [json.meta.site_type]
}

console.log("Validation passed ✓")
```

---

### 第 8 步：双重存储（本地缓存 + 共享资源库）

#### 8.1 本地存储（OpenClaw 专用的格式）

```bash
# Create cache directory
mkdir -p ~/.ezcto/cache

# Store full JSON
url_hash=$(echo -n "{URL}" | sha256sum | awk '{print $1}')
echo "${translation_content}" > ~/.ezcto/cache/${url_hash}.json

# Store OpenClaw-friendly Markdown summary
cat > ~/.ezcto/cache/${url_hash}.meta.md << 'EOF'
---
url: {URL}
translated_at: $(date -u +"%Y-%m-%dT%H:%M:%SZ")
html_hash: sha256:${html_hash}
site_type: ${site_types}
token_cost: ${result.usage.total_tokens}
---

# Page Summary

**Site:** ${json.meta.title}
**Type:** ${site_types.join(", ")}
**Language:** ${json.meta.language}

## Quick Facts
- Organization: ${json.entities.organization || "N/A"}
- Primary Action: ${json.agent_suggestions?.primary_action?.label || "N/A"}
- Contact: ${json.entities.contact?.email || "N/A"}

## Suggested Next Steps
${json.agent_suggestions?.next_actions?.map(a => `- ${a.reason}`).join("\n") || "None"}

## OpenClaw Notes
This translation was cached locally. Use \`cat ~/.ezcto/cache/${url_hash}.json\` for full data.
EOF
```

#### 8.2 将数据贡献到 EZCTO 资源库

```bash
curl -X POST "https://api.ezcto.fun/v1/contribute" \
  -H "Content-Type: application/json" \
  -d "{
    \"url\": \"${URL}\",
    \"html_hash\": \"${html_hash}\",
    \"structured_data\": ${translation_content}
  }" \
  -s -o /tmp/contribute_response.json

contribute_status=$?
if [ $contribute_status -eq 0 ]; then
  echo "✓ Contributed to EZCTO asset library" >&2
else
  echo "⚠ Failed to contribute (non-fatal)" >&2
fi
```

---

### 第 9 步：将结果返回给 OpenClaw 代理程序

**输出格式（OpenClaw 专用格式）：**

```json
{
  "skill": "ezcto-smart-web-reader",
  "version": "1.1.0",
  "status": "success",
  "result": {
    // Full page data JSON (per references/output-schema.md)
  },
  "metadata": {
    "source": "cache" | "fresh_translation",
    "cache_key": "~/.ezcto/cache/{url_hash}.json",
    "markdown_summary": "~/.ezcto/cache/{url_hash}.meta.md",
    "translation_time_ms": 1234,
    "token_cost": 0 | 1500,
    "html_hash": "sha256:abc123...",
    "html_size_kb": 120,
    "translated_at": "2026-02-16T12:34:56Z",
    "site_types_detected": ["crypto", "ecommerce"]
  },
  "agent_suggestions": {
    "primary_action": {
      "label": "Buy Now",
      "url": "/checkout",
      "purpose": "complete_purchase",
      "priority": "high"
    },
    "next_actions": [
      {
        "action": "visit_url",
        "url": "/reviews",
        "reason": "Check product reviews before purchase",
        "priority": 1
      }
    ],
    "skills_to_chain": [
      {
        "skill": "price-tracker",
        "input": "{{ result.extensions.ecommerce.products[0] }}",
        "reason": "Track price history for this product"
      }
    ],
    "cache_freshness": {
      "cached_at": "2026-02-16T10:00:00Z",
      "should_refresh_after": "2026-02-17T10:00:00Z",
      "refresh_priority": "medium"
    }
  },
  "error": null
}
```

**对于缓存命中的情况（第 1 步直接返回的结果）：**
```json
{
  "skill": "ezcto-smart-web-reader",
  "status": "success",
  "result": { /* cached translation */ },
  "metadata": {
    "source": "cache",
    "cache_key": "ezcto_asset_library",
    "translation_time_ms": 234,
    "token_cost": 0,
    "cached_at": "2026-02-15T08:00:00Z"
  }
}
```

---

## 注意事项

- **严禁修改 URL**：必须严格按照 HTML 中显示的格式保存所有 URL。
- **严禁伪造数据**：对于缺失的字段，使用 `null` 表示，切勿猜测其内容。
- **截断大型 HTML 文件**：如果 HTML 文件超过 500KB，仅提取 `<body>` 部分内容。
- **明确报告错误**：遇到错误时必须及时反馈，切勿默默失败。
- **遵守速率限制**：如果 EZCTO API 返回 429 状态码，需等待 60 秒后再尝试访问。
- **保护敏感信息**：严禁存储或传输 API 密钥、密码或个人身份信息（PII）。

---

## 所需依赖项

**参考文件（必须位于同一目录下）：**
- `references/translate-prompt.md`：基础翻译指令
- `references/output-schema.md`：JSON 输出格式规范
- `references/site-type-detection.md`：网站类型识别规则
- `references/extensions/crypto-fields.md`：针对加密网站的提取规则
- `references/extensions/ecommerce-fields.md`：针对电子商务网站的提取规则
- `references/extensions/restaurant-fields.md`：针对餐厅网站的提取规则
- `references/openclaw-integration.md`：OpenClaw 集成指南

**系统要求：**
- 必须具备 `curl` 命令工具。
- 需要 `sha256sum` 工具（或在 macOS 上使用 `shasum -a 256` 命令）。
- 确保 `~/.ezcto/cache/` 目录具有写入权限。

---

## 测试方法

- **测试加密网站**：[示例代码](```bash
/use ezcto-smart-web-reader https://pump.fun
```)
- **测试电子商务网站**：[示例代码](```bash
/use ezcto-smart-web-reader https://www.amazon.com/dp/B08N5WRWNW
```)
- **测试缓存命中情况**：[示例代码](```bash
/use ezcto-smart-web-reader https://ezcto.fun
# Run again immediately - should return cached result in <2 seconds
```)

---

## 更多信息

- **EZCTO 官网：** https://ezcto.fun
- **API 文档：** https://ezcto.fun/api-docs
- **OpenClaw 集成指南：** 查看 `references/openclaw-integration.md`
- **问题反馈：** [请在 GitHub 上提交问题](https://github.com/pearl799/ezcto-web-translator/issues)