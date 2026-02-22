---
name: anima
description: "Anima能够将设计理念转化为实际的全栈Web应用程序，这些应用程序具备可编辑的代码、内置的数据库、用户认证功能以及托管服务。作为AI团队中的“设计代理”，Anima为各个开发成员提供设计指导，确保界面设计的一致性和品牌风格。用户可以通过三种方式启动开发流程：描述自己的需求（通过提示生成代码）、克隆现有网站（通过链接导入代码），或直接将Figma设计文件转换为代码（Figma到代码的转换）。此外，Anima还能直接从Figma设计文件生成符合设计规范的代码，并将其集成到现有的代码库中。当用户提供Figma设计文件的URL、网站URL、Anima Playground的URL，或者提出设计、开发、原型制作等请求，或者希望发布或部署应用程序时，Anima会自动启动相应的处理流程。"
compatibility: "Requires Anima MCP server connection (HTTP transport). For headless environments, requires an ANIMA_API_TOKEN."
homepage: "https://github.com/AnimaApp/mcp-server-guide"
metadata: {"clawdbot":{"emoji":"🎨","requires":{"env":["ANIMA_API_TOKEN"]},"primaryEnv":"ANIMA_API_TOKEN"},"author":"animaapp","version":"1.0.9"}
---
# 使用 Anima 进行设计与开发

## 概述

Anima 是您 AI 编码团队中的设计助手。这项技能赋予了团队成员设计意识，并使他们能够将视觉创意转化为可投入生产的代码。

根据您的需求，有两种不同的实现路径：

### 路径 A：创建并发布（完整应用程序的创建）

从零开始构建完整的应用程序。无需本地代码库。Anima 负责所有工作：设计、代码生成、可扩展的数据库和托管。您可以在几分钟内将想法转化为可访问的在线应用程序。

此路径非常适合**并行创建多个版本**。可以使用不同的提示同时生成同一想法的多个版本，然后选择最佳版本，并通过在线 playground 进一步优化。整个过程无需编写任何代码或管理基础设施。

**创建 Anima Playground 的方法：** 提示、克隆 URL、Figma URL

**您将获得：**
- 一个在 Anima Playground 中可正常运行的应用程序
- 并行生成多个版本并进行比较的能力
- 无需浪费令牌用于文件扫描、依赖项解析或构建工具
- 已连接的可扩展数据库
- 发布时具备可扩展的托管服务

### 路径 B：集成到代码库（基于设计的代码生成）

将 Anima 中的设计元素和体验整合到您现有的项目中。当您已有代码库，并希望从 Figma 设计 URL 或现有的 Anima Playground 中实现特定组件或页面时，可以使用此方法。

**流程：** Figma URL 到代码（codegen）、Anima Playground 到代码

**您将获得：**
- 从 Anima Playground 设计中生成的、适配您技术栈的代码
- 精确的设计令牌、资产和实现指南

---

## 先决条件

- 必须连接并能够访问 Anima MCP 服务器
- 用户必须拥有 Anima 账户（提供免费 tier）
- 对于使用 Figma 的流程：在 Anima 认证过程中需要连接 Figma 账户
- 对于无头环境：需要 Anima API 令牌

## 重要提示：超时设置

Anima 的 `playground-create` 工具从零开始生成完整的应用程序，这需要一些时间：

- **从提示到代码（p2c）：** 通常需要 3-7 分钟
- **从链接到代码（l2c）：** 通常需要 3-7 分钟
- **从 Figma 到代码（f2c）：** 通常需要 2-5 分钟
- **发布 playground：** 通常需要 1-3 分钟

**对于 `playground-create` 和 `playground-publish` 调用，请始终设置 10 分钟的超时（600000 毫秒）。默认的超时设置可能会导致失败。**

## 设置

