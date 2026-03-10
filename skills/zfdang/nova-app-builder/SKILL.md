---
name: nova-app-builder
description: "构建并部署 Nova 平台应用程序（这些应用程序运行在 Sparsity Nova 或 sparsity.cloud 上，属于 TEE 类型）。当用户需要创建一个 Nova 应用程序、编写相应的代码、将其打包成 Docker 镜像，并部署到 Nova 平台以获取可运行的 URL 时，可以使用此流程。该流程涵盖了整个应用程序的生命周期：从项目初始化（scaffold）、代码编写、构建、推送到部署，以及运行状态的验证。相关请求包括：“为我构建一个 Nova 应用程序”、“部署到 Nova 平台”、“在 sparsity.cloud 上创建一个 TEE 应用程序”以及“我想在 Nova 上运行一个 TEE 应用程序”。"
---
# Nova 应用构建器

**端到端工作流程：** 构建框架 → 编写代码 → 推送到 Git → 创建应用 → 构建应用 → 部署 → （在链上：在链上创建应用 → 注册版本 → 生成 ZK 证明 → 注册实例）。

## 架构概述

Nova 应用运行在 AWS Nitro Enclaves 内部，由 **Enclaver**（Sparsity 版本）管理，并由 **Odyn**（Enclave 内的 PID 1）监督。关键概念包括：

