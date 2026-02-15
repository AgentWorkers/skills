---
name: beautiful-mermaid
description: |
  Render beautiful Mermaid diagrams as SVGs or ASCII art. Use when user sends Mermaid code blocks 
  (\`\`\`mermaid ... \`\`\`) and wants to visualize them. Supports: Flowcharts, State, Sequence, Class, ER diagrams.
  Features: Ultra-fast (100+ diagrams <500ms), zero DOM dependencies, 15 built-in themes, Shiki theme compatibility.
  Perfect for: Telegram messages, terminal output, web interfaces, CLI tools.
---

# Beautiful Mermaid

将 Mermaid 图表渲染为美观的 SVG 或 ASCII 艺术品。支持超快速渲染、完全可自定义主题，并且完全不依赖 DOM。专为人工智能时代设计。

## 使用场景

在以下情况下使用此工具：
- 用户提供了 Mermaid 代码块（``\`\`mermaid ... \`\`\`）
- 用户请求“渲染”或“可视化”图表
- 用户需要图表的终端/ASCII 输出
- 用户需要带主题的图表（内置 15 个主题）
- 用户需要用于丰富用户界面的 SVG 输出

## 安装

```bash
npm install beautiful-mermaid
# or
bun add beautiful-mermaid
# or
pnpm add beautiful-mermaid
```

## 快速入门

### SVG 输出（默认）

```typescript
import { renderMermaid } from 'beautiful-mermaid'

const svg = await renderMermaid(`
  graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action]
    B -->|No| D[End]
`)
```

### ASCII 输出（终端）

```typescript
import { renderMermaidAscii } from 'beautiful-mermaid'

const ascii = renderMermaidAscii(`graph LR; A --> B --> C`)
```

**输出结果：**
```
┌───┐     ┌───┐     ┌───┐
│   │     │   │     │   │
│ A │────►│ B │────►│ C │
│   │     │   │     │   │
└───┘     └───┘     └───┘
```

## 支持的图表类型

| 类型 | 语法 | 描述 |
|------|--------|-------------|
| 流程图 | `graph TD/LR/BT/RL` | 支持所有方向 |
| 状态图 | `stateDiagram-v2` | 状态机图 |
| 序列图 | `sequenceDiagram` | 序列/交互图 |
| 类图 | `classDiagram` | 类继承图 |
| 实体关系图 | `erDiagram` | 实体关系图 |

### 流程图示例

\`\`\`mermaid
graph TD
  A[开始] --> B{决策}
  B -->|是| C[行动]
  B -->|否| D[结束]
  C --> D
\`\`\`

### 序列图示例

\`\`\`mermaid
sequenceDiagram
  Alice->>Bob: 你好，Bob！
  Bob-->>Alice: 你好，Alice！
\`\`\`

## 主题系统

### 内置主题（15 个）

```typescript
import { renderMermaid, THEMES } from 'beautiful-mermaid'

// Use a built-in theme
const svg = await renderMermaid(diagram, THEMES['tokyo-night'])

// Available themes:
THEMES['zinc-light']
THEMES['zinc-dark']
THEMES['tokyo-night']
THEMES['tokyo-night-storm']
THEMES['tokyo-night-light']
THEMES['catppuccin-mocha']
THEMES['catppuccin-latte']
THEMES['nord']
THEMES['nord-light']
THEMES['dracula']
THEMES['github-light']
THEMES['github-dark']
THEMES['solarized-light']
THEMES['solarized-dark']
THEMES['one-dark']
```

### 自定义主题（单色模式）

```typescript
// Just two colors - the system derives everything
const svg = await renderMermaid(diagram, {
  bg: '#1a1b26',  // Background
  fg: '#a9b1d6',  // Foreground
})
```

### 高级主题

```typescript
const svg = await renderMermaid(diagram, {
  bg: '#1a1b26',
  fg: '#a9b1d6',
  line: '#3d59a1',    // Edge color
  accent: '#7aa2f7',  // Arrow heads
  muted: '#565f89',   // Secondary text
  surface: '#292e42', // Node fill
  border: '#3d59a1',  // Node stroke
})
```

### 与 Shiki 主题的兼容性

```typescript
import { renderMermaid, fromShikiTheme } from 'beautiful-mermaid'
import { getHighlighter } from 'shiki'

const highlighter = await getHighlighter({ theme: 'vitesse-dark' })
const colors = fromShikiTheme(highlighter.getTheme('vitesse-dark'))
const svg = await renderMermaid(diagram, colors)
```

## ASCII/Unicode 输出

适用于终端环境：

```typescript
import { renderMermaidAscii } from 'beautiful-mermaid'

// Unicode (prettier, default)
const unicode = renderMermaidAscii(`graph LR; A --> B`)

// Pure ASCII (maximum compatibility)
const ascii = renderMermaidAscii(`graph LR; A --> B`, { useAscii: true })

// Custom spacing
renderMermaidAscii(diagram, {
  useAscii: false,
  paddingX: 5,          // Horizontal spacing
  paddingY: 5,          // Vertical spacing
  boxBorderPadding: 1,  // Inner padding
})
```

## API 参考

### `renderMermaid(text, options?)`: 返回一个 Promise<string> 类型的结果

将 Mermaid 代码渲染为 SVG。

**参数：**
| 参数 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `bg` | string | `#FFFFFF` | 背景颜色 |
| `fg` | string | `#27272A` | 前景颜色 |
| `line` | string? | — | 边缘颜色 |
| `accent` | string? | — | 箭头颜色、高亮部分 |
| `muted` | string? | — | 次要文本颜色 |
| `surface` | string? | — | 节点填充颜色 |
| `border` | string? | — | 节点边框颜色 |
| `font` | string | `Inter` | 字体系列 |
| `transparent` | boolean | `false` | 是否使用透明背景 |

### `renderMermaidAscii(text, options?)`: 返回一个 string 类型的结果

将 Mermaid 代码渲染为 ASCII/Unicode 格式。该过程是同步的。

**参数：**
| 参数 | 类型 | 默认值 | 描述 |
|--------|------|---------|-------------|
| `useAscii` | boolean | `false` | 是否使用 ASCII 格式（而非 Unicode） |
| `paddingX` | number | `5` | 节点之间的水平间距 |
| `paddingY` | number | `5` | 节点之间的垂直间距 |
| `boxBorderPadding` | number | `1` | 节点内边距 |

### 主题：`Record<string, DiagramColors>`

提供了所有 15 个内置主题的详细信息。

### `fromShikiTheme(theme): DiagramColors`

从 Shiki 主题中提取图表的颜色。

## 在 OpenClaw 中的使用

### Telegram 集成

可以在 Telegram 中将图表渲染为 SVG 并作为图片发送：

```typescript
import { renderMermaid } from 'beautiful-mermaid'

async function sendMermaid(message: string) {
  const blocks = extractMermaidBlocks(message)
  
  for (const block of blocks) {
    const svg = await renderMermaid(block.code, THEMES['tokyo-night'])
    // Send SVG as photo to Telegram
  }
}
```

### 终端/命令行界面输出

```typescript
import { renderMermaidAscii } from 'beautiful-mermaid'

function printDiagram(code: string) {
  const ascii = renderMermaidAscii(code)
  console.log(ascii)
}
```

## 性能特点

- **100 多个图表** 的渲染时间少于 500 毫秒 |
- **完全不依赖 DOM**（纯 TypeScript 实现） |
- **超快渲染速度**：无需浏览器或 Puppeteer 等工具 |

## 与其他工具的比较

| 功能 | beautiful-mermaid | mmdc |
|---------|------------------|------|
| 依赖性 | 完全不依赖 DOM | 需要 Puppeteer |
| 渲染速度 | 100 多个图表仅需不到 500 毫秒 | 渲染速度较慢 |
| ASCII 输出 | 支持 | 不支持 |
| 主题支持 | 内置 15 个主题 + 支持 Shiki 主题 | 仅支持 CSS 主题 |
| 代码体积 | 体积轻量 | 代码体积较大 |

## 示例工作流程

**输入：**
```
Here is the system architecture:

\`\`\`mermaid
graph TD
  User --> LB[Load Balancer]
  LB --> API[API Server]
  API --> DB[(Database)]
  API --> Cache
\`\`\`

And the flow:

\`\`\`mermaid
sequenceDiagram
  participant U as User
  participant A as API
  U->>A: Request
  A-->>U: Response
\`\`\`
```

**操作：** 使用相应主题渲染两个图表。

**输出：** 发送两张带有图例的 SVG 图片。

## 资源链接

- **npm 包：** https://www.npmjs.com/package/beautiful-mermaid
- **GitHub 仓库：** https://github.com/lukilabs/beautiful-mermaid
- **实时演示：** https://agents.craft.do/mermaid