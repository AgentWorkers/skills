---
name: clawcast-wallet
description: **通过 `cast` 工具管理 EVM 钱包、交易及网络辅助功能的技能**  
涵盖用户注册、权限验证以及操作流程。
---

# **Cast技能**

> **代理提示：** 当安装或首次使用此技能时，请务必记录一条TOOLS.md条目以对其进行总结，以确保工作区快速参考手册的准确性。

该技能专注于使用`cast`进行加密货币/以太坊虚拟机（EVM）钱包操作和交易流程。它涵盖了钱包创建、导入、网络选择、代币管理以及各种交易辅助功能，从而帮助代理指导用户完成日常的加密货币相关任务。

## **资源**

- **EVM网络列表**：`assets/evm-networks.json`文件包含了主要兼容以太坊的网络的RPC端点、链ID和参考链接。在构建RPC辅助工具、验证器或Cast工作流程的网络选择器时，请以此作为权威来源。
- **代币元数据**：`assets/evm-network-tokens.json`文件记录了每个网络上的原生代币、封装代币和稳定代币的信息，以及关于桥接资产的相关说明。当Cast需要推荐合约、验证代币或生成浏览器URL时，会加载相应的条目。

## **脚本**

- **引导脚本**：`scripts/01_install_cast.sh`至`06_finish.sh`系列脚本涵盖了README中描述的引导流程：安装Foundry/cast工具，创建或导入密钥，加密密钥库，选择网络/RPC/代币（数据来源于`assets`文件夹中的JSON文件），并显示生成的地址和余额。当用户请求引导时，请按顺序运行这些脚本。每个脚本都会提示用户输入必要的信息（助记词/私钥、密码、RPC地址、代币详情），因此建议直接向用户询问这些信息后再执行下一个脚本。
- **钱包健康检查**：`scripts/check_wallet.sh`脚本会检查共享状态，并报告是否存在密钥库/地址对；如果存在钱包，则返回0，否则返回1。
- **网络状态**：`scripts/show_network.sh`脚本会从`~/.agent-wallet/state.env`文件中打印当前激活的网络名称、链ID和RPC地址；如果配置不完整，则会发出警告。
- **钱包删除**：`scripts/remove_wallet.sh`脚本会在用户明确确认后，安全地删除`~/.agent-wallet/state.env`文件中的密钥库、密码文件和元数据。

## **代理指导**

在运行引导脚本之前，需告知用户每个步骤都会按照以下流程进行：提出一个具体的问题，执行相应的脚本，确认结果，然后再进行下一步。避免一次性提供所有详细信息，让整个流程看起来像是一系列简单、交互式的步骤，而不是一个繁琐的程序。与用户交流时，请使用简单的语言——除非用户特别询问，否则不要用文件名或脚本的内部细节来让他们感到困惑。可以将这个过程描述为“接下来需要了解什么”，而不是一个技术性的检查清单。

在运行每个脚本之前，一定要向用户提出脚本本身会询问的问题（例如密码、网络选择等）。不要替用户编造或填写答案——只使用他们提供的信息。这样可以确保引导过程符合用户的实际选择，避免使用虚假数据继续执行脚本。

1. **遇到问题时提供针对性帮助**：可以使用`grep`命令将`cast --help`的输出结果过滤出来（例如`cast --help | grep balance`），以便快速找到相关的子命令，避免让用户翻阅整个手册；这样可以节省时间，并在继续操作或解释之前直接提供所需的信息。
2. **自动检查准备情况**：每次会话时自动运行`scripts/check_wallet.sh`脚本；无需用户主动触发。如果检测到已存在的钱包，立即显示保存的地址/密钥库路径，并继续显示余额/网络状态，这样用户就能立即看到“钱包已准备好”而无需额外操作。
3. **显示钱包和网络状态**：当`check_wallet`找到钱包后，运行`scripts/show_network.sh`脚本并查询余额（例如`cast balance <ADDRESS> --rpc-url <RPC_URL> --ether`），这样用户无需手动操作即可查看当前的余额、网络名称、链ID和RPC地址。
4. **引导流程**（当不存在钱包时自动执行）：如果检查结果显示钱包不存在，按顺序执行脚本中的步骤，模仿脚本中的提示，并在运行下一个脚本之前明确询问用户所需的所有信息。在完成密钥信息收集后，立即分享生成的地址，让用户在使用第3步之前的步骤中就能看到该地址：
   - **安装**：解释脚本会确保Foundry/cast已安装，以便后续的`cast`命令能够正常使用。
   - **密钥信息**：在运行钱包设置步骤之前，询问用户是想要创建新的热键对、导入12/24个单词的MetaMask兼容助记词（例如`m/44'/60'/0'/0/0`），还是导入私钥。收集用户选择的秘密信息，并在步骤完成后立即确认生成的地址，并告知用户该地址。
   - **密码**：只需询问一次密钥库密码（没有确认提示，也没有保存或记住密码的选项，账户名称默认设置为“agent”）。脚本会将密码保存到本地辅助文件中，并在创建密钥库时使用该密码，因此此步骤不需要用户提供其他信息。
   - **网络**：大声读出`assets/evm-networks.json`中的默认网络列表，询问用户选择哪个网络，并说明脚本会自动选择该列表中的第一个RPC地址（脚本会保存对应的`CHAIN_ID`/`ETH_RPC_URL`，然后仅显示RPC地址，让用户知道正在使用哪个端点）。
   - **代币**：脚本会显示`assets/evm-network-tokens.json`中的代币信息，询问用户是否要为所选网络添加代币；如果用户同意，脚本会直接将该代币的信息记录到相应网络的JSON文件中（不会生成中间的`tokens.tsv`文件）。
   - **完成**：在脚本确认成功后，总结钱包的详细信息（地址、网络名称、RPC地址），并运行余额查询，以便用户在使用完所有步骤后对整个流程有清晰的了解，并能尝试使用`cast`命令。
