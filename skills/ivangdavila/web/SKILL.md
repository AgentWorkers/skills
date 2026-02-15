---
name: Web Development
description: 使用 HTML、CSS、JavaScript、现代框架以及最佳实践来构建、调试和部署网站。
---
## 快速参考

| 需要帮助的内容 | 参考文档 |
|------|-----|
| HTML/CSS 相关问题 | `html-css.md` |
| JavaScript 模式 | `javascript.md` |
| React/Next.js/相关框架 | `frameworks.md` |
| 部署到生产环境 | `deploy.md` |
| 性能/SEO/无障碍访问 | `performance.md` |

## 重要规则

1. **`DOCTYPE` 的重要性** — 缺少 `<!DOCTYPE html>` 会触发“怪异模式”（quirks mode），导致布局行为不可预测。
2. **CSS 的特异性优先于层叠规则** — `.class` 选择器会覆盖元素选择器，无论它们的顺序如何。
3. **使用 `===` 而不是 `==`** — 类型强制转换会导致 `"0" == false` 的结果为 `true`。
4. **循环中的异步操作** — `forEach` 不会等待异步操作完成；请使用 `for...of` 或 `Promise.all`。
5. **CORS 是服务器端的问题** — 无法通过客户端解决；需要在服务器上配置 `Access-Control-Allow-Origin`。
6. **响应式布局** — 必须添加 `<meta name="viewport">` 标签；否则移动设备会显示桌面页面的宽度。
7. **表单提交时需要阻止默认行为** — 需要在提交处理函数中调用 `e.preventDefault()`。
8. **图片需要指定尺寸** — 如果缺少 `width` 或 `height`，会导致布局错位（影响页面的视觉效果）。
9. **使用 HTTPS** — 如果页面中包含 HTTP 资源，浏览器可能会阻止这些资源的加载。
10. **环境变量泄露** — 使用 `NEXT_PUBLIC_*` 变量会暴露敏感信息；切勿在变量前添加前缀。

## 常见问题解答

- **如何实现响应式布局？** 使用媒体查询（media queries）来创建以移动设备优先的 CSS；在 320px、768px、1024px 等不同屏幕尺寸下进行测试。
- **如何部署到生产环境？** 请参考 `deploy.md` 中关于 Vercel、Netlify 或 VPS 的部署指南。
- **如何解决 CORS 错误？** 服务器必须正确设置响应头；如果无法控制服务器，请使用代理来处理跨源请求。
- **如何提升页面性能？** 使用 Lighthouse 工具进行性能审计，重点优化 LCP（内容加载时间）、CLS（布局 Shift）、FID（First Input Delay）等指标；对非可视区域的图片使用懒加载技术。
- **如何优化 SEO？** 为每个页面设置合适的标题和描述，使用语义化的 HTML 结构，添加 OG 标签，并生成 sitemap.xml 文件。

## 框架选择指南

- **静态内容，快速构建** — 可以选择 Astro 或纯 HTML。
- **包含 MDX 的博客/文档** — 可以使用 Astro 或 Next.js 的 App Router 功能。
- **需要身份验证的交互式应用** — 可以选择 Next.js 或 Remix。
- **需要完全控制服务器端渲染（SSR）/客户端渲染（ISR）** — Next.js 是最佳选择。
- **简单的单页应用（SPA），无需 SEO** — 可以使用 Vite 结合 React/Vue 进行开发。