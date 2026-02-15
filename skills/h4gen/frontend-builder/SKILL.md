---
name: no-code-frontend-builder
description: **元技能：为非程序员生成可投入生产的 React UI**  
该元技能通过整合 `frontend-design-ultimate`、`shadcn-ui` 和 `react-expert` 三个工具，帮助用户快速生成高质量的 React UI 组件。当用户描述所需的 UI 界面（如仪表盘、登录页面、管理界面等）时，该技能能够提供一套完整的、可直接复用的 TSX 组件代码，同时附带详细的设置指南和依赖项说明。用户只需将这些代码复制粘贴到项目中，即可快速实现所需的 UI 功能。
homepage: https://clawhub.ai
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"🧩","requires":{"bins":["node","npm","npx"],"env":[],"config":[]},"note":"Requires local installation of frontend-design-ultimate, shadcn-ui, and react-expert."}}
---

# 目的

使非程序员能够根据自然语言的需求获取生产级的前端组件。

这一元技能协调了三个上游技能，并生成可直接使用的输出结果，通常为一个 `.tsx` 文件以及简明的设置说明。

它不会替代上游技能的逻辑，也不假设所有依赖项都已经安装完毕。

## 所需安装的技能

- `frontend-design-ultimate`（最新检查版本：`1.0.0`）
- `shadcn-ui`（最新检查版本：`1.0.0`）
- `react-expert`（最新检查版本：`0.1.0`）

**安装/更新：**

```bash
npx -y clawhub@latest install frontend-design-ultimate
npx -y clawhub@latest install shadcn-ui
npx -y clawhub@latest install react-expert
npx -y clawhub@latest update --all
```

**验证：**

```bash
npx -y clawhub@latest list
```

## OpenClaw 兼容性说明

本技能的编写遵循 OpenClaw 的技能加载规则：
- 使用带有 YAML 前言和 Markdown 正文的 `SKILL.md` 文件
- 前言中的键应使用单行格式
- `metadata` 以单行 JSON 对象的形式编码
- 不支持任何自定义的顶级前言键

如果后续修改了该文件，请保持这些规则不变。

## 运行时前提条件

**最低要求的本地环境：**
- Node.js 18 及以上版本
- npm
- 配置了 Tailwind 的 React + TypeScript 项目

**相关生态系统依赖项：**
- `tailwindcss`（用于布局/样式）
- `lucide-react`（许多 shadcn 示例中使用的图标）
- `next-themes`（shadcn 指南中的主题切换功能）
- `react-hook-form`, `zod`, `@hookform/resolvers`（用于表单处理的库）
- **可选：** `framer-motion`（来自 `frontend-design-ultimate` 的动画效果库）
- **可选：** `recharts` 或其他等效的图表库（如果需要使用图表组件）

如果用户需要使用 shadcn 组件但它们尚未安装，请在输出中包含相应的安装命令：

```bash
npx shadcn@latest init
npx shadcn@latest add card button badge tabs table sheet sidebar
```

**默认设置：**
除非用户明确指定使用 Next.js，否则默认生成与框架无关的 React `.tsx` 文件，该文件可以在 Vite 或 Next.js 中直接运行，只需进行少量适配。

## 用户必须首先提供的输入信息**

- `ui_goal`（仪表板、登录页、管理员面板等）
- `theme_mode`（`dark`、`light` 或 `system`）
- `primary_metrics`（例如收入、月收入、增长率等指标）
- `chart_expectation`（折线图、条形图、面积图；静态图或交互式图）
- `layout_density`（`compact`、`balanced`、`spacious`）
- `brand_constraints`（颜色、Logo、字体样式要求）
- `target_framework`（`vite-react`、`nextjs` 或 `generic-react`）
- `single_file_strict`（`true`/`false`）

如果缺少任何关键输入信息，请明确设定默认值，并在 `Assumptions` 部分说明。

## 各工具的职责

### `frontend-design-ultimate`

- 负责提供视觉方向和具体的设计决策：
  - 确定整体的美学风格
  - 定义字体层次结构和颜色系统
  - 确保页面具有移动优先的响应式设计
  - 避免使用重复的、缺乏设计感的布局

**参考的指导原则：**
- 保持统一的设计风格
- 包含一个醒目的视觉元素
- 优先使用 CSS 变量和强烈的色彩对比
- 避免使用通用的默认字体

### `shadcn-ui`

- 提供强大的 UI 基础组件和组合模式：
  - 卡片、标签页、表格、导航栏、徽章、对话框等组件
  - 支持主题切换和暗模式显示
  - 提供可预测的组件结构，以便快速集成到项目中

