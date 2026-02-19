---
name: Slides
slug: slides
version: 1.0.0
description: 使用编程工具创建、编辑和自动化演示文稿，确保视觉效果的一致性，并通过项目式学习来掌握用户风格的偏好设置。
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---
## 使用场景

用户需要创建、编辑或自动化生成演示文稿。系统会负责选择合适的工具（如 `python-pptx`、`Google Slides API`、`reveal.js`、`Marp`、`Slidev`），应用用户的风格偏好，生成视觉上统一的演示文稿，并验证最终输出效果。

## 架构

项目相关的文件和样式存储在 `~/slides/` 目录下。具体设置方法请参考 `memory-template.md`。

```
~/slides/
├── memory.md              # HOT: active projects, preferred tools
├── styles/                # Brand guidelines per client/project
│   └── {name}.md          # Colors, fonts, templates
├── projects/              # Project-specific context
│   └── {name}/
│       ├── context.md     # Audience, purpose, constraints
│       └── versions.md    # Version history
└── templates/             # Approved slide structures
    └── {type}.md          # pitch, lesson, report, etc.
```

## 快速参考

| 主题 | 文件 |
|-------|------|
| 文档设置 | `memory-template.md` |
| 程序化工具 | `tools.md` |
| 视觉设计规则 | `design.md` |
| 演示文稿格式 | `formats.md` |

## 数据存储

所有数据均存储在 `~/slides/` 目录下。首次使用时需要手动创建相关文件。

```bash
mkdir -p ~/slides/{styles,projects,templates}
```

## 使用范围

本技能仅用于：
- 使用指定的工具创建或编辑演示文稿
- 将用户设定的样式偏好保存到本地文件（`~/slides/`）
- 读取用户的模板和品牌规范
- 生成用于验证的可视化输出文件

本技能绝不会：
- 访问用户的电子邮件、日历或联系人信息
- 在未经用户许可的情况下发起网络请求
- 读取 `~/slides/` 目录之外的文件或项目相关文件
- 自动将演示文稿发送到外部服务

## 自我更新机制

本技能不会自行修改其自身的文档（`SKILL.md`）。用户学习到的设计风格会保存在 `~/slides/styles/` 目录中，项目相关信息则存储在 `~/slides/projects/` 目录下。

## 核心规则

### 1. 首先明确使用场景
在生成演示文稿之前，需要明确以下内容：
- **用途**：是用于 pitching、教学、报告还是演示？
- **目标受众**：投资者、学生、高管还是客户？
- **使用的工具**：PowerPoint、Google Slides 还是基于 Web 的工具（如 reveal.js）？
- 如果存在相关样式文件，请从 `~/slides/styles/` 中加载。

### 2. 根据输出格式选择工具
| 需求 | 工具 | 使用场景 |
|------|------|-------------|
| .pptx 格式的文件 | `python-pptx` | 需要使用 PowerPoint，适用于离线环境 |
| Google Slides | `Google Slides API` | 适用于协作和云存储 |
| 基于 Web 的演示文稿 | `reveal.js`、`Slidev`、`Marp` | 适用于开发人员讲解或内容较多的场景 |
| 快速生成 PDF 文件 | `Marp` | 适用于简单的演示文稿，支持快速导出 |

### 3. 保持视觉一致性
- 在生成演示文稿之前，务必加载用户设定的样式。
- 如果用户没有指定样式，可以使用系统的默认设置或询问用户的品牌颜色和字体。
- 所有幻灯片的排版结构应保持一致。
- 每个演示文稿最多使用 3-4 种颜色。
- 详细的设计规则请参考 `design.md`。

### 4. 控制内容密度
- 每张幻灯片最多使用 6 个项目符号。
- 每个项目符号最多包含 6 个单词（遵循“6x6”原则）。
- 每张幻灯片只展示一个主要观点。
- 如果内容过多，应将其拆分成多张幻灯片展示。

### 5. 在交付前进行验证
- 生成关键幻灯片的预览图或截图。
- 检查文本是否清晰可读（正文字体大小至少为 24pt），对比度是否合适，对齐是否正确。
- 对于重要的演示文稿，在完成全部制作前，先向用户展示 2-3 张幻灯片以获取反馈。

### 6. 了解用户偏好
- 当用户提供样式指南时，将其保存到 `~/slides/styles/{name}.md` 文件中。
- 当用户修改设计选择时，更新相应的样式文件。
- 当用户批准模板后，将其保存到 `~/slides/templates/` 目录中。
- 新项目开始时，创建相应的项目文件夹（格式为 `~/slides/projects/{name}/`）。

### 7. 版本管理
- 每次重要修改都需记录在 `projects/{name}/versions.md` 文件中。
- 记录修改日期、具体内容以及适用的目标受众。
- 便于快速对比不同版本的差异（例如：“从版本 2 开始有哪些变化？”）

## 常见错误

- 在使用 `python-pptx` 时，务必使用 `pptx.util` 模块中的 `Inches()`、`Pt()`、`Emu()` 函数，切勿使用原始数字。
- 在编写 `Marp` 的文档时，YAML 文件的开头必须包含 `marp: true`。
- 在使用 `reveal.js` 时，使用 `---` 分隔水平幻灯片，`--` 分隔垂直幻灯片。
- `Slidev` 的语法与 `reveal.js` 不同，请查阅相应框架的官方文档。
- 使用 `Google Slides API` 时，注意批量更新以避免超出使用频率限制。
- 在处理图片时，务必指定图片的尺寸，因为自动调整尺寸可能导致显示问题。
- 除非明确需要嵌入，否则应使用系统的默认字体。