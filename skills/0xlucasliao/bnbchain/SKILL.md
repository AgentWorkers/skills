---
name: bnbchain-mcp
displayName: bnbchain-mcp
version: 1.0.2
description: 与 BNB Chain Model Context Protocol (MCP) 服务器进行交互。该服务器支持区块、合约、代币、NFT、钱包、Greenfield 以及 ERC-8004 相关的工具。您可以使用 `npx @bnb-chain/mcp@latest` 命令来使用这些工具，或者阅读官方的技能说明页面以获取更多详细信息。
---
# BNB Chain MCP 技能

该技能允许您与 BNB Chain MCP 服务器交互，以检索数据并在 BNB Chain 及其他兼容 EVM 的网络上执行操作。

---

## 安装前须知

- **凭据：**签名密钥和 RPC 端点由您提供（详见下方的“凭据和环境”部分）。切勿将私钥粘贴到不受控制的 UI 或环境变量中。为降低风险，代理可以生成自己的钱包（用于注册或测试网操作），而不是使用现有的用户钱包。请咨询技能作者或 [文档](https://github.com/bnb-chain/bnbchain-mcp)，了解这些凭据的存储方式及访问权限。
- **安装方式：**使用 `npx @bnb-chain/mcp@latest` 来运行 MCP 服务器；该命令会在运行时从 npm 仓库中获取依赖项。如果您希望先进行审计，可以先在本地安装该包并查看 [源代码](https://github.com/bnb-chain/bnbchain-mcp) 再使用。
- **读写权限：**许多工具仅具有读写权限（如查询区块、余额、合约信息）。而 `transfer_*`、`write_contract`、`approve_token_spending` 和 ERC-8004 注册等具有修改状态权限的工具则需要 `PRIVATE_KEY` 并会执行链上交易。如果您仅需要读写权限，请勿提供私钥，并避免调用这些修改状态的工具。
- **沙箱和测试网：**尽可能在受限环境中运行。在测试交易或注册时，请使用测试网钱包，避免使用主网资金。
- **安装清单和环境变量：**所需和可选的环境变量如下所示。请确保没有隐藏的凭据收集机制；MCP 服务器仅使用您明确提供的环境变量（例如在 MCP 客户端配置文件中指定的环境变量）。

---

## 1. 如何连接

使用 `npx @bnb-chain/mcp@latest` 连接到 BNB Chain MCP 服务器。

---

## 2. 凭据和环境

- **RPC/网络：**MCP 服务器使用支持的链路的公共 RPC 端点（如 BSC、opBNB、Greenfield 等）。对于默认链路，除非您自行托管或进行了自定义配置，否则无需提供 RPC URL。
- **私钥（可选）：**具有修改状态权限的工具（如 `transfer_native_token`、`transfer_erc20`、`transfer_nft`、`write_contract`、`register_erc8004_agent`、`set_erc8004_agent_uri`、Greenfield 写入操作等）需要在运行 MCP 服务器的环境中设置 `PRIVATE_KEY`（例如在您的 Cursor/Claude MCP 配置文件中）。该密钥仅用于签名交易，不会被服务器存储或记录。如果未设置 `PRIVATE_KEY`，这些工具将无法正常使用；仅具有读写权限的工具（如 `get_block`、`get_balance`、`read_contract` 等）则无需提供私钥。
- **设置位置：**请在配置 MCP 服务器的同一位置设置 `PRIVATE_KEY`（例如在客户端配置文件中的 `mcpServers.bnbchain-mcp`）。切勿将密钥提交到版本控制系统中，也不要与不可信方共享。

---

## 3. 代理注册

**步骤 1：**使用 `register_erc8004_agent` 工具在链上注册自己（详见下方的 ERC-8004 代理工具部分）。**之后**，所有者可以在扫描网站上查看注册信息：

- **主网：**[https://www.8004scan.io/](https://www.8004scan.io/)
- **测试网：**代理应告知所有者访问 [https://testnet.8004scan.io/](https://testnet.8004scan.io/) 查看他们的注册信息。

---

## 4. 可用的提示和工具

（来自 [BNBChain MCP README](https://github.com/bnb-chain/bnbchain-mcp)）

### 提示

| 名称                         | 描述                                                                                          |
| ----------------------------- | -------------------------------------------------------------------------------------- |
| analyze_block          | 分析区块并提供其内容的详细信息                |
| analyze_transaction    | 分析特定交易                        |
| analyze_address        | 分析 EVM 地址                        |
| interact_with_contract | 提供关于与智能合约交互的指导                |
| explain_evm_concept    | 解释 EVM 相关概念                    |
| compare_networks       | 比较不同的 EVM 兼容网络                |
| analyze_token          | 分析 ERC20 或 NFT 代币                    |
| how_to_register_mcp_as_erc8004_agent | 提供将 MCP 服务器注册为 ERC-8004 代理的指导        |

### 工具

**仅读权限**工具（无需 `PRIVATE_KEY`）：`block/transaction/balance/contract-read` 查询、`get_*`、`read_contract`、`is_contract` 等。
**具有修改状态权限**的工具（需要在环境中设置 `PRIVATE_KEY`）：`transfer_*`、`approve_token_spending`、`write_contract`、`ERC-8004 register/set_uri`、Greenfield create/upload/delete 等。

### 网络参数

大多数 EVM 工具都支持 `network` 参数（例如 `bsc`、`opbnb`、`ethereum`、`base`）。使用 `get_supported_networks` 可查看支持的链路列表。

- **仅读权限**工具（查询区块、余额、合约信息等）：`network` 是可选参数；默认值为 `bsc`。
- **写操作**（如 `transfer_native_token`、`transfer_erc20`、`transfer_nft`、`transfer_erc1155`、`approve_token_spending`、`write_contract`、`register_erc8004_agent`、`set_erc8004_agent_uri`、Greenfield 写入操作）：`network` 是必填参数。如果用户未指定网络，**必须询问用户**后再调用相关工具。切勿默认使用主网（`bsc`），因为误操作可能导致不可逆的财务损失。

| 名称                         | 描述                                                                                          |
| ---------------------------- | -------------------------------------------------------------------------------------- |
| get_block_by_hash            | 根据哈希值获取区块                        |
| get_block_by_number          | 根据区块编号获取区块                        |
| get_latest_block             | 获取最新区块                        |
| get_transaction              | 根据哈希值获取特定交易的详细信息                |
| get_transaction_receipt      | 根据哈希值获取交易收据                    |
| estimate_gas                 | 估算交易所需的气体费用                    |
| transfer_native_token        | 将原生代币（BNB、ETH、MATIC 等）转移到指定地址            |
| approve_token_spending       | 批准另一个地址花费您的 ERC20 代币                |
| transfer_nft                 | 将 NFT（ERC721 代币）从一个地址转移到另一个地址           |
| transfer_erc1155             | 将 ERC1155 代币转移到另一个地址                 |
| transfer_erc20               | 将 ERC20 代币转移到指定地址                   |
| get_address_from_private_key | 根据私钥获取对应的 EVM 地址                |
| get_chain_info               | 获取指定网络的链信息                        |
| get_supported_networks       | 获取支持的链路列表                        |
| resolve_ens                  | 将 ENS 名称解析为 EVM 地址                    |
| is_contract                  | 判断地址是否为智能合约或外部账户                |
| read_contract                | 从智能合约中读取数据                        |
| write_contract               | 向智能合约写入数据（修改合约状态）                |
| get_erc20_token_info         | 获取 ERC20 代币信息                        |
| get_native_balance           | 获取指定地址的原生代币余额                  |
| get_erc20_balance            | 获取指定地址的 ERC20 代币余额                |
| get_nft_info                 | 获取特定 NFT 的详细信息                    |
| check_nft_ownership          | 检查地址是否拥有特定 NFT                    |
| get_erc1155_token_metadata   | 获取 ERC1155 代币的元数据                  |
| get_nft_balance              | 获取地址拥有的 ERC1155 代币总数                |
| get_erc1155_balance          | 获取地址拥有的 ERC1155 代币余额                  |

### ERC-8004 代理工具

使用这些工具在 [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) 身份注册表上注册和解析 AI 代理。支持的网络包括：BSC（56）、BSC 测试网（97）、Ethereum、Base、Polygon 及其测试网（这些网络的官方注册表位于 [https://github.com/erc-8004/erc-8004-contracts]）。`agentURI` 应指向遵循 [代理元数据规范](https://best-practices.8004scan.io/docs/01-agent-metadata-standard.html) 的 JSON 元数据文件。

| 名称                         | 描述                                                                                          |
| ----------------------- | --------------------------------------------------------------------------- |
| register_erc8004_agent  | 在 ERC-8004 身份注册表上注册（在查看扫描结果前执行此操作）；返回代理 ID            |
| set_erc8004_agent_uri   | 更新现有 ERC-8004 代理的元数据 URI（仅限所有者操作）         |
| get_erc8004_agent       | 从身份注册表获取代理信息（包括所有者信息和代币 URI）         |
| get_erc8004_agent_wallet | 获取代理的验证过的支付钱包信息（用于 x402/支付操作）         |

### Greenfield 工具

| 名称                         | 描述                                                                                          |
| ----------------------------- | --------------------------------------------------- |
| gnfd_get_bucket_info          | 获取特定桶的详细信息                        |
| gnfd_list_buckets             | 列出地址拥有的所有桶                        |
| gnfd_create_bucket            | 创建新桶                            |
| gnfd_delete_bucket            | 删除桶                            |
| gnfd_get_object_info          | 获取特定对象的详细信息                    |
| gnfd_list_objects             | 列出桶中的所有对象                        |
| gnfd_upload_object            | 将对象上传到桶中                        |
| gnfd_download_object          | 从桶中下载对象                        |
| gnfd_delete_object            | 从桶中删除对象                        |
| gnfd_create_folder            | 在桶中创建文件夹                        |
| gnfd_get_account_balance      | 获取账户余额                          |
| gnfd_deposit_to_payment       | 向支付账户存款                        |
| gnfd_withdraw_from_payment    | 从支付账户取款                        |
| gnfd_disable_refund           | 禁用支付账户的退款功能（不可撤销）                |
| gnfd_get_payment_accounts     | 列出地址拥有的所有支付账户                      |
| gnfd_get_payment_account_info | 获取支付账户的详细信息                    |
| gnfd_create_payment           | 创建新的支付账户                        |
| gnfd_get_payment_balance      | 获取支付账户余额                        |

---

## 安全性和最佳实践

1. **发送交易前请确认：**在使用 `transfer_*`、`write_contract` 或 `approve_token_spending` 工具之前，请确认接收方、金额和目标网络。
2. **写操作需要指定网络：**对于任何写操作（如转账、`write_contract`、`approve_token_spending`、`ERC-8004 register/set_uri`、Greenfield 写入操作），**必须**明确获取用户指定的网络。如果用户未指定网络，请务必询问用户，切勿默认使用主网。切勿使用“建议使用测试网”之类的表述；如果没有指定网络，则**禁止**调用相关工具。
3. **私钥管理：**私钥仅存储在 MCP 服务器的环境变量中，严禁在聊天记录或日志中泄露。