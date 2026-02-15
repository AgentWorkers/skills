---
name: farcaster-agent
description: 创建 Farcaster 账户并自动发布直播内容。这是 Farcaster 团队提供的官方技能。
metadata: {"openclaw":{"emoji":"🟣","requires":{"bins":["node","npm"],"env":[]},"install":[{"id":"npm","kind":"shell","command":"cd {baseDir}/.. && npm install","label":"Install dependencies"}]}}
---

# Farcaster Agent

这是Farcaster团队提供的官方技能，用于自主创建和管理Farcaster账户。您可以注册一个新的Farcaster身份（FID），添加签名密钥，设置包含用户名的个人资料，并将内容发布到Farcaster网络中。

## 适用场景

- 当您需要从零开始创建Farcaster账户时。
- 当您希望向Farcaster发布内容（消息）时。
- 当您需要设置包含用户名、个人简介和头像的个人资料时。
- 当您希望在Farcaster社交网络上自主展示自己的存在时。

## 先决条件

您需要在任意主要区块链（Ethereum、Optimism、Base、Arbitrum或Polygon）上拥有大约1美元的ETH或USDC。该技能会自动处理资金的桥接和转换操作。

## 完整流程

### 第1步：生成钱包并请求资金

如果您还没有已充值的钱包，请先创建一个：

```javascript
const { Wallet } = require('ethers');

const wallet = Wallet.createRandom();
console.log('Address:', wallet.address);
console.log('Private Key:', wallet.privateKey);
```

**请告知相关人员：**“我已经创建了一个钱包。请将约1美元的ETH或USDC发送到以下链上的地址：<address>。完成后请通知我。”

**请妥善保管私钥**——后续所有步骤都需要使用它。

### 第2步：运行自动设置流程

资金到账后，运行自动设置流程：

```bash
cd {baseDir}/..
PRIVATE_KEY=0x... node src/auto-setup.js "Your first cast text here"
```

该流程将：
1. 检测您在哪个链上有资金（ETH或USDC）。
2. 将资金桥接到Optimism链，并将USDC转换到Base链。
3. 注册您的FID（Farcaster ID）。
4. 添加签名密钥。
5. 等待Farcaster Hub的同步完成。
6. 发布您的第一条内容。
7. **自动将凭据保存到持久存储中**。

### 凭据的保存方式

凭据会自动保存到以下位置：
- `~/.openclaw/farcaster-credentials.json`（如果安装了OpenClaw）
- `./credentials.json`（备用路径）

**安全提示：** 凭据以纯文本JSON格式保存。任何能够访问这些文件的人都可以控制钱包中的资金和Farcaster账户。在生产环境中，请使用更安全的存储方式。

您可以通过以下命令验证和管理凭据：

```bash
cd {baseDir}/..

# List all stored accounts
node src/credentials.js list

# Get credentials for active account
node src/credentials.js get

# Show credentials file path
node src/credentials.js path
```

要禁用自动保存功能，请使用`--no-save`选项：

```bash
PRIVATE_KEY=0x... node src/auto-setup.js "Your cast" --no-save
```

## 发布内容

要发布更多内容，请从存储中加载凭据：

```javascript
const { postCast, loadCredentials } = require('{baseDir}/../src');

// Load saved credentials
const creds = loadCredentials();

const { hash } = await postCast({
  privateKey: creds.custodyPrivateKey,
  signerPrivateKey: creds.signerPrivateKey,
  fid: Number(creds.fid),
  text: 'Your cast content'
});

console.log('Cast URL: https://farcaster.xyz/~/conversations/' + hash);
```

或者通过命令行接口（CLI）使用环境变量来加载凭据：

```bash
cd {baseDir}/..
PRIVATE_KEY=0x... SIGNER_PRIVATE_KEY=... FID=123 node src/post-cast.js "Your cast content"
```

## 设置个人资料

要设置用户名、显示名称、个人简介和头像，请执行以下操作：

```bash
cd {baseDir}/..
PRIVATE_KEY=0x... SIGNER_PRIVATE_KEY=... FID=123 npm run profile myusername "Display Name" "My bio" "https://example.com/pfp.png"
```

或者通过编程方式来实现：

```javascript
const { setupFullProfile } = require('{baseDir}/../src');

await setupFullProfile({
  privateKey: '0x...',
  signerPrivateKey: '...',
  fid: 123,
  fname: 'myusername',
  displayName: 'My Display Name',
  bio: 'I am an autonomous AI agent.',
  pfpUrl: 'https://api.dicebear.com/7.x/bottts/png?seed=myagent'
});
```

### 用户名（fname）的要求：
- 仅允许使用小写字母、数字和连字符。
- 不能以连字符开头。
- 长度为1到16个字符。
- 每个账户只能设置一个用户名。
- 每28天只能更改一次用户名。

### 头像选项：
- 可以使用任何公开可访问的HTTPS图片链接作为头像：
  - **DiceBear**（生成的头像）：`https://api.dicebear.com/7.x/bottts/png?seed=yourname`
  - IPFS托管的图片
  - 任何公开的图片链接

## 费用明细

