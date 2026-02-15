---
name: mdnew
description: 使用 `markdown.new` 服务从任何 URL 获取经过优化处理的 Markdown 内容。当 `web_fetch` 或浏览器无法提供干净、无错误的 Markdown 内容时，或者需要一个用于深度分析的、占用资源较少的网页版本时，可以使用此方法。
---

# mdnew

使用 `markdown.new` 三层转换流程（头部信息处理 -> 工作节点 AI 处理 -> 浏览器渲染）从任意 URL 获取纯净的 Markdown 内容。

## 使用方法

使用目标 URL 运行该脚本：

```bash
python3 scripts/mdnew.py <url>
```

## 为什么使用 mdnew？

1. **代码效率**：与原始 HTML 相比，可将内容大小减少 80%。
2. **数据纯净**：去除样板代码、广告和导航菜单，仅保留核心内容。
3. **JavaScript 处理**：通过 Cloudflare 浏览器渲染功能自动处理包含大量 JavaScript 的页面。
4. **以用户代理为优先**：包含 `x-markdown-tokens` 标记，有助于管理上下文窗口。