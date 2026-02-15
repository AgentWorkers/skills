---
id: shadcn-ui
name: shadcn/ui
version: 1.0.0
author: OpenClaw Community
description: 完成 shadcn/ui 的文档编写。这些组件采用 Radix UI 和 Tailwind CSS 构建，设计精美。您可以将其直接复制到自己的应用程序中。文档内容涵盖了安装方法、组件使用、主题设置、表单设计、图表功能以及与框架的集成方法。
categories:
  - ui
  - components
  - documentation
  - design-system
tags:
  - shadcn
  - ui
  - components
  - tailwind
  - radix
  - react
  - nextjs
  - design-system
  - accessibility
  - theming
homepage: https://ui.shadcn.com
repository: https://github.com/shadcn-ui/ui
documentation: https://ui.shadcn.com/docs
---

# shadcn/ui 文档

本文档是从官方 shadcn/ui 仓库中提取的完整 shadcn/ui 文档。

## 目录

本技能包包含 **201 个 MDX 文件**（总计 1.4MB），涵盖以下内容：

### 入门
- **安装**：Next.js、Vite、Remix、Astro、Laravel、Gatsby、React Router、Tanstack Router 的配置方法
- **命令行工具（CLI）**：shadcn/ui 的命令行工具及其使用方法
- **组件配置**：组件的配置与自定义
- **主题设置**：CSS 变量、暗黑模式及主题定制
- **排版**：字体设置与排版相关工具

### 组件（50 多个）
- **折叠面板（Accordion）**：可折叠的内容区域
- **警告提示（Alert）**：上下文相关的反馈信息
- **头像（Avatar）**：用户头像
- **状态指示器（Badge）**：显示组件状态
- **按钮（Button）**：具有多种样式的交互式按钮
- **日历（Calendar）**：日期选择器和日历视图
- **卡片（Card）**：内容容器
- **复选框（Checkbox）**：多选控件
- **下拉菜单（Combobox）**：可搜索的下拉选择框
- **命令面板（Command）**：命令面板
- **上下文菜单（Context Menu）**：右键菜单
- **数据表格（Data Table）**：可排序、可过滤的表格
- **日期选择器（Date Picker）**：日期选择功能
- **对话框（Dialog）**：弹出式对话框
- **侧边栏（Drawer）**：滑出式面板
- **下拉菜单（Dropdown Menu）**：操作菜单
- **表单（Form）**：带验证功能的表单组件
- **悬停卡片（Hover Card）**：可悬停的卡片内容
- **输入框（Input）**：文本输入框
- **标签（Label）**：表单标签
- **菜单栏（Menubar）**：应用程序菜单栏
- **导航菜单（Navigation Menu）**：站点导航
- **分页（Pagination）**：页面导航功能
- **弹出窗口（Popover）**：浮动内容框
- **进度条（Progress）**：进度指示器
- **单选组（Radio Group）**：单选按钮组
- **可调整大小的面板（Resizable）**：可调整大小的面板
- **滚动区域（Scroll Area）**：自定义滚动条
- **选择框（Select）**：下拉选择框
- **分隔符（Separator）**：视觉分隔符
- **滑动面板（Sheet）**：可滑动的面板
- **加载提示（Skeleton）**：加载时的占位符
- **滑块（Slider）**：范围输入框
- **切换开关（Switch）**：切换开关
- **表格（Table）**：数据表格
- **标签页（Tabs）**：标签页界面
- **多行文本输入框（Textarea）**：多行文本输入框
- **提示信息（Toast）**：弹出式提示信息
- **切换按钮（Toggle）**：切换按钮
- **工具提示（Tooltip）**：上下文相关的提示信息
- **还有更多……**

### 高级功能
- **图表（Charts）**：Recharts 图表的集成（面积图、条形图、折线图、饼图、雷达图、辐射图）
- **表单（Forms）**：React Hook Form、Tanstack Form 的使用方法及与 Zod 的集成
- **数据表格（Data Tables）**：高级表格样式
- **暗黑模式（Dark Mode）**：主题切换功能
- **Figma**：设计与 Figma 的集成
- **图标（Icons）**：Lucide、Radix 图标库

### 框架集成
- **Next.js**：App Router、Pages Router 的集成
- **Vite**：React + Vite 的配置方法
- **Remix**：Remix 的集成
- **Astro**：Astro 的集成
- **Laravel**：Inertia.js + Laravel 的集成
- **Gatsby**：Gatsby 的集成
- **React Router**：React Router v7 的集成
- **Tanstack Router**：Tanstack Router 的集成

### 组件注册与分发
- **组件注册系统（Registry）**：组件注册系统
- **自定义组件注册表（Custom Registry）**：构建自己的组件注册表
- **命名空间（Namespace）**：自定义命名空间
- **身份验证（Authentication）**：通过组件注册系统进行身份验证
- **MCP**：Model Context Protocol 的集成

### 开发者资源
- **变更日志（Changelog）**：版本历史与更新信息
- **关于项目（About）**：项目理念与原则
- **常见问题解答（FAQ）**：常见问题的解答
- **命令行工具参考（CLI Reference）**：完整的命令行工具文档
- **右-to-left 语言支持（RTL Support）**：支持从右到左的语言显示

## 使用说明

本文档提供了以下方面的全面指导：
1. **组件安装**：如何将组件添加到项目中
2. **组件定制**：主题设置、样式调整及多种样式变体
3. **框架集成**：如何将组件集成到 Next.js、Vite、Remix 等框架中
4. **表单与验证**：如何使用 React Hook Form 和 Zod 进行表单设计与验证
5. **图表与数据展示**：如何使用 Recharts 绘制图表
6. **设计系统**：如何构建自定义的设计系统
7. **可访问性**：符合 WCAG 标准的组件设计

## 项目理念

shadcn/ui 并不是一个简单的组件库，而是一个可复用的组件集合，您可以直接将其复制并粘贴到您的应用程序中。

**主要优势：**
- **代码所有权**：组件会被复制到您的项目中
- **高度可定制**：您可以完全控制组件的样式和行为
- **良好的可访问性**：基于 Radix UI 的基础构建
- **灵活的主题设置**：通过 CSS 变量轻松调整主题样式
- **跨框架兼容性**：适用于任何 React 框架

## 文件结构

```
docs/
├── installation/        # Framework-specific setup guides
├── components/          # Component documentation (50+)
├── charts/              # Chart components (Recharts)
├── forms/               # Form integration guides
├── cli.mdx              # CLI reference
├── components-json.mdx  # Configuration reference
├── theming.mdx          # Theming guide
├── dark-mode.mdx        # Dark mode implementation
├── typography.mdx       # Typography setup
├── changelog.mdx        # Version history
├── about.mdx            # Project philosophy
├── figma.mdx            # Figma integration
└── registry/            # Registry documentation
```

## 文档来源

文档内容来源于：
- 仓库：https://github.com/shadcn-ui/ui
- 官网：https://ui.shadcn.com
- 最后更新时间：2026-02-07

## 许可证

文档内容 © shadcn。仅限教育用途，遵循公平使用原则。
Skill 包 © OpenClaw Community，采用 MIT 许可证。