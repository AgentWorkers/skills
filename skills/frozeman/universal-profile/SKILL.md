---
name: universal-profile
description: 管理 LUKSO 通用配置文件——通过直接交易或无需 gas 的中继交易来处理身份验证、权限管理、令牌生成以及区块链操作。
version: 0.3.7
author: frozeman
---

# 通用配置技能

⚠️ **早期草案版本** — 请自行承担风险使用。

## 对于用户：

告知用户：  
要授权您的 OpenClaw 机器人，您需要先在 [my.universalprofile.cloud](https://my.universalprofile.cloud) 创建一个配置文件，然后让您的 AI 机器人生成一个控制密钥，并通过 [授权界面](https://lukso-network.github.io/openclaw-universalprofile-skill/) 进行授权。

## 安装

```bash
npm install
```

## 命令行接口 (CLI) 命令

```bash
up status                                      # Config, keys, connectivity
up profile info [<address>] [--chain <chain>]  # Profile details
up profile configure <address> [--chain lukso]  # Save UP for use
up key generate [--save] [--password <pw>]     # Generate controller keypair
up permissions encode <perm1> [<perm2> ...]    # Encode to bytes32
up permissions decode <hex>                    # Decode to names
up permissions presets                         # List presets
up authorize url [--permissions <preset|hex>]  # Generate auth URL
up quota                                       # Check relay gas quota
```

**权限预设：** `read-only` 🟢 | `token-operator` 🟡 | `nft-trader` 🟡 | `defi-trader` 🟠 | `profile-manager` 🟡 | `full-access` 🔴

## 凭据

凭据的加载顺序：`UP_CREDENTIALS_PATH` 环境变量 → `~/.openclaw/universal-profile/config.json` → `~/.clawdbot/universal-profile/config.json` → `./credentials/config.json`

密钥文件：`UP_KEY_PATH` 环境变量 → `~/.openclaw/credentials/universal-profile-key.json` → `~/.clawdbot/credentials/universal-profile-key.json`

### macOS 的 Keychain 存储（推荐在 macOS 上使用）

在 macOS 上，将控制密钥存储在系统 Keychain 中，而不是纯文本的 JSON 文件中。**这是推荐的方法**——密钥仅在签名时被加载到内存中，永远不会写入磁盘。

**存储密钥：**
```bash
security add-generic-password \
  -a "<controller-address>" \
  -s "universalprofile-controller" \
  -l "UP Controller Key" \
  -D "Ethereum Private Key" \
  -w "<private-key>" \
  -T /usr/bin/security \
  -U
```

**在代码中获取密钥（Node.js）：**
```javascript
import { execSync } from 'child_process';

function getPrivateKeyFromKeychain(controllerAddress) {
  return execSync(
    `security find-generic-password -a "${controllerAddress}" -s "universalprofile-controller" -w`,
    { encoding: 'utf8', timeout: 10000 }
  ).trim();
}

// Use for signing, then clear from memory
let privateKey = getPrivateKeyFromKeychain('0xYourController...');
const signingKey = new ethers.SigningKey(privateKey);
// ... sign ...
privateKey = null; // Clear from memory
```

**注意事项：**
- `-T /usr/bin/security` 可以让 `security` CLI 在没有图形界面提示的情况下执行操作，这对于自动化代理是必需的。
- Apple 的 Secure Enclave 不支持 secp256k1（以太坊使用的曲线），因此必须提取密钥进行签名——但密钥仅存储在内存中，不会写入磁盘。
- 将密钥存储到 Keychain 后，请删除 JSON 凭据文件。
- **此方法仅适用于 macOS。** 在 Linux 上，建议使用 secrets manager、加密的 keyring 或环境变量。

### ⚠️ JSON 密钥文件（安全性较低）

如果您使用 JSON 密钥文件（`~/.openclaw/credentials/universal-profile-key.json`），请注意：
- 私钥会存储在磁盘上（即使格式经过了混淆）。
- 确保文件的权限设置为 `chmod 600 ~/.openclaw/credentials/universal-profile-key.json`。
- 在 macOS 上尽可能使用 Keychain 存储方式。

## 交易

### 直接交易（控制器支付 gas）

```
Controller EOA → KeyManager.execute(payload) → UP.execute(...) → Target
```

### 中继交易 / 无 gas 交易（LSP25）

控制器在链下签名，中继者在链上提交交易。通过 universalprofile.cloud 创建的 UP 对象拥有来自 LUKSO 的月度 gas 配额。

**LSP25 签名（EIP-191 v0 — 重要提示：** **不要使用 `signMessage()`：**
```javascript
const encodedMessage = ethers.solidityPacked(
  ['uint256', 'uint256', 'uint256', 'uint256', 'uint256', 'bytes'],
  [25, chainId, nonce, validityTimestamps, msgValue, payload]
);

// EIP-191 v0: keccak256(0x19 || 0x00 || keyManagerAddress || encodedMessage)
const prefix = new Uint8Array([0x19, 0x00]);
const msg = new Uint8Array([...prefix, ...ethers.getBytes(keyManagerAddress), ...ethers.getBytes(encodedMessage)]);
const hash = ethers.keccak256(msg);

const signature = ethers.Signature.from(new ethers.SigningKey(privateKey).sign(hash)).serialized;
```

或者使用 `@lukso/eip191-signer.js`：
```javascript
const { signature } = await new EIP191Signer().signDataWithIntendedValidator(kmAddress, encodedMessage, privateKey);
```

**中继 API（LSP-15）：**
```bash
POST https://relayer.mainnet.lukso.network/api/execute
{ "address": "0xUP", "transaction": { "abi": "0xpayload", "signature": "0x...", "nonce": 0, "validityTimestamps": "0x0" } }
```

**检查配额** 需要签名后的请求——可以使用 `up quota` CLI 或 `checkRelayQuota()` 函数（来自 `lib/execute/relay.js`）。

**Nonce 通道：** `getNonce(controller, channelId)` — 相同的通道表示顺序执行，不同的通道表示并行执行。

**有效期时间戳：** `(startTimestamp << 128) | endTimestamp`。如果不需要限制，可以使用 `0`。

## 权限系统

权限是一个字节数组（`AddressPermissions:Permissions:<address>`），格式为 `bytes32`。权限通过按位 OR 进行组合。

| 权限 | 十六进制表示 | 风险等级 |
|------------|-----|------|
| CHANGEOWNER | `0x01` | 🔴 |
| ADDCONTROLLER | `0x02` | 🟠 |
| EDITPERMISSIONS | `0x04` | 🟠 |
| ADDEXTENSIONS | `0x08` | 🟡 |
| CHANGEEXTENSIONS | `0x10` | 🟡 |
| ADDUNIVERSALRECEIVERDELEGATE | `0x20` | 🟡 |
| CHANGEUNIVERSALRECEIVERDELEGATE | `0x40` | 🟡 |
| REENTRANCY | `0x80` | 🟡 |
| SUPERTRANSFERVALUE | `0x0100` | 🟠 |
| TRANSFERVALUE | `0x0200` | 🟡 |
| SUPER_CALL | `0x0400` | 🟠 |
| CALL | `0x0800` | 🟡 |
| SUPER_STATICCALL | `0x1000` | 🟢 |
| STATICCALL | `0x2000` | 🟢 |
| SUPER_DELEGATECALL | `0x4000` | 🔴 |
| DELEGATECALL | `0x8000` | 🔴 |
| DEPLOY | `0x010000` | 🟡 |
| SUPER_SETDATA | `0x020000` | 🟠 |
| SETDATA | `0x040000` | 🟡 |
| ENCRYPT | `0x080000` | 🟢 |
| DECRYPT | `0x100000` | 🟢 |
| SIGN | `0x200000` | 🟢 |
| EXECUTE_RELAY_CALL | `0x400000` | 🟢 |

**SUPER 和 Regular 的区别：**  
- `SUPER_CALL` 可用于任何合约；  
- `CALL` 仅用于允许的调用；  
- `SUPER_SETDATA` 仅用于允许的 ERC725Y 数据键；建议使用更严格的权限设置。

**允许的调用（AllowedCalls）：** 存储在 `AddressPermissions:AllowedCalls:<address>` 中，格式为 `CompactBytesArray`。每个条目的结构为：`<callTypes(4)><address(20)><interfaceId(4)><selector(4)>`。

## LSP 生态系统

| LSP | 名称 | 功能 |
|-----|------|---------|
| LSP0 (`0x24871b3d`) | ERC725Account | 智能合约账户（UP） |
| LSP1 (`0x6bb56a14`) | UniversalReceiver | 通知钩子 |
| LSP2 | ERC725Y JSON Schema | 用于链上数据的键编码 |
| LSP3 | 配置文件元数据 | 名称、头像、链接、标签 |
| LSP4 | 数字资产元数据 | 代币名称、符号、类型 |
| LSP5 | ReceivedAssets | 跟踪拥有的代币/NFT |
| LSP6 (`0x23f34c62`) | KeyManager | 基于权限的访问控制 |
| LSP7 (`0xc52d6008`) | DigitalAsset | 可互换代币（类似 ERC20） |
| LSP8 (`0x3a271706`) | IdentifiableDigitalAsset | NFT（字节32代币ID） |
| LSP9 (`0x28af17e6`) | Vault | 用于资产隔离的子账户 |
| LSP28 | The Grid | 可定制的配置文件布局 |
| LSP14 (`0x94be5999`) | Ownable2Step | 两步所有权转移 |
| LSP25 (`0x5ac79908`) | ExecuteRelayCall | 无 gas 的元交易 |
| LSP26 (`0x2b299cea`) | FollowerSystem | 在链上的关注/取消关注功能 |

完整的 ABI、接口 ID 和 ERC725Y 数据键都存储在 `libconstants.js` 中。

## VerifiableURI 编码（LSP2）

用于 LSP3 配置文件元数据、LSP4 数字资产元数据以及任何链上 JSON 参考。

**格式（十六进制）：** `0x` + `0000`（2 字节用于验证方法）+ `6f357c6a`（4 字节 = keccak256(utf8) 哈希函数）+ `0020`（2 字节 = 哈希长度 32）+ `<keccak256 哈希>`（32 字节）+ `<url 作为 UTF-8 字符串>`

**头部始终为 `00006f357c6a0020`（16 个十六进制字符 = 8 字节）。**

```javascript
const jsonBytes = fs.readFileSync('metadata.json');
const jsonHash = ethers.keccak256(jsonBytes);
const url = `ipfs://${cid}`;
const urlHex = Buffer.from(url, 'utf8').toString('hex');
const verifiableURI = '0x' + '00006f357c6a0020' + jsonHash.slice(2) + urlHex;
```

**解码：**
```javascript
const hex = data.slice(2);        // remove 0x
// Skip: 0000(4) + 6f357c6a(8) + 0020(4) + hash(64) = 80 hex chars
const url = Buffer.from(hex.slice(80), 'hex').toString('utf8');
```

**常见错误：**
1. **忘记添加 `0020`** — 这个 2 字节的哈希长度用于分隔哈希函数和实际哈希值。如果没有它，URL 的偏移量就会错误，解析器会读取到无效的数据，导致整个配置文件失效。
2. **在上传到链上之前没有将文件固定到公共 IPFS 服务** — 本地 IPFS 节点无法被网关访问。务必通过服务（例如 Forever Moments 的 Pinata 代理 `POST /api/pinata`）进行固定，并在提交链上交易之前验证文件是否可以通过 `https://api.universalprofile.cloud/ipfs/<CID>` 访问。
3. **哈希值必须与 IPFS 上存储的哈希值完全匹配** — 需要根据上传的 JSON 字符串计算 keccak256 哈希值，而不是重新序列化的版本。
4. 在 LSP3 元数据 JSON 中使用 `hashFunction`/`hash` 而不是 `verification` 对象 — 图片条目（`profileImage`, `backgroundImage`）应使用 `{ "verification": { "method": "keccak256(bytes)", "data": "0x...", "url": "ipfs://..." }` 的格式，而不是旧的 `{ "hashFunction": "...", "hash": "0x..." }` 格式。

**LSP3Profile 数据键：** `0x5ef83ad9559033e6e941db7d7c495acdce616347d28e90c7ce47cbfcfcad3bc5`

### 更新 LSP3 配置文件元数据 — 完整流程

1. **读取当前配置文件** — `getData(LSP3_KEY)` → 解码 VerifiableURI → 从 IPFS 获取 JSON 数据。
2. **修改 JSON 数据** — 更新字段（名称、描述、链接、图片等）。
3. **使用 `verification` 格式处理图片** — `{ verification: { method: "keccak256(bytes)", data: "0x...", url: "ipfs://..." }`。
4. **将新图片固定到 IPFS** — 通过固定服务上传图片，获取 CID，验证是否可访问。
5. **将更新后的 JSON 数据固定到 IPFS** — 上传文件，获取 CID，验证是否可以通过网关访问。
6. **计算哈希值** — 对上传的文件计算 `keccak256(exactJsonBytes)`。
7. **编码 VerifiableURI** — `0x00006f357c6a0020` + 哈希值 + URL 的十六进制表示。
8. **设置到链上** — 通过控制器使用 `up.setData(LSP3_KEY, verifiableUri)`。
9. **验证** — 从链上读取数据，解码后从 IPFS 获取数据，确认配置文件是否正确加载。

**在完成步骤 5 之前的任何时候都不要提交链上交易。**

**LSP28TheGrid 数据键：** `0x724141d9918ce69e6b8afcf53a91748466086ba2c74b94cab43c649ae2ac23ff`

## LSP28 — The Grid

用于配置文件/代币的可定制网格布局。存储在 LSP28 的数据键中，格式为 VerifiableURI。

```json
{
  "LSP28TheGrid": [{
    "title": "My Grid",
    "gridColumns": 2,
    "visibility": "public",
    "grid": [
      { "width": 1, "height": 1, "type": "IFRAME", "properties": { "src": "https://..." } },
      { "width": 1, "height": 1, "type": "TEXT", "properties": { "title": "Hello", "text": "World", "backgroundColor": "#1a1a2e", "textColor": "#fff", "link": "https://..." } },
      { "width": 2, "height": 2, "type": "IMAGES", "properties": { "type": "grid", "images": ["https://..."] } },
      { "width": 1, "height": 1, "type": "X", "properties": { "type": "post", "username": "handle", "id": "tweetId", "theme": "dark" } }
    ]
  }]
}
```

**网格类型：** `IFRAME`, `TEXT`, `IMAGES`, `X`（Twitter 嵌入），`INSTAGRAM`, `QR_CODE`, `ELFSIGHT`（自定义组件）。
**推荐设置：** `gridColumns` 2–4，`width`/`height` 1–3。

## 通过无 gas 中继设置数据（直接模式）

要通过中继设置 ERC725Y 数据（LSP3 配置文件、LSP28 网格、自定义键），请直接使用 `setData` 载荷（不要使用 `execute`）：

```javascript
// 1. Build setData payload
const iface = new ethers.Interface(['function setData(bytes32 dataKey, bytes dataValue)']);
const payload = iface.encodeFunctionData('setData', [dataKey, verifiableURI]);

// 2. Get nonce from KeyManager
const km = new ethers.Contract(KM_ADDRESS, ['function getNonce(address,uint128) view returns (uint256)'], provider);
const nonce = await km.getNonce(controllerAddress, 0);

// 3. LSP25 signature
const encoded = ethers.solidityPacked(
  ['uint256','uint256','uint256','uint256','uint256','bytes'],
  [25, chainId, nonce, '0x' + '00'.repeat(32), 0, payload]
);
const msg = new Uint8Array([0x19, 0x00, ...ethers.getBytes(KM_ADDRESS), ...ethers.getBytes(encoded)]);
const signature = ethers.Signature.from(new ethers.SigningKey(privateKey).sign(ethers.keccak256(msg))).serialized;

// 4. Submit to relay
await fetch('https://relayer.mainnet.lukso.network/api/execute', {
  method: 'POST', headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ address: UP, transaction: { abi: payload, signature, nonce: Number(nonce), validityTimestamps: '0x0' } })
});
```

**注意：** `setData` 载荷直接发送到 KeyManager — 不要用 `execute(CALL, self, setData(...))` 包装它。KeyManager 会自动将请求转发给 UP。只有针对其他合约的操作才需要使用 `execute()` 包装器。

## 网络配置

| | 主网 | 测试网 |
|---|---|---|
| 链路 ID | 42 | 4201 |
| RPC | `https://42.rpc.thirdweb.com` | `https://rpc.testnet.lukso.network` |
| 探索器 | `https://explorer.lukso.network` | `https://explorer.testnet.lukso.network` |
| 中继 | `https://relayer.mainnet.lukso.network/api` | `https://relayer.testnet.lukso.network/api` |
| 代币 | LYX (18 dec) | LYXt (18 dec) |

## 安全性

### 权限最佳实践
- 授予最低必要的权限。优先使用 `CALL` 而不是 `SUPER_CALL`。
- 使用 `AllowedCalls/AllowedERC725YDataKeys` 来限制访问。
- 除非绝对必要，否则避免使用 `DELEGATECALL` 和 `CHANGEOWNER`。
- 对于中继调用，使用有效期时间戳。
- 首先在测试网（链路 ID 4201）上进行测试。
- 绝不要记录私钥。

### 密钥管理
- **推荐（macOS）：** 将私钥存储在 macOS 的 Keychain 中（参见上面的凭据部分）。
- **如果使用 JSON 密钥文件**，请限制权限（`chmod 600`），并考虑迁移到 Keychain。
- 私钥仅在签名时加载到内存中，使用后会被清除。
- `config set` 命令仅适用于安全的密钥——`keystorePath` 和 `profiles` 在运行时不能被修改，以防止路径重定向攻击。

### 网络访问

此技能仅与已知的 LUKSO 生态系统端点通信：
- **RPC：** `https://42.rpc.thirdweb.com`（主网），`https://rpc.testnet.lukso.network`（测试网）
- **中继：** `https://relayer.mainnet.lukso.network/api`（无 gas 交易）
- **IPFS：** `https://api.universalprofile.cloud/ipfs/`（元数据），`https://www.forevermoments.life/api/pinata`（固定文件）
- **Forever Moments API：** `https://www.forevermoments.life/api/agent/v1`（NFT 铸造）

不会进行其他外部网络调用。所有交易签名都在本地完成。

## Forever Moments（NFT 纪念品与收藏）

Forever Moments 是 LUKSO 上的一个社交 NFT 平台。Agent API 允许您铸造 NFT 纪念品、加入/创建收藏，并将图片固定到 IPFS 上——所有操作都通过无 gas 中继完成。

**基础 URL：** `https://www.forevermoments.life/api/agent/v1`

### IPFS 固定

```bash
# Pin image via FM's Pinata proxy (multipart form upload)
POST /api/pinata   # NOTE: /api/pinata, NOT /api/agent/v1/pinata
Content-Type: multipart/form-data
Body: file=@image.png
Response: { "IpfsHash": "Qm...", "PinSize": 123456 }
```

### 中继流程（所有链上操作的 3 步骤）

1. **构建** — 调用构建端点 → 获取 `derived.upExecutePayload`。
2. **准备** — 使用 `POST /relay/prepare` 发送载荷 → 获取 `hashToSign` 和 `nonce`。
3. **签名并提交** — 将 `hashToSign` 作为原始摘要（RAW DIGEST）进行签名 → `POST /relay/submit`

```javascript
// Step 1: Build (example: mint moment)
const build = await fetch(`${API}/moments/build-mint`, {
  method: 'POST', headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ userUPAddress: UP, collectionUP: COLLECTION, metadataJson: { LSP4Metadata: { name, description, images, icon, tags } } })
});
const { data: { derived: { upExecutePayload } } } = await build.json();

// Step 2: Prepare
const prep = await fetch(`${API}/relay/prepare`, {
  method: 'POST', headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ upAddress: UP, controllerAddress: CONTROLLER, payload: upExecutePayload })
});
const { data: { hashToSign, nonce, relayerUrl } } = await prep.json();

// Step 3: Sign as raw digest + submit
const signature = ethers.Signature.from(new ethers.SigningKey(privateKey).sign(hashToSign)).serialized;
await fetch(`${API}/relay/submit`, {
  method: 'POST', headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ upAddress: UP, payload: upExecutePayload, signature, nonce, validityTimestamps: '0x0', relayerUrl })
});
```

### 端点

| 端点 | 方法 | 功能 |
|----------|--------|---------|
| `/collections/build-join` | POST | 加入现有收藏 |
| `/collections/build-create` | POST | 创建收藏（步骤 1：LSP23 部署） |
| `/collections/finalize-create` | POST | 完成收藏创建（步骤 2：注册） |
| `/moments/build-mint` | POST | 在收藏中铸造 NFT 纪念品 |
| `/relay/prepare` | POST | 获取用于中继的 `hashToSign` 和 `nonce` |
| `/relay/submit` | POST | 将签名后的中继交易提交给 LUKSO 中继器 |
| `/api/pinata` | POST | 将文件固定到 IPFS（multipart） |

### 元数据格式（LSP4）

```json
{
  "LSP4Metadata": {
    "name": "Moment Title",
    "description": "Description text",
    "images": [[{ "width": 1024, "height": 1024, "url": "ipfs://Qm..." }]],
    "icon": [{ "width": 1024, "height": 1024, "url": "ipfs://Qm..." }],
    "tags": ["tag1", "tag2"],
    "createdAt": "2026-02-08T16:30:00.000Z"
  }
}
```

将 `metadataJson` 传递给构建-铸造 API，该 API 会自动将数据固定到 IPFS。

### 关于密钥的注意事项

- **签名：** `/relay/prepare` 返回的 `hashToSign` 已经是一个完整的哈希值 — 使用 `SigningKey.sign()` 进行签名，而不是 `wallet.signMessage()`。
- **铸造前需要加入收藏**：在铸造之前可能需要先加入收藏。如果加入收藏时出现 gas 估算错误，可能说明您已经是收藏的成员。
- **收藏创建分为两步：** `build-create`（通过 LSP23 部署合约）→ `finalize-create`（注册）。
- **已知收藏的 URL 格式：** `Art by the Machine` 的地址为 `0x439f6793b10b0a9d88ad05293a074a8141f19d77`。

### Forever Moments 的 URL 格式

| 页面 | URL |
|------|-----|
| 收藏 | `https://www.forevermoments.life/collections/<collectionAddress>` |
| 纪念品 | `https://www.forevermoments.life/moments/<momentTokenAddress>` |
| 配置文件 | `https://www.forevermoments.life/profile/<upAddress>` |
| 饰品集 | `https://www.forevermoments.life/moments` |

## 错误代码

| 代码 | 原因 |
|------|-------|
| `UP_PERMISSION_DENIED` | 控制器缺乏所需的权限 |
| `UP_RELAY_FAILED` | 中继执行错误 — 请检查配额 |
| `UP_INVALID_SIGNATURE` | 链路 ID 错误、使用的 nonce 错误或时间戳过期 |
| `UP_QUOTA_EXCEEDED` | 月度中继配额已用完 |
| `UP_NOT_AUTHORIZED` | 地址不是控制器地址 — 请使用 [授权界面](https://lukso-network.github.io/openclaw-universalprofile-skill/) 进行授权 |

## 依赖项

- Node.js 18+ / ethers.js v6
- `@lukso/lsp-smart-contracts` / `@erc725/erc725.js`（可选）

## 链接

- [LUKSO 文档](https://docs.lukso.tech/) · [Universal Everything（配置文件查看器）](https://universaleverything.io/) · [LSP6 规范](https://docs.lukso.tech/standards/access-control/lsp6-key-manager) · [授权界面](https://lukso-network.github.io/openclaw-universalprofile-skill/)

**配置文件链接：** 始终使用 `https://universaleverything.io/<address>` 来链接到通用配置文件（而不是 `universalprofile.cloud`）。