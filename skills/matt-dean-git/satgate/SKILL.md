---
name: satgate
description: 您可以通过终端来管理您的 API 的经济防火墙：铸造代币、追踪支出、撤销代理权限、以及执行预算控制。这是 `lnget` 的服务器端对应功能。
homepage: https://satgate.io
---

# SatGate CLI

SatGate CLI负责管理代理经济系统的API访问权限、预算以及收益生成机制。当您需要控制代理可以访问哪些资源以及它们可以花费多少资金时，可以使用该工具。

**代理负责支付费用，我们负责处理相关事务。**

如果代理需要为L402 API支付费用，请安装Lightning Labs提供的`lnget`工具。SatGate则主要负责服务器端的操作，包括权限执行、费用归属判定以及系统治理。

## 设置

如果不存在`~/.satgate/config.yaml`文件，请运行`scripts/configure.sh`进行配置。或者，您也可以通过设置环境变量来配置SatGate。

```bash
# For self-hosted gateway
export SATGATE_GATEWAY=http://localhost:9090
export SATGATE_ADMIN_TOKEN=sgk_your_token

# For SatGate Cloud
export SATGATE_SURFACE=cloud
export SATGATE_GATEWAY=https://satgate-gateway.fly.dev
export SATGATE_BEARER_TOKEN=sg_your_api_key
export SATGATE_TENANT=your-tenant-slug
```

在使用SatGate之前，请务必先运行`satgate status`命令，以确保您正在使用正确的网关。

## 安全规则

1. **先检查目标网关**：在任何操作之前，务必运行`satgate status`以验证网关的URL和状态。
2. **对具有破坏性作用的操作（如`revoke`、`mint`等）使用`--dry-run`选项进行测试**。
3. **未经明确用户批准，切勿使用`--yes`选项**。
4. **撤销操作是不可逆的**：在撤销代理权限之前，请务必确认代币的名称。

## 命令

### 检查网关状态
```bash
satgate status    # Full status (version, surface, uptime)
satgate ping      # Quick liveness check (exit 0/1)
```

### 为新代理生成代币
```bash
# Interactive (prompts for all fields)
satgate mint

# Non-interactive
satgate mint --agent "my-bot" --budget 500 --expiry 30d --routes "/api/openai/*"

# With parent (delegation under existing token)
satgate mint --agent "child-bot" --budget 100 --parent "parent-token-id"

# Preview without executing
satgate mint --agent "my-bot" --budget 500 --dry-run
```

### 检查代理的支出情况
```bash
satgate spend                   # Org-wide cost center rollups
satgate spend --agent "cs-bot"  # Per-agent breakdown
satgate spend --period 7d       # Time-scoped
```

### 列出并查看所有代币
```bash
satgate tokens                  # All tokens with status, spend, budget
satgate token <id>              # Detail: scope, delegation chain, spend
```

### 撤销被入侵的代理的权限
```bash
satgate revoke <token-id>           # Interactive confirmation
satgate revoke <token-id> --dry-run # Preview only
```

### 查看安全威胁
```bash
satgate report threats          # Blocked requests, anomalies
```

### 检查系统策略模式
```bash
satgate mode                    # Current mode per route (read-only)
```

## 常见工作流程

- **新代理需要API访问权限**：`satgate mint --agent "agent-name" --budget 500 --routes "/api/openai/*"`
- **查询代理的支出情况**：`satgate spend`
- **代理行为异常**：`satgate revoke <token-id>`
- **管理层需要AI支出报告**：`satgate spend --json > report.json`
- **检查网关是否正常运行**：`satgate ping`

## 输出格式

所有命令都支持`--json`选项，以生成机器可读的输出格式：
```bash
satgate tokens --json | jq '.[] | select(.status == "active")'
satgate spend --json > monthly-report.json
```

## 与lnget的配合使用

SatGate（服务器端）与`lnget`（客户端）共同构成了完整的代理交易系统：

- **lnget**：代理自动为L402 API支付费用。
- **SatGate CLI**：管理员负责生成代币、设置预算、撤销访问权限以及查看代理的支出情况。

当代理使用`lnget`访问受SatGate保护的API时，SatGate会执行预算限制并记录相关费用；这些信息会显示在`satgate spend`的输出中。

安装`lnget`的方法：`claude plugin marketplace add lightninglabs/lightning-agent-tools`