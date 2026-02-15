---
name: 8004-agent
version: 0.0.1
description: >
  8004 Agent Skill for registering AI agents on the ERC-8004 Trustless Agents
  standard and authenticating them via SIWA (Sign In With Agent). Use this skill when an agent
  needs to: (1) create or manage an Ethereum wallet for onchain identity, (2) register on the
  ERC-8004 Identity Registry as an NFT-based agent identity (SIGN UP), (3) authenticate with a
  server by proving ownership of an ERC-8004 identity using a signed challenge (SIGN IN / SIWA),
  (4) build or update an ERC-8004 registration file (metadata JSON with endpoints, trust models,
  services), (5) upload agent metadata to IPFS or base64 data URI, (6) look up or verify an
  agent's onchain registration. The agent persists public identity state in MEMORY.md. Private
  keys are held in a separate keyring proxy server — the agent can request signatures but never
  access the key itself.
  Triggers on: ERC-8004, trustless agents, agent registration, SIWA, Sign In With Agent,
  agent identity NFT, Agent0 SDK, agent wallet, agent keystore, keyring proxy.
---

# 8004代理技能 v0.0.1

在链上注册AI代理（使用ERC-8004标准），并通过**SIWA（使用代理登录）**进行身份验证。

## 概述

ERC-8004（“无信任代理”）提供了三个作为链上单例部署的注册表：

- **身份注册表** — 使用ERC-721 NFT。每个代理都会获得一个唯一的`agentId`（tokenId）和一个指向JSON注册文件的`agentURI`。
- **声誉注册表** — 客户向代理提供的反馈信号（分数、标签）。
- **验证注册表** — 第三方验证器的证明（zkML、TEE、质押重执行）。

**SIWA（使用代理登录）**是一种基于挑战-响应的身份验证协议（灵感来自SIWE / EIP-4361），代理通过签署结构化消息来证明其对ERC-8004身份的所有权。详情请参见[references/siwa-spec.md](references/siwa-spec.md)。

---

## 安全架构

> **详细信息**：[references/security-model.md](references/security-model.md)

代理的私钥是其链上身份的根基。必须防止私钥被注入、意外暴露或被文件系统窥探。

### 原理：私钥永远不会进入代理进程

所有的签名操作都委托给**keyring代理服务器**——这是一个单独的进程，它保存加密后的私钥，并仅暴露经过HMAC验证的签名接口。代理可以请求签名，但在任何情况下（即使是通过注入代码完全控制）也无法提取私钥。

**为什么这很安全：**

| 属性 | 详情 |
|---|---|
| **密钥隔离** | 私钥存储在单独的操作系统进程中；永远不会进入代理内存 |
| **传输认证** | 使用HMAC-SHA256对方法、路径、请求体和时间戳进行加密；30秒的重放窗口 |
| **审计追踪** | 每个签名请求都会记录时间戳、接口、源IP以及成功/失败状态 |
| **攻击限制** | 即使代理被完全控制，也只能请求签名——无法提取私钥 |

**环境变量：**

| 变量 | 使用者 | 用途 |
|---|---|---|
| `KEYRING_PROXY_URL` | 代理 | 代理服务器URL（私有地址，例如`http://keyring-proxy:3100`）或公共地址 |
| `KEYRING_PROXY_SECRET` | 代理和客户端 | 共享的HMAC密钥 |
| `KEYRING_PROXY_PORT` | 代理服务器 | 监听端口（默认：3100） |
| `AGENT_PRIVATE_KEY` | 代理服务器 | 十六进制编码的私钥（0x...）——建议使用现有的钱包而不是重新生成 |
| `KEYSTORE_PASSWORD` | 代理服务器 | 加密文件密钥库的密码（如果使用了`AGENT_PRIVATE_KEY`则不需要） |

> **自动检测**：当设置了`KEYRING_PROXY_URL`时，`KEYSTORE_BACKEND`会自动设置为`proxy`——无需手动设置。当在代理服务器上设置了`AGENT_PRIVATE_KEY`时，`KEYSTORE_BACKEND`会自动设置为`env`。

> 代理服务器默认使用AES加密的V3 JSON密钥库（scrypt KDF）来存储密钥。如果想使用现有的钱包，可以在代理服务器上设置`AGENT_PRIVATE_KEY`——此时密钥将存储在内存中（无需加密文件）。

### 密钥库API

`@buildersgarden/siwa/keystore`模块仅提供以下操作——这些操作都不会返回私钥：

`getSigner()`在代理后端是不可用的——请使用`signMessage()`或`signTransaction()`代替。

### 重要提示：安装并使用SDK

代理必须使用`@buildersgarden/siwa` SDK与keyring代理进行交互。SDK会自动处理HMAC认证。

**步骤1 — 安装SDK**（如果环境中还没有安装）：

**步骤2 — 设置环境变量：**

**步骤3 — 使用SDK函数**（切勿直接调用代理的HTTP接口）：

