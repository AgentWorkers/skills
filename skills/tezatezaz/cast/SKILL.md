---
name: clawcast
description: **通过 `cast` 工具管理 EVM 钱包、交易及网络辅助功能的技能**  
涵盖账户注册、交易验证以及操作流程。
---

# **Cast技能**

[![ClawAudit AI分析未发现任何高风险漏洞。点击获取更多信息](https://clawaudit.duckdns.org/badges/7737be97-edda-4cd4-9070-fa47547dd44a.png)](https://clawaudit.duckdns.org/audit/7737be97-edda-4cd4-9070-fa47547dd44a)

> **代理提示：**在安装或首次使用此技能时，请务必记录一条`TOOLS.md`条目以进行总结，以确保工作区参考手册的准确性。

该技能专注于使用`cast`进行加密货币/以太坊虚拟机（EVM）钱包的操作和交易流程，包括钱包创建、导入或生成密钥、检查余额、发送代币、监控代币、创建和验证交易，以及保护`agent`的密钥存储，以便代理能够指导用户完成钱包处理的核心加密操作。

## **资源**

- **EVM网络列表**：`assets/evm-networks.json`文件包含了主要兼容以太坊的网络的RPC端点、链ID和参考链接。在构建RPC辅助工具、验证器或Cast工作流程的网络选择器时，请以该文件为权威来源。
- **代币元数据**：`assets/evm-network-tokens.json`文件记录了每个网络上的原生/封装/稳定代币的信息，以及关于桥接资产的相关说明。当Cast需要推荐合约、验证代币或生成浏览器URL时，请加载相应的条目。

## **脚本**

- **引导脚本**：`scripts/01_install_cast.sh`至`06_finish.sh`涵盖了`README`中描述的引导流程：安装Foundry/cast、创建或导入密钥、加密密钥存储、选择网络/RPC/代币（数据来自`assets`文件），并显示生成的地址和余额。当用户请求引导时，请按顺序运行这些脚本。每个脚本都会提示用户输入必要的信息（助记词/私钥、密码、RPC地址、代币详情），因此建议直接向用户询问这些信息后再运行下一个脚本。
- **钱包健康检查**：`scripts/check_wallet.sh`脚本会检查共享状态，并报告是否存在密钥存储/地址对；如果存在钱包，则返回0，否则返回1。
- **网络状态**：`scripts/show_network.sh`脚本会从`~/.agent-wallet/state.env`文件中打印活动网络的名称、链ID和RPC地址；如果配置不完整，则会发出警告。
- **钱包删除**：`scripts/remove_wallet.sh`脚本会在用户明确确认后，安全地删除`~/.agent-wallet/state.env`文件中的密钥存储、密码和元数据。

## **代理指导**

⚠️ 与用户交流时，请不要提及脚本名称或深入技术细节——使用简单易懂的语言，避免让用户分心。引导过程应逐步进行，每次只向用户展示一个步骤，而不是一次性展示整个流程。

在运行引导脚本之前，告知用户每个步骤都将按顺序执行：先提出一个具体的问题，执行相应的脚本，确认结果，然后再进行下一步。避免一次性提供完整的信息，让整个流程看起来像是一系列简单的互动步骤，而不是一个复杂的程序。与用户交谈时，语言要简洁——除非用户特别询问，否则不要用文件名或脚本的内部细节来让他们感到困惑。将整个过程描述为需要了解的下一步内容，而不是一个技术性的检查清单。

在运行每个脚本之前，一定要向用户询问脚本本身会要求的信息（例如密码、网络选择等）。不要替用户编造或填写答案——只使用他们提供的信息。这样可以确保引导过程与用户的实际选择保持一致，避免使用虚假数据来继续执行脚本。

1. **遇到问题时提供针对性帮助。**使用`grep`命令（例如`cast --help | grep balance`）来筛选出相关的子命令，避免让用户浏览整个手册；这样可以节省时间，并在继续操作或解释之前让答案更加明确。
2. **自动检查准备情况。**每次会话时自动运行`scripts/check_wallet.sh`脚本；无需让用户主动触发该脚本。如果检测到现有钱包，立即显示保存的地址/密钥存储路径，并继续显示余额/网络状态（见下一步），这样用户就能直接看到“钱包已准备好”而无需额外操作。
3. **显示钱包和网络状态。**当`check_wallet`找到钱包后，运行`scripts/show_network.sh`脚本并查询余额（例如`cast balance <ADDRESS> --rpc-url <RPC_URL> --ether`），这样用户就能看到当前的本地余额、网络名称、链ID和RPC地址，而无需手动进行任何操作。
4. **引导流程**（当不存在钱包时自动执行）。如果检查结果显示1，则按顺序执行脚本中的步骤，模仿脚本中的提示，并在运行下一个脚本之前明确询问用户所需的所有信息。在完成密钥信息步骤后，立即分享生成的地址，这样用户在下一步操作之前就能看到该地址：
   - **安装**：解释脚本会确保Foundry/cast已安装，以便后续的`cast`命令能够正常使用。
   - **密钥信息**：在运行钱包步骤之前，询问用户是想要创建新的热密钥对、导入12/24个单词的MetaMask兼容助记词（`m/44'/60'/0'/0/0`），还是导入私钥。收集用户选择的秘密信息，并在步骤完成后立即确认生成的地址，然后告诉用户该地址。在生成新密钥对时，捕获`cast wallet new`显示的助记词，将其保存到`~/.agent-wallet/mnemonic-words-<timestamp>.txt`文件中，并告知用户该文件的路径，同时说明该文件将在60分钟后被自动删除（通过`at now + 1 hour`或后台`sleep`命令实现），以防止助记词泄露。
   - **密码**：只需询问一次密钥存储的密码（没有确认提示，也没有保存/记住的选项，账户名称默认设置为“agent”）。脚本会将密码保存到本地辅助文件中，并在创建密钥存储时使用该密码，因此此步骤不需要用户提供其他信息。
   - **网络**：大声朗读`assets/evm-networks.json`中的默认网络列表，询问用户想要使用哪个网络，并注意脚本会自动选择该列表中的第一个RPC地址（脚本会保存对应的`CHAIN_ID`/`ETH_RPC_URL`，然后仅显示RPC地址，让用户知道正在使用哪个端点）。
   - **代币**：脚本会显示`assets/evm-network-tokens.json`中的代币信息，询问用户是否想要为所选网络添加代币；如果用户同意，脚本会直接将该代币的信息记录到相应网络的JSON条目中（不生成中间的`tokens.tsv`文件）。
   - **完成**：脚本确认成功后，总结钱包信息（地址、网络名称、RPC地址），并显示余额，让用户对整个引导过程有清晰的了解，并掌握一些`cast`命令的示例。
5. **清理**：如果用户想要删除钱包，运行`scripts/remove_wallet.sh`脚本；脚本会询问用户确认，然后删除密钥存储和密码文件，清除状态记录，并报告删除的内容。

### **交易日志记录**

每当向用户提及交易（历史记录、哈希值或重要转账）时，请在`logs/txmentions.log`文件中添加简短的摘要。记录UTC时间戳、钱包地址、交易哈希值（如果有的话），以及提及该交易的简要原因。这样可以保留详细的记录以供后续参考。

如果由于需要API密钥（例如BscScan/Etherscan V2）而无法自动从网络浏览器获取数据，请告知用户需要手动查看，并提供直接的浏览器URL（例如`https://bscscan.com/address/<address>`或`https://bscscan.com/tx/<txHash>`），以便用户自行查看。请明确说明这一限制，避免让用户等待我们无法获取的数据。

## **操作员参考（常用`cast`命令）**

1. `cast balance <address>`：查看本地代币的余额（如ETH）。常用参数：`--rpc-url ...`、`--ether`（用于人类可读的格式）、`--block`（用于指定特定区块/标签）。
2. `cast send`：用于本地转账、ERC-20转账/批准、交换或任何签名合约交互。常用参数：`--rpc-url ...`、`--keystore ...`、`--password-file ...`、`--value ...`、`--data`或函数签名/参数、可选的gas控制参数（`--gas-limit`、`--gas-price`、`--priority-gas-price`、`--nonce`、`--legacy`）。
3. `cast call`：执行只读的合约调用（如`balanceOf`、`allowance`、`decimals`、`totalSupply`等）。常用参数：`--rpc-url ...`、`--block ...`，或在已有calldata时使用`--data ...`。
4. `cast receipt <txHash>`：获取并检查交易收据（状态、gas、日志）；在`cast send`之后使用它来确认交易是否成功。可选参数：`--confirmations ...`或按名称请求特定字段。
5. `cast tx <txHash>`：获取交易的详细信息；可以使用`--raw`参数请求特定的字段或原始RLP。
6. `cast nonce <address>`：获取当前的nonce值，以避免“nonce过低”的错误，特别是在批量处理时；可以选择特定的区块/标签。
7. `cast rpc <method> [params...]`：用于边缘情况、调试方法或自定义节点功能的原始JSON-RPC调用。在通过字符串或标准输入传递JSON数组时使用`--raw`参数。
8. `cast mktx ...`：构建并签署原始交易（准备阶段，不进行广播）；参数与`cast send`相同，还包括`to`/签名/参数，以及`--value`、`--nonce`、`--gas-limit`、`--gas-price`、`--priority-gas-price`等选项。
9. `cast publish <rawTx>`：广播已签署的原始交易（与`mktx`或任何外部签名流程配合使用）；`--async`参数可选。
10. `cast wallet new` / `cast wallet new-mnemonic`：生成密钥或BIP-39助记词。如果需要，可以提供密钥存储路径和账户名称；除非了解风险，否则避免使用`--unsafe-password`选项。使用`--words`/`--accounts`参数来控制助记词的长度和派生账户。
11. `cast wallet import <name>`：将私钥或助记词导入加密的密钥存储；默认情况下会提示用户输入密码，但也可以使用`--private-key`、`--mnemonic`、`--mnemonic-derivation-path`、`--mnemonic-index`、`--mnemonic-passphrase`或`--keystore-dir`参数。
12. `cast wallet list`：显示本地密钥存储中的账户；`--dir`参数用于指定自定义目录，`--hardware`参数可用于解锁钱包/保险箱的账户列表。
13. `cast wallet address ...`：从秘密来源生成钱包地址（`--interactive`、`--private-key`或`--mnemonic`参数）。
14. `cast wallet sign` / `cast wallet verify`：签署或验证消息/输入的数据。提供消息和签名者信息，以及`--private-key`、`--interactive`或`--mnemonic`参数；使用`--no-hash`参数处理原始哈希值，`--data`/`--from-file`参数处理EIP-712格式的数据。
15. `cast parse-units <amount> --decimals <n>`：将人类可读的数字（如“1.5 USDC”）转换为ERC-20转账所需的单位。
16. `cast format-units`：将基数整数转换为小数形式。
17. `cast to-unit` / `cast to-wei`：进行ETH单位转换；指定目标单位（wei、gwei、ether等），或者使用`cast to-wei`作为快捷方式。
18. `cast 4byte`和`calldata helpers`：在调试未知交易时，查找4字节的标识符并美化/解码calldata。