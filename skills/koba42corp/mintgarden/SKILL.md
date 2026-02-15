# MintGarden 技能

通过 MintGarden API 浏览、搜索和分析 Chia NFT（非同质化代币）。

## 功能概述

- 搜索 NFT 和收藏品
- 查看收藏品统计信息、最低售价、交易量
- 跟踪 NFT 的所有权和交易历史
- 监控最近的交易和活动
- 获取热门收藏品和顶级交易者信息
- 访问用户个人资料和投资组合

## 命令

所有命令可以通过以下方式执行：
- 在 Telegram 中输入 `/mg <命令>`
- 在 Telegram 中输入 `/mintgarden <命令>`
- 在 CLI（命令行接口）中输入 `mg <命令>`
- 在 CLI 中输入 `mintgarden <命令>`

### 搜索

```bash
/mg search <query>              # Search everything
/mg search nfts "rare zombie"   # Search NFTs only
/mg search collections "pixel"  # Search collections only
```

### 收藏品

```bash
/mg collections list            # Top collections by volume
/mg collection <id>             # Collection details
/mg collection nfts <id>        # NFTs in collection
/mg collection stats <id>       # Collection statistics
/mg collection activity <id>    # Recent sales/transfers
```

### NFT

```bash
/mg nft <launcher_id>           # NFT details
/mg nft history <launcher_id>   # Trade history
/mg nft offers <launcher_id>    # Active offers
```

### 个人资料

```bash
/mg profile <username>          # Profile details
/mg profile nfts <username>     # User's NFTs
/mg profile activity <username> # User's recent activity
```

### 事件与统计信息

```bash
/mg events                      # Recent global activity
/mg events <collection_id>      # Collection-specific events
/mg stats                       # Global marketplace stats
/mg trending                    # Trending collections (24h)
/mg top collectors              # Top collectors (7d)
/mg top traders                 # Top traders (7d)
```

### 快捷键

```bash
/mg col1abc...                  # Quick collection lookup
/mg nft1abc...                  # Quick NFT lookup
/mg did:chia:...                # Quick profile lookup
```

## 用户代理使用说明

当用户询问关于 Chia NFT、收藏品或 MintGarden 的信息时：

```javascript
const { handleCommand } = require('./skills/mintgarden');

// Natural language → formatted response
const output = await handleCommand('show me trending collections');
```

该技能负责：
- 命令解析与标准化
- 发起 API 调用并处理错误
- 生成格式化的文本输出（适用于 CLI 和 Telegram）
- 对大量结果进行分页显示

## API 客户端

如需自定义集成，请直接使用 API 客户端：

```javascript
const MintGardenAPI = require('./skills/mintgarden/lib/api');
const api = new MintGardenAPI();

// Search
const results = await api.search('zombie');
const nfts = await api.searchNFTs('rare', { limit: 50 });

// Collections
const collections = await api.getCollections({ sort: 'volume_7d' });
const collection = await api.getCollection('col1abc...');
const stats = await api.getCollectionStats('col1abc...');

// NFTs
const nft = await api.getNFT('nft1abc...');
const history = await api.getNFTHistory('nft1abc...');

// Profiles
const profile = await api.getProfile('username');
const profileNFTs = await api.getProfileNFTs('did:chia:...');

// Events
const events = await api.getEvents({ limit: 20 });
const trending = await api.getTrending({ period: '24h' });

// Stats
const globalStats = await api.getGlobalStats();
const topCollectors = await api.getTopCollectors({ period: '7d' });
```

## 安装

```bash
cd skills/mintgarden
npm install
chmod +x cli.js
npm link  # Makes 'mg' and 'mintgarden' global
```

## 配置

无需 API 密钥——MintGarden API 是公开的。

**可选设置：** 通过环境变量设置自定义基础 URL：

```bash
export MINTGARDEN_API_URL=https://api.mintgarden.io
```

## 输出格式

所有命令返回的文本格式适用于：
- 命令行终端
- Telegram 消息
- Discord 消息
- WhatsApp 消息

**注意：** 为保证 WhatsApp 的兼容性，输出内容不包含 Markdown 表格格式。

## 错误处理

- 无效的 ID → 显示清晰的错误信息
- API 请求失败 → 提供重试提示
- 网络问题 → 30 秒后自动超时
- 没有找到结果 → 显示“未找到”的提示信息

## 限制

- 默认每条查询返回 50 个结果
- 最大查询结果数量为 100 个
- 无请求速率限制（MintGarden 的设计较为宽松）
- 可通过 API 客户端实现分页功能

## 使用示例

- **在收藏品中查找稀有 NFT：**
```bash
/mg collection nfts col1abc...
```

- **查看最低售价：**
```bash
/mg collection col1abc...
```

- **查看热门 NFT：**
```bash
/mg trending
```

- **跟踪特定 NFT 的交易情况：**
```bash
/mg nft history nft1abc...
```

- **监控市场动态：**
```bash
/mg events
```

## 使用技巧

- 使用快捷键快速查询（直接粘贴 ID）
- 收藏品 ID 以 `col1` 开头
- NFT 的标识符（launcher ID）以 `nft1` 开头
- 个人资料 ID 以 `did:chia:` 开头
- 每小时更新一次热门收藏品列表
- 交易量统计默认基于 7 天的数据

## 支持资源

- MintGarden API 文档：https://api.mintgarden.io/docs
- Chia NFT 相关信息：https://mintgarden.io
- 如有 bug 报告，请提交到技能的仓库中