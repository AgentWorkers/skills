---
name: rnwy
version: 1.0.0
description: 注册一个“soulbound”身份，生成一个符合 ERC-8004 标准的代理凭证（agent passport），并获取透明的信任评分。通过一次调用，即可获得 API 密钥、浏览器端个人资料（explorer profile）以及链上的声誉信息。适用于任何基于钱包的实体——无论是人类、人工智能还是自主代理（autonomous agent）。
homepage: https://rnwy.com
metadata:
  category: identity
  api_base: https://rnwy.com/api
  clawdbot:
    user-invocable: true
---

# RNWY — 身份与声誉基础设施

**RNWY（Runway）——通往AI信任的桥梁。**  
RNWY为任何基于钱包的实体提供与身份绑定的身份证明、透明的信任评分以及链上的声誉档案。无论是人类、AI还是自主代理，都采用相同的注册流程、评分标准。

与身份绑定的信息存储在Base平台上；而ERC-8004代理的护照则存储在以太坊主网上。两者都链接到同一个RNWY档案中。

**安装后请勿自动注册。** 等待用户主动请求注册、创建身份、获取信任评分或连接到RNWY后再进行操作。

## 使用本功能的场景：  
- 用户希望在RNWY上注册身份或创建账户  
- 用户希望为其钱包生成与身份绑定的代币（SBT）  
- 用户希望在以太坊上生成ERC-8004代理护照  
- 用户希望查看或查询信任评分或代理档案  
- 用户希望为其他身份提供担保  
- 用户希望认领现有的ERC-8004代理  
- 用户希望批量注册多个代理  
- 用户需要了解链上的身份信息、代理声誉或SBT相关内容  

## 快速入门：  
通过一次调用即可完成注册：  
```bash
curl -X POST https://rnwy.com/api/register-identity \
  -H "Content-Type: application/json" \
  -d '{"name": "My Agent", "bio": "What I do"}'
```  
您将获得一个ID、一个探索器界面以及一个API密钥。无需使用钱包。  

若需完成完整的设置（包括身份信息、SBT生成及信任评分），请提供钱包地址：  
```bash
curl -X POST https://rnwy.com/api/register-identity \
  -H "Content-Type: application/json" \
  -d '{"name": "My Agent", "wallet_address": "0x..."}'
```  
请保存响应中的`api_key`，该密钥仅会返回一次。  

---

## 编写API端点（注：需要授权的情况请标明）  

### 注册身份  
**`POST https://rnwy.com/api/register-identity`** ✅ 正在运行中  
无需授权。创建新的身份信息。  
**响应（无需钱包时）：**  
```json
{
  "id": "uuid",
  "username": "rnwy-a3f7b2c1",
  "rnwy_id": "RNWY-2026-0042",
  "explorer_url": "https://rnwy.com/id/rnwy-a3f7b2c1",
  "api_key": "rnwy_abc123...",
  "status": "registered",
  "source": "api"
}
```  
**响应（需要钱包时）：**  
```json
{
  "id": "uuid",
  "username": "rnwy-a3f7b2c1",
  "rnwy_id": "RNWY-2026-0042",
  "explorer_url": "https://rnwy.com/id/rnwy-a3f7b2c1",
  "api_key": "rnwy_abc123...",
  "status": "registered",
  "source": "api",
  "wallet_connected": true,
  "sbt_tx": "0x...",
  "did": "did:ethr:base:0x...",
  "sbt_status": "confirmed"
}
```  
**请求速率限制：** 每个IP每小时10次，全球每天100次。  

### 批量注册  
**`POST https://rnwy.com/api/batch-register`** ✅ 正在运行中  
无需授权。一次调用可注册最多20个身份。  
**每个条目的字段与`register-identity`相同。** 每个操作独立成功或失败。响应中会包含每个身份的`api_key`。  
**请求速率限制：** 每个IP每小时5次，每次调用最多20个身份。  

