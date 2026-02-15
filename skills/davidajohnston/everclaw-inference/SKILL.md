---
name: everclaw
version: 0.9.7
description: 您所拥有的AI推理能力将通过Morpheus去中心化网络持续为OpenClaw代理提供支持。您可以通过质押MOR代币来使用Kimi K2.5及30多个模型，并通过循环利用已质押的MOR代币来维持推理功能的持续运行。该系统具备以下特性：  
- Morpheus API Gateway支持零配置启动；  
- 兼容OpenAI的代理服务，具备自动会话管理功能；  
- 具备自动重试机制，可自动创建新的会话；  
- 支持OpenAI标准的错误分类机制，以防止冷却效应（cooldown effects）的累积；  
- 支持Venice API密钥的多密钥认证机制；  
- Gateway Guardian v4版本具备计费监控功能；  
- 提供通过OpenClaw进行的推理探针（inference probes）；  
- 支持Venice DIEM信用的主动监控；  
- 为陷入僵局的子代理提供断路器（circuit breaker）保护机制；  
- 具备自动重启功能；  
- 智能会话管理功能，可防止仪表板过载；  
- 集成了多种安全防护措施；  
- 通过macOS Keychain实现零依赖的钱包管理；  
- 提供x402支付客户端，支持代理之间的USDC交易；  
- 支持ERC-8004标准，可用于在Base平台上发现无需信任的代理（trustless agents）。
homepage: https://everclaw.com
metadata:
  openclaw:
    emoji: "♾️"
    requires:
      bins: ["curl", "node"]
      env:
        - name: WALLET_PRIVATE_KEY
          optional: true
          description: "Morpheus wallet private key — injected at runtime from 1Password or macOS Keychain. NEVER stored on disk."
        - name: ETH_NODE_ADDRESS
          optional: true
          default: "https://base-mainnet.public.blastapi.io"
          description: "Base mainnet RPC endpoint for blockchain operations."
        - name: OP_SERVICE_ACCOUNT_TOKEN
          optional: true
          description: "1Password service account token (retrieved from macOS Keychain at runtime)."
    credentials:
      - name: "Wallet Private Key"
        storage: "macOS Keychain or 1Password (never on disk)"
        required: false
        description: "Required only for local P2P inference (MOR staking). Not needed for API Gateway mode."
      - name: "Morpheus API Gateway Key"
        storage: "openclaw.json providers config"
        required: false
        description: "Free API key from app.mor.org. Community bootstrap key included for initial setup."
    network:
      outbound:
        - host: "api.mor.org"
          purpose: "Morpheus API Gateway — model inference and session management"
        - host: "base-mainnet.public.blastapi.io"
          purpose: "Base L1 RPC — blockchain transactions (session open/close, MOR staking)"
        - host: "provider.mor.org"
          purpose: "Morpheus P2P network — direct inference via staked sessions"
        - host: "api.venice.ai"
          purpose: "Venice API — primary inference provider (when configured)"
      local:
        - port: 8082
          purpose: "Morpheus proxy-router (Go binary) — blockchain session management"
        - port: 8083
          purpose: "Morpheus-to-OpenAI proxy (Node.js) — translates OpenAI API to proxy-router"
    persistence:
      services:
        - name: "com.morpheus.router"
          purpose: "Proxy-router for Morpheus P2P inference"
          mechanism: "launchd KeepAlive (macOS)"
        - name: "com.morpheus.proxy"
          purpose: "OpenAI-compatible proxy translating to Morpheus"
          mechanism: "launchd KeepAlive (macOS)"
        - name: "ai.openclaw.guardian"
          purpose: "Gateway health watchdog with billing-aware escalation"
          mechanism: "launchd StartInterval (macOS)"
      directories:
        - "~/morpheus/ — proxy-router binary, config, session data"
        - "~/.openclaw/workspace/skills/everclaw/ — skill files"
        - "~/.openclaw/logs/ — guardian logs"
    install:
      method: "git clone (recommended) or clawhub install everclaw-inference"
      note: "curl | bash installer available but users should review scripts before executing. All scripts are open source at github.com/profbernardoj/everclaw."
    tags: ["inference", "everclaw", "morpheus", "mor", "decentralized", "ai", "blockchain", "base", "persistent", "fallback", "guardian", "security"]
---

# ♾️ Everclaw — 您专属的AI推理工具，持续为您的OpenClaw代理提供强大支持

