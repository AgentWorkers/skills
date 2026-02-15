---
name: create-token
description: **在Nad.fun上创建代币的指南**  
本指南涵盖了完整的4个步骤：上传图片、上传元数据、为 vanity 地址生成盐值（salt），以及通过 BondingCurveRouter 合同将代币部署到链上。
user-invocable: true
argument-hint: [name] [symbol]
---

# Nad.fun 代币创建流程

## 先决条件：具备 `monad-development` 技能

在继续之前，请检查是否已安装 `monad-development` 技能。如果未安装，请通过 ClawHub 进行安装：

```bash
clawhub search "monad"
```

从搜索结果中找到并安装 `monad-development` 技能。该技能是执行第 3 步和第 4 步中的钱包管理和链上操作所必需的。

---

请按照以下 4 个步骤帮助用户创建 Nad.fun 代币。每个步骤都依赖于前一步的输出结果。

## API 基本地址

**生产环境：** `https://api.nadapp.net`

## 合同地址

```
BondingCurveRouter = "0x6F6B8F1a20703309951a5127c45B49b1CD981A22"
Lens              = "0x7e78A8DE94f21804F7a17F4E8BF9EC2c872187ea"
```

---

## 第 1 步：上传图片

**POST** `/agent/token/image`

- **Content-Type：** `image/png`、`image/jpeg`、`image/webp` 或 `image/svg+xml`
- **Body：** 原始二进制图片数据（最大 5MB）
- **返回值：** `image_uri`（CDN URL）和 `is_nsfw`（布尔值）

```js
const imageResponse = await fetch("https://api.nadapp.net/agent/token/image", {
  method: "POST",
  headers: { "Content-Type": imageFile.type },
  body: imageFile,
});
const { image_uri, is_nsfw } = await imageResponse.json();
```

### 错误代码
| 状态 | 描述 |
|--------|-------------|
| 400 | 图片格式无效或图片缺失 |
| 413 | 图片大小超过 5MB 的限制 |
| 500 | NSFW 验证失败或上传失败 |

---

## 第 2 步：上传元数据

**POST** `/agent/token/metadata`

- **Content-Type：** `application/json`
- **需要：** 第 1 步中的 `image_uri`

### 请求体

**必填字段：**

| 字段 | 类型 | 约束条件 |
|-------|------|-------------|
| `image_uri` | string | 必须来自 `https://storage.nadapp.net/` |
| `name` | string | 1-32 个字符 |
| `symbol` | string | 1-10 个字符，仅支持字母和数字（`/^[a-zA-Z0-9]+$/`）

**可选字段：**

| 字段 | 类型 | 约束条件 |
|-------|------|-------------|
| `description` | string 或 null | 最多 500 个字符 |
| `website` | string 或 null | 必须以 `https://` 开头 |
| `twitter` | string 或 null | 必须包含 `x.com` 并以 `https://` 开头 |
| `telegram` | string 或 null | 必须包含 `t.me` 并以 `https://` 开头 |

```js
const metadataResponse = await fetch("https://api.nadapp.net/agent/token/metadata", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    image_uri,
    name: "My Token",
    symbol: "MTK",
    description: "An awesome token for the Nad.fun",
    website: "https://mytoken.com",
    twitter: "https://x.com/mytoken",
    telegram: "https://t.me/mytoken",
  }),
});
const { metadata_uri } = await metadataResponse.json();
```

### 错误代码
| 状态 | 描述 |
|--------|-------------|
| 400 | NSFW 状态未知、数据无效或验证失败 |
| 500 | 上传到存储或数据库失败 |

---

## 第 3 步：生成代币盐值（Salt）

**POST** `/agent/salt`

- **Content-Type：** `application/json`
- **需要：** 第 2 步中的 `metadata_uri`
- 返回一个以 `7777` 结尾的代币地址

### 请求体

| 字段 | 类型 | 描述 |
|-------|------|-------------|
| `creator` | string | 创建者的钱包地址（EVM 格式） |
| `name` | string | 代币名称（必须与元数据中的名称一致） |
| `symbol` | string | 代币符号（必须与元数据中的符号一致 |
| `metadata_uri` | string | 第 2 步中的元数据 URI |

