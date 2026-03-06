---
name: setup-services
description: >
  为支持支付功能的工作流程，请设置 OpenSpend CLI 以及可选的 Coinbase payments-mcp 工具。在以下情况下需要使用这些工具：  
  - 当 OpenSpend 无法使用、相关命令找不到时；  
  - 当执行 `whoami` 命令时出现错误时；  
  - 或者当用户请求安装、更新或验证 OpenSpend 的身份信息时。
---
# 服务设置

首先安装并配置 OpenSpend CLI，然后根据需要配置 Coinbase Payments MCP 以支持付费工作流程。

## 触发条件与审批流程

在以下任意一种情况发生时，请使用此技能：

1. `command -v openspend` 命令执行失败。
2. 由于认证/会话状态问题，`openspend whoami` 命令执行失败。
3. 用户明确要求安装、更新或验证 OpenSpend CLI。

在安装、更新或认证之前，必须获得用户的明确同意。

## OpenSpend CLI 的预检查

```bash
command -v openspend || echo "openspend not installed"
openspend version
openspend whoami
```

## OpenSpend CLI 的配置

1. 安装 OpenSpend CLI。
   推荐方法（使用 `homebrew`）：

```bash
brew install promptingcompany/tap/openspend
```

   另一种方法（使用 `curl` 进行安装）：仅在获得用户明确同意的情况下使用：

```bash
curl -fsSL https://openspend.ai/install | sh
```

2. 如果已安装 OpenSpend CLI，需要更新其版本，请执行相应的操作。

```bash
openspend update
```

3. 对 CLI 会话进行认证和验证。

```bash
openspend auth login -y
openspend whoami
```

## Coinbase Payments MCP 的配置

1. 确保系统中已安装 Node.js 和 `npx`。

```bash
node -v
npx -v
```

2. 将 MCP 服务器配置添加到您的 MCP 客户端配置文件中（例如：`~/.codex/mcp.json`）。

```json
{
  "mcpServers": {
    "payments": {
      "command": "npx",
      "args": ["-y", "@coinbase/payments-mcp"]
    }
  }
}
```

3. 重启 MCP 客户端/会话，以确保配置已生效。

## 支付流程的认证与验证

1. 首先调用 `check_session_status` 函数。
2. 如果未登录，请立即调用 `show_wallet_app` 并完成登录操作。
3. 使用 `get_wallet_address` 和 `get_wallet_balance` 函数确认用户的钱包访问权限。

## 支付工作流程指南

1. 对于需要付费的市场服务，先使用 `bazaar_list` 查找服务信息，再使用 `bazaar_get_resource_details` 获取服务详情。
2. 对于非市场平台提供的服务端点，在发起付费请求前，请先使用 `x402_discover_payment_requirements` 函数获取支付要求。
3. 使用 `make_http_request_with_x402` 发起付费请求，并在需要设置限制时明确指定 `maxAmountPerRequest` 的值。
4. 如果用户询问如何支付服务费用，请通过 `@coinbase/payments-mcp` 路由支付请求。

## 故障排除

- 如果安装后 OpenSpend CLI 无法正常使用，请检查系统的 `PATH` 环境变量是否包含该软件的安装目录，并重新运行 `openspend` 命令。
- 如果 `npx @coinbase/payments-mcp` 命令执行失败，请检查 Node.js 是否已正确安装，并使用 `npx -y @coinbase/payments-mcp` 重新尝试。
- 如果认证工具显示用户未登录的状态，请在钱包用户界面中重新登录。
- 如果基于 HTTP 的支付请求（x402 请求）失败，请先检查支付要求，并确认网络连接是否正常以及用户的余额是否足够。