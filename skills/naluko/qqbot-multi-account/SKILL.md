---
name: qqbot-multi-account
slug: qqbot-multi-account
version: 1.0.0
author: OpenClaw Community
description: >
  **QQBot 多账号运维排障技能**  
  适用于 OpenClaw 环境中涉及多个机器人（Bot）和多个代理（Agent）的场景，提供账号绑定检查、重复会话诊断以及主动发送消息等功能，并支持与本地插件进行数据打包和导出。  
  **相关术语说明：**  
  - **QQBot 多账号**：指在同一系统中管理多个 QQBot 账号。  
  - **双机器人**：指系统中同时运行两个或多个 QQBot 实例。  
  - **双代理**：指系统中同时运行两个或多个代理服务器。  
  - **账号绑定**：指将用户账号与特定 QQBot 或代理服务器关联的过程。  
  - **重复会话**：指同一用户在同一时间段内多次发起的会话请求。  
  - **appId 隔离**：指对不同账号或代理使用的唯一标识符（appId）进行区分和管理。  
  **主要功能：**  
  1. **账号绑定检查**：验证多个账号是否已正确绑定到相应的 QQBot 或代理服务器。  
  2. **重复会话诊断**：识别并处理用户在同一时间段内重复发起的会话请求，避免系统资源浪费。  
  3. **主动发送消息**：根据预设规则或用户指令，向指定账号或代理发送消息。  
  4. **本地插件集成**：支持与第三方插件集成，实现更丰富的功能扩展。  
  **使用场景示例：**  
  - 在企业级应用中，需要确保每个员工使用的 QQBot 账号与正确的代理服务器匹配。  
  - 当检测到重复会话时，系统可以自动阻止或提醒用户。  
  - 可以通过配置规则，实现自动化消息发送，提高工作效率。  
  **触发词示例：**  
  - “检查 QQBot 多账号绑定情况”  
  - “排查双机器人导致的系统故障”  
  - “实现 appId 隔离，提升系统安全性”  
  - “优化重复会话处理逻辑”
metadata:
  openclaw:
    emoji: 🤖
    tags: [qqbot, multi-account, multi-agent, routing, troubleshooting, diagnostics]
---
# QQBot 多账户管理

这是一项专为在多账户、多代理环境中运行 QQBot 的 OpenClaw 操作员设计的可发布技能。

## 适用场景

- `K1 -> 主节点`、`K2 -> 代理2` 的部署模式
- 诊断由于跨账户事件处理导致的重复会话问题
- 验证绑定信息（bindings）、账户信息（accounts）、应用 ID（appId）、网关端口（gateway port）以及运行时状态（runtime state）
- 通过特定的机器人账户发送主动 QQ 消息或文件
- 将本地的 `qqbot` 插件导出为可移植的压缩文件，以便后续使用或备份

## 该技能的功能

- 了解多账户 QQBot 路由所需的最低配置要求
- 检查绑定信息（bindings）和账户定义（accounts）是否与预期的代理映射（agent map）一致
- 识别运行时状态下导致重复会话问题的根本原因
- 快速检查本地 OpenClaw 与 QQBot 的部署情况
- 将本地修改过的插件打包，以便传输或发布

## 最低配置示例

```json
{
  "bindings": [
    {
      "agentId": "main",
      "match": {
        "channel": "qqbot",
        "accountId": "K1"
      }
    },
    {
      "agentId": "agent2",
      "match": {
        "channel": "qqbot",
        "accountId": "K2"
      }
    }
  ],
  "channels": {
    "qqbot": {
      "enabled": true,
      "accounts": {
        "K1": {
          "appId": "YOUR_APP_ID_1",
          "clientSecretFile": "/path/to/qqbot_k1.secret",
          "name": "K1"
        },
        "K2": {
          "appId": "YOUR_APP_ID_2",
          "clientSecretFile": "/path/to/qqbot_k2.secret",
          "name": "K2"
        }
      }
    }
  }
}
```

## 关键实施注意事项

如果一条 QQ 消息同时到达两个代理节点，请不要立即认为绑定信息（bindings）有误。在多账户部署环境中，插件运行时必须根据应用 ID（appId）来隔离各个账户的状态，特别是以下方面：
- 访问令牌缓存（access token cache）
- 单次请求令牌处理机制（token singleflight promise）
- 背景令牌刷新控制器（background token refresh controller）

如果这些配置是全局性的（而非账户级别的），则一个账户可能会占用另一个账户的事件流，从而导致重复会话。

## 推荐的工作流程

### 1. 检查本地状态

```bash
bash {baseDir}/scripts/inspect-qqbot.sh
```

### 2. 查阅相关参考资料

- `references/multi-account-routing.md`
- `references/proactive-send.md`

### 3. 在需要时导出本地插件

```bash
bash {baseDir}/scripts/export-local-qqbot.sh
```

默认情况下，该操作会将插件导出为可移植的压缩文件，并保存在 `{baseDir}/dist/` 目录中。