*由[Morpheus AI](https://mor.org)提供支持*

您可以使用自己的推理能力访问Kimi K2.5、Qwen3、GLM-4、Llama 3.3等模型。Everclaw将您的OpenClaw代理连接到Morpheus的P2P网络：您可以质押MOR代币、开启会话，并通过这些操作持续、自主地使用AI服务。

> 📦 **ClawHub命令：** `clawhub install everclaw-inference` — [clawhub.ai/DavidAJohnston/everclaw-inference](https://clawhub.ai/DavidAJohnston/everclaw-inference)

> ⚠️ **名称冲突警告：** ClawHub上还有一个名为“Everclaw Vault”的不同产品，它也使用了“everclaw”这个名称。**请务必使用`everclaw-inference`**，切勿使用`clawhub install everclaw`或`clawhub update everclaw`。详情请参阅`CLAWHUB_WARNING.md`。

## 工作原理

1. **获取MOR代币**：通过Uniswap或Aerodrome从ETH/USDC兑换MOR代币（具体步骤见下文）。
2. 在本地运行一个**代理路由器**（Morpheus Lumerin Node）作为客户端。
3. 路由器连接到Base主网并查找模型提供者。
4. 持质押的MOR代币用于开启与提供者的会话（MOR代币会被锁定，不会被消耗）。
5. 将推理请求发送到`http://localhost:8082/v1/chat/completions`。
6. 会话结束后，您的MOR代币会被返还（扣除少量使用费用）。
7. 将返还的MOR代币重新质押，以持续使用AI服务。

## 获取MOR代币

您需要MOR代币才能进行推理。如果您已经在Base上拥有ETH、USDC或USDT，可以按照以下步骤操作：

```bash
# Swap ETH for MOR
bash skills/everclaw/scripts/swap.sh eth 0.01

# Swap USDC for MOR
bash skills/everclaw/scripts/swap.sh usdc 50
```

或者您也可以在DEX上手动兑换：
- **Uniswap：** [在Base上兑换MOR和ETH](https://app.uniswap.org/explore/tokens/base/0x7431ada8a591c955a994a21710752ef9b882b8e3)
- **Aerodrome：** [在Aerodrome上兑换MOR](https://aerodrome.finance/swap?from=eth&to=0x7431ada8a591c955a994a21710752ef9b882b8e3)

如果您还没有在Base上拥有MOR代币，可以在Coinbase上购买ETH，然后将其转移到Base上，再进行兑换。详细步骤请参阅`references/acquiring-mor.md`。

**需要多少代币？** MOR代币会被锁定，不会被消耗。日常使用大约需要50-100个MOR代币。0.005 ETH足够支付Base平台的Gas费用。

## 架构

```
Agent → proxy-router (localhost:8082) → Morpheus P2P Network → Provider → Model
                ↓
         Base Mainnet (MOR staking, session management)
```

---

## 1. 安装

### 选项A：ClawHub（最简单的方式）

```bash
clawhub install everclaw-inference
```

要更新版本，请运行：`clawhub update everclaw-inference`

⚠️ **请使用`everclaw-inference`，而不是`everclaw`。ClawHub上的`everclaw`仅用于另一个无关的产品。

### 选项B：一键安装工具

这个工具可以完成新的安装、更新操作，并检测与ClawHub的名称冲突：

```bash
# Fresh install
curl -fsSL https://raw.githubusercontent.com/profbernardoj/everclaw/main/scripts/install-everclaw.sh | bash

# Or if you already have the skill:
bash skills/everclaw/scripts/install-everclaw.sh

# Check for updates
bash skills/everclaw/scripts/install-everclaw.sh --check
```

### 选项C：手动克隆Git代码

```bash
git clone https://github.com/profbernardoj/everclaw.git ~/.openclaw/workspace/skills/everclaw
```

要更新版本，请执行：`cd ~/.openclaw/workspace/skills/everclaw && git pull`

## 安装Morpheus路由器

克隆完成后，安装代理路由器：

```bash
bash skills/everclaw/scripts/install.sh
```

此命令会下载适用于您操作系统/架构的最新代理路由器版本，将其解压到`~/morpheus/`目录，并生成初始配置文件。

## 手动安装

1. 访问[Morpheus-Lumerin-Node的发布页面](https://github.com/MorpheusAIs/Morpheus-Lumerin-Node/releases)。
2. 下载适用于您平台的版本（例如`mor-launch-darwin-arm64.zip`）。
3. 将文件解压到`~/morpheus/`目录。
4. 在macOS上运行：`xattr -cr ~/morpheus/`。

## 所需文件

安装完成后，`~/morpheus/`目录应包含以下文件：

| 文件 | 用途 |
|------|---------|
| `proxy-router` | 主要二进制文件 |
| `.env` | 配置文件（包含RPC、合约和端口信息） |
| `models-config.json` | 将区块链模型ID映射到API类型的配置文件 |
| `.cookie` | 自动生成的认证凭据 |

---

## 2. 配置

### `.env`文件

`.env`文件用于配置代理路由器在Base主网上的消费者模式。关键配置项如下：

```bash
# RPC endpoint — MUST be set or router silently fails
ETH_NODE_ADDRESS=https://base-mainnet.public.blastapi.io
ETH_NODE_CHAIN_ID=8453

# Contract addresses (Base mainnet)
DIAMOND_CONTRACT_ADDRESS=0x6aBE1d282f72B474E54527D93b979A4f64d3030a
MOR_TOKEN_ADDRESS=0x7431aDa8a591C955a994a21710752EF9b882b8e3

# Wallet key — leave blank, inject at runtime via 1Password
WALLET_PRIVATE_KEY=

# Proxy settings
PROXY_ADDRESS=0.0.0.0:3333
PROXY_STORAGE_PATH=./data/badger/
PROXY_STORE_CHAT_CONTEXT=true
PROXY_FORWARD_CHAT_CONTEXT=true
MODELS_CONFIG_PATH=./models-config.json

# Web API
WEB_ADDRESS=0.0.0.0:8082
WEB_PUBLIC_URL=http://localhost:8082

# Auth
AUTH_CONFIG_FILE_PATH=./proxy.conf
COOKIE_FILE_PATH=./.cookie

# Logging
LOG_COLOR=true
LOG_LEVEL_APP=info
LOG_FOLDER_PATH=./data/logs
ENVIRONMENT=production
```

⚠️ **必须设置`ETH_NODE_ADDRESS`。**如果不设置，路由器将尝试连接到空字符串，导致所有区块链操作失败。同时，`MODELS_CONFIG_PATH`必须指向`models-config.json`文件。

### models-config.json

⚠️ **此文件是必需的。**如果没有这个文件，聊天功能会显示“api adapter not found”的错误。

```json
{
  "$schema": "./internal/config/models-config-schema.json",
  "models": [
    {
      "modelId": "0xb487ee62516981f533d9164a0a3dcca836b06144506ad47a5c024a7a2a33fc58",
      "modelName": "kimi-k2.5:web",
      "apiType": "openai",
      "apiUrl": ""
    },
    {
      "modelId": "0xbb9e920d94ad3fa2861e1e209d0a969dbe9e1af1cf1ad95c49f76d7b63d32d93",
      "modelName": "kimi-k2.5",
      "apiType": "openai",
      "apiUrl": ""
    }
  ]
}
```

⚠️ **注意格式：** JSON文件使用`"models"`数组，其中包含`"modelId"`、`"modelName"`、`"apiType"`和`"apiUrl"`字段。`apiUrl`字段保持为空——路由器会从区块链中自动解析提供者的端点。请为所有要使用的模型添加相应的条目。详细信息请参阅`references/models.md`。

---

## 3. 启动路由器

### 安全启动（使用1Password）

代理路由器需要您的钱包私钥。**切勿将私钥保存在磁盘上**。请在运行时通过1Password注入私钥：

```bash
bash skills/everclaw/scripts/start.sh
```

或者您也可以手动进行配置：

```bash
cd ~/morpheus
source .env

# Retrieve private key from 1Password (never touches disk)
export WALLET_PRIVATE_KEY=$(
  OP_SERVICE_ACCOUNT_TOKEN=$(security find-generic-password -a "YOUR_KEYCHAIN_ACCOUNT" -s "op-service-account-token" -w) \
  op item get "YOUR_ITEM_NAME" --vault "YOUR_VAULT_NAME" --fields "Private Key" --reveal
)

export ETH_NODE_ADDRESS
nohup ./proxy-router > ./data/logs/router-stdout.log 2>&1 &
```

## 健康检查

等待几秒钟，然后检查路由器的运行状态：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/healthcheck
```

预期响应：HTTP 200。

### 停止路由器

```bash
bash skills/everclaw/scripts/stop.sh
```

或者您可以使用`pkill -f proxy-router`命令停止路由器。

---

## 4. 资金质押

在开启会话之前，需要批准Diamond合约，以便代表您转移MOR代币：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/approve?spender=0x6aBE1d282f72B474E54527D93b979A4f64d3030a&amount=1000000000000000000000"
```

⚠️ `/blockchain/approve`端点使用查询参数，而不是JSON格式的数据。`amount`参数以wei为单位（1000000000000000000 = 1 MOR代币）。请批准较大的金额，以避免频繁重新授权。

## 5. 开启会话

通过模型ID（而非bid ID）来开启会话：

```bash
MODEL_ID="0xb487ee62516981f533d9164a0a3dcca836b06144506ad47a5c024a7a2a33fc58"

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/models/${MODEL_ID}/session" \
  -H "Content-Type: application/json" \
  -d '{"sessionDuration": 3600}'
```

⚠️ **始终使用模型ID端点**，而不是bid ID。使用bid ID会导致“dial tcp: missing address”的错误。

### 会话时长

- 会话时长以秒为单位：3600秒 = 1小时，86400秒 = 1天。
- 需要执行两次区块链交易：一次用于授权转移，一次用于开启会话。
- 会话期间，MOR代币会被锁定。
- 会话结束后，MOR代币会被返还到您的钱包。

### 响应

响应中会包含一个`sessionId`（十六进制字符串）。请保存这个ID，因为它在推理过程中是必需的。

## 使用脚本

```bash
# Open a 1-hour session for kimi-k2.5:web
bash skills/everclaw/scripts/session.sh open kimi-k2.5:web 3600

# List active sessions
bash skills/everclaw/scripts/session.sh list

# Close a session
bash skills/everclaw/scripts/session.sh close 0xSESSION_ID_HERE
```

---

## 6. 发送推理请求

### ⚠️ 重要提示：**请求头信息，而非请求体内容**

`session_id`和`model_id`是HTTP请求头信息，而不是请求体内容。这是最常见的错误之一。

**正确做法：**

```bash
curl -s -u "admin:$COOKIE_PASS" "http://localhost:8082/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "session_id: 0xYOUR_SESSION_ID" \
  -H "model_id: 0xYOUR_MODEL_ID" \
  -d '{
    "model": "kimi-k2.5:web",
    "messages": [{"role": "user", "content": "Hello, world!"}],
    "stream": false
  }'
```

**错误做法（会导致“session not found”错误）：**

```bash
# DON'T DO THIS
curl -s ... -d '{
  "model": "kimi-k2.5:web",
  "session_id": "0x...",   # WRONG — not a body field
  "model_id": "0x...",     # WRONG — not a body field
  "messages": [...]
}'
```

## 使用聊天脚本

```bash
bash skills/everclaw/scripts/chat.sh kimi-k2.5:web "What is the meaning of life?"
```

### 流式传输

在请求体中设置`"stream": true`。响应将以Server-Sent Events (SSE)格式发送。

---

## 7. 关闭会话

关闭会话以释放锁定的MOR代币：

```bash
curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/sessions/0xSESSION_ID/close"
```

或者您也可以使用相应的脚本来关闭会话：

```bash
bash skills/everclaw/scripts/session.sh close 0xSESSION_ID
```

### 注意：**

会话关闭后，锁定的MOR代币会被返还到您的钱包。

---

## 8. 会话管理

### 会话是临时性的

⚠️ **会话在路由器重启后不会被保留**。如果重启代理路由器，您需要重新开启会话。虽然区块链上会保留会话记录，但路由器的内存状态会丢失。

### 监控

```bash
# Check balance (MOR + ETH)
bash skills/everclaw/scripts/balance.sh

# List sessions
bash skills/everclaw/scripts/session.sh list
```

### 会话生命周期

1. **开启会话** → MOR代币被锁定，会话处于活动状态。
2. **活动状态** → 使用`session_id`头发送推理请求。
3. **会话过期** → MOR代币自动返还。
4. **手动关闭会话** → MOR代币立即返还。

### 重启后重新开启会话

重启路由器后，请执行以下操作：

```bash
# Wait for health check
sleep 5

# Re-open sessions for models you need
bash skills/everclaw/scripts/session.sh open kimi-k2.5:web 3600
```

---

## 9. 检查余额

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)

# MOR and ETH balance
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/balance | jq .

# Active sessions
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/sessions | jq .

# Available models
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/models | jq .
```

---

## 10. 故障排除

有关详细的故障排除指南，请参阅`references/troubleshooting.md`。以下是一些常见问题的解决方法：

| 错误 | 解决方法 |
|-------|-----|
| `session not found` | 使用`session_id/model_id`作为HTTP请求头信息，而不是请求体内容。 |
| `dial tcp: missing address` | 使用模型ID开启会话，而不是bid ID。 |
| `api adapter not found` | 确保`models-config.json`文件中包含了所需的模型配置。 |

---

## 11. 关键合约地址（Base主网）

| 合约 | 地址 |
|----------|---------|
| Diamond | `0x6aBE1d282f72B474E54527D93b979A4f64d3030a` |
| MOR Token | `0x7431ada8a591C955a994a21710752ef9b882b8e3` |

## 快速参考

| 动作 | 命令 |
|--------|---------|
| 安装 | `bash skills/everclaw/scripts/install.sh` |
| 启动 | `bash skills/everclaw/scripts/start.sh` |
| 停止 | `bash skills/everclaw/scripts/stop.sh` |
| 将ETH兑换为MOR | `bash skills/everclaw/scripts/swap.sh eth 0.01` |
| 将USDC兑换为MOR | `bash skills/everclaw/scripts/swap.sh usdc 50` |
| 开启会话 | `bash skills/everclaw/scripts/session.sh open <model> [duration>` |
| 关闭会话 | `bash skills/everclaw/scripts/session.sh close <session_id>` |
| 列出会话 | `bash skills/everclaw/scripts/session.sh list` |
| 发送提示 | `bash skills/everclaw/scripts/chat.sh <model> "prompt"` |
| 检查余额 | `bash skills/everclaw/scripts/balance.sh` |
| **诊断** | `bash skills/everclaw/scripts/diagnose.sh` |
| 仅配置诊断 | `bash skills/everclaw/scripts/diagnose.sh --config` |
| 快速诊断 | `bash skills/everclaw/scripts/diagnose.sh --quick` |

---

## 12. 钱包管理（v0.4）

Everclaw v0.4版本包含了一个自包含的钱包管理器，无需依赖任何外部账户。无需使用1Password、Foundry或Safe Wallet，只需macOS的Keychain和Node.js（这些工具已随OpenClaw一起提供）。

### 设置（一个命令）

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs setup
```

此命令会生成一个新的以太坊钱包，并将私钥存储在macOS的Keychain中（私钥在存储时会被加密，并受您的登录密码/Touch ID保护）。

### 导入现有钱包密钥

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs import-key 0xYOUR_PRIVATE_KEY
```

### 检查余额

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs balance
```

此命令会显示ETH、MOR和USDC的余额，以及用于Diamond合约的MOR代币余额。

### 将ETH/USDC兑换为MOR

```bash
# Swap 0.05 ETH for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap eth 0.05

# Swap 50 USDC for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap usdc 50
```

此命令会通过Uniswap V3在Base平台上执行兑换操作。无需任何外部工具，使用的内置工具为viem（已随OpenClaw一起提供）。

### 批准MOR代币用于质押

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs approve
```

此命令会批准使用您的MOR代币进行质押。

### 安全模型

- 私钥存储在macOS的Keychain中（存储时会被加密）。
- 由您的登录密码/Touch ID保护。
- 私钥在运行时注入，使用完毕后会被立即清除。
- 私钥永远不会以明文形式保存在磁盘上。
- 高级用户可以选择使用1Password作为备用方案（向下兼容）。

## 完整命令参考

| 命令 | 描述 |
|---------|-------------|
| `setup` | 生成钱包并存储在Keychain中 |
| `address` | 显示钱包地址 |
| `balance` | 显示ETH、MOR和USDC的余额 |
| `swap eth <amount>` | 通过Uniswap V3将ETH兑换为MOR |
| `swap usdc <amount>` | 通过Uniswap V3将USDC兑换为MOR |
| `approve [amount]` | 批准使用MOR代币进行质押 |
| `export-key` | 打印私钥（请谨慎使用） |
| `import-key <0xkey>` | 导入现有的私钥 |

---

## 13. OpenAI兼容的代理（v0.2）

Morpheus代理路由器需要自定义的认证机制（使用`.cookie`进行Basic认证）和自定义的HTTP请求头信息（`session_id`、`model_id`），这些是标准OpenAI客户端所不支持的。Everclaw提供了一个轻量级的代理来解决这个问题。

### 功能

```
OpenClaw/any client → morpheus-proxy (port 8083) → proxy-router (port 8082) → Morpheus P2P → Provider
```

- 接受标准的OpenAI `/v1/chat/completions`请求。
- 根据需求自动开启区块链会话（无需手动管理会话）。
- 在会话到期前自动续订会话（默认设置为会话到期前1小时）。
- 自动注入Basic认证信息和`session_id`/`model_id`请求头。
- 提供 `/health`、`/v1/models`、`/v1/chat/completions`等接口。

### 安装

```bash
bash skills/everclaw/scripts/install-proxy.sh
```

安装步骤如下：
- 将`morpheus-proxy.mjs`文件安装到`~/morpheus/proxy/`目录。
- 将`gateway-guardian.sh`文件安装到`~/.openclaw/workspace/scripts/`目录。
- 在macOS系统中，这些文件会通过launchd服务在系统启动时自动运行。

### 配置

以下环境变量是可选的，默认值均为合理设置：

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| MORPHEUS_PROXY_PORT` | `8083` | 代理路由器监听的端口 |
| MORPHEUS_ROUTER_URL` | `http://localhost:8082` | 代理路由器的URL |
| MORPHEUS COOKIE_PATH` | `~/morpheus/.cookie` | 认证cookie的存储路径 |
| MORPHEUS_SESSION_duration` | `604800`秒 | 会话持续时间 |
| MORPHEUS_RENEW_BEFORE` | `3600`秒 | 会话续订间隔（默认为1小时） |
| MORPHEUS_PROXY_API_KEY` | `morpheus-local` | 用于代理认证的bearer token |

### 会话时长

会话期间，MOR代币会被锁定。会话持续时间越长，锁定的MOR代币越多，但区块链交易次数相应减少：

| 会话时长 | 锁定的MOR代币数量 | 交易次数 |
|----------|--------------------:|:-------------|
| 1小时 | ~11个MOR代币 | 每小时大约1次交易 |
| 1天 | ~274个MOR代币 | 每天大约2次交易 |
| 7天 | ~1,915个MOR代币 | 每周大约2次交易 |

会话结束后或过期时，MOR代币会被返还给您的钱包。

### 健康检查

```bash
curl http://127.0.0.1:8083/health
```

---

## 14. 可用的模型

```bash
curl http://127.0.0.1:8083/v1/models
```

---

## 15. 直接使用（无需OpenClaw）

```bash
curl http://127.0.0.1:8083/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer morpheus-local" \
  -d '{
    "model": "kimi-k2.5",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'
```

---

## 可靠性说明

- `kimi-k2.5`（非Web版本）是最可靠的模型，建议作为首选备用模型。
- `kimi-k2.5:web`（Web搜索版本）在P2P路由过程中容易超时，不建议作为备用模型使用。
- 提供者连接可能会偶尔中断，但通常可以重试成功。
- 代理本身作为一个KeepAlive服务运行，如果崩溃会自动重启。

## 16. 代理的弹性（v0.5）

v0.5版本对代理进行了三项关键改进，以防止由于**冷却机制连锁反应**导致长时间中断：

#### 问题：冷却机制连锁反应

当主要提供者（例如venice）返回错误时，OpenClaw的故障转移机制会将该提供者标记为“处于冷却状态”。如果Morpheus代理也返回错误（OpenClaw将其误判为计费错误），**两个提供者都会进入冷却状态**，导致代理完全离线（有时会持续6小时以上）。

#### 解决方案1：OpenAI兼容的错误分类

现在代理返回的错误信息采用OpenAI规定的格式，包含`type`和`code`字段：

```json
{
  "error": {
    "message": "Morpheus session unavailable: ...",
    "type": "server_error",
    "code": "morpheus_session_error",
    "param": null
  }
}
```

**关键区别：** 所有Morpheus相关的错误都会被标记为“server_error”，而不会被标记为“billing”或“rate_limit_error”。这样OpenClaw就能正确处理这些错误，避免不必要的长时间中断。

代理返回的错误代码如下：

| 代码 | 含义 |
|------|---------|
| `morpheus_session_error` | 无法打开或刷新区块链会话 |
| `morpheus_inference_error` | 提供者在推理过程中返回错误 |
| `morpheus_upstream_error` | 与代理路由器的连接失败 |
| `timeout` | 推理请求超时 |
| `model_not_found` | 请求的模型在`models-config.json`文件中不存在 |

#### 解决方案2：自动重试会话

当代理路由器返回与会话相关的错误时（例如会话过期、无效或未找到模型），代理会：

1. **使缓存的会话失效**。
2. **自动开启一个新的区块链会话**。
3. **重新尝试推理请求**。

这样可以处理代理路由器重启后丢失内存中的会话状态，或者长时间运行的会话中断的情况。

## 17. 配置OpenClaw以使用Morpheus作为备用提供者（v0.2）

配置OpenClaw，使其在主要API的信用耗尽时使用Morpheus作为备用提供者。

### 步骤1：添加Morpheus提供者

通过配置文件或手动编辑`openclaw.json`来添加Morpheus提供者：

```json5
{
  "models": {
    "providers": {
      "morpheus": {
        "baseUrl": "http://127.0.0.1:8083/v1",
        "apiKey": "morpheus-local",
        "api": "openai-completions",
        "models": [
          {
            "id": "kimi-k2.5",
            "name": "Kimi K2.5 (via Morpheus)",
            "reasoning": true,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          },
          {
            "id": "kimi-k2-thinking",
            "name": "Kimi K2 Thinking (via Morpheus)",
            "reasoning": true,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          },
          {
            "id": "glm-4.7-flash",
            "name": "GLM 4.7 Flash (via Morpheus)",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

### 步骤2：设置备用提供者

建议使用多级备用提供者（从v0.5版本开始）：

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "venice/claude-opus-4-6",
        "fallbacks": [
          "venice/claude-opus-45",   // Different model, same provider
          "venice/kimi-k2-5",        // Open-source model, same provider
          "morpheus/kimi-k2.5"       // Decentralized fallback
        ]
      },
      "models": {
        "venice/claude-opus-45": { "alias": "Claude Opus 4.5" },
        "venice/kimi-k2-5": { "alias": "Kimi K2.5" },
        "morpheus/kimi-k2.5": { "alias": "Kimi K2.5 (Morpheus)" },
        "morpheus/kimi-k2-thinking": { "alias": "Kimi K2 Thinking (Morpheus)" },
        "morpheus/glm-4.7-flash": { "alias": "GLM 4.7 Flash (Morpheus)" }
      }
    }
  }
}
```

#### 为什么需要多级备用提供者？

**原因：** 单一备用提供者会导致单点故障。如果主要提供者和备用提供者同时进入冷却状态（例如，都遇到计费错误），代理就会离线。通过使用多个备用提供者，可以确保至少有一个路径可用。

### 步骤3：配置认证配置文件

OpenClaw支持为每个提供者配置多个API密钥，并自动轮换使用这些密钥：

```json
{
  "venice:default": {
    "type": "api_key",
    "provider": "venice",
    "key": "VENICE-INFERENCE-KEY-YOUR_KEY_HERE"
  },
  "morpheus:default": {
    "type": "api_key",
    "provider": "morpheus",
    "key": "morpheus-local"
  }
}
```

#### 单个密钥的配置（最低要求，v0.9.1版本）

将配置文件添加到`~/.openclaw/agents/main/agent/auth-profiles.json`中：

```json
{
  "venice:default": {
    "type": "api_key",
    "provider": "venice",
    "key": "VENICE-INFERENCE-KEY-YOUR_KEY_HERE"
  },
  "morpheus:default": {
    "type": "api_key",
    "provider": "morpheus",
    "key": "morpheus-local"
  }
}
```

#### 多个密钥的配置（推荐，v0.9.1版本）

如果您有多个Venice API密钥（例如来自不同的账户或计划），请将它们全部添加到配置文件中，并按照信用额度从高到低的顺序排列：

**auth-profiles.json**文件的内容如下：

```json
{
  "version": 1,
  "profiles": {
    "venice:key1": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_PRIMARY_KEY"
    },
    "venice:key2": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_SECOND_KEY"
    },
    "venice:key3": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_THIRD_KEY"
    },
    "morpheus:default": {
      "type": "api_key",
      "provider": "morpheus",
      "key": "morpheus-local"
    }
  }
}
```

**openclaw.json**文件用于注册这些配置文件，并指定轮换顺序：

```json5
{
  "auth": {
    "profiles": {
      "venice:key1": { "provider": "venice", "mode": "api_key" },
      "venice:key2": { "provider": "venice", "mode": "api_key" },
      "venice:key3": { "provider": "venice", "mode": "api_key" },
      "morpheus:default": { "provider": "morpheus", "mode": "api_key" }
    },
    "order": {
      "venice": ["venice:key1", "venice:key2", "venice:key3"]
    }
  }
}
```

#### `auth.order`参数的作用

`auth.order`参数非常重要。如果不设置，OpenClaw会使用轮询机制（按使用顺序依次尝试密钥），这可能导致信用分配不均衡。通过设置明确的顺序，可以确保按照预期的顺序使用密钥。

#### 多密钥轮换的原理

OpenClaw的认证机制会自动处理密钥的轮换：

1. **会话粘性**：每个会话都会使用固定的密钥，以确保会话的连续性。
2. **计费限制**：如果某个密钥返回计费错误，该密钥会被禁用，并在一段时间后重新尝试使用其他密钥。
3. **失败后的恢复**：禁用某个密钥后，OpenClaw会立即尝试使用下一个密钥。

---

## 18. 检查余额

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)

# MOR and ETH balance
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/balance | jq .

# Active sessions
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/sessions | jq .

# Available models
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/models | jq .
```

---

## 19. 故障排除

有关详细的故障排除指南，请参阅`references/troubleshooting.md`。以下是一些常见的错误及其解决方法：

| 错误 | 解决方法 |
|-------|-----|
| `session not found` | 使用`session_id/model_id`作为HTTP请求头信息，而不是请求体内容。 |
| `dial tcp: missing address` | 使用模型ID开启会话，而不是bid ID。 |
| `api adapter not found` | 确保`models-config.json`文件中包含了所需的模型配置。 |
| `ERC20: transfer amount exceeds balance` | 关闭旧的会话以释放锁定的MOR代币。 |
| 重启后会话丢失 | 这是正常现象，重启后可以重新开启会话。 |
| MorpheusUI与代理冲突 | 不要同时运行MorpheusUI和无界代理（agentless proxy）。 |

---

## 关键合约地址（Base主网）

| 合约 | 地址 |
|----------|---------|
| Diamond | `0x6aBE1d282f72B474E54527D93b979A4f64d3030a` |
| MOR Token | `0x7431aDa8a591C955a994a21710752ef9b882b8e3` |

## 快速参考

| 动作 | 命令 |
|--------|---------|
| 安装 | `bash skills/everclaw/scripts/install.sh` |
| 启动 | `bash skills/everclaw/scripts/start.sh` |
| 停止 | `bash skills/everclaw/scripts/stop.sh` |
| 将ETH兑换为MOR | `bash skills/everclaw/scripts/swap.sh eth 0.01` |
| 将USDC兑换为MOR | `bash skills/everclaw/scripts/swap.sh usdc 50` |
| 开启会话 | `bash skills/everclaw/scripts/session.sh open <model> [duration>` |
| 关闭会话 | `bash skills/everclaw/scripts/session.sh close <session_id>` |
| 列出会话 | `bash skills/everclaw/scripts/session.sh list` |
| 发送提示 | `bash skills/everclaw/scripts/chat.sh <model> "prompt"` |
| 检查余额 | `bash skills/everclaw/scripts/balance.sh` |
| **诊断** | `bash skills/everclaw/scripts/diagnose.sh` |
| 仅配置诊断 | `bash skills/everclaw/scripts/diagnose.sh --config` |
| 快速诊断 | `bash skills/everclaw/scripts/diagnose.sh --quick` |

---

## 20. 钱包管理（v0.4）

Everclaw v0.4版本包含了一个自包含的钱包管理器，无需依赖任何外部账户。无需使用1Password、Foundry或Safe Wallet，只需macOS的Keychain和Node.js（这些工具已随OpenClaw一起提供）。

### 设置（一个命令）

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs setup
```

此命令会生成一个新的以太坊钱包，并将私钥存储在macOS的Keychain中（私钥在存储时会被加密，并受您的登录密码/Touch ID保护）。

### 导入现有钱包密钥

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs import-key 0xYOUR_PRIVATE_KEY
```

### 检查余额

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs balance
```

此命令会显示ETH、MOR和USDC的余额，以及用于Diamond合约的MOR代币余额。

### 将ETH/USDC兑换为MOR

```bash
# Swap 0.05 ETH for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap eth 0.05

# Swap 50 USDC for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap usdc 50
```

此命令会通过Uniswap V3在Base平台上执行兑换操作。无需任何外部工具，使用的内置工具为viem（已随OpenClaw一起提供）。

### 批准使用MOR代币进行质押

___CODE_BLOCK_27***

此命令会批准使用您的MOR代币进行质押。

### 安全性

- 私钥存储在macOS的Keychain中（存储时会被加密）。
- 由您的登录密码/Touch ID保护。
- 私钥在运行时注入，使用完毕后会被立即清除。
- 私钥永远不会以明文形式保存在磁盘上。
- 高级用户可以选择使用1Password作为备用方案（向下兼容）。

## 完整命令参考

| 命令 | 描述 |
|---------|-------------|
| `setup` | 生成钱包并存储在Keychain中 |
| `address` | 显示钱包地址 |
| `balance` | 显示ETH、MOR和USDC的余额 |
| `swap eth <amount>` | 通过Uniswap V3将ETH兑换为MOR |
| `swap usdc <amount>` | 通过Uniswap V3将USDC兑换为MOR |
| `approve [amount]` | 批准使用MOR代币进行质押 |
| `export-key` | 打印私钥（请谨慎使用） |
| `import-key <0xkey>` | 导入现有的私钥 |

---

## 21. OpenAI兼容的代理（v0.2）

Morpheus代理路由器需要自定义的认证机制（使用`.cookie`进行Basic认证）和自定义的HTTP请求头信息（`session_id`、`model_id`），这些是标准OpenAI客户端所不支持的。Everclaw提供了一个轻量级的代理来解决这个问题。

### 功能

```
OpenClaw/any client → morpheus-proxy (port 8083) → proxy-router (port 8082) → Morpheus P2P → Provider
```

- 接受标准的OpenAI `/v1/chat/completions`请求。
- 根据需求自动开启区块链会话（无需手动管理会话）。
- 在会话到期前自动续订会话（默认为会话到期前1小时）。
- 自动注入Basic认证信息和`session_id`/`model_id`请求头。
- 提供 `/health`、`/v1/models`、`/v1/chat/completions`等接口。

### 安装

```bash
bash skills/everclaw/scripts/install-proxy.sh
```

安装步骤如下：
- 将`morpheus-proxy.mjs`文件安装到`~/morpheus/proxy/`目录。
- 将`gateway-guardian.sh`文件安装到`~/.openclaw/workspace/scripts/`目录。
- 在macOS系统中，这些文件会通过launchd服务在系统启动时自动运行。

### 配置

以下环境变量是可选的，默认值均为合理设置：

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| MORPHEUS_PROXY_PORT` | `8083` | 代理路由器监听的端口 |
| MORPHEUS_ROUTER_URL` | `http://localhost:8082` | 代理路由器的URL |
| MORPHEUS COOKIE_PATH` | `~/morpheus/.cookie` | 认证cookie的存储路径 |
| MORPHEUS_SESSION_duration` | `604800`秒 | 会话持续时间 |
| MORPHEUS_RENEW_BEFORE` | `3600`秒 | 会话续订间隔（默认为1小时） |
| MORPHEUS_PROXY_API_KEY` | `morpheus-local` | 用于代理认证的bearer token |

### 会话时长

会话期间，MOR代币会被锁定。会话持续时间越长，锁定的MOR代币越多，但区块链交易次数相应减少：

| 会话时长 | 锁定的MOR代币数量 | 交易次数 |
|----------|--------------------:|:-------------|
| 1小时 | ~11个MOR代币 | 每小时大约1次交易 |
| 1天 | ~274个MOR代币 | 每天大约2次交易 |
| 7天 | ~1,915个MOR代币 | 每周大约2次交易 |

会话结束后或过期时，MOR代币会被返还给您的钱包。

### 健康检查

```bash
curl http://127.0.0.1:8083/health
```

---

## 22. 可用的模型

```bash
curl http://127.0.0.1:8083/v1/models
```

---

## 23. 直接使用（无需OpenClaw）

```bash
curl http://127.0.0.1:8083/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer morpheus-local" \
  -d '{
    "model": "kimi-k2.5",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'
```

---

## 可靠性说明

- `kimi-k2.5`（非Web版本）是最可靠的模型，建议作为首选备用模型。
- `kimi-k2.5:web`（Web搜索版本）在P2P路由过程中容易超时，不建议作为备用模型使用。
- 提供者连接可能会偶尔中断，但通常可以重试成功。
- 代理本身作为一个KeepAlive服务运行，如果崩溃会自动重启。

## 24. 代理的弹性（v0.5）

v0.5版本对代理进行了三项关键改进，以防止由于**冷却机制连锁反应**导致长时间中断：

#### 问题：冷却机制连锁反应

当主要提供者（例如venice）返回错误时，OpenClaw的故障转移机制会将该提供者标记为“处于冷却状态”。如果Morpheus代理也返回错误（OpenClaw将其误判为计费错误），**两个提供者都会进入冷却状态**，导致代理完全离线（有时会持续6小时以上）。

#### 解决方案1：OpenAI兼容的错误分类

现在代理返回的错误信息采用OpenAI规定的格式，包含`type`和`code`字段：

```json
{
  "error": {
    "message": "Morpheus session unavailable: ...",
    "type": "server_error",
    "code": "morpheus_session_error",
    "param": null
  }
}
```

**关键区别：** 所有Morpheus相关的错误都会被标记为“server_error”，而不会被标记为“billing”或“rate_limit_error”。这样OpenClaw就能正确处理这些错误，避免不必要的长时间中断。

代理返回的错误代码如下：

| 代码 | 含义 |
|------|---------|
| `morpheus_session_error` | 无法打开或刷新区块链会话 |
| `morpheus_inference_error` | 提供者在推理过程中返回错误 |
| `morpheus_upstream_error` | 与代理路由器的连接失败 |
| `timeout` | 推理请求超时 |
| `model_not_found` | 请求的模型在`models-config.json`文件中不存在 |

#### 解决方案2：自动重试会话

当代理路由器返回与会话相关的错误（例如会话过期、无效或未找到模型）时，代理会：

1. **使缓存的会话失效**。
2. **自动开启一个新的区块链会话**。
3. **重新尝试推理请求**。

这样可以处理代理路由器重启后丢失内存中的会话状态，或者长时间运行的会话中断的情况。

## 25. 配置OpenClaw以使用Morpheus作为备用提供者（v0.2）

配置OpenClaw，使其在主要API的信用耗尽时使用Morpheus作为备用提供者。

### 步骤1：在`openclaw.json`中添加Morpheus提供者

通过配置文件或手动编辑`openclaw.json`来添加Morpheus提供者：

```json5
{
  "models": {
    "providers": {
      "morpheus": {
        "baseUrl": "http://127.0.0.1:8083/v1",
        "apiKey": "morpheus-local",
        "api": "openai-completions",
        "models": [
          {
            "id": "kimi-k2.5",
            "name": "Kimi K2.5 (via Morpheus)",
            "reasoning": true,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          },
          {
            "id": "kimi-k2-thinking",
            "name": "Kimi K2 Thinking (via Morpheus)",
            "reasoning": true,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          },
          {
            "id": "glm-4.7-flash",
            "name": "GLM 4.7 Flash (via Morpheus)",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

### 步骤2：设置备用提供者

建议使用多级备用提供者（从v0.5版本开始）：

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "venice/claude-opus-4-6",
        "fallbacks": [
          "venice/claude-opus-45",   // Different model, same provider
          "venice/kimi-k2-5",        // Open-source model, same provider
          "morpheus/kimi-k2.5"       // Decentralized fallback
        ]
      },
      "models": {
        "venice/claude-opus-45": { "alias": "Claude Opus 4.5" },
        "venice/kimi-k2-5": { "alias": "Kimi K2.5" },
        "morpheus/kimi-k2.5": { "alias": "Kimi K2.5 (Morpheus)" },
        "morpheus/kimi-k2-thinking": { "alias": "Kimi K2 Thinking (Morpheus)" },
        "morpheus/glm-4.7-flash": { "alias": "GLM 4.7 Flash (Morpheus)" }
      }
    }
  }
}
```

#### 为什么需要多级备用提供者？

**原因：** 单一备用提供者会导致单点故障。如果主要提供者和备用提供者同时进入冷却状态（例如，都遇到计费错误），代理就会离线。通过使用多个备用提供者，可以确保至少有一个路径可用。

### 步骤3：配置认证配置文件

OpenClaw支持为每个提供者配置多个API密钥，并自动轮换使用这些密钥：

```json
{
  "venice:default": {
    "type": "api_key",
    "provider": "venice",
    "key": "VENICE-INFERENCE-KEY-YOUR_KEY_HERE"
  },
  "morpheus:default": {
    "type": "api_key",
    "provider": "morpheus",
    "key": "morpheus-local"
  }
}
```

#### 单个密钥的配置（最低要求，v0.9.1版本）

将配置文件添加到`~/.openclaw/agents/main/agent/auth-profiles.json`中：

```json
{
  "venice:default": {
    "type": "api_key",
    "provider": "venice",
    "key": "VENICE-INFERENCE-KEY-YOUR_KEY_HERE"
  },
  "morpheus:default": {
    "type": "api_key",
    "provider": "morpheus",
    "key": "morpheus-local"
  }
}
```

#### 多个密钥的配置（推荐，v0.9.1版本）

如果您有多个Venice API密钥（例如来自不同的账户或计划），请将它们全部添加到配置文件中，并按照信用额度从高到低的顺序排列：

**auth-profiles.json`文件的内容如下：

```json
{
  "version": 1,
  "profiles": {
    "venice:key1": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_PRIMARY_KEY"
    },
    "venice:key2": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_SECOND_KEY"
    },
    "venice:key3": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_THIRD_KEY"
    },
    "morpheus:default": {
      "type": "api_key",
      "provider": "morpheus",
      "key": "morpheus-local"
    }
  }
}
```

**openclaw.json`文件用于注册这些配置文件，并指定轮换顺序：

```json5
{
  "auth": {
    "profiles": {
      "venice:key1": { "provider": "venice", "mode": "api_key" },
      "venice:key2": { "provider": "venice", "mode": "api_key" },
      "venice:key3": { "provider": "venice", "mode": "api_key" },
      "morpheus:default": { "provider": "morpheus", "mode": "api_key" }
    },
    "order": {
      "venice": ["venice:key1", "venice:key2", "venice:key3"]
    }
  }
}
```

#### `auth.order`参数的作用

`auth.order`参数非常重要。如果不设置，OpenClaw会使用轮询机制（按使用顺序依次尝试密钥），这可能导致信用分配不均衡。通过设置明确的顺序，可以确保按照预期的顺序使用密钥。

#### 多密钥轮换的原理

OpenClaw的认证机制会自动处理密钥的轮换：

1. **会话粘性**：每个会话都会使用固定的密钥，以确保会话的连续性。
2. **计费限制**：如果某个密钥返回计费错误，该密钥会被禁用，并在一段时间后重新尝试使用其他密钥。
3. **失败后的恢复**：禁用某个密钥后，OpenClaw会立即尝试使用下一个密钥。

---

## 26. 检查余额

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)

# MOR and ETH balance
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/balance | jq .

# Active sessions
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/sessions | jq .

# Available models
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/models | jq .
```

---

## 27. 故障排除

有关详细的故障排除指南，请参阅`references/troubleshooting.md`。以下是一些常见的错误及其解决方法：

| 错误 | 解决方法 |
|-------|-----|
| `session not found` | 使用`session_id/model_id`作为HTTP请求头信息，而不是请求体内容。 |
| `dial tcp: missing address` | 使用模型ID开启会话，而不是bid ID。 |
| `api adapter not found` | 确保`models-config.json`文件中包含了所需的模型配置。 |
| `ERC20: transfer amount exceeds balance` | 关闭旧的会话以释放锁定的MOR代币。 |
| 重启后会话丢失 | 这是正常现象，重启后可以重新开启会话。 |
| MorpheusUI与代理冲突 | 不要同时运行MorpheusUI和无界代理（agentless proxy）。 |

---

## 28. 关键合约地址（Base主网）

| 合约 | 地址 |
|----------|---------|
| Diamond | `0x6aBE1d282f72B474E54527D93b979A4f64d3030a` |
| MOR Token | `0x7431aDa8a591C955a994a21710752ef9b882b8e3` |

## 快速参考

| 动作 | 命令 |
|--------|---------|
| 安装 | `bash skills/everclaw/scripts/install.sh` |
| 启动 | `bash skills/everclaw/scripts/start.sh` |
| 停止 | `bash skills/everclaw/scripts/stop.sh` |
| 将ETH兑换为MOR | `bash skills/everclaw/scripts/swap.sh eth 0.01` |
| 将USDC兑换为MOR | `bash skills/everclaw/scripts/swap.sh usdc 50` |
| 开启会话 | `bash skills/everclaw/scripts/session.sh open <model> [duration>` |
| 关闭会话 | `bash skills/everclaw/scripts/session.sh close <session_id>` |
| 列出会话 | `bash skills/everclaw/scripts/session.sh list` |
| 发送提示 | `bash skills/everclaw/scripts/chat.sh <model> "prompt"` |
| 检查余额 | `bash skills/everclaw/scripts/balance.sh` |
| **诊断** | `bash skills/everclaw/scripts/diagnose.sh` |
| 仅配置诊断 | `bash skills/everclaw/scripts/diagnose.sh --config` |
| 快速诊断 | `bash skills/everclaw/scripts/diagnose.sh --quick` |

---

## 29. 钱包管理（v0.4）

Everclaw v0.4版本包含了一个自包含的钱包管理器，无需依赖任何外部账户。无需使用1Password、Foundry或Safe Wallet，只需macOS的Keychain和Node.js（这些工具已随OpenClaw一起提供）。

### 设置（一个命令）

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs setup
```

此命令会生成一个新的以太坊钱包，并将私钥存储在macOS的Keychain中（私钥在存储时会被加密，并受您的登录密码/Touch ID保护）。

### 导入现有钱包密钥

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs import-key 0xYOUR_PRIVATE_KEY
```

### 检查余额

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs balance
```

此命令会显示ETH、MOR和USDC的余额，以及用于Diamond合约的MOR代币余额。

### 将ETH/USDC兑换为MOR

```bash
# Swap 0.05 ETH for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap eth 0.05

# Swap 50 USDC for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap usdc 50
```

此命令会通过Uniswap V3在Base平台上执行兑换操作。无需任何外部工具，使用的内置工具为viem（已随OpenClaw一起提供）。

### 批准使用MOR代币进行质押

___CODE_BLOCK_27***

此命令会批准使用您的MOR代币进行质押。

### 安全性

- 私钥存储在macOS的Keychain中（存储时会被加密）。
- 由您的登录密码/Touch ID保护。
- 私钥在运行时注入，使用完毕后会被立即清除。
- 私钥永远不会以明文形式保存在磁盘上。
- 高级用户可以选择使用1Password作为备用方案（向下兼容）。

## 完整命令参考

| 命令 | 描述 |
|---------|-------------|
| `setup` | 生成钱包并存储在Keychain中 |
| `address` | 显示钱包地址 |
| `balance` | 显示ETH、MOR和USDC的余额 |
| `swap eth <amount>` | 通过Uniswap V3将ETH兑换为MOR |
| `swap usdc <amount>` | 通过Uniswap V3将USDC兑换为MOR |
| `approve [amount]` | 批准使用MOR代币进行质押 |
| `export-key` | 打印私钥（请谨慎使用） |
| `import-key <0xkey>` | 导入现有的私钥 |

---

## 30. OpenAI兼容的代理（v0.2）

Morpheus代理路由器需要自定义的认证机制（使用`.cookie`进行Basic认证）和自定义的HTTP请求头信息（`session_id`、`model_id`），这些是标准OpenAI客户端所不支持的。Everclaw提供了一个轻量级的代理来解决这个问题。

### 功能

```
OpenClaw/any client → morpheus-proxy (port 8083) → proxy-router (port 8082) → Morpheus P2P → Provider
```

- 接受标准的OpenAI `/v1/chat/completions`请求。
- 根据需求自动开启区块链会话（无需手动管理会话）。
- 在会话到期前自动续订会话（默认为会话到期前1小时）。
- 自动注入Basic认证信息和`session_id`/`model_id`请求头。
- 提供 `/health`、`/v1/models`、`/v1/chat/completions`等接口。

### 安装

```bash
bash skills/everclaw/scripts/install-proxy.sh
```

安装步骤如下：
- 将`morpheus-proxy.mjs`文件安装到`~/morpheus/proxy/`目录。
- 将`gateway-guardian.sh`文件安装到`~/.openclaw/workspace/scripts/`目录。
- 在macOS系统中，这些文件会通过launchd服务在系统启动时自动运行。

### 配置

以下环境变量是可选的，默认值均为合理设置：

| 变量 | 默认值 | 描述 |
|----------|---------|-------------|
| MORPHEUS_PROXY_PORT` | `8083` | 代理路由器监听的端口 |
| MORPHEUS_ROUTER_URL` | `http://localhost:8082` | 代理路由器的URL |
| MORPHEUS COOKIE_PATH` | `~/morpheus/.cookie` | 认证cookie的存储路径 |
| MORPHEUS_SESSION_duration` | `604800`秒 | 会话持续时间 |
| MORPHEUS_RENEW_BEFORE` | `3600`秒 | 会话续订间隔（默认为1小时） |
| MORPHEUS_PROXY_API_KEY` | `morpheus-local` | 用于代理认证的bearer token |

### 会话时长

会话期间，MOR代币会被锁定。会话持续时间越长，锁定的MOR代币越多，但区块链交易次数相应减少：

| 会话时长 | 锁定的MOR代币数量 | 交易次数 |
|----------|--------------------:|:-------------|
| 1小时 | ~11个MOR代币 | 每小时大约1次交易 |
| 1天 | ~274个MOR代币 | 每天大约2次交易 |
| 7天 | ~1,915个MOR代币 | 每周大约2次交易 |

会话结束后或过期时，MOR代币会被返还给您的钱包。

### 健康检查

```bash
curl http://127.0.0.1:8083/health
```

---

## 31. 可用的模型

```bash
curl http://127.0.0.1:8083/v1/models
```

---

## 32. 直接使用（无需OpenClaw）

```bash
curl http://127.0.0.1:8083/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer morpheus-local" \
  -d '{
    "model": "kimi-k2.5",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'
```

---

## 可靠性说明

- `kimi-k2.5`（非Web版本）是最可靠的模型，建议作为首选备用模型。
- `kimi-k2.5:web`（Web搜索版本）在P2P路由过程中容易超时，不建议作为备用模型使用。
- 提供者连接可能会偶尔中断，但通常可以重试成功。
- 代理本身作为一个KeepAlive服务运行，如果崩溃会自动重启。

## 33. 代理的弹性（v0.5）

v0.5版本对代理进行了三项关键改进，以防止由于**冷却机制连锁反应**导致长时间中断：

#### 问题：冷却机制连锁反应

当主要提供者（例如venice）返回错误时，OpenClaw的故障转移机制会将该提供者标记为“处于冷却状态”。如果Morpheus代理也返回错误（OpenClaw将其误判为计费错误），**两个提供者都会进入冷却状态**，导致代理完全离线（有时会持续6小时以上）。

#### 解决方案1：OpenAI兼容的错误分类

现在代理返回的错误信息采用OpenAI规定的格式，包含`type`和`code`字段：

```json
{
  "error": {
    "message": "Morpheus session unavailable: ...",
    "type": "server_error",
    "code": "morpheus_session_error",
    "param": null
  }
}
```

**关键区别：** 所有Morpheus相关的错误都会被标记为“server_error”，而不会被标记为“billing”或“rate_limit_error”。这样OpenClaw就能正确处理这些错误，避免不必要的长时间中断。

代理返回的错误代码如下：

| 代码 | 含义 |
|------|---------|
| `morpheus_session_error` | 无法打开或刷新区块链会话 |
| `morpheus_inference_error` | 提供者在推理过程中返回错误 |
| `morpheus_upstream_error` | 与代理路由器的连接失败 |
| `timeout` | 推理请求超时 |
| `model_not_found` | 请求的模型在`models-config.json`文件中不存在 |

#### 解决方案2：自动重试会话

当代理路由器返回与会话相关的错误（例如会话过期、无效或未找到模型）时，代理会：

1. **使缓存的会话失效**。
2. **自动开启一个新的区块链会话**。
3. **重新尝试推理请求**。

这样可以处理代理路由器重启后丢失内存中的会话状态，或者长时间运行的会话中断的情况。

## 34. 配置OpenClaw以使用Morpheus作为备用提供者（v0.2）

配置OpenClaw，使其在主要API的信用耗尽时使用Morpheus作为备用提供者。

### 步骤1：通过配置文件或手动编辑`openclaw.json`来添加Morpheus提供者

```json5
{
  "models": {
    "providers": {
      "morpheus": {
        "baseUrl": "http://127.0.0.1:8083/v1",
        "apiKey": "morpheus-local",
        "api": "openai-completions",
        "models": [
          {
            "id": "kimi-k2.5",
            "name": "Kimi K2.5 (via Morpheus)",
            "reasoning": true,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          },
          {
            "id": "kimi-k2-thinking",
            "name": "Kimi K2 Thinking (via Morpheus)",
            "reasoning": true,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          },
          {
            "id": "glm-4.7-flash",
            "name": "GLM 4.7 Flash (via Morpheus)",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

### 步骤2：设置备用提供者

建议使用多级备用提供者（从v0.5版本开始）：

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "venice/claude-opus-4-6",
        "fallbacks": [
          "venice/claude-opus-45",   // Different model, same provider
          "venice/kimi-k2-5",        // Open-source model, same provider
          "morpheus/kimi-k2.5"       // Decentralized fallback
        ]
      },
      "models": {
        "venice/claude-opus-45": { "alias": "Claude Opus 4.5" },
        "venice/kimi-k2-5": { "alias": "Kimi K2.5" },
        "morpheus/kimi-k2.5": { "alias": "Kimi K2.5 (Morpheus)" },
        "morpheus/kimi-k2-thinking": { "alias": "Kimi K2 Thinking (Morpheus)" },
        "morpheus/glm-4.7-flash": { "alias": "GLM 4.7 Flash (Morpheus)" }
      }
    }
  }
}
```

#### 为什么需要多级备用提供者？

**原因：** 单一备用提供者会导致单点故障。如果主要提供者和备用提供者同时进入冷却状态（例如，都遇到计费错误），代理就会离线。通过使用多个备用提供者，可以确保至少有一个路径可用。

### 步骤3：配置认证配置文件

OpenClaw支持为每个提供者配置多个API密钥，并自动轮换使用这些密钥：

```json
{
  "venice:default": {
    "type": "api_key",
    "provider": "venice",
    "key": "VENICE-INFERENCE-KEY-YOUR_KEY_HERE"
  },
  "morpheus:default": {
    "type": "api_key",
    "provider": "morpheus",
    "key": "morpheus-local"
  }
}
```

#### 单个密钥的配置（最低要求，v0.9.1版本）

将配置文件添加到`~/.openclaw/agents/main/agent/auth-profiles.json`中：

```json
{
  "venice:default": {
    "type": "api_key",
    "provider": "venice",
    "key": "VENICE-INFERENCE-KEY-YOUR_KEY_HERE"
  },
  "morpheus:default": {
    "type": "api_key",
    "provider": "morpheus",
    "key": "morpheus-local"
  }
}
```

#### 多个密钥的配置（推荐，v0.9.1版本）

如果您有多个Venice API密钥（例如来自不同的账户或计划），请将它们全部添加到配置文件中，并按照信用额度从高到低的顺序排列：

**auth-profiles.json`文件的内容如下：

```json
{
  "version": 1,
  "profiles": {
    "venice:key1": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_PRIMARY_KEY"
    },
    "venice:key2": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_SECOND_KEY"
    },
    "venice:key3": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_THIRD_KEY"
    },
    "morpheus:default": {
      "type": "api_key",
      "provider": "morpheus",
      "key": "morpheus-local"
    }
  }
}
```

**openclaw.json`文件用于注册这些配置文件，并指定轮换顺序：

