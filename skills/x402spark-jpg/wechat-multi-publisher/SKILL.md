---
name: wechat-mp-publisher
description: "通过一次 API 调用，可以将一篇或多篇 Markdown 文章发布到微信官方账号（公众号）的草稿箱中。该功能支持多篇文章的组合发布（主文章 + 子文章），支持使用 Unsplash 服务自动选择封面图片（并提供 12 张图片作为备用选项进行轮询），支持自定义样式（如金色引用高亮显示、段落分隔符、强调性标题），支持内联图片自动上传到微信内容分发网络（CDN），支持自动提取文章摘要，并提供立即发布的选项。当用户需要将 Markdown 文件推送到微信草稿箱、安排文章的发布时间，或实现公众号内容的自动化发布时，该功能非常实用。"
---
# wechat-mp-publisher

将 Markdown 文章发布到微信官方账号的草稿箱中。

## 主要特性

- **多篇文章推送** — 一个草稿中可以包含主文章以及最多 7 篇子文章（区别于仅支持单篇文章的工具）
- **智能封面图片** — 根据关键词从 Unsplash 图库中选择图片；如果未找到匹配的图片，会使用备用图片池中的 12 张图片；每篇文章都会使用不同的封面图片
- **自定义样式** — 金色引文高亮显示，使用 `&&` 作为章节分隔符，标题采用特殊颜色
- **内联图片** — 本地 PNG/JPG 图片会自动上传到微信的内容分发网络（CDN）
- **灵活的认证方式** — 可通过环境变量或 `~/.config/wechat-mp/credentials.json` 文件进行配置

## 快速入门

```bash
# Install dependency
npm install @wenyan-md/core

# Set credentials
export WECHAT_APP_ID=your_appid
export WECHAT_APP_SECRET=your_appsecret

# Push to draft box
node scripts/publish.mjs main-article.md [sub-article.md ...]
```

有关完整的认证设置、IP 白名单以及定时任务自动化配置，请参阅 `references/setup.md`。

## Markdown 规范

**章节分隔符**（显示为渐变背景）：
```
paragraph text

&&

next paragraph
```

**章节标题**（显示为带特殊颜色的 H2 标题）：
```
&& My Section Title
```

**金色引文** — 当文本以以下格式开头时，会自动高亮显示：
- `真正的...` / `不是...而是...` / `底层逻辑是...` / `关键不是...`

## 命令行接口（CLI）参考

```
node scripts/publish.mjs <main.md> [sub1.md] [sub2.md] ...
  --dry-run        Render to /tmp/wechat-preview/ without uploading
  --publish        Also trigger freepublish after draft creation
  --media-id=xxx   Publish an existing draft by media_id
```

## 作者字段

通过设置 `WECHAT AUTHOR` 环境变量，可以自定义在微信中显示的作者名称。