在尝试任何 Anima MCP 调用之前，请先验证连接是否正常。尝试调用任意 Anima MCP 工具。如果响应正常，说明连接成功；如果失败，则用户需要设置认证信息。详情请参阅 [设置指南](https://github.com/AnimaApp/mcp-server-guide/blob/main/anima-skill-references/setup.md)。

---

## 选择合适的路径

在开始使用工具和参数之前，先确定哪条路径符合用户的目标。

### 何时使用路径 A（创建并发布）

- 用户希望根据描述、参考网站或 Figma 设计来**创建新内容**
- 用户希望立即获得一个可共享的在线应用程序 URL
- 没有现有的代码库需要整合
- 目的是进行原型设计、探索视觉方向或发布独立的应用程序

### 何时使用路径 B（集成到代码库）

- 用户已有**现有项目**，并希望从 Figma 中添加组件或页面
- 用户希望将生成的代码文件添加到他们的代码库中，而不是获取托管的应用程序
- 用户已经在 Anima Playground 中构建了某些内容，并希望将代码拉取到本地

### 模糊情况

| 用户的请求 | 可能的路径 | 原因 |
|---|---|---|
| “实现这个 Figma 设计” | **路径 B** | “实现”意味着需要在用户的项目中编写代码 |
| “将这个 Figma 变成一个在线网站” | **路径 A**（f2c） | “在线网站”表示用户需要托管服务 |
| “为我构建一个类似这样的应用程序” + URL | **路径 A**（l2c） | 需要从零开始克隆和重建 |
| “将这个 Figma 组件添加到我的项目中” | **路径 B** | “添加到我的项目中”意味着需要将代码集成到代码库 |
| “克隆这个网站” | **路径 A**（l2c） | 克隆意味着需要从零开始重新构建 |
| “下载 playground 的代码” | **路径 B** | 用户希望获取本地代码文件 |

如果仍然不清楚，可以询问：“您是需要一个可托管的在线应用程序，还是需要代码文件来添加到项目中？”

---

## 从请求到提示

在调用任何工具之前，代理需要判断：这个请求是否已经准备好构建，或者是否需要进一步澄清？如果已经准备好，应该如何编写提示来让 Anima 发挥作用？

### 何时请求帮助，何时开始构建

**判断标准：** 您能否编写一个包含**目的**、**目标受众**和**3-5 个关键特性**的提示？可以 = 开始构建；否则 = 需要请求帮助。

**适合直接构建的提示：**
- “构建一个食谱分享应用程序，用户可以上传照片并评价彼此的菜肴”（目的明确、目标受众明确、特性具体）
- “克隆 stripe.com”（请求明确）
- “将这个 Figma 变成一个在线网站” + Figma URL（意图和输入信息明确）

**适合请求帮助的提示：**
- “为我构建一个网站”（是什么类型的网站？为谁构建？）
- “为我的业务制作某个东西”（业务的具体需求是什么？）
- “创建一个应用程序”（应用程序应该实现什么功能？）

在请求帮助时，请一次性提供所有信息。不要分次提问。如果用户回答含糊不清，可以跳过澄清步骤，转而使用 [探索模式](#explore-mode-parallel-variants) 生成 3 个版本进行对比。展示结果往往比询问更有效。

### 编写提示

Anima 是一个具有设计感知能力的 AI。请像与创意合作者交流一样与它沟通，而不是像使用代码编译器一样。描述您想要的整体感觉，而不是具体的实现细节。过度指定代码和十六进制值会**抑制 Anima 的设计智能**，导致生成的结果缺乏个性。

**提示中应包含的内容：** 目的、目标受众、风格/氛围、3-5 个关键特性、内容基调。

**提示中不应包含的内容：** 代码片段、CSS 值、十六进制颜色、像素尺寸、字体大小、组件库名称（请使用 `uiLibrary` 参数代替）、实现细节、文件结构。

**示例（过度指定的提示）：**
```
Create a dashboard. Use #1a1a2e background, #16213e sidebar at 280px width,
#0f3460 cards with 16px padding, border-radius 12px. Header height 64px with
a flex row, justify-between. Font: Inter 14px for body, 24px bold for headings.
```

**示例（描述性的提示）：**
```
SaaS analytics dashboard for a B2B product team. Clean, minimal feel.
Sidebar navigation, KPI cards for key metrics, a usage trend chart, and a
recent activity feed. Professional but approachable. Think Linear meets Stripe.
```

## 路径 A：创建并发布

### 第一步：确定使用哪种流程

根据用户提供的信息及其需求，选择合适的流程。

**用户提供文本描述或想法 → p2c**

这是最灵活的路径。Anima 会根据您的描述完成所有设计工作。非常适合新应用程序、原型设计和创意探索。

**用户提供网站 URL → l2c**

使用 l2c 功能克隆网站。Anima 会将整个网站重新创建为一个可编辑的 playground。

**用户提供 Figma URL → f2c（路径 A）或 codegen（路径 B）**

有两种子情况：
- **“将这个网站变成一个在线应用程序”** 或 **“把这个网站制作成一个可运行的网站”** → 使用 f2c（路径 A）。根据 Figma 设计创建一个完整的 playground。
- **“在我的项目中实现这个设计”** 或 **“将这个组件添加到我的代码库中”** → 使用 codegen（路径 B）。生成可用于整合的代码文件。

**快速参考：**

| 用户提供的内容 | 意图 | 使用的流程 | 使用的工具 |
|---|---|---|---|
| 文本描述 | 创建新内容 | p2c | `playground-create` 类型="p2c" |
| 网站 URL | 克隆网站 | l2c | `playground-create` 类型="l2c" |
| Figma URL | 将其变成在线应用程序 | f2c | `playground-create` 类型="f2c" |
| Figma URL | 在我的项目中实现设计 | codegen | `codegen-figma_to_code`（路径 B） |

### 第二步：创建

#### 从提示到代码（p2c）

用简单的语言描述您的需求。Anima 会根据描述进行设计并生成一个包含品牌元素的完整 playground。

```
playground-create(
  type: "p2c",
  prompt: "SaaS analytics dashboard for a B2B product team. Clean, minimal feel. Sidebar navigation, KPI cards for key metrics, a usage trend chart, and a recent activity feed. Professional but approachable.",
  framework: "react",
  styling: "tailwind",
  guidelines: "Dark mode, accessible contrast ratios"
)
```

**p2c 特定的参数：**

| 参数 | 是否必需 | 说明 |
|---|---|---|
| `prompt` | 是 | 需要构建的内容的文本描述 |
| `guidelines` | 否 | 额外的编码指南或限制条件 |

**样式选项：** `tailwind`, `css`, `inline_styles`

#### 从链接到代码（l2c）

提供网站 URL。Anima 会将其重新创建为一个包含可生产代码的可编辑 playground。

```
playground-create(
  type: "l2c",
  url: "https://stripe.com/payments",
  framework: "react",
  styling: "tailwind",
  language: "typescript",
  uiLibrary: "shadcn"
)
```

**l2c 特定的参数：**

| 参数 | 是否必需 | 说明 |
| `url` | 是 | 需要克隆的网站 URL |

**样式选项：** `tailwind`, `inline_styles`

**UI 库选项：** 仅支持 `shadcn`

**语言：** l2c 始终使用 `typescript`

#### 从 Figma 到 Playground（f2c）

提供 Figma URL。Anima 会将设计实现为一个可预览和迭代的完整 playground。

**URL 格式：** `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

**提取所需信息：**
- **文件键：** `/design/` 之后的部分（例如，`kL9xQn2VwM8pYrTb4ZcHjF`）
- **节点 ID：** `node-id` 查询参数的值，用冒号替换 `-`（例如，`42-15` 变成 `42:15`）

```
playground-create(
  type: "f2c",
  fileKey: "kL9xQn2VwM8pYrTb4ZcHjF",
  nodesId: ["42:15"],
  framework: "react",
  styling: "tailwind",
  language: "typescript",
  uiLibrary: "shadcn"
)
```

**f2c 特定的参数：**

| 参数 | 是否必需 | 说明 |
| `fileKey` | 是 | 来自 URL 的 Figma 文件键 |
| `nodesId` | 是 | Figma 节点 ID 的数组（使用冒号 `:` 而不是 `-`） |

**样式选项：** `tailwind`, `plain_css`, `css_modules`, `inline_styles`

**UI 库选项：** `mui`, `antd`, `shadcn`, `clean_react`

### 第三步：发布

创建 playground 后，将其部署到在线 URL 或作为 npm 包发布。

#### 作为 Web 应用程序发布

```
playground-publish(
  sessionId: "abc123xyz",
  mode: "webapp"
)
```

响应中会包含发布后的应用程序的在线 URL。

#### 作为设计系统（npm 包）发布

```
playground-publish(
  sessionId: "abc123xyz",
  mode: "designSystem",
  packageName: "@myorg/design-system",
  packageVersion: "1.0.0"
)
```

### 探索模式：并行生成多个版本

这是路径 A 的强大功能。当用户请求“为我构建 X”或“制作一个原型 X”时，可以并行生成多个版本，然后发布所有版本并返回在线 URL 供用户比较。

**工作流程：**

1. **根据用户的想法生成 3 个不同的版本**：
   - 版本 1：忠实于原始设计的版本
   - 版本 2：更具创意或个人风格的版本
   - 版本 3：采用不同的视觉风格或布局的版本

2. **并行调用 3 次 `playground-create`（每个版本使用一次 p2c）

3. **每个版本生成完成后**，立即调用 `playground-publish`（模式设置为 webapp）

4. **返回所有 3 个在线 URL**，让用户选择最喜欢的一个版本或请求进一步优化。如果有的话，可以使用截图工具将每个页面截图并展示在聊天中。

**时间安排：** 3 个版本同时生成，因此总耗时大约与单个版本相同（约 5-7 分钟的生成时间 + 1-3 分钟的发布时间）。预计结果将在 10 分钟内准备好。

**生成优质版本的提示技巧：**
- 确保三个版本的核心概念保持一致
- 在视觉风格上有所差异：例如，“极简且干净”、“鲜明且色彩丰富”、“企业级且专业”
- 为每个版本添加具体的设计指导原则以区分它们
- 如果用户提供了参考网站或风格建议，将其融入其中一个版本
- 遵循上述 [提示编写原则](#crafting-the-prompt)：描述整体氛围和目的，而不是实现细节

---

## 路径 B：集成到代码库

### 第一步：确定使用哪种流程

| 用户提供的内容 | 使用的流程 | 使用的工具 |
|---|---|---|
| 提供 Figma URL 并希望将代码集成到项目中 | Figma to Code | `codegen-figma_to_code` |
| 提供 Anima Playground URL 并希望将代码下载到本地 | Download | `project-download_from_playground` |

### 第二步：根据项目技术栈调整参数

| 项目技术栈 | 相关参数 | 设置值 |
|---|---|---|
| React | `framework` | `"react"` |
| 无 React | `framework` | `"html"` |
| Tailwind | `styling` | `"tailwind"` |
| CSS Modules | `styling` | `"css_modules"` |
| Plain CSS | `styling` | `"plain_css"` |
| TypeScript | `language` | `"typescript"` |
| MUI | `uiLibrary` | `"mui"` |
| Ant Design | `uiLibrary` | `"antd"` |
| shadcn | `uiLibrary` | `"shadcn"` |

### 第三步：生成代码

#### 从 Figma 到代码（直接实现）

```
codegen-figma_to_code(
  fileKey: "kL9xQn2VwM8pYrTb4ZcHjF",
  nodesId: ["42:15"],
  framework: "react",
  styling: "tailwind",
  language: "typescript",
  uiLibrary: "shadcn",
  assetsBaseUrl: "./assets"
)
```

在实现代码时，可以使用响应中的信息（截图、资产、设计指南）作为参考。

您也可以使用 `project-download_from_playground` 将现有的 Anima Playground 中的代码下载到您的项目中。

---

## 额外参考资料

- [设置指南](https://github.com/AnimaApp/mcp-server-guide/blob/main/anima-skill-references/setup.md)
- [MCP 工具参考](https://github.com/AnimaApp/mcp-server-guide/blob/main/anima-skill-references/mcp-tools.md)
- [示例](https://github.com/AnimaApp/mcp-server-guide/blob/main/anima-skill-references/examples.md)
- [故障排除](https://github.com/AnimaApp/mcp-server-guide/blob/main/anima-skill-references/troubleshooting.md)
- [Anima MCP 文档](https://docs.animaapp.com/docs/integrations/anima-mcp)