SDK会从环境变量中读取`KEYRING_PROXY_URL`和`KEYRING_PROXY_SECRET`，并自动构建正确的HMAC头部。

### 备用方案：手动HMAC认证（不使用SDK）

如果你绝对无法安装SDK（例如在非Node.js环境中，或者运行环境有限制），你可以使用下面描述的HMAC协议直接调用代理的HTTP接口。**尽可能使用SDK**。

**每个请求都必须包含的头部字段**（`GET /health`除外）：

| 字段 | 值 |
|---|---|
| `Content-Type` | `application/json` |
| `X-Keyring-Timestamp` | 当前时间（以Unix时间戳的毫秒形式） |
| `X-Keyring-Signature` | 请求体的HMAC-SHA256十六进制摘要 |

**HMAC请求体格式** — 一个由换行符（`\n`）分隔的四个部分组成的字符串：

**计算签名：**

**时间戳限制：** 如果时间戳与服务器时间相差超过**30秒**，服务器将拒绝请求。

**示例 — 在没有SDK的情况下创建钱包（使用Node.js）：**

**示例 — 在Python中创建钱包：**

**可用的接口：**

| 接口 | 请求体 | 响应 |
|---|---|---|
| `POST /create-wallet` | `{}` | `{ address, backend }` |
| `POST /has-wallet` | `{}` | `{ hasWallet: boolean }` |
| `POST /get-address` | `{}` | `{ address }` |
| `POST /sign-message` | `{ message: string }` | `{ signature, address }` |
| `POST /sign-transaction` | `{ tx: { to, data, nonce, chainId, type, maxFeePerGas, ... } }` | `{ signedTx, address }` |
| `POST /sign-authorization` | `{ auth: { chainId, address, nonce } }` | `{ signedAuthorization }` |
| `GET /health` | — | `{ status: "ok", backend }`（无需认证） |

### MEMORY.md：仅存储公共数据

MEMORY.md仅存储代理的公共身份信息——**绝不存储私钥**：

**生命周期规则：**

1. **在任何操作之前** — 首先读取MEMORY.md。如果钱包已经存在，则跳过创建步骤；如果已经注册，则跳过重新注册步骤。
2. **创建钱包后** — 将地址和后端信息写入MEMORY.md。私钥仅存储在代理的密钥库中。
3. **注册完成后** — 将`agentId`、`agentRegistry`、`agentURI`和`chainId`写入MEMORY.md。
4. **通过SIWA登录后** — 将会话令牌添加到`Sessions`部分。

**模板**：[assets/MEMORY.md.template](assets/MEMORY.md.template)

---

## 部署keyring代理

在签署任何内容之前，代理需要一个正在运行的**keyring代理**——这个单独的进程负责保存私钥并执行所有加密操作。

### 选项A — Railway（推荐）

使用Railway模板一键部署：

