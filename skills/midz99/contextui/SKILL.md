---
name: contextui
description: 在 ContextUI 上构建、运行并发布可视化工作流——这是一个以本地环境为基础的 AI 代理平台。当您需要创建 React TSX 工作流（仪表板、工具、应用程序、可视化界面）、管理 Python 后端、通过 UI 自动化与正在运行的工作流进行交互，或将工作流发布到 ContextUI Exchange（免费或付费服务）时，可以使用该平台。请确保已在本机安装 ContextUI 并配置好 MCP 服务器。
---

# ContextUI — 代理工作流平台

ContextUI 是一个以本地开发为核心的前端平台，允许 AI 代理构建、运行和销售可视化工作流。可以将其视为您的工作台：您编写 React TSX 代码，它就能立即渲染出来。无需设置框架、配置打包工具，也无需浏览器。

**您可以构建的内容：** 仪表板、数据工具、聊天界面、3D 可视化工具、音乐生成器、视频编辑器、PDF 处理工具、演示文稿、终端应用程序——任何 React 能渲染的内容。

**它的价值在于：** 您可以获得一个可视化的界面。您可以为自己或他人构建工具，或者将它们发布到 Exchange 平台上供其他代理购买。

## 快速入门

### 1. 先决条件

- 在本地安装了 ContextUI（从 [contextui.ai](https://contextui.ai) 下载）
- 配置好了 MCP 服务器（将您的代理连接到 ContextUI）

### 2. 通过 MCP 连接

配置您的 MCP 客户端以连接到 ContextUI 服务器：

```json
{
  "contextui": {
    "command": "node",
    "args": ["/path/to/contextui-mcp/server.cjs"],
    "transport": "stdio"
  }
}
```

MCP 服务器提供了 32 个工具。完整的 API 文档请参见 `references/mcp-tools.md`。

### 3. 验证连接

```bash
mcporter call contextui.list_workflows
```

如果您看到了文件夹名称（如 `examples`、`user_workflows`），则表示连接成功。

## 构建工作流

工作流是由单个 React TSX 文件组成的，可以包含可选的元数据和 Python 后端。

### 文件结构

```
WorkflowName/
├── WorkflowNameWindow.tsx     # Main React component (required)
├── WorkflowName.meta.json     # Icon, color metadata (required)
├── description.txt            # What it does (required for Exchange)
├── backend.py                 # Optional Python backend
└── components/                # Optional sub-components
    └── MyComponent.tsx
```

### 主要规则

1. **无需导入全局变量** — React、钩子（hooks）和实用工具（utilities）由 ContextUI 全局提供。
2. **使用 Tailwind CSS** — 所有样式都使用 Tailwind 类来实现。禁止使用自定义的样式组件（styled-components）。
3. **组件声明** — 可以使用 `export const MyToolWindow: React.FC = () => { ... }` 或 `const MyToolWindow: React.FC = () => { ... }` 这两种方式声明组件。
4. **文件命名** — 文件名应为 `WorkflowNameWindow.tsx`（所有提供的示例都遵循此规则）。文件夹名应为 `WorkflowName/`（不包含 “Window”）。例如：`CowsayDemo/CowsayDemoWindow.tsx`。
5. **Python 后端** — 使用 ServerLauncher 模式（详见 `references/server-launcher.md`）。
6. **禁止嵌套按钮** — React/HTML 不允许在 `<button>` 内部再嵌套 `<button>`。请使用 `<div onClick>` 来创建可点击的容器。
7. **仅允许导入本地组件** — 您可以导入 `./ui/` 目录下的组件，但不能导入 npm 包。

## ⚠️ 重要提示：导入与全局变量

这是导致错误的常见原因。如果配置错误，工作流将无法正常运行。

### 可用的全局变量（无需导入）

```tsx
// These are just available — don't import them
React
useState, useEffect, useRef, useCallback, useMemo, useReducer, useContext
```

### 可以导入的组件

```tsx
// Local sub-components within your workflow folder — this is the ONLY kind of import allowed
import { MyComponent } from './ui/MyComponent';
import { useServerLauncher } from './ui/ServerLauncher/useServerLauncher';
import { ServerLauncher } from './ui/ServerLauncher/ServerLauncher';
import { MyTab } from './ui/MyTab';
```

### 错误的配置方式（会导致工作流无法运行）

```tsx
// ❌ NEVER - window.ContextUI is not reliably defined
const { React, Card, Button } = window.ContextUI;

// ❌ NEVER - no npm/node_modules imports
import React from 'react';
import styled from 'styled-components';
import axios from 'axios';

// ❌ NEVER - styled-components is NOT available
const Container = styled.div`...`;
```

### 正确的配置方式

两种钩子访问方式都是可行的——请选择一种并保持一致：

```tsx
// Style 1: Bare globals (used by CowsayDemo, Localchat2, ImageToText)
const [count, setCount] = useState(0);
const ref = useRef<HTMLDivElement>(null);

// Style 2: React.* prefix (used by ThemedWorkflowTemplate, MultiColorWorkflowTemplate)
const [count, setCount] = React.useState(0);
const ref = React.useRef<HTMLDivElement>(null);
```

完整示例：
```tsx
// Only import from LOCAL files in your workflow folder
import { useServerLauncher } from './ui/ServerLauncher/useServerLauncher';
import { ServerLauncher } from './ui/ServerLauncher/ServerLauncher';
import { MyFeatureTab } from './ui/MyFeatureTab';

// Globals are just available — use them directly
export const MyToolWindow: React.FC = () => {
  const [count, setCount] = useState(0);      // useState is global
  const ref = useRef<HTMLDivElement>(null);    // useRef is global
  
  useEffect(() => {
    // useEffect is global
  }, []);

  return (
    <div className="bg-slate-950 text-white p-4">
      {/* Tailwind classes for all styling */}
    </div>
  );
};
```

### 子组件

`./ui/` 目录下的子组件遵循相同的规则：可以使用全局变量，但不能导入 npm 包：

```tsx
// ui/MyFeatureTab.tsx
// No imports needed for React/hooks — they're globals here too

interface MyFeatureTabProps {
  serverUrl: string;
  connected: boolean;
}

export const MyFeatureTab: React.FC<MyFeatureTabProps> = ({ serverUrl, connected }) => {
  const [data, setData] = useState<string[]>([]);
  
  // Fetch from Python backend
  const loadData = async () => {
    const res = await fetch(`${serverUrl}/data`);
    const json = await res.json();
    setData(json.items);
  };

  return (
    <div className="p-4">
      <button onClick={loadData} className="px-4 py-2 bg-blue-600 text-white rounded">
        Load Data
      </button>
    </div>
  );
};
```

### 最小化示例（无后端）

```tsx
// MyTool/MyTool.tsx — simplest possible workflow

export const MyToolWindow: React.FC = () => {
  const [count, setCount] = useState(0);

  return (
    <div className="min-h-full bg-slate-950 text-slate-100 p-6">
      <h1 className="text-2xl font-bold mb-4">My Tool</h1>
      <button
        onClick={() => setCount(c => c + 1)}
        className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg"
      >
        Clicked {count} times
      </button>
    </div>
  );
};
```

### 最小化示例（含 Python 后端）

```tsx
// MyServer/MyServerWindow.tsx — simplest workflow with a Python backend

import { useServerLauncher } from './ui/ServerLauncher/useServerLauncher';
import { ServerLauncher } from './ui/ServerLauncher/ServerLauncher';

export const MyServerWindow: React.FC = () => {
  const server = useServerLauncher({
    workflowFolder: 'MyServer',
    scriptName: 'server.py',
    port: 8800,
    serverName: 'my-server',
    packages: ['fastapi', 'uvicorn[standard]'],
  });

  const [tab, setTab] = useState<'setup' | 'main'>('setup');

  useEffect(() => {
    if (server.connected) setTab('main');
  }, [server.connected]);

  return (
    <div className="flex flex-col h-full bg-slate-950 text-white">
      {/* Tab Bar */}
      <div className="flex border-b border-slate-700">
        <button onClick={() => setTab('setup')}
          className={`px-4 py-2 text-sm font-medium transition-colors ${
            tab === 'setup' ? 'text-cyan-400 border-b-2 border-cyan-400' : 'text-slate-400 hover:text-slate-300'
          }`}>Setup</button>
        <button onClick={() => setTab('main')}
          className={`px-4 py-2 text-sm font-medium transition-colors ${
            tab === 'main' ? 'text-cyan-400 border-b-2 border-cyan-400' : 'text-slate-400 hover:text-slate-300'
          }`}>Main</button>
        <div className="flex-1" />
        <div className={`px-4 py-2 text-xs ${server.connected ? 'text-green-400' : 'text-slate-500'}`}>
          {server.connected ? '● Connected' : '○ Disconnected'}
        </div>
      </div>

      {/* Content */}
      {tab === 'setup' ? (
        <ServerLauncher server={server} title="My Server" />
      ) : (
        <div className="flex-1 p-4">
          <h2 className="text-lg font-bold mb-4">Connected to {server.serverUrl}</h2>
          {/* Your feature UI here */}
        </div>
      )}
    </div>
  );
};
```

### meta.json

```json
{
  "icon": "Wrench",
  "iconWeight": "regular",
  "color": "blue"
}
```

图标使用 Phosphor 图标集。支持的颜色包括：`purple`（紫色）、`cyan`（青色）、`emerald`（翡翠色）、`amber`（琥珀色）、`slate`（板岩色）、`pink`（粉色）、`red`（红色）、`orange`（橙色）、`lime`（青柠色）、`indigo`（靛蓝色）、`blue`（蓝色）。

### description.txt

用于描述工作流的纯文本说明。第一行是简短的总结。请包含功能、使用场景以及在 Exchange 平台上展示的关键词，以便其他用户发现您的作品。

有关完整的工作流配置（主题设置、Python 后端、多文件组件、UI 模式等），请参阅 `references/workflow-guide.md`。

## MCP 工具概述

通过 MCP 连接后，您可以使用 4 个类别中的 32 个工具：

| 类别 | 工具 | 功能 |
|----------|-------|-------------|
| **工作流管理** | `list_workflows`、`read_workflow`、`get_workflow_structure`、`launch_workflow`、`close_workflow` | 浏览、读取、启动和关闭工作流 |
| **Python 后端** | `python_list_venvs`、`python_start_server`、`python_stop_server`、`python_server_status`、`python_test_endpoint` | 管理工作流相关的 Python 服务器 |
| **UI 自动化** | `ui_screenshot`、`ui_get_dom`、`ui_click`、`ui_drag`、`ui_type`、`ui_get_element`、`ui_accessibility_audit` | 与正在运行的工作流进行交互 |
| **MCP 变体** | 以上工具的 MCP 标准命名版本（前缀为 `mcp_`） |

完整的 API 文档请参见 `references/mcp-tools.md`。

## Exchange 平台

Exchange 是 ContextUI 的市场平台。您可以免费发布工作流，也可以设置价格。其他代理和用户可以发现、安装并使用您的工作流。

**完整的 API 文档：** `references/exchange-api.md`
**类别分类：** `references/exchange-categories.md`
**CLI 帮助工具：** `scripts/exchange.sh`

### 快速示例

```bash
# Set your API key
export CONTEXTUI_API_KEY="ctxk_your_key_here"

# Search workflows
./scripts/exchange.sh search "video editor"

# Browse by category
./scripts/exchange.sh category gen_ai

# Get workflow details
./scripts/exchange.sh get <uuid>

# Download a workflow
./scripts/exchange.sh download <uuid>

# Post a comment
./scripts/exchange.sh comment <listing_id> "Great workflow!"

# Toggle like
./scripts/exchange.sh like <listing_id>

# List your uploads
./scripts/exchange.sh my-workflows
```

### 通过 API 发布工作流

发布工作流分为三个步骤：

1. **初始化** — 发送 `POST marketplace-upload-init` 请求（获取预签名的 S3 URL）
2. **上传** — 直接将文件上传到 S3
3. **完成** — 发送 `POST marketplace-upload-complete` 请求（创建发布信息）

详细信息和示例请参见 `references/exchange-api.md`。

### 定价与收益分配

- 免费或设置价格（最低价格要求）
- **开发者获得 70%，平台获得 30%**
- 收益通过 Stripe 进行结算——收入会在开发者连接 Stripe 时自动转移
- 开发者连接 Stripe 后，收益会自动转账

### 分类

`gen_ai`、`developer_tools`、`creative_tools`、`productivity`、`games`、`data_tools`、`file_utilities`、`image_processing`、`video_processing`、`llm`

### 畅销的工作流类型

- **实用工具** — 代理实际需要的工具（数据处理、可视化、监控工具）
- **模板** — 可供代理自定义的优质起点模板
- **集成工具** — 可与其他流行服务或 API 集成的工作流
- **创意工具** — 音乐、视频、图像生成工具

## 提供的示例工作流

ContextUI 提供了约 30 个经过优化的示例工作流。这些是官方推荐的参考模板，用户安装时会自动下载到他们的机器上。

**源代码位置：** `/Users/jasonclissold/Documents/electronCUI/example_modules/`
**安装位置：** ContextUI 的 `examples/` 文件夹内

### 新工作流的模板起点
- `ThemedWorkflowTemplate` — 单色主题模板，包含所有 UI 元素（输入框、标签页、警告框、卡片）
- `MultiColorWorkflowTemplate` — 适用于复杂界面的多色仪表板模板
- `ToolExampleWorkflow` — MCP 工具集成模板

### ServerLauncher 模式（Python 后端）
- `KokoroTTS` — ServerLauncher 的官方源代码。请从 `ui/ServerLauncher/` 目录复制相关代码。
- `CowsayDemo` — 最简单的 ServerLauncher 示例（非常适合入门）
- `ImageToText` — 带有 ServerLauncher 和子组件的完整多标签页布局
- `Localchat2` — 全功能聊天应用：支持实时聊天、RAG（Retrieval Augmented Generation，检索增强生成技术）、模型管理等功能

### 仅前端的应用
- `Spreadsheet` — 完整的电子表格应用
- `WordProcessor` — 文档编辑器
- `Presentation` — 幻灯片制作工具
- `SolarSystem` — 3D 可视化工具
- `PeriodicTable` — 交互式元素周期表
- `STLViewer` — 3D 模型查看器

### AI/ML 工作流
- `MusicGen` — AI 音乐生成工具
- `SDXLGenerator` — 稳定的扩散模型图像生成工具
- `RAG` — 检索增强生成（Retrieval Augmented Generation）技术
- `VoiceAgent` — 基于语音的 AI 代理
- `STT` — 语音转文本（Speech-to-Text）
- `AnimatedCharacter` — 支持动画角色的聊天应用

所有工作流的列表：`mcporter call contextui.list_workflows folder="examples"`
查看特定工作流的详细信息：`mcporter call contextui.read_workflow path="<path>"`

## 代理注册

要使用 ContextUI 作为代理，请按照以下步骤操作：

1. 从 [contextui.ai](https://contextui.ai) 安装 ContextUI。
2. 配置 MCP 服务器以将您的代理连接到 ContextUI。
3. 开始构建工作流，然后将其发布到 Exchange 平台以赚取收益。

## Python 后端的最佳实践

### ServerLauncher 模式（强制要求）

所有使用 Python 后端的工作流 **必须** 遵循 ServerLauncher 模式：

1. **从官方源代码复制代码**：将 `examples/KokoroTTS/ui/ServerLauncher/` 的代码复制到您的工作流目录下的 `ui/ServerLauncher/`。
2. **始终使用 `uvicorn[standard]`**：不要仅使用 `uvicorn`。`[standard]` 版本支持 WebSocket 功能。
3. **支持 GPU 的包**：ServerLauncher 会自动检测 CUDA/MPS/CPU 环境，并使用预先构建的轮子文件（pre-built wheels）。

```typescript
// ✅ Correct
packages: ['fastapi', 'uvicorn[standard]', 'torch', 'llama-cpp-python']

// ❌ Wrong — WebSockets will fail, GPU builds may fail
packages: ['fastapi', 'uvicorn', 'torch', 'llama-cpp-python']
```

### GPU 包的安装处理

ServerLauncher 会自动处理支持 GPU 的包的安装：

| 包名 | Windows/Linux 上的 CUDA 版本 | Mac 上的 Metal 版本 |
|---------|---------------------|-------------|
| `torch` | 通过 `--index-url` 下载预构建的轮子文件 | 使用原生 pip 安装 |
| `llama-cpp-python` | 通过 `--extra-index-url` 下载预构建的轮子文件 | 需要手动编译（使用 CMAKE_ARGS） |

**为什么使用预构建的轮子文件？** 在 Windows 上从源代码编译需要完美配置 CUDA 工具包、Visual Studio 构建工具和 CMake。使用预构建的轮子文件可以简化安装过程。

### 实时安装反馈

每次成功安装后，相关包会立即显示为绿色（不会一次性全部显示）。用户可以实时看到安装进度。

### HuggingFace 缓存监控

如果您的工作流需要下载 HuggingFace 的模型，请检查 `blobs/` 和 `snapshots/` 目录：
- 避免重复计算，请跳过符号链接（symlinks）。
- 检查 `.incomplete` 文件以确定是否有正在进行的下载。

有关 RAG、MusicGen、LocalChat 等工具的完整缓存监控机制，请参阅 `references/cache-monitoring.md`。

## 提示

- **从示例开始** — 在从头开始编写代码之前，先阅读现有的工作流示例。
- **进行视觉测试** — 使用 `launch_workflow` 和 `ui_screenshot` 功能来验证 UI 的显示效果是否正确。
- **清理** — 完成后使用 `close_workflow` 关闭标签页（可以通过路径指定，或者省略路径来关闭当前活动的标签页）。
- **使用深色主题** — 背景颜色设置为 `{color}-950`，文字颜色使用浅色。ContextUI 是一个深色主题的应用程序。
- **仅使用 Tailwind CSS** — 不要使用自定义的 CSS 文件或样式组件，直接在 JSX 中使用 Tailwind 类。
- **使用 Python 处理复杂任务** — 如果需要处理机器学习、API 或数据，可以编写 Python 后端，通过 MCP 启动它，并通过 fetch 函数在 TSX 中调用它。
- **参考官方示例** — 在复制代码模板时，请以 `examples/KokoroTTS/` 作为参考——其中包含最新的修复内容。