```json5
{
  "auth": {
    "profiles": {
      "venice:key1": { "provider": "venice", "mode": "api_key" },
      "venice:key2": { "provider": "venice", "mode": "api_key" },
      "venice:key3": { "provider": "venice", "mode": "api_key" },
      "morpheus:default": { "provider": "morpheus", "mode": "api_key" }
    },
    "order": {
      "venice": ["venice:key1", "venice:key2", "venice:key3"]
    }
  }
}
```

#### `auth.order`参数的作用

`auth.order`参数非常重要。如果不设置，OpenClaw会使用轮询机制（按使用顺序依次尝试密钥），这可能导致信用分配不均衡。通过设置明确的顺序，可以确保按照预期的顺序使用密钥。

#### 多密钥轮换的原理

OpenClaw的认证机制会自动处理密钥的轮换：

1. **会话粘性**：每个会话都会使用固定的密钥，以确保会话的连续性。
2. **计费限制**：如果某个密钥返回计费错误，该密钥会被禁用，并在一段时间后重新尝试使用其他密钥。
3. **失败后的恢复**：禁用某个密钥后，OpenClaw会立即尝试使用下一个密钥。

---

## 35. 配置OpenClaw以使用Morpheus作为备用提供者（v0.2）

配置OpenClaw，使其在主要API的信用耗尽时使用Morpheus作为备用提供者。

