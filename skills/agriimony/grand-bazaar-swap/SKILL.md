---
name: grand-bazaar-swap
description: 使用已部署的 AirSwap Swap 合同，在 Base 平台上执行并记录 Grand Bazaar 的 P2P 交易。包括可重复的工作流程，涵盖审批、EIP-712 签名、交易信息发布（包括铸造和深度链接）、交易执行以及跨 ERC20/ERC721/ERC1155 标准的验证过程。
---
# Grand Bazaar P2P 交易

本文档介绍了如何在 **Base 主网** 上使用已部署的 AirSwap `Swap` 合同执行 **代理对代理（agent-to-agent）交易**。

**发送方代币的标准路由规则** 如下：
- ERC20 到 ERC20 -> 使用 `SwapERC20` 合同（Base 主网地址：`0x95D598D839dE1B030848664960F0A20b848193F4`）
- ERC20 发送方（非 ERC20 到 ERC20 的路由） -> 使用 ERC20 发送方的 Swap 合同
- ERC721 发送方 -> 使用 ERC721 发送方的 Swap 合同
- ERC1155 发送方 -> 使用 ERC1155 发送方的 Swap 合同

发送方仍然是提交交易的钱包，并且必须满足所选 Swap 合同对发送方类型的限制。

## 已部署的合约
请参阅：`references/base-mainnet-deployments.md`

## 安全规则
- 绝不要在聊天中粘贴或记录私钥。
- 进行演示时建议使用新的测试钱包。
- 始终从少量交易开始。
- 在批准交易前，请验证代币地址。

## 工作流程

### 有利的接收方报价规则
当有人提出交易报价且价格对您来说非常划算时，应快速接受该报价，并进行安全检查。

请按照以下步骤操作：
1. 解析报价信息，查找 `GBZ1:<compressedOrder>`。
2. 解压并重新构建订单和签名。
3. 验证发送方钱包的地址和签名。
4. 运行发送方的预交易检查。
5. 如果检查通过，则执行交易。
6. 使用 Grand Bazaar 的成功模板回复报价：
  - `感谢您的交易 🤝`
  - `https://basescan.org/tx/<txHash>`
  - 将回复发布到原始报价的链接中。

这尤其适用于需要快速响应的直接报价情况，但安全预检查仍然是必须的。

### 有利的发送方出价规则
在与其他用户或代理协商时，主动提出有利的出价以提高交易成交的概率。

默认的出价策略：
- 从公平的市场价格开始，然后稍微偏向交易对手方。
- 保持交易金额和 gas 使用量在实际可行的范围内。
- 在协商过程中优先使用私密的定向订单，只有在对方请求时才公开订单信息。
- 设置合理的到期时间，以便快速做出决策并确保交易能够执行。
- 在发布订单之前，先在链上验证：
  - 在目标 Swap 合同上调用 `Swap.check(senderWallet, orderWithSignature)`。
  - 确保 `nonceUsed(signer, nonce) === false`。
- 在发送方流程中忽略 `SenderAllowanceLow`，因为发送方会在接收方发现报价后进行批准。
- 如果除了 `SenderAllowanceLow` 之外还有其他检查错误，禁止发布订单。
- 每次发布订单时都必须遵循以下两步流程：
  1) 发布包含详细信息的订单报价，格式为 `GBZ1:<compressedOrder>`。
     - 对于私密订单，通过 API 字段（`mentions`、`mentions_positions`）包含交易对手方的信息。
  2) 立即发布一个后续的嵌入链接，链接到 Grand Bazaar 的 `/c/<step1CastHash>`。

### 注意事项
- 绝不要绕过预交易或签名检查。
- 绝不要使用不安全的 gas 设置来强制执行交易。
- 不要超出配置的风险容忍度进行让步。

### 定价参数
请参阅：`references/pricing-params.md`
该文件包含了定价阈值、影响评估、协商步骤和执行安全限制的详细信息。

这是一个双方协议：
- 一个代理作为签名者（Signer）。
- 另一个代理作为发送方（Sender）。

### 0) 分配角色
- 签名者（Signer）设置交易条款并签署 EIP-712 订单。
- 发送方（Sender）在链上提交 `swap` 交易，并支付发送方的 ERC20 代币金额加上协议费用。

由于每个部署的 Swap 合同都有不可变的 `requiredSenderKind`，因此发送方的代币类型必须与路由到的合约类型相匹配。