- **Enclaver**：将您的 Docker 镜像打包成 EIF（Enclave Image File），并管理 Enclave 的生命周期。
- **Odyn**：Enclave 内的监督者；提供内部 API 用于签名、认证、加密、KMS、S3 等功能，并管理网络连接。
- **Nova 平台**：位于 [sparsity.cloud](https://sparsity.cloud) 的云平台 — 从 Git 中构建 EIF，运行 Enclaves，并暴露应用 URL。
- **Nova KMS**：分布式密钥管理；Enclave 应用通过 `/v1/kms/derive` 接口获取密钥。
- **Nova Python SDK**：位于 `enclave/nova_python_sdk/` 的官方 SDK — 可以通过 `from nova_python_sdk.odyn import Odyn` 进行导入。该 SDK 随 `nova-app-template` 和所有示例代码一起提供。

## 两种开发路径

| | 最小化框架 | 完整模板分支 |
|---|---|---|
| **起点** | `scripts/scaffold.py` | **从 [nova-app-template](https://github.com/sparsity-xyz/nova-app-template)` 分支 |
| **配置** | 平台 API 中的 `advanced` 字段处理所有配置 | 同样 — 在创建应用时设置 `advanced` 字段；平台会自动生成 `enclaver.yaml` |
| **是否需要 `enclaver.yaml`？** | 不需要 — 平台会自动生成 | 不需要 — 平台会根据 `advanced` 字段生成 |
| **`enclave/config.py`** | 不适用 | 应用级别的业务逻辑配置（合约地址、链 ID 等） |
| **功能** | 最小化：签名、认证、HTTP | 完整版：KMS、应用钱包、端到端加密、S3、Helios、React 用户界面、预言机 |

> ⚠️ **`enclaver.yaml` 和 `nova-build.yaml` 由 Nova 平台自动生成** — 开发者无需编写或提供这些文件。控制平面会在触发构建流程之前根据应用设置生成它们。S3 存储和 AWS 凭据完全由平台管理；开发者无需接触这些配置。

## 入门前需要准备的资料

> **在开始之前，请确保您的技能是最新的：**
> ```bash
> clawhub update nova-app-builder
> ```
> 旧版本的模板中缺少 `Dockerfile.txt`，这会导致构建失败。

- **应用思路**：您的应用具体做什么？
- **Nova 账户 + API 密钥**：在 [sparsity.cloud](https://sparsity.cloud) 注册账户 → 访问 **账户** → 然后获取 **API 密钥**。
- **GitHub 仓库 + GitHub PAT**：仅用于将您的应用代码推送到 GitHub。Nova 平台会从仓库 URL 中构建应用。PAT 不会传递给 Nova 平台。

  **GitHub PAT 设置方法：**
  1. 登录 GitHub → 设置 → 开发者设置 → 个人访问令牌 → 详细设置令牌
  2. 需要的权限：**内容**（读写）和 **元数据**（读）
  3. 使用令牌进行推送：
     ```bash
     git remote set-url origin https://oauth2:${GH_TOKEN}@github.com/<user>/<repo>.git
     git push origin main
     ```

> ⚠️ **请不要询问 Docker 注册表凭证、AWS S3 凭据或 `enclaver.yaml`。**
> Nova 平台会内部处理 Docker 构建、镜像注册表和 S3/存储配置。
> 开发者无需接触 AWS 凭据或编写 `enclaver.yaml` — 平台会根据 `advanced` 字段自动生成它。
> 应用仅通过内部 API 端点 (`/v1/s3/*`) 进行存储操作；Odyn 负责其余的逻辑处理。

## 完整工作流程

### 第 1 步 — 构建项目框架

```bash
python3 scripts/scaffold.py \
  --name <app-name> \
  --desc "<one-line description>" \
  --port <port> \
  --out <output-dir>
```

> **端口选择**：任何端口都可以。在创建应用时通过 `advanced.app_listening_port` 设置端口。该端口必须与 Dockerfile 中的 `EXPOSE` 设置相匹配。不强制使用 8080 端口。

这会生成一个结构为 `<output-dir>/<app-name>/` 的目录：
```
<app-name>/
├── Dockerfile
└── enclave/
    ├── main.py
    ├── odyn.py
    └── requirements.txt
```

> **注意**：模板中包含一个 `Dockerfile.txt` 文件（clawhub 无法分发没有扩展名的文件）。`scaffold.py` 会自动将其重命名为 `Dockerfile` 并替换端口信息。无需手动操作。

**或者，您也可以从 [nova-app-template](https://github.com/sparsity-xyz/nova-app-template)` 分支来获取完整的、适用于生产环境的结构：**
```
nova-app-template/
├── Makefile
├── Dockerfile
├── enclaver.yaml          ← reference template only; portal parses listening port from it;
│                            platform generates the real enclaver.yaml from app settings
├── enclave/
│   ├── app.py             ← entry point (not main.py)
│   ├── routes.py          ← FastAPI route handlers
│   ├── config.py          ← app business logic config (chain RPCs, contract address, etc.)
│   ├── chain.py           ← chain interaction helpers (app-specific ABI, contract reads)
│   ├── tasks.py           ← background scheduler (oracle, periodic jobs)
│   ├── nova_python_sdk/   ← canonical Nova SDK (do not modify)
│   │   ├── odyn.py        ← identity, attestation, encryption, S3, KMS/app-wallet wrappers
│   │   ├── kms_client.py  ← thin client for KMS and app-wallet request handlers
│   │   ├── rpc.py         ← shared RPC transport + environment switching
│   │   └── env.py         ← IN_ENCLAVE + endpoint resolution helpers
│   └── requirements.txt
├── frontend/              ← React/Next.js UI (served at /frontend)
└── contracts/             ← example on-chain contracts
```
功能包括：KMS、应用钱包、端到端加密、S3（KMS 加密）、Helios 双链 RPC、React 用户界面、示例合约和预言机。

### 第 2 步 — 编写应用逻辑

编辑 `enclave/main.py`（简化框架版本）或 `enclave/routes.py`（完整模板版本）。关键代码模式如下：

**最小化的 FastAPI 应用：**
```python
import os, httpx
from fastapi import FastAPI

app = FastAPI()
IN_ENCLAVE = os.getenv("IN_ENCLAVE", "false").lower() == "true"
ODYN_BASE = "http://localhost:18000" if IN_ENCLAVE else "http://odyn.sparsity.cloud:18000"

@app.get("/api/hello")
def hello():
    r = httpx.get(f"{ODYN_BASE}/v1/eth/address", timeout=10)
    return {"message": "Hello from TEE!", "enclave": r.json()["address"]}
```

> ⚠️ **`IN_ENCLAVE` 并不是由 Enclaver 自动设置的** — 这是一个应用级别的约定。在本地开发时，您需要在 Dockerfile 中设置 `ENV IN_ENCLAVE=false`；在生产环境中，平台会自动设置为 `true`。

**推荐使用 Nova Python SDK**（适用于完整模板版本；代码位于 [nova-app-template](https://github.com/sparsity-xyz/nova-app-template)）：
```python
from nova_python_sdk.odyn import Odyn
from nova_python_sdk.kms_client import NovaKmsClient

odyn = Odyn()  # auto-detects IN_ENCLAVE env var
kms = NovaKmsClient(endpoint=odyn.endpoint)

@app.get("/api/hello")
def hello():
    return {"address": odyn.eth_address(), "random": odyn.get_random_bytes().hex()}

@app.post("/api/sign")
def sign(body: dict):
    return odyn.sign_message(body["message"])

@app.post("/api/store")
def store(body: dict):
    odyn.s3_put(body["key"], body["value"].encode())
    return {"stored": True}
```

**使用应用钱包和 KMS 的情况：**
```python
from nova_python_sdk.kms_client import NovaKmsClient

kms = NovaKmsClient(endpoint=odyn.endpoint)

@app.get("/api/wallet")
def wallet():
    return kms.app_wallet_address()     # {"address": "0x...", "app_id": 0}

@app.post("/api/sign")
def sign(body: dict):
    return kms.app_wallet_sign(body["message"])   # {"signature": "0x..."}

@app.post("/api/sign-tx")
def sign_tx(body: dict):
    return kms.app_wallet_sign_tx(body)  # EIP-1559 transaction signing
```

**SDK 模块的职责：**
- `nova_python_sdk/odyn.py`：处理身份验证、认证、加密功能，以及 `/v1/kms/*` 和 `/v1/app-wallet/*` 的接口。
- `nova_python_sdk/kms_client.py`：作为 KMS 和应用钱包操作的轻量级客户端。
- `nova_python_sdk/rpc.py`：提供通用的 RPC 传输机制和环境切换功能；应用特定的合约逻辑应放在 `enclave/chain.py` 中。
- `nova_python_sdk/env.py`：提供 `IN_ENCLAVE` 环境变量和端点解析的帮助功能。

**运行时端点的优先级（来自 `env.py`）：**
- Odyn API：`ODYN_API_BASE_URL` → `ODYN_ENDPOINT` → `http://127.0.0.1:18000`（当 `IN_ENCLAVE=true` 时）→ `http://odyn.sparsity.cloud:18000`（其他情况）
- 业务链 RPC：`ETHEREUM_MAINNET_RPC_URL` → `BUSINESS_chain_RPC_URL` → `http://127.0.0.1:18546`（Enclave 内部）→ `http://odyn.sparsity.cloud:18546`（其他情况）
- 认证链 RPC：`NOVA_AUTH_chain_RPC_URL` → `AUTHCHAIN_RPC_URL` → `http://127.0.0.1:18545`（Enclave 内部）→ `http://odyn.sparsity.cloud:18545`（其他情况）

**双链拓扑结构**（如模板所示）：
- **认证/注册链**：使用 Base Sepolia（端口 84532）进行 KMS 认证和应用注册。
- **业务链**：使用 Ethereum Mainnet（端口 1）执行业务逻辑。

> ⚠️ **在创建应用之前必须确定 Helios RPC 端口** — 这些端口会在 `advanced.helios_chains[]` 中设置，并在创建时固定下来。请谨慎选择端口值。

关于 Enclave 代码的规则：
- **与 Odyn 的通信（使用 `requests` 或 `httpx`）：两者都可以使用 — 因为 Odyn 是本地服务。
- **外部出站 HTTP 请求**：必须使用 `httpx`（支持代理）；不要使用 `requests` 或 `urllib`，因为它们可能会绕过出口代理。
- 持久化数据存储：使用 `/v1/s3/*` 端点（或 `odyn.s3_put()`）；Enclave 的文件系统是临时性的。
- 密钥信息：通过 KMS (`/v1/kms/derive`) 生成；切勿从环境变量或硬编码中获取。
- 本地测试：使用 `IN_ENCLAVE=false python3 app.py`（通过 `uvicorn main:app --port <port>` 启动应用）。Odyn 的调用会发送到公共模拟服务器。

**关于 `/.well-known/attestation` 路由的说明：** 在生产环境中，这个端点由 Caddy 路由到辅助 API（端口 18001）—— **不是** 由应用代码处理的。某些示例中可能在本地开发环境中使用了这个端点，但在生产环境中不应使用。

### 第 3 步 — 提交代码到 Git

您的仓库只需包含 `Dockerfile` 和应用代码。无需在本地进行 Docker 构建 — Nova 平台会直接从您的 Git 仓库中构建应用。

KMS 集成完全由平台处理 — 在创建应用时只需在 `advanced` 配置中设置 `enable_decentralized_kms: true`（可选）和 `enable_app_wallet: true`。您的代码中不需要包含合约地址、应用 ID 或手动配置 KMS 参数。

```bash
git add .
git commit -m "Initial Nova app"
git push origin main
```

### 第 4 步 — 部署到 Nova 平台

部署过程分为 **三个步骤**：**创建应用 → 触发构建 → 创建部署**。

#### 通过门户网站进行部署（推荐给初次使用者）

**门户网站流程（适用于简化框架和完整模板版本）：**

1. 访问 [sparsity.cloud](https://sparsity.cloud) → **应用** → **创建应用**。
2. 填写以下信息：
   - **应用名称**、**仓库 URL**、可选的描述、`metadata_uri`、`app_contract_addr`。
   - 配置 **高级设置**（端口、出站设置、KMS、应用钱包、S3、Helios 功能开关、链选择）。
   - 提交 → 复制 **应用 sqid**。

   > 仓库 URL 会存储在应用记录中，并用于后续的所有构建过程 — 在构建时无需再次提供。

3. 在应用页面的 **版本** 部分 → 点击 **+ 新版本**：
   - **Git 参考**：`main`（或标签/提交 SHA 值）。
   - **版本号**：例如 `1.0.0`。
   - 提交。

4. 等待构建状态变为 **成功**（平台会构建 Docker 镜像 → 生成 EIF → 生成带有 Sigstore/cosign 签名的 `build-attestation.json`）。

5. 在 **版本** 页面中找到成功的版本 → 点击 **部署此版本**：
   - 选择 **地区**。
   - 选择 **层级**：`standard` 或 `performance`。
   - 提交。

6. 等待部署状态变为 **运行中** → 复制 **应用 URL**（从应用详情中获取主机名）。

   > 部署界面不需要输入环境变量或凭据。

#### 通过 API 进行部署（脚本方式）

您可以通过脚本交互式地决定是否在链上注册应用。使用 `--onchain` 参数始终执行注册操作，使用 `--no-onchain` 参数则跳过此步骤。

```bash
# Preview config without deploying
python3 scripts/nova_deploy.py \
  --repo https://github.com/you/my-app \
  --name "my-app" \
  --port 8080 \
  --api-key <your-nova-api-key> \
  --dry-run

# Deploy (will prompt for on-chain at the end)
python3 scripts/nova_deploy.py \
  --repo https://github.com/you/my-app \
  --name "my-app" \
  --port 8080 \
  --api-key <your-nova-api-key>

# Deploy + on-chain registration in one shot
python3 scripts/nova_deploy.py \
  --repo https://github.com/you/my-app \
  --name "my-app" \
  --port 8080 \
  --api-key <your-nova-api-key> \
  --onchain
```

### 第 5 步 — 验证应用的运行状态

```bash
# Health check
curl https://<hostname>/

# Hello endpoint (returns enclave address + signature)
curl https://<hostname>/api/hello

# Attestation (proves it's a real Nitro Enclave) — POST, returns binary CBOR
# In production, /.well-known/attestation is Caddy → Aux API; not app code
curl -sX POST https://<hostname>/.well-known/attestation --output attestation.bin
```

> **注意**：只有在使用 [nova-app-template](https://github.com/sparsity-xyz/nova-app-template) 分支的情况下，`/api/app-wallet` 端口才可用。简化框架版本使用的是 `/api/hello` 端口。

### 第 6 步 — 在链上进行注册（可选，但对建立信任很重要）

应用运行后，需要在链上进行注册以建立可验证的信任关系。

**推荐使用脚本进行注册：**
```bash
python3 scripts/nova_deploy.py ... --onchain
```
脚本会自动执行步骤 6a–6d，并等待注册完成。

**也可以手动通过 API 进行注册**（分为 4 个步骤）：

```bash
# 6a. Create app on-chain
curl -sX POST "$BASE/apps/$SQID/create-onchain" \
  -H "Authorization: Bearer $TOKEN"
# Poll: GET /api/apps/{sqid}/status → onchain_app_id is set when done

# 6b. Enroll build version on-chain (PCR measurements → trusted code fingerprint)
curl -sX POST "$BASE/apps/$SQID/builds/$BUILD_ID/enroll" \
  -H "Authorization: Bearer $TOKEN"

# Poll enrollment via build status endpoint
while true; do
  ENROLLED=$(curl -s "$BASE/builds/$BUILD_ID/status" \
    -H "Authorization: Bearer $TOKEN" \
    | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('is_enrolled',''))")
  echo "Enrolled: $ENROLLED"
  [ "$ENROLLED" = "True" ] && break
  sleep 10
done

# 6c. Generate ZK proof (SP1-based)
curl -sX POST "$BASE/zkproof/generate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"deployment_id\": $DEPLOY_ID}"

# Poll proof via deployment status endpoint (or /zkproof/status/{deployment_id})
while true; do
  PROOF=$(curl -s "$BASE/deployments/$DEPLOY_ID/status" \
    -H "Authorization: Bearer $TOKEN" \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('proof_status',''))")
  echo "Proof status: $PROOF"
  [ "$PROOF" = "proved" ] && break
  [ "$PROOF" = "failed" ] && echo "Proof failed!" && exit 1
  sleep 30
done

# 6d. Register instance on-chain (manual — auto-registration has been removed)
curl -sX POST "$BASE/apps/$SQID/instance/register" \
  -H "Authorization: Bearer $TOKEN"

# Poll: GET /api/deployments/{id}/status → onchain_instance_id is set when done
# Or use unified: GET /api/apps/{sqid}/status → latest_onchain_instance_id
```

**每个步骤的作用：**
- **在链上创建应用**：在 Nova 应用注册表合约中注册您的应用。
- **注册版本**：将 EIF 的 PCR 测量结果记录在链上。
- **生成 ZK 证明**：平台会根据 Enclave 的 Nitro 认证结果生成 SP1 零知识证明。
- **注册实例**：在链上验证 ZK 证明，并将运行中的实例与其注册版本关联起来。

注册完成后，任何人都可以通过链上验证来确认该实例与审核后的构建结果一致。

## Odyn 内部 API 参考

所有 API 端点都位于 `http://127.0.0.1:18000`（仅限 Enclave 内部使用，生产环境中不公开）。

**始终可用的 API 端点：**

| 端点 | 方法 | 描述 |
|---|---|---|
| `/v1/eth/address` | GET | Enclave 的 Ethereum 地址和公钥 |
| `/v1/eth/sign` | POST | 使用 EIP-191 签名（可选，支持认证） |
| `/v1/eth/sign-tx` | POST | 签署 EIP-1559 类型的交易 |
| `/v1/random` | GET | 从 NSM 获取的 32 字节随机数 |
| `/v1/attestation` | POST | 原生的 CBOR 格式的认证数据 |
| `/v1/encryption/public_key` | GET | Enclave 的 P-384 公钥 |
| `/v1/encryption/encrypt` | POST | 对客户端响应进行加密 |
| `/v1/encryption/decrypt` | POST | 解密客户端发送的数据 |

**根据 `advanced` 配置启用的功能：**

| 端点组 | 开启条件 | 描述 |
|---|---|---|
| `/v1/s3/*` | `enable_s3_storage: true` | 基于 S3 的对象存储 |
| `/v1/kms/derive` | `enable_decentralized_kms: true` | 启用去中心化 KMS 功能 |
| `/v1/kms/kv/put\|get\|delete` | `enable_decentralized_kms: true` | 基于 KMS 的键值存储（支持过期时间设置） |
| `/v1/app-wallet/address` | `enable_app_wallet: true` | 启用应用钱包功能 |
| `/v1/app-wallet/sign` | `enable_app_wallet: true` | 通过应用钱包进行 EIP-191 类型的消息签名 |
| `/v1/app-wallet/sign-tx` | `enable_app_wallet: true` | 通过应用钱包进行 EIP-1559 类型的交易签名 |

**生产环境中的端口暴露规则：**
- 运行时仅暴露 **两个端口**：`host app port → enclave app port` 和 `host attestation port → enclave Aux API port 18001`。
- `/.well-known/attestation*` 会被 Caddy 路由到辅助 API（端口 18001）。
- **主要 API（18000）在生产环境中不公开**。

**Odyn 模拟服务**（用于本地开发）：
- 主要 API：`http://odyn.sparsity.cloud:18000`
- 辅助 API：`http://odyn.sparsity.cloud:18001`
- Helios RPC 预设端口：`http://odyn.sparsity.cloud:18545`（通过 `:18553`）

## 重要注意事项

1. **在创建应用时必须设置 `advanced` 参数**。省略该参数会导致构建失败。现在只有 `advanced` 参数存在；旧的 `enclaver` 参数已从 API 中移除。
2. 您的仓库只需包含 `Dockerfile` 和应用代码。平台会在构建时处理其余所有步骤。
3. **应用 ID 格式**：使用 `sqid`（字符串格式，例如 `abc123`），并在所有 URL 路径中使用该格式，而不是整数 `id`。
4. 端口设置：通过 `advanced.app_listening_port` 进行配置。该端口必须与 Dockerfile 中的 `EXPOSE` 设置相匹配。模板仓库中的 `enclaver.yaml` 仅用于参考；门户网站会从中读取端口信息。
5. 仓库 URL 在创建应用时设置一次 — 构建时无需重复设置。构建过程只需要 `git_ref` 和 `version` 参数。
6. 部署时需要指定地区和层级：地区包括 `ap-south-1`（默认）、`us-east-1`、`us-west-1`、`eu-west-1`；层级包括 `standard`（2 vCPU/5 GiB）或 `performance`（6 vCPU/13 GiB）。部署过程中不需要设置环境变量。
7. **Helios RPC**：使用 `references/nova-api.md` 中规定的端口映射。端口在创建应用时固定不变。
8. **KMS 依赖关系**：如果设置了 `enable_app_wallet` 或 `enable_s3_kms_encryption`，则意味着需要使用 KMS 和 Helios；同时也会使用 `kms_app_id` 和 `nova_appRegistry`。
9. KMS 和 S3 的配置完全由平台管理 — 无需手动设置 AWS 凭据或编写 `enclaver.yaml`。
10. 无需手动推送代码到 Docker 注册表。
11. **链上操作（创建应用 → 注册 → 生成 ZK 证明）对于公开可验证性是必需的，但对于功能性的应用来说是可以省略的。
12. 应用注册现在是手动完成的 — 自动注册功能已被移除。在生成 ZK 证明后，可以使用 `POST /api/apps/{app_sqid}/instance/register` 进行注册。
13. 门户网站辅助 API（`clone-repo`、`get-enclaver-config`）用于在输入仓库 URL 时自动填充 `enclaver.yaml` 中的监听端口信息。直接使用 API 时不需要这些 API。
14. 构建过程中会生成 `build-attestation.json` 文件，其中包含 PCR0/PCR1/PCR2、源仓库信息、提交信息以及 GitHub 运行元数据 — 文件会使用 Sigstore/cosign 进行签名，并存储在链外。
15. `IN_ENCLAVE` 参数不是由 Enclaver 自动设置的 — 在本地开发时需要在 Dockerfile 中设置 `ENV IN_ENCLAVE=false`；在生产环境中会自动设置为 `true`。

## 常见问题及解决方法

| 问题 | 解决方法 |
|---|---|
| 构建后缺少 `Dockerfile` | 运行 `clawhub update nova-app-builder` 后重新构建。模板中包含 `Dockerfile.txt`，`scaffold.py` 会自动将其重命名为 `Dockerfile`。 |
| 应用程序期望 `enclaver.yaml` 或旧配置文件**：`enclaver.yaml` 由 Nova 平台自动生成 — 开发者无需提供。在创建应用时设置 `advanced` 参数即可控制所有平台级配置。使用完整模板时，只需关注 `enclave/config.py`（应用业务逻辑配置）。 |
| API 端点 `console.sparsity.cloud` 无法访问**：可能是 `nova_deploy.py` 的旧版本导致的。运行 `clawhub update nova-app-builder` 后问题会解决。正确的端点是 `https://sparsity.cloud/api`。 |
| 使用 `from odyn import Odyn` 时出错**：使用的是旧版本的导入路径。新 SDK 位于 `nova_python_sdk/`，请使用 `from nova_python_sdk.odyn import Odyn`。 |
| 构建过程卡在 `pending` 状态**：检查 nova 构建仓库中的 GitHub Actions 任务；可能是任务排队导致的。 |
| 构建失败**：查看构建响应中的 `error_message`；通常是由于 Dockerfile 问题引起的。 |
| 部署 API 返回 401 错误**：在 sparsity.cloud 重新生成 API 密钥。 |
| 应用部署超过 10 分钟仍未完成**：通过 `GET /api/apps/{sqid}/detail` 查看应用日志。 |
| 在 Enclave 内部使用 `httpx` 时请求失败**：在 `advanced` 配置中添加 `egress_allow` 选项。注意：`**` 仅用于匹配域名；直接 IP 连接需要添加 `0.0.0.0/0`。 |
| 直接 IP 连接被阻止**：在 `advanced.egress_allow` 配置中添加 `0.0.0.0/0`（IPv4）和/或 `::/0`（IPv6）。 |
| S3 操作失败**：确保 `169.254.169.254` 和 S3 端点在 `egress_allow` 配置中。 |
| `/v1/kms/*` 返回 400 错误**：在创建应用时确保 `enable_decentralized_kms: true` 和 `enable_helios_rpc: true` 都已设置。 |
| 应用钱包功能不可用**：在创建应用时确保 `enable_app_wallet: true` 已设置。 |
| 外部请求时代理设置未被正确应用**：对于外部 HTTP 请求，请使用 `httpx`（支持代理）。`requests`/`urllib` 可能会绕过出口代理。注意：`requests` 仅用于内部 Odyn 调用。 |
| 健康检查返回 502 错误**：应用正在启动中，请等待 Enclave 完全启动。 |
| ZK 证明生成失败**：查看 `GET /api/zkproof/status/{deployment_id}` 以获取详细信息。 |
| 在生产环境中 `/.well-known/attestation` 返回错误的格式**：在生产环境中，这是由 Caddy 路由到辅助 API（端口 18001）导致的 — 不是应用代码的问题。在生产环境中请移除应用端的自定义路由逻辑。 |

## 参考文件

- **`references/odyn-api.md`**：Odyn 的完整内部 API 文档（包括签名、加密、KMS、应用钱包、认证等功能）。
- **`references/nova-api.md`：Nova 平台的 REST API 完整端点参考。

## Nova 示例项目

| 示例 | 描述 |
|---|---|
| [hello-world-tee](https://github.com/sparsity-xyz/sparsity-nova-examples/tree/main/hello-world-tee) | **最简单的示例** — 仅包含身份验证和认证功能；使用 `nova_python_sdk/`。 |
| [echo-vault](https://github.com/sparsity-xyz/sparsity-nova-examples/tree/main/echo-vault) | **最佳的后端参考** — 包含 S3 数据持久化和 Helios RPC 功能；是官方 SDK 的来源。 |
| [secured-chat-bot](https://github.com/sparsity-xyz/sparsity-nova-examples/tree/main/secured-chat-bot) | **最佳的端到端加密参考** — 支持浏览器到 Enclave 的 P-384 ECDH 加密。 |
| [rng-oracle](https://github.com/sparsity-xyz/sparsity-nova-examples/tree/main/oracles/rng-oracle) | 包含基于 Enclave 的随机数生成功能。 |
| [price-oracle](https://github.com/sparsity-xyz/sparsity-nova-examples/tree/main/oracles/price-oracle) | 包含外部 API 验证和签名功能。 |

> **Nova Python SDK**：官方 SDK 位于 `enclave/nova_python_sdk/`，在 [nova-app-template](https://github.com/sparsity-xyz/nova-app-template) 和所有示例项目中都有提供。请勿修改 SDK 文件，直接将整个目录复制到您的项目中。 |

## 关键链接

- Nova 平台：https://sparsity.cloud
- **Nova 平台 API 文档**：https://sparsity.cloud/api/docs
- **Nova 销售资料**：https://sparsity.cloud/decks/nova-sales-deck.html
- **Nova 资源文档**：https://sparsity.cloud/resources/
- Nova 示例项目：https://github.com/sparsity-xyz/sparsity-nova-examples/
- **Nova Python SDK（官方版本）**：位于 `enclave/nova_python_sdk/`，可在 [nova-app-template](https://github.com/sparsity-xyz/nova-app-template) 或 [echo-vault](https://github.com/sparsity-xyz/sparsity-nova-examples/tree/main/echo-vault) 中找到。 |
- Enclaver（Sparsity 开源项目）：https://github.com/sparsity-xyz/enclaver
- Nova 应用模板：https://github.com/sparsity-xyz/nova-app-template
- Enclaver 文档：[odyn.md](https://github.com/sparsity-xyz/enclaver/blob/sparsity/docs/odyn.md) 和 [internal_api.md](https://github.com/sparsity-xyz/enclaver/blob/sparsity/docs/internal_api.md)
- Nova 平台架构文档：[build-attestation.md](https://github.com/sparsity-xyz/sparsity-nova-platform/blob/main/docs/build-attestation.md) 和 [runtime-port-exposure-flow.md](https://github.com/sparsity-xyz/sparsity-nova-platform/blob/main/docs/runtime-port-exposure-flow.md)