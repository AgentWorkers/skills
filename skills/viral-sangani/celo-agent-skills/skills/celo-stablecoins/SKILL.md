---
name: celo-stablecoins
description: **与 Celo 的稳定币生态系统协作**  
在 Celo 平台上使用 USDm、EURm、USDC、USDT 或其他区域性的 Mento 稳定币进行开发时，请参考本指南。
license: Apache-2.0
metadata:
  author: celo-org
  version: "1.0.0"
---

# Celo稳定币

本技能涵盖了在Celo区块链上使用稳定币的相关内容，包括Mento稳定币以及其他主要的稳定币。

## 使用场景

- 查看稳定币余额  
- 转移稳定币  
- 开发支付应用程序  
- 处理地区性货币  
- 在Celo上集成USDC或USDT  

## 稳定币分类  

### Mento稳定币  

Mento协议提供了与多种法定货币挂钩的去中心化稳定币：  

| 符号 | 货币 | 主网地址 |  
|--------|----------|-----------------|
| USDm | 美元 | 0x765de816845861e75a25fca122bb6898b8b1282a |  
| EURm | 欧元 | 0xd8763cba276a3738e6de85b4b3bf5fded6d6ca73 |  
| BRLm | 巴西雷亚尔 | 0xe8537a3d056da446677b9e9d6c5db704eaab4787 |  
| XOFm | 西非CFA法郎 | 0x73F93dcc49cB8A239e2032663e9475dd5ef29A08 |  
| KESm | 肯尼亚先令 | 0x456a3D042C0DbD3db53D5489e98dFb038553B0d0 |  
| PHPm | 菲律宾比索 | 0x105d4A9306D2E55a71d2Eb95B81553AE1dC20d7B |  
| COPm | 哥伦比亚比索 | 0x8a567e2ae79ca692bd748ab832081c45de4041ea |  
| GBPm | 英镑 | 0xCCF663b1fF11028f0b19058d0f7B674004a40746 |  
| CADm | 加元 | 0xff4Ab19391af240c311c54200a492233052B6325 |  
| AUDm | 澳元 | 0x7175504C455076F15c04A2F90a8e352281F492F9 |  
| ZARm | 南非兰特 | 0x4c35853A3B4e647fD266f4de678dCc8fEC410BF6 |  
| GHSm | 加纳塞地 | 0xfAeA5F3404bbA20D3cc2f8C4B0A888F55a3c7313 |  
| NGNm | 尼日利亚奈拉 | 0xE2702Bd97ee33c88c8f6f92DA3B733608aa76F71 |  
| JPYm | 日元 | 0xc45eCF20f3CD864B32D9794d6f76814aE8892e20 |  
| CHFm | 瑞士法郎 | 0xb55a79F398E759E43C95b979163f30eC87Ee131D |  

### 中心化稳定币  

| 符号 | 发行者 | 主网地址 | 小数位数 |  
|--------|--------|-----------------|----------|  
| USDC | Circle | 0xcebA9300f2b948710d2653dD7B07f33A8B32118C | 6 |  
| USDT | Tether | 0x48065fbbe25f71c9282ddf5e1cd6d6a887483d5e | 6 |  

### 其他稳定币  

| 符号 | 发行者 | 货币 | 主网地址 |  
|--------|--------|----------|-----------------|
| vEUR | VNX | 欧元 | 0x9346f43c1588b6df1d52bdd6bf846064f92d9cba |  
| vGBP | VNX | 英镑 | 0x7ae4265ecfc1f31bc0e112dfcfe3d78e01f4bb7f |  
| vCHF | VNX | 瑞士法郎 | 0xc5ebea9984c485ec5d58ca5a2d376620d93af871 |  
| USDM | Mountain Protocol | 美元（带收益） | 0x59D9356E565Ab3A36dD77763Fc0d87fEaf85508C |  
| USDA | Angle | 美元（带收益） | 0x0000206329b97DB379d5E1Bf586BbDB969C63274 |  
| EURA | Angle | 欧元（带收益） | 0xC16B81Af351BA9e64C1a069E3Ab18c244A1E3049 |  
| USDGLO | Glo Foundation | 美元（基于社会影响） | 0x4f604735c1cf31399c6e711d5962b2b3e0225ad3 |  
| BRLA | BRLA Digital | 巴西雷亚尔 | 0xfecb3f7c54e2caae9dc6ac9060a822d47e053760 |  
| COPM | Minteo | 哥伦比亚比索 | 0xC92E8Fc2947E32F2B574CCA9F2F12097A71d5606 |  
| G$ | GoodDollar | UBI Token | 0x62b8b11039fcfe5ab0c56e502b1c372a3d2a9c7a |  

## 测试网地址（Celo Sepolia）  

