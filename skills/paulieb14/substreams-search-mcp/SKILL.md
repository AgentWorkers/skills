# 子流搜索

从 substreams.dev 注册表中搜索、检查和分析 Substreams 包——从发现阶段到部署阶段。

## 工具

- **search_substreams**：根据关键词、排序顺序和区块链网络在 substreams.dev 包注册表中进行搜索。
- **inspect_package**：检查 `.spkg` 文件，查看其模块图（DAG）、protobuf 输出类型、依赖关系以及 Mermaid 图表。
- **list_package_modules**：提供轻量级的模块列表，包括模块类型及其输入/输出信息。
- **get_sink_config**：分析数据接收端（sink）的配置，提取 SQL 模式，并生成可执行的 CLI 命令。

## 系统要求

- **运行环境**：Node.js >= 18（通过 `npx` 运行）。
- **环境变量**：无需任何环境变量。所有搜索和包检查操作均使用公共 API，无需 API 密钥。

## 安装

```bash
npx substreams-search-mcp
```

## 网络与数据处理方式

- `search_substreams` 会抓取 substreams.dev 注册表的公共页面数据（无需 API 密钥）。
- `inspect_package` 和 `get_sink_config` 从 spkg.io URL 下载 `.spkg` 文件以解析 protobuf 元数据。
- 该工具不使用本地数据库或持久化存储。
- SSE 传输方式（`--http` / `--http-only`）会在端口 3849 上启动一个本地 HTTP 服务器（可通过 `MCP_HTTP_PORT` 环境变量进行配置）。

## 使用场景

- 查找适用于任何区块链（如 Ethereum、Solana、Arbitrum、Base 等）的 Substreams 包。
- 在部署前检查模块图并了解数据流。
- 获取适用于 PostgreSQL、ClickHouse 或子图实体数据接收端的配置命令。
- 在没有内置数据接收端配置的包中查找兼容的数据接收端模块。