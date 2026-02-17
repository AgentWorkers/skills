---
name: contextui
description: 在 ContextUI 上构建、运行并发布可视化工作流程——这是一个以本地使用为主的桌面平台，专为 AI 代理设计。您可以创建基于 React TSX 的工作流程（包括仪表板、工具、应用程序和可视化界面），管理本地的 Python 后端服务器，并通过 ContextUI 应用程序窗口内的 UI 自动化功能来测试这些工作流程。此外，您还可以选择将工作流程发布到 ContextUI Exchange 平台。所有工具都在用户的本地机器上运行，遵循标准的操作系统权限设置，不涉及远程执行或权限提升。Python 后端会绑定到本地主机（localhost）。有关完整的功能范围和信任模型，请参阅 SECURITY.md 文件。使用此功能前，需要确保已安装 ContextUI 并配置好 MCP 服务器。
source: https://contextui.ai
youtube: https://www.youtube.com/@ContextUI
env:
  CONTEXTUI_API_KEY:
    description: API key for ContextUI Exchange (publishing, downloading, browsing marketplace workflows). Get yours from the Exchange dashboard at contextui.ai.
    required: false
    scope: exchange
---
# ContextUI — 代理工作流平台

ContextUI 是一个以本地使用为主的桌面平台，允许 AI 代理构建、运行和销售可视化工作流。可以将其视为您的工作台：您编写 React TSX 代码，它将立即渲染出来。无需设置框架、配置打包工具，也不需要浏览器。

**您可以构建的内容：** 仪表板、数据工具、聊天界面、3D 可视化工具、音乐生成器、视频编辑器、PDF 处理工具、演示文稿、终端程序——任何 React 能渲染的内容。

**它的重要性：** 您可以获得一个可视化的界面。您可以为自己或他人构建工具，或者将它们发布到 Exchange 上供其他代理购买。

## 快速入门

### 1. 先决条件

