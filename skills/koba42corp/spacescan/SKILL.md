# Spacescan 技能

通过 Spacescan.io API 探索 Chia 区块链。

## 功能

- 查看区块和交易记录
- 检查地址余额
- 监控网络统计信息
- 搜索区块链数据
- 跟踪 CAT 代币和 NFT 的状态
- 获取 XCH 的价格

## ⚠️ 需要 API 密钥

Spacescan 需要一个 API 密钥。您可以在以下链接获取密钥：https://www.spacescan.io/apis

请设置环境变量：
```bash
export SPACESCAN_API_KEY=your_key_here
```

或者将其添加到您的 shell 配置文件（如 ~/.zshrc 或 ~/.bashrc）中：
```bash
echo 'export SPACESCAN_API_KEY=your_key_here' >> ~/.zshrc
source ~/.zshrc
```

## 命令

所有命令可以通过以下方式执行：
- 在 Telegram 中输入 `/scan <命令>`
- 在 Telegram 中输入 `/spacescan <命令>`
- 在 CLI 中输入 `scan <命令>`
- 在 CLI 中输入 `spacescan <命令>`

### 区块
```bash
/scan block latest          Get latest block
/scan block <height>        Get block by height
/scan block <hash>          Get block by hash
/scan blocks <start> <end>  Get block range
```

### 交易记录
```bash
/scan tx <id>               Get transaction details
```

### 地址
```bash
/scan address <addr>        Get address info
/scan address balance <a>   Get address balance
/scan address txs <addr>    Get recent transactions
```

### 代币
```bash
/scan coin <id>             Get coin details
```

### 网络信息
```bash
/scan stats                 Network statistics
/scan network               Network info
/scan space                 Network space (EiB)
/scan mempool               Mempool status
/scan price                 XCH price
```

### 代币
```bash
/scan cats                  List CAT tokens
/scan cat <id>              Get CAT details
```

### NFT
```bash
/scan nft <id>              Get NFT details
```

### 搜索
```bash
/scan search <query>        Search blockchain
/scan <long_hash>           Quick search
```

## 代理使用方法
```javascript
const { handleCommand } = require('./skills/spacescan');

// Requires SPACESCAN_API_KEY environment variable
const output = await handleCommand('block latest');
```

## API 客户端
```javascript
const SpacescanAPI = require('./skills/spacescan/lib/api');
const api = new SpacescanAPI('your-api-key');

// Get latest block
const block = await api.getLatestBlock();

// Get address balance
const balance = await api.getAddressBalance('xch1...');

// Get network stats
const stats = await api.getNetworkStats();

// Search
const result = await api.search('xch1...');
```

## 安装
```bash
cd skills/spacescan
npm install
chmod +x cli.js
npm link  # Makes 'scan' and 'spacescan' global
```

## 配置

**注意：** 请务必设置您的 API 密钥。

您可以在以下链接获取密钥：https://www.spacescan.io/apis

免费 tier 提供一定的使用限制。

## 示例

- **查看最新区块：**
```bash
/scan block latest
```

- **获取地址余额：**
```bash
/scan address balance xch1...
```

- **网络统计信息：**
```bash
/scan stats
```

- **XCH 价格：**
```bash
/scan price
```

## 支持

- Spacescan 官网：https://www.spacescan.io
- API 计划：https://www.spacescan.io/apis
- 错误报告：请提交到技能仓库（skill repository）