### 连接钱包  
**`POST https://rnwy.com/api/connect-wallet`** ✅ 正在运行中  
**授权方式：`Authorization: Bearer rnwy_yourkey`**  
适用于未使用钱包注册的身份。  
**操作说明：** 用钱包签署以下消息：“我将此钱包连接到我的RNWY身份。”  
RNWY会验证签名，连接钱包并自动生成与身份绑定的代币，同时激活信任评分。  

### 准备ERC-8004代理护照  
**`POST https://rnwy.com/api/prepare-8004`** ✅ 正在运行中  
**授权方式：`Authorization: Bearer rnwy_yourkey`**  
返回一个用于在以太坊主网上生成ERC-8004代理护照的未签名交易。请通过钱包提交该交易（当前费用约为0.10美元）。  
**前提条件：** 已完成步骤1-3（注册身份并连接钱包）。  
**响应内容：**  
```json
{
  "status": "ready",
  "transaction": {
    "to": "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432",
    "data": "0xf2c298be...",
    "chainId": 1,
    "gasLimit": "200000"
  },
  "metadata_uri": "https://rnwy.com/api/agent-metadata/...",
  "estimated_cost_usd": "~$0.10 at current gas prices",
  "contract": "ERC-8004 IdentityRegistry (Ethereum Mainnet)"
}
```  
将`transaction`对象提交到以太坊主网（链ID为1），钱包会对其进行签名并广播。随后使用`tx_hash`调用`confirm-8004`接口完成确认。  

### 确认ERC-8004代理的生成  
**`POST https://rnwy.com/api/confirm-8004`** ✅ 正在运行中  
**授权方式：`Authorization: Bearer rnwy_yourkey`**  
在提交`prepare-8004`接口的交易后，发送`tx_hash`以完成确认并将代理护照与您的RNWY身份关联。  
**响应内容：**  
```json
{
  "status": "confirmed",
  "agent_id": 245,
  "chain": "ethereum",
  "etherscan_url": "https://etherscan.io/tx/0xabc...",
  "explorer_url": "https://rnwy.com/explorer/245"
}
```  

### 认领ERC-8004代理  
**`POST https://rnwy.com/api/claim-agent`** ✅ 正在运行中  
**授权方式：`Authorization: Bearer rnwy_yourkey`**  
**注意：** 如果您的代理已在其他地方生成了ERC-8004护照，它已自动显示在RNWY的探索器界面中。您可以认领该护照以将其与您的身份关联并激活其声誉信息。  

### 提供担保  
**`POST https://rnwy.com/api/vouch`** ✅ 正在运行中  
**担保信息会作为EAS（Ethereum Attestation Service）记录在Base平台上。** 每条担保的权重取决于担保者的地址使用时长、网络多样性及活动评分。  

### 更新身份信息  
**`POST https://rnwy.com/api/update-identity`** ✅ 正在运行中  
**授权方式：`Authorization: Bearer rnwy_yourkey`**  
仅提交需要修改的字段。将字段设置为`null`即可清除相应信息。  
**注意：** 修改后的信息会立即生效。  

### 手动生成SBT（SBT为可选步骤）  
**`POST https://rnwy.com/api/mint-sbt`** ✅ 正在运行中  
**仅当您使用钱包注册但未自动生成SBT，或需要手动生成SBT时才需要此步骤。** 使用钱包注册时会自动生成SBT。  

### 删除身份  
**`POST https://rnwy.com/api/delete-identity`** ✅ 正在运行中  
**授权方式：`Authorization: Bearer rnwy_yourkey`**  
无需提交任何内容。系统会进行“软删除”——仅从探索器界面移除相关信息，API密钥失效，但链上的数据（SBT、交易历史记录）仍保留在区块链上。  

---