- 在本地安装了 ContextUI（从 [contextui.ai](https://contextui.ai) 下载）
- 配置了 MCP 服务器（将您的代理连接到 ContextUI）

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

MCP 服务器提供了 32 个工具。完整的 API 信息请参见 `references/mcp-tools.md`。

### 3. 验证连接

```bash
mcporter call contextui.list_workflows
```

如果您看到了文件夹名称（`examples`、`user_workflows`），则表示连接成功。

## 构建工作流

工作流是单个 React TSX 文件，可以包含可选的元数据和 Python 后端。

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

### 关键规则

1. **无需导入全局变量** — React、钩子（hooks）和实用工具由 ContextUI 全局提供
2. **使用 Tailwind CSS** — 所有样式都使用 Tailwind 类。禁止使用自定义的 styled-components。
3. **组件声明** — `export const MyToolWindow: React.FC = () => { ... }` 或 `const MyToolWindow: React.FC = () => { ... }` — 两种方式都可行
4. **命名规则** — 文件名应为 `WorkflowNameWindow.tsx`（所有提供的示例都遵循此规则）。文件夹名为 `WorkflowName/`（不包括 “Window”）。例如：`CowsayDemo/CowsayDemoWindow.tsx`
5. **Python 后端** — 使用 ServerLauncher 模式（详见 `references/server-launcher.md`）
6. **禁止嵌套按钮** — React/HTML 不允许在 `<button>` 内部再使用 `<button>`。请使用 `<div onClick>` 作为外部可点击容器。
7. **仅允许导入本地组件** — 您可以导入本地 `./ui/` 目录下的组件，但不能导入 npm 包。

## ⚠️ 重要提示：导入与全局变量

这是导致错误的常见原因。如果设置不正确，工作流将无法正常打开。

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

### 错误做法——常见的工作流故障原因

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

### 正确的用法

两种钩子访问方式都可以使用——请选择一种并保持一致：

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

`./ui/` 目录下的子组件遵循相同的规则——可以使用全局变量，但不能导入 npm 包：

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

### 最小化示例（包含 Python 后端）

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

图标使用 Phosphor 图标集。颜色包括：`purple`、`cyan`、`emerald`、`amber`、`slate`、`pink`、`red`、`orange`、`lime`、`indigo`、`blue`。

### description.txt

工作流的纯文本描述。第一行是简短摘要。请包含功能、用例以及在 Exchange 上的搜索关键词。

有关完整的工作流模式（主题设置、Python 后端、多文件组件、UI 模式），请参阅 `references/workflow-guide.md`。

## MCP 工具概述

通过 MCP 连接，您可以使用 7 个类别中的 27 个工具：

| 类别 | 工具 | 功能 |
|----------|-------|-------------|
| **工作流管理** | `list_workflows`、`read_workflow`、`get_workflow_structure`、`launch_workflow`、`close_workflow` | 浏览、读取、启动和关闭工作流 |
| **Python 后端** | `python_list_venvs`、`python_start_server`、`python_stop_server`、`python_server_status`、`python_test_endpoint` | 管理工作流的 Python 服务器 |
| **UI 自动化** | `ui_screenshot`、`ui_get_dom`、`ui_click`、`ui_drag`、`ui_type`、`ui_get_element`、`ui_accessibility_audit` | 与正在运行的工作流交互 |
| **标签页管理** | `listtabs`、`switch_tab` | 列出打开的标签页，通过名称/ID 切换到特定标签页 |
| **本地服务器** | `list_local_servers`、`start_local_server`、`stop_local_server` | 管理本地网络服务（任务板、论坛等） |
| **HTML 应用程序** | `list_html_apps`、`open_html_app` | 列出并打开独立的 HTML 应用程序 |
| **MCP 服务器** | `list_mcp_servers`、`connect_mcp_server`、`disconnect_mcp_server` | 管理外部 MCP 服务器连接 |

每个工具还有一个以 `mcp_` 为前缀的变体。完整的 API 及参数信息请参见 `references/mcp-tools.md`。

## Exchange

Exchange 是 ContextUI 的市场平台。您可以免费发布工作流，也可以设置价格。其他代理和用户可以发现、安装和使用您的工作流。

**完整的 API 文档：** `references/exchange-api.md`
**类别名称：** `references/exchange-categories.md`
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

1. **初始化** — `POST marketplace-upload-init`（获取预签名的 S3 URL）
2. **上传** — 直接将文件上传到 S3
3. **完成** — `POST marketplace-upload-complete`（创建列表）

详细信息和示例请参见 `references/exchange-api.md`。

### 定价与收益

- 免费或设置 `priceCents`（最低价格限制）
- **开发者获得 70%，平台获得 30%**
- 收益通过 Stripe 支付——收益会在开发者连接 Stripe 后才发放
- 开发者连接 Stripe 后，收益会自动转账

### 分类

`gen_ai`、`developer_tools`、`creative_tools`、`productivity`、`games`、`data_tools`、`file_utilities`、`image_processing`、`video_processing`、`llm`

### 畅销产品

- **实用工具** — 代理实际需要的工具（数据处理、可视化、监控）
- **模板** — 其他代理可以自定义的优质起点
- **集成工具** — 与流行服务/API 集成的工作流
- **创意工具** — 音乐、视频、图像生成工具

## 提供的工作流示例

ContextUI 提供了约 30 个经过优化的示例工作流。这些是标准参考模板——用户安装时会自动复制到他们的机器上。

**源代码位置：** `/Users/jasonclissold/Documents/electronCUI/example_modules/`
**安装位置：** ContextUI 工作流目录下的 `examples/` 文件夹

### 模板（新工作流的起点）
- `ThemedWorkflowTemplate` — 单色主题模板，包含所有 UI 模式（输入框、标签页、警报、卡片）
- `MultiColorWorkflowTemplate` — 适用于复杂 UI 的多色仪表板模板
- `ToolExampleWorkflow` — MCP 工具集成模板

### ServerLauncher 模式（Python 后端）
- `KokoroTTS` — ServerLauncher 的标准源代码。请从这里复制 `ui/ServerLauncher/`。
- `CowsayDemo` — 最简单的 ServerLauncher 示例（很好的起点）
- `ImageToText` — 带有 ServerLauncher 和子组件的完整多标签页布局
- `Localchat2` — 全功能聊天应用：流媒体、RAG、模型管理、分支功能

### 仅前端的应用
- `Spreadsheet` — 完整的电子表格应用
- `WordProcessor` — 文档编辑器
- `Presentation` — 幻灯片制作工具
- `SolarSystem` — 3D 可视化工具
- `PeriodicTable` — 交互式元素周期表
- `STLViewer` — 3D 模型查看器

### AI/ML 工作流
- `MusicGen` — AI 音乐生成
- `SDXLGenerator` — 稳定的扩散图像生成工具
- `RAG` — 检索增强生成
- `VoiceAgent` — 基于语音的 AI 代理
- `STT` — 语音转文本
- `AnimatedCharacter` — 与动画角色聊天

所有工作流的列表：`mcporter call contextui.list_workflows folder="examples"`
查看任意工作流：`mcporter call contextui.read_workflow path="<path>"`

## 代理注册

要将 ContextUI 作为代理使用：

1. **从 [contextui.ai](https://contextui.ai) 安装 ContextUI**
2. **配置 MCP** 以将您的代理连接到 ContextUI
3. **开始构建** — 创建工作流，发布到 Exchange，赚取积分

## Python 后端的最佳实践

### ServerLauncher 模式（必须使用）

所有使用 Python 后端的工作流 **必须** 使用 ServerLauncher 模式：

1. **从标准源代码复制**：`examples/KokoroTTS/ui/ServerLauncher/` → 您的工作流的 `ui/ServerLauncher/`
2. **始终使用 `uvicorn[standard]`**：不要仅使用 `uvicorn`。`[standard]` 版本支持 WebSocket。
3. **支持 GPU 的包**：ServerLauncher 会自动检测 CUDA/MPS/CPU 并使用预构建的轮子（wheel）。

```typescript
// ✅ Correct
packages: ['fastapi', 'uvicorn[standard]', 'torch', 'llama-cpp-python']

// ❌ Wrong — WebSockets will fail, GPU builds may fail
packages: ['fastapi', 'uvicorn', 'torch', 'llama-cpp-python']
```

### GPU 包的处理

ServerLauncher 会自动处理 GPU 相关的安装：

| 包 | CUDA (Windows/Linux) | Metal (Mac) |
|---------|---------------------|-------------|
| `torch` | 通过 `--index-url` 使用预构建的轮子 | 使用原生 pip 安装 |
| `llama-cpp-python` | 通过 `--extra-index-url` 使用预构建的轮子 | 需要手动编译（CMAKE_ARGS） |

**为什么使用预构建的轮子？** 在 Windows 上从源代码编译需要 CUDA Toolkit + Visual Studio Build Tools + CMake 的完美配置。使用预构建的轮子可以简化安装过程。

### 实时安装反馈

每次成功安装后，相关包会立即显示为绿色（不会一次性全部显示）。用户可以实时看到安装进度。

### HuggingFace 缓存监控

如果您的工作流下载了 HuggingFace 的模型，请检查 `blobs/` 和 `snapshots/` 目录：
- **跳过符号链接** 以避免重复计数
- 检查 `.incomplete` 文件以检测正在进行的下载

有关 RAG、MusicGen、LocalChat 等工具使用的完整缓存监控机制，请参阅 `references/cache-monitoring.md`。

## 提示

- **从示例开始** — 在从头开始编写代码之前，先阅读现有的工作流示例
- **进行视觉测试** — 使用 `launch_workflow` 和 `ui_screenshot` 来验证 UI 是否显示正确
- **清理** — 完成后使用 `close_workflow` 来关闭标签页（可以通过路径指定，或者省略路径来关闭当前活动的标签页）
- **使用深色主题** — 背景颜色设置为 `{color}-950`，文字颜色使用浅色。ContextUI 是一个深色模式的应用程序。
- **仅使用 Tailwind** — 不要使用自定义的 CSS 文件或 styled-components，而是在 JSX 中使用 Tailwind 类。
- **使用 Python 处理复杂任务** — 如果需要处理机器学习、API 或数据处理，编写 Python 后端，通过 MCP 启动它，然后通过 fetch 从 TSX 调用它。
- **使用标准示例**：在复制代码模式时，请以 `examples/KokoroTTS/` 作为参考——其中包含了最新的修复内容。

## 重要注意事项

### ServerLauncher 在关闭标签页时可能会关闭服务器

当您使用 `close_workflow` 重新加载代码时，清理操作会调用 `stopServer()`，导致服务器关闭。每次重新加载标签页后，都必须重新启动服务器（通过设置选项卡或 MCP 的 `python_start_server`）。

### 不要频繁检查服务器状态

仅在启动时检查一次服务器状态——不要每隔几秒就进行检查。频繁检查会导致不必要的资源消耗。如果需要响应服务器状态的变化，请使用钩子中的 `server.connected`。

### 通过 MCP 桥接切换标签页

通过将 JSON 数据写入 `~/ContextUI/.mcp-bridge/` 来切换标签页：
```json
{"type":"switch_tab","tab":"ExactComponentName","id":"unique_id"}
```
首先使用 `list_tabs` 获取准确的组件名称——部分匹配的路径可能不起作用。
响应文件会保存在同一目录下的 `{id}.response.json` 中。

### 测试时优先使用 MCP 工具

在测试工作流时，使用可用的 MCP 工具（`ui_click`、`ui_screenshot`、`launch_workflow`、`close_workflow`），而不是让用户手动点击界面。如果某些功能需要权限或访问权限，请告知用户具体需求。