### 步骤1：通过配置文件或手动编辑`openclaw.json`来添加Morpheus提供者

```json5
{
  "models": {
    "providers": {
      "morpheus": {
        "baseUrl": "http://127.0.0.1:8083/v1",
        "apiKey": "morpheus-local",
        "api": "openai-completions",
        "models": [
          {
            "id": "kimi-k2.5",
            "name": "Kimi K2.5 (via Morpheus)",
            "reasoning": true,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          },
          {
            "id": "kimi-k2-thinking",
            "name": "Kimi K2 Thinking (via Morpheus)",
            "reasoning": true,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          },
          {
            "id": "glm-4.7-flash",
            "name": "GLM 4.7 Flash (via Morpheus)",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

### 步骤2：设置多级备用提供者

建议使用多级备用提供者（从v0.5版本开始）：

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "venice/claude-opus-4-6",
        "fallbacks": [
          "venice/claude-opus-45",   // Different model, same provider
          "venice/kimi-k2-5",        // Open-source model, same provider
          "morpheus/kimi-k2.5"       // Decentralized fallback
        ]
      },
      "models": {
        "venice/claude-opus-45": { "alias": "Claude Opus 4.5" },
        "venice/kimi-k2-5": { "alias": "Kimi K2.5" },
        "morpheus/kimi-k2.5": { "alias": "Kimi K2.5 (Morpheus)" },
        "morpheus/kimi-k2-thinking": { "alias": "Kimi K2 Thinking (Morpheus)" },
        "morpheus/glm-4.7-flash": { "alias": "GLM 4.7 Flash (Morpheus)" }
      }
    }
  }
}
```