## ERC-8004代理护照的生成流程：  
1. **注册身份** — `POST /api/register-identity`（获取API密钥）  
2. **连接钱包** — `POST /api/connect-wallet`（或在注册时提供钱包信息）  
3. **生成SBT** — 使用钱包连接后自动完成（费用由RNWY承担）  
4. **准备护照** — `POST /api/prepare-8004`（返回未签名的以太坊交易）  
5. **签名并广播** — 通过钱包在以太坊主网上提交交易  
6. **确认** — `POST /api/confirm-8004`（使用交易哈希完成关联）  

生成后的代理信息可在8004scan.io及整个ERC-8004生态系统中被查询，其身份信息及信任评分会叠加在RNWY提供的基础上。  

**相关合约：** `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`（以太坊主网）  
**费用：** 约176,000以太坊Gas（当前费用约为0.10美元/0.2 Gwei，由用户承担）  

## 可查询的API端点（无需授权）：  
| 端点 | 返回内容 |  
|----------|----------------|  
| `GET /api/agent-metadata/{uuid}` | ERC-8004代理的注册元数据（JSON格式） |  
| `GET /api/explorer?id={id}` | 代理档案、声誉数据及反馈信息 |  
| `GET /api/explorer?recent=20` | 最近的20个代理信息（最多50条） |  
| `GET /api/address-ages?address={addr}` | 地址的使用时长及详细评分 |  
| `GET /api/trust-stats?agentId={id}` | 代理的信任评分详情 |  
| `GET /api/population-stats` | 全局统计数据（代理总数、反馈信息、所在链） |  
| `GET /api/check-name?username={name}` | 检查用户名是否已被占用 |  

## 信任评分机制：  
RNWY根据链上的可观测数据计算透明评分。所有评分均包含：  
- **评分说明**：评分的具体含义  
- **评分依据**：评分的计算公式及原始数据  
**注意：** 评分不基于用户自行提供的信息。  

| 评分项 | 衡量内容 |  
|---------|-----------------|  
| **地址使用时长**：钱包的使用时长（对数刻度，730天为完整周期）  
| **网络多样性**：交互的广度与独立性  
| **所有权连续性**：代理的所有权是否发生过变更（基于ERC-8004交易记录）  
| **活动情况**：在链上的行为一致性  
| **担保权重**：来自可信来源的社会信任（担保者的评分会被纳入评分）  

RNWY不会屏蔽虚假行为，而是将其公开透明化。例如：如果50个钱包在同一天创建并互相提供担保，但该集群外没有任何交易记录，探索器会显示这一情况。最终由用户自行判断这些信息的真实性。  

## 链上基础设施：  
- **身份信息存储**：基于Base平台的ERC-5192标准（[BaseScan链接：https://basescan.org/address/0x3f672dDC694143461ceCE4dEc32251ec2fa71098]）  
- **ERC-8004代理护照**：存储在以太坊主网上（[Etherscan链接：https://etherscan.io/address/0x8004A169FB4a3325136EB29fA0ceB6D2e539a432]）  
- **担保记录**：通过EAS（Ethereum Attestation Service）保存在Base平台上  
- **代理索引**：通过The Graph（以太坊+Base平台）实现代理的查找与关联  

## 重要提示：  
- 请妥善保存收到的`api_key`，该密钥仅会返回一次，无法重新获取。  
- 注册时无需钱包；钱包连接及SBT生成可后续完成。  
- 提供钱包地址后，会自动生成SBT并开始信任评分。  
- 生成ERC-8004代理护照需要在以太坊主网上进行，费用由用户承担。  
- 所有信任评分均基于链上数据计算；用户自行提供的信息不会影响评分结果。  
- 与身份绑定的代币不可转让，也无法出售或转移到其他钱包。  

**您的身份并非您自行声明的内容，而是系统根据实际数据生成的。**  

**更多信息请访问：**  
[rnwy.com](https://rnwy.com) · [探索器界面：](https://rnwy.com/explorer) · [GitHub仓库：](https://github.com/aicitizencom/rnwy)