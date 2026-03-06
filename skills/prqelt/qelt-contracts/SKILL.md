---
name: QELT Contracts
description: Verify and inspect smart contracts on the QELT blockchain using the Mainnet Indexer verification API. Use when asked to verify Solidity source code, check if a contract is verified, retrieve ABIs, list compiler versions, poll a verification job, or submit multi-file contracts (with OpenZeppelin imports). Rate limit: 10 submissions/hour.
read_when:
  - Verifying a Solidity smart contract on QELT
  - Checking if a QELT contract address is already verified
  - Retrieving ABI or source code for a verified QELT contract
  - Listing supported Solidity compiler versions on QELT
  - Polling a contract verification job status
homepage: https://mnindexer.qelt.ai
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["curl"]}}}
allowed-tools: Bash(qelt-contracts:*)
---

# QELT 智能合约验证功能

QELT 主网索引器通过 REST API 提供生产级别的合约验证服务。支持 500 多个 Solidity 版本、构造函数参数、库链接、多文件合约（75 个以上文件）、`viaIR` 编译以及自动检测 EVM 版本。

**API 基址：** `https://mnindexer.qelt.ai`  
**速率限制：** 每个 IP 每小时最多 10 次验证请求  
**任务超时时间：** 600 秒（10 分钟）  
**状态轮询：** 无限制——可随时每 3–5 秒轮询一次  

## 安全注意事项  

- 请勿提交包含私钥或敏感信息的源代码。  
- 验证结果是永久性的——合约代码在验证后会公开。  
- 在提交之前务必检查合约是否已被验证（以避免占用速率限制）。  
- 即使状态显示为 `completed`，也不代表合约已通过验证——请务必检查 `result.verified === true`。  
- 状态轮询是无限次的——在任务仍在处理中时请勿重复提交。  

## 验证流程  

### 1. 首先检查合约是否已被验证  

```bash
curl -fsSL "https://mnindexer.qelt.ai/api/v2/contracts/0xCONTRACT/verification"
```  

如果 `verified` 的值为 `true`，则直接将现有的源代码/ABI 返回给用户，无需再次提交。  

### 2. 提交单文件合约  

```bash
curl -fsSL -X POST "https://mnindexer.qelt.ai/api/v1/verification/submit" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xCONTRACT",
    "sourceCode": "// SPDX-License-Identifier: MIT\npragma solidity ^0.8.20;\n...",
    "compilerVersion": "0.8.20",
    "contractName": "MyContract",
    "optimizationUsed": true,
    "runs": 200,
    "evmVersion": "shanghai",
    "constructorArguments": "0x000...",
    "libraries": {}
  }'
```  

响应格式：`{"success": true, "jobId": "uuid", "statusUrl": "/api/v1/verification/status/uuid"}`  

### 3. 提交多文件合约（包含导入语句）  

对于使用 OpenZeppelin 或其他 `import` 语句的合约：  

```bash
curl -fsSL -X POST "https://mnindexer.qelt.ai/api/v1/verification/submit-multi" \
  -H "Content-Type: application/json" \
  -d '{
    "address": "0xCONTRACT",
    "compilerVersion": "v0.8.17+commit.8df45f5f",
    "contractName": "MyToken",
    "optimizationUsed": true,
    "runs": 200,
    "viaIR": true,
    "evmVersion": "london",
    "mainFile": "contracts/MyToken.sol",
    "sourceFiles": {
      "contracts/MyToken.sol": "pragma solidity ^0.8.17; ...",
      "@openzeppelin/contracts/token/ERC20/ERC20.sol": "..."
    }
  }'
```  

### 4. 轮询验证状态  

```bash
curl -fsSL "https://mnindexer.qelt.ai/api/v1/verification/status/JOB_ID"
```  

状态变化：`pending` → `processing` → `completed` → `failed`  

**注意：** 当状态显示为 `completed` 时，务必检查 `result.verified === true`，因为这可能表示字节码不匹配。  

### 5. 获取编译器版本  

```bash
curl -fsSL "https://mnindexer.qelt.ai/api/v2/verification/compiler-versions"
```  

### 6. 获取 EVM 版本  

```bash
curl -fsSL "https://mnindexer.qelt.ai/api/v2/verification/evm-versions"
```  

**EVM 版本选择：**  
| Solidity 版本范围 | 对应的 EVM 版本 |  
|---------------|-------------|  
| 0.5.14 – 0.8.4 | `istanbul` |  
| 0.8.5 | `berlin` |  
| 0.8.6 – 0.8.17 | `london` |  
| 0.8.18 – 0.8.19 | `paris` |  
| 0.8.20 – 0.8.23 | `shanghai` |  
| 0.8.24+ | `cancun` |  

QELT 主网使用的是 `cancun` EVM 版本——对于 Solidity 0.8.24 及更高版本的合约，请使用 `cancun`。  

## 速率限制  

| API 端点 | 限制次数 |  
|----------|-------|  
| `POST /api/v1/verification/submit` | 每个 IP 每小时 10 次 |  
| `POST /api/v1/verification/submit-multi` | 每个 IP 每小时 10 次 |  
| `GET /api/v1/verification/status/:jobId` | 无限制 |  
| 其他所有 GET 端点 | 无速率限制 |  

**速率限制相关头部信息：** `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`, `Retry-After`  

## 常见错误及解决方法  

| 错误现象 | 可能原因 | 解决方法 |  
|---------|-------------|-----|  
| `verified: false`（尽管显示为 `completed`） | 编译器/优化参数设置不正确 | 确保使用正确的配置参数 |  
| HTTP 429 | 达到速率限制 | 等待 `Retry-After` 时间后重试（通常为 3600 秒） |  
| `status: "failed"` | 编译错误 | 查看 `message` 字段以获取详细信息 |  
| 超时（600 秒后） | 合约文件过大或使用了 `viaIR` 编译方式 | 正常现象；任务仍会完成 |  

## 最佳实践：  

1. 提交前先检查合约状态（使用 `GET /api/v2/contracts/:address/verification`）  
2. 对于包含 `import` 语句的合约，使用 `/submit-multi` 方法  
3. 如果在 Hardhat 配置中设置了 `viaIR: true`，请在提交时也设置 `viaIR: true`  
4. 每 3–5 秒轮询一次验证状态——避免重复提交未完成的请求  

## 开发者工具  

**Hardhat 插件：** `npm install --save-dev @qelt/hardhat-verify@latest`  

**CLI 工具：** `npm install -g qelt-verify` → `qelt-verify verify 0x... ./Contract.sol --compiler-version 0.8.20 --optimize`