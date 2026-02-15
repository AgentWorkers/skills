---
name: relayplane
description: 在每月通常花费100美元使用OpenClaw的情况下，每月可以节省约47美元。本地代理会自动将简单任务路由到成本更低的模型上进行处理。
user-invocable: true
model-invocable: false
disableModelInvocation: true
homepage: https://relayplane.com
version: 3.1.0
author: Continuum
license: MIT
metadata:
  openclaw:
    emoji: "🚀"
    category: ai-tools
    instruction-only: true
---
# RelayPlane

**每月在 OpenClaw 上花费 100 美元？只需保留 47 美元即可。** 已有超过 835 名开发者在使用该工具。

## 功能介绍

RelayPlane 是一个本地代理服务，它通过自动将简单的 LLM（Large Language Model）任务路由到成本更低的模型来帮助您节省费用。复杂的推理任务仍由 Opus 处理，而文件读取、状态检查以及简单的编辑操作则由 Haiku 完成。只需安装一次，无需修改任何代码；如果出现故障，系统会自动切换到备用方案。

**对于每月 API 使用量超过 60 美元的用户来说，该工具完全可以实现成本回收。** 如果您的月支出在 100 美元以上，预计每月可节省 40 至 70 美元。

## 安装

全局安装代理服务：

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

## 命令行接口 (CLI) 指令

安装完成后，可以直接使用以下 CLI 命令：

| 命令 | 功能 |
|---------|-------------|
| `relayplane-proxy` | 启动代理服务器 |
| `relayplane-proxy stats` | 查看使用情况和费用明细 |
| `relayplane-proxy telemetry off` | 禁用遥测功能 |
| `relayplane-proxy telemetry status` | 检查遥测设置状态 |
| `relayplane-proxy --help` | 显示所有可用选项 |

## 配置

代理服务默认运行在 `localhost:3001` 端口。您可以通过 CLI 参数进行配置：

```bash
relayplane-proxy --port 8080        # Custom port
relayplane-proxy --host 0.0.0.0     # Bind to all interfaces
relayplane-proxy --offline          # No telemetry, no network except LLM APIs
relayplane-proxy --audit            # Show telemetry payloads before sending
```

## 环境变量

在启动服务之前，请先设置您的 API 密钥：

```bash
export ANTHROPIC_API_KEY=sk-ant-...
export OPENAI_API_KEY=sk-...
# Optional: Google, xAI
export GEMINI_API_KEY=...
export XAI_API_KEY=...
```

## 隐私政策

- **您的输入内容仅保存在本地**，不会被发送到 RelayPlane；  
- **遥测数据仅包含令牌计数、延迟信息和使用的模型类型**；  
- **您可以随时选择退出遥测功能**（使用 `relayplane-proxy telemetry off`）；  
- **支持完全离线模式**（使用 `relayplane-proxy --offline`）。

## 相关链接

- **文档：** https://relayplane.com/docs  
- **GitHub 仓库：** https://github.com/RelayPlane/proxy  
- **npm 包：** https://www.npmjs.com/package/@relayplane/proxy