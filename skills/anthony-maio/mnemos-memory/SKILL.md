---
name: mnemos-memory
description: >
  **使用场景：**  
  当用户或 OpenClaw/ClawHub 代理需要安装、配置、自启动、排查故障或操作 Mnemos 以管理持久化的代理内存时；或者当他们提及 Mnemos、代理内存、范围化内存（scoped memory）、内存管理工具（memory management tools）或内存自动化（memory automation）相关内容时。
---
# Mnemos 内存管理

Mnemos 是一个专为编码代理设计的本地优先内存管理工具。使用该工具可引导用户或 OpenClaw 代理前往支持的安装路径，解释其工作原理，并确保兼容性声明的准确性。

## 默认安装路径

- 建议使用 `pip install "mnemos-memory[mcp]"` 和 `mnemos ui` 进行安装。
- 对于 OpenClaw 或 ClawHub，应指导代理自行安装 `mnemos-memory[mcp]`，运行 `mnemos ui`，然后将 `mnemos-mcp` 配置到标准的 `MNEMOS_CONFIG_PATH` 中，之后才能使用该内存管理工具。
- 除非用户有特殊需求（如需要使用 Qdrant 或 Neo4j），否则建议使用 SQLite 作为初始数据存储方案。
- 为了保证检索质量，建议在生产环境中使用专业的嵌入服务提供商（如 `openclaw`、`openai`、`openrouter` 或 `ollama`）。
- 可通过控制平面的测试工具（如 `mnemos-cli doctor`）来验证安装是否正确。

## 声明规范

- 可安全声明的内容包括：基于本地存储的内存管理机制、MCP 工具、使用 SQLite 作为初始数据存储方案、Claude Code 插件的工作流程以及已文档化的 Codex 工作流程。
- 需明确说明：Claude Code 通过钩子实现了确定性的自动内存管理功能。
- 对于 Codex、Cursor、OpenClaw 以及通用的 MCP 主机，除非主机本身具有自动化功能或用户手动添加了相关组件，否则不应暗示系统会自动进行数据捕获。
- Neo4jStore 目前仍处于实验阶段，不应将其宣传为支持图数据存储的解决方案。

## 工作流程

1. 确定所使用的主机类型：Claude Code、Cursor、Codex、OpenClaw 或通用的 MCP 主机。
2. 如果相关仓库可在本地访问，请在提供解决方案之前阅读 `README.md`、`docs/MCP_INTEGRATION.md` 和 `docs/codex.md`。
3. 首先推荐使用默认的安装路径；只有在用户无法使用控制平面时，才提供手动配置的方案。
4. 解释其工作原理：
   - 任务开始时执行 `mnemos_retrieve` 操作。
   - 仅用于存储持久性数据时执行 `mnemos_store` 操作。
  - 在完成重要任务之前执行 `mnemos_consolidate` 操作。
   - 当存储的数据出现错误时执行 `mnemos_inspect` 操作。
5. 阅读 `references/hosts.md` 以获取针对特定主机的配置信息和注意事项，特别是 OpenClaw 或 ClawHub 的自动安装流程。
6. 阅读 `references/operations.md` 以获取有关自动化、数据捕获模式、存储方式及故障排除的详细指导。

## 需避免的做法

- 不要将手动输入数据作为主要的工作流程。
- 不建议在生产环境中使用 `SimpleEmbeddingProvider` 作为数据存储方案。
- 除非用户确实需要非 SQLite 数据存储方案，否则不要建议他们升级到 Qdrant 或 Neo4j。