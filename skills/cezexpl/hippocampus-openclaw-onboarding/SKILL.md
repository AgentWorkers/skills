---
name: hippocampus-openclaw-onboarding
description: 在品牌化、可重复的设置环境下启动 OpenClaw：包括工作区（workspace）、代理 ID（agent ID）、API 密钥（API key）或引导令牌（bootstrap token），以及 MCP 连接（MCP wiring）。
---
# Hippocampus OpenClaw 上线指南

当您将新的 OpenClaw 实例或工作空间连接到 Hippocampus 存储系统时，请使用本指南。

## 设置目标

- 定义一个稳定的工作空间名称。
- 为根代理分配一个唯一的 `agent_id`。
- 配置网关 URL 和身份验证信息。
- 确保子代理能够继承工作空间的内存身份信息。

## 推荐的操作流程

1. 通过 Hippocampus 门户进行注册或登录。
2. 在控制面板中创建一个根 OpenClaw 代理。
3. 复制生成的启动脚本（bootstrap one-liner）。
4. 运行以下命令：
   `npx hipokamp-mcp setup --bootstrap-token <token> --gateway <gateway-origin>`
5. 允许 `hipokamp-mcp` 将配置信息写入 `~/.hipokamp/config.json` 文件中。
6. 验证系统的运行状态，并完成首次的数据存储/检索操作。

## 注意事项

- 每个 OpenClaw 实例应使用一个根代理。
- 所有子代理的 ID 需要属于同一工作空间命名空间。
- 建议优先使用启动脚本进行配置，而非直接粘贴长期有效的 API 密钥。
- 不要在不相关的工作空间之间重复使用凭据。

## 相关组件

- `hippocampus-memory-core`：完成设置后使用的核心组件。
- `hippocampus-subagent-memory`：用于实现子代理的隔离管理。
- `@hippocampus/openclaw-context-engine`：用于实现与 Hippocampus 的原生生命周期集成。