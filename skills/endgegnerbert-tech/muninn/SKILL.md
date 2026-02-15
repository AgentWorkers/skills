---
name: muninn
version: 2.1.14
description: "**通用上下文协议（Universal Context Protocol, CXP）与AI代理的长期记忆（Long-Term Memory）**  
Muninn MCP为AI代理提供了项目级别的持久化存储功能，用于存储架构决策、开发模式以及相关的技术上下文信息。当代理需要在不同会话之间保留项目历史记录、快速检索相关代码片段（最多可节省95%的存储空间），或维护架构的一致性时，该工具尤为实用。它通过沙箱化的CXP引擎支持本地语义搜索，并采用零侵入式的安全模型来保护数据安全。  

**触发条件（Trigger Conditions）：**  
- 上下文（Context）  
- 内存（Memory）  
- 项目架构（Project Architecture）  
- 持久化学习（Persistent Learning）  
- 令牌优化（Token Optimization）  
- 语义搜索（Semantic Search）"
author: blackknight
tags: mcp, context, memory, productivity, long-term-memory
runtime: node
permissions:
  - path: "~/.muninn/"
    access: "read-write"
    description: "Global configuration and project state storage."
  - path: "./.muninn/"
    access: "read-write"
    description: "Project-local memory storage and context indices."
install: "npm install -g muninn-core"
---

# Muninn MCP

**面向人工智能驱动开发的通用内存层**

Muninn MCP（Memory Context Protocol）是一个标准化的内存层，确保人工智能代理能够访问项目特定的知识。它通过提供一个共享的、项目级的“大脑”（project-local “Brain”），弥合了不同AI会话和工具之间的差距。

## 安全性与风险缓解（符合审计标准）

Muninn MCP v2.1.14在架构设计上充分考虑了安全性与代理的安全性：

### 1. 命令注入防护（RCE）
- **仅执行二进制文件**：所有对内部`cxp`引擎的调用都使用`child_process.execFile`，从而绕过了shell解释过程，使得shell注入变得不可能。
- **输入验证**：所有查询都通过严格的白名单正则表达式（`/[\w\s\-\.\?\!\(\)\[\]]/`）进行验证。
- **长度限制**：输入长度被限制在500个字符以内，以防止缓冲区相关攻击。

### 2. 环境完整性（零攻击策略）
- **禁止强制修改**：自动写入`.cursorrules`或`CLAUDE.md`的操作被禁用。
- **仅限手动使用**：`enforce_rules`工具仅用于项目启动时的手动配置。
- **被动式中间件**：默认情况下，自动的上下文拦截功能被禁用；Muninn仅作为一个高保真的库使用，而不是一个拦截代理。

### 3. 本地优先的隐私保护原则
- **100% 本地处理**：任何数据、遥测信息或代码都不会离开主机机器。所有语义搜索都通过高性能的Rust引擎在设备上完成。

## 代理使用方式

代理通过Muninn MCP来维护项目级的“大脑”：
1. **同步**：在会话开始时调用`brain_check`以加载项目级别的知识。
2. **学习**：使用`add_memory`来处理架构决策、修复漏洞或引入新的开发模式。
3. **搜索**：利用`search_context`进行深度语义搜索，以查找相关的文件和逻辑。

## 设置

### 使用npm安装（推荐）
```bash
npm install -g muninn-core
```

### 手动配置
将相关配置添加到您的MCP设置文件中（例如`claude_desktop_config.json`）：
```json
{
  "mcpServers": {
    "muninn": {
      "command": "npx",
      "args": ["-y", "muninn-core"]
    }
  }
}
```

---
*由BlackKnight维护。版本：2.1.14*