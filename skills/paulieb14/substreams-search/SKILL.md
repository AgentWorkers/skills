# 子流搜索（Substreams Search）

从 substreams.dev 注册表中搜索、检查和分析 Substreams 包——涵盖从发现到部署的整个过程。

## 工具

- **search_substreams**：根据关键词、排序顺序和区块链网络在 substreams.dev 包注册表中进行搜索。
- **inspect_package**：检查 `.spkg` 文件，查看其模块图（DAG）、protobuf 输出类型、依赖关系以及 Mermaid 图表。
- **list_package_modules**：提供轻量级的模块列表，包括模块类型及其输入/输出信息。
- **get_sink_config**：分析数据接收端（sink）的配置信息，提取 SQL 模式，并生成可执行的 CLI 命令。

## 安装

```bash
npx substreams-search-mcp
```

## 使用场景

- 查找适用于任何区块链（如 Ethereum、Solana、Arbitrum、Base 等）的 Substreams 包。
- 在部署前检查模块图并理解数据流。
- 获取用于 PostgreSQL、ClickHouse 或其他数据接收端（sink）的配置命令。
- 在没有内置数据接收端配置的包中查找兼容的数据接收端模块。