#### 为什么需要多级备用提供者？

**原因：** 单一备用提供者会导致单点故障。如果主要提供者和备用提供者同时进入冷却状态（例如，都遇到计费错误），代理就会离线。通过使用多个备用提供者，可以确保至少有一个路径可用。

### 步骤3：配置认证配置文件

OpenClaw支持为每个提供者配置多个API密钥，并自动轮换使用这些密钥：

```json
{
  "venice:default": {
    "type": "api_key",
    "provider": "venice",
    "key": "VENICE-INFERENCE-KEY-YOUR_KEY_HERE"
  },
  "morpheus:default": {
    "type": "api_key",
    "provider": "morpheus",
    "key": "morpheus-local"
  }
}
```

#### 单个密钥的配置（最低要求，v0.9.1版本）

将配置文件添加到`~/.openclaw/agents/main/agent/auth-profiles.json`中：

```json
{
  "venice:default": {
    "type": "api_key",
    "provider": "venice",
    "key": "VENICE-INFERENCE-KEY-YOUR_KEY_HERE"
  },
  "morpheus:default": {
    "type": "api_key",
    "provider": "morpheus",
    "key": "morpheus-local"
  }
}
```

#### 多个密钥的配置（推荐，v0.9.1版本）

如果您有多个Venice API密钥（例如来自不同的账户或计划），请将它们全部添加到配置文件中，并按照信用额度从高到低的顺序排列：