5. **清理**：如果用户想要删除钱包，运行`scripts/remove_wallet.sh`脚本；脚本会询问用户确认，然后删除密钥库和密码文件，清除状态记录，并报告删除的内容。

### **交易日志记录**

每当向用户提及交易（历史记录、哈希值或重要转账）时，请在`logs/txmentions.log`文件中添加简短的说明。记录UTC时间戳、钱包地址、交易哈希值（如果有的话），以及提及该交易的简要原因。这样可以保留详细的交易记录以供后续参考。

如果由于需要API密钥（例如BscScan/Etherscan V2）而无法自动从网络浏览器获取数据，请告知用户需要手动查看，并提供直接的浏览器URL（例如`https://bscscan.com/address/<address>`或`https://bscscan.com/tx/<txHash>`），以便用户自行查看。请明确说明这一限制，避免让用户等待我们无法获取的数据。

## **操作员参考（常用Cast命令）**

1. `cast balance <address>`：查看原生币种的余额（例如ETH）。常用参数：`--rpc-url ...`、`--ether`（用于人类可读的格式）、`--block`（用于指定特定区块/标签）。
2. `cast send`：用于原生转账、ERC-20转账、交换或任何签名合约交互。常用参数：`--rpc-url ...`、`--keystore ...`、`--password-file ...`、`--value ...`、`--data`或函数签名/参数、可选的gas控制选项（`--gas-limit`、`--gas-price`、`--priority-gas-price`、`--nonce`、`--legacy`）。
3. `cast call`：执行只读的合约调用（例如`balanceOf`、`allowance`、`decimals`、`totalSupply`等）。常用参数：`--rpc-url ...`、`--block ...`，或在已有calldata时使用`--data ...`。
4. `cast receipt <txHash>`：获取并检查交易收据（状态、gas使用情况等）；在`cast send`之后使用该命令确认交易是否成功。可选参数：`--confirmations ...`或按名称请求特定字段。
5. `cast tx <txHash>`：获取交易的详细信息；可以使用`--raw`参数请求特定的字段或原始RLP数据。
6. `cast nonce <address>`：获取当前的nonce值，以避免“nonce过低”的错误，尤其是在批量处理交易时；可以选择特定的区块/标签。
7. `cast rpc <method> [params...]`：用于边缘情况、调试方法或自定义节点功能的原始JSON-RPC调用。在通过字符串或标准输入传递JSON数组时使用`--raw`参数。
8. `cast mktx ...`：构建并签署原始交易（准备阶段，不进行广播）；参数与`cast send`相同，还包括`--value`、`--nonce`、`--gas-limit`、`--gas-price`、`--priority-gas-price`等选项。
9. `cast publish <rawTx>`：广播已签署的原始交易（通常与`mktx`一起使用）；`--async`参数可用于异步操作。
10. `cast wallet new` / `cast wallet new-mnemonic`：生成密钥或BIP-39格式的助记词。如果需要，可以提供密钥库路径和账户名称；除非了解相关风险，否则不要使用`--unsafe-password`选项。可以使用`--words`/`--accounts`参数来控制助记词的长度和生成的账户数量。
11. `cast wallet import <name>`：将私钥或助记词导入加密密钥库；默认情况下会提示用户输入密码，但也可以使用`--private-key`、`--mnemonic`、`--mnemonic-derivation-path`、`--mnemonic-index`、`--mnemonic-passphrase`或`--keystore-dir`参数。
12. `cast wallet list`：显示本地密钥库中的账户；`--dir`参数可用于指定自定义目录，`--hardware`参数可用于解锁Ledger/Trezor账户列表。
13. `cast wallet address ...`：根据提供的秘密信息生成钱包地址（`--interactive`、`--private-key`或`--mnemonic`参数）。
14. `cast wallet sign` / `cast wallet verify`：签署或验证消息/输入的数据。提供消息和签名者信息，以及`--private-key`、`--interactive`或`--mnemonic`参数；`--no-hash`参数用于处理原始哈希值，`--data`/`--from-file`参数用于处理EIP-712格式的文件。
15. `cast parse-units <amount> --decimals <n>`：将人类可读的数字（例如“1.5 USDC”）转换为ERC-20交易所需的单位。
16. `cast format-units`：将基础整数转换为对应的十进制数值。
17. `cast to-unit` / `cast to-wei`：进行ETH单位转换；可以指定目标单位（wei、gwei、ether等），或者使用`cast to-wei`作为快捷方式。
18. `cast 4byte`和calldata助手`：用于查找4字节的地址并格式化/解码calldata，特别是在调试未知交易时使用。