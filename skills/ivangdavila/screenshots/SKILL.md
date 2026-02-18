---
name: Screenshots
slug: screenshots
version: 1.0.1
description: 生成专业的App Store和Google Play应用截图，这些截图会自动调整大小、包含设备边框、营销文案，并支持迭代的视觉学习功能。
changelog: Preferences now persist across skill updates
metadata: {"clawdbot":{"emoji":"📱","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 快速参考

| 用途 | 文件名       |
|---------|-----------|
| 存储尺寸和规格      | `specs.md`     |
| 市场营销文本叠加层    | `text-style.md`   |
| 按类别划分的视觉模板    | `templates.md`   |
| 完整的创建工作流程    | `workflow.md`   |
| 从反馈中学习     | `feedback.md`    |

## 内存存储

用户偏好设置存储在 `~/screenshots/memory.md` 文件中。激活后即可查看。

**格式说明：**
```markdown
# Screenshots Memory

## Style Preferences
- style: dominant-color | gradient | minimal | dark | light
- fonts: preferred headline fonts
- frames: with-frame | frameless | floating
- tone: punchy | descriptive | minimal

## Learned Patterns
- templates that converted well
- font/size combinations that worked
```

首次使用时创建文件夹：`mkdir -p ~/screenshots`

## 工作区结构

```
~/screenshots/
├── memory.md              # Style preferences (persistent)
├── {app-slug}/
│   ├── config.md          # Brand: colors, fonts, style
│   ├── raw/               # Raw simulator/device captures
│   ├── v1/, v2/           # Version exports
│   └── latest -> v2/      # Symlink to current
└── templates/             # Reusable visual templates
```

## 核心工作流程

1. **收集数据** — 收集原始截图、应用图标以及品牌颜色信息。
2. **尺寸处理** — 根据 `specs.md` 文件生成所有所需的屏幕尺寸。
3. **样式设计** — 应用背景、设备边框和文本叠加层。
4. **质量审核** — 使用视觉检查工具验证截图质量。
5. **迭代优化** — 根据用户反馈进行调整。
6. **导出结果** — 按商店/设备/语言对截图进行分类。

## 质量检查清单

使用视觉检查工具验证每一组截图：
- [ ] 缩略图中的文本是否可读？
- [ ] 图片中是否有不安全的文本区域（如屏幕角落、刘海区域）？
- [ ] 所有截图的样式是否一致？
- [ ] 设备边框是否与目标尺寸匹配？
- [ ] 颜色是否与应用品牌风格协调？

**如果任何一项检查未通过**，请在展示给用户之前进行修复。

## 版本控制规则

- **严禁覆盖现有文件** — 每批截图都保存在 `v{n}/` 目录下。
- **创建符号链接 `latest` 指向当前已批准的版本**。
- `config.md` 文件用于存储品牌相关的设置，以便后续重新生成截图。
- 当用户要求“恢复旧样式”时，需要对比不同版本的截图。