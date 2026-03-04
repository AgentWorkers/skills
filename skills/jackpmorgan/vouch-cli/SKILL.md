---
name: vouch-cli
description: >
  使用 Vouch CLI 在 Base 平台上为 AI 代理生成、验证和管理加密身份信息。适用于以下场景：  
  - 代理需要设置身份并注册账户；  
  - 通过 X、GitHub 或 DNS 将社交身份信息与代理身份关联；  
  - 使用 EIP-712 封装对出站消息进行加密签名；  
  - 根据链上身份记录验证传入的已签名消息；  
  - 将经过验证的消息发送给其他代理；  
  - 接收并处理传入的已验证消息；  
  - 构建、测试和部署基于 OpenAI 的代理；  
  - 按身份或能力查询代理信息；  
  - 管理运行时密钥委托和信任白名单；  
  - 管理账户使用情况、API 密钥及计费信息；  
  - 将代理的 API 端点发布到链上目录。
  Signs, verifies, and manages cryptographic identity for AI agents using the
  Vouch CLI on Base. Use when an agent needs to: set up identity and register
  an account; link social identities via X, GitHub, or DNS; cryptographically
  sign outbound messages with EIP-712 envelopes; verify inbound signed messages
  against onchain identity records; send verified messages to other agents;
  receive and process incoming verified messages; scaffold, test, and deploy
  OpenAI-powered agents; look up agents by identity or capability; manage
  runtime key delegations and trust allowlists; manage account usage, API keys,
  and billing; or publish agent endpoints to the onchain directory.
compatibility: Requires the vouch binary on PATH and jq for JSON processing
allowed-tools: Bash(vouch:*) Bash(jq:*)
metadata:
  author: vouch
  version: "1.0.0"
---
# Vouch CLI

Vouch 为基于 Base 的 AI 代理提供可验证的身份认证服务。代理可以创建一个身份钱包，将社交账户（如 X 或 GitHub）与 API 账户关联起来（可选），并链接其他身份验证方式（包括 DNS），同时可以委托使用期限有限的运行时密钥。所有消息都会被封装成 EIP-712 格式的签名包，并通过直接调用 VouchHub 智能合约进行验证。

```
Account (OAuth + API key) ──manages──> Wallet (identity)
                                            │
       ┌────────────────────────────────────┤
       ▼                                    ▼
  Linked Identities                  Runtime Key (delegated, scoped)
  (X, GitHub, DNS)                         │
                                           └──sign──> Envelope (EIP-712)
                                                           │
                              Recipient ──verify──> VouchHub (RPC)
                                                           │
                                                    ✓ signer → wallet → linked identities
```

## 安装

```bash
curl -fsSL https://vouch.directory/install.sh | bash
```

验证安装结果：`vouch --version`

## 全局参数

- `--json` — 以 JSON 格式输出结果（通过 pip 运行时会自动启用）
- `--config <path>` — 配置文件路径（默认为 `~/.vouch/config.toml`）
- `--network <base-sepolia|base>` — 更改网络配置

## 新用户入门流程

### 完整的设置向导

使用 `vouch init` 可以完成以下步骤：生成钱包、连接社交账户（X 或 GitHub）以创建 API 账户并关联身份信息，最后委托运行时密钥。

```bash
vouch init
```

设置流程：
1. **生成钱包** — 在本地 `~/.vouch/keys/` 目录下生成新的身份密钥对。
2. **保存配置** — 将配置信息写入 `~/.vouch/config.toml` 文件。
3. **连接账户** — 通过浏览器进行 X 或 GitHub 的 OAuth 验证，创建 API 账户并关联链上身份。
4. **委托运行时密钥** — 为代理生成一个有效期为 24 小时的签名密钥。

重新初始化现有设置：

```bash
vouch init --force
```

这是推荐的初始命令，它可以完成启动消息签名和验证所需的所有操作。

### 在新机器上登录

如果已有 API 密钥，可以使用以下命令进行登录：

```bash
vouch login --api-key vk_...
```

**参数：** `--api-key <vk_...>`（必需）。执行此命令前会先验证 API 密钥的有效性。

## 关联身份验证方式

Vouch 支持三种身份验证方式：每种方式都可以将社交账户或域名与链上钱包关联起来。

### 关联 X（Twitter）账户

**交互模式**：会打开浏览器进行 OAuth 验证。

**脚本模式**：

**参数：** `--wallet-key <hex>`, `--attestation <json>`

### 关联 GitHub 账户

**交互模式**：会打开浏览器进行 OAuth 验证。

**脚本模式**：

**参数：** `--wallet-key <hex>`, `--attestation <json>`

### 通过 DNS 关联域名

需要先使用 `vouch init` 创建 API 账户，因为仅凭 DNS 无法验证用户身份。关联域名时，系统会要求用户提供 DNS 挑战信息并显示需要添加的 TXT 记录，之后进行验证。

**交互模式**：

**参数：** `--wallet-key <hex>`, `--domain <domain>`

### 撤销已关联的身份验证方式

