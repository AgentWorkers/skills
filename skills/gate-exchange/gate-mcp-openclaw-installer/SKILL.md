---
name: gate-mcp-openclaw-installer
description: 适用于所有 Gate.com MCP 服务器的一键安装程序，涵盖现货/期货交易、去中心化交易所（DEX）、市场信息和新闻等功能。适用于用户需要使用 mcporter 来安装、配置或管理 Gate MCP 服务器的场景。
---
# Gate MCP

这是为 OpenClaw 完整开发的 Gate.com MCP 服务器安装程序。

## 快速入门

```bash
# Install all Gate MCP servers (default)
./scripts/install.sh

# Selective installation
./scripts/install.sh --select
```

## MCP 服务器

| 服务器 | 端点          | 认证方式 | 说明                |
|--------|--------------|---------|-------------------|
| `gate`   | `npx -y gate-mcp`    | API 密钥 + 秘钥   | 现货/期货/期权交易        |
| `gate-dex` | `https://api.gatemcp.ai/mcp/dex` | 固定的 x-api-key (MCP_AK_8W2N7Q) + 授权方式: Bearer ${GATE_MCP_TOKEN}` | DEX 操作             |
| `gate-info` | `https://api.gatemcp.ai/mcp/info` | 无                | 市场数据             |
| `gate-news` | `https://api.gatemcp.ai/mcp/news` | 无                | 新闻推送             |

## 安装模式

### 1. 全部安装（默认）
```bash
./scripts/install.sh
```
安装全部 4 个服务器。安装过程中会提示输入 API 凭据。

### 选择性安装
```bash
./scripts/install.sh --select
# or
./scripts/install.sh -s
```
通过交互式菜单选择要安装的服务器。

## 常用命令

```bash
# Market data (no auth)
mcporter call gate-info.list_tickers currency_pair=BTC_USDT
mcporter call gate-news.list_news

# Trading (requires auth)
mcporter call gate.list_spot_accounts
mcporter call gate.list_tickers currency_pair=ETH_USDT

# Wallet (requires auth)
mcporter call gate-dex.list_balances
```

## API 配置

### 获取 API 密钥
1. 访问 https://www.gate.com/myaccount/profile/api-key/manage
2. 创建具有以下权限的 API 密钥：
   - **读取**：市场数据、账户信息
   - **交易**：现货/保证金/期货交易
   - **提款**：钱包操作

### Gate-Dex 的授权
当执行 `gate-dex` 操作（如 `list_balances`、`transfer`、`swap`）时，如果系统提示“需要授权”，请按照以下步骤操作：
   (1) 打开 [https://web3.gate.com/](https://web3.gate.com/) 创建或绑定钱包（如需）；
   (2) 系统会提供一个可点击的 Google 认证链接，点击该链接完成 OAuth 授权。安装程序使用固定的 x-api-key 进行认证。

### 凭据存储
安装程序会将 API 凭据安全地存储在 `mcporter` 配置文件中。

## 故障排除

**找不到 mcporter**
```bash
npm install -g mcporter
```

**连接失败**
- 确认 API 密钥是否正确
- 检查网络连接
- 确保 `mcporter` 守护进程正在运行：`mcporter daemon status`

## 参考资料
- [Gate MCP GitHub 仓库](https://github.com/gate/gate-mcp)
- [Gate Skills 项目](https://github.com/gate/gate-skills)
- [Gate API 文档](https://www.gate.com/docs/developers/apiv4/en/)