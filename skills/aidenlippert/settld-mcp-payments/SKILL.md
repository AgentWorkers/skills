---
name: settld-mcp-payments
description: 将 OpenClaw 代理连接到 Settld MCP，以实现基于报价的授权和可验证收据的付费工具调用。
version: 0.1.0
author: Settld
---
# Settld MCP Payments Skill

本技能用于指导 OpenClaw 代理使用 Settld 来执行付费的 MCP (Mandated Contracting Partner) 工具调用。

## 该技能的功能

- 发现 Settld 提供的 MCP 工具（例如：`settld.*`）
- 执行包含 x402 挑战/授权/重试流程的付费工具调用
- 从工具响应中获取可验证的支付/结算信息
- 在 Settld 中生成符合审计标准的日志记录和收据

## 先决条件

- Node.js 20 及以上版本
- Settld API 密钥（`SETTLD_API_KEY`）
- Settld API 基本 URL（`SETTLD_BASE_URL`）
- 租户 ID（`SETTLD_TENANT_ID`）
- 可选：付费工具的基地址（`SETTLD_PAID_TOOLS_BASE_URL`）

## MCP 服务器注册

请使用 `mcp-server.example.json` 文件中的服务器配置信息进行注册。

服务器命令示例：

```bash
npx ["-y","settld-mcp"]
```

**必需的环境变量：**
- `SETTLD_BASE_URL`
- `SETTLD_TENANT_ID`
- `SETTLD_API_KEY`

**可选的环境变量：**
- `SETTLD_PAID_TOOLS_BASE_URL`
- `SETTLD_PROTOCOL`

## 代理使用方法

1. 调用 `settld.about` 以验证连接是否正常。
2. 对于需要付费的搜索/数据请求，使用以下命令：
   - `settld.exa_search_paid`
   - `settld.weather_current_paid`
3. 对于与协议生命周期相关的操作，使用以下命令：
   - `settld.create_agreement`
   - `settld.submit_evidence`
   - `settld.settle_run`
   - `settld.resolve_settlement`

## 示例测试命令：

- “调用 `settld.about` 并返回结果 JSON。”
- “执行 `settld.weather_current_paid`，查询芝加哥地区的天气信息，并确保返回的响应中包含 `x-settld-*` 标头。”

## 安全注意事项

- 将 `SETTLD_API_KEY` 视为敏感信息，切勿在日志或聊天输出中显示其完整内容。
- 确保只有受信任的提供商和符合租户政策的用户才能使用这些付费工具。