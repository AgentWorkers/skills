---
name: anima
description: "Anima能够将设计理念转化为实际的全栈Web应用程序，这些应用程序具备可编辑的代码、内置的数据库、用户认证功能以及托管服务。作为AI生态系统中的“设计代理”，Anima为各个设计组件提供了设计意识与品牌一致性，帮助它们在构建用户界面时保持统一的设计风格。用户可以通过三种方式实现目标：一是通过提示来生成代码；二是通过链接将现有网站的内容直接克隆到新的应用程序中；三是将Figma中的设计文件转换为可执行的代码。此外，Anima还能直接从Figma设计文件生成符合设计规范的代码，并将其集成到现有的代码库中。系统会在用户提供Figma设计文件的URL、网站URL、Anima Playground的URL，或者用户提出设计、构建、原型制作等请求时自动启动相应的处理流程；同时，用户也可以选择发布或部署已完成的应用程序。"
compatibility: "Requires Anima MCP server connection (HTTP transport). For headless environments, requires mcporter CLI (via npx) and an ANIMA_API_TOKEN."
homepage: "https://github.com/AnimaApp/mcp-server-guide"
metadata: {"clawdbot":{"emoji":"🎨","requires":{"bins":["npx"],"env":["ANIMA_API_TOKEN"]},"primaryEnv":"ANIMA_API_TOKEN"},"author":"animaapp","version":"1.0"}
---
# 使用 Anima 进行设计和开发

## 概述

Anima 是您 AI 编码团队中的设计助手。该技能赋予团队设计意识、品牌一致性，并能够将视觉创意转化为可投入生产的代码。

根据您的需求，有两种不同的使用路径：

### 路径 A：创建与发布（完整应用程序开发）

从零开始构建完整的应用程序。无需本地代码库。Anima 负责所有工作：设计、代码生成、可扩展的数据库和托管。您可以在几分钟内从想法生成到可访问的在线网址。

此路径非常适合**并行创建多个版本**。可以使用不同的提示同时生成同一想法的多个版本，然后选择最佳版本，并通过在线平台进行进一步优化。整个过程无需编写任何代码或管理基础设施。

**创建 Anima 在线平台的方法：** 提示、克隆网址、Figma 网址

**您将获得：**
- 一个在 Anima 在线平台上可运行的完整应用程序
- 并行生成多个版本并进行比较的能力
- 无需浪费令牌用于文件扫描、依赖项解析或构建工具
- 已连接的可扩展数据库
- 发布时具备可扩展的托管服务

### 路径 B：集成到代码库（基于设计的代码生成）

将 Anima 中的设计元素和体验整合到您现有的项目中。当您已有代码库，并希望从 Figma 设计网址或现有的 Anima 在线平台中实现特定组件或页面时，可以使用此方法。

**流程：** Figma 网址到代码（codegen），Anima 在线平台到代码

**您将获得：**
- 从 Anima 在线平台设计生成的代码，适配您的开发环境
- 精确的设计令牌、资产和实现指南

---

## 先决条件

- 必须连接并能够访问 Anima MCP 服务器（请参阅 [设置](references/setup.md)）
- 用户必须拥有 Anima 账户（提供免费 tier）
- 对于使用 Figma 的流程：在 Anima 认证过程中需要连接 Figma 账户
- 对于 OpenClaw/无头环境：需要 `mcporter` CLI（通过 npm/npx 安装）和 Anima API 令牌

## 重要提示：超时设置

Anima 的 `playground-create` 工具从零开始生成完整应用程序，这需要一些时间：

- **从提示到代码（p2c）：** 通常需要 3-7 分钟
- **从链接到代码（l2c）：** 通常需要 3-7 分钟
- **从 Figma 到代码（f2c）：** 通常需要 2-5 分钟
- **发布在线平台（playground-publish）：** 通常需要 1-3 分钟

