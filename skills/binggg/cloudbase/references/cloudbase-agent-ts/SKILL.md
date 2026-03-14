---
name: cloudbase-agent-ts
description: "使用 Cloudbase Agent（TypeScript）构建和部署 AI 代理。Cloudbase Agent 是一个基于 TypeScript 的 SDK，实现了 AG-UI 协议。适用场景包括：  
1. 使用 @cloudbase/agent-server 部署代理服务器；  
2. 结合 ClientStateAnnotation 使用 LangGraph 适配器；  
3. 使用 clientTools() 结合 LangChain 适配器；  
4. 构建实现 AbstractAgent 接口的自定义适配器；  
5. 理解 AG-UI 协议的事件；  
6. 使用 @ag-ui/client 构建 Web UI 客户端；  
7. 使用 @cloudbase/agent-ui-miniprogram 构建微信小程序 UI。"
alwaysApply: false
---
# Cloudbase Agent（TypeScript）

这是一个TypeScript SDK，用于使用AG-UI协议将AI代理部署为HTTP服务。

> **注意：** 该技能仅适用于**TypeScript/JavaScript**项目。

## 适用场景

当您需要进行以下AI代理开发时，可以使用此技能：
- 使用AG-UI协议将AI代理部署为HTTP服务
- 使用LangGraph或LangChain框架构建代理后端
- 创建实现AbstractAgent接口的自定义代理适配器
- 理解AG-UI协议的事件和消息流
- 构建能够与AG-UI兼容的代理进行交互的Web UI客户端
- 构建用于AI代理交互的微信小程序UI

**不适用场景：**
- 仅用于调用AI模型的简单场景（请使用`ai-model-*`技能）
- CloudBase云函数（请使用`cloud-functions`技能）
- 不包含代理功能的CloudRun后端服务（请使用`cloudrun-development`技能）

## 使用方法（针对代码代理）

1. **选择合适的适配器**
   - 对于基于状态图的工作流程，使用LangGraph适配器
   - 对于基于链式的代理模式，使用LangChain适配器
   - 为特定的代理逻辑构建自定义适配器

2. **部署代理服务器**
   - 使用`@cloudbase/agent-server`来暴露HTTP端点
   - 根据需要配置CORS、日志记录和可观测性
   - 将代理服务器部署到CloudRun或任何Node.js托管环境中

3. **构建UI客户端**
   - 对于Web应用程序，使用`@ag-ui/client`
   - 对于微信小程序，使用`@cloudbase/agent-ui-miniprogram`
   - 连接到代理服务器的 `/send-message` 或 `/agui` 端点

4. **参考以下路由表**以获取每个任务的详细文档：

## 路由表

| 任务 | 参考文档 |
|------|------|
| 部署代理服务器 (@cloudbase/agent-server) | [server-quickstart](server-quickstart.md) |
| 使用LangGraph适配器 | [adapter-langgraph](adapter-langgraph.md) |
| 使用LangChain适配器 | [adapter-langchain](adapter-langchain.md) |
| 构建自定义适配器 | [adapter-development](adapter-development.md) |
| 理解AG-UI协议 | [agui-protocol](agui-protocol.md) |
| 构建UI客户端（Web或小程序） | [ui-clients](ui-clients.md) |
| 深入了解@cloudbase/agent-ui-miniprogram | [ui-miniprogram](ui-miniprogram.md) |

## 快速入门

```typescript
import { run } from "@cloudbase/agent-server";
import { LanggraphAgent } from "@cloudbase/agent-adapter-langgraph";

run({
  createAgent: () => ({ agent: new LanggraphAgent({ workflow }) }),
  port: 9000,
});
```