[![在Railway上部署](https://railway.com/button.svg)](https://railway.com/deploy/siwa-keyring-proxy?referralCode=ZUrs1W)

这会部署一个基于`packages/keyring-proxy/Dockerfile`构建的`keyring-proxy`服务。在Railway中设置以下环境变量：

| 变量 | 是否必需 | 说明 |
|---|---|---|
| `KEYRING_PROXY_SECRET` | 是 | 共享的HMAC-SHA256密钥。必须与你的代理匹配。 |
| `KEYSTORE_PASSWORD` | 可选 | 加密文件密钥库的密码（默认后端） |
| `AGENT_PRIVATE_KEY` | 可选 | 十六进制编码的私钥（0x...），用于使用现有的钱包 |

部署完成后，记录代理的URL（例如`https://your-keyring-proxy.up.railway.app`），并将其设置为代理的`KEYRING_PROXY_URL`。

> 完整的部署指南，包括架构细节、OpenClaw网关设置和验证步骤：[https://siwabuilders.garden/docs/deploy](https://siwabuilders.garden/docs/deploy)

### 选项B — Docker（自托管）

### 选项C — 本地开发

### 一旦代理运行起来，就在代理上设置以下环境变量：

当设置了`KEYRING_PROXY_URL`后，`proxy`密钥库的后端会自动被检测到——无需手动设置`KEYSTORE_BACKEND`。

---

## 工作流程：注册代理

### 步骤0：检查MEMORY.md和密钥库

### 步骤1：创建钱包（私钥存储在代理中，地址存储在MEMORY.md中）

### 步骤1b：为钱包充值（注册前必须完成）

**注意：**在任何链上交易之前，钱包必须有ETH作为Gas费用。**注册、URI更新和元数据更改都需要支付Gas费用。**

创建钱包后，你必须：

1. **向用户显示钱包地址和目标链**，以便他们可以发送资金：
   - 地址：通过`createWallet()`或`getAddress()`返回的地址
   - 链路：代理将注册的链（例如Base Sepolia链的ID `84532`，Base主网的ID `8453`）
2. **告诉用户向该地址发送ETH**（或该链的本地Gas代币）。
3. **等待用户确认**他们已经为钱包充值后，再继续进行注册。

对于测试网，建议使用以下 faucet：
- **Base Sepolia**：[Base Sepolia faucet](https://www.alchemy.com/faucets/base-sepolia) 或从ETH到Sepolia的桥接服务
- **ETH Sepolia**：[Sepolia faucet](https://www.alchemy.com/faucets/ethereum-sepolia)

> **在钱包充值完成之前，切勿尝试进行任何链上交易。**否则交易会因资金不足而失败。

向用户显示的示例消息：

### 步骤2：构建注册文件

按照ERC-8004规范创建一个JSON文件。可以使用[assets/registration-template.json](assets/registration-template.json)作为起点。

所需字段：`type`、`name`、`description`、`image`、`services`、`active`。

构建完成后，更新MEMORY.md中的配置文件：

### 步骤3：上传元数据

**选项A — IPFS（推荐使用Pinata）：**

**选项B — 使用Base64数据URI：**

### 步骤4：在链上注册（通过代理进行签名）

代理会构建交易并将签名操作委托给代理：

有关每个链上已部署的地址，请参阅[references/contract-addresses.md](references/contract-addresses.md)。

### 替代方案：Agent0 SDK

### 替代方案：create-8004-agent CLI

### 在执行`npm run register`后，使用输出的结果更新MEMORY.md中的`agentId`。

---

## 工作流程：登录代理（SIWA — 使用代理登录）

完整规范：[references/siwa-spec.md](references/siwa-spec.md)

### 步骤0：从MEMORY.md中读取公共身份信息

### 步骤1：从服务器请求随机数（nonce）

### 步骤2：通过代理进行签名（私钥不会被暴露）

### 步骤3：提交并保存会话信息

### SIWA消息格式

### 服务器端验证

服务器必须：

1. 从签名中恢复签名者信息（EIP-191）
2. 将恢复的地址与消息中的地址进行匹配
3. 验证域名绑定、随机数以及时间窗口的有效性
4. **在链上调用`ownerOf(agentId)`以确认签名者拥有该代理的NFT**
5. **（可选）** 根据`SIWAVerifyCriteria`评估代理的状态、所需服务、信任模型和声誉分数
6. 发放会话令牌

`@buildersgarden/siwa/siwa`中的`verifySIWA()`方法接受一个可选的`criteria`参数（第六个参数），以在验证所有权后执行额外的检查：

有关完整的实现参考，请查看测试服务器的`verifySIWARequest()`方法。

| 接口 | 方法 | 说明 |
|---|---|---|
| `/siwa/nonce` | POST | 生成并返回一个随机数 |
| `/siwa/verify` | POST | 接受`{ message, signature }`，进行验证并返回会话令牌/JWT |

---

## MEMORY.md快速参考

| 部分 | 编写时间 | 关键字段 |
|---|---|---|
| **钱包** | 注册步骤1 | 地址、密钥库后端、创建时间 |
| **注册** | 注册步骤4 | 状态、代理ID、代理注册表信息、链ID |
| **代理信息** | 注册步骤2 | 名称、描述、图片 |
| **服务** | 添加服务后 | 每项服务占一行 |
| **会话** | 每次使用SIWA登录后 | 会话令牌、域名、会话有效期 |
| **备注** | 随时可以添加 | 自由格式的注释（例如充值交易信息、使用的fountain等） |

**MEMORY.md中不包含的内容：** 私钥、密钥库密码、助记短语。

## 参考文件

- **[references/security-model.md](references/security-model.md)** — 威胁模型、密钥库架构、防止私钥被注入的防护措施 |
- **[references/siwa-spec.md](references/siwa-spec.md)** — 完整的SIWA协议规范（消息格式、字段定义、安全考虑）
- **[references/contract-addresses.md](references/contract-addresses.md)** | 每个链上已部署的注册表地址、ABI片段 |
- **[references/registration-guide.md](references/registration-guide.md)** | 详细的注册文件格式、接口类型、更新流程

## 核心库（`@buildersgarden/siwa`包）

- **`@buildersgarden/siwa/keystore`** — 提供安全的密钥存储抽象功能，并支持keyring代理 |
- **`@buildersgarden/siwa/memory` | 提供读取/写入MEMORY.md的辅助函数（仅存储公共数据） |
- **`@buildersgarden/siwa/siwa` | 负责构建SIWA消息、通过密钥库进行签名以及服务器端的验证（支持可选的验证条件） |
- **`@buildersgarden/siwa/registry` | 从链上注册表中读取代理信息（`getAgent`）和声誉信息（`getReputation`），并输出ERC-8004格式的值：`ServiceType`、`TrustModel`、`ReputationTag` |
- **`@buildersgarden/siwa/proxy-auth` | 为keyring代理提供HMAC-SHA256认证功能 |

## 资源文件

- **[assets/MEMORY.md.template](assets/MEMORY.md.template)** — 代理的公共身份信息存储文件的模板 |
- **[assets/registration-template.json](assets/registration-template.json)** — 注册文件的模板