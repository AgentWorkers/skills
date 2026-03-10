---
name: agent-chat-ux
version: 1.5.2
author: Charles Sears
description: "OpenClaw 控制界面的多代理用户体验功能包括：  
- 代理选择器  
- 单个代理的会话管理  
- 带搜索功能的会话历史查看器  
- 根据代理名称筛选的会话标签页  
- 创建代理的向导  
- 表情符号选择器  
- 后端代理的创建、读取、更新和删除（CRUD）操作  
- 用于显示代理授权状态的徽章  
这些功能共同构成了 OpenClaw 控制界面的核心用户交互组件。"
---
# agent-chat-ux

**名称:** agent-chat-ux  
**版本:** 1.5.2  
**作者:** Charles Sears  
**描述:** 用于 OpenClaw 控制界面的多代理用户体验功能 — 包括代理选择器、代理会话管理、带搜索功能的会话历史查看器、可按代理筛选的会话列表（会话名称友好显示）、创建代理向导、表情符号选择器，以及后端代理的创建、更新和删除操作。

---

## ⚠️ 安全性与透明度说明

在应用此技能的补丁之前，请注意以下事项：

### 凭据访问 (`agents.wizard`)

AI 向导的后端（`agents.wizard` RPC）会通过 HTTP 直接调用配置的模型提供者 API。为此，它需要一个 API 密钥。凭证的解析顺序如下：  
1. **默认配置认证** — 如果解析模式为 `api-key`（最常见情况），则使用该方式。  
2. **认证配置文件** — 查找与提供者匹配的第一个 `api_key` 类型的配置文件。仅读取 `provider` 和 `type` 字段；不会记录日志或返回其他信息。  
3. **环境变量** — 最后尝试使用 `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY`。  

> **如果您不希望向导读取您的认证配置文件**，请在环境中设置 `ANTHROPIC_API_KEY`，并确保默认认证模式已经是 `api-key` — 在这种情况下，步骤 2 将完全跳过。  

### 外部 API 调用

`agents.wizard` 会进行一次 HTTP POST 请求，目标地址为：  
- `https://api.anthropic.com/v1/messages`（Anthropic 模型）  
- `https://api.openai.com/v1/chat/completions`（OpenAI 兼容模型）  

该请求仅携带用户提供的描述信息，不包含来自您系统的其他数据。  

### 补丁范围

这些补丁仅修改与代理相关的文件：  
| 补丁 | 被修改的文件 | 修改内容 |