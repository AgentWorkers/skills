---
name: gizmolab-tools
description: 您可以在 [tools.gizmolab.io](http://tools.gizmolab.io) 上使用 GizmoLab 提供的免费区块链开发工具，在 [ui.gizmolab.io](http://ui.gizmolab.io) 上找到 Web3 UI 组件。Ethereum 相关的工具包括 Contract UI（用于与智能合约交互）、Transaction Decoder（用于解析交易数据）、ENS Lookup（用于查询以太坊名称服务中的地址信息）以及 Burner Wallet（用于销毁代币）。Solana 相关的工具包括 Token Creation（用于创建代币）、Token Minting（用于铸造代币）、Token Snapshots（用于生成代币快照）以及 Token Swaps（用于进行代币交易）。这些工具和组件适用于构建去中心化应用程序（dApps）、与智能合约进行交互或执行区块链操作。
---

# GizmoLab 工具与用户界面 (Tools & UI)

**工具 (Tools):** https://tools.gizmolab.io/ – 免费的区块链开发者工具  
**用户界面库 (UI Library):** https://ui.gizmolab.io/ – Web3 组件库  

## 可用工具 (Available Tools)  

### Ethereum 工具 (Ethereum Tools)  

| 工具 | URL | 功能 |  
|------|-----|---------|  
| 合同界面 (Contracts UI) | `/ethereum/contracts/ui` | 与任何智能合约交互（读写）  
| 交易解码器 (Transaction Decoder) | `/ethereum/converters/transaction-decoder` | 解码原始交易数据  
| ENS 查询 (ENS Lookup) | `/ethereum/ens/lookup` | 将 ENS 名称解析为地址  
| 燃烧钱包 (Burner Wallet) | `/ethereum/wallets/burner` | 生成临时钱包  

### Solana 工具 (Solana Tools)  

| 工具 | URL | 功能 |  
|------|-----|---------|  
| 创建代币 (Create Token) | `/solana/token/create` | 创建新的 SPL 代币  
| 铸造代币 (Mint Token) | `/solana/token/mint` | 向指定地址铸造代币  
| 代币快照 (Token Snapshot) | `/solana/token/snapshot/token` | 获取代币持有者信息  
| 交易对换 (Swap) | `/solana/swap` | 通过 Jupiter 进行代币交易  

## 使用方法 (Usage)  

所有工具均为基于 Web 的。可以使用浏览器直接访问这些工具进行操作。  

### 示例：ENS 查询 (Example: ENS Lookup)  
```
1. browser action=open targetUrl="https://tools.gizmolab.io/ethereum/ens/lookup"
2. browser action=snapshot  
3. Find the ENS input field, type the name
4. Click lookup/resolve button
5. browser action=snapshot to see result
```  

### 示例：交易解码器 (Example: Transaction Decoder)  
```
1. browser action=open targetUrl="https://tools.gizmolab.io/ethereum/converters/transaction-decoder"
2. browser action=snapshot
3. Paste raw transaction hex into input
4. Click decode button
5. browser action=snapshot to see decoded data
```  

### 示例：创建 Solana 代币 (Example: Create Solana Token)  
```
1. browser action=open targetUrl="https://tools.gizmolab.io/solana/token/create"
2. browser action=snapshot
3. Connect wallet when prompted
4. Fill token details (name, symbol, decimals, supply)
5. Click create and confirm transaction
```  

## 工具详情 (Tool Details)  

### 合同界面 (Contracts UI)  
- 输入合约地址和 ABI  
- 选择网络（Mainnet、Goerli、Sepolia 等）  
- 读取合约状态或执行交易  
- 支持所有兼容 EVM 的合约  

### 交易解码器 (Transaction Decoder)  
- 输入：原始交易十六进制数据（0x...）  
- 输出：解码后的函数调用、参数及返回值  
- 可处理任何类型的交易数据  

### ENS 查询 (ENS Lookup)  
- 正向查询：ENS 名称 → Ethereum 地址  
- 反向查询：地址 → ENS 名称  
- 显示解析器、注册者及合约有效期  

### 燃烧钱包 (Burner Wallet)  
- 生成随机私钥和地址  
- 仅用于测试  
- 严禁用于实际资金操作  

### Solana 代币创建 (Solana Token Create)  
- 创建新的 SPL 代币  
- 设置代币名称、符号、小数位数及初始发行量  
- 上传代币图片/元数据  
- 需要连接钱包（推荐使用 Phantom 或 Solflare）  

### Solana 代币铸造 (Solana Token Mint)  
- 铸造额外代币  
- 输入代币地址和铸造数量  
- 用户需具有代币管理权限  

### Solana 代币快照 (Solana Token Snapshot)  
- 获取所有代币持有者列表  
- 导出为 CSV 文件  
- 显示当前时间点的代币余额  

### Solana 交易对换 (Solana Swap)  
- 通过 Jupiter 平台进行代币交易  
- 自动匹配最优交易价格  
- 需要连接钱包才能执行交易  

## 支持的网络 (Supported Networks)  
**Ethereum:** Mainnet、Goerli、Sepolia、Base、Polygon、Arbitrum、Optimism、Avalanche、BNB Chain  
**Solana:** Mainnet、Devnet  

## 提示 (Tips)  
- 进行合约交互前，请准备好 ABI（可从 Etherscan 获取）  
- 交易解码器可离线使用（无需网络连接）  
- 燃烧钱包为临时账户，请在需要时保存私钥  
- Solana 工具需连接钱包（推荐使用 Phantom）  

---

# GizmoLab 用户界面 – Web3 组件库 (GizmoLab UI – Web3 Component Library)  
全栈 Web3 组件，用于构建去中心化应用（dApps）：https://ui.gizmolab.io/  

## 可用组件 (Available Components)  

| 组件 | URL | 功能 |  
|-----------|-----|---------|  
| 无 gas 费用 NFT 铸造组件 (Abstract Gasless NFT Mint) | `/components/abstract-gasless-nft-mint` | 无需 gas 费用即可铸造 NFT  
| 抽象登录组件 (Abstract Sign In) | `/components/abstract-sign-in` | 使用 Abstract Global Wallet 登录  
| 链路选择器组件 (Chain Selector) | `/components/chain-selector` | 用于切换区块链网络的弹出窗口  
| 加密产品卡片组件 (Crypto Product Card) | `/components/crypto-product-card` | 支持使用加密货币支付或自定义 ERC20 产品信息  
| NFT 铸造卡片组件 (NFT Mint Card) | `/components/nft-mint-card` | 集成智能合约的 NFT 铸造功能  
| NFT 投资组合组件 (NFT Portfolio) | `/components/nft-portfolio` | 查看 NFT 持有情况  
| LiFi 小部件 (LiFi Widget) | `/components/lifi-widget` | 支持跨链桥接和交易  
| Polymarket 小部件 (Polymarket Widget) | `/components/polymarket-widget` | 支持预测市场交易  

## 安装指南 (Installation Guides)  
详细安装指南请访问：https://ui.gizmolab.io/docs/  
- **安装 Abstract Global Wallet**：设置账户抽象层  
- **安装 Next.js 14**：配置 Next.js 项目  
- **安装 Dynamic**：实现动态钱包集成  
- **安装 Shadcn UI**：配置 Shadcn 用户界面  
- **部署 EVM 合约**：部署智能合约  

## 组件使用方法 (Using Components)  

### 1. 浏览组件 (Browse Components)  
```
browser action=open targetUrl="https://ui.gizmolab.io/components"
browser action=snapshot
```  

### 2. 查看组件详情 (View Component Details)  
每个组件页面包含：  
- 实时预览/演示  
- 安装说明  
- 可复制的代码片段  
- 属性/配置选项  

### 3. 示例：添加 NFT 铸造卡片 (Example: Add NFT Mint Card)  
```
1. Go to /components/nft-mint-card
2. Copy the installation command
3. Copy the component code
4. Configure with your contract address
5. Import and use in your dApp
```  

## 技术栈 (Tech Stack)  
组件基于以下技术构建：  
- **React / Next.js 14**  
- **Shadcn UI**（基于 Tailwind CSS）  
- **Wagmi / Viem**（用于 Ethereum 交互）  
- **账户抽象层（Account Abstraction）**  

## 测试环境 (Playground)  
可在：https://ui.gizmolab.io/playground 实时测试组件功能  

## 定制开发 (Custom Development)  
如需定制 Web3 组件或开发去中心化应用，请：  
- 预约咨询：https://calendly.com/gizmolab/30min  
- 联系我们：https://gizmolab.io/contact