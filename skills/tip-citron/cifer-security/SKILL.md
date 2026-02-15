---
name: cifer-sdk
description: 使用 `cifer-sdk`（一个基于 Node.js 的 npm 包）实现抗量子攻击的加密功能。内容包括 SDK 的初始化、钱包的设置、密钥的生成、文本的加密/解密，以及在所有支持的区块链网络（Ethereum、Sepolia、Ternoa）上进行文件加密/解密。当用户提到 `CIFER`、`cifer-sdk`、抗量子攻击加密、ML-KEM、密钥生成或与区块链相关的加密数据/文件时，请参考本文档。
---

# CIFER SDK — 完整集成指南

## 概述

CIFER SDK 为区块链应用提供了抗量子攻击的加密方案（基于 ML-KEM-768 和 AES-256-GCM 算法）。加密所需的密钥对存储在链上：公钥存储在 IPFS 上，私钥则分散存储在多个安全节点（enclaves）中。

**软件包**: `cifer-sdk`（npm）
**支持的区块链网络**: Ethereum 主网（1）、Sepolia（11155111）、Ternoa（752025）
**Blackbox 服务地址**: `https://cifer-blackbox.ternoa.dev:3010`

完整的 API 参考请参见 [reference.md](reference.md)。

---

## 快速设置

```bash
npm install cifer-sdk ethers dotenv
```

在 `package.json` 文件中，必须将 `"type"` 设置为 `"module"`，以便支持 ESM（ESM 是一种模块导入机制）。

```javascript
import 'dotenv/config';
import { createCiferSdk, keyManagement, blackbox } from 'cifer-sdk';
import { Wallet, JsonRpcProvider } from 'ethers';
```

---

## 第 1 步：初始化 SDK

```javascript
const sdk = await createCiferSdk({
  blackboxUrl: 'https://cifer-blackbox.ternoa.dev:3010',
});

const chainId = 1; // Ethereum Mainnet (or 11155111 for Sepolia, 752025 for Ternoa)
const controllerAddress = sdk.getControllerAddress(chainId);
const rpcUrl = sdk.getRpcUrl(chainId);
```

调用 `sdk.getSupportedChainIds()` 可以获取所有支持的区块链网络列表。

---

## 第 2 步：创建钱包签名器（服务器端）

```javascript
const provider = new JsonRpcProvider(rpcUrl);
const wallet = new Wallet(process.env.PRIVATE_KEY, provider);

// Signer adapter — this is what the SDK expects
const signer = {
  async getAddress() { return wallet.address; },
  async signMessage(message) { return wallet.signMessage(message); },
};
```

对于浏览器钱包，建议使用内置的适配器进行操作：
```javascript
import { Eip1193SignerAdapter } from 'cifer-sdk';
const signer = new Eip1193SignerAdapter(window.ethereum);
```

---

## 第 3 步：创建密钥

创建密钥需要支付一定的费用（以原生代币形式）。请先检查账户余额。

```javascript
const fee = await keyManagement.getSecretCreationFee({
  chainId, controllerAddress, readClient: sdk.readClient,
});

const txIntent = keyManagement.buildCreateSecretTx({ chainId, controllerAddress, fee });

const tx = await wallet.sendTransaction({
  to: txIntent.to,
  data: txIntent.data,
  value: txIntent.value,
});
const receipt = await tx.wait();
const secretId = keyManagement.extractSecretIdFromReceipt(receipt.logs);
```

---

## 第 4 步：等待密钥同步

创建密钥后，节点集群会生成相应的密钥对（在 Ethereum 主网上通常需要 30–120 秒）。

```javascript
let ready = false;
while (!ready) {
  ready = await keyManagement.isSecretReady(
    { chainId, controllerAddress, readClient: sdk.readClient },
    secretId,
  );
  if (!ready) await new Promise(r => setTimeout(r, 5000));
}
```

或者，您也可以直接读取当前的密钥状态：
```javascript
const state = await keyManagement.getSecret(
  { chainId, controllerAddress, readClient: sdk.readClient },
  secretId,
);
// state.owner, state.delegate, state.isSyncing, state.publicKeyCid
```

---

## 第 5 步：加密文本

```javascript
const encrypted = await blackbox.payload.encryptPayload({
  chainId,
  secretId,
  plaintext: 'Your secret message',
  signer,
  readClient: sdk.readClient,
  blackboxUrl: sdk.blackboxUrl,
});
// Returns: { cifer, encryptedMessage }
```

---

## 第 6 步：解密文本

执行解密操作的用户必须是密钥的所有者或被授权的代理。

```javascript
const decrypted = await blackbox.payload.decryptPayload({
  chainId,
  secretId,
  encryptedMessage: encrypted.encryptedMessage,
  cifer: encrypted.cifer,
  signer,
  readClient: sdk.readClient,
  blackboxUrl: sdk.blackboxUrl,
});
// Returns: { decryptedMessage }
```

---

## 第 7 步：加密文件

文件加密操作是异步进行的，适用于 Node.js 18 及更高版本的程序，并且支持使用 `Blob` 对象。

```javascript
import { readFile, writeFile } from 'fs/promises';

const buffer = await readFile('myfile.pdf');
const blob = new Blob([buffer], { type: 'application/pdf' });

// Start encrypt job
const job = await blackbox.files.encryptFile({
  chainId, secretId, file: blob, signer,
  readClient: sdk.readClient, blackboxUrl: sdk.blackboxUrl,
});

// Poll until done
const status = await blackbox.jobs.pollUntilComplete(job.jobId, sdk.blackboxUrl, {
  intervalMs: 2000,
  maxAttempts: 120,
  onProgress: (j) => console.log(`${j.progress}%`),
});

// Download encrypted .cifer file (no auth needed for encrypt jobs)
const encBlob = await blackbox.jobs.download(job.jobId, { blackboxUrl: sdk.blackboxUrl });
await writeFile('myfile.pdf.cifer', Buffer.from(await encBlob.arrayBuffer()));
```

