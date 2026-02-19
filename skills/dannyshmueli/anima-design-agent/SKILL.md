---
name: anima
description: "Anima能够将设计理念转化为完整的、全栈的Web应用程序，这些应用程序具备可编辑的代码、内置的数据库、用户认证功能以及托管服务。作为AI团队中的“设计代理”，Anima为各个设计团队提供了设计上的指导，并确保了界面设计的一致性。用户可以通过三种方式来使用Anima：  
1. **描述需求并生成代码**：通过输入具体要求来直接生成相应的Web应用程序代码；  
2. **克隆现有网站**：通过提供网站的URL来快速复制该网站的代码结构；  
3. **将Figma设计转换为代码**：可以直接将Figma中的设计文件转换为适用于现有代码库的代码格式。  
当用户提供Figma设计文件的URL、网站URL、Anima Playground的URL，或者提出设计、开发、原型制作等请求时，Anima会自动启动相应的处理流程。此外，用户还可以选择发布或部署这些Web应用程序。"
compatibility: "Requires Anima MCP server connection (HTTP transport). For headless environments, requires an ANIMA_API_TOKEN."
homepage: "https://github.com/AnimaApp/mcp-server-guide"
metadata: {"clawdbot":{"emoji":"🎨","requires":{"env":["ANIMA_API_TOKEN"]},"primaryEnv":"ANIMA_API_TOKEN"},"author":"animaapp","version":"1.0.2"}
---
# 使用 Anima 进行设计和开发

## 概述

Anima 是您 AI 编码团队中的设计辅助工具。该技能赋予团队设计意识、品牌一致性，并能够将视觉创意转化为可投入生产的代码。

根据您的需求，有两种不同的使用路径：

### 路径 A：创建并发布（完整应用程序开发）

从零开始构建完整的应用程序。无需本地代码库。Anima 负责所有工作：设计、代码生成、可扩展的数据库和托管。您可以在几分钟内从想法生成到可访问的在线 URL。

此路径非常适合**并行创建多个版本**。可以使用不同的提示同时生成同一想法的多个版本，然后选择最佳版本，并通过打开游乐场 URL 进行进一步优化。整个过程无需编写任何代码或管理基础设施。

**创建 Anima 游乐场的方法：** 提示、克隆 URL、Figma URL

**您将获得：**
- 一个在 Anima 游乐场中可正常运行的应用程序
- 并行生成多个版本并进行比较的能力
- 无需浪费令牌用于文件扫描、依赖项解析或构建工具
- 已连接的可扩展数据库
- 发布时具备可扩展的托管服务

### 路径 B：集成到代码库（基于设计的代码生成）

将 Anima 中的设计元素和体验整合到您现有的项目中。当您已有代码库，并希望从 Figma 设计 URL 或现有的 Anima 游乐场中实现特定组件或页面时，可以使用此方法。

**流程：** Figma URL 到代码（codegen）、Anima 游乐场到代码

**您将获得：**
- 从 Anima 游乐场设计生成的代码，适配您的开发环境
- 精确的设计令牌、资产和实现指南

---

## 先决条件

- 必须连接并能够访问 Anima MCP 服务器（请参阅 [设置](references/setup.md)）
- 用户必须拥有 Anima 账户（提供免费层级）
- 对于使用 Figma 的流程：在 Anima 认证过程中需要连接 Figma 账户
- 对于无头环境：需要 Anima API 令牌（请参阅 [设置](references/setup.md)

## 重要提示：超时设置

Anima 的 `playground-create` 工具从零开始生成完整应用程序，这需要一些时间：

- **从提示到代码（p2c）：** 通常需要 3-7 分钟
- **从链接到代码（l2c）：** 通常需要 3-7 分钟
- **从 Figma 到代码（f2c）：** 通常需要 2-5 分钟
- **发布游乐场（playground-publish）：** 通常需要 1-3 分钟

**始终为 `playground-create` 和 `playground-publish` 调用设置 10 分钟的超时时间（600000 毫秒）。默认超时设置可能会导致失败。**

## 设置

在尝试任何 Anima MCP 调用之前，请验证连接是否正常：

**交互式环境（Claude Code、Cursor、Codex）：** 尝试调用任何 Anima MCP 工具（例如，列出工具）。如果响应正常，则表示已连接——无需进行设置。如果失败，请通过浏览器 OAuth 进行 Anima MCP 服务器的连接和认证。

