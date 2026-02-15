---
name: pencil-renderer
description: |
  Render DNA codes to Pencil .pen frames. Does ONE thing well.

  Input: DNA code + component type (hero, card, form, etc.)
  Output: .pen frame ID + screenshot

  Use when: design-exploration or other orchestrators need to render
  visual proposals using Pencil MCP backend.
effort: high
---

# PencilRenderer

通过MCP将美学DNA代码转换为Pencil格式的 `.pen` 文件。

## 接口

**输入：**
- DNA代码：`[布局、颜色、字体样式、动画效果、元素间距、背景颜色]`
- 组件类型：`hero` | `card` | `form` | `nav` | `footer` | `section` | `button` | `input`
- 可选参数：组件名称、尺寸、父组件ID

**输出：**
- `.pen` 文件中的组件ID
- 组件渲染后的截图

## 工作流程

### 1. 确保文档准备就绪

```javascript
// Check if editor open
mcp__pencil__get_editor_state({ include_schema: false })

// If no editor, open or create
mcp__pencil__open_document({ filePathOrTemplate: "new" })
```

### 2. 获取样式基础信息

```javascript
// Get available style guide tags
mcp__pencil__get_style_guide_tags()

// Get style guide matching DNA mood
// Map DNA to relevant tags:
// - dark color → ["dark-mode", "moody"]
// - light color → ["light", "clean"]
// - spacious density → ["airy", "whitespace"]
// etc.
mcp__pencil__get_style_guide({ tags: [mapped_tags] })
```

### 3. 将DNA代码转换为Pencil组件属性

参考文档：`references/dna-to-pencil.md`

DNA代码中的各个属性与Pencil组件属性之间存在一一对应的映射关系。
示例：`centered` 布局对应 `alignItems: "center"`；对称的间距对应 `padding: equal`。

### 4. 执行设计操作

参考文档：`references/batch-design-patterns.md`

```javascript
mcp__pencil__batch_design({
  filePath: "<path>.pen",
  operations: `
    frame=I(document, {type: "frame", name: "Hero-Brutalist", ...properties})
    heading=I(frame, {type: "text", content: "Headline", ...typography})
    // ... additional operations
  `
})
```

### 5. 捕获渲染结果

```javascript
// Screenshot for visual verification
mcp__pencil__get_screenshot({ nodeId: "frameId" })
```

### 6. 返回结果

```markdown
Frame ID: [id]
DNA: [layout, color, typography, motion, density, background]
```

同时提供组件的截图。

## 组件模板

| 组件类型 | 结构组成 |
|------|-----------|
| `hero` | 容器 + 标题 + 子标题 + 呼叫行动的按钮 |
| `card` | 容器 + 图片区域 + 内容 + 行动按钮 |
| `form` | 容器 + 标签 + 输入框 + 提交按钮 |
| `nav` | 容器 + 徽标 + 链接 | 行动按钮 |
| `footer` | 容器 | 列表式布局 | 链接 | 法律声明 |
| `section` | 容器 | 标题 | 内容网格 |
| `button` | 带文本的框架 | 图标位置 |
| `input` | 带标签的输入框 | 输入字段 | 校验功能 |

## DNA代码与Pencil属性的快速对照表

| DNA代码中的属性 | 对应的Pencil组件属性 |
|------------|-------------------------|
| Layout: centered | `alignItems: "center"` | 对齐方式设置为“居中”，所有元素间距相等 |
| Layout: asymmetric | `offsetPositions` | 元素位置有偏移，间距不等 |
| Layout: bento | `grid` | 使用网格布局，各元素宽度不同 |
| Color: dark | `fill: "dark"` | 背景颜色为深色，前景颜色较浅 |
| Color: gradient | `fill: {type: "linear", stops: [...]}` | 使用线性渐变填充 |
| Typography: display-heavy | `headingSize` | 标题字体大小较大，对比度较高 |
| Typography: minimal | `fontFamily` | 使用简洁的字体系列 |
| Density: spacious | `gap: 24-48` | 元素间距较大，填充较多 |
| Density: compact | `gap: 8-16` | 元素间距较小，填充较少 |
| Background: solid | `fill: singleColor` | 背景颜色为单一颜色 |
| Background: textured | `G()` | 使用G()函数生成纹理或图片背景 |

## 限制条件

- **唯一目标**：将DNA代码渲染为对应的Pencil组件。
- **必须使用Pencil MCP**：如果Pencil MCP不可用，转换将失败。
- **映射关系是确定的**：相同的DNA代码总是生成相同的组件结构。
- **组件是可组合的**：由系统调度器调用，用户无法直接操作。

## 参考文档

- `references/dna-to-pencil.md`：完整的属性映射关系
- `references/batch-design-patterns.md`：常见的设计操作流程
- `aesthetic-system/references/dna-codes.md`：DNA代码中各属性的定义

## 集成方式

- **调用方**：`design-exploration`调度器（当Pencil后端可用时）
- **组成模块**：`aesthetic-system`（负责解析DNA代码）