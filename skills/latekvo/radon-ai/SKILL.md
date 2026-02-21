---
name: radon-ai
description: 使用 Radon IDE 的 AI 工具进行 React Native 开发：可以查询库文档、查看日志和网络流量、截图、检查组件树结构，并与用户的应用程序进行交互。
license: MIT
metadata:
  ecosystem: react-native
  author: Software Mansion
---
## 该技能提供的功能

Radon AI 是一个 MCP（Machine Learning Platform）服务器，它提供了一套工具来增强您的开发体验。这些工具可以帮助您获取 React Native 生态系统的最新信息，访问一系列原本无法获得的调试数据，并直接与您的应用程序进行交互。

我们为大多数 React Native 库及其相关文档、版本、API、配置细节和使用模式建立了索引，以提供更全面和准确的信息。该知识库每天都会更新。

## 可用的工具

- `get_library_description`：返回库的详细描述及其使用场景。
- `query_documentation`：根据提供的查询返回相关的文档片段。
- `reload_application`：触发正在开发模拟器中运行的应用程序的重新加载。当您需要重置应用程序的状态，或者应用程序因某些操作而崩溃或出现故障时，可以使用此工具。共有三种重新加载方法：
  - `reloadJs`：仅重新加载 JavaScript 部分，不会触发应用程序的本地部分的重建或重启。适用于需要重新启动 JavaScript 状态的情况。
  - `restartProcess`：重启应用程序的本地部分。适用于需要重置出现故障的本地库或组件的情况。
  - `rebuild`：同时重建 JavaScript 和本地部分。当对本地部分进行了修改时，需要使用此方法，因为这些修改通常会导致应用程序的完全重建。
- `view_application_logs`：返回所有的构建、打包和运行时日志。当用户遇到应用程序问题、构建失败或控制台出现错误时，可以使用此功能。
- `view_screenshot`：显示应用程序开发视口的截图。当需要检查用户在移动设备上看到的内容时，可以使用此功能。
- `view_component_tree`：显示正在运行的应用程序的组件树（视图层次结构）。此工具仅显示已挂载的组件，因此项目的某些部分可能无法显示。在需要了解 UI 整体结构（例如解决布局问题或查看项目文件结构与组件结构之间的关系）时，可以使用此工具。
- `view_network_logs`：查看网络调试器的内容。返回应用程序发起的所有网络请求的列表，包括方法、URL、状态、时长和大小等信息。此工具可用于调试网络问题、检查 API 调用或验证应用程序是否与后端服务正确通信。接受一个 `pageIndex` 参数（基于 0 的索引或 `"latest"`）。
- `view_network_request_details`：获取特定网络请求的所有详细信息。返回给定请求的头部信息、请求体和其他元数据。在 `view_network_logs` 之后使用此工具来详细检查某个特定请求。接受一个 `requestId` 参数。

## 何时使用这些工具

- 在使用 VS Code 或 Cursor 运行 Radon IDE 的 React Native 或 Expo 项目中工作时。
- 使用 `query_documentation` 和 `get_library_description` 来获取关于库的准确、最新的信息，而不是依赖训练数据。
- 使用 `view_application_logs` 和 `view_screenshot` 来调试运行时错误、构建失败或 UI 问题。
- 在对应用程序进行结构更改之前，使用 `view_component_tree` 来了解组件的层次结构。
- 在对代码进行更改后，使用 `reload_application` 来验证修复效果或查看更改是否已反映在运行的应用程序中。
- 使用 `view_network_logs` 和 `view_network_request_details` 来调试网络问题、检查 API 调用或验证后端通信。

## 先决条件

- 必须在 VS Code 或 Cursor 中安装并激活 Radon IDE 扩展程序。
- 必须打开一个正在运行 Radon IDE 的 React Native 或 Expo 项目。
- 拥有有效的 Radon IDE 许可证。

## 限制

- Radon AI 提供的响应仍可能包含大型语言模型（LLM）的错误。在采取任何行动之前，请务必验证重要信息！
- 该知识库仅包含文档文件，不包含库的完整源代码。