---
name: SVG
version: 1.1.0
changelog: "Restructured with auxiliary files for focused reference"
description: 创建并优化 SVG 图形，确保其具有正确的 `viewBox` 属性、良好的可访问性以及美观的 CSS 样式。
metadata: {"clawdbot":{"emoji":"📐","requires":{},"os":["linux","darwin","win32"]}}
---
## 快速参考

| 主题 | 文件 | 常见错误 |
|-------|------|----------|
| viewBox 与缩放 | `viewbox.md` | 如果缺少 `viewbox`，则无法进行缩放 |
| 屏幕阅读器 | `accessibility.md` | 图像元素（`<img>`）应使用 `role="img"` 以及 `title` 属性 |
| SVGO 配置 | `optimization.md` | 默认情况下，`viewbox` 和 `title` 属性会被删除 |
| 内联 SVG 与外部 SVG 的区别 | `embedding.md` | `<img>` 元素无法通过 CSS 进行样式设置 |
| `currentColor` 的使用 | `styling.md` | 使用 `currentColor` 作为填充颜色可能会导致样式问题 |

## 关键默认设置

```svg
<!-- Minimum viable SVG -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
  <path d="..."/>
</svg>
```

## 常见错误检查清单

- [ ] 是否设置了 `viewbox`（而不仅仅是 `width`/`height`） |
- [ ] 图像元素的坐标是否在 `viewbox` 的范围内 |
- [ ] 如果需要自定义填充颜色，不要硬编码 `fill="#000"` |
- [ ] 对于具有说明性的 SVG 元素，应使用 `role="img"` 和 `<title>` |
- [ ] 对于装饰性的 SVG 元素，应设置 `aria-hidden="true"` |
- [ ] 确保页面上所有内联 SVG 元素都有唯一的 ID |
- [ ] 对于外部 `.svg` 文件，必须添加 `xmlns` 属性 |

## 内存存储

用户偏好设置会保存在 `~/svg/memory.md` 文件中。首次使用时会自动生成该文件。

```markdown
## User Preferences
<!-- SVG workflow defaults. Format: "setting: value" -->
<!-- Examples: default_viewbox: 0 0 24 24, prefer_inline: true -->

## Accessibility Mode
<!-- informative | decorative -->

## Optimization
<!-- Tool and settings. Format: "tool: setting" -->
<!-- Examples: svgo: preset-default, remove_metadata: true -->

## Icon Defaults
<!-- Fill and sizing preferences -->
<!-- Examples: fill: currentColor, default_size: 24x24 -->
```

*如果某个部分为空，表示使用默认设置。系统会随着时间的推移学习用户的偏好设置。*