### 0.1) 各方的职责
**签名者（Signer）的职责**：
- 决定交易条款并构建订单。
- 批准签名者的资产，并将其发送到 Swap 合同。
- 为订单生成 EIP-712 签名。
- 将签名的订单发送给发送方代理。

**必须执行的签名者批准步骤**：
- 在执行交易之前，始终进行签名者所需的批准流程。
- 在未检查链上余额是否足够之前，不要假设现有的余额已经足够。
- 对于 `SwapERC20`，签名者所需的金额是 `signerAmount + signerProtocolFee`，因为费用是从签名者的代币账户中支付的。
- 如果签名者的余额低于所需金额，请提交批准交易并等待确认后再签署订单。
- 发送方的余额不得阻止签名者的交易发布。在签名者的验证过程中忽略 `SenderAllowanceLow`。
- 如果签名者在没有获得批准的情况下尝试发布交易，视为无效的操作流程。

**协议费用的相关说明**：
- 旧版 Swap：协议费用在发送方一侧进行计算。
- SwapERC20：协议费用在签名者一侧进行计算。
- 在签名者/接收者界面上的显示：
  - 费用信息、调整后的金额预览和费用调整后的价值预览必须显示在实际支付费用的一方。
- 只有在选择了两种代币后，才能显示费用相关的预览信息。

**发送方（Sender）的职责**：
- 验证订单详情和到期时间。
- 确保发送方的 ERC20 余额足够支付订单金额和费用。
- 批准发送方的 ERC20 代币到 Swap 合同。
- 提交 `swap` 交易。
- 将交易哈希发送给签名者。

### 1) 确保账户余额充足
- 发送方需要 Base ETH 作为交易费用。
- 发送方需要发送方的 ERC20 代币。
- 签名者需要 Base ETH 作为交易费用。
- 签名者需要自己的代币，并且必须批准交易。

**发送方执行前的关键检查**：
- 验证签名者的代币余额至少为 `order.signer.amount`。
- 验证签名者用于 Swap 的余额至少为 `order.signer.amount`。
- 验证发送方的代币余额至少为 `order.sender.amount + protocolFee + affiliateAmount`。
- 验证发送方用于 Swap 的余额是否足够。
- 确认订单的到期时间有足够的缓冲时间。
- 估算交易所需的 gas 量，如果估算值超过 `MAX_GAS_LIMIT`，则中止交易。
- 将 `maxPriorityFeePerGas` 上限设置为当前 gas 价格的 10%。

### 2) 批准交易
- 发送方批准使用自己的 ERC20 代币进行交易。
- 签名者批准使用自己的代币进行交易。

### 3) 创建订单
订单字段包括：
- `nonce`：每个签名者唯一的标识符。
- `expiry`：以 Unix 秒为单位的时间戳。
- `protocolFee`：执行时必须与 `Swap.protocolFee()` 匹配。
- `signer`：订单的相关方信息。
- `sender`：订单的另一方信息。
- `affiliateWallet`、`affiliateAmount`：可选，目前设置为零。

### 4) 签署 EIP-712 订单
根据路由到的 Swap 合同，使用特定的域名和类型。

**旧版 Swap v4.2**：
- 域名：`SWAP`
- 版本：`4.2`
- chainId：`8453`
- 验证合约：路由到的旧版 Swap 合同地址。
- 订单类型：
  - `Order(uint256 nonce,uint256 expiry,uint256 protocolFee,Party signer,Party sender,address affiliateWallet,uint256 affiliateAmount)`
  - `Party(address wallet,address token,bytes4 kind,uint256 id,uint256 amount)`

**SwapERC20 v4.3**：
- 域名：`SWAP_ERC20`
- 版本：`4.3`
- chainId：`8453`
- 验证合约：`0x95D598D839dE1B030848664960F0A20b848193F4`
- 订单类型：
  - `OrderERC20(uint256 nonce,uint256 expiry,address signerWallet,address signerToken,uint256 signerAmount,uint256 protocolFee,address senderWallet,address senderToken,uint256 senderAmount)`

### 5) 执行交易
发送方调用：
- `swap(recipient, maxRoyalty, order)`

**推荐的默认值**：
- 在测试环境中，`recipient` 设置为发送方（`recipient = sender`）。
- 除非签名者的代币是 ERC2981 NFT，否则 `maxRoyalty` 设置为 0。

### 6) 确认交易
- 在 BaseScan 上检查交易哈希。
- 在交易前后检查账户余额。

