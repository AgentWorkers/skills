---
name: HTML
description: 避免常见的HTML错误——这些错误可能导致可访问性问题、表单使用上的陷阱以及搜索引擎优化（SEO）方面的疏漏。
metadata: {"clawdbot":{"emoji":"🌐","os":["linux","darwin","win32"]}}
---

## 防止布局偏移
- 即使使用了CSS来设置 `<img>` 的 `width` 和 `height`，浏览器仍会在图片加载前预留相应的显示空间。
- 当图片没有明确的尺寸时，可以使用 CSS 中的 `aspect-ratio` 属性作为备用方案，以实现响应式布局。

## 表单相关注意事项
- `autocomplete` 属性具有特定的含义，例如 `autocomplete="email"` 或 `autocomplete="new-password"`，而不仅仅是简单的 `on/off` 模式。
- 对于单选框或复选框组，必须同时使用 `<fieldset>` 和 `<legend>`，这样屏幕阅读器才能正确读取组标题。
- `inputmode` 属性用于控制虚拟键盘的显示方式，例如 `inputmode="numeric"` 会显示数字键盘（且不进行任何验证）。
- `enterkeyhint` 属性可以改变移动设备键盘上的按键显示文本，例如 `enterkeyhint="search"` 或 `enterkeyhint="send"`。

## 可访问性方面的问题
- 跳过链接（`<a href="#main" class="skip">跳转到内容</a>`）必须是页面中第一个可聚焦的元素，位于导航栏之前。
- 使用 `<th scope="col">` 或 `scope="row>` 可以确保屏幕阅读器能够正确识别表格中的标题。
- `aria-hidden="true"` 用于隐藏不可交互的装饰性图标，而不是交互式元素。
- 对于仅用于布局的表格，应使用 `role="presentation"` 属性（不过实际上应尽量避免使用表格）。

## 链接安全
- 当使用 `target="_blank"` 时，必须同时设置 `rel="noopener noreferrer"`：`noopener` 可防止外部脚本通过 `window.opener` 打开链接，`noreferrer` 可隐藏链接的来源信息。
- 用户生成的链接应添加 `rel="nofollow ugc"` 标签，以告知搜索引擎这些链接是用户自己创建的内容。

## SEO 相关设置
- 使用 `<link rel="canonical"` 可避免页面内容重复；每个页面都应设置指向自身内容的canonical链接。
- `og:image` 标签中的图片路径必须是绝对路径，因为相对路径在社交媒体平台上可能无法正确显示。
- `twitter:card` 标签的属性值（`summary`、`summary_large_image`、`player`）是有特定含义的，不能随意设置。

## 常见的问题和疏忽
- 使用 `<button type="button">` 可以防止按钮被误认为是表单提交按钮（默认情况下，`<button>` 的类型是 `type="submit"`，会触发表单提交）。
- `<dialog>` 元素用于创建模态窗口，它自带焦点捕获和退出处理机制。
- 使用 `<details>` 和 `<summary>` 可以创建折叠式内容，这些元素默认就是可访问的，无需额外的 JavaScript 代码。
- 空元素（如 `<img>`）在 HTML5 中不需要加上闭合斜杠（`<img>` 和 `<img />` 都是有效的）。