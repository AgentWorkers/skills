---
name: webflow-designer-extension
description: 构建可在 Webflow Designer 中运行的扩展程序。这些扩展程序可用于创建、调试或修改 Webflow Designer 扩展程序（即与 Webflow Designer API 相互作用的 iframe）。内容涵盖命令行界面（CLI）的使用方法、元素操作、样式设置、组件应用、页面设计、变量管理、资源文件处理、错误处理，以及 Webflow 设计系统中的用户界面设计模式。
license: MIT
compatibility: "create-webflow-extension, @webflow/webflow-cli"
metadata:
  author: "[Ben Sabic](https://bensabic.dev)"
  version: "1.1.0"
---
# Webflow Designer扩展开发

开发可在Webflow Designer中运行的扩展程序，这些扩展程序以iframe的形式嵌入到Designer中，并通过调用Designer API来操作页面元素、样式等。

## 快速入门流程

> **前提条件：** 首先需要在Webflow中注册您的应用程序——请参阅 [references/register-app.md](references/register-app.md)。您需要拥有具有管理员权限的工作空间（Workspace）。

1. **创建项目框架：** 使用 `npx create-webflow-extension@latest`（系统会提示您输入项目名称、选择包管理器以及配置代码检查工具）。
2. **开发代码：** 进入项目目录后执行 `cd <项目名称> && pnpm dev`（代码将在本地服务器（localhost:1337）上运行）；该命令也支持使用npm、yarn或bun。
3. **测试扩展程序：** 通过工作空间设置（Workspace Settings）> 应用程序与集成（Apps & Integrations）> 开发（Develop）将扩展程序安装到测试网站上。
4. **打开扩展程序：** 在Designer中点击“E”键以打开扩展程序面板并启动该扩展程序。
5. **构建扩展程序：** 使用 `pnpm build` 命令准备扩展程序的部署版本。

### 命令行工具（CLI）选项

```bash
npx create-webflow-extension@latest [project-name] [options]

Options:
  --pm <pnpm|npm|yarn|bun>           Package manager to use (default: pnpm)
  --linter <oxlint|biome|eslint>     Linter to use (default: oxlint)
  --skip-git                         Skip git initialization
  --skip-install                     Skip dependency installation
  --quiet                            Suppress output
```

## Designer API

有关所有API方法、使用模式和代码示例，请参阅以下参考文档。您可以从[Designer API参考文档](references/designer-apis-reference.md)开始，该文档提供了全面的概述：

- **[Designer APIs Reference](references/designer-apis-reference.md)**：汇总了所有`webflow.*`系列API。
- **[Elements API](references/elements-api.md)**：用于选择、插入元素以及设置元素预设。
- **[Styles API](references/styles-api.md)**：用于创建样式、设置CSS属性、定义断点（breakpoints）和伪状态（pseudo-states）。
- **[Components API](references/components-api.md)**：用于定义组件、创建组件实例以及编辑组件属性。
- **[Variables API](references/variables-api.md)**：用于管理设计相关的变量（如颜色、尺寸、字体、数字、百分比等）。
- **[Error Handling](references/error-handling.md)**：介绍错误处理机制、错误类型及恢复方法。

## 项目结构

该项目结构由 `create-webflow-extension` 工具生成（基于React 19、TypeScript和Rspack框架构建）：

```
my-extension/
├── public/
│   └── index.html        # Entry point
├── src/
│   ├── App.tsx           # Main React component
│   ├── main.tsx          # React entry point
│   └── index.css         # Styles
├── webflow.json          # Extension settings
├── rspack.config.ts      # Rspack bundler configuration
├── package.json
└── tsconfig.json
```

## 参考文档

每个参考文档都包含YAML格式的元数据（`name`、`description`和`tags`），以便于搜索。您可以使用相应的搜索工具快速找到所需文档：

```bash
# List all references with metadata
python scripts/search_references.py --list

# Search by tag (exact match)
python scripts/search_references.py --tag <tag>

# Search by keyword (across name, description, tags, and content)
python scripts/search_references.py --search <query>
```

### 命令行工具（CLI）与开发工具

- **[references/create-webflow-extension-reference.md](references/create-webflow-extension-reference.md)**：用于创建Webflow扩展程序的命令行工具指南。
- **[references/webflow-cli-reference.md](references/webflow-cli-reference.md)**：Webflow提供的命令行工具，用于部署、打包和展示扩展程序。

### Designer API详细信息

- **[references/designer-apis-reference.md](references/designer-apis-reference.md)**：所有API和方法的详细说明。
- **[references/elements-api.md](references/elements-api.md)**：元素操作与预设设置。
- **[references/styles-api.md](references/styles-api.md)**：样式设置、断点管理及伪状态应用。
- **[references/components-api.md](references/components-api.md)**：组件定义与实例管理。
- **[references/pages-api.md](references/pages-api.md)**：页面和文件夹的管理功能。
- **[references/variables-api.md](references/variables-api.md)**：设计变量及其集合管理。
- **[references/assets-api.md](references/assets-api.md)**：资产上传与管理工作。
- **[references/extension-utilities.md](references/extension-utilities.md)**：扩展程序相关的辅助功能（如站点信息、事件处理、通知机制、应用程序发现等）。
- **[references/error-handling.md](references/error-handling.md)**：错误处理机制及恢复策略。
- **[references/code-examples.md](references/code-examples.md)**：结合多个API的示例代码。

### 设计与市场推广

- **[references/design-guidelines.md](references/design-guidelines.md)**：关于如何设计符合Webflow风格的界面。
- **[references/register-app.md](references/register-app.md)**：如何注册Webflow应用程序并配置其功能。
- **[references/marketplace-guidelines.md](references/marketplace-guidelines.md)**：扩展程序在市场上的审核标准（包括安全性、技术性能、设计质量、品牌定位等）。
- **[references/app-submission-and-listing.md](references/app-submission-and-listing.md)**：如何提交扩展程序并创建有效的市场列表。
- **[references/faq.md](references/faq.md)**：关于扩展程序、市场推广及常见问题的解答。

## 辅助脚本

- **`scripts/search_references.py`：根据标签或关键词搜索参考文档，或列出所有参考文档及其元信息。

## 资源文件

- **`assets/webflow-variables.css`：包含Webflow设计系统所需的CSS变量（如颜色、字体样式等）。

## 开发最佳实践

1. **检查元素状态**：在添加或修改元素内容前，务必先检查 `element.children` 的值；在操作文本内容前，先确认 `element.textContent` 的正确性。
2. **优雅地处理错误**：使用 `try/catch` 语句捕获错误，并通过 `webflow.notify()` 向用户显示错误信息（详见 [Error Handling](references/error-handling.md)）。
3. **响应式设计**：在设置样式时，需在多个屏幕分辨率下进行测试（详见 [Styles API](references/styles-api.md)）。
4. **利用变量**：使用设计变量来实现一致的视觉效果（详见 [Variables API](references/variables-api.md)。
5. **监听事件**：通过监听Designer的事件来保持扩展程序状态与Designer的同步（详见 [Extension Utilities](references/extension-utilities.md)）。
6. **合理设置尺寸**：使用 `webflow.setExtensionSize()` 来调整扩展程序的显示尺寸（详见 [Extension Utilities](references/extension-utilities.md)）。