| 符号 | 测试网地址 |  
|--------|-----------------|  
| USDm | 0xdE9e4C3ce781b4bA68120d6261cbad65ce0aB00b |  
| EURm | 0xA99dC247d6b7B2E3ab48a1fEE101b83cD6aCd82a |  
| BRLm | 0x2294298942fdc79417DE9E0D740A4957E0e7783a |  
| XOFm | 0x5505b70207aE3B826c1A7607F19F3Bf73444A082 |  
| KESm | 0xC7e4635651E3e3Af82b61d3E23c159438daE3BbF |  
| PHPm | 0x0352976d940a2C3FBa0C3623198947Ee1d17869E |  
| COPm | 0x5F8d55c3627d2dc0a2B4afa798f877242F382F67 |  
| GBPm | 0x85F5181Abdbf0e1814Fc4358582Ae07b8eBA3aF3 |  
| CADm | 0xF151c9a13b78C84f93f50B8b3bC689fedc134F60 |  
| AUDm | 0x5873Faeb42F3563dcD77F0fbbdA818E6d6DA3139 |  
| ZARm | 0x10CCfB235b0E1Ed394bACE4560C3ed016697687e |  
| GHSm | 0x5e94B8C872bD47BC4255E60ECBF44D5E66e7401C |  
| NGNm | 0x3d5ae86F34E2a82771496D140daFAEf3789dF888 |  
| JPYm | 0x85Bee67D435A39f7467a8a9DE34a5B73D25Df426 |  
| CHFm | 0x284E9b7B623eAE866914b7FA0eB720C2Bb3C2980 |  
| USDT | 0xd077A400968890Eacc75cdc901F0356c943e4fDb |  

## 查看余额  

### 使用viem  

```typescript
import { createPublicClient, http, formatUnits } from "viem";
import { celo } from "viem/chains";

const publicClient = createPublicClient({
  chain: celo,
  transport: http("https://forno.celo.org"),
});

const ERC20_ABI = [
  {
    name: "balanceOf",
    type: "function",
    stateMutability: "view",
    inputs: [{ name: "account", type: "address" }],
    outputs: [{ type: "uint256" }],
  },
  {
    name: "decimals",
    type: "function",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint8" }],
  },
] as const;

// USDm (18 decimals)
const USDm = "0x765de816845861e75a25fca122bb6898b8b1282a";

const balance = await publicClient.readContract({
  address: USDm,
  abi: ERC20_ABI,
  functionName: "balanceOf",
  args: ["0xYourAddress"],
});

console.log("USDm Balance:", formatUnits(balance, 18));

// USDC (6 decimals)
const USDC = "0xcebA9300f2b948710d2653dD7B07f33A8B32118C";

const usdcBalance = await publicClient.readContract({
  address: USDC,
  abi: ERC20_ABI,
  functionName: "balanceOf",
  args: ["0xYourAddress"],
});

console.log("USDC Balance:", formatUnits(usdcBalance, 6));
```  

## 转移稳定币  

### 使用viem  

```typescript
import { createWalletClient, http, parseUnits } from "viem";
import { privateKeyToAccount } from "viem/accounts";
import { celo } from "viem/chains";

const account = privateKeyToAccount("0xYourPrivateKey");

const walletClient = createWalletClient({
  account,
  chain: celo,
  transport: http("https://forno.celo.org"),
});

const ERC20_ABI = [
  {
    name: "transfer",
    type: "function",
    stateMutability: "nonpayable",
    inputs: [
      { name: "to", type: "address" },
      { name: "amount", type: "uint256" },
    ],
    outputs: [{ type: "bool" }],
  },
] as const;

const USDm = "0x765de816845861e75a25fca122bb6898b8b1282a";

// Transfer 10 USDm
const hash = await walletClient.writeContract({
  address: USDm,
  abi: ERC20_ABI,
  functionName: "transfer",
  args: ["0xRecipientAddress", parseUnits("10", 18)],
});

console.log("Transaction hash:", hash);
```  

### 转移USDC（6位小数）  

```typescript
const USDC = "0xcebA9300f2b948710d2653dD7B07f33A8B32118C";

// Transfer 10 USDC (note: 6 decimals)
const hash = await walletClient.writeContract({
  address: USDC,
  abi: ERC20_ABI,
  functionName: "transfer",
  args: ["0xRecipientAddress", parseUnits("10", 6)],
});
```  

## 使用cast（Foundry）  

```bash
# Check USDm balance
cast call 0x765de816845861e75a25fca122bb6898b8b1282a \
  "balanceOf(address)(uint256)" \
  0xYourAddress \
  --rpc-url https://forno.celo.org

# Transfer USDm
cast send 0x765de816845861e75a25fca122bb6898b8b1282a \
  "transfer(address,uint256)" \
  0xRecipientAddress \
  10000000000000000000 \
  --rpc-url https://forno.celo.org \
  --private-key $PRIVATE_KEY
```  

## 小数处理  

| 代币类型 | 小数位数 | 1个代币的Wei值 |  
|------------|----------|----------------|  
| Mento（USDm、EURm等） | 18 | 1000000000000000000 |  
| USDC | 6 | 1000000 |  
| USDT | 6 | 1000000 |  

在格式化或解析金额之前，请务必检查代币的小数位数。  

## 获取测试代币  

1. 从Celo faucet获取CELO：https://faucet.celo.org  
2. 在Mento平台上将CELO兑换为稳定币：https://app.mento.org  

## 额外资源  

- [token-addresses.md](references/token-addresses.md) – 完整的代币地址参考