# Wojak.ink 技能

该技能允许用户浏览、搜索并分析来自 wojak.ink 收藏的 Wojak Farmers Plot NFTs。

## 功能概述

**基本功能：**
- 按 NFT ID、名称或特性进行搜索
- 按角色类型查看最低售价
- 浏览来自 Dexie 的市场列表
- 查看单个 NFT 的详细信息
- 跟踪收藏统计数据

**高级功能：**
- 🎯 稀有性评估与评分
- 📊 价格历史跟踪与趋势分析
- 🎨 特性分析与分布
- 💎 价格发现器（寻找价格较低的 NFT）
- 📈 市场统计与分析
- 🔔 历史数据存储

## 收藏信息

**Wojak Farmers Plot**
- 总共 4,200 个 NFT，基于 Chia 区块链
- 14 种角色类型（Wojak、Soyjak、Waifu 及其变体）
- 收藏 ID：`col10hfq4hml2z0z0wutu3a9hvt60qy9fcq4k4dznsfncey4lu6kpt3su7u9ah`
- 官网：https://wojak.ink

## 命令

所有命令均可通过以下方式执行：
- 在 Telegram 中输入 `/wojak <命令>`
- 在 CLI 中输入 `wojak <命令>`

### 基本命令

#### 查看最低售价

```bash
/wojak floor                    # Collection floor price
/wojak floor wojak              # Wojak character floor
/wojak floor soyjak             # Soyjak character floor
/wojak floor papa-tang          # Papa Tang floor
```

### 搜索

```bash
/wojak search "king"            # Search NFTs by trait/name
/wojak search 42                # Find NFT #42 specifically
/wojak search "bepe"            # Find all Bepe variants
```

### 浏览市场列表

```bash
/wojak listings                 # Show all current listings
/wojak listings wojak           # Show Wojak listings only
/wojak listings alien-waifu     # Show Alien Waifu listings
```

### 查看 NFT 详情

```bash
/wojak nft 1                    # Info about NFT #0001
/wojak nft 4200                 # Info about NFT #4200
```

### 查看收藏统计数据

```bash
/wojak stats                    # Collection-wide statistics
/wojak characters               # List all character types
```

### 高级功能

#### 稀有性分析

```bash
/wojak rarity 1                 # Estimate rarity for NFT #0001
/wojak rarity 4200              # Check rarity for NFT #4200
```

提供：
- 估计的稀有性评分
- 稀有性等级（普通 → 传奇）
- 在收藏中的大致排名
- 角色类型信息

#### 价格历史与趋势

```bash
/wojak history recent           # Last 10 sales
/wojak history trend 24         # 24-hour price trend
/wojak history stats 168        # 7-day price statistics
/wojak track                    # Record current floor price
/wojak track wojak              # Track Wojak floor price
```

功能：
- 销售历史跟踪
- 价格趋势检测（上涨/下跌/稳定）
- 统计分析（最低价/最高价/平均价/变化百分比）
- 数据自动存储

#### 特性分析

```bash
/wojak traits                   # List trait categories
/wojak traits Head              # Head trait distribution
/wojak traits Background        # Background trait distribution
```

分析：
- 特性类别（基础、面部、服装等）
- 特性稀有性百分比
- 特性组合
- 每个特性的裸体售价

#### 价格发现器

```bash
/wojak deals                    # Find 10%+ discounts
/wojak deals 20                 # Find 20%+ discounts
/wojak deals 5                  # Find 5%+ discounts
```

自动执行：
- 计算平均挂牌价格
- 找到价格低于阈值的 NFT
- 按最佳交易顺序排序
- 显示节省百分比

## 角色类型

该收藏包含 14 种角色类型：

| 角色 | 数量 | ID 范围 |
|-----------|-------|----------|
| Wojak | 800 | #0001-#0800 |
| Soyjak | 700 | #0801-#1500 |
| Waifu | 500 | #1501-#2000 |
| Baddie | 500 | #2001-#2500 |
| Papa Tang | 100 | #2501-#2600 |
| Monkey Zoo | 300 | #2601-#2900 |
| Bepe Wojak | 200 | #2901-#3100 |
| Bepe Soyjak | 200 | #3101-#3300 |
| Bepe Waifu | 200 | #3301-#3500 |
| Bepe Baddie | 200 | #3501-#3700 |
| Alien Wojak | 150 | #3701-#3850 |
| Alien Soyjak | 150 | #3851-#4000 |
| Alien Waifu | 100 | #4001-#4100 |
| Alien Baddie | 100 | #4101-#4200 |

## 代理使用

当用户询问关于 Wojak NFT、收藏或市场数据时，该技能会：

```javascript
const { handleCommand } = require('./skills/wojak-ink');

// Natural language → formatted response
const output = await handleCommand(['floor', 'wojak']);
```

该技能负责：
- 命令解析与标准化
- 向 MintGarden 和 Dexie 发送 API 请求
- 数据缓存（有效期 5 分钟）
- 生成格式化的文本输出（适用于 CLI/Telegram）

## API 客户端

该技能使用两个主要 API：

### MintGarden API
- NFT 元数据和收藏统计信息
- 基础地址：`https://api.mintgarden.io`
- 无需 API 密钥

### Dexie API
- 市场报价和列表信息
- 基础地址：`https://api.dexie.space/v1`
- 无需 API 密钥

## 安装

```bash
cd ~/clawd/skills/wojak-ink
npm install
chmod +x cli.js
npm link  # Makes 'wojak' command global
```

## 输出格式

所有命令返回的文本适合：
- 终端输出（CLI）
- Telegram 消息
- Discord 消息
- WhatsApp 消息

（注意：WhatsApp 不支持 Markdown 格式，因此输出文本为纯文本。）

## 缓存

- 列表缓存：5 分钟
- 避免过多的 API 请求
- 可通过代码强制刷新数据

## 示例

**查找最便宜的 Wojak NFT：**
```bash
wojak floor wojak
```

**搜索特定 NFT：**
```bash
wojak nft 1337
```

**查看所有 Papa Tang 的列表：**
```bash
wojak listings papa-tang
```

**按特性搜索：**
```bash
wojak search "king crown"
```

## 已实现的功能

✅ 稀有性评分
✅ 价格历史跟踪
✅ 特性分析框架
✅ 价格发现器
✅ 市场趋势检测
✅ 历史数据存储

## 未来改进计划

- 完整整合特性数据（需要收集数据）
- 查看钱包投资组合
- 实时销售通知
- 通过 Telegram 发送价格警报
- 基于完整元数据的高级稀有性排名
- 特性组合稀有性评分
- 跨收藏比较

## 提示

- 角色类型名称不区分大小写
- 可以使用带填充或不带填充的 NFT ID 进行搜索
- 搜索支持部分匹配
- 列表信息每 5 分钟自动更新一次

## 支持资源

- 收藏官网：https://wojak.ink
- MintGarden：https://mintgarden.io
- Dexie：https://dexie.space
- 如有 bug，请提交到技能仓库