---

## 第 8 步：解密文件

```javascript
const encBuffer = await readFile('myfile.pdf.cifer');
const encBlob = new Blob([encBuffer]);

const decJob = await blackbox.files.decryptFile({
  chainId, secretId, file: encBlob, signer,
  readClient: sdk.readClient, blackboxUrl: sdk.blackboxUrl,
});

const decStatus = await blackbox.jobs.pollUntilComplete(decJob.jobId, sdk.blackboxUrl, {
  intervalMs: 2000, maxAttempts: 120,
});

// Download decrypted file (auth REQUIRED for decrypt jobs)
const decBlob = await blackbox.jobs.download(decJob.jobId, {
  blackboxUrl: sdk.blackboxUrl,
  chainId, secretId, signer, readClient: sdk.readClient,
});
await writeFile('myfile-decrypted.pdf', Buffer.from(await decBlob.arrayBuffer()));
```

---

## 列出现有密钥

```javascript
const secrets = await keyManagement.getSecretsByWallet(
  { chainId, controllerAddress, readClient: sdk.readClient },
  wallet.address,
);
// secrets.owned: bigint[]   — secrets you own
// secrets.delegated: bigint[] — secrets delegated to you
```

---

## 委派机制

您可以设置一个代理来执行解密操作（但代理无权加密或修改密钥）：
```javascript
const txIntent = keyManagement.buildSetDelegateTx({
  chainId, controllerAddress, secretId, newDelegate: '0xDelegateAddress',
});
await wallet.sendTransaction({ to: txIntent.to, data: txIntent.data });
```

取消代理授权：
```javascript
const txIntent = keyManagement.buildRemoveDelegationTx({
  chainId, controllerAddress, secretId,
});
```

---

## 重要说明

- **最低 SDK 版本要求**: 请使用 `cifer-sdk@0.3.1` 或更高版本。早期版本可能存在函数调用错误。
- **数据传输限制**: 文本加密的最大长度约为 16KB（使用 `encryptPayload` 函数）。对于较大规模的数据，请使用文件加密方式。
- **区块更新机制**: 如果区块编号过期，SDK 会自动重试最多 3 次。
- **密钥同步时间**: 在 Ternoa 上约为 30–60 秒，在 Ethereum 主网上约为 60–120 秒。
- **文件下载权限**: 加密文件的下载操作无需身份验证；解密文件的下载操作则需要具备签名权限（`signer`）以及 `readClient` 功能。
- **费用**: 创建密钥需要支付费用（以原生代币计，例如在 Ethereum 主网上约为 0.0005 ETH）。请先调用 `getSecretCreationFee()` 函数查询费用详情。
- **私钥安全**: 绝不要在前端代码中暴露私钥。对于 Node.js 环境，应使用服务器端的签名器来处理密钥操作。

## 错误处理

```javascript
import { isCiferError, isBlockStaleError } from 'cifer-sdk';

try {
  await blackbox.payload.encryptPayload({ ... });
} catch (error) {
  if (isBlockStaleError(error)) {
    // RPC returning stale blocks, SDK already retried 3x
  } else if (error instanceof SecretNotReadyError) {
    // Wait and retry
  } else if (isCiferError(error)) {
    console.error(error.code, error.message);
  }
}
```

---

## 完整示例代码

```javascript
import 'dotenv/config';
import { createCiferSdk, keyManagement, blackbox } from 'cifer-sdk';
import { Wallet, JsonRpcProvider } from 'ethers';

const sdk = await createCiferSdk({ blackboxUrl: 'https://cifer-blackbox.ternoa.dev:3010' });
const chainId = 1;
const controllerAddress = sdk.getControllerAddress(chainId);
const provider = new JsonRpcProvider(sdk.getRpcUrl(chainId));
const wallet = new Wallet(process.env.PRIVATE_KEY, provider);
const signer = {
  async getAddress() { return wallet.address; },
  async signMessage(msg) { return wallet.signMessage(msg); },
};

// Create secret
const fee = await keyManagement.getSecretCreationFee({ chainId, controllerAddress, readClient: sdk.readClient });
const txIntent = keyManagement.buildCreateSecretTx({ chainId, controllerAddress, fee });
const tx = await wallet.sendTransaction({ to: txIntent.to, data: txIntent.data, value: txIntent.value });
const receipt = await tx.wait();
const secretId = keyManagement.extractSecretIdFromReceipt(receipt.logs);

// Wait for sync
let ready = false;
while (!ready) {
  ready = await keyManagement.isSecretReady({ chainId, controllerAddress, readClient: sdk.readClient }, secretId);
  if (!ready) await new Promise(r => setTimeout(r, 5000));
}

// Encrypt & decrypt
const enc = await blackbox.payload.encryptPayload({
  chainId, secretId, plaintext: 'Hello CIFER!', signer,
  readClient: sdk.readClient, blackboxUrl: sdk.blackboxUrl,
});
const dec = await blackbox.payload.decryptPayload({
  chainId, secretId, encryptedMessage: enc.encryptedMessage, cifer: enc.cifer,
  signer, readClient: sdk.readClient, blackboxUrl: sdk.blackboxUrl,
});
console.log(dec.decryptedMessage); // "Hello CIFER!"
```