**无头环境（OpenClaw、服务器端代理）：** 尝试调用任何 Anima MCP 工具。如果响应正常，则表示已连接。如果失败，用户需要从 [dev.animaapp.com](https://dev.animaapp.com) 的 **Anima 设置 → API 密钥** 生成 API 密钥，并在他们的环境中进行配置。

请参阅 [references/setup.md](references/setup.md) 以获取每种环境的详细步骤说明。

---

## 选择合适的路径

在开始使用工具和参数之前，先确定哪种路径符合用户的目标。

### 何时使用路径 A（创建并发布）

- 用户希望根据描述、参考网站或 Figma 设计**创建新内容**
- 用户希望立即获得一个可共享的在线 URL
- 没有现有的代码库需要集成
- 目的是进行原型设计、探索视觉方向或发布独立应用程序

### 何时使用路径 B（集成到代码库）

- 用户已有**现有项目**，并希望从 Figma 中添加组件或页面
- 用户希望将生成的代码文件添加到他们的代码库中，而不是托管一个应用程序
- 用户已经在 Anima 游乐场中构建了某些内容，并希望将代码拉取到本地

### 模糊情况

| 用户请求 | 可能的路径 | 原因 |
|---|---|---|
| “实现这个 Figma 设计” | **路径 B** | “实现”意味着需要在他们的项目中使用代码 |
| “将这个 Figma 变成一个在线网站” | **路径 A**（f2c） | “在线网站”表示他们需要托管服务 |
| “为我构建一个类似这样的应用程序” + URL | **路径 A**（l2c） | 克隆并从零开始重新构建 |
| “将这个 Figma 组件添加到我的项目中” | **路径 B** | “添加到我的项目中”意味着需要将代码集成到代码库 |
| “克隆这个网站” | **路径 A**（l2c） | 克隆意味着从零开始捕获并重新构建 |
| “下载游乐场的代码” | **路径 B** | 用户希望获得本地文件 |

如果仍然不清楚，可以询问：“您是需要一个可托管的在线应用程序，还是希望获得可以添加到项目中的代码文件？”

---

## 从请求到提示

在调用任何工具之前，代理需要判断：这个请求是否已经准备好构建，或者是否需要进一步澄清？如果已经准备好，应该如何编写提示来让 Anima 发挥作用？

### 何时请求帮助，何时开始构建

**判断标准：** 您能否编写一个包含**目的**、**目标受众**和**3-5 个关键特性**的提示？可以 = 开始构建。不可以 = 需要请求帮助。

**需要立即构建的提示示例：**
- “构建一个食谱分享应用程序，用户可以上传照片并评价彼此的菜肴”（目的明确，受众明确，特性具体）
- “克隆 stripe.com”（请求明确）
- “将这个 Figma 变成一个在线网站” + Figma URL（意图和输入都明确）

**需要请求帮助的提示示例：**
- “为我构建一个网站”（是什么类型的网站？为谁构建？）
- “为我的业务制作一些东西”（业务是做什么的？）
- “创建一个应用程序”（应用程序应该实现什么功能？）

在请求帮助时，请一次性提供所有信息。不要分次提问。如果用户回答含糊不清，可以跳过澄清步骤，而是使用 [探索模式（#explore-mode-parallel-variants）来生成 3 个版本。展示结果比询问更有效。

### 撰写提示

Anima 是一个具有设计感知能力的 AI。将其视为一个创意合作伙伴，而不是代码编译器。描述您想要的效果，而不是具体的实现细节。过度指定代码和十六进制值会**覆盖 Anima 的设计智能**，导致生成通用化的结果。

**提示中应包含的内容：** 目的、目标受众、风格/情绪、3-5 个关键特性、内容基调。

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

根据用户提供的信息和他们的需求，确定使用哪种流程。

**用户有文本描述或想法 → p2c**

这是最灵活的路径。Anima 会根据您的描述完成所有设计工作。适用于新应用程序、原型设计和创意探索。

**用户有网站 URL → l2c**

使用 l2c 功能克隆网站。Anima 会将整个网站重新创建为一个可编辑的游乐场。

**用户有 Figma URL → f2c（路径 A）或 codegen（路径 B）**

有两种子情况：
- **“将这个变成一个在线应用程序”** 或 **“把这个变成一个可运行的网站”** → 使用 f2c（路径 A）。根据 Figma 设计创建一个完整的游乐场。
- **“在我的项目中实现这个”** 或 **“将这个组件添加到我的代码库中”** → 使用 codegen（路径 B）。生成用于集成的代码文件。

**快速参考：**

| 用户提供的内容 | 意图 | 流程 | 工具 |
|---|---|---|---|
| 文本描述 | 创建新内容 | p2c | `playground-create` type="p2c" |
| 网站 URL | 克隆网站 | l2c | `playground-create` type="l2c" |
| Figma URL | 将其变成在线应用程序 | f2c | `playground-create` type="f2c" |
| Figma URL | 在我的项目中实现 | codegen | `codegen-figma_to_code`（路径 B） |

### 第二步：创建

#### 从提示到代码（p2c）

用简单的语言描述您的需求。Anima 会根据描述进行设计并生成一个包含品牌元素的完整游乐场。

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

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `prompt` | 是 | 要构建内容的文本描述 |
| `guidelines` | 否 | 额外的编码指南或限制 |

**样式选项：`tailwind`、`css`、`inline_styles`

**返回值：`{ success, sessionId, playgroundUrl }`

#### 从链接到代码（l2c）

提供一个网站 URL。Anima 会将整个网站克隆到一个包含可生产代码的可编辑游乐场中。

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

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `url` | 是 | 要克隆的网站 URL |

**样式选项：`tailwind`、`inline_styles`

**UI 库选项：** 仅支持 `shadcn`

**语言：** l2c 始终使用 `typescript`

**返回值：`{ success, sessionId, playgroundUrl }`

#### 从 Figma 到游乐场（f2c）

提供一个 Figma URL。Anima 会将设计实现为一个完整的游乐场，您可以在此进行预览和迭代。

**URL 格式：** `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

**提取信息：**
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

| 参数 | 是否必需 | 描述 |
|---|---|---|
| `fileKey` | 是 | 来自 URL 的 Figma 文件键 |
| `nodesId` | 是 | Figma 节点 ID 的数组（使用冒号 `:` 替换 `-`） |

**样式选项：** `tailwind`、`plain_css`、`css_modules`、`inline_styles`

**UI 库选项：** `mui`、`antd`、`shadcn`、`clean_react`

**返回值：`{ success, sessionId, playgroundUrl }`

### 第三步：发布

创建游乐场后，将其部署到在线 URL 或作为 npm 包发布。

#### 作为 Web 应用程序发布

```
playground-publish(
  sessionId: "abc123xyz",
  mode: "webapp"
)
```

**返回值：** `{ success, liveUrl, subdomain }`

应用程序将在类似 `https://winter-sun-2691.dev.animaapp.io` 的 URL 上可用。

#### 作为设计系统（npm 包）发布

```
playground-publish(
  sessionId: "abc123xyz",
  mode: "designSystem",
  packageName: "@myorg/design-system",
  packageVersion: "1.0.0"
)
```

**返回值：** `{ success, packageUrl, packageName, packageVersion }`

### 探索模式：并行生成多个版本

这是路径 A 的核心功能。当用户请求“为我构建 X”或“制作原型 X”时，会并行生成多个版本，然后发布所有版本并返回截图以供比较。

**工作流程：**

1. **根据用户的想法生成 3 个提示版本**。每个版本都有不同的创意角度：
   - 版本 1：忠实于原始设计的直接实现
   - 版本 2：更具创意或个人风格的实现
   - 版本 3：不同的视觉风格或布局

2. **并行启动 3 个 `playground-create` 调用**（每个版本对应一个请求，类型为 p2c）

3. **每个版本完成后**，立即调用 `playground-publish`（模式设置为 webapp）

4. **如果可以使用网页截图工具，为每个发布的在线 URL 截取全页截图**。可选方法包括：
   - **浏览器自动化工具**（Puppeteer、Playwright、browser MCP 工具）——导航到 URL 并捕获截图
   - **截图工具**（ScreenshotOne、Screenshotly、urlbox 等）——通过 HTTP 请求捕获页面截图
   - **您环境中可用的任何其他截图工具**

   提取截图的提示：
   - 等待 React/JS 渲染完成 5-10 秒后再截图；使用全页模式；视口宽度 1280px 可以获得更好的效果。带有滚动动画的动态网站较难捕获为静态图片。
   如果没有截图工具，可以跳过此步骤——直接返回在线 URL。用户可以直接查看这些版本。

5. **返回所有 3 个在线 URL**（以及生成的截图，如果有的话），以便用户选择最喜欢的一个或请求进一步优化。

**时间安排：** 3 个版本同时生成，因此总耗时大约与单个版本相同（约 5-7 分钟的构建时间 + 1-3 分钟的发布时间）。预计结果将在 10 分钟内准备好。

**生成有效提示的提示技巧：**
- 确保三个版本的核心概念保持一致
- 在视觉风格上有所差异：例如，“极简且干净”、“鲜明且色彩丰富”、“企业级且专业”
- 为每个版本添加具体的设计指导原则以区分它们
- 如果用户提供了参考网站或风格，请将其融入其中一个版本
- 遵循上述 [提示编写原则](#crafting-the-prompt)：描述整体风格和目的，而不是实现细节

---

## 路径 B：集成到代码库

### 第一步：确定使用哪种流程

| 用户提供的内容 | 使用的流程 | 工具 |
|---|---|---|
| Figma URL + 希望将代码集成到项目中 | Figma to Code | `codegen-figma_to_code` |
| Anima 游乐场 URL + 希望将代码下载到本地 | Download | `project-download_from_playground` |

### 第二步：检测项目环境

**检查以下文件：**
- `package.json` 以确定使用的框架（React、Vue）、样式（Tailwind）和 UI 库（MUI、Ant Design、shadcn）
- `tsconfig.json` 以确定是否使用 TypeScript
- 现有的组件文件以了解命名规范和文件结构
- 现有的样式文件以确定 CSS 方式（模块化 CSS、纯 CSS、Tailwind 工具）

**将检测到的环境与工具参数对应起来：**

| 检测到的环境 | 对应的参数 | 值 |
|---|---|---|
| 依赖项中包含 React | `framework` | `"react"` |
| 未使用 React | `framework` | `"html"` |
| 依赖项中包含 Tailwind | `styling` | `"tailwind"` |
| CSS 模块文件（*.module.css） | `styling` | `"css_modules"` |
| 使用 TypeScript | `language` | `"typescript"` |
| 依赖项中包含 MUI | `uiLibrary` | `"mui"` |
| 依赖项中包含 Ant Design | `uiLibrary` | `"antd"` |
| 依赖项中包含 shadcn 组件 | `uiLibrary` | `"shadcn"` |

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

**返回值：**

| 参数 | 描述 |
|---|---|
| `files` | 生成的代码文件，格式为 `{path: {content, isBinary}` |
| `assets` | 图片和资源的数组，格式为 `{name, url}` |
| `snapshotsUrls` | 可用于视觉参考的截图 URL，格式为 `{nodeId: url}` |
| `guidelines` | 实现指南（非常重要：请遵循这些指南） |
| `tokenUsage` | 生成的代码文件数量估计 |

**调用 `codegen-figma_to_code` 后，请执行以下步骤：**

1. 从 `snapshotsUrls` 下载截图文件以供视觉参考
2. 查看和分析截图以了解实际的外观
3. 从生成的组件中解析 `data-variant` 属性，并将其映射到您的组件属性中
4. 从生成的样式中提取 CSS 变量并使用相应的颜色
5. 阅读并遵循响应中提供的详细指南
6. 从返回的 URL 下载所有资源，并将它们放置在 `assets baseUrl` 路径下
7. 将最终实现与截图进行对比，确保视觉效果一致

#### 从游乐场下载代码

将现有的 Anima 游乐场中的代码下载到本地项目中。

```
project-download_from_playground(
  playgroundUrl: "https://dev.animaapp.com/chat/abc123xyz"
)
```

**返回值：** 预签名的下载 URL（有效时间为 10 分钟）。下载压缩文件，解压后根据项目的规范进行调整。

**重要提示：** 将 Anima 生成的代码视为设计和功能的表示，而不是最终代码样式。请根据您的项目规范、组件和设计要求对其进行调整。

---

## 其他参考资料

- **[设置指南](references/setup.md)：** 交互式和无头环境的 MCP 连接设置
- **[MCP 工具参考](references/mcp-tools.md)：** 所有 Anima MCP 工具的完整参数表
- **[示例](references/examples.md)：** 常见场景的端到端操作指南
- **[故障排除](references/troubleshooting.md)：** 常见问题及解决方法
- [Anima MCP 文档](https://docs.animaapp.com/docs/integrations/anima-mcp)
- [Anima 游乐场](https://dev.animaapp.com)
- [企业级设计系统设置](https://anima-forms.typeform.com/to/gDr77Woe)