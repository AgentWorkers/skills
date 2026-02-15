---
name: artifacts-builder
description: 这是一套工具，用于使用现代前端Web技术（React、Tailwind CSS、shadcn/ui）创建复杂的多组件claude.ai HTML页面。适用于需要状态管理、路由功能或shadcn/ui组件的项目；不适用于简单的单文件HTML/JSX页面。
license: Complete terms in LICENSE.txt
---

# 工件构建器（Artifact Builder）

要构建强大的 Claude.ai 前端工件，请按照以下步骤操作：

1. 使用 `scripts/init-artifact.sh` 初始化前端仓库。
2. 通过编辑生成的代码来开发你的工件。
3. 使用 `scripts/bundle-artifact.sh` 将所有代码打包成一个单独的 HTML 文件。
4. 向用户展示该工件。
5. （可选）测试该工件。

**技术栈**：React 18 + TypeScript + Vite + Parcel（打包工具）+ Tailwind CSS + shadcn/ui

## 设计与样式指南

**非常重要**：为了避免常见的设计问题（如过度使用居中布局、紫色渐变、统一的圆角以及 Inter 字体），请避免使用这些设计元素。

## 快速入门

### 第一步：初始化项目

运行初始化脚本以创建一个新的 React 项目：
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

该脚本会创建一个配置齐全的项目，包含：
- ✅ React + TypeScript（通过 Vite 实现）
- ✅ Tailwind CSS 3.4.1 及其配套的 shadcn/ui 样式系统
- ✅ 配置了路径别名（`@/`）
- ✅ 预装了 40 多个 shadcn/ui 组件
- ✅ 包含了所有 Radix UI 依赖项
- ✅ 配置了 Parcel（用于打包，通过 `.parcelrc` 文件）
- ✅ 兼容 Node.js 18 及更高版本（自动检测并固定 Vite 的版本）

### 第二步：开发你的工件

要构建工件，请编辑生成的文件。有关开发指导，请参阅下面的 **常见开发任务**。

### 第三步：将代码打包成单个 HTML 文件

使用以下命令将 React 应用程序打包成一个单独的 HTML 文件：
```bash
bash scripts/bundle-artifact.sh
```

此操作会生成 `bundle.html`——一个包含所有 JavaScript、CSS 以及依赖项的独立文件。该文件可以直接在 Claude 对话中作为工件分享给用户。

**要求**：你的项目根目录下必须有一个 `index.html` 文件。

**脚本的功能**：
- 安装打包所需的依赖项（parcel、@parcel/config-default、parcel-resolver-tspaths、html-inline）
- 创建支持路径别名的 `.parcelrc` 配置文件
- 使用 Parcel 进行打包（不生成源映射文件）
- 使用 html-inline 将所有资源内联到 HTML 文件中

### 第四步：与用户分享工件

最后，将打包好的 HTML 文件分享给用户，以便他们可以将其作为工件查看。

### 第五步：测试/可视化工件（可选）

注意：这一步完全是可选的。只有在必要时或用户要求时才需要进行。

要测试或可视化工件，可以使用现有的工具（包括其他 Skills 或内置工具，如 Playwright 或 Puppeteer）。通常建议在展示工件之后再进行测试，因为提前测试会增加请求与最终结果显示之间的延迟。如果需要或出现问题，可以在展示工件之后再进行测试。

## 参考资料

- **shadcn/ui 组件**：https://ui.shadcn.com/docs/components