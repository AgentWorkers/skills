---
name: pencil-to-code
description: |
  Export .pen design to React/Tailwind code. Does ONE thing well.

  Input: .pen frame ID or file path
  Output: React component code + Tailwind config

  Use when: design-exploration or user needs implementation code
  from a finalized Pencil design.
effort: high
---

# 将 Pencil 设计转换为 React/Tailwind 代码

本工具可将 Pencil 格式的 `.pen` 文件导出为适用于生产环境的 React/Tailwind 代码。

## 界面

**输入参数：**
- 需要导出的框架 ID（或整个文档）
- 目标框架：React（默认）、Vue、HTML
- 可选参数：组件名称、输出路径

**输出结果：**
- 带有 Tailwind 样式的 React 组件
- 从 `.pen` 文件中提取的样式配置（作为 Tailwind 主题）
- 可选：提供截图以供验证

## 工作流程

### 1. 读取设计结构

```javascript
// Get full frame tree
mcp__pencil__batch_get({
  filePath: "<path>.pen",
  nodeIds: ["frameId"],
  readDepth: 10,
  resolveInstances: true,
  resolveVariables: true
})

// Get design variables/theme
mcp__pencil__get_variables({ filePath: "<path>.pen" })
```

### 2. 提取设计元素（Design Tokens）

将 `.pen` 文件中的变量转换为 Tailwind 样式：

```css
/* From .pen variables */
@theme {
  --color-primary: [from variables.colors.primary];
  --color-background: [from variables.colors.background];
  --font-sans: [from variables.fonts.body];
  /* ... */
}
```

参考文档：`references/token-extraction.md`

### 3. 将设计元素映射到对应的 React 组件

| `.pen` 元素类型 | 对应的 React 组件 |
|---------------|--------------|
| `frame`（包含布局） | `<div className="flex ...">` |
| `frame`（包含子元素） | 包含子元素的 React 组件 |
| `text` | `<p>`, `<h1-6>`, 或 `<span>` |
| `ref`（引用） | 可重用的 React 组件 |
| `rectangle` | 带有填充颜色的 `<div>` |
| `ellipse` | `<div className="rounded-full">` |
| `image` | `<img>` 或 `fill: url()` |

参考文档：`references/node-mapping.md`

### 4. 生成代码

- **组件结构：**  
  ```tsx
// components/[ComponentName].tsx
import { cn } from "@/lib/utils"

interface [ComponentName]Props {
  className?: string
  // Extracted props from design
}

export function [ComponentName]({ className, ...props }: [ComponentName]Props) {
  return (
    <div className={cn("[tailwind classes]", className)}>
      {/* Nested structure */}
    </div>
  )
}
```

- **Tailwind 样式映射：**  
  ```
.pen property → Tailwind class
--------------------------------
fill: #000     → bg-black
layout: horizontal → flex flex-row
gap: 16        → gap-4
padding: [16,24,16,24] → py-4 px-6
fontSize: 24   → text-2xl
fontWeight: 700 → font-bold
cornerRadius: [8,8,8,8] → rounded-lg
```

### 5. 验证（可选）

```javascript
// Screenshot the .pen frame
mcp__pencil__get_screenshot({ nodeId: "frameId" })

// Compare visually with rendered React
// (Manual step or browser automation)
```

### 6. 输出结果

```markdown
## Generated Components

### [ComponentName]
- File: `components/[ComponentName].tsx`
- Props: [list extracted props]

### Theme Configuration
- File: `app/globals.css` (additions)

## Verification
Screenshot comparison: [attached]
```

## 代码规范

### 布局系统

```
.pen                          Tailwind
--------------------------------------
layout: "vertical"         → flex flex-col
layout: "horizontal"       → flex flex-row
layout: "grid"             → grid
alignItems: "center"       → items-center
justifyContent: "center"   → justify-center
gap: 8                     → gap-2
gap: 16                    → gap-4
gap: 24                    → gap-6
width: "fill_container"    → w-full
height: "fill_container"   → h-full
```

### 间距（8 点网格系统）

```
.pen padding                  Tailwind
----------------------------------------
[8,8,8,8]                  → p-2
[16,16,16,16]              → p-4
[16,24,16,24]              → py-4 px-6
[24,32,24,32]              → py-6 px-8
```

### 字体样式

```
.pen                          Tailwind
----------------------------------------
fontSize: 12               → text-xs
fontSize: 14               → text-sm
fontSize: 16               → text-base
fontSize: 20               → text-xl
fontSize: 24               → text-2xl
fontSize: 32               → text-3xl
fontSize: 48               → text-5xl
fontWeight: 400            → font-normal
fontWeight: 500            → font-medium
fontWeight: 600            → font-semibold
fontWeight: 700            → font-bold
```

### 颜色设置

```
.pen                          Tailwind
----------------------------------------
fill: "#FFFFFF"            → bg-white
fill: "#000000"            → bg-black
fill: variable             → bg-[var(--color-name)]
textColor: "#6B7280"       → text-gray-500
stroke: "#E5E5E5"          → border-gray-200
```

### 边缘圆角

```
.pen cornerRadius             Tailwind
----------------------------------------
[0,0,0,0]                  → rounded-none
[4,4,4,4]                  → rounded
[8,8,8,8]                  → rounded-lg
[16,16,16,16]              → rounded-2xl
[9999,9999,9999,9999]      → rounded-full
```

## 限制条件：
- 仅负责将设计文件转换为代码，不允许对设计内容进行任何修改。
- 使用 Tailwind 4 的 `@theme` 系统（CSS 首先被解析）。
- 默认输出格式为 React + TypeScript。
- 使用语义化的 HTML 元素。
- 在适当的位置添加 `aria` 属性以提高可访问性。

## 参考文档：
- `references/node-mapping.md`：完整的元素到组件映射关系。
- `references/token-extraction.md`：如何从 `.pen` 文件中提取样式变量。
- `design-tokens/`：相关的样式变量命名规范。

## 集成方式：
- 由 `design-exploration` 工具在用户选择设计方向后调用。
- 用户也可以直接使用该工具。

**依赖库：**
- `design-tokens`（用于生成组件结构）。