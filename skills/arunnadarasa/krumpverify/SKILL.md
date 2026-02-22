---
name: clawhub-krump-verify
description: 该功能使AI代理（例如OpenClaw）能够理解并使用Krump Verify来验证Story IP上的链上舞蹈动作。当用户或代理需要验证舞蹈动作、通过USDC.k或x402/EVVM收据进行支付、调用KrumpVerify合约、与ClawHub（clawhub.ai）集成，或在Story Aeneid上构建类似的EVVM/x402应用程序时，可以使用此功能。
---
# ClawHub与Krump Verify：用于代理的验证功能

在使用[ClawHub](https://clawhub.ai/)和Krump Verify时，请参考本文档。该工具支持对舞蹈动作进行链上验证，验证结果会与注册的Story IP地址进行比对，并支持使用USDC.k或x402/EVVM支付方式进行结算。代理可以自主执行验证操作，人类用户也可以通过浏览器进行链上审计。

**想要构建类似的应用程序吗？**请参阅[docs/BUILDING_WITH_EVVM_X402_STORY_AENEID.md](../../../docs/BUILDING_WITH_EVVM_X402_STORY_AENEID.md)，其中详细介绍了使用EVVM/x402/USDC.k在Story Aeneid框架下构建应用程序的步骤、可能遇到的问题以及相应的解决方法。

---

## Krump Verify的功能

- **验证**：将舞蹈动作的数据哈希（moveDataHash）与注册的Story IP地址进行比对。费用将支付到智能合约的“treasury”账户中，验证结果会记录在链上，并生成`Verified(ipId, verifier, receiptHash, timestamp)`事件。
- **区块链**：使用的区块链是Story Aeneid（链ID为1315），浏览器地址为`https://aeneid.storyscan.io`。
- **费用**：支持使用USDC.k（小数点后6位）。默认的`verificationFee`值为1e6（即1 USDC.k），具体费用可通过`verificationFee()`函数获取。

---

## 两种支付方式

### 1. 直接支付（用户/代理在链上支付）

1. 用户/代理通过USDC.k合约调用`approve(KrumpVerify, verificationFee)`来批准支付。
2. 然后调用`verifyMove(ipId, moveDataHash, proof)`进行验证。合约会执行`transferFrom(msg.sender, treasury, verificationFee)`操作，并将支付记录在链上。

### 2. 使用x402/EVVM支付（更适合代理使用）

1. **为EVVM钱包充值**：首先使用USDC.k为EVVM钱包充值，然后调用`Treasury.deposit(USDC.k, amount)`。
2. 用户需要签署EIP-712格式的TransferWithAuthorization交易（域名为`adapter`），交易内容中必须包含`"pay"`字段，以及接收方地址、代币数量和金额等信息。执行者地址设置为`0x0`，并设置`isAsyncExec`为`false`。
3. 中继节点（具有`RECEIPT_SUBMITTER_ROLE`角色）会调用`payViaEVVMWithX402(...)`函数来提交支付记录。
4. 支付方随后调用`verifyMoveWithReceipt(ipId, moveDataHash, proof, paymentReceiptId)`进行验证。此时不会发生链上转账，支付记录仅被中继节点使用一次。`msg.sender`字段必须与支付记录中的`payer`字段相匹配。

---

## 使用x402支付时的注意事项

- 在使用x402支付时，确保支付记录中的`hash payload`包含`"pay"`字段；执行者地址必须设置为`0x0`；同时需要使用`sync nonce`进行交易，并将`isAsyncExec`设置为`false`。
- 在部署合约之前，必须设置智能合约的IP地址、许可证（如果需要的话）以及版税信息。
- 如果支付方没有足够的EVVM余额，必须先完成充值操作（即调用`Treasury.deposit`）才能使用x402支付。

---

## 关键数据类型

| 名称 | 类型 | 说明 |
|------|------|-------------|
| `ipId` | address | 注册的Story IP地址 |
| `moveDataHash` | bytes32 | 舞蹈动作数据的Keccak256哈希值 |
| `proof` | bytes | 可选字段，例如签名或验证所需的额外信息；也可以设置为`0x` |
| `paymentReceiptId` / `receiptId` | bytes32 | 中继节点提交的支付记录的唯一标识符 |
| `receiptHash` | bytes32 | 验证完成后返回的哈希值，每个验证请求都是唯一的 |

---

## KrumpVerify合约接口

- **读取操作**：`verificationFee()`、`paymentReceipts(bytes32)`（返回支付方信息、支付金额和支付记录的使用状态）、`receiptUsed(bytes32)`。
- **写入操作**：任何人都可以调用`verifyMove(ipId, moveDataHash, proof)`和`verifyMoveWithReceipt(ipId, moveDataHash, proof, paymentReceiptId)`。
- **具有`RECEIPT_SUBMITTER_ROLE`的用户**：可以调用`submitPaymentReceipt(receiptId, payer, amount)`来提交支付记录。
- **事件**：`Verified(ipId, verifier, receiptHash, timestamp)`、`PaymentReceiptSubmitted(receiptId, payer, amount)`。

代理可以通过`PaymentReceiptSubmitted(payer=user)`查询未使用的支付记录，并通过`paymentReceipts(receiptId).used == false`来过滤未使用的记录。

---

## 默认合约地址

- `KrumpVerify`：`0x012eD5BfDd306Fa7e959383A8dD63213b7c7AeA5`（可通过`VITE_KRUMP_VERIFY_ADDRESS`进行修改）。
- `KrumpVerifyNFT`：`0x602789919332d242A1Cb70d462CEbb570a53A6Ac`。
- `KrumpTreasury`：`0xa2e9245cE7D7B89554E86334a76fbE6ac5dc4617`。
- `USDC.k`：`0xd35890acdf3BFFd445C2c7fC57231bDE5cAFbde5`。
- `EVVM Treasury`：`0x977126dd6B03cAa3A87532784E6B7757aBc9C1cc`。
- `EVVM Core`：`0xa6a02E8e17b819328DDB16A0ad31dD83Dd14BA3b`；`EVVM原生x402适配器`的地址为`0xDf5eaED856c2f8f6930d5F3A5BCE5b5d7E4C73cc`。

---

## 中继节点（Relayer）

- **本地环境**：使用`relayer/`和`RELAYER_PRIVATE_KEY`配置，运行在端口7350上。本地环境的前端地址为`http://localhost:7350`。
- **生产环境**：使用Fly.io平台上的`krump-x402-relayer`服务（地址：`https://krump-x402-relayer.fly.dev`），需设置`fly secrets set RELAYER_PRIVATE_KEY=0x...`；前端地址同样为`https://krump-x402-relayer.fly.dev`。

---

## 合约部署

- 使用`script/DeployAll.s.sol`脚本部署`KrumpTreasury`、`KrumpVerify`（包含Story IP地址、许可证和版税信息）以及`KrumpVerifyNFT`合约。部署者会获得`RECEIPT_SUBMITTER_ROLE`角色；如果需要，可以通过环境变量`RELAYER_ADDRESS`将该角色分配给其他地址。
- 部署命令：`./deploy.sh`或`forge script script/DeployAll.s.sol:DeployAll --rpc-url https://aeneid.storyrpc.io --broadcast --gas-price 10000000000 --legacy`。详细信息请参阅[DEPLOY.md](../../DEPLOY.md)。

---

## 代理的自主性与人工审核

- **自主操作**：代理可以使用钱包（或委托他人代签）通过x402进行支付，然后让中继节点提交支付记录，最后调用`verifyMoveWithReceipt`进行验证。
- **人工审核**：所有验证操作和支付记录都会记录在链上，人类用户可以通过浏览器查看`Verified`/`PaymentReceiptSubmitted`事件以及`receiptUsed`/`paymentReceipts`状态来进行审核。
- **项目仓库**：所有相关合约和前端界面都存储在该仓库中，支持充值EVVM钱包、使用x402支付以及查看支付记录等功能。

---

## 快速参考

- **使用钱包支付进行验证**：先调用`approve(USDC.k)`，再调用`verifyMove(ipId, moveDataHash, proof)`。
- **使用支付记录进行验证**：调用`verifyMoveWithReceipt(ipId, moveDataHash, proof, paymentReceiptId)`（注意`msg.sender`必须与支付记录中的`payer`字段匹配）。
- **提交支付记录**：只有中继节点可以调用`submitPaymentReceipt(receiptId, payer, amount)`；此时需满足`amount >= verificationFee`且`payer`不为空的条件，同时确保支付记录尚未被提交。
- **关于x402支付的构建指南**：请参阅[docs/BUILDING_WITH_EVVM_X402_STORY_AENEID.md](../../../docs/BUILDING_WITH_EVVM_X402_STORY_AENEID.md)。

如需查看完整的合约和配置详情，请参阅项目仓库中的[README](../../../README.md)和[DEPLOY.md]文件，以及`src/KrumpVerify.sol`合约文件。