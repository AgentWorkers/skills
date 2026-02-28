---
name: Apple Health
slug: apple-health
version: 1.0.0
homepage: https://clawic.com/skills/apple-health
description: 通过MCP设置将代理连接到Apple Health数据导出，实现模式验证和隐私安全的分析。
changelog: Initial release with Apple Health MCP integration workflow and guarded query patterns.
metadata: {"clawdbot":{"emoji":"❤️","requires":{"bins":["node","npx"],"env":["HEALTH_DATA_DIR"]},"install":[{"id":"npm","kind":"npm","package":"@neiltron/apple-health-mcp","bins":["apple-health-mcp"],"label":"Install Apple Health MCP Server (npm)"}],"os":["darwin","linux","win32"]}}
---
## 设置

首次使用时，请阅读 `setup.md` 以获取集成指南。

## 使用场景

当用户希望代理程序读取 Apple Health 数据以获取趋势分析、数据汇总或进行 SQL 分析时，可以使用本技能。代理程序负责处理数据导出的验证、与 MCP 服务器的连接以及安全的查询/报告流程，同时不会泄露用户的私人健康记录。

## 架构

数据存储在 `~/apple-health/` 目录下。具体设置方法请参阅 `memory-template.md`。

```
~/apple-health/
|-- memory.md              # Status, client integration state, latest export path
|-- integrations.md        # Connected MCP clients and validation notes
|-- query-log.md           # Reusable SQL/report prompts and known-good outputs
`-- archive/               # Retired paths and old troubleshooting notes
```

## 快速参考

根据需要使用这些文件，避免过度依赖主文档中的说明。

| 主题 | 文件名 |
|-------|------|
| 设置流程 | `setup.md` |
| 数据存储模板 | `memory-template.md` |
| MCP 客户端配置 | `mcp-config.md` |
| 查询模板 | `query-recipes.md` |
| 备用 CLI 路径 | `fallback-cli.md` |

## 核心规则

### 1. 在开始操作前确认集成模式
首先明确以下集成模式之一：
- `csv-export`：使用 Apple Health 的 CSV 导出格式并通过 MCP 服务器传输数据；
- `not-now`：用户仅处于规划阶段，尚未开始设置。

**注意**：切勿通过终端代理程序直接访问 HealthKit API。本技能仅依赖于导出的数据。

### 2. 在连接 MCP 服务器之前验证本地导出数据
在配置之前，必须确保以下条件：
- 导出文件夹必须存在于本地且可读；
- 文件夹中必须包含符合 `HKQuantityTypeIdentifier*.csv`、`HKCategoryTypeIdentifier*.csv` 或 `HKWorkoutActivityType*.csv` 格式的文件；
- 该文件夹不能是空的解压文件夹。

如果验证失败，请先修复数据路径问题。

### 3. 在配置 MCP 服务器之前进行运行时检查
在连接 MCP 服务器之前，请验证运行环境：
- 使用的 Node.js 版本必须是 LTS 版本（18、20 或 22）；
- 如果执行 `npx @neiltron/apple-health-mcp` 时出现 `duckdb.node` 未安装的错误，请切换到 LTS 版本的 Node.js 并重试；
- 确保 `HEALTH_DATA_DIR` 变量指向有效的绝对路径。

如果运行环境不兼容，请停止操作并修复问题。

### 4. 使用明确的路径和命令配置 MCP 服务器
请按照 `mcp-config.md` 中的说明配置 MCP 服务器：
- 命令：`npx`
- 参数：`[@neiltron/apple-health-mcp]`
- 环境变量：`HEALTH_DATA_DIR=/absolute/path/to/export`

切勿使用未经验证的占位符或相对路径。

### 5. 先定义数据结构，再执行查询
首先运行 `health_schema` 命令以发现数据结构并映射可用表格；
之后再执行 `health_query` 或 `health_report`。

如果表格名称与预期不同，请根据实际数据结构调整 SQL 语句。

### 6. 默认使用带时间范围的查询
所有分析查询都应包含时间范围和明确的单位；
建议使用滚动窗口（如 `last 7d`、`30d`、`90d`），并且一次最多比较两个时间窗口。

**注意**：除非用户特别要求，否则避免进行无时间范围的完整历史数据扫描。

### 7. 监控数据更新情况并及时刷新
在内存中记录最后一次数据导出的时间戳，当数据过时时发出警告；
如果用户需要当天的分析结果，请先请求最新的 iPhone 数据导出。

## 常见问题

- **错误1**：假设终端代理程序可以直接访问 HealthKit 数据 → 设置失败（实际只能使用导出的数据）；
- **错误2**：在 MCP 配置中使用了错误的导出路径 → 服务器虽然启动但无法返回数据；
- **错误3**：在未完成数据结构检测之前执行 SQL 查询 → 由于表格名称错误导致查询失败；
- **错误4**：对大量数据进行无时间范围的查询 → 分析速度慢且输出结果不准确；
- **错误5**：使用过时的数据导出结果生成“今日”指标 → 推荐结果不准确；
- **错误6**：在非 LTS 版本的 Node.js 上运行 MCP 包 → 可能导致 DuckDB 模块错误，从而影响程序启动。

## 外部接口

| 接口 | 发送的数据 | 用途 |
|---------|-----------|---------|
| https://registry.npmjs.org | 仅包含 MCP 服务器包的安装元数据 | 下载 MCP 服务器包 |
| https://raw.githubusercontent.com | 公开的 markdown 文档 | 查看备用技能的详细说明 |
| https://apps.apple.com | 应用程序下载链接 | 下载用于 iPhone 的 CSV 导出工具 |

**注意**：默认情况下，不应将任何健康记录数据发送到外部。

## 安全性与隐私

**外部传输的数据**：
- 发送到 npm 的包安装请求；
- 来自 App Store 的可选应用程序下载数据。

**本地存储的数据**：
- Apple Health 的 CSV 导出文件；
- MCP 服务器的查询结果和汇总数据；
- 存储在 `~/apple-health/` 目录中的数据。

**本技能的特性**：
- **不直接访问 iCloud Health 数据**；
- **不会绕过 Apple 的权限提示**；
- **除非用户明确要求，否则不会上传健康数据文件**。

## 注意事项

使用本技能意味着您依赖第三方工具（`@neiltron/apple-health-mcp` 及相应的 iPhone 数据导出工具）；
请仅在确认信任这些工具的情况下进行安装和运行。

## 相关技能

如果用户同意，可以使用以下技能进行扩展：
- `clawhub install <slug>`：安装相关工具：
  - `health`：提供通用的健康数据处理指南；
  - `ios`：针对 iOS 平台的设置和故障排除；
  - `sleep`：用于分析睡眠数据的工作流程；
  - `api`：提供可靠的 API 接口和集成调试工具；
  - `swift`：在涉及应用程序代码时提供 HealthKit 相关的实现细节。

## 反馈建议

- 如果觉得本技能有用，请给 `clawhub` 评分（例如：给 `apple-health` 给予星标）；
- 为了获取最新信息，请使用 `clawhub sync` 命令保持同步。