### 7) 以 AirSwap Web 兼容的压缩格式分享订单
**Farcaster 提及规则**：
- 不要假设简单的 `@username` 文本就能创建提及记录。
- 通过 API 发布订单时，必须同时设置 `mentions` 和 `mentions_positions`：
  - `mentions`：目标 FIDs 的数组。
  - `mentions_positions`：UTF-8 字节偏移量。
- 重要提示：在使用 hub 的 `makeCastAdd` 方法时，不要在文本中重复处理地址。如果两个地址都存在，客户端可能会显示重复的地址。
- 在发送订单之前，必须根据 UTF-8 字节计算提及偏移量。
- 发送订单之前的验证规则：
  - `mentions.length === mentions_positions.length`。
- 每个偏移量都必须指向 `text` 中对应的 `@handle` 代币的开始位置。
- 对于私密订单的接收方，如果可用，请优先使用接收方的 Neynar `verified_addresses.primary.eth_address`。
- 如果没有可用的主要验证地址，则只能使用托管地址。

**长链接预算规则**：
- 在包含带有压缩订单查询参数的迷你应用链接时，尽量减少订单公告文本的长度。
- 优先使用迷你应用的链接，而不是在订单文本中直接嵌入原始的压缩数据。
- 如果需要遵守长链接长度限制，不要在同一条订单信息中同时包含长文本和原始的压缩数据。

**严格的订单解析格式**：
- 如果迷你应用通过订单哈希加载订单信息，必须在订单信息中包含一条专门的行：
  - `GBZ1:<compressedOrder>`
  - `GBZ1:` 必须大写，并且位于行的开头。
- 在 `<compressedOrder>` 内部不要有空格。
- 每条订单信息中只能包含一条 `GBZ1:` 行。
- 如果应用程序解析器无法识别这条行，应显示错误信息。

**NFT 订单的元数据和嵌入规则**：
- 在签名者步骤中，如果可能的话，包含 NFT 的元数据：
  - 优先使用合约元数据中的 NFT 符号作为元数据。
- 如果可用，将 NFT 图像嵌入到订单信息中。
- 对于包含两个 NFT 的订单，嵌入顺序如下：
  - `embed[0] = 签名者的 NFT 图像`
  - `embed[1] = 发送方的 NFT 图像`
- 如果只有一方涉及 NFT，只需嵌入一个 NFT 图像。

**人类可读的订单信息格式**：
- 第一步订单信息必须包含根据代币类型生成的自然语言摘要。
- 标准的格式如下：
  - `I offer <signer-leg text> for <sender-leg text>`
  - 根据代币类型的不同，格式如下：
    - ERC20：`I offer <amount> <symbol>`
    - ERC721：`I offer <symbol> #<tokenId>`
    - ERC1155：`I offer <qty>x <symbol> #<tokenId>`
- 示例：
    - ERC20 -> ERC20：`I offer 12 USDC for 0.005 WETH`
    - ERC721 -> ERC20：`I offer PFP #176 for 200 USDC`
    - ERC721 -> ERC721：`I offer 200 USDC for PFP #176`
    - ERC1155 -> ERC721：`I offer 3x GAMEITEM #42 for 10 USDC`
- 在摘要下方添加上下文信息：
    - 私密订单：`私密订单 • 在 <human-duration> 内到期`
    - 公开订单：`公开订单 • 在 <human-duration> 内到期`
- 机器生成的订单信息必须保持不变，并单独显示：
  - `GBZ1:<compressedOrder>`
- 通过 API 提及接收方时：
  - 不要仅依赖简单的处理地址。
  - 提供 `mentions` 和 `mentions_positions`，确保它们与 UTF-8 字节偏移量对齐。

**ERC721 订单和余额的处理（旧版 Swap）**：
- 在旧版 Swap 合同中，对于 ERC721 的发送方，代币数量通过 `id` 编码，`amount` 必须设置为 `0`。
- 当 ERC721 在发送方时，不要使用 `amount = 1`，否则可能会导致链上的 `AmountOrIDInvalid` 错误。
- 在当前测试的流程中，签名者的 ERC721 代币应编码为 `id=<tokenId>`，`amount=0`。

**ERC721 的批准流程（安全性和兼容性）**：
- 对于 ERC721，建议使用明确的批准方式：
  - `approve(swapContract, tokenId)`
- 不要依赖 `setApprovalForAll` 来处理 ERC721 的批准。
- 旧版 Swap 对 ERC721 的余额检查是 `getApproved(tokenId) == swapContract`。
- 因此，`isApprovedForAll` 仍然可以显示 `SignerAllowanceLow`。
- 对于 ERC721，UI/API 的余额检查必须使用 `getApproved(tokenId)`。

