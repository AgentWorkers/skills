---
name: streme-launcher
description: 在 Streme (streme.fun) 上启动代币——这是一个基于 Base 的流媒体代币平台。当部署带有内置质押奖励、Uniswap V3 流动性以及可选的代币锁定机制的 SuperTokens 时，可以使用该功能。该功能会在执行“launch token on streme”、“deploy streme token”、“create supertoken”或任何与 Streme 代币相关的部署任务时被触发。
---

# Streme Token Launcher

通过 Streme 的 V2 合同在 Base 上部署 SuperTokens。这些 Token 具备自动的 Uniswap V3 流动性、Superfluid 流媒体质押奖励，以及可选的锁定机制（vesting vault）。

## 快速入门

```typescript
import { createWalletClient, http, parseEther, encodeAbiParameters } from 'viem';
import { base } from 'viem/chains';
import { privateKeyToAccount } from 'viem/accounts';

// See references/contracts.md for full ABIs
const DEPLOYER = '0x8712F62B3A2EeBA956508e17335368272f162748';

const tokenConfig = {
  _name: 'My Token',
  _symbol: 'MYTOKEN',
  _supply: parseEther('100000000000'), // 100B
  _fee: 10000, // 10%
  _salt: '0x0...', // from generateSalt()
  _deployer: walletAddress,
  _fid: 0n, // Farcaster FID or 0
  _image: 'https://example.com/image.png',
  _castHash: 'deployment',
  _poolConfig: {
    tick: -230400,
    pairedToken: '0x4200000000000000000000000000000000000006', // WETH
    devBuyFee: 10000
  }
};

// Deploy with 10% staking (1 day lock, 365 day stream)
const stakingAlloc = createStakingAllocation(10, 1, 365);
await deployWithAllocations(tokenConfig, [stakingAlloc]);
```

## 合同地址（Base 主网）

| 合同 | 地址         |
|---------|------------|
| STREME_PUBLIC_DEPLOYER_V2 | `0x8712F62B3A2EeBA956508e17335368272f162748` |
| STREME_SUPER_TOKEN_FACTORY | `0xB973FDd29c99da91CAb7152EF2e82090507A1ce9` |
| STREME_ALLOCATIONHOOK | `0xC907788f3e71a6eC916ba76A9f1a7C7C19384c7B` |
| LP_FACTORY | `0xfF65a5f74798EebF87C8FdFc4e56a71B511aB5C8` |
| MAIN_STREME (用于生成盐值) | `0x5797a398fe34260f81be65908da364cc18fbc360` |
| WETH (Base) | `0x4200000000000000000000000000000000000006` |

## 部署流程

1. **生成盐值** - 调用 `generateSalt()` 函数以获取唯一的 Token 地址。
2. **上传 Token 图像** - 将 Token 的图像文件托管到指定的位置（详见下文关于图像托管的部分）。
3. **配置参数** - 创建 `tokenConfig` 和分配策略。
4. **进行部署** - 调用 `deployWithAllocations()` 函数完成部署。

## 图像托管

Token 的图像文件必须为公开可访问的 URL。可选的托管方式包括：

### IPFS（推荐）
```typescript
// Using Pinata
const pinata = new PinataSDK({ pinataJwt: PINATA_JWT });
const { IpfsHash } = await pinata.pinFileToIPFS(fileStream);
const imageUrl = `https://gateway.pinata.cloud/ipfs/${IpfsHash}`;
```

### Cloudinary
```typescript
import { v2 as cloudinary } from 'cloudinary';

const result = await cloudinary.uploader.upload(imagePath, {
  folder: 'tokens',
  transformation: [{ width: 400, height: 400, crop: 'fill' }]
});
const imageUrl = result.secure_url;
```

### 直接 URL
任何公开可访问的图像 URL 都可以。

### 图像文件要求：
- 格式：PNG、JPG、GIF、WebP
- 大小：小于 5MB（建议小于 1MB）
- 尺寸：建议为正方形（400x400）

### 上传脚本
```bash
# IPFS via Pinata
PINATA_JWT=xxx npx ts-node scripts/upload-image.ts pinata ./token.png

# Cloudinary
CLOUDINARY_CLOUD_NAME=xxx CLOUDINARY_API_KEY=xxx CLOUDINARY_API_SECRET=xxx \
  npx ts-node scripts/upload-image.ts cloudinary ./token.png

# imgBB (free)
npx ts-node scripts/upload-image.ts imgbb ./token.png
```

## 分配策略

### 质押分配（类型 1）
将 Token 分配给质押者，并随着时间逐步释放。

```typescript
function createStakingAllocation(
  percentage: number,    // % of supply (e.g., 10)
  lockDays: number,      // min stake duration
  flowDays: number,      // reward stream duration
  delegate?: string      // optional admin address
) {
  const lockSec = lockDays * 86400;
  const flowSec = flowDays * 86400;
  
  return {
    allocationType: 1,
    admin: delegate || '0x0000000000000000000000000000000000000000',
    percentage: BigInt(percentage),
    data: encodeAbiParameters(
      [{ type: 'uint256' }, { type: 'int96' }],
      [BigInt(lockSec), BigInt(flowSec)]
    )
  };
}
```

### 锁定分配（类型 0）
将 Token 锁定在特定账户中，并设置可选的解锁条件。

```typescript
function createVaultAllocation(
  percentage: number,     // % of supply
  beneficiary: string,    // recipient address
  lockDays: number,       // lockup (min 7 days)
  vestingDays: number     // vesting after lock
) {
  const lockSec = Math.max(lockDays, 7) * 86400;
  const vestSec = vestingDays * 86400;
  
  return {
    allocationType: 0,
    admin: beneficiary,
    percentage: BigInt(percentage),
    data: encodeAbiParameters(
      [{ type: 'uint256' }, { type: 'uint256' }],
      [BigInt(lockSec), BigInt(vestSec)]
    )
  };
}
```

### 分配规则：
- 质押比例 + 锁定比例合计不得超过 100%。
- 剩余部分将分配给 Uniswap V3 的流动性池（LP）。
- Token 的锁定期限至少为 7 天。
- 标准配置：10% 用于质押，90% 用于流动性池。

## Token 配置默认值

| 参数          | 值         |
|---------------|------------|
| 总供应量       | 100,000,000,000 (1000 亿) |
| 创建者费用       | 10,000 (10%)     |
| 开发者购买费用     | 10,000 (10%)     |
| 每次交易费用     | -23,040       |
| 配对 Token      | WETH         |

## API 端点

```bash
# Get tokens by deployer
GET https://api.streme.fun/api/tokens/deployer/{address}

# Search all tokens
GET https://api.streme.fun/api/tokens

# Token details
GET https://api.streme.fun/api/tokens/{address}
```

## 完整实现

完整的部署脚本请参见 `scripts/deploy-token.ts`。
完整的 ABI（Application Binary Interface）和类型定义请参见 `references/contracts.md`。

## 常见部署模式

### 标准部署（10% 用于质押）
```typescript
const allocations = [createStakingAllocation(10, 1, 365)];
```

### 带有团队锁定机制的部署（10% 用于质押 + 10% 用于锁定）
```typescript
const allocations = [
  createStakingAllocation(10, 1, 365),
  createVaultAllocation(10, teamAddress, 30, 365)
];
```

### 最大流动性配置（无额外分配）
```typescript
const allocations = [];
// 100% goes to Uniswap V3 LP
```