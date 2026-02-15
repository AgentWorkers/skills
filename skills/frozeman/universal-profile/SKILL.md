---
name: universal-profile
description: 管理 LUKSO 通用配置文件——通过直接交易或无需 gas 的中继交易来处理身份验证、权限管理、令牌生成以及区块链操作。
version: 0.5.0
author: frozeman
---
# 通用配置文件技能

要授权您的 OpenClaw 机器人，请在 [my.universalprofile.cloud](https://my.universalprofile.cloud) 创建一个配置文件，生成一个控制器密钥，然后通过 [授权 UI](https://lukso-network.github.io/openclaw-universalprofile-skill/) 进行授权。

## 身份与执行

您的 **通用配置文件（UP）地址** 是您在链上的身份。控制器密钥只是一个签名密钥，用于代表您的 UP 执行操作——可以将其视为会话密钥。

所有与其他合约的交互（跟随、转账、合约调用）都应通过 UP 进行，以便这些操作归属于您的配置文件，而不是您的控制器 EOA（Externally Owned Account）。有两种方法可以实现这一点：

**1. 直接执行**（控制器支付 gas）：
```
Controller → UP.execute(0, targetContract, 0, encodedCall)
```

**2. 无 gas 中继**（LUKSO 中继器支付 gas）：
```
Controller signs payload → Relayer submits → KeyManager → UP.execute(...)
```

这两种方法都能确保目标合约中的 `msg.sender` 是您的 UP 地址。有关实现细节，请参阅 [交易](#transactions)。

唯一的例外是 `setData()` / `setDataBatch()`——这些可以直接在 UP 上调用，因为它们会内部检查控制器的权限。

## 安装

```bash
npm install
```

## CLI 命令

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

### 必需的环境变量（可选——支持基于文件的凭证）

| 变量 | 用途 |
|----------|---------|
| `UP_CREDENTIALS_PATH` | 包含 UP 地址和控制器信息的 config.json 文件路径 |
| `UP_KEY_PATH` | 包含控制器私钥的 JSON 文件路径 |

### 基于文件的凭证位置（按顺序检查）

**配置：** `UP_CREDENTIALS_PATH` 环境变量 → `~/.openclaw/universal-profile/config.json` → `~/.clawdbot/universal-profile/config.json`

**密钥：** `UP_KEY_PATH` 环境变量 → `~/.openclaw/credentials/universal-profile-key.json` → `~/.clawdbot/credentials/universal-profile-key.json`

### 密钥存储

控制器私钥可以通过以下方式提供：

1. **环境变量**（推荐用于持续集成/自动化环境）：将 `UP_KEY_PATH` 设置为指向安全的 JSON 密钥文件
2. **JSON 密钥文件**：位于 `~/.openclaw/credentials/universal-profile-key.json`
3. **macOS Keychain**（仅限 macOS）：使用 `security add-generic-password` 将密钥存储在 Keychain 中。如果找不到基于文件的密钥，技能的凭证加载器会尝试从 Keychain 中获取密钥。

**安全最佳实践：**
- 限制密钥文件的权限：`chmod 600 ~/.openclaw/credentials/universal-profile-key.json`
- 私钥仅在签名时加载到内存中，之后立即清除
- 尽量使用权限最小的专用控制器密钥（参见下面的权限最佳实践）
- 在 Linux 上，使用环境变量或秘密管理器

## 交易

### 直接执行（控制器支付 gas）

```
Controller EOA → KeyManager.execute(payload) → UP.execute(...) → Target
```

```javascript
const payload = up.interface.encodeFunctionData('execute', [0, recipient, ethers.parseEther('1.5'), '0x']);
await (await km.execute(payload)).wait();
```

### 中继 / 无 gas 中继（LSP25）

控制器在链下签名，中继器在链上提交交易。通过 universalprofile.cloud 创建的 UP 有来自 LUKSO 的月度 gas 配额。

**LSP25 签名（EIP-191 v0 — 重要提示：请勿使用 `signMessage()`）：**

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

**检查配额** 需要签名请求——使用 `up quota` CLI 或 `checkRelayQuota()`（来自 `lib/execute/relay.js`）。

**Nonce 通道：** `getNonce(controller, channelId)` — 相同的通道表示顺序执行，不同的通道表示并行执行。

**有效时间戳：** `(startTimestamp << 128) | endTimestamp`。如果不需要限制，可以使用 `0`。

## 权限系统

权限是一个字节数组 `AddressPermissions:Permissions:<address>`。通过按位 OR 进行组合。

| 权限 | 十六进制值 | 风险等级 |
|------------|-----|------|
| CHANGEOWNER | `0x01` | 🔴 |
| ADDCONTROLLER | `0x02` | 🟠 |
| EDITPERMISSIONS | `0x04` | 🟠 |
| ADDEXTENSIONS | `0x08` | 🟡 |
| CHANGEEXTENSIONS | `0x10` | 🟡 |
| ADDUNIVERSALRECEIVERDELEGATE | `0x20` | 🟡 |
| CHANGEUNIVERSALRECEIVERDELEGATE | `0x40` | 🟡 |
| REENTRANCY | `0x80` | 🟡 |
| SUPER_TRANSFERVALUE | `0x0100` | 🟠 |
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

**SUPER 与普通权限的区别：** `SUPER_CALL` 可用于任何合约；`CALL` 仅用于允许的调用；`SUPER_SETDATA` 仅用于允许的 ERC725Y 数据键。建议使用受限权限。

**允许的调用：** `AddressPermissions:AllowedCalls:<address>` 中的 `CompactBytesArray`。每个条目的格式为：`<callTypes(4)><address(20)><interfaceId(4)><selector(4)>`。

## LSP 生态系统

| LSP | 名称 | 用途 |
|-----|------|---------|
| LSP0 (`0x24871b3d`) | ERC725Account | 智能合约账户（UP） |
| LSP1 (`0x6bb56a14`) | UniversalReceiver | 通知钩子 |
| LSP2 | ERC725Y JSON Schema | 链上数据的键编码 |
| LSP3 | 配置文件元数据 | 名称、头像、链接、标签 |
| LSP4 | 数字资产元数据 | 代币名称、符号、类型 |
| LSP5 | ReceivedAssets | 跟踪拥有的代币/NFTs |
| LSP6 (`0x23f34c62`) | KeyManager | 基于权限的访问控制 |
| LSP7 (`0xc52d6008`) | DigitalAsset | 可互换代币（类似 ERC20） |
| LSP8 (`0x3a271706`) | IdentifiableDigitalAsset | NFTs（字节32代币 ID） |
| LSP9 (`0x28af17e6`) | Vault | 资产隔离的子账户 |
| LSP28 | The Grid | 可定制的配置文件布局 |
| LSP14 (`0x94be5999`) | Ownable2Step | 两步所有权转移 |
| LSP25 (`0x5ac79908`) | ExecuteRelayCall | 无 gas 的元交易 |
| LSP26 (`0x2b299cea`) | FollowerSystem | 链上的关注/取消关注功能 |

完整的 ABI、接口 ID 和 ERC725Y 数据键都在 `libconstants.js` 中。

## LSP26 — 关注/取消关注

关注和取消关注必须通过 `execute()` 经由 UP 进行路由。LSP26 FollowerSystem 合约的地址在主网上是 `0xf01103E5a9909Fc0DBe8166dA7085e0285daDDcA`。

**⚠️ 严禁直接使用控制器密钥调用 `follow()`——否则关注操作将从控制器地址而不是 UP 地址进行注册。**

## VerifiableURI 编码（LSP2）

用于 LSP3 配置文件元数据、LSP4 资产元数据以及任何链上 JSON 参考。

**格式（十六进制）：** `0x` + `0000`（2 字节验证方法）+ `6f357c6a`（4 字节 = keccak256(utf8) 哈希函数）+ `0020`（2 字节 = 哈希长度 32）+ `<keccak256 哈希>`（32 字节）+ `<url 作为 UTF-8 hex>`

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
1. **忘记添加 `0020`** — 这个 2 字节的哈希长度用于区分哈希函数和实际哈希值。如果没有它，URL 的偏移量就会错误，导致解析器读取到无效数据，从而破坏整个配置文件。
2. **在上传到链上之前没有将文件固定到公共 IPFS 服务** — 本地 IPFS 节点无法被网关访问。务必通过服务（例如 Forever Moments Pinata 代理 `POST /api/pinata`）进行固定，并在提交链上交易之前验证文件是否可以通过 `https://api.universalprofile.cloud/ipfs/<CID>` 访问。
3. **哈希值必须与 IPFS 上存储的字节完全匹配** — 从上传的 JSON 字符串计算 keccak256 哈希值，而不是重新序列化的版本。
4. 在 LSP3 元数据 JSON 中使用 `hashFunction`/`hash` 而不是 `verification` 对象 — 图片条目（profileImage, backgroundImage）应使用 `{ "verification": { "method": "keccak256(bytes)", "data": "0x...", "url": "ipfs://..." }` 的格式，而不是旧的 `{ "hashFunction": "...", "hash": "0x..." }` 格式。

**LSP3Profile 数据键：** `0x5ef83ad9559033e6e941db7d7c495acdce616347d28e90c7ce47cbfcfcad3bc5`

### 更新 LSP3 配置文件元数据 — 完整流程

1. **读取当前配置文件** — `getData(LSP3_KEY)` → 解码 VerifiableURI → 从 IPFS 获取 JSON
2. **修改 JSON** — 更新字段（名称、描述、链接、图片等）
3. **对图片使用 `verification` 格式** — `{ verification: { method: "keccak256(bytes)", data: "0x...", url: "ipfs://..." }`
4. **将新图片固定到 IPFS** — 通过固定服务上传，获取 CID，验证是否可访问
5. **将更新后的 JSON 固定到 IPFS** — 上传文件，获取 CID，验证是否可以通过网关访问
6. **计算哈希值** — `keccak256(exactJsonBytes)`（上传文件的哈希值）
7. **编码 VerifiableURI** — `0x00006f357c6a0020` + 哈希值 + URL 的十六进制表示
8. **在链上设置** — 从控制器调用 `up.setData(LSP3_KEY, verifiableUri)`
9. **验证** — 从链上读取数据，解码，从 IPFS 获取，确认配置文件已正确加载

**在完成步骤 5 之前，切勿提交链上交易。**

**LSP28TheGrid 数据键：** `0x724141d9918ce69e6b8afcf53a91748466086ba2c74b94cab43c649ae2ac23ff`

## LSP28 — The Grid

用于配置文件/代币的可定制网格布局。存储在 LSP28 数据键中，格式为 VerifiableURI。

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

**网格类型：** `IFRAME`, `TEXT`, `IMAGES`, `X` (Twitter 嵌入), `INSTAGRAM`, `QR_CODE`, `ELFSIGHT`（自定义小部件）。
**推荐配置：** `gridColumns` 2–4, `width`/`height` 1–3。

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

**注意：** `setData` 载荷直接发送到 KeyManager — 不要用 `execute(CALL, self, setData(...))` 包装它。KeyManager 会自动将调用转发给 UP。只有针对其他合约的操作才需要使用 `execute()` 包装器。

## 网络配置

| | 主网 | 测试网 |
|---|---|---|
| 链路 ID | 42 | 4201 |
| RPC | `https://42.rpc.thirdweb.com` | `https://rpc.testnet.lukso.network` |
| 浏览器 | `https://explorer.lukso.network` | `https://explorer.testnet.lukso.network` |
| 中继 | `https://relayer.mainnet.lukso.network/api` | `https://relayer.testnet.lukso.network/api` |
| 代币 | LYX (18 dec) | LYXt (18 dec) |

## 安全性

### 权限最佳实践
- 授予最小权限。优先使用 `CALL` 而不是 `SUPER_CALL`。
- 使用 `AllowedCalls/AllowedERC725YDataKeys` 来限制访问。
- 除非绝对必要，否则避免使用 `DELEGATECALL` 和 `CHANGEOWNER`。
- 对于中继调用，使用有效时间戳。
- 首先在测试网（链 ID 4201）上进行测试。
- 严禁记录私钥。

### 密钥管理
- 限制密钥文件的权限：对所有凭证文件设置 `chmod 600`
- 私钥仅在签名时加载到内存中，之后立即清除
- 使用权限最小的专用控制器密钥 — 绝不要使用 UP 所有者密钥
- `config set` 命令仅限于安全密钥 — `keystorePath` 和 `profiles` 不能在运行时被修改，以防止路径重定向攻击
- 严禁记录、打印或传输私钥

### 网络访问

此技能仅与已知的 LUKSO 生态系统端点通信：
- **RPC：** `https://42.rpc.thirdweb.com`（主网），`https://rpc.testnet.lukso.network`（测试网）
- **中继：** `https://relayer.mainnet.lukso.network/api`（无 gas 交易）
- **IPFS：** `https://api.universalprofile.cloud/ipfs/`（元数据），`https://www.forevermoments.life/api/pinata`（固定文件）
- **Forever Moments API：** `https://www.forevermoments.life/api/agent/v1`（NFT 铸造）

不进行任何其他外部网络调用。所有交易签名都在本地完成。

## Forever Moments（NFT 瞬间与收藏）

Forever Moments 是 LUKSO 上的一个社交 NFT 平台。Agent API 允许您铸造 Moment NFT、创建收藏，并将图片固定到 IPFS — 所有操作都通过无 gas 中继完成。

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

1. **构建** — 调用构建端点 → 获取 `derived.upExecutePayload`
2. **准备** — 使用 `POST /relay/prepare` 和载荷 → 获取 `hashToSign` + `nonce`
3. **签名并提交** — 将 `hashToSign` 作为 RAW DIGEST 签名（不要使用 `signMessage()`）→ `POST /relay/submit`

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

| 端点 | 方法 | 用途 |
|----------|--------|---------|
| `/collections/build-join` | POST | 加入现有收藏 |
| `/collections/build-create` | POST | 创建收藏（步骤 1：LSP23 部署） |
| `/collections/finalize-create` | POST | 完成收藏创建（步骤 2：注册） |
| `/moments/build-mint` | POST | 在收藏中铸造 Moment NFT |
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

将 `metadataJson` 传递给 build-mint，API 会自动将其固定到 IPFS。

### 关于密钥的注意事项

- **签名：** `/relay/prepare` 返回的 `hashToSign` 已经是一个完整的哈希值 — 使用 `SigningKey.sign()` 进行签名，而不是 `wallet.signMessage()` |
- **铸造前需要加入收藏**：在铸造之前，您可能需要先加入一个收藏。如果加入收藏时出现 gas 估算错误，可能说明您已经是该收藏的成员 |
- **收藏创建分为两步：** `build-create`（通过 LSP23 部署合约）→ `finalize-create`（注册） |
- **已知收藏的 URL 格式：** `https://www.forevermoments.life/collections/<collectionAddress>` |

## 错误代码

| 代码 | 原因 |
|------|-------|
| `UP_PERMISSION_DENIED` | 控制器缺乏所需权限 |
| `UP_RELAY_FAILED` | 中继执行错误 — 请检查配额 |
| `UP_INVALID_SIGNATURE` | 使用错误的链 ID、nonce 或过期的时间戳 |
| `UP_QUOTA_EXCEEDED` | 月度中继配额已用完 |
| `UP_NOT_AUTHORIZED` | 地址不是控制器地址 — 请使用 [授权 UI](https://lukso-network.github.io/openclaw-universalprofile-skill/) |

## 依赖项

- Node.js 18+ / ethers.js v6
- `@lukso/lsp-smart-contracts` / `@erc725/erc725.js`（可选）

## 链接

- [LUKSO 文档](https://docs.lukso.tech/) · [Universal Everything（配置文件查看器）](https://universaleverything.io/) · [LSP6 规范](https://docs.lukso.tech/standards/access-control/lsp6-key-manager) · [授权 UI](https://lukso-network.github.io/openclaw-universalprofile-skill/)

**配置文件链接：** 始终使用 `https://universaleverything.io/<address>` 来链接到通用配置文件（而不是 universalprofile.cloud）。