**参数：** `--wallet-key <hex>`（必需），`--provider <x|github|dns>`（必需）

## 签署出站消息

将任何 JSON 格式的消息内容封装成 EIP-712 格式的签名包：

**脚本模式**：

**参数：** `--payload '<json>'`（或通过 stdin 传递消息内容），`--key <address>`，`--scope <text>`，`--expiry <duration>`（签名有效期）

## 验证入站消息

系统会检查消息的签名、有效期、随机数、消息内容哈希值、委托状态以及是否在允许的发送列表中：

**脚本模式**：

**参数：** `--envelope '<json>'`（签名包格式），`--url <endpoint>`（验证目标端点），`--skip-allowlist`（是否跳过允许列表检查）

## 发送已验证的消息

将签名后的消息通过 POST 请求发送到其他代理的端点：

**脚本模式**：

**参数：** `--payload '<json>'`（或通过 stdin 传递消息内容），`--url <endpoint>`（目标端点地址），`--key <address>`（可选），`--scope <text>`（消息权限范围），`--expiry <duration>`（签名有效期，默认为 1 小时）

## 接收已验证的消息

运行一个 HTTP 服务器来接收、验证并处理签名后的消息：

**脚本模式**：
- 服务器监听 `/vouch` 和 `/` 端口（仅接受 POST 请求）。
- 在接收消息前会对消息进行加密验证。
- 处理器的输出结果会以 JSON 格式返回；如果没有指定处理器，验证通过的消息会直接以换行符分隔的形式输出到标准输出。

**响应格式：**

**参数：** `--port <int>`（默认端口 8080），`--handler <script>`（处理程序脚本），`--allowlist`（允许的发送列表），`--rate-limit <float>`（每 IP 的请求限制次数，默认为无限）

## 代理开发框架

可以使用 Vouch 框架创建、运行和部署基于 OpenAI 的代理程序。

### 创建代理

提供交互式向导，帮助用户生成可部署的代理项目：

**参数：** 代理名称、描述、编程语言（Node.js 或 Python）、使用的 OpenAI API 密钥以及端口号。项目会保存在 `~/.vouch/agents/<name/>` 目录下。

### 在本地运行代理

**参数：** 使用 `vouch receive` 命令启动代理，指定代理的处理程序和端口号。代理会接收并处理已验证的消息，并使用配置的 OpenAI 模型进行处理。

### 部署到 Vercel 服务器

**参数：** 需要安装 Vercel CLI（`npm i -g vercel`）。部署完成后会显示代理的实时端点地址。使用 `--prod` 参数可进行生产环境部署（默认为预览模式）。

部署完成后，需要将代理的端点发布到指定的目录：

**参数：** ...

## 查看身份信息和代理列表

**参数：** ...

## 查看当前使用的身份验证方式

**参数：** ...

## 管理密钥委托

**参数：** 创建新的运行时密钥委托；续订现有委托时保持原有设置。

**参数：** ...

**限制：** 每分钟最多只能委托 5 次，每次委托的有效期为 30 天。

**参数：** 撤销特定密钥时需要提供密钥地址和有效期。

## 在链上注册代理的端点和功能

**参数：** ...

## 管理允许的发送列表

**参数：** 当允许列表生效时，`vouch verify` 和 `vouch receive --allowlist` 仅接受来自列表中允许的代理的消息。

## 账户管理和计费

**参数：** 查看账户使用情况。

**参数：** ...

## 查看 API 密钥列表

**参数：** ...

## 查看计费状态

**参数：** ...

## 计费方式说明

| 功能          | 免费          | 付费（按使用量计费）        |
|----------------|------------------|----------------------|
| 验证请求        | 无限次数        | 免费                |
| 中继交易        | 每月 10 次       | 每次 0.05 美元           |
更多计费详情请访问：https://vouch_directory/dashboard/billing 或通过控制台进行升级。

## 全新代理的设置流程

**参数：** ...

**发送消息后进行签名验证的完整流程：**

**参数：** ...

**向其他代理发送已验证的消息：**

**参数：** ...

**代理之间的消息交互：**

**参数：** ...

**创建、测试并部署代理：**

**参数：** ...

**为代理配置允许列表和请求限制：**

**参数：** ...

**在批量操作前检查使用情况：**

**参数：** ...

**按功能查找代理：**

**参数：** ...

**设置完成后关联额外的身份验证方式：**

**参数：** ...

**在流程中完成签名、发送和验证操作：**

**参数：** ...

## 重置当前配置**

**参数：** 可以撤销当前的链上身份信息并重新开始设置。交互模式下需要通过浏览器进行 OAuth 验证；脚本模式下可跳过链上身份的撤销操作。

**参数：** ...

**仅用于脚本模式（仅用于重置操作）：** ...

**参数：** `--wallet-key <hex>`（启用脚本模式），`--force`（跳过链上身份撤销操作）。

**彻底销毁代理配置：**

**参数：** 撤销链上身份信息并清除所有本地数据。

**参数：** （仅用于脚本模式）