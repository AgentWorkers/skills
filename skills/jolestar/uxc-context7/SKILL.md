---
name: context7
description: 使用 Context7 MCP 查询最新的库文档和代码示例。当您需要 npm 包、Python 库或其他编程语言的当前版本特定文档时，请使用该工具。
metadata:
  short-description: Query library docs via Context7 MCP
---
# Context7 技能

使用此技能可以查询库的文档和代码示例。

## 先决条件

- 已安装 `uxc` 技能（安装方法请参见 [uxc 技能](https://github.com/holon-run/uxc/tree/main/skills/uxc)）
- 具备访问 `https://mcp.context7.com/mcp` 的网络权限

## 核心工作流程

1. 默认情况下，使用固定的命令链接：
   - `command -v context7-mcp-cli`
   - 如果该命令不存在，请创建它：`uxc link context7-mcp-cli mcp.context7.com/mcp`
   - `context7-mcp-cli -h`
   - 如果检测到命令冲突且无法安全地重复使用，请停止操作，并请求技能维护者选择其他命令名称。

2. 将库名称解析为库 ID：
   - `context7-mcp-cli resolve-library-id libraryName=react query='useState hook'`

3. 查询文档：
   - `context7-mcp-cli query-docs libraryId=/reactjs/react.dev query='how to use useState'`

## 可用工具

- **resolve-library-id**：将包/库名称解析为 Context7 的库 ID
- **query-docs**：查询特定库的文档和代码示例

## 使用示例

### 查找 React 文档

```bash
# First resolve the library
context7-mcp-cli resolve-library-id libraryName=react query='React useState hook'
```

### 查询特定文档

```bash
context7-mcp-cli query-docs '{"libraryId":"/reactjs/react.dev","query":"how to use useEffect"}'
```

### 查询 Node.js 文档

```bash
context7-mcp-cli resolve-library-id libraryName=node query='file system'
```

## 注意事项

- 首先需要提供库名称，然后使用返回的库 ID 进行查询
- Context7 提供针对特定版本的最新文档
- 支持 npm 包、Python 库等
- `context7-mcp-cli <操作> ...` 等同于 `uxc mcp.context7.com/mcp <操作> ...`
- 如果链接设置暂时不可用，可以备用直接使用 `uxc mcp.context7.com/mcp ...` 的命令。

## 参考文件

- 工作流程详情：`references/usage-patterns.md`