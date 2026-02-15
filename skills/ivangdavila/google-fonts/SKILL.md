---
name: Google Fonts
description: 以适当的性能加载 Google 字体，实现字体子集化，并使用经过验证的字体搭配方案。
metadata: {"clawdbot":{"emoji":"🔤","requires":{},"os":["linux","darwin","win32"]}}
---

## 加载字体时常见的错误

- 如果缺少 `display=swap` 属性，字体在加载完成前将不可见——务必将其添加到 URL 中。
- 只加载实际使用的字体权重：例如 `wght@400;600;700`，而不要加载整个字体系列；每个未使用的字体权重都会占用约 20KB 的磁盘空间。
- 如果缺少 `<link rel="preconnect" href="https://fonts.googleapis.com">` 和 `<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>` 标签，字体加载速度会变慢。

## 可变字体

- Inter、Roboto Flex、Montserrat、Open Sans 等字体都有可变版本——只需下载一个文件即可包含所有权重。
- 使用 `wght@100..900` 的语法来指定可变字体权重，这样只需下载一个文件即可。
- 在 CSS 中设置 `font-weight: 450` 即可适用于该范围内的任意权重值。
- 请查看字体页面上的 “Variable” 标签，并非所有 Google Fonts 都支持可变字体功能。

## 字体子集设置

- 默认字体集包含拉丁字符集——只有当需要波兰语、越南语等语言时，才需要添加 `&subset=latin-ext`。
- CJK 字体（如 Noto Sans JP）文件体积较大；Google 会将其分割后提供，但仍然比较占用带宽。
- 未使用的字体子集会导致资源浪费——请确认实际需要哪些字符。

## 经验证的字体搭配方案

**衬线字体 + 简体无衬线字体（经典对比风格）：**
- Playfair Display（标题）+ Source Sans Pro（正文）
- Lora（标题）+ Roboto（正文）
- Libre Baskerville（标题）+ Montserrat（正文）
- Merriweather（标题）+ Open Sans（正文）

**仅使用简体无衬线字体（现代/简洁风格）：**
- Inter（两者均可）——通过调整字体权重来区分层次结构。
- Montserrat（标题）+ Hind（正文）
- Poppins（标题）+ Nunito（正文）
- Work Sans（标题）+ Open Sans（正文）

**适用于技术或创业项目：**
- Space Grotesk（标题）+ Space Mono（代码）
- DM Sans（标题）+ DM Mono（代码）
- IBM Plex Sans + IBM Plex Mono

**仅用于标题的显示字体：**
- Abril Fatface、Bebas Neue、Oswald——切勿将这些字体用于正文。

## 根据用途选择字体

- **长篇阅读：** Merriweather、Lora、Source Serif Pro、Crimson Text
- **用户界面/交互设计：** Inter、Roboto、Open Sans、Nunito Sans（这些字体的 x 高度较大，小字号时仍清晰易读）
- **强调性标题：** Playfair Display、Oswald、Bebas Neue（不适合用于正文）
- **等宽字体：** JetBrains Mono、Fira Code、Source Code Pro

## 常见错误

- 为了 “保险起见” 而加载 6 种或更多字体权重——实际上只需加载实际使用的权重（通常为 2-3 种）。
- 将显示字体（如 Lobster、Pacifico、Abril Fatface）用于正文——这些字体仅适用于标题。
- 选择过于相似的字体（例如 Roboto 和 Open Sans）——使用其中一个即可。
- CSS 中缺少 `font-weight` 属性——如果只加载了 400 和 700 这两个权重，`font-weight: 600` 会失效。
- 未设置备用字体堆叠——务必使用 `font-family: 'Inter', system-ui, sans-serif`。

## 自主托管字体

- 自主托管字体可满足 GDPR 规范要求——Google Fonts 会从 Google 服务器加载字体，同时会记录用户的 IP 地址。
- 使用 `google-webfonts-helper` 工具来下载字体文件。
- 在 `@font-face` 规定中也需要添加 `font-display: swap` 属性。
- 如果你的内容分发网络（CDN）比 Google 的更接近用户，自主托管字体可能会加快加载速度。