**auth-profiles.json`文件的内容如下：

```json
{
  "version": 1,
  "profiles": {
    "venice:key1": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_PRIMARY_KEY"
    },
    "venice:key2": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_SECOND_KEY"
    },
    "venice:key3": {
      "type": "api_key",
      "provider": "venice",
      "key": "VENICE-INFERENCE-KEY-YOUR_THIRD_KEY"
    },
    "morpheus:default": {
      "type": "api_key",
      "provider": "morpheus",
      "key": "morpheus-local"
    }
  }
}
```

**openclaw.json`文件用于注册这些配置文件，并指定轮换顺序：

```json5
{
  "auth": {
    "profiles": {
      "venice:key1": { "provider": "venice", "mode": "api_key" },
      "venice:key2": { "provider": "venice", "mode": "api_key" },
      "venice:key3": { "provider": "venice", "mode": "api_key" },
      "morpheus:default": { "provider": "morpheus", "mode": "api_key" }
    },
    "order": {
      "venice": ["venice:key1", "venice:key2", "venice:key3"]
    }
  }
}
```

#### `auth.order`参数的作用

`auth.order`参数非常重要。如果不设置，OpenClaw会使用轮询机制（按使用顺序依次尝试密钥），这可能导致信用分配不均衡。通过设置明确的顺序，可以确保按照预期的顺序使用密钥。

