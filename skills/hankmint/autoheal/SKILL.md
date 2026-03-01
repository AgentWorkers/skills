---
name: autoheal
version: 1.0.0
description: 为任何项目添加基于人工智能的错误监控和自动修复功能。
requires:
  env:
    - AUTOHEAL_API_KEY
---
# AutoHeal AI 技能

AutoHeal 能够捕获 JavaScript/TypeScript 代码在生产环境中出现的错误，利用人工智能进行分析，并生成针对特定平台的修复建议，这些修复建议可以直接粘贴到您的 AI 编码工具中。

## 1. 在项目中设置 AutoHeal

### 浏览器项目（React、Next.js、Vue、Svelte 等）

将以下代码片段添加到您的应用程序的入口文件中（例如 `main.tsx`、`layout.tsx`、`App.vue`）：

```html
<script>
window.onerror = function(msg, source, line, col, err) {
  fetch("https://autohealai.com/api/errors/ingest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      key: process.env.AUTOHEAL_API_KEY || "YOUR_API_KEY",
      message: msg,
      stack: err?.stack || "",
      source_url: source,
      browser: navigator.userAgent
    })
  }).catch(() => {});
};

window.onunhandledrejection = function(e) {
  const err = e.reason;
  fetch("https://autohealai.com/api/errors/ingest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      key: process.env.AUTOHEAL_API_KEY || "YOUR_API_KEY",
      message: err?.message || String(err),
      stack: err?.stack || "",
      source_url: window.location.href,
      browser: navigator.userAgent
    })
  }).catch(() => {});
};
</script>
```

### Node.js / 服务器项目

将以下代码片段添加到您的服务器入口文件中：

```javascript
process.on('uncaughtException', (err) => {
  fetch("https://autohealai.com/api/errors/ingest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      key: process.env.AUTOHEAL_API_KEY,
      message: err.message,
      stack: err.stack || ""
    })
  }).catch(() => {});
});

process.on('unhandledRejection', (reason) => {
  const err = reason instanceof Error ? reason : new Error(String(reason));
  fetch("https://autohealai.com/api/errors/ingest", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      key: process.env.AUTOHEAL_API_KEY,
      message: err.message,
      stack: err.stack || ""
    })
  }).catch(() => {});
});
```

## 2. 检查错误状态

错误被捕获后，您可以查看其分析状态：

```bash
curl -s "https://autohealai.com/api/errors/{ERROR_ID}/status" \
  -H "Authorization: Bearer $AUTOHEAL_API_KEY"
```

响应内容：
```json
{
  "status": "analyzed",
  "message": "Cannot read properties of undefined",
  "has_fix": true,
  "fix_id": "uuid-here",
  "dashboard_url": "https://autohealai.com/dashboard/errors/{ERROR_ID}"
}
```

可能的错误状态：`new`（新错误）、`analyzing`（正在分析中）、`analyzed`（分析完成）、`fix_applied`（修复已应用）、`ignored`（被忽略）

您可以在 `dashboard_url` 查看包含 AI 生成修复建议的完整错误信息。

## 3. 手动报告错误

您可以直接将任何错误信息发送给 AutoHeal：

```bash
curl -X POST "https://autohealai.com/api/errors/ingest" \
  -H "Content-Type: application/json" \
  -d '{
    "key": "'$AUTOHEAL_API_KEY'",
    "message": "TypeError: Cannot read properties of undefined (reading '\''map'\'')",
    "stack": "TypeError: Cannot read properties of undefined\n    at renderList (src/components/List.tsx:15:23)"
  }'
```

响应内容：
```json
{
  "status": "queued",
  "error_id": "uuid-here"
}
```

系统会在几秒钟内利用人工智能分析该错误。请使用响应中的 `error_id` 来查看错误的状态。