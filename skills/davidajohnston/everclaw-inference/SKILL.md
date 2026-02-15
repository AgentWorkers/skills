---
name: everclaw
version: 0.9.2
description: 您所拥有的AI推理能力将通过Morpheus去中心化网络持续为OpenClaw代理提供支持。通过质押MOR代币，您可以访问Kimi K2.5及30多个其他模型，并通过循环利用已质押的MOR代币来维持推理功能的持续运行。该系统还具备以下特性：  
- Morpheus API Gateway支持零配置启动；  
- 兼容OpenAI的代理服务，具备自动会话管理功能；  
- 具备自动重试机制，可在会话失效时自动重新发起请求；  
- 支持OpenAI标准的错误分类机制，有效防止因错误导致的系统故障；  
- 提供多密钥认证机制，用于管理Venice API密钥；  
- Gateway Guardian v2版本具备推理探针功能及自我修复机制；  
- 集成了安全防护功能；  
- 通过macOS Keychain实现零依赖的钱包管理；  
- 提供x402支付客户端，支持代理之间的USDC交易；  
- 支持ERC-8004标准，便于在Base平台上发现无需信任关系的代理节点。
homepage: https://everclaw.com
metadata:
  openclaw:
    emoji: "♾️"
    requires:
      bins: ["curl", "node"]
    tags: ["inference", "everclaw", "morpheus", "mor", "decentralized", "ai", "blockchain", "base", "persistent", "fallback", "guardian", "security"]
---

# ♾️ Everclaw — 您专属的AI推理服务，持续为您的OpenClaw代理提供强大支持

