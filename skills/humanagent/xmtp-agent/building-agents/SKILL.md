---
name: building-agents
description: 核心 XMTP 代理 SDK 的设置与使用模式。适用于创建新代理、处理消息、配置中间件或设置环境变量等场景。该 SDK 会在代理初始化、XMTP 配置完成、消息处理或中间件实现时触发相应的操作。
license: MIT
metadata:
  author: xmtp
  version: "1.0.0"
---

# XMTP代理基础

使用`@xmtp/agent-sdk`在XMTP网络上构建基于事件驱动、中间件支持的消息代理。

## 适用场景

在以下情况下请参考本指南：
- 创建新的XMTP代理
- 设置环境变量
- 处理文本消息和事件
- 实现中间件
- 使用过滤器及上下文辅助工具

## 规则分类（按优先级）

| 优先级 | 分类 | 影响程度 | 前缀 |
|----------|----------|--------|--------|
| 1 | 设置 | 关键（CRITICAL） | `setup-` |
| 2 | 事件 | 高（HIGH） | `events-` |
| 3 | 中间件 | 中等（MEDIUM） | `middleware-` |
| 4 | 过滤器 | 中等（MEDIUM） | `filters-` |

## 快速参考

### 设置（关键（CRITICAL）  
- `setup-environment` - 配置代理的环境变量  
- `setup-from-env` - 使用`Agent.createFromEnv()`创建代理  
- `setup-manual` - 手动创建代理（包含签名功能）  

### 事件（高（HIGH）  
- `events-text` - 处理文本消息  
- `events-lifecycle` - 处理启动/停止事件  
- `events-conversation` - 处理新私信和群组对话  
- `events-message-types` - 处理不同类型的消息（如回复、附件等）  

### 中间件（中等（MEDIUM）  
- `middleware-basics` - 创建并注册中间件  
- `middleware-error-handling` - 处理中间件链中的错误  
- `middleware-command-router` - 使用`CommandRouter`处理特定命令  

### 过滤器（中等（MEDIUM）  
- `filters-message-types` - 按消息类型进行过滤  
- `filters-sender` - 过滤掉来自自身的消息  

## 安装  

```bash
npm install @xmtp/agent-sdk
# or
yarn add @xmtp/agent-sdk
```

## 快速入门  

```typescript
import { Agent } from "@xmtp/agent-sdk";
import { getTestUrl } from "@xmtp/agent-sdk/debug";

// Create agent using environment variables
const agent = await Agent.createFromEnv();

// Handle text messages
agent.on("text", async (ctx) => {
  await ctx.conversation.sendText("Hello from my XMTP Agent!");
});

// Log when ready
agent.on("start", () => {
  console.log(`Agent online: ${getTestUrl(agent.client)}`);
});

await agent.start();
```

## 环境变量  

| 变量 | 用途 | 示例 |
|----------|---------|---------|
| `XMTP_WALLET_KEY` | 钱包的私钥 | `0x1234...abcd` |
| `XMTP_DB_ENCRYPTION_KEY` | 数据库加密密钥 | `0xabcd...1234` |
| `XMTP_ENV` | 网络环境 | `dev` 或 `production` |
| `XMTP_DB_DIRECTORY` | 数据库目录 | `./data` |

## 使用方法  

详细说明请参阅各规则文件：  

```
rules/setup-environment.md
rules/events-text.md
rules/middleware-basics.md
```