#### 多密钥轮换的原理

OpenClaw的认证机制会自动处理密钥的轮换：

1. **会话粘性**：每个会话都会使用固定的密钥，以确保会话的连续性。
2. **计费限制**：如果某个密钥返回计费错误，该密钥会被禁用，并在一段时间后重新尝试使用其他密钥。
3. **失败后的恢复**：禁用某个密钥后，OpenClaw会立即尝试使用下一个密钥。

---

## 36. 检查余额

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)

# MOR and ETH balance
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/balance | jq .

# Active sessions
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/sessions | jq .

# Available models
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/models | jq .
```

---

## 37. 故障排除

有关详细的故障排除指南，请参阅`references/troubleshooting.md`。以下是一些常见的错误及其解决方法：

| 错误 | 解决方法 |
|-------|-----|
| `session not found` | 使用`session_id/model_id`作为HTTP请求头信息，而不是请求体内容。 |
| `dial tcp: missing address` | 使用模型ID开启会话，而不是bid ID。 |
| `api adapter not found` | 确保`models-config.json`文件中包含了所需的模型配置。 |
| `ERC20: transfer amount exceeds balance` | 关闭旧的会话以释放锁定的MOR代币。 |
| 重启后会话丢失 | 这是正常现象，重启后可以重新开启会话。 |
| MorpheusUI与代理冲突 | 不要同时运行MorpheusUI和无界代理（agentless proxy）。 |

---

## 38. 关键合约地址（Base主网）

| 合约 | 地址 |
|----------|---------|
| Diamond | `0x6aBE1d282f72B474E54527D93b979A4f64d3030a` |
| MOR Token | `0x7431aDa8a591C955a994a21710752ef9b882b8e3` |

## 快速参考

| 动作 | 命令 |
|--------|---------|
| 安装 | `bash skills/everclaw/scripts/install.sh` |
| 启动 | `bash skills/everclaw/scripts/start.sh` |
| 停止 | `bash skills/everclaw/scripts/stop.sh` |
| 将ETH兑换为MOR | `bash skills/everclaw/scripts/swap.sh eth 0.01` |
| 将USDC兑换为MOR | `bash skills/everclaw/scripts/swap.sh usdc 50` |
| 开启会话 | `bash skills/everclaw/scripts/session.sh open <model> [duration>` |
| 关闭会话 | `bash skills/everclaw/scripts/session.sh close <session_id>` |
| 列出会话 | `bash skills/everclaw/scripts/session.sh list` |
| 发送提示 | `bash skills/everclaw/scripts/chat.sh <model> "prompt"` |
| 检查余额 | `bash skills/everclaw/scripts/balance.sh` |
| **诊断** | `bash skills/everclaw/scripts/diagnose.sh` |
| 仅配置诊断 | `bash skills/everclaw/scripts/diagnose.sh --config` |
| 快速诊断 | `bash skills/everclaw/scripts/diagnose.sh --quick` |

---

## 39. 钱包管理（v0.4）

Everclaw v0.4版本包含了一个自包含的钱包管理器，无需依赖任何外部账户。无需使用1Password、Foundry或Safe Wallet，只需macOS的Keychain和Node.js（这些工具已随OpenClaw一起提供）。

### 设置（一个命令）

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs setup
```

此命令会生成一个新的以太坊钱包，并将私钥存储在macOS的Keychain中（私钥在存储时会被加密，并受您的登录密码/Touch ID保护）。

### 导入现有钱包密钥

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs import-key 0xYOUR_PRIVATE_KEY
```

### 检查余额

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs balance
```

此命令会显示ETH、MOR和USDC的余额，以及用于Diamond合约的MOR代币余额。

### 将ETH/USDC兑换为MOR

```bash
# Swap 0.05 ETH for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap eth 0.05

# Swap 50 USDC for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap usdc 50
```

此命令会通过Uniswap V3在Base平台上执行兑换操作。无需任何外部工具，使用的内置工具为viem（已随OpenClaw一起提供）。

### 批准使用MOR代币进行质押

___CODE_BLOCK_27***

此命令会批准使用您的MOR代币进行质押。

### 安全性

- 私钥存储在macOS的Keychain中（存储时会被加密）。
- 由您的登录密码/Touch ID保护。
- 私钥在运行时注入，使用完毕后会被立即清除。
- 私钥永远不会以明文形式保存在磁盘上。
- 高级用户可以选择使用1Password作为备用方案（向下兼容）。