*由[Morpheus AI](https://mor.org)提供技术支持*

您可以使用自己的推理能力访问Kimi K2.5、Qwen3、GLM-4、Llama 3.3等模型。Everclaw将您的OpenClaw代理连接到Morpheus的P2P网络：质押MOR代币，开启会话，并回收代币以持续、自主地使用AI服务。

> ⚠️ **注意：**另一个名为“Everclaw Vault”的产品（提供加密云存储服务）也在ClawHub上使用了“everclaw”这个名称。**请勿运行`clawhub update everclaw`命令**，否则它可能会覆盖此技能的相关设置。该技能的更新请从GitHub获取：`cd skills/everclaw && git pull`。详情和恢复步骤请参阅`CLAWHUB_WARNING.md`。

## 工作原理

1. **获取MOR代币**：通过Uniswap或Aerodrome从ETH/USDC兑换MOR代币（具体方法见下文）。
2. 在本地运行一个代理路由器（Morpheus Lumerin Node）作为客户端。
3. 路由器连接到Base主网并发现模型提供者。
4. 持币质押MOR代币以开启与提供者的会话（MOR代币会被锁定，不会被消耗）。
5. 向`http://localhost:8082/v1/chat/completions`发送推理请求。
6. 会话结束后，您的MOR代币会被返还（扣除少量使用费用）。
7. 将返还的MOR代币重新质押以开启新的会话，从而持续使用您自己的推理服务。

## 获取MOR代币

您需要在Base平台上拥有MOR代币才能进行质押。如果您已经拥有ETH、USDC或USDT，可以按照以下步骤操作：

```bash
# Swap ETH for MOR
bash skills/everclaw/scripts/swap.sh eth 0.01

# Swap USDC for MOR
bash skills/everclaw/scripts/swap.sh usdc 50
```

或者您也可以在DEX平台上手动兑换：
- **Uniswap**：[在Base平台上兑换MOR/ETH](https://app.uniswap.org/explore/tokens/base/0x7431ada8a591c955a994a21710752ef9b882b8e3)
- **Aerodrome**：[在Aerodrome平台上兑换MOR](https://aerodrome.finance/swap?from=eth&to=0x7431ada8a591c955a994a21710752ef9b882b8e3)

如果您还没有在Base平台上任何资产，请先在Coinbase购买ETH，然后转移到Base平台，再兑换成MOR代币。详细步骤请参阅`references/acquiring-mor.md`。

**需要多少代币？**MOR代币仅被锁定，不会被消耗。日常使用50-100个MOR代币就足够了。0.005 ETH的费用足以覆盖数月的Base网络使用费用。

## 架构

```
Agent → proxy-router (localhost:8082) → Morpheus P2P Network → Provider → Model
                ↓
         Base Mainnet (MOR staking, session management)
```

---

## 1. 安装

### 推荐安装方式：一键安装器（v0.9.2）

这个安装器可以完成新安装、更新以及检测ClawHub名称冲突的问题：

```bash
# Fresh install
curl -fsSL https://raw.githubusercontent.com/profbernardoj/everclaw/main/scripts/install-everclaw.sh | bash

# Or if you already have the skill:
bash skills/everclaw/scripts/install-everclaw.sh

# Check for updates
bash skills/everclaw/scripts/install-everclaw.sh --check
```

安装器将：
- 检测并警告ClawHub上“Everclaw Vault”名称的冲突。
- 从GitHub克隆代码（新安装）或使用`git pull`进行更新。
- 显示设置路由器、代理和钱包的下一步操作。

### 替代方案：手动克隆代码

```bash
git clone https://github.com/profbernardoj/everclaw.git ~/.openclaw/workspace/skills/everclaw
```

### 更新

⚠️ **请勿使用`clawhub update everclaw`命令**——ClawHub上使用的是另一个产品的名称。请始终通过git进行更新：

```bash
cd ~/.openclaw/workspace/skills/everclaw && git pull
```

### 安装Morpheus路由器

克隆完成后，安装代理路由器：

```bash
bash skills/everclaw/scripts/install.sh
```

该命令会下载适用于您操作系统/架构的最新代理路由器版本，将其解压到`~/morpheus/`目录，并生成初始配置文件。

### 手动安装

1. 访问[Morpheus-Lumerin-Node的发布页面](https://github.com/MorpheusAIs/Morpheus-Lumerin-Node/releases)。
2. 下载适用于您平台的版本（例如`mor-launch-darwin-arm64.zip`）。
3. 解压到`~/morpheus/`目录。
4. 在macOS系统中，运行`xattr -cr ~/morpheus/`命令。

## 所需文件

安装完成后，`~/morpheus/`目录应包含以下文件：

| 文件 | 用途 |
|------|---------|
| `proxy-router` | 主执行文件 |
| `.env` | 配置文件（包含RPC、合约和端口信息） |
| `models-config.json` | 将区块链模型ID映射到API类型的配置文件 |
| `.cookie` | 自动生成的认证凭证 |

---

## 2. 配置

### `.env`文件

`.env`文件用于配置代理路由器在Base主网上的消费者模式。关键配置变量如下：

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

⚠️ **必须设置`ETH_NODE_ADDRESS`。**如果不设置，路由器将默认连接到空字符串，导致所有区块链操作失败。同时，`MODELS_CONFIG_PATH`必须指向`models-config.json`文件。

### `models-config.json`文件

⚠️ **此文件是必需的。**如果没有这个文件，聊天功能会因“api adapter not found”错误而无法使用。

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

⚠️ **注意文件格式**：JSON文件使用`"models"`数组，其中包含`"modelId"`、`"modelName"`、`"apiType"`和`"apiUrl"`字段。`apiUrl`字段保持为空——路由器会从区块链中自动解析提供者端点。请为要使用的每个模型添加相应的条目。详细信息请参阅`references/models.md`。

---

## 3. 启动路由器

### 安全启动（使用1Password）

代理路由器需要您的钱包私钥。**请勿将私钥存储在磁盘上**。请在运行时通过1Password注入私钥：

```bash
bash skills/everclaw/scripts/start.sh
```

或者您可以手动设置私钥：

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

### 健康检查

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

或者您也可以使用`pkill -f proxy-router`命令停止路由器。

---

## 4. 资金质押

在开启会话之前，需要批准Diamond合约以代表您转移MOR代币：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/approve?spender=0x6aBE1d282f72B474E54527D93b979A4f64d3030a&amount=1000000000000000000000"
```

⚠️ `/blockchain/approve`端点使用查询参数，而不是JSON请求体。`amount`参数以wei为单位（1000000000000000000 = 1 MOR代币）。请批准较大的金额，以避免频繁重新授权。

---

## 5. 开启会话

通过模型ID开启会话（而不是通过 bid ID）：

```bash
MODEL_ID="0xb487ee62516981f533d9164a0a3dcca836b06144506ad47a5c024a7a2a33fc58"

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/models/${MODEL_ID}/session" \
  -H "Content-Type: application/json" \
  -d '{"sessionDuration": 3600}'
```

⚠️ **始终使用模型ID端点**，而不是bid ID。使用bid ID会导致“dial tcp: missing address”错误。

### 会话时长

- 会话时长以秒为单位：3600秒 = 1小时，86400秒 = 1天。
- 需要执行两次区块链交易：一次用于批准转账，一次用于开启会话。
- 会话期间，MOR代币会被锁定。
- 会话结束后，MOR代币会被返还到您的钱包。

### 响应

响应中会包含一个`sessionId`（十六进制字符串）。请保存这个字符串，因为它用于后续的推理请求。

### 使用脚本

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

`session_id`和`model_id`属于HTTP请求头信息，而不是请求体内容。这是最常见的错误来源。

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

### 使用聊天脚本

```bash
bash skills/everclaw/scripts/chat.sh kimi-k2.5:web "What is the meaning of life?"
```

### 流式传输

在请求体中设置`"stream": true`。响应将以Server-Sent Events (SSE)格式返回。

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

会话结束后，锁定的MOR代币会被返还到您的钱包。请关闭不需要的会话，以便释放出更多的MOR代币用于新的会话。

---

## 8. 会话管理

### 会话是临时性的

### 注意：**

**会话在路由器重启后不会被保留**。如果重启代理路由器，您需要重新开启会话。虽然区块链上的会话仍然存在，但路由器的内存状态会丢失。

### 监控

```bash
# Check balance (MOR + ETH)
bash skills/everclaw/scripts/balance.sh

# List sessions
bash skills/everclaw/scripts/session.sh list
```

### 会话生命周期

1. **开启会话** → MOR代币被锁定，会话处于活动状态。
2. **活动状态** → 使用`session_id`请求头发送推理请求。
3. **会话过期** → 会话时长结束，MOR代币自动返还。
4. **手动关闭会话** → 立即关闭会话，MOR代币也会被返还。

### 重启后重新开启会话

重启路由器后，请按照以下步骤操作：

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

详情请参阅`references/troubleshooting.md`。常见故障及解决方法如下：

| 错误 | 解决方法 |
|-------|-----|
| `session not found` | 使用`session_id/model_id`作为HTTP请求头信息，而不是请求体内容 |
| `dial tcp: missing address` | 使用模型ID开启会话 |
| `api adapter not found` | 将模型添加到`models-config.json`文件中 |
| `ERC20: transfer amount exceeds balance` | 关闭旧的会话以释放锁定的MOR代币 |

---

## 11. 钱包管理（v0.4）

Everclaw v0.4版本包含了一个独立的钱包管理器，无需依赖任何外部服务。无需1Password、Foundry或Safe Wallet，只需macOS Keychain和Node.js（已随OpenClaw一起提供）。

### 设置（一键完成）

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs setup
```

该命令会生成一个新的以太坊钱包，并将私钥存储在您的macOS Keychain中（加密存储，受登录密码/Touch ID保护）。

### 导入现有私钥

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs import-key 0xYOUR_PRIVATE_KEY
```

### 检查余额

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs balance
```

该命令可以显示ETH、MOR和USDC的余额，以及用于Diamond合约的MOR代币余额。

### 交换ETH/USDC为MOR代币

```bash
# Swap 0.05 ETH for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap eth 0.05

# Swap 50 USDC for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap usdc 50
```

该命令会通过Uniswap V3在Base平台上执行代币交换。无需任何外部工具，使用的内置工具为viem（随OpenClaw一起提供）。

### 批准MOR代币用于质押

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs approve
```

该命令用于批准Morpheus Diamond合约使用您的MOR代币进行会话质押。

### 安全机制

- 私钥存储在macOS Keychain中（加密存储）。
- 由您的登录密码/Touch ID保护。
- 私钥仅在运行时注入，使用完毕后立即从环境中清除。
- 私钥永远不会以明文形式存储在磁盘上。
- 对于高级用户，支持使用1Password作为备用方案（向下兼容）。

### 完整命令参考

| 命令 | 说明 |
|---------|-------------|
| `setup` | 生成钱包并存储在Keychain中 |
| `address` | 显示钱包地址 |
| `balance` | 显示ETH、MOR和USDC的余额 |
| `swap eth <amount>` | 通过Uniswap V3交换ETH为MOR |
| `swap usdc <amount>` | 通过Uniswap V3交换USDC为MOR |
| `approve [amount]` | 批准使用MOR代币进行质押 |
| `export-key` | 打印私钥（请谨慎使用） |
| `import-key <0xkey>` | 导入现有的私钥 |

---

## 12. OpenAI兼容代理（v0.2）

Morpheus代理路由器需要自定义认证（使用`.cookie`进行基本认证）和自定义HTTP请求头（`session_id`、`model_id`），这些在标准OpenAI客户端中不可用。Everclaw提供了一个轻量级的代理来解决这个问题。

### 功能介绍

```
OpenClaw/any client → morpheus-proxy (port 8083) → proxy-router (port 8082) → Morpheus P2P → Provider
```

- 接受标准的OpenAI `/v1/chat/completions`请求。
- 根据需求自动开启区块链会话（无需手动管理会话）。
- 在会话到期前自动续订（默认为1小时前）。
- 自动注入基本认证信息和`session_id`/`model_id`请求头。
- 提供 `/health`、`/v1/models`、`/v1/chat/completions`等接口。

### 安装

```bash
bash skills/everclaw/scripts/install-proxy.sh
```

安装步骤如下：
- 将`morpheus-proxy.mjs`文件解压到`~/morpheus/proxy/`目录。
- 将`gateway-guardian.sh`文件添加到`~/.openclaw/workspace/scripts/`目录。
- 在macOS系统中，使用`launchd`服务使代理路由器在系统启动时自动运行。

### 配置

以下环境变量为可选设置（默认值合理）：

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `MORPHEUS_PROXY_PORT` | `8083` | 代理路由器监听的端口 |
| `MORPHEUS_ROUTER_URL` | `http://localhost:8082` | 代理路由器地址 |
| `MORPHEUS COOKIE_PATH` | `~/morpheus/.cookie` | 认证cookie的存储路径 |
| `MORPHEUS_SESSION_DURATION` | `604800`（7天） | 会话持续时间（秒） |
| `MORPHEUS_RENEW_BEFORE` | `3600`（1小时） | 会话续订间隔（秒） |
| `MORPHEUS_PROXY_API_KEY` | `morpheus-local` | 代理认证所需的bearer令牌 |

### 会话时长

会话期间，MOR代币会被锁定。会话持续时间越长，锁定的MOR代币越多，但区块链交易次数越少：

| 会话时长 | 锁定的MOR代币数量 | 交易次数 |
|----------|--------------------:|:-------------|
| 1小时 | ~11 MOR | 每小时 |
| 1天 | ~274 MOR | 每天 |
| 7天 | ~1,915 MOR | 每周 |

会话结束后或过期时，MOR代币会被返还。代理会在会话到期前自动续订，从而实现连续的推理服务，同时降低质押成本。

### 健康检查

```bash
curl http://127.0.0.1:8083/health
```

### 可用的模型

```bash
curl http://127.0.0.1:8083/v1/models
```

### 直接使用（无需OpenClaw）

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

### 可靠性说明

- **`kimi-k2.5`（非Web版本）是最可靠的模型，建议作为首选备用模型。
- **`kimi-k2.5:web`（Web搜索版本）在P2P路由时容易超时，不建议作为备用模型使用。
- 提供者连接可能会暂时中断，但通常可以重试。
- 代理本身作为一个KeepAlive服务运行，如果崩溃会自动重启。

### 代理的容错性（v0.5）

v0.5版本对代理进行了三项关键改进，以防止因**冷却机制连锁反应**导致的长时间中断：

#### 问题：冷却机制连锁反应

当主要提供者（例如venice）返回错误时，OpenClaw的故障转移机制会将该提供者标记为“处于冷却状态”。如果Morpheus代理也返回错误（OpenClaw可能将其误判为计费错误），**两个提供者都会进入冷却状态**，导致代理完全离线（有时会持续6小时以上）。

#### 解决方案1：OpenAI兼容的错误编码

现在代理返回的错误信息符合OpenAI的格式，包含`type`和`code`字段：

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

**关键区别：**所有Morpheus相关的错误都会被标记为`"server_error"`，而不会被标记为`"billing"`或`"rate_limit_error"`。这样OpenClaw会将其视为临时故障并适当重试，而不会将提供者置于长时间冷却状态。

代理返回的错误代码如下：

| 错误代码 | 含义 |
|------|---------|
| `morpheus_session_error` | 无法打开或刷新区块链会话 |
| `morpheus_inference_error` | 提供者在推理过程中返回错误 |
| `morpheus_upstream_error` | 与代理路由器的连接失败 |
| `timeout` | 请求超时 |
| `model_not_found` | 请求的模型不存在 |

#### 解决方案2：自动会话重试

当代理路由器返回与会话相关的错误时（例如会话过期、无效或未找到模型），代理会：
1. **使缓存的会话失效**。
2. **打开一个新的区块链会话**。
3. **重新尝试推理请求**。

#### 多层备用机制

配置OpenClaw时，可以为不同的提供者设置多个备用模型：

```json5
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "venice/claude-opus-4-6",
        "fallbacks": [
          "venice/claude-opus-45",    // Try different Venice model first
          "venice/kimi-k2-5",         // Try yet another Venice model
          "morpheus/kimi-k2.5"        // Last resort: decentralized inference
        ]
      }
    }
  }
}
```

这样，如果主要模型出现问题，OpenClaw会尝试其他模型（可能具有不同的计费限制），然后再尝试Morpheus模型。

---

## 13. OpenClaw集成（v0.2）

配置OpenClaw以使用Morpheus作为备用提供者，确保代理在主要API的信用耗尽时仍能继续运行。

### 第1步：添加Morpheus提供者

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

### 第2步：设置备用机制

建议使用多层备用机制（从v0.5版本开始）：

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

### 为什么需要多层备用机制？

**单层备用机制**存在单点故障风险。如果主要提供者和备用提供者同时进入冷却状态（例如，都出现计费错误），代理将无法运行。通过设置多层备用模型，可以确保至少有一个路径可用。

### 第3步：配置认证配置文件

OpenClaw支持为每个提供者配置多个API密钥，并自动轮换使用顺序。当某个密钥的信用耗尽时，OpenClaw只会禁用该密钥，并自动切换到下一个密钥（使用相同的模型和新的信用额度）。这是防止系统中断的最有效方法。

#### 单密钥配置（最低要求）

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

### 多密钥配置（推荐使用，从v0.9.1版本开始）

如果您有多个Venice API密钥（例如来自不同的账户或计划），请将它们全部添加到配置文件中，并指定使用顺序：

**auth-profiles.json**文件示例：

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

**openclaw.json**文件用于注册这些配置文件并指定使用顺序：

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

### `auth.order`参数的作用

`auth.order`参数非常重要。如果不设置，OpenClaw会使用轮询顺序（按使用频率排序），这可能无法准确反映实际的信用使用情况。通过指定使用顺序，OpenClaw会按照您指定的顺序尝试不同的密钥。

#### 多密钥轮换的工作原理

OpenClaw的认证机制会自动处理密钥轮换：
1. **会话粘性**：每个会话都会固定使用一个密钥，以确保提供者缓存的有效性。
2. **计费限制**：如果某个密钥返回计费错误，该密钥会被禁用，并在一段时间后重新尝试使用。
3. **失败后的处理**：禁用某个密钥后，OpenClaw会立即尝试使用`auth.order`列表中的下一个密钥。
4. **多模型备用**：只有在所有Venice相关的密钥都被禁用后，才会尝试其他备用模型。

---

## 14. OpenClaw集成（v0.2）

配置OpenClaw以使用Morpheus作为备用提供者，确保代理在主要API的信用耗尽时仍能继续运行。

### 第1步：通过配置文件或手动编辑`openclaw.json`来添加Morpheus提供者。

### 第2步：设置多层备用机制

建议从v0.5版本开始使用多层备用机制：

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

### 为什么需要多层备用机制？

**单层备用机制**存在单点故障风险。如果主要提供者和备用提供者同时进入冷却状态，代理将无法运行。通过设置多层备用模型，可以确保至少有一个路径可用。

### 第3步：配置认证配置文件

OpenClaw支持为每个提供者配置多个API密钥，并自动轮换使用顺序。当某个密钥的信用耗尽时，OpenClaw只会禁用该密钥，并自动尝试使用下一个密钥（使用相同的模型和新的信用额度）。

---

## 15. OpenClaw集成（v0.2）

### 安装步骤

### 推荐安装方式：一键安装器（v0.9.2）

这个安装器可以完成新安装、更新以及检测ClawHub名称冲突的问题：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)

# MOR and ETH balance
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/balance | jq .

# Active sessions
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/sessions | jq .

# Available models
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/blockchain/models | jq .
```

安装器会：
- 检测并警告ClawHub上“Everclaw Vault”名称的冲突。
- 从GitHub克隆代码（新安装）或使用`git pull`进行更新。
- 显示设置路由器、代理和钱包的下一步操作。

### 替代方案：手动克隆代码

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

### 更新

### 注意：**

**请勿使用`clawhub update everclaw`命令**——ClawHub上使用的是另一个产品的名称。请始终通过git进行更新：

```bash
tail -f ~/.openclaw/logs/guardian.log
```

### 安装Morpheus路由器

克隆完成后，安装代理路由器：

```bash
bash skills/everclaw/scripts/install.sh
```

该命令会下载适用于您操作系统/架构的最新代理路由器版本，将其解压到`~/morpheus/`目录，并生成初始配置文件。

### 手动安装

1. 访问[Morpheus-Lumerin-Node的发布页面](https://github.com/MorpheusAIs/Morpheus-Lumerin-Node/releases)。
2. 下载适用于您平台的版本（例如`mor-launch-darwin-arm64.zip`）。
3. 解压到`~/morpheus/`目录。
4. 在macOS系统中，运行`xattr -cr ~/morpheus/`命令。

### 所需文件

安装完成后，`~/morpheus/`目录应包含以下文件：

| 文件 | 用途 |
|------|---------|
| `proxy-router` | 主执行文件 |
| `.env` | 配置文件（包含RPC、合约和端口信息） |
| `models-config.json` | 将区块链模型ID映射到API类型的配置文件 |
| `.cookie` | 自动生成的认证凭证 |

---

## 16. 配置

### `.env`文件

`.env`文件用于配置代理路由器在Base主网上的消费者模式。关键配置变量如下：

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

#### 注意：

- **必须设置`ETH_NODE_ADDRESS`。**如果不设置，路由器将无法连接到区块链，所有操作都会失败。
- `MODELS_CONFIG_PATH`必须指向`models-config.json`文件。

### `models-config.json`文件

#### 注意：

**此文件是必需的。**如果没有这个文件，聊天功能会因“api adapter not found”错误而无法使用。

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

#### 注意文件格式：

JSON文件使用`"models"`数组，其中包含`"modelId"`、`" modelName"`、`"apiType"`和`"apiUrl`字段。`apiUrl`字段保持为空——路由器会从区块链中自动解析提供者端点。请为要使用的每个模型添加相应的条目。详细信息请参阅`references/models.md`。

---

## 17. 启动代理路由器

### 安全启动（使用1Password）

代理路由器需要您的钱包私钥。**请勿将私钥存储在磁盘上**。请在运行时通过1Password注入私钥：

```bash
bash skills/everclaw/scripts/start.sh
```

或者您也可以手动设置私钥：

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

### 检查代理路由器的运行状态

等待几秒钟，然后检查代理路由器的运行状态：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/healthcheck
```

预期响应：HTTP 200。

### 停止代理路由器

```bash
bash skills/everclaw/scripts/stop.sh
```

或者您也可以使用`pkill -f proxy-router`命令停止代理路由器。

---

## 18. 资金质押

在开启会话之前，需要批准Diamond合约以代表您转移MOR代币：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/approve?spender=0x6aBE1d282f72B474E54527D93b979A4f64d3030a&amount=1000000000000000000000"
```

### 注意：

**/blockchain/approve`端点使用查询参数，而不是JSON请求体。**`amount`参数以wei为单位（1000000000000000000 = 1 MOR代币）。请批准较大的金额，以避免频繁重新授权。

---

## 19. 开启会话

通过模型ID开启会话（而不是通过bid ID）：

```bash
MODEL_ID="0xb487ee62516981f533d9164a0a3dcca836b06144506ad47a5c024a7a2a33fc58"

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/models/${MODEL_ID}/session" \
  -H "Content-Type: application/json" \
  -d '{"sessionDuration": 3600}'
```

### 注意：

**始终使用模型ID端点**，而不是bid ID。使用bid ID会导致“dial tcp: missing address”错误。

### 会话时长

会话时长以秒为单位：
- 3600秒 = 1小时
- 86400秒 = 1天

开启会话需要执行两次区块链交易：一次用于批准转账，一次用于开启会话。
会话期间，MOR代币会被锁定。
会话结束后，MOR代币会被返还到您的钱包。

### 响应

响应中会包含一个`sessionId`（十六进制字符串）。请保存这个字符串，因为它用于后续的推理请求。

### 使用脚本

```bash
# Open a 1-hour session for kimi-k2.5:web
bash skills/everclaw/scripts/session.sh open kimi-k2.5:web 3600

# List active sessions
bash skills/everclaw/scripts/session.sh list

# Close a session
bash skills/everclaw/scripts/session.sh close 0xSESSION_ID_HERE
```

---

## 20. 发送推理请求

### 注意：

**重要提示：**`session_id`和`model_id`属于HTTP请求头信息，而不是请求体内容。这是最常见的错误来源。

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

---

## 21. 使用聊天脚本

```bash
bash skills/everclaw/scripts/chat.sh kimi-k2.5:web "What is the meaning of life?"
```

### 流式传输

在请求体中设置`"stream": true`。响应将以Server-Sent Events (SSE)格式返回。

---

## 22. 关闭会话

关闭会话以释放锁定的MOR代币：

```bash
curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/sessions/0xSESSION_ID/close"
```

或者您也可以使用相应的脚本来关闭会话：

```bash
bash skills/everclaw/scripts/session.sh close 0xSESSION_ID
```

### 注意：

会话结束后，锁定的MOR代币会被返还到您的钱包。请关闭不需要的会话，以便释放出更多的MOR代币用于新的会话。

---

## 23. 会话管理

### 会话是临时性的

### 注意：

**会话在路由器重启后不会被保留**。如果重启代理路由器，您需要重新开启会话。虽然区块链上的会话仍然存在，但路由器的内存状态会丢失。

### 监控

```bash
# Check balance (MOR + ETH)
bash skills/everclaw/scripts/balance.sh

# List sessions
bash skills/everclaw/scripts/session.sh list
```

### 会话生命周期

1. **开启会话** → MOR代币被锁定，会话处于活动状态。
2. **活动状态** → 使用`session_id`请求头发送推理请求。
3. **会话过期** → 会话时长结束，MOR代币自动返还。
4. **关闭会话** → 手动关闭会话，MOR代币立即返还。

### 重启后重新开启会话

重启代理路由器后，请按照以下步骤操作：

```bash
# Wait for health check
sleep 5

# Re-open sessions for models you need
bash skills/everclaw/scripts/session.sh open kimi-k2.5:web 3600
```

---

## 24. 检查余额

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

## 25. 故障排除

详情请参阅`references/troubleshooting.md`。常见故障及解决方法如下：

| 错误 | 解决方法 |
|-------|-----|
| `session not found` | 使用`session_id/model_id`作为HTTP请求头信息，而不是请求体内容 |
| `dial tcp: missing address` | 使用模型ID开启会话 |
| `api adapter not found` | 将模型添加到`models-config.json`文件中 |
| `ERC20: transfer amount exceeds balance` | 关闭旧的会话以释放锁定的MOR代币 |
| 会话在重启后消失** | 正常现象——重启后重新开启会话 |

---

## 26. 关键合约地址（Base主网）

| 合约 | 地址 |
|----------|---------|
| Diamond | `0x6aBE1d282f72B474E54527D93b979A4f64d3030a` |
| MOR Token | `0x7431aDa8a591C955a994a21710752ef9b882b8e3` |

## 快速参考

| 功能 | 命令 |
|--------|---------|
| 安装 | `bash skills/everclaw/scripts/install.sh` |
| 启动 | `bash skills/everclaw/scripts/start.sh` |
| 停止 | `bash skills/everclaw/scripts/stop.sh` |
| 交换ETH为MOR | `bash skills/everclaw/scripts/swap.sh eth 0.01` |
| 交换USDC为MOR | `bash skills/everclaw/scripts/swap.sh usdc 50` |
| 开启会话 | `bash skills/everclaw/scripts/session.sh open <model> [duration]` |
| 关闭会话 | `bash skills/everclaw/scripts/session.sh close <session_id>` |
| 列出会话 | `bash skills/everclaw/scripts/session.sh list` |
| 发送提示 | `bash skills/everclaw/scripts/chat.sh <model> "prompt"` |
| 检查余额 | `bash skills/everclaw/scripts/balance.sh` |

---

## 27. 钱包管理（v0.4）

Everclaw v0.4版本包含了一个独立的钱包管理器，无需依赖任何外部服务。无需1Password、Foundry或Safe Wallet，只需macOS Keychain和Node.js（已随OpenClaw一起提供）。

### 设置（一键完成）

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs setup
```

该命令会生成一个新的以太坊钱包，并将私钥存储在您的macOS Keychain中（加密存储，受登录密码/Touch ID保护）。

### 导入现有私钥

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs import-key 0xYOUR_PRIVATE_KEY
```

### 检查余额

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs balance
```

该命令可以显示ETH、MOR和USDC的余额，以及用于Diamond合约的MOR代币余额。

### 交换ETH/USDC为MOR

```bash
# Swap 0.05 ETH for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap eth 0.05

# Swap 50 USDC for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap usdc 50
```

该命令会通过Uniswap V3在Base平台上执行代币交换。无需任何外部工具，使用的内置工具为viem（随OpenClaw一起提供）。

### 批准MOR代币用于质押

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs approve
```

该命令用于批准Morpheus Diamond合约使用您的MOR代币进行会话质押。

### 安全机制

- 私钥存储在macOS Keychain中（加密存储）。
- 由您的登录密码/Touch ID保护。
- 私钥仅在运行时注入，使用完毕后立即从环境中清除。
- 私钥永远不会以明文形式存储在磁盘上。
- 对于高级用户，支持使用1Password作为备用方案（向下兼容）。

### 完整命令参考

| 命令 | 说明 |
|---------|-------------|
| `setup` | 生成钱包并存储在Keychain中 |
| `address` | 显示钱包地址 |
| `balance` | 显示ETH、MOR和USDC的余额 |
| `swap eth <amount>` | 通过Uniswap V3交换ETH为MOR |
| `swap usdc <amount>` | 通过Uniswap V3交换USDC为MOR |
| `approve [amount]` | 批准使用MOR代币进行质押 |
| `export-key` | 打印私钥（请谨慎使用） |
| `import-key <0xkey>` | 导入现有的私钥 |

---

## 28. OpenAI兼容代理（v0.2）

Morpheus代理路由器需要自定义认证（使用`.cookie`进行基本认证）和自定义HTTP请求头（`session_id`、`model_id`），这些在标准OpenAI客户端中不可用。Everclaw提供了一个轻量级的代理来解决这个问题。

### 功能介绍

```
OpenClaw/any client → morpheus-proxy (port 8083) → proxy-router (port 8082) → Morpheus P2P → Provider
```

- 接受标准的OpenAI `/v1/chat/completions`请求。
- 根据需求自动开启区块链会话（无需手动管理会话）。
- 在会话到期前自动续订（默认为1小时前）。
- 自动注入基本认证信息和`session_id`/`model_id`请求头。
- 提供 `/health`、`/v1/models`、`/v1/chat/completions`等接口。

### 安装步骤

```bash
bash skills/everclaw/scripts/install-proxy.sh
```

安装步骤如下：
- 将`morpheus-proxy.mjs`文件解压到`~/morpheus/proxy/`目录。
- 将`gateway-guardian.sh`文件添加到`~/.openclaw/workspace/scripts/`目录。
- 在macOS系统中，使用`launchd`服务使代理路由器在系统启动时自动运行。

### 配置

以下环境变量为可选设置（默认值合理）：

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `MORPHEUS_PROXY_PORT` | `8083` | 代理路由器监听的端口 |
| MORPHEUS_ROUTER_URL` | `http://localhost:8082` | 代理路由器地址 |
| MORPHEUS COOKIE_PATH` | `~/morpheus/.cookie` | 认证cookie的存储路径 |
| MORPHEUS_SESSION_DURATION` | `604800`（7天） | 会话持续时间（秒） |
| MORPHEUS_RENEW_BEFORE` | `3600`（1小时） | 会话续订间隔（秒） |
| MORPHEUS_PROXY_API_KEY` | `morpheus-local` | 代理认证所需的bearer令牌 |

### 会话时长

会话期间，MOR代币会被锁定。会话持续时间越长，锁定的MOR代币越多，但区块链交易次数越少：

| 会话时长 | 锁定的MOR代币数量 | 交易次数 |
|----------|--------------------:|:-------------|
| 1小时 | ~11 MOR | 每小时 |
| 1天 | ~274 MOR | 每天 |
| 7天 | ~1,915 MOR | 每周 |

会话结束后或过期时，MOR代币会被返还。代理会在会话到期前自动续订，从而实现连续的推理服务，同时降低质押成本。

### 健康检查

```bash
curl http://127.0.0.1:8083/health
```

### 可用的模型

```bash
curl http://127.0.0.1:8083/v1/models
```

### 直接使用（无需OpenClaw）

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

### 可靠性说明

- **`kimi-k2.5`（非Web版本）是最可靠的模型，建议作为首选备用模型。
- **`kimi-k2.5:web`（Web搜索版本）在P2P路由时容易超时，不推荐作为备用模型。
- 提供者连接可能会暂时中断，但通常可以重试。
- 代理本身作为一个KeepAlive服务运行，如果崩溃会自动重启。

### 代理的容错性（v0.5）

v0.5版本对代理进行了三项关键改进，以防止因**冷却机制连锁反应**导致的长时间中断：

#### 问题：冷却机制连锁反应

当主要提供者（例如venice）返回错误时，OpenClaw的故障转移机制会将该提供者标记为“处于冷却状态”。如果Morpheus代理也返回错误（OpenClaw可能将其误判为计费错误），**两个提供者都会进入冷却状态**，导致代理完全离线（有时会持续6小时以上）。

#### 解决方案1：OpenAI兼容的错误编码

现在代理返回的错误信息符合OpenAI的格式，包含`type`和`code`字段：

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

**关键区别：**所有Morpheus相关的错误都会被标记为`"server_error"`，而不会被标记为`"billing"`或`"rate_limit_error"`。这样OpenClaw会将其视为临时故障并适当重试，而不会将提供者置于长时间冷却状态。

代理返回的错误代码如下：

| 错误代码 | 含义 |
|------|---------|
| `morpheus_session_error` | 无法打开或刷新区块链会话 |
| `morpheus_inference_error` | 提供者在推理过程中返回错误 |
| `morpheus_upstream_error` | 与代理路由器的连接失败 |
| `timeout` | 请求超时 |
| `model_not_found` | 请求的模型不存在 |

#### 解决方案2：自动会话重试

当代理路由器返回与会话相关的错误时（例如会话过期、无效或未找到模型），代理会：
1. **使缓存的会话失效**。
2. **打开一个新的区块链会话**。
3. **重新尝试推理请求**。

#### 处理代理重启后的情况

#### 1. **安全启动（使用1Password）**

代理路由器需要您的钱包私钥。**请勿将私钥存储在磁盘上**。请在运行时通过1Password注入私钥：

```bash
bash skills/everclaw/scripts/start.sh
```

或者您也可以手动设置私钥：

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

### 检查代理路由器的运行状态

等待几秒钟，然后检查代理路由器的运行状态：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/healthcheck
```

预期响应：HTTP 200。

### 停止代理路由器

```bash
bash skills/everclaw/scripts/stop.sh
```

或者您也可以使用`pkill -f proxy-router`命令停止代理路由器。

---

## 29. 开启会话前需要批准Diamond合约

在开启会话之前，需要批准Diamond合约以代表您转移MOR代币：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/approve?spender=0x6aBE1d282f72B474E54527D93b979A4f64d3030a&amount=1000000000000000000000"
```

### 注意：

**/blockchain/approve`端点使用查询参数，而不是JSON请求体。**`amount`参数以wei为单位（1000000000000000000 = 1 MOR代币）。请批准较大的金额，以避免频繁重新授权。

---

## 30. 根据模型ID开启会话

通过模型ID开启会话（而不是通过bid ID）：

```bash
MODEL_ID="0xb487ee62516981f533d9164a0a3dcca836b06144506ad47a5c024a7a2a33fc58"

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/models/${MODEL_ID}/session" \
  -H "Content-Type: application/json" \
  -d '{"sessionDuration": 3600}'
```

### 注意：

**始终使用模型ID端点**，而不是bid ID。使用bid ID会导致“dial tcp: missing address”错误。

### 会话时长

会话时长以秒为单位：
- 3600秒 = 1小时
- 86400秒 = 1天

开启会话需要执行两次区块链交易：一次用于批准转账，一次用于开启会话。
会话期间，MOR代币会被锁定。
会话结束后，MOR代币会被返还到您的钱包。

### 响应

响应中会包含一个`sessionId`（十六进制字符串）。请保存这个字符串，因为它用于后续的推理请求。

### 使用脚本

```bash
# Open a 1-hour session for kimi-k2.5:web
bash skills/everclaw/scripts/session.sh open kimi-k2.5:web 3600

# List active sessions
bash skills/everclaw/scripts/session.sh list

# Close a session
bash skills/everclaw/scripts/session.sh close 0xSESSION_ID_HERE
```

---

## 31. 发送推理请求

### 注意：

**重要提示：**`session_id`和`model_id`属于HTTP请求头信息，而不是请求体内容。这是最常见的错误来源。

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

---

## 32. 使用聊天脚本

```bash
bash skills/everclaw/scripts/chat.sh kimi-k2.5:web "What is the meaning of life?"
```

### 流式传输

在请求体中设置`"stream": true`。响应将以Server-Sent Events (SSE)格式返回。

---

## 33. 关闭会话

关闭会话以释放锁定的MOR代币：

```bash
curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/sessions/0xSESSION_ID/close"
```

或者您也可以使用相应的脚本来关闭会话：

```bash
bash skills/everclaw/scripts/session.sh close 0xSESSION_ID
```

### 注意：

会话结束后，锁定的MOR代币会被返还到您的钱包。请关闭不需要的会话，以便释放出更多的MOR代币用于新的会话。

---

## 34. 会话管理

### 会话是临时性的

### 注意：

**会话在路由器重启后不会被保留**。如果重启代理路由器，您需要重新开启会话。虽然区块链上的会话仍然存在，但路由器的内存状态会丢失。

### 监控

```bash
# Check balance (MOR + ETH)
bash skills/everclaw/scripts/balance.sh

# List sessions
bash skills/everclaw/scripts/session.sh list
```

### 会话生命周期

1. **开启会话** → MOR代币被锁定，会话处于活动状态。
2. **活动状态** → 使用`session_id`请求头发送推理请求。
3. **会话过期** → 会话时长结束，MOR代币自动返还。
4. **关闭会话** → 手动关闭会话，MOR代币立即返还。

### 重启后重新开启会话

重启代理路由器后，请按照以下步骤操作：

```bash
# Wait for health check
sleep 5

# Re-open sessions for models you need
bash skills/everclaw/scripts/session.sh open kimi-k2.5:web 3600
```

---

## 35. 检查余额

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

## 36. 故障排除

详情请参阅`references/troubleshooting.md`。常见故障及解决方法如下：

| 错误 | 解决方法 |
|-------|-----|
| `session not found` | 使用`session_id/model_id`作为HTTP请求头信息，而不是请求体内容 |
| `dial tcp: missing address` | 使用模型ID开启会话 |
| `api adapter not found` | 将模型添加到`models-config.json`文件中 |
| `ERC20: transfer amount exceeds balance` | 关闭旧的会话以释放锁定的MOR代币 |
| 会话在重启后消失** | 正常现象——重启后重新开启会话 |
| MorpheusUI与代理路由器同时运行** | 请勿同时运行MorpheusUI和代理路由器 |

---

## 37. 主要合约地址（Base主网）

| 合约 | 地址 |
|----------|---------|
| Diamond | `0x6aBE1d282f72B474E54527D93b979A4f64d3030a` |
| MOR Token | `0x7431aDa8a591C955a994a21710752ef9b882b8e3` |

## 快速参考

| 功能 | 命令 |
|--------|---------|
| 安装 | `bash skills/everclaw/scripts/install.sh` |
| 启动 | `bash skills/everclaw/scripts/start.sh` |
| 停止 | `bash skills/everclaw/scripts/stop.sh` |
| 交换ETH为MOR | `bash skills/everclaw/scripts/swap.sh eth 0.01` |
| 交换USDC为MOR | `bash skills/everclaw/scripts/swap.sh usdc 50` |
| 开启会话 | `bash skills/everclaw/scripts/session.sh open <model> [duration]` |
| 关闭会话 | `bash skills/everclaw/scripts/session.sh close <session_id>` |
| 列出会话 | `bash skills/everclaw/scripts/session.sh list` |
| 发送提示 | `bash skills/everclaw/scripts/chat.sh <model> "prompt"` |
| 检查余额 | `bash skills/everclaw/scripts/balance.sh` |

---

## 38. 钱包管理（v0.4）

Everclaw v0.4版本包含了一个独立的钱包管理器，无需依赖任何外部服务。无需1Password、Foundry或Safe Wallet，只需macOS Keychain和Node.js（已随OpenClaw一起提供）。

### 设置（一键完成）

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs setup
```

该命令会生成一个新的以太坊钱包，并将私钥存储在您的macOS Keychain中（加密存储，受登录密码/Touch ID保护）。

### 导入现有私钥

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs import-key 0xYOUR_PRIVATE_KEY
```

### 检查余额

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs balance
```

该命令可以显示ETH、MOR和USDC的余额，以及用于Diamond合约的MOR代币余额。

### 交换ETH/USDC为MOR

```bash
# Swap 0.05 ETH for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap eth 0.05

# Swap 50 USDC for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap usdc 50
```

该命令会通过Uniswap V3在Base平台上执行代币交换。无需任何外部工具，使用的内置工具为viem（随OpenClaw一起提供）。

### 批准MOR代币用于质押

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs approve
```

该命令用于批准Morpheus Diamond合约使用您的MOR代币进行会话质押。

### 安全机制

- 私钥存储在macOS Keychain中（加密存储）。
- 由您的登录密码/Touch ID保护。
- 私钥仅在运行时注入，使用完毕后立即从环境中清除。
- 私钥永远不会以明文形式存储在磁盘上。
- 对于高级用户，支持使用1Password作为备用方案（向下兼容）。

### 完整命令参考

| 命令 | 说明 |
|---------|-------------|
| `setup` | 生成钱包并存储在Keychain中 |
| `address` | 显示钱包地址 |
| `balance` | 显示ETH、MOR和USDC的余额 |
| `swap eth <amount>` | 通过Uniswap V3交换ETH为MOR |
| `swap usdc <amount>` | 通过Uniswap V3交换USDC为MOR |
| `approve [amount]` | 批准使用MOR代币进行质押 |
| `export-key` | 打印私钥（请谨慎使用） |
| `import-key <0xkey>` | 导入现有的私钥 |

---

## 39. OpenAI兼容代理（v0.2）

Morpheus代理路由器需要自定义认证（使用`.cookie`进行基本认证）和自定义HTTP请求头（`session_id`、`model_id`），这些在标准OpenAI客户端中不可用。Everclaw提供了一个轻量级的代理来解决这个问题。

### 功能介绍

```
OpenClaw/any client → morpheus-proxy (port 8083) → proxy-router (port 8082) → Morpheus P2P → Provider
```

- 接受标准的OpenAI `/v1/chat/completions`请求。
- 根据需求自动开启区块链会话（无需手动管理会话）。
- 在会话到期前自动续订（默认为1小时前）。
- 自动注入基本认证信息和`session_id`/`model_id`请求头。
- 提供 `/health`、`/v1/models`、`/v1/chat/completions`等接口。

### 安装步骤

```bash
bash skills/everclaw/scripts/install-proxy.sh
```

安装步骤如下：
- 将`morpheus-proxy.mjs`文件解压到`~/morpheus/proxy/`目录。
- 将`gateway-guardian.sh`文件添加到`~/.openclaw/workspace/scripts/`目录。
- 在macOS系统中，使用`launchd`服务使代理路由器在系统启动时自动运行。

### 配置

以下环境变量为可选设置（默认值合理）：

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| `MORPHEUS_PROXY_PORT` | `8083` | 代理路由器监听的端口 |
| MORPHEUS_ROUTER_URL` | `http://localhost:8082` | 代理路由器地址 |
| MORPHEUS COOKIE_PATH` | `~/morpheus/.cookie` | 认证cookie的存储路径 |
| MORPHEUS_SESSION_DURATION` | `604800`（7天） | 会话持续时间（秒） |
| MORPHEUS_RENEW_BEFORE` | `3600`（1小时） | 会话续订间隔（秒） |
| MORPHEUS_PROXY_API_KEY` | `morpheus-local` | 代理认证所需的bearer令牌 |

### 会话时长

会话期间，MOR代币会被锁定。会话持续时间越长，锁定的MOR代币越多，但区块链交易次数越少：

| 会话时长 | 锁定的MOR代币数量 | 交易次数 |
|----------|--------------------:|:-------------|
| 1小时 | ~11 MOR | 每小时 |
| 1天 | ~274 MOR | 每天 |
| 7天 | ~1,915 MOR | 每周 |

会话结束后或过期时，MOR代币会被返还。代理会在会话到期前自动续订，从而实现连续的推理服务，同时降低质押成本。

### 健康检查

```bash
curl http://127.0.0.1:8083/health
```

### 可用的模型

```bash
curl http://127.0.0.1:8083/v1/models
```

### 直接使用（无需OpenClaw）

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

### 可靠性说明

- **`kimi-k2.5`（非Web版本）是最可靠的模型，建议作为首选备用模型。
- **`kimi-k2.5:web`（Web搜索版本）在P2P路由时容易超时，不推荐作为备用模型。
- 提供者连接可能会暂时中断，但通常可以重试。
- 代理本身作为一个KeepAlive服务运行，如果崩溃会自动重启。

### 代理的容错性（v0.5）

v0.5版本对代理进行了三项关键改进，以防止因**冷却机制连锁反应**导致的长时间中断：

#### 问题：冷却机制连锁反应

当主要提供者（例如venice）返回错误时，OpenClaw的故障转移机制会将该提供者标记为“处于冷却状态”。如果Morpheus代理也返回错误（OpenClaw可能将其误判为计费错误），**两个提供者都会进入冷却状态**，导致代理完全离线（有时会持续6小时以上）。

#### 解决方案1：OpenAI兼容的错误编码

现在代理返回的错误信息符合OpenAI的格式，包含`type`和`code`字段：

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

**关键区别：**所有Morpheus相关的错误都会被标记为`"server_error"`，而不会被标记为`"billing"`或`"rate_limit_error"`。这样OpenClaw会将其视为临时故障并适当重试，而不会将提供者置于长时间冷却状态。

代理返回的错误代码如下：

| 错误代码 | 含义 |
|------|---------|
| `morpheus_session_error` | 无法打开或刷新区块链会话 |
| `morpheus_inference_error` | 提供者在推理过程中返回错误 |
| `morpheus_upstream_error` | 与代理路由器的连接失败 |
| `timeout` | 请求超时 |
| `model_not_found` | 请求的模型不存在 |

#### 解决方案2：自动会话重试

当代理路由器返回与会话相关的错误（例如会话过期、无效或未找到模型）时，代理会：
1. **使缓存的会话失效**。
2. **打开一个新的区块链会话**。
3. **重新尝试推理请求**。

#### 处理代理重启后的情况

#### 1. **安全启动（使用1Password）**

代理路由器需要您的钱包私钥。**请勿将私钥存储在磁盘上**。请在运行时通过1Password注入私钥：

```bash
bash skills/everclaw/scripts/start.sh
```

或者您也可以手动设置私钥：

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

### 检查代理路由器的运行状态

等待几秒钟，然后检查代理路由器的运行状态：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/healthcheck
```

预期响应：HTTP 200。

### 停止代理路由器

```bash
bash skills/everclaw/scripts/stop.sh
```

或者您也可以使用`pkill -f proxy-router`命令停止代理路由器。

---

## 40. 开启会话前需要批准Diamond合约

在开启会话之前，需要批准Diamond合约以代表您转移MOR代币：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/approve?spender=0x6aBE1d282f72B474E54527D93b979A4f64d3030a&amount=1000000000000000000000"
```

### 注意：

**/blockchain/approve`端点使用查询参数，而不是JSON请求体。**`amount`参数以wei为单位（1000000000000000000 = 1 MOR代币）。请批准较大的金额，以避免频繁重新授权。

---

## 41. 根据模型ID开启会话

通过模型ID开启会话（而不是通过bid ID）：

```bash
MODEL_ID="0xb487ee62516981f533d9164a0a3dcca836b06144506ad47a5c024a7a2a33fc58"

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/models/${MODEL_ID}/session" \
  -H "Content-Type: application/json" \
  -d '{"sessionDuration": 3600}'
```

### 注意：

**始终使用模型ID端点**，而不是bid ID。使用bid ID会导致“dial tcp: missing address”错误。

### 会话时长

会话时长以秒为单位：
- 3600秒 = 1小时
- 86400秒 = 1天

开启会话需要执行两次区块链交易：一次用于批准转账，一次用于开启会话。
会话期间，MOR代币会被锁定。
会话结束后，MOR代币会被返还到您的钱包。

### 响应

响应中会包含一个`sessionId`（十六进制字符串）。请保存这个字符串，因为它用于后续的推理请求。

### 使用脚本

```bash
# Open a 1-hour session for kimi-k2.5:web
bash skills/everclaw/scripts/session.sh open kimi-k2.5:web 3600

# List active sessions
bash skills/everclaw/scripts/session.sh list

# Close a session
bash skills/everclaw/scripts/session.sh close 0xSESSION_ID_HERE
```

---

## 42. 发送推理请求

### 注意：

**重要提示：**`session_id`和`model_id`属于HTTP请求头信息，而不是请求体内容。这是最常见的错误来源。

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

---

## 43. 使用聊天脚本

```bash
bash skills/everclaw/scripts/chat.sh kimi-k2.5:web "What is the meaning of life?"
```

### 流式传输

在请求体中设置`"stream": true`。响应将以Server-Sent Events (SSE)格式返回。

---

## 44. 关闭会话

关闭会话以释放锁定的MOR代币：

```bash
curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/sessions/0xSESSION_ID/close"
```

或者您也可以使用相应的脚本来关闭会话：

```bash
bash skills/everclaw/scripts/session.sh close 0xSESSION_ID
```

### 注意：

会话结束后，锁定的MOR代币会被返还到您的钱包。请关闭不需要的会话，以便释放出更多的MOR代币用于新的会话。

---

## 45. 会话管理

### 会话是临时性的

### 注意：

**会话在路由器重启后不会被保留**。如果重启代理路由器，您需要重新开启会话。虽然区块链上的会话仍然存在，但路由器的内存状态会丢失。

### 监控

```bash
# Check balance (MOR + ETH)
bash skills/everclaw/scripts/balance.sh

# List sessions
bash skills/everclaw/scripts/session.sh list
```

### 会话生命周期

1. **开启会话** → MOR代币被锁定，会话处于活动状态。
2. **活动状态** → 使用`session_id`请求头发送推理请求。
3. **会话过期** → 会话时长结束，MOR代币自动返还。
4. **关闭会话** → 手动关闭会话，MOR代币立即返还。

### 重启后重新开启会话

重启路由器后，请按照以下步骤操作：

```bash
# Wait for health check
sleep 5

# Re-open sessions for models you need
bash skills/everclaw/scripts/session.sh open kimi-k2.5:web 3600
```

---

## 46. 检查余额

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

## 47. 故障排除

详情请参阅`references/troubleshooting.md`。常见故障及解决方法如下：

| 错误 | 解决方法 |
|-------|-----|
| `session not found` | 使用`session_id/model_id`作为HTTP请求头信息，而不是请求体内容 |
| `dial tcp: missing address` | 使用模型ID开启会话 |
| `api adapter not found` | 将模型添加到`models-config.json`文件中 |
| `ERC20: transfer amount exceeds balance` | 关闭旧的会话以释放锁定的MOR代币 |
| 会话在重启后消失** | 正常现象——重启后重新开启会话 |
| MorpheusUI与代理路由器同时运行** | 请勿同时运行MorpheusUI和代理路由器 |

---

## 48. 主要合约地址（Base主网）

| 合约 | 地址 |
|----------|---------|
| Diamond | `0x6aBE1d282f72B474E54527D93b979A4f64d3030a` |
| MOR Token | `0x7431aDa8a591C955a994a21710752ef9b882b8e3` |

## 快速参考

| 功能 | 命令 |
|--------|---------|
| 安装 | `bash skills/everclaw/scripts/install.sh` |
| 启动 | `bash skills/everclaw/scripts/start.sh` |
| 停止 | `bash skills/everclaw/scripts/stop.sh` |
| 交换ETH为MOR | `bash skills/everclaw/scripts/swap.sh eth 0.01` |
| 交换USDC为MOR | `bash skills/everclaw/scripts/swap.sh usdc 50` |
| 开启会话 | `bash skills/everclaw/scripts/session.sh open <model> [duration]` |
| 关闭会话 | `bash skills/everclaw/scripts/session.sh close <session_id>` |
| 列出会话 | `bash skills/everclaw/scripts/session.sh list` |
| 发送提示 | `bash skills/everclaw/scripts/chat.sh <model> "prompt"` |
| 检查余额 | `bash skills/everclaw/scripts/balance.sh` |

---

## 49. 钱包管理（v0.4）

Everclaw v0.4版本包含了一个独立的钱包管理器，无需依赖任何外部服务。无需1Password、Foundry或Safe Wallet，只需macOS Keychain和Node.js（已随OpenClaw一起提供）。

### 设置（一键完成）

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs setup
```

该命令会生成一个新的以太坊钱包，并将私钥存储在您的macOS Keychain中（加密存储，受登录密码/Touch ID保护）。

### 导入现有私钥

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs import-key 0xYOUR_PRIVATE_KEY
```

### 检查余额

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs balance
```

该命令可以显示ETH、MOR和USDC的余额，以及用于Diamond合约的MOR代币余额。

### 交换ETH/USDC为MOR

```bash
# Swap 0.05 ETH for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap eth 0.05

# Swap 50 USDC for MOR
node skills/everclaw/scripts/everclaw-wallet.mjs swap usdc 50
```

该命令会通过Uniswap V3在Base平台上执行代币交换。无需任何外部工具，使用的内置工具为viem（随OpenClaw一起提供）。

### 批准MOR代币用于质押

```bash
node skills/everclaw/scripts/everclaw-wallet.mjs approve
```

该命令用于批准Morpheus Diamond合约使用您的MOR代币进行会话质押。

### 安全机制

- 私钥存储在macOS Keychain中（加密存储）。
- 由您的登录密码/Touch ID保护。
- 私钥仅在运行时注入，使用完毕后立即从环境中清除。
- 私钥永远不会以明文形式存储在磁盘上。
- 对于高级用户，支持使用1Password作为备用方案（向下兼容）。

### 完整命令参考

| 命令 | 说明 |
|---------|-------------|
| `setup` | 生成钱包并存储在Keychain中 |
| `address` | 显示钱包地址 |
| `balance` | 显示ETH、MOR和USDC的余额 |
| `swap eth <amount>` | 通过Uniswap V3交换ETH为MOR |
| `swap usdc <amount>` | 通过Uniswap V3交换USDC为MOR |
| `approve [amount] | 批准使用MOR代币进行质押 |
| `export-key` | 打印私钥（请谨慎使用） |
| `import-key <0xkey` | 导入现有的私钥 |

---

## 50. OpenAI兼容代理（v0.2）

Morpheus代理路由器需要自定义认证（使用`.cookie`进行基本认证）和自定义HTTP请求头（`session_id`、`model_id`），这些在标准OpenAI客户端中不可用。Everclaw提供了一个轻量级的代理来解决这个问题。

### 功能介绍

```
OpenClaw/any client → morpheus-proxy (port 8083) → proxy-router (port 8082) → Morpheus P2P → Provider
```

- 接受标准的OpenAI `/v1/chat/completions`请求。
- 根据需求自动开启区块链会话（无需手动管理会话）。
- 在会话到期前自动续订（默认为1小时前）。
- 自动注入基本认证信息和`session_id`/`model_id`请求头。
- 提供 `/health`、`/v1/models`、`/v1/chat/completions`等接口。

### 安装步骤

```bash
bash skills/everclaw/scripts/install-proxy.sh
```

安装步骤如下：
- 将`morpheus-proxy.mjs`文件解压到`~/morpheus/proxy/`目录。
- 将`gateway-guardian.sh`文件添加到`~/.openclaw/workspace/scripts/`目录。
- 在macOS系统中，使用`launchd`服务使代理路由器在系统启动时自动运行。

### 配置

以下环境变量为可选设置（默认值合理）：

| 变量 | 默认值 | 说明 |
|----------|---------|-------------|
| MORPHEUS_PROXY_PORT` | `8083` | 代理路由器监听的端口 |
| MORPHEUS_ROUTER_URL` | `http://localhost:8082` | 代理路由器地址 |
| MORPHEUS COOKIE_PATH` | `~/morpheus/.cookie` | 认证cookie的存储路径 |
| MORPHEUS_SESSION_DURATION` | `604800`（7天） | 会话持续时间（秒） |
| MORPHEUS_RENEW_BEFORE` | `3600`（1小时） | 会话续订间隔（秒） |
| MORPHEUS_PROXY_API_KEY` | `morpheus-local` | 代理认证所需的bearer令牌 |

### 会话时长

会话期间，MOR代币会被锁定。会话持续时间越长，锁定的MOR代币越多，但区块链交易次数越少：

| 会话时长 | 锁定的MOR代币数量 | 交易次数 |
|----------|--------------------:|:-------------|
| 1小时 | ~11 MOR | 每小时 |
| 1天 | ~274 MOR | 每天 |
| 7天 | ~1,915 MOR | 每周 |

会话结束后或过期时，MOR代币会被返还。代理会在会话到期前自动续订，从而实现连续的推理服务，同时降低质押成本。

### 健康检查

```bash
curl http://127.0.0.1:8083/health
```

### 可用的模型

```bash
curl http://127.0.0.1:8083/v1/models
```

### 直接使用（无需OpenClaw）

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

### 可靠性说明

- **`kimi-k2.5`（非Web版本）是最可靠的模型，建议作为首选备用模型。
- **`kimi-k2.5:web`（Web搜索版本）在P2P路由时容易超时，不推荐作为备用模型。
- 提供者连接可能会暂时中断，但通常可以重试。
- 代理本身作为一个KeepAlive服务运行，如果崩溃会自动重启。

### 代理的容错性（v0.5）

v0.5版本对代理进行了三项关键改进，以防止因**冷却机制连锁反应**导致的长时间中断：

#### 问题：冷却机制连锁反应

当主要提供者（例如venice）返回错误时，OpenClaw的故障转移机制会将该提供者标记为“处于冷却状态”。如果Morpheus代理也返回错误（OpenClaw可能将其误判为计费错误），**两个提供者都会进入冷却状态**，导致代理完全离线（有时会持续6小时以上）。

#### 解决方案1：OpenAI兼容的错误编码

现在代理返回的错误信息符合OpenAI的格式，包含`type`和`code`字段：

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

**关键区别：**所有Morpheus相关的错误都会被标记为`"server_error"`，而不会被标记为`"billing"`或`"rate_limit_error"`。这样OpenClaw会将其视为临时故障并适当重试，而不会将提供者置于长时间冷却状态。

代理返回的错误代码如下：

| 错误代码 | 含义 |
|------|---------|
| `morpheus_session_error` | 无法打开或刷新区块链会话 |
| `morpheus_inference_error` | 提供者在推理过程中返回错误 |
| `morpheus_upstream_error` | 与代理路由器的连接失败 |
| `timeout` | 请求超时 |
| `model_not_found` | 请求的模型不存在 |

#### 解决方案2：自动会话重试

当代理路由器返回与会话相关的错误（例如会话过期、无效或未找到模型）时，代理会：
1. **使缓存的会话失效**。
2. **打开一个新的区块链会话**。
3. **重新尝试推理请求**。

#### 处理代理重启后的情况

#### 1. **安全启动（使用1Password）**

代理路由器需要您的钱包私钥。**请勿将私钥存储在磁盘上**。请在运行时通过1Password注入私钥：

```bash
bash skills/everclaw/scripts/start.sh
```

或者您也可以手动设置私钥：

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

### 检查代理路由器的运行状态

等待几秒钟，然后检查代理路由器的运行状态：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)
curl -s -u "admin:$COOKIE_PASS" http://localhost:8082/healthcheck
```

预期响应：HTTP 200。

### 停止代理路由器

```bash
bash skills/everclaw/scripts/stop.sh
```

或者您也可以使用`pkill -f proxy-router`命令停止代理路由器。

---

## 51. 开启会话前需要批准Diamond合约

在开启会话之前，需要批准Diamond合约以代表您转移MOR代币：

```bash
COOKIE_PASS=$(cat ~/morpheus/.cookie | cut -d: -f2)

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/approve?spender=0x6aBE1d282f72B474E54527D93b979A4f64d3030a&amount=1000000000000000000000"
```

### 注意：

**/blockchain/approve`端点使用查询参数，而不是JSON请求体。**`amount`参数以wei为单位（1000000000000000000 = 1 MOR代币）。请批准较大的金额，以避免频繁重新授权。

---

## 52. 根据模型ID开启会话

通过模型ID开启会话（而不是通过bid ID）：

```bash
MODEL_ID="0xb487ee62516981f533d9164a0a3dcca836b06144506ad47a5c024a7a2a33fc58"

curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/models/${MODEL_ID}/session" \
  -H "Content-Type: application/json" \
  -d '{"sessionDuration": 3600}'
```

### 注意：

**始终使用模型ID端点**，而不是bid ID。使用bid ID会导致“dial tcp: missing address”错误。

### 会话时长

会话时长以秒为单位：
- 3600秒 = 1小时
- 86400秒 = 1天

开启会话需要执行两次区块链交易：一次用于批准转账，一次用于开启会话。
会话期间，MOR代币会被锁定。
会话结束后，MOR代币会被返还到您的钱包。

### 响应

响应中会包含一个`sessionId`（十六进制字符串）。请保存这个字符串，因为它用于后续的推理请求。

### 使用脚本

```bash
# Open a 1-hour session for kimi-k2.5:web
bash skills/everclaw/scripts/session.sh open kimi-k2.5:web 3600

# List active sessions
bash skills/everclaw/scripts/session.sh list

# Close a session
bash skills/everclaw/scripts/session.sh close 0xSESSION_ID_HERE
```

---

## 53. 发送推理请求

### 注意：

**重要提示：**`session_id`和`model_id`属于HTTP请求头信息，而不是请求体内容。这是最常见的错误来源。

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

---

## 54. 使用聊天脚本

```bash
bash skills/everclaw/scripts/chat.sh kimi-k2.5:web "What is the meaning of life?"
```

### 流式传输

在请求体中设置`"stream": true`。响应将以Server-Sent Events (SSE)格式返回。

---

## 55. 关闭会话

关闭会话以释放锁定的MOR代币：

```bash
curl -s -u "admin:$COOKIE_PASS" -X POST \
  "http://localhost:8082/blockchain/sessions/0xSESSION_ID/close"
```

或者您也可以使用相应的脚本来关闭会话：

```bash
bash skills/everclaw/scripts/session.sh close 0xSESSION_ID
```

### 注意：

会话结束后，锁定的MOR代币会被返还到您的钱包。请关闭不需要的会话，以便释放出更多的MOR代币用于新的会话。

---

## 56. 会话管理

### 会话是临时性的

### 注意：

**会话在路由器重启后不会被保留**。如果重启代理路由器，您需要重新开启会话。虽然区块链上的会话仍然存在，但路由器的内存状态会丢失。

### 监控

```bash
# Check balance (MOR + ETH)
bash skills/everclaw/scripts/balance.sh

# List sessions
bash skills/everclaw/scripts/session.sh list
```

### 会话生命周期

1. **开启会话** → MOR代币被锁定，会话处于活动状态。
2. **活动状态** → 使用`session_id`请求头发送推理请求。
3. **会话过期** → 会话时长结束，MOR代币自动返还。
4. **关闭会话** → 手动关闭会话，MOR代币立即返还。

### 重启后重新开启会话

重启路由器后，请按照以下步骤操作：

```bash
# Wait for health check
sleep 5

# Re-open sessions for models you need
bash skills/everclaw/scripts/session.sh open kimi-k2.5:web 3600
```

---

## 57. 检查余额

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

## 58. 故障排除

详情请参阅`references/troubleshooting.md`。常见故障及解决方法如下：

| 错误 | 解决方法 |
|-------|-----|
| `session not found` | 使用`session_id/model_id`作为HTTP请求头信息，而不是请求体内容 |
| `dial tcp: missing address` | 使用模型ID开启会话 |
| `api adapter not found` | 将模型添加到`models-config.json`文件中 |
| `ERC20: transfer amount exceeds balance` | 关闭旧的会话以释放锁定的MOR代币 |
| 会话在重启后消失** | 正常现象——重启后重新开启会话 |

---

## 59. x402支付客户端（v0.7）

Everclaw v0.7版本包含了一个x402支付客户端，允许您的代理向任何支持x402协议的端点发送USDC支付。[x402协议](https://x402.org)是一种基于HTTP的支付协议：当服务器返回HTTP 402状态码时，您的代理会自动签名支付请求并尝试完成支付。

### x402的工作原理

```
Agent → request → Server returns 402 + PAYMENT-REQUIRED header
Agent → parse requirements → sign EIP-712 payment → retry with PAYMENT-SIGNATURE header
Server → verify signature via facilitator → settle USDC → return resource
```

### 使用CLI命令

```bash
# Make a request to an x402-protected endpoint
node scripts/x402-client.mjs GET https://api.example.com/data

# Dry-run: see what would be paid without signing
node scripts/x402-client.mjs --dry-run GET https://api.example.com/data

# Set max payment per request
node scripts/x402-client.mjs --max-amount 0.50 GET https://api.example.com/data

# POST with body
node scripts/x402-client.mjs POST https://api.example.com/task '{"prompt":"hello"}'

# Check daily spending
node scripts/x402-client.mjs --budget
```

### 使用编程方式

```javascript
import { makePayableRequest, createX402Client } from './scripts/x402-client.mjs';

// One-shot request
const result = await makePayableRequest("https://api.example.com/data");
// result.paid → true if 402 was handled
// result.amount → "$0.010000" (USDC)
// result.body → response content

// Reusable client with budget limits
const client = createX402Client({
  maxPerRequest: 0.50,  // $0.50 USDC max per request
  dailyLimit: 5.00,     // $5.00 USDC per day
  dryRun: false,
});

const res = await client.get("https://agent-api.example.com/query?q=weather");
const data = await client.post("https://agent-api.example.com/task", { prompt: "hello" });

// Check spending
console.log(client.budget());
// { date: "2026-02-11", spent: "$0.520000", remaining: "$4.480000", limit: "$5.000000", transactions: 3 }
```

### 支付流程

1. **发送请求** — 向任何URL发送标准HTTP请求。
2. **检测x402状态码** — 服务器返回`HTTP 402`状态码，并在请求头中包含`PAYMENT-REQUIRED`字段，其中包含支付详情。
3. **检查预算** — 根据每次请求的最大限额（默认为1.00美元）和每日限额（默认为10.00美元）进行验证。
4. **使用EIP-712签名** — 使用代理的钱包签署`TransferWithAuthorization`（EIP-3009）支付请求。
5. **发送请求** — 服务器收到请求后，会验证签名并完成支付。
6. **响应** — 服务器返回请求的资源。

### 安全性

- **私钥在运行时从1Password获取**（从未存储在磁盘上）——遵循Bag