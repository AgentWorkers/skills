---
name: agorahub
version: "1.0.0"
description: "AgoraHub 代理注册表：您可以发现并使用 14 种以上经过验证的 AI 代理，用于执行哈希计算、编码、格式化等开发任务。试用这些代理无需注册。"
metadata:
  openclaw:
    emoji: "🌐"
    requires:
      bins: ["curl", "jq"]
      env: ["AGORAHUB_API_KEY"]
    primaryEnv: "AGORAHUB_API_KEY"
---

# AgoraHub — 人工智能代理注册平台

AgoraHub 是一个开放的代理注册平台，提供了 14 个经过验证的演示代理，您可以立即使用它们，无需注册。对于社区代理，您可以在 [https://agorahub.dev/dashboard/api-keys](https://agorahub.dev/dashboard/api-keys) 获取 API 密钥。

**基础 URL：** `https://agorahub.dev`

---

## 1. 发现可用代理

列出所有作为 MCP 工具提供的代理：

```bash
curl -s https://agorahub.dev/api/mcp/tools | jq '.tools[] | {name, description}'
```

### 按标签筛选

```bash
curl -s "https://agorahub.dev/api/mcp/tools?tags=crypto" | jq '.tools[] | {name, description}'
```

### 按名称/描述搜索

```bash
curl -s "https://agorahub.dev/api/mcp/tools?q=hash" | jq '.tools[] | {name, description}'
```

---

## 2. 调用代理

所有 14 个演示代理都不需要 API 密钥即可使用。对于社区代理，请添加 `-H "Authorization: Bearer $AGORAHUB_API_KEY"`。

### 通用调用格式

```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_<agent-slug>_<skill-id>","arguments":{...}}' | jq
```

---

## 3. 代理快速参考

### Echo 代理
回显带有时间戳的消息。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_echo-agent_echo","arguments":{"message":"hello world"}}' | jq
```

### 哈希生成器
生成加密哈希（md5、sha1、sha256、sha512）。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_hash-generator_hash","arguments":{"text":"hello","algorithm":"sha256"}}' | jq
```

**同时使用所有算法生成哈希：**
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_hash-generator_hash-all","arguments":{"text":"hello"}}' | jq
```

### 密码生成器
生成具有可定制选项的安全密码。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_password-generator_generate","arguments":{"length":20,"count":3,"symbols":true}}' | jq
```

### JSON 格式化器
验证、美化或压缩 JSON 数据。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_json-formatter_format","arguments":{"json":"{\"key\":\"value\",\"num\":42}"}}' | jq
```

### Base64 编码器
将文本编码为 Base64 格式：
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_base64-codec_encode","arguments":{"text":"hello world"}}' | jq
```

**将 Base64 编码解码回文本：**
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_base64-codec_decode","arguments":{"text":"aGVsbG8gd29ybGQ="}}' | jq
```

### UUID 生成器
生成 v4 或 v7 格式的 UUID。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_uuid-generator_generate","arguments":{"version":"v4","count":5}}' | jq
```

### 正则表达式测试器
测试文本中的正则表达式模式。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_regex-tester_test","arguments":{"pattern":"\\d+","text":"abc 123 def 456"}}' | jq
```

### JWT 解码器
解码 JWT 令牌（不进行验证）。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_jwt-decoder_decode","arguments":{"token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"}}' | jq
```

### Markdown 转 HTML
将 Markdown 文本转换为 HTML。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_markdown-to-html_convert","arguments":{"markdown":"# Hello\n\n**Bold** and *italic*"}}' | jq
```

### 文本统计
分析文本的单词数量、阅读时间等信息。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_text-stats_analyze","arguments":{"text":"The quick brown fox jumps over the lazy dog. This is a sample text for analysis."}}' | jq
```

###Lorem Ipsum 生成器
生成占位文本。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_lorem-ipsum_generate","arguments":{"format":"paragraphs","count":2}}' | jq
```

### CSV/JSON 转换器
将 CSV 转换为 JSON：
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_csv-json-converter_csv-to-json","arguments":{"csv":"name,age\nAlice,30\nBob,25"}}' | jq
```

将 JSON 转换为 CSV：
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_csv-json-converter_json-to-csv","arguments":{"data":[{"name":"Alice","age":30},{"name":"Bob","age":25}]}}' | jq
```

### 颜色转换器
在十六进制、RGB 和 HSL 之间转换颜色。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_color-converter_convert","arguments":{"color":"#ff6600"}}' | jq
```

### 时间戳转换器
在 Unix 时间戳、ISO 8601 和人类可读日期之间进行转换。
```bash
curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_timestamp-converter_convert","arguments":{"timestamp":"now"}}' | jq
```

---

## 4. 错误处理

检查响应中的 HTTP 状态码和 `isError` 字段：

- **200** — 成功。解析 `content[0].text` 以获取结果。
- **400** — 请求错误。查看 `error` 字段以获取详细信息（工具名称缺失、格式无效）。
- **401** — 需要身份验证。仅适用于非演示代理。设置 `AGORAHUB_API_KEY`。
- **404** — 未找到代理或技能。使用发现端点来列出可用工具。
- **429** — 请求次数受限。查看 `Retry-After` 头部字段。
- **500** — 内部错误。重试或在 [https://github.com/Codevena/AgoraHub/issues](https://github.com/Codevena/AgoraHub/issues) 报告问题。

```bash
# Example: check for errors
RESPONSE=$(curl -s -w "\n%{http_code}" -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name":"agora_echo-agent_echo","arguments":{"message":"test"}}')
HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | head -n -1)

if [ "$HTTP_CODE" -ne 200 ]; then
  echo "Error ($HTTP_CODE): $(echo "$BODY" | jq -r '.error // .content[0].text')"
else
  echo "$BODY" | jq '.content[0].text | fromjson'
fi
```

---

## 5. 使用 API 密钥（社区代理）

对于非演示代理，请使用您的 API 密钥进行身份验证：

```bash
export AGORAHUB_API_KEY="agora_your_key_here"

curl -s -X POST https://agorahub.dev/api/mcp/tools/call \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $AGORAHUB_API_KEY" \
  -d '{"name":"agora_some-community-agent_skill","arguments":{...}}' | jq
```

您可以在 [https://agorahub.dev/dashboard/api-keys](https://agorahub.dev/dashboard/api-keys) 获取 API 密钥。