**参考的指导原则：**
- 组件会被直接复制到项目中（而非通过托管的运行时 SDK 提供）
- 为引用的组件提供安装命令
- 优先使用可组合的组件来实现布局和数据展示

### `react-expert`

- 确保组件的行为正确性和可维护性：
  - 设计状态和数据流
  - 严格遵循 TypeScript 的编码规范
  - 保证组件的可访问性和渲染行为的可预测性
  - 为复杂的 UI 组件提供性能优化

**参考的指导原则：**
- 避免不必要的状态变更和可能导致不稳定性的代码
- 使用语义化的结构，并在效果处理中保持代码的清晰性
- 为组件的属性和数据提供明确的类型定义

## 正确的执行顺序

执行步骤如下：
1. **需求解析**：将用户请求转化为明确的目标、约束条件和输出格式。
2. **设计方向（frontend-design-ultimate）**：选择一种具体的设计风格；定义颜色调色板、字体比例、间距和页面布局。
3. **组件架构（shadcn-ui）**：将页面元素映射到相应的 UI 基础组件（如侧边栏、卡片、标签页、表格、徽章等）；列出所需安装的 shadcn 组件。
4. **React 逻辑实现（react-expert）**：实现类型化的数据模型和渲染逻辑；在需要的地方添加状态管理和钩子函数。
5. **输出整合**：默认生成一个 `.tsx` 文件；包含简短的设置说明和安装命令；列出所有必要的依赖项。

## 输出格式要求

**默认输出应包含：**
- **设置说明（Setup）**：
  - 缺少依赖项的 npm/npx 安装命令
  - 生成代码中使用的 shadcn 组件的安装命令
- **单个 TypeScript 文件（Single TSX File）**：
  - 一个独立的 React 组件（使用 TypeScript 编写）
  - 文件顶部列出了所有导入的依赖项
  - 除非用户提供了真实的数据源，否则包含模拟数据
- **假设条件（Assumptions）**：
  - 由于缺少某些输入信息而选择的默认值
- **适配说明（Adaptation Notes）**：
  - 指出如何插入真实的 API 数据
  - 如果某些组件不可用，需要移除哪些导入依赖项

**其他注意事项：**
- 不生成辅助脚本；除非用户特别要求，否则不提供多文件的结构框架。
- 如果目标项目中未预装图表库，**默认使用带有占位符的简单图表布局**；或者使用轻量级的内联 SVG 图表逻辑。
- **图表处理规则**：如果目标项目中未提供图表库，**默认使用带有占位符的简单图表组件**；如果使用外部图表库（如 Recharts），请提供安装命令并明确标注为可选组件。

**示例场景：收入仪表板（暗模式）**

**执行流程：**
1. `frontend-design-ultimate` 定义暗色主题、粗体字体和仪表板的布局（侧边栏 + 指标网格 + 图表区域）。
2. `shadcn-ui` 将这些布局元素映射到 `Card`、`Badge`、`Tabs` 等基础组件。
3. `react-expert` 为关键绩效指标（KPI）创建类型化的数据结构和渲染逻辑。
4. 最终输出结果为一个可直接使用的 `.tsx` 文件以及相应的设置命令。

**质量检查**：
在最终输出之前，需确保：
- 组件能够正常编译为 TypeScript 文件（代码中不存在缺失的符号）
- 设计具有明确的目的性，不是基于默认模板的通用设计
- 暗模式下的显示效果一致且易于阅读
- 支持移动设备的响应式布局（`sm/md/lg`）
- 所引用的 UI 组件都包含在设置命令中
- 不会将虚假的 API 调用误认为是真实的集成功能

**错误处理规则：**
- 如果发现任何问题，返回 `Needs Revision` 并列出具体的缺失项。
- **切勿声称“开箱即用”**，除非所有依赖项都已明确列出。
- **切勿使用未在设置中声明的库中的组件**。
- **未解决的决策应明确标注在 `Assumptions` 部分**。
- **优先选择高质量的组件，而不是使用功能广泛但结构粗糙的框架。**

**其他注意事项：**
- 如果缺少任何必要的上游技能，应立即停止工作并报告具体的缺失项。
- 如果缺乏项目背景信息，输出应使用通用的 React 版本，并说明需要进行的适配工作。
- 如果缺少图表依赖项，应提供替代的渲染方案和安装命令。
- 如果存在冲突的约束条件（例如“单文件结构”与“完整的应用程序路由”），需在文档中说明权衡方案。