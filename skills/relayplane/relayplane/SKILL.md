---
name: relayplane
description: 通过智能模型路由，可将 API 成本降低 40% 至 60%。系统会自动将简单任务路由到成本更低的模型进行处理。
user-invocable: true
model-invocable: false
disableModelInvocation: true
homepage: https://relayplane.com
version: 3.0.0
author: Continuum
license: MIT
metadata:
  openclaw:
    emoji: "🚀"
    category: ai-tools
    instruction-only: true
---

# RelayPlane

**通过智能模型路由，将您的AI API成本降低40-60%**

## 功能介绍

RelayPlane是一个本地代理，它根据任务的复杂程度将您的LLM（Large Language Model）请求路由到最合适的模型。简单任务会被发送到成本较低的模型（如Haiku），而需要复杂推理的任务则会使用更高级的模型（如Opus）。

## 安装

全局安装代理：

```bash
npm install -g @relayplane/proxy
```

## 快速入门

```bash
# 1. Start the proxy
relayplane-proxy

# 2. Point OpenClaw at it (add to your shell config)
export ANTHROPIC_BASE_URL=http://localhost:3001
export OPENAI_BASE_URL=http://localhost:3001

# 3. Run OpenClaw normally - requests now route through RelayPlane
```

## 命令行接口（CLI）命令

安装完成后，可以直接使用以下命令：

| 命令 | 描述 |
|---------|-------------|
| `relayplane-proxy` | 启动代理服务器 |
| `relayplane-proxy stats` | 查看使用情况和成本明细 |
| `relayplane-proxy telemetry off` | 禁用遥测功能 |
| `relayplane-proxy telemetry status` | 检查遥测设置状态 |
| `relayplane-proxy --help` | 显示所有可用命令 |

## 配置

代理默认运行在`localhost:3001`端口上。您可以通过CLI参数进行配置：

```bash
relayplane-proxy --port 8080        # Custom port
relayplane-proxy --host 0.0.0.0     # Bind to all interfaces
relayplane-proxy --offline          # No telemetry, no network except LLM APIs
relayplane-proxy --audit            # Show telemetry payloads before sending
```

## 环境变量

在启动之前，请设置您的API密钥：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
# Optional: Google, xAI
export GEMINI_API_KEY=...
export XAI_API_KEY=...
```

## 隐私政策

- **您的输入内容仅保存在本地**，不会被发送到RelayPlane；
- **遥测数据为匿名化信息**，仅包含令牌计数、延迟和使用的模型信息；
- **您可以随时选择退出遥测功能**：`relayplane-proxy telemetry off`；
- **支持完全离线模式**：`relayplane-proxy --offline`。

## 链接

- **文档**：https://relayplane.com/docs
- **GitHub仓库**：https://github.com/RelayPlane/proxy
- **npm包**：https://www.npmjs.com/package/@relayplane/proxy