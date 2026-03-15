---
name: relayplane
description: OpenClaw的代理操作层（Agent Operations Layer）：具备可观测性（observability）、治理能力（governance）以及成本优化（cost optimization）功能，并支持自动故障转移（automatic failover），确保您的系统设置始终稳定运行（Never breaks your setup）。
user-invocable: true
model-invocable: false
disableModelInvocation: true
homepage: https://relayplane.com
version: 4.1.0
author: Continuum
license: MIT
metadata:
  openclaw:
    emoji: "🔀"
    category: ai-tools
    instruction-only: true
---
# RelayPlane

**OpenRouter 的路由管理工具。RelayPlane 负责监控、控制和优化代理服务的运行。**

对于 OpenClaw 的高级用户来说，RelayPlane 是一个不可或缺的辅助工具。您的代理在每次会话中会发起大量 API 请求，而 RelayPlane 可以帮助您实时了解这些请求的详细情况、控制成本，并对它们进行统一管理。

## 功能概述

RelayPlane 是一个 **可选的优化层**，它位于代理的请求处理流程中。它能够将简单的请求路由到成本更低的处理模型上，同时严格执行预算限制，并记录所有请求的详细信息。如果出现任何问题，系统会自动切换回原始的直接服务提供商。

**核心原则：** RelayPlane 绝不成为系统运行的依赖项。即使代理服务出现故障，您的代理程序仍能继续正常工作，确保零停机时间。

## 安装

```bash
npm install -g @relayplane/proxy@latest
```

## 快速入门

```bash
# 1. Start the proxy (runs on localhost:4100 by default)
relayplane-proxy

# 2. Add to your openclaw.json:
#    { "relayplane": { "enabled": true } }

# 3. That's it. OpenClaw routes through RelayPlane when healthy,
#    falls back to direct provider calls automatically.
```

## ⚠️ 重要提示：**切勿设置 `BASE_URL`

**请勿这样做：**
```bash
# ❌ WRONG — hijacks ALL traffic, breaks OpenClaw if proxy dies
export ANTHROPIC_BASE_URL=http://localhost:4100
```

**建议使用配置文件进行配置：**
```json
// ✅ RIGHT — openclaw.json
{
  "relayplane": {
    "enabled": true
  }
}
```

通过配置文件的方式，系统会使用“断路器”机制来处理代理服务的故障：如果代理服务不可用，请求会直接转发到原始服务提供商。而直接设置 `BASE_URL` 会导致系统崩溃，因此请务必避免这种做法。

## 架构设计

```
Agent → OpenClaw Gateway → Circuit Breaker → RelayPlane Proxy → Provider
                                   ↓ (on failure)
                              Direct to Provider
```

- **断路器机制**：如果连续三次请求失败，系统会自动绕过代理服务，持续 30 秒。
- **自动恢复**：系统会通过健康检查来检测代理服务的恢复情况。
- **进程管理**：代理服务可以由 Gateway 自动启动和管理。

## 配置设置

基本配置（其余选项均使用默认值）：
```json
{
  "relayplane": {
    "enabled": true
  }
}
```

高级配置选项：
```json
{
  "relayplane": {
    "enabled": true,
    "proxyUrl": "http://127.0.0.1:4100",
    "autoStart": true,
    "circuitBreaker": {
      "failureThreshold": 3,
      "resetTimeoutMs": 30000,
      "requestTimeoutMs": 3000
    }
  }
}
```

## 命令行工具

| 命令 | 功能说明 |
|---------|-------------|
| `relayplane-proxy` | 启动代理服务器 |
| `relayplane-proxy stats` | 查看使用情况和成本明细 |
| `relayplane-proxy --port 8080` | 设置自定义端口 |
| `relayplane-proxy --offline` | 关闭遥测功能 |
| `relayplane-proxy --help` | 显示所有可用命令 |

## 程序化使用（v1.3.0 及以上版本）

```typescript
import { RelayPlaneMiddleware, resolveConfig } from '@relayplane/proxy';

const config = resolveConfig({ enabled: true });
const middleware = new RelayPlaneMiddleware(config);

// Route a request — tries proxy, falls back to direct
const response = await middleware.route(request, directSend);

// Check status
const status = middleware.getStatus();
console.log(middleware.formatStatus());
```

### 高级功能：全面代理服务管理

```typescript
import { createSandboxedProxyServer } from '@relayplane/proxy';

const { server, middleware } = createSandboxedProxyServer({
  enableLearning: true,    // Enable pattern detection
  enforcePolicies: true,   // Enforce budget/model policies
  relayplane: { enabled: true },  // Circuit breaker wrapping
});

await server.start();
// All three pillars active: Observes + Governs + Learns
// Circuit breaker protects against proxy failures
```

## v1.4.0 的新特性

**三大核心功能集成：**
- **监控**（学习引擎）：记录每次请求的详细信息，确保决策过程透明可查。
- **控制**（策略引擎）：设置预算上限、允许使用的模型列表以及审批流程。
- **优化**（学习引擎）：识别使用模式、提供成本优化建议并管理规则。

**沙箱模式架构（v1.3.0 及以上版本）：**
- **自动故障转移**：确保系统稳定运行，避免服务中断。
- **进程管理**：代理服务作为受控的子进程运行。
- **健康检查**：实时检测代理服务的运行状态。
- **统计与监控**：提供关键性能指标（如 p50/p95/p99 延迟、请求量等）。

**学习引擎接口（v1.4.0 及以上版本）：**
- `GET /v1/analytics/summary`：按时间范围查看分析数据。
- `POST /v1/analytics/analyze`：检测使用模式、异常情况并生成优化建议。
- `GET /v1/suggestions`：查看待处理的优化建议列表。
- `POST /v1/suggestions/:id/approve` / `reject`：处理优化建议。
- `GET /v1/rules`：查看当前生效的规则。
- `GET /v1/rules/:id/effectiveness`：评估规则的实际效果。

## 隐私保护

- **数据安全**：您的输入数据仅在本地处理，不会被发送到 RelayPlane 服务器。
- **匿名数据收集**：仅记录令牌使用次数、请求延迟及使用的模型信息。
- **随时可取消数据收集**：通过 `relayplane-proxy --offline` 命令关闭遥测功能。
- **完全离线模式**：使用 `relayplane-proxy --offline` 可使系统完全脱离网络环境。

## 相关链接

- **官方文档**：https://relayplane.com/docs
- **GitHub 仓库**：https://github.com/RelayPlane/proxy
- **npm 包**：https://www.npmjs.com/package/@relayplane/proxy