```js
const saltResponse = await fetch("https://api.nadapp.net/agent/salt", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    creator: walletAddress,
    name: "My Token",
    symbol: "MTK",
    metadata_uri: metadataUri,
  }),
});
const { salt, address } = await saltResponse.json();
```

- **返回值：** `salt`（bytes32 十六进制字符串）和 `address`（带有 `7777` 后缀的代币地址）

### 错误代码
| 状态 | 描述 |
|--------|-------------|
| 400 | 参数无效 |
| 408 | 超时 - 达到最大迭代次数 |
| 500 | 服务器内部错误 |

---

## 第 4 步：在链上创建代币

使用前几步的数据调用 `BondingCurveRouter.create()` 方法。

### TokenCreationParams

```solidity
struct TokenCreationParams {
    string name;
    string symbol;
    string tokenURI;      // metadata_uri from Step 2
    uint256 amountOut;    // 0 for no initial buy, or use Lens.getInitialBuyAmountOut(amountIn)
    bytes32 salt;         // salt from Step 3
    uint8 actionId;       // always 1 (graduate to Capricorn V3)
}
```

```solidity
function create(TokenCreationParams calldata params) external payable returns (address token, address pool);
```

### 选项 A：不进行初始购买

仅发送部署费用作为 `msg.value`。

```js
const curve = new ethers.Contract(BONDING_CURVE_ADDRESS, BONDING_CURVE_ABI, signer);
const [deployFee,,] = await curve.feeConfig();

const params = {
  name, symbol,
  tokenURI: metadata_uri,
  amountOut: 0,
  salt,
  actionId: 1,
};

const tx = await router.create(params, { value: deployFee });
await tx.wait();
```

### 选项 B：进行初始购买

发送 `deployFee + amountIn` 作为 `msg.value`。使用 `Lens.getInitialBuyAmountOut(amountIn)` 来获取 `amountOut`。

```js
const lens = new ethers.Contract(LENS_ADDRESS, LENS_ABI, signer);
const expectedAmountOut = await lens.getInitialBuyAmountOut(amountIn);

const [deployFee,,] = await curve.feeConfig();

const params = {
  name, symbol,
  tokenURI: metadata_uri,
  amountOut: expectedAmountOut,
  salt,
  actionId: 1,
};

const tx = await router.create(params, { value: deployFee + amountIn });
await tx.wait();
```

---

## 用于链上操作的钱包

在第 3 步（生成盐值）和第 4 步（链上部署）中，使用 `monad-development` 技能提供的钱包。该技能负责所有钱包配置、私钥管理和 RPC 设置。在调用盐值 API 以及发送 `BondingCurveRouter.create()` 交易时，使用该技能提供的签名者和钱包地址（`creator` 字段）。

---

## 重要规则

1. **顺序流程** - 每个步骤都依赖于前一步的输出结果。
2. **NSFW 验证** - 第 1 步会自动检查图片是否适合公开展示；该验证结果会记录在元数据中。
3. **URL 验证** - 所有 URL 必须使用 HTTPS 协议。Twitter 的链接必须以 `x.com` 结尾，Telegram 的链接必须以 `t.me` 结尾。
4. **图片域名限制** - 元数据中仅接受来自 `https://storage.nadapp.net/` 的图片 URL。
5. **生成盐值** - 如果在指定迭代次数内找不到符合条件的代币地址，可能会超时。
6. **actionId** - 始终使用 `1`（表示使用 Capricorn V3 版本）。

## 代码生成注意事项：

- 除非用户另有指定，否则默认使用 `ethers` v6 语法。
- 在进行下一步之前，务必处理每个 API 调用中的错误。
- 第 3 步中的 `salt` 和第 2 步中的 `metadata_uri` 都是第 4 步所必需的。
- 在进行初始购买时，务必使用 `Lens.getInitialBuyAmountOut()` 来获取正确的 `amountOut` 值。