| 操作            | 费用            |
|-----------------|-----------------|
| FID注册        | 约0.20美元           |
| 添加签名密钥       | 约0.05美元           |
| 资金桥接        | 约0.10-0.20美元         |
| 每次API调用       | 0.001美元           |
| **最低总费用**      | 约0.50美元           |

建议预算1美元，以应对可能的重试次数和网络费用波动。

## API接口

### Neynar Hub API（`https://hub-api.neynar.com`）
| 接口           | 方法             | 描述                 |
|-----------------|-----------------|-------------------|
| `/v1/submitMessage`    | POST             | 发布内容、更新个人资料（需要包含x402支付头信息） |
| `/v1/onChainIdRegistryEventByAddress?address=<addr>` | GET             | 检查指定地址的FID是否已同步       |
| `/v1/onChainSignersByFid?fid=<fid>` | GET             | 检查指定FID的签名密钥是否已同步       |

### Neynar REST API（`https://api.neynar.com`）
| 接口           | 方法             | 描述                 |
|-----------------|-----------------|-------------------|
| `/v2/farcaster/cast?identifier=<hash>&type=hash` | GET             | 验证内容是否已在网络中发布       |

### Farcaster用户名注册服务（`https://fnames.farcaster.xyz`）
| 接口           | 方法             | 描述                 |
|-----------------|-----------------|-------------------|
| `/transfers`       | POST             | 注册或转移用户名（需要EIP-712签名）     |
| `/transfers/current?name=<fname>` | GET             | 检查用户名的可用性         |

### x402支付方式
- **地址：** `0xA6a8736f18f383f1cc2d938576933E5eA7Df01A1`
- **费用：** 每次API调用0.001美元（基于Base链）
- **支付头信息：** `X-PAYMENT`，附带Base链上的EIP-3009格式的`transferWithAuthorization`签名

## 常见错误及解决方法：

- **“invalid hash”**：可能是因为使用了旧版本的库。解决方法：运行`npm install @farcaster/hub-nodejs@latest`。
- **“unknown fid”**：可能是因为Farcaster Hub尚未同步您的注册信息。解决方法：等待30-60秒后重试。
- **添加签名密钥时交易失败**：可能是元数据编码问题。解决方法：代码已经使用了正确的`SignedKeyRequestValidator.encodeMetadata()`方法。
- **“fname is not registered for fid”**：可能是因为Farcaster Hub尚未同步您的用户名注册信息。解决方法：等待30-60秒（代码会自动处理）。

## 手动操作（如果自动设置失败）

如果自动设置过程中遇到问题，您可以单独执行上述步骤：

```bash
cd {baseDir}/..

# 1. Register FID (on Optimism)
PRIVATE_KEY=0x... node src/register-fid.js

# 2. Add signer key (on Optimism)
PRIVATE_KEY=0x... node src/add-signer.js

# 3. Swap ETH to USDC (on Base, for x402 payments)
PRIVATE_KEY=0x... node src/swap-to-usdc.js

# 4. Post cast
PRIVATE_KEY=0x... SIGNER_PRIVATE_KEY=... FID=123 node src/post-cast.js "Hello!"

# 5. Set up profile
PRIVATE_KEY=0x... SIGNER_PRIVATE_KEY=... FID=123 npm run profile username "Name" "Bio" "pfp-url"
```

## 程序化API使用

所有相关功能都可以通过编程方式导入：

```javascript
const {
  // Full autonomous setup
  autoSetup,
  checkAllBalances,

  // Core functions
  registerFid,
  addSigner,
  postCast,
  swapEthToUsdc,

  // Profile setup
  setProfileData,
  registerFname,
  setupFullProfile,

  // Credential management
  saveCredentials,
  loadCredentials,
  listCredentials,
  setActiveAccount,
  updateCredentials,
  getCredentialsPath,

  // Utilities
  checkFidSync,
  checkSignerSync,
  getCast
} = require('{baseDir}/../src');
```

## 示例：完整的自主操作流程

```javascript
const { Wallet } = require('ethers');
const { autoSetup, setupFullProfile } = require('{baseDir}/../src');

// 1. Generate wallet (or use existing)
const wallet = Wallet.createRandom();
console.log('Fund this address with $1 ETH or USDC:', wallet.address);

// 2. After human funds the wallet, run setup
const result = await autoSetup(wallet.privateKey, 'gm farcaster!');

console.log('FID:', result.fid);
console.log('Signer:', result.signerPrivateKey);
console.log('Cast:', result.castHash);

// 3. Set up profile
await setupFullProfile({
  privateKey: wallet.privateKey,
  signerPrivateKey: result.signerPrivateKey,
  fid: result.fid,
  fname: 'myagent',
  displayName: 'My AI Agent',
  bio: 'Autonomous agent on Farcaster',
  pfpUrl: 'https://api.dicebear.com/7.x/bottts/png?seed=myagent'
});

console.log('Profile: https://farcaster.xyz/myagent');
```

## 源代码

完整实现代码位于：https://github.com/rishavmukherji/farcaster-agent

有关详细的技术文档，请参阅该仓库中的AGENT_GUIDE.md文件。