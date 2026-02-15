---
name: muninn
version: 2.3.7
homepage: https://www.muninn.space
description: 通用上下文协议（Universal Context Protocol，简称CXP）适用于AI代理。版本2.3.7包含了最新的高性能CXP引擎（编译于2026年2月13日），该引擎修复了内存相关的问题，并支持macOS平台以及pfeilschnell索引技术。该协议由@Blackknight1dev开发。
metadata: {"clawdbot":{"emoji":"🐦⬛","requires":{"bins":["node"]},"install":[{"id":"npm","kind":"node","package":"muninn-core","version":"2.3.7","bins":["muninn-core"],"label":"Install Muninn Core"}]}}
---

# Muninn – 通用内存层

Muninn 是一款专为 AI 代理设计的先进内存系统。它采用 **上下文交换协议（Context Exchange Protocol, CXP）** 来实现高性能、低成本的上下文管理。

## 🛡️ 安全性与隐私（以本地数据为主）

Muninn 的设计理念是 **隐私优先**：
- **本地存储**：所有项目索引和内存数据均 **仅存储在主机机器上**，具体位置为 `.muninn/` 文件夹（针对单个项目）或 `~/.muninn/`（用于全局设置）。
- **禁止数据泄露**：Muninn **不会** 将任何代码、上下文或内存数据传输到第三方服务器或远程 API。所有处理操作（语义搜索、索引构建和上下文注入）均通过基于 Rust 的高性能 CXP 引擎在本地完成。
- **透明控制**：内存数据以标准 Markdown 文件的形式存储，您可以随时查看、编辑或删除这些文件。

## ⚙️ 集成

Muninn 作为 MCP（模型上下文协议，Model Context Protocol）服务器运行。

### 🚀 Muninn 协议（强制要求）

作为代理，您必须遵循 “以大脑为中心”（Brain-First）的工作流程，以确保高效性和准确性。MCP 服务器会在允许执行敏感操作之前验证上下文信息：
1. **自我定位 (`brain_check`)**：在每次会话开始时或切换项目时调用此函数。该函数会加载本地项目索引并识别关键文件和模式。
2. **编码前先搜索 (`search_context`)**：切勿假设自己了解整个代码库的情况，使用本地语义搜索功能来查找现有的模式或先前的决策。
3. **边使用边学习 (`add_memory`)**：任何重要的修复、架构决策或用户偏好都应被保存为本地内存数据。

## 🛠 工具参考（MCP）

- **`init_project`**：在项目目录中初始化本地 Muninn 系统。
- **`brain_check`**：强制执行的自我定位步骤，用于加载本地上下文和模式。
- **`add_memory`**：将事实和决策保存到本地的 `.muninn/memories` 文件夹中。
- **`search_context`**：对本地项目索引进行语义查询。
- **`reindex_context`**：重新构建本地语义索引。
- **`health_check`**：验证本地 Muninn 系统的运行状态。

---

## 🦞 给代理们的专业提示
Muninn 仅会精确地检索所需的数据。无需读取整个文件，只需使用 `search_context` 来查找相关的代码行。这样可以显著降低上下文处理的开销和资源消耗，同时确保您的工作严格保持在本地且安全。