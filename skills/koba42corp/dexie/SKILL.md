# Dexie Skill

通过 Dexie.space API 追踪 Chia DEX 的交易情况。

## 功能概述

- 列出活跃/已完成的交易报价
- 查看代币价格和流动性
- 搜索代币（CATs）
- 监控交易对
- 获取平台统计数据

## 命令

所有命令可以通过以下方式执行：
- 在 Telegram 中输入 `/dex <命令>`
- 在 Telegram 中输入 `/dexie <命令>`
- 在 CLI 中输入 `dex <命令>`
- 在 CLI 中输入 `dexie <命令>`

### 交易报价

```bash
/dex offers                List active offers
/dex offers completed      List completed offers
/dex offers cancelled      List cancelled offers
/dex offer <id>            Get offer details
```

### 代币信息

```bash
/dex assets                List top tokens by volume
/dex asset <id|code>       Get token details (e.g., SBX, DBX)
/dex search <query>        Search tokens
/dex price <code>          Get token price
```

### 交易对信息

```bash
/dex pairs                 List trading pairs
/dex pair <id>             Get pair details
```

### 平台统计数据

```bash
/dex stats                 Get platform statistics
```

### 快捷键

```bash
/dex SBX                   Quick price lookup
/dex DBX                   Quick price lookup
```

## 代理使用说明

当用户询问关于 Chia DEX、交易或代币价格的信息时：

```javascript
const { handleCommand } = require('./skills/dexie');

// Natural language → formatted response
const output = await handleCommand('show me top tokens');
```

## API 客户端

用于自定义集成：

```javascript
const DexieAPI = require('./skills/dexie/lib/api');
const api = new DexieAPI();

// Get active offers
const offers = await api.getOffers({ page_size: 20, status: 0 });

// Get token details
const token = await api.getAsset('a628c1c2c6fcb74d53746157e438e108eab5c0bb3e5c80ff9b1910b3e4832913');

// List all assets
const assets = await api.getAssets({ page_size: 50, sort: 'volume' });

// Get trading pairs
const pairs = await api.getPairs();
```

## 安装

无需安装任何额外的软件——Dexie API 是公开的。

## 输出格式

所有命令返回的文本格式适用于：
- 终端输出（CLI）
- Telegram 消息
- Discord 消息
- WhatsApp 消息

## 示例

**查看代币价格：**
```bash
/dex price SBX
```

**列出活跃的交易报价：**
```bash
/dex offers
```

**搜索代币：**
```bash
/dex search bucks
```

**获取平台统计数据：**
```bash
/dex stats
```

## 注意事项

- 资产 ID 是长十六进制字符串
- 代币代码通常较短（例如：SBX、DBX、XCH）
- 可以使用搜索功能按名称查找代币
- 价格以美元（USD）显示
- 交易量和流动性以 XCH 表示

## 帮助资源

- Dexie.space：https://dexie.space
- API 文档：https://api.dexie.space/v1
- 错误报告：请提交到技能仓库（skill repository）