**ERC1155 的批准流程**：
- 使用 `setApprovalForAll(swapContract, true)` 来处理 ERC1155 的批准。

**类型路由规则**：
- 如果 UI 中的类型显示有延迟，但在选择批准路径之前，必须在链上确定代币的类型。
- 不要假设 `tokenId` 仅代表 ERC721；ERC1155 也可能涉及其他类型的代币。

**处理带有版税的 NFT（ERC2981）**：
- 如果签名者的代币支持 ERC2981，可以从发送方获取版税。
- 版税检查路径：
  - 在签名者代币上使用 `supportsInterface(0x2a55205a)`。
- `royaltyInfo(signerTokenId, senderAmountRaw)`。
- 单位是原始的发送方代币单位（例如 USDC）。
- 接收方在批准交易时必须包括：
  - `senderAmount + protocolFee + affiliateAmount + royaltyAmount`
- 旧版 Swap 的执行必须设置 `maxRoyalty` 不小于计算出的版税金额，否则会返回错误 `RoyaltyExceedsMax(...)`。

**社交发布和代理交接**：
- 使用 AirSwap Web 支持的压缩 ERC20 订单格式。
- 这是一个 URL 安全的压缩数据包，不是 keccak 哈希值。
- 由于压缩格式的限制，这个数据包可能太大，不适合在一条消息中发送。
- 在发送完整的压缩订单时，可以使用长链接。

**编码字段**：
- `chainId`
- `swapContract`
- `nonce`
- `expiry`
- `signerWallet`
- `signerToken`
- `signerAmount`
- `protocolFee`
- `senderWallet`
- `senderToken`
- `senderAmount`
- `v`
- `r`
- `s`

`signer_make_order.js` 现在将订单信息写入：
- `airswapWeb.compressedOrder`
- `airswapWeb.orderPath` 的格式为 `/order/<compressedOrder>`

`make_cast_payload.js` 将订单信息写入：
- `airswapWeb.orderUrl`，使用 URL 编码的压缩格式以生成可点击的链接。
- 原始的 `compressedOrder` 保持未编码状态，以便机器解析和执行。

### 8) 解压并处理收到的订单
- 如果您只收到压缩后的订单数据包，使用 AirSwap 的 `decompressFullOrderERC20(compressedOrder)` 函数进行解压。
- 建议在内存中处理解压后的数据，不要依赖本地 JSON 文件作为持久化存储。
- 使用 Farcaster 的订单数据作为标准的订单传输和存储方式。

如果您从 `make_cast_payload.js` 接收到结构化的订单数据包：
- 读取 `payload.airswapWeb.compressedOrder`。
- 解压数据包以恢复完整的订单信息和签名。
- 对于机器人执行，忽略任何人类可读的总金额，根据订单字段计算发送方需要支付的费用：
  - `feeAmount = order.sender.amount * order.protocolFee / 10000`
  - `totalRequired = order.sender.amount + feeAmount + order.affiliateAmount`

然后按照发送方的流程执行交易：
- 设置 `SENDER_PRIVATE_KEY`。
- 运行 `node scripts/sender_execute_order.js`。

发送方的执行脚本已经包含了以下检查：
- 到期时间检查。
- 对非公开订单的发送方钱包限制。
- EIP-712 签名的验证。
- 签名者的余额和余额的预检查。
- 发送方的余额和余额的预检查。

## 脚本
脚本位于 `scripts/` 目录下。
这些脚本是参考实现，可以由一个操作员使用两个密钥来运行进行测试。
在实际的代理对代理交易中，签名者和发送方应该分别运行各自的脚本。

**推荐的设置**：
- 使用 Node.js 20+ 版本。
- 在临时文件夹中安装依赖项：
  - `npm i ethers@5 lz-string`

然后运行以下脚本之一：
- `node scripts/signer_make_order.js`
- `node scripts/sender_execute_order.js`
- `node scripts/make_cast_payload.js` 以生成人类可读的订单信息和机器可读的数据包。
- `scripts/post_cast_farcaster_agent.js` 由于安全原因被禁用。
  - 原因：避免在共享的技能脚本审计中同时进行文件读取和网络发送操作。
- 使用 Neynar/OpenClaw 的发布路径。

**单机端到端测试**：
- `node scripts/test_weth_usdc_swap.js`

**详细信息和参数**：
请参阅 `scripts/README.md`。