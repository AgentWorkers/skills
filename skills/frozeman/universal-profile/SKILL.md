---
name: universal-profile
description: 管理 LUKSO 通用配置文件——包括身份信息、权限设置、令牌管理以及区块链操作功能。支持 Base 和 Ethereum 之间的跨链交互。
version: 0.7.0
author: frozeman
---
# 通用配置技能（Universal Profile Skill）

**授权您的机器人：** 在 [my.universalprofile.cloud](https://my.universalprofile.cloud) 创建一个配置文件，生成一个控制器密钥，然后通过 [授权界面](https://openclaw.universalprofile.cloud) 进行授权。

## 核心概念

- **UP（通用配置）**：智能合约账户（LSP0/ERC725Account），这是链上的身份标识。
- **KeyManager（LSP6）**：用于访问控制；控制器拥有权限位掩码。
- **控制器（Controller）**：具有代表 UP 执行操作的权限的Externally Owned Account（EOA）。
- 所有对外部合约的调用都必须通过 `execute()` 方法路由到 UP，因此 `msg.sender` 为 UP 的地址。
- **例外：** `setData()`/`setDataBatch()` 可以直接在 UP 上调用（内部会检查权限）。

## 执行模型

### 直接执行（所有链——控制器支付手续费）
```
Controller → UP.execute(operation, target, value, data) → Target
```
控制器直接在 UP 合约上调用 `execute()`。UP 通过其 KeyManager（LSP20）内部验证权限。**切勿直接调用 KeyManager 的 execute() 方法**，始终通过 UP 进行调用。

### 无手续费中继（仅限 LUKSO 链路——42/4201）
```
Controller signs LSP25 → Relay API submits → KeyManager.executeRelayCall() → UP
```
控制器签署消息，然后 LUKSO 中继服务提交交易。**切勿自行调用 executeRelayCall()——中继 API 会处理这个操作**。

**⚠️ 重要提示：** 无手续费中继功能仅存在于 LUKSO 主网（42）和测试网（4201）上。在 Base、Ethereum 及其他所有链路上，控制器必须持有原生 ETH 并直接支付手续费。**

**典型手续费成本：** LUKSO 通过中继几乎免费；Base 约 0.001-0.01 美元/笔交易；Ethereum 约 0.10-1.00 美元/笔交易。

## 网络

| 链路 | ID | RPC | 探索器（Explorer） | 中继（Relay） | 代币（Token） |
|---|---|---|---|---|
| LUKSO | 42 | `https://42.rpc.thirdweb.com` | `https://explorer.lukso.network` | `https://relayer.mainnet.lukso.network/api` | LYX |
| LUKSO 测试网 | 4201 | `https://rpc.testnet.lukso.network` | `https://explorer.testnet.lukso.network` | `https://relayer.testnet.lukso.network/api` | LYXt |
| Base | 8453 | `https://mainnet.base.org` | `https://basescan.org` | ❌ | ETH |
| Ethereum | 1 | `https://eth.llamarpc.com` | `https://etherscan.io` | ❌ | ETH |

## 命令行界面（CLI）

**预设选项：**  
`read-only` 🟢 | `token-operator` 🟡 | `nft-trader` 🟡 | `defi-trader` 🟠 | `profile-manager` 🟡 | `full-access` 🔴

## 凭据（Credentials）

配置文件的查找顺序：  
`UP_CREDENTIALS_PATH` 环境变量 → `~/.openclaw/universal-profile/config.json` → `~/.clawdbot/universal-profile/config.json`

密钥的查找顺序：  
`UP_KEY_PATH` 环境变量 → `~/.openclaw/credentials/universal-profile-key.json` → `~/.clawdbot/credentials/universal-profile-key.json`

新凭据的默认路径：  
`~/.openclaw/credentials/universal-profile-key.json`

**技能配置文件路径：**  
`~/.openclaw/skills/universal-profile/config.json`

**预期的 JSON 格式：**  
```json
{
  "universalProfile": {
    "address": "0xYourUniversalProfileAddress"
  },
  "controller": {
    "address": "0xYourControllerAddress",
    "privateKey": "0xYourPrivateKey"
  }
}
```

**密钥文件的权限设置：**  
`chmod 600`。密钥仅用于签名，使用后会被清除。如果凭据文件对其他用户或组可见，技能会发出警告。

## 权限（bytes32 类型的 BitArray）

| 权限 | 十六进制值 | 风险等级 | 备注 |
|---|---|---|---|
| CHANGEOWNER | 0x01 | 🔴 | |
| ADDCONTROLLER | 0x02 | 🟠 | |
| EDITPERMISSIONS | 0x04 | 🟠 | |
| ADDEXTENSIONS | 0x08 | 🟡 | |
| CHANGEEXTENSIONS | 0x10 | 🟡 | |
| ADDUNIVERSALRECEIVERDELEGATE | 0x20 | 🟡 | |
| CHANGEUNIVERSALRECEIVERDELEGATE | 0x40 | 🟡 | |
| REENTRANCY | 0x80 | 🟡 | |
| SUPER_TRANSFERVALUE | 0x0100 | 🟠 | 任何接收者均可 |
| TRANSFERVALUE | 0x0200 | 🟡 | 仅限允许的调用（AllowedCalls） |
| SUPER_CALL | 0x0400 | 🟠 | 任何合约均可 |
| CALL | 0x0800 | 🟡 | 仅限允许的调用（AllowedCalls） |
| SUPER_STATICCALL | 0x1000 | 🟢 | |
| STATICCALL | 0x2000 | 🟢 | |
| SUPER_DELEGATECALL | 0x4000 | 🔴 | |
| DELEGATECALL | 0x8000 | 🔴 | |
| DEPLOY | 0x010000 | 🟡 | |
| SUPER_SETDATA | 0x020000 | 🟠 | 任何密钥均可 |
| SETDATA | 0x040000 | 🟡 | 仅限允许的 ERC725YDataKeys |
| ENCRYPT | 0x080000 | 🟢 | |
| DECRYPT | 0x100000 | 🟢 | |
| SIGN | 0x200000 | 🟢 | |
| EXECUTE_RELAY_CALL | 0x400000 | 🟢 | |

**说明：**  
`SUPER` 级别的权限具有最大权限；普通权限仅限于允许的调用（AllowedCalls）或允许的 ERC725YDataKeys。建议使用受限权限。

## 交易（Transactions）

### 直接执行（所有链路）
```javascript
// Controller calls UP.execute() directly — works on LUKSO, Base, Ethereum
const provider = new ethers.JsonRpcProvider(rpcUrl);  // use correct RPC for chain
const wallet = new ethers.Wallet(controllerPrivateKey, provider);
const up = new ethers.Contract(upAddress, ['function execute(uint256,address,uint256,bytes) payable returns (bytes)'], wallet);
await (await up.execute(0, recipient, ethers.parseEther('0.01'), '0x')).wait();
```

### 无手续费中继（仅限 LUKSO 链路）

**LSP25 中继签名——EIP-191 v0，切勿使用 `signMessage()`：**
```javascript
const encoded = ethers.solidityPacked(
  ['uint256','uint256','uint256','uint256','uint256','bytes'],
  [25, chainId, nonce, validityTimestamps, msgValue, payload]
);
const prefix = new Uint8Array([0x19, 0x00]);
const msg = new Uint8Array([...prefix, ...ethers.getBytes(kmAddress), ...ethers.getBytes(encoded)]);
const signature = ethers.Signature.from(new ethers.SigningKey(privateKey).sign(ethers.keccak256(msg))).serialized;
```

**中继 API：**
```
POST https://relayer.mainnet.lukso.network/api/execute
{ "address": "0xUP", "transaction": { "abi": "0xpayload", "signature": "0x...", "nonce": 0, "validityTimestamps": "0x0" } }
```

**中继调用的 `payload` 是完整的 `UP.execute(...)` 调用数据。**中继服务会调用 `KeyManager.executeRelayCall()`——切勿直接调用 KM。**

**通过中继进行 `setData` 操作时，`payload` 是 `setData(...)` 的调用数据（不需要用 `execute()` 包装）。**

**随机数通道（Nonce）：** `getNonce(controller, channelId)`——相同的通道表示顺序执行，不同的通道表示并行执行。**有效期时间戳：**(startTimestamp << 128) | endTimestamp`。若无限制，使用 `0`。**

## 跨链部署（LSP23）**

UP 可以通过重新执行原始的 LSP23 工厂调用数据，在其他链路上重新部署。

### 工厂与实现（LUKSO、Base、Ethereum 上的地址相同）

| 合约 | 地址 |  
|---|---|
| LSP23 工厂 | `0x2300000A84D25dF63081feAa37ba6b62C4c89a30` |
| UniversalProfileInit v0.14.0 | `0x3024D38EA2434BA6635003Dc1BDC0daB5882ED4F` |
| LSP6KeyManagerInit v0.14.0 | `0x2Fe3AeD98684E7351aD2D408A43cE09a738BF8a4` |
| PostDeploymentModule | `0x000000000066093407b6704B89793beFfD0D8F00` |

**工作流程：**
1. 获取原始部署数据：`node commands/cross-chain-deploy-data.js <upAddress> [--verify]`
2. 为目标链上的控制器充值 ETH。
3. 向工厂提交相同的调用数据：`wallet.sendTransaction({ to: factoryAddress, data: calldata, value: 0n })`
4. 通过 [授权界面](https://openclaw.universalprofile.cloud) 在新链路上授权控制器（权限因链路而异）。

### 限制：
- 旧版本的 UP（LSP23 之前的版本）没有部署事件。
- 确定性要求使用相同的盐值（salt）、实现代码和初始化数据。

## LSP 生态系统

| LSP | 接口 ID | 名称 | 功能 |
|---|---|---|---|
| LSP0 | 0x24871b3d | ERC725Account | 智能合约账户（UP） |
| LSP1 | 0x6bb56a14 | UniversalReceiver | 通知钩子（Notification hooks） |
| LSP2 | — | ERC725Y JSON 格式 | 密钥编码 |
| LSP3 | — | 配置文件元数据 | 名称、头像、链接、标签 |
| LSP4 | — | 数字资产元数据 | 代币名称、符号、类型 |
| LSP5 | — | 持有资产（ReceivedAssets） | 跟踪拥有的代币/NFTs |
| LSP6 | 0x23f34c62 | KeyManager | 基于权限的访问控制 |
| LSP7 | 0xc52d6008 | 数字资产（DigitalAsset） | 可互换代币（类似 ERC20） |
| LSP8 | 0x3a271706 | 可识别数字资产（IdentifiableDigitalAsset） | NFTs（bytes32 类型的代币 ID） |
| LSP9 | 0x28af17e6 | 仓库（Vault） | 用于资产隔离的子账户 |
| LSP14 | 0x94be5999 | 两步所有权转移（Ownable2Step） |
| LSP25 | 0x5ac79908 | 执行中继调用（ExecuteRelayCall） | 无手续费的中继交易（仅限 LUKSO） |
| LSP26 | 0x2b299cea | 关注/取消关注系统（Follow/Unfollow） | 链上关注/取消关注功能 |
| LSP28 | — | TheGrid | 可定制的配置文件布局 |

完整的 ABI、接口 ID 和 ERC725Y 数据键位于 `libconstants.js` 中。

## LSP26 的关注/取消关注功能

**合约地址：** `0xf01103E5a9909Fc0DBe8166dA7085e0285daDDcA`（仅限 LUKSO 主网）。

**必须通过 `execute()` 方法路由到 UP——切勿直接由控制器调用。**  
```javascript
const followData = lsp26Iface.encodeFunctionData('follow', [targetAddress]);
// Direct: km.execute(up.encodeFunctionData('execute', [0, LSP26_ADDR, 0, followData]))
// Relay: sign + submit via relay API
```

## 可验证 URI（LSP2）

**格式：**  
`0x` + `00006f357c6a0020`（8 字节的头部）+ `keccak256hash`（32 字节）+ `url as UTF-8 hex`  

**解码步骤：**  
跳过前 80 个十六进制字符（2 + 8 + 4 + 64 + 2），剩余部分为 UTF-8 格式的 URL。

**常见错误：**  
- 忘记添加 `0020` 作为哈希长度字节；  
- 在链上交易前未将文件固定到 IPFS；  
- 重新序列化后哈希值不匹配。

### LSP3 配置文件更新流程：
1. 读取当前配置：`getData(0x5ef83ad9559033e6e941db7d7c495acdce616347d28e90c7ce47cbfcfcad3bc5)` → 解码可验证 URI → 获取 JSON 数据。
2. 修改 JSON 数据。
3. 使用以下格式创建文件：`{ verification: { method: "keccak256(bytes)", data: "0x...", url: "ipfs://..." }`（用于图片）。
4. 将图片和 JSON 数据固定到 IPFS，通过网关验证其可访问性。
5. 计算 `keccak256(exactJsonBytes)`，然后生成可验证 URI。
6. 从控制器调用 `setData(LSP3_KEY, verifiableUri)`。
7. 验证：重新读取、解码、获取数据并确认。

**LSP3 的密钥格式：**  
`0x5ef83ad9559033e6e941db7d7c495acdce616347d28e90c7ce47cbfcfcad3bc5`  
**LSP28 的密钥格式：**  
`0x724141d9918ce69e6b8afcf53a91748466086ba2c74b94cab43c649ae2ac23ff`

## LSP28 的 TheGrid 功能

**TheGrid 的布局信息存储在 LSP28 的密钥中，以可验证 URI 的形式提供。**  
**支持的文件类型：** `IFRAME`, `TEXT`, `IMAGES`, `X`, `INSTAGRAM`, `QR_CODE`, `ELFSIGHT`。  
**网格列数：** 2–4；** **宽度/高度：** 1–3。

## Forever Moments（仅限 LUKSO）

**社交 NFT 平台。**  
代理 API：`https://www.forevermoments.life/api/agent/v1`。

### 三步中继流程：**
1. **构建（Build）**：`POST /moments/build-mint`（或 `/collections/build-join` 等）→ 获取 `derived.upExecutePayload`。
2. **准备（Prepare）**：`POST /relay/prepare`，传入 `{ upAddress, controllerAddress, payload }` → 获取 `hashToSign` 和 `nonce`。
3. **签名并提交（Sign & Submit）**：使用 `SigningKey.sign()` 对 `hashToSign` 进行签名（**不要使用 `signMessage()`**），然后提交到 `/relay/submit`。

**端点：**
- `/collections/build-join`：创建集合。
- `/collections/build-create` + `/collections/finalize-create`：创建集合（两步流程）。
- `/moments/build-mint`：铸造 Moment NFT。
- `/relay/prepare` + `/relay/submit`：执行中继操作。
- `/api/pinata`（非 `/api/agent/v1/pinata`）：将文件固定到 IPFS。

### 元数据（LSP4）  
**已知集合示例：** `0x439f6793b10b0a9d88ad05293a074a8141f19d77`

**URL 格式：**
- 集合：`https://www.forevermoments.life/collections/<addr>`
- 时刻（Moment）：`https://www.forevermoments.life/moments/<addr>`
- 配置文件：`https://www.forevermoments.life/profile/<addr>`

## 错误代码**

| 代码 | 原因 |
|---|---|
| UP_PERMISSION_DENIED | 控制器缺乏所需权限 |
| UP_RELAY_FAILED | 中继错误——检查配额（仅限 LUKSO） |
| UP_INVALID_SIGNATURE | 链路 ID 错误、使用的随机数无效或时间戳过期 |
| UP_QUOTA_EXCEEDED | 每月中继配额已用完（仅限 LUKSO） |
| UP_NOT_AUTHORIZED | 非控制器——请使用 [授权界面](https://openclaw.universalprofile.cloud) 进行授权 |

## 安全性建议：**
- 仅授予最低必要的权限。优先使用 `CALL` 而不是 `SUPER_CALL`。
- 使用 `AllowedCalls` 或 `AllowedERC725YDataKeys` 来限制权限。
- 除非必要，否则避免使用 `DELEGATECALL` 和 `CHANGEOWNER`。
- 绝不要记录、打印或传输私钥。
- 先在测试网（4201）上进行测试。
- 配置文件中的设置仅限于受信任的密钥。

## 依赖项：**
Node.js 18+、ethers.js v6、viem。

**参考链接：**
[LUKSO 文档](https://docs.lukso.tech/) · [Universal Everything](https://universaleverything.io/) · [LSP6 规范](https://docs.lukso.tech/standards/access-control/lsp6-key-manager) · [授权界面](https://openclaw.universalprofile.cloud)

**配置文件 URL：**  
始终使用 `https://universaleverything.io/<address>`