**始终为 `playground-create` 和 `playground-publish` 调用设置 10 分钟的超时时间（600000 毫秒）。默认超时设置可能会导致失败。**

## 设置

在尝试任何 Anima MCP 调用之前，请确认连接是否正常：

**交互式环境**（Claude Code、Cursor、Codex）：尝试调用任何 Anima MCP 工具（例如，列出工具）。如果响应正常，则表示连接成功——无需进行设置。如果失败，请通过浏览器 OAuth 进行 Anima MCP 服务器的认证。

**无头环境**（OpenClaw、mcporter）：首先运行健康检查：
```bash
npx mcporter list anima-mcp --schema --output json
```
如果返回工具列表，则表示连接正常——可以继续创建。如果出现错误，请进行认证：
1. 用户在 [dev.animaapp.com](https://dev.animaapp.com) 的 **Anima 设置 → API 密钥** 中生成 API 密钥
2. 使用该密钥配置 mcporter（请参阅 [设置](references/setup.md)
3. 重新运行健康检查以确认连接状态

**只有在健康检查失败时才需要进行设置。** 如果连接已经正常，请不要要求用户重新认证。

请参阅 [references/setup.md](references/setup.md)，了解每种环境的详细步骤。

---

## 选择合适的路径

在开始使用工具和参数之前，先确定哪种路径符合用户的目标。

### 何时使用路径 A（创建与发布）

- 用户希望根据描述、参考网站或 Figma 设计来构建新内容
- 用户希望立即获得可共享的在线网址
- 没有现有的代码库需要整合
- 目的是进行原型设计、探索视觉方向或发布独立应用程序

### 何时使用路径 B（集成到代码库）

- 用户已有现有项目，并希望从 Figma 添加组件或页面
- 用户希望将生成的代码文件添加到他们的代码库中，而不是获取托管的应用程序
- 用户已经在 Anima 在线平台上构建了某些内容，并希望将代码拉取到本地

### 模糊情况

| 用户需求 | 可能的路径 | 原因 |
|---|---|---|
| “实现这个 Figma 设计” | **路径 B** | “实现”意味着需要在用户的项目中编写代码 |
| “将这个 Figma 变成在线网站” | **路径 A**（f2c） | “在线网站”表示需要托管服务 |
| “为我构建一个类似这样的应用程序” + 网址 | **路径 A**（l2c） | 需要从零开始克隆和重建 |
| “将这个 Figma 组件添加到我的项目中” | **路径 B** | “添加到我的项目中”表示需要将代码集成到代码库 |
| “克隆这个网站” | **路径 A**（l2c） | 克隆意味着需要从零开始捕获和重建 |
| “下载在线平台的代码” | **路径 B** | 用户希望获取本地代码文件 |

如果仍然不清楚，可以询问：“您是需要一个可托管的在线应用程序，还是希望获取可以添加到项目中的代码文件？”

---

## 从请求到提示

在调用任何工具之前，助手需要判断：这个请求是否已经准备好构建，或者是否需要进一步澄清？如果已经准备好，应该如何编写提示来让 Anima 发挥作用？

### 何时询问，何时构建

**判断标准：** 您能否编写一个包含**目的**、**目标受众**和**3-5 个关键特性**的提示？可以编写提示 = 开始构建。否则 = 需要进一步询问。

**适合直接构建的提示示例：**
- “构建一个食谱分享应用程序，用户可以在其中上传照片并评价彼此的菜肴”（目的明确、目标受众明确、特性具体）
- “克隆 stripe.com”（需求明确）
- “将这个 Figma 变成在线网站” + Figma 网址（意图和输入都明确）

**适合询问的提示示例：**
- “为我构建一个网站”（是什么类型的网站？为谁构建？）
- “为我的业务制作某个东西”（业务的具体需求是什么？）
- “创建一个应用程序”（应用程序应该实现什么功能？）

在询问时，请将所有信息集中在一条消息中。不要分多次提问。如果用户回答含糊不清，可以直接使用 [探索模式](#explore-mode-parallel-variants) 生成 3 个版本进行比较。展示结果比直接询问更有效。

### 撰写提示

Anima 是一个具有设计感知能力的 AI。请将其视为一个创意合作伙伴，而不是代码编译器。描述您想要实现的感觉，而不是具体的像素级实现细节。过度指定代码和十六进制值会**覆盖 Anima 的设计智能**，导致生成的结果过于通用。

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

## 路径 A：创建与发布

### 第一步：确定流程

根据用户提供的信息及其需求，选择合适的流程。

**用户提供文本描述或想法 → p2c**

这是最灵活的路径。Anima 会根据您的描述完成所有设计工作。非常适合新应用程序、原型设计和创意探索。

**用户提供网站网址 → l2c**

使用 l2c 功能克隆网站。Anima 会将整个网站重新创建为一个可编辑的在线平台。

**用户提供 Figma 网址 → f2c（路径 A）或 codegen（路径 B）**

有两种子情况：
- **“将这个网站变成在线应用程序”** 或 **“将其变成一个可运行的网站”** → 使用 f2c（路径 A）。根据 Figma 设计创建一个完整的在线平台。
- **“在我的项目中实现这个设计”** 或 **“将这个组件添加到我的代码库中”** → 使用 codegen（路径 B）。生成可用于整合的代码文件。

**快速参考：**

| 用户提供的内容 | 目的 | 流程 | 使用的工具 |
|---|---|---|---|
| 文本描述 | 创建新内容 | p2c | `playground-create` type="p2c" |
| 网站网址 | 克隆网站 | l2c | `playground-create` type="l2c" |
| Figma 网址 | 将其变成在线应用程序 | f2c | `playground-create` type="f2c" |
| Figma 网址 | 在我的项目中实现设计 | codegen | `codegen-figma_to_code`（路径 B） |

### 第二步：创建

#### 从提示到代码（p2c）

用简单的语言描述您的需求。Anima 会根据描述进行设计并生成一个包含品牌元素的完整在线平台。

**交互式操作：**
```
playground-create(
  type: "p2c",
  prompt: "SaaS analytics dashboard for a B2B product team. Clean, minimal feel. Sidebar navigation, KPI cards for key metrics, a usage trend chart, and a recent activity feed. Professional but approachable.",
  framework: "react",
  styling: "tailwind",
  guidelines: "Dark mode, accessible contrast ratios"
)
```

**OpenClaw (mcporter)：**
```bash
npx mcporter call anima-mcp.playground-create --timeout 600000 --args '{
  "type": "p2c",
  "prompt": "SaaS analytics dashboard for a B2B product team. Clean, minimal feel. Sidebar navigation, KPI cards for key metrics, a usage trend chart, and a recent activity feed. Professional but approachable.",
  "framework": "react",
  "styling": "tailwind",
  "guidelines": "Dark mode, accessible contrast ratios"
}' --output json
```

**p2c 特定参数：**

| 参数 | 是否必需 | 说明 |
|---|---|---|
| `prompt` | 是 | 需要构建的内容的文本描述 |
| `guidelines` | 否 | 额外的编码指南或约束条件 |

**样式选项：** `tailwind`, `css`, `inline_styles`

**返回值：`{ success, sessionId, playgroundUrl }`

#### 从链接到代码（l2c）

提供网站网址。Anima 会将整个网站克隆为一个包含可生产代码的可编辑在线平台。

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

**l2c 特定参数：**

| 参数 | 是否必需 | 说明 |
|---|---|---|
| `url` | 是 | 需要克隆的网站网址 |

**样式选项：** `tailwind`, `inline_styles`

**UI 库选项：** 仅支持 `shadcn`

**语言：** l2c 始终使用 `typescript`

**返回值：`{ success, sessionId, playgroundUrl }`

#### 从 Figma 到在线平台（f2c）

提供 Figma 网址。Anima 会将设计实现为一个可预览和迭代的完整在线平台。

**网址格式：** `https://figma.com/design/:fileKey/:fileName?node-id=1-2`

**提取信息：**
- **文件键：** `/design/` 之后的部分（例如，`kL9xQn2VwM8pYrTb4ZcHjF`）
- **节点 ID：** `node-id` 查询参数的值，将 `-` 替换为 `:`（例如，`42-15` 变成 `42:15`）

**f2c 特定参数：**

| 参数 | 是否必需 | 说明 |
| `fileKey` | 是 | 来自 Figma 的文件键 |
| `nodesId` | 是 | Figma 节点 ID 的数组（使用 `:` 而不是 `-`） |

**样式选项：** `tailwind`, `plain_css`, `css_modules`, `inline_styles`

**UI 库选项：** `mui`, `antd`, `shadcn`, `clean_react`

**返回值：`{ success, sessionId, playgroundUrl }`

### 第三步：发布

创建在线平台后，将其部署到在线网址或作为 npm 包发布。

#### 作为 Web 应用程序发布

**交互式操作：**
```
playground-publish(
  sessionId: "abc123xyz",
  mode: "webapp"
)
```

**OpenClaw (mcporter)：**
```bash
npx mcporter call anima-mcp.playground-publish --timeout 600000 --args '{
  "sessionId": "abc123xyz",
  "mode": "webapp"
}' --output json
```

**返回值：** `{ success, liveUrl, subdomain }`

应用程序将在类似 `https://winter-sun-2691.dev.animaapp.io` 的网址上可用。

#### 作为设计系统发布（npm 包）

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

这是路径 A 的核心功能。当用户请求“为我构建 X”或“制作 X 的原型”时，可以并行生成多个版本，然后发布所有版本并返回截图以供比较。

**工作流程：**

1. **根据用户的想法生成 3 个不同的提示版本**：
   - 版本 1：忠实于原始设计的直接实现
   - 版本 2：更具创意或个人风格的实现
   - 版本 3：不同的视觉风格或布局

2. **并行启动所有 3 个 `playground-create` 调用**（每个版本一个）：
   ```bash
   # Repeat for each variant prompt, all running simultaneously
   npx mcporter call anima-mcp.playground-create --timeout 600000 --args '{
     "type": "p2c",
     "prompt": "<variant-prompt>",
     "framework": "react",
     "styling": "tailwind"
   }' --output json &
   ```

3. **每个版本完成后**，立即发布它：
   ```bash
   npx mcporter call anima-mcp.playground-publish --timeout 600000 --args '{
     "sessionId": "<returned-session-id>",
     "mode": "webapp"
   }' --output json
   ```

4. **如果具备网页截图功能，请对每个发布的在线网址进行全页截图**。可选的方法包括：
   - **浏览器自动化工具**（Puppeteer、Playwright、浏览器 MCP 工具）——导航到网址并捕获截图
   - **截图工具**（ScreenshotOne、Screenshotly、urlbox 等）——通过 HTTP 请求捕获页面截图
   - **您环境中可用的任何其他截图工具**

   提示：等待 React/JS 渲染完成 5-10 秒后再进行截图；使用全页模式；视口宽度设置为 1280px 可以获得更好的效果。带有滚动动画的网站较难捕获为静态图像。

   如果没有截图工具，可以跳过此步骤——直接返回在线网址。用户可以直接查看这些网址。

5. **返回所有 3 个在线网址**（以及捕获的截图，如果有的话），以便用户选择最喜欢的一个或要求进一步优化。

**时间安排：** 3 个版本并行生成，因此总耗时大约与单个版本相同（约 5-7 分钟的构建时间 + 1-3 分钟的发布时间）。预计结果将在 10 分钟内准备好。

**生成有效提示的技巧：**
- 确保三个版本的核心概念保持一致
- 在视觉风格上有所区别：例如，“极简且干净”、“鲜明且色彩丰富”、“企业级且专业”
- 为每个版本添加具体的设计指导原则以区分它们
- 如果用户提供了参考网站或风格，请将其融入其中一个版本
- 遵循上述 [提示编写原则](#crafting-the-prompt)：描述整体感觉和目的，而不是具体实现细节

---

## 路径 B：集成到代码库

### 第一步：确定流程

| 用户提供的内容 | 使用的流程 | 使用的工具 |
|---|---|---|
| Figma 网址 + 希望将代码添加到项目中 | Figma to Code | `codegen-figma_to_code` |
| Anima 在线平台网址 + 希望将代码下载到本地 | Download | `project-download_from_playground` |

### 第二步：检测项目环境

**检查以下文件：**
- `package.json` 中的框架（React、Vue）、样式（Tailwind）和 UI 库（MUI、Ant Design、shadcn）
- `tsconfig.json` 中的 TypeScript 使用情况
- 现有组件文件中的命名规范和文件结构
- 现有的 CSS 风格（模块化 CSS、纯 CSS、Tailwind 工具）

**将检测到的环境与工具参数对应起来：**

| 检测到的环境 | 对应的参数 | 值 |
|---|---|---|
| 依赖项中包含 React | `framework` | `"react"` |
| 未包含 React | `framework` | `"html"` |
| 依赖项中包含 Tailwind | `styling` | `"tailwind"` |
| CSS 模块文件（*.module.css） | `styling` | `"css_modules"` |
| 纯 CSS 文件 | `styling` | `"plain_css"` |
| 项目中包含 TypeScript 配置 | `language` | `"typescript"` |
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

| 参数 | 说明 |
|---|---|
| `files` | 生成的代码文件，格式为 `{path: {content, isBinary}` |
| `assets` | 包含图片和资源的文件数组，格式为 `{name, url}` |
| `snapshotsUrls` | 可用于视觉参考的截图网址 `{nodeId: url}` |
| `guidelines` | 实现指南（非常重要：请遵循这些指南） |
| `tokenUsage` | 生成的代码文件数量 |

**调用 `codegen-figma_to_code` 后，请按照以下步骤操作：**

1. 从 `snapshotsUrls` 下载截图文件以供视觉参考
2. 查看和分析截图以了解实际的外观效果
3. 从生成的组件中解析 `data-variant` 属性，并将其映射到您的组件属性中
4. 从生成的样式中提取 CSS 变量并使用相应的颜色
5. 阅读并遵循返回的详细 `guidelines`
6. 从返回的网址下载所有资源，并将它们放置在 `assetsBaseUrl` 路径下
7. 将最终的实现与截图进行对比，确保视觉效果一致

#### 从在线平台下载代码

将现有的 Anima 在线平台中的代码下载到本地项目中。

```
project-download_from_playground(
  playgroundUrl: "https://dev.animaapp.com/chat/abc123xyz"
)
```

**返回值：** 预签名的 zip 文件下载链接（有效期 10 分钟）。下载 zip 文件，解压后根据项目的需求进行调整。

**重要提示：** 将 Anima 生成的代码视为设计的体现，而不是最终的代码样式。请根据您的项目规范、组件和设计要求对其进行调整。

---

## 其他参考资料

- **[设置指南](references/setup.md)：** 交互式和无头环境的 MCP 连接设置
- **[MCP 工具参考](references/mcp-tools.md)：** 所有 Anima MCP 工具的参数表
- **[示例](references/examples.md)：** 常见场景的完整操作指南
- **[故障排除](references/troubleshooting.md)：** 常见问题及解决方法
- [Anima MCP 文档](https://docs.animaapp.com/docs/integrations/anima-mcp)
- [Anima 在线平台](https://dev.animaapp.com)
- [企业级设计系统设置](https://anima-forms.typeform.com/to/gDr77Woe)