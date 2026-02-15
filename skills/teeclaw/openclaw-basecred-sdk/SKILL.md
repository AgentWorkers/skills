---
name: openclaw-basecred-sdk
version: 1.0.2
author: teeclaw
license: MIT
description: 通过 Ethos Network、Talent Protocol 和 Farcaster，使用 neutral basecred-sdk 来检查个人的声誉。该工具可以获取可组合的声誉数据（包括原始分数、等级及相关信号），用于身份验证和信任评估。当您需要验证某人在链上的可信度、创作者/构建者的评分，或 Farcaster 的质量指标时，可以使用该工具。
tags: [reputation, identity, ethos, talent, farcaster, basecred, onchain, verification]
metadata:
  openclaw:
    requires:
      bins: [node]
---

# basecred-sdk-skill

**OpenClaw技能：通过Ethos Network、Talent Protocol和Farcaster使用中立的basecred-sdk来检查用户的声誉。**

## 概述

该技能提供了一个命令行界面（CLI），用于调用[@basecred/sdk](https://www.npmjs.com/package/@basecred/sdk)，以从多个Web3身份提供者获取中立的、可组合的声誉数据：

- **Ethos Network**：社交信誉（推荐、评价、分数）
- **Talent Protocol**：构建者和创作者的评分
- **Farcaster (Neynar)**：账户质量指标

该SDK的设计目的是让声誉数据可以被观察，但不会对其进行评判。它返回原始分数、等级和信号——没有排名、百分位数或信任判断。

## 安全性

**该技能使用安全的、硬编码的凭证加载方式**——详细审计信息请参见[SECURITY.md](./SECURITY.md)。

**简而言之：**
- ✅ 凭证从`~/.openclaw/.env`文件中加载（硬编码路径，无目录遍历风险）
- ✅ 上游包[@basecred/sdk@0.6.2]已经过审计且无安全问题（MIT许可证，依赖项极少）
- ✅ 无敏感信息被记录或写入磁盘
- ✅ 只提供只读的API访问权限（公开声誉数据）

## 先决条件

### 必需条件

- Node.js 18及以上版本
- OpenClaw运行时环境

### 可选的API密钥

**环境变量**（位于`~/.openclaw/.env`文件中）：

```bash
# Optional: Enables Talent Protocol builder/creator scores
TALENT_API_KEY=your_talent_api_key

# Optional: Enables Farcaster quality scores
NEYNAR_API_KEY=your_neynar_api_key
```

**注意：**
- Ethos Network不需要API密钥
- 如果没有`TALENT_API_KEY`，则无法获取构建者/创作者的评分
- 如果没有`NEYNAR_API_KEY`，则无法获取Farcaster的评分
- 即使部分数据缺失，该技能仍能正常工作（具有容错机制）

**获取API密钥：**
- Talent Protocol：https://talentprotocol.com
- Neynar：https://neynar.com

## 安装

```bash
cd ~/.openclaw/workspace/skills/openclaw-basecred-sdk
npm install
```

## 使用方法

### 基本检查

```bash
./scripts/check-reputation.mjs 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

**输出（JSON格式）：**
```json
{
  "address": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "timestamp": "2026-02-10T07:00:00.000Z",
  "availability": {
    "ethos": "not_found",
    "talent": "available",
    "farcaster": "available"
  },
  "data": {
    "talent": {
      "builderScore": 86,
      "builderLevel": "Practitioner",
      "builderRank": 8648,
      "creatorScore": 103,
      "creatorLevel": "Established",
      "creatorRank": null
    },
    "farcaster": {
      "score": 1,
      "passesQuality": true
    }
  },
  "recency": "recent"
}
```

### 命令选项

```bash
# Summary format (default)
./scripts/check-reputation.mjs <address>

# Full unified profile
./scripts/check-reputation.mjs <address> --full

# Human-readable output
./scripts/check-reputation.mjs <address> --human

# JSON output (default)
./scripts/check-reputation.mjs <address> --json

# Show help
./scripts/check-reputation.mjs --help
```

### 示例

**检查vitalik.eth的声誉：**
```bash
./scripts/check-reputation.mjs 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

**人类可读的格式：**
```bash
./scripts/check-reputation.mjs 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --human
```

**包含所有数据的完整个人资料：**
```bash
./scripts/check-reputation.mjs 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 --full
```

## 输出格式

### 概要格式（默认）

```json
{
  "address": "0x...",
  "timestamp": "ISO-8601",
  "availability": {
    "ethos": "available|not_found|error",
    "talent": "available|not_found|error",
    "farcaster": "available|not_found|error"
  },
  "data": {
    "ethos": {
      "score": 1732,
      "level": "Established",
      "vouches": 5,
      "reviews": { "positive": 12, "neutral": 1, "negative": 0 },
      "hasNegativeReviews": false
    },
    "talent": {
      "builderScore": 86,
      "builderLevel": "Practitioner",
      "builderRank": 8648,
      "creatorScore": 103,
      "creatorLevel": "Established",
      "creatorRank": null
    },
    "farcaster": {
      "score": 0.97,
      "passesQuality": true
    }
  },
  "recency": "recent|stale|dormant"
}
```

### 完整个人资料格式

有关完整的输出格式，请参阅[@basecred/sdk文档](https://github.com/Callmedas69/basecred/tree/main/packages/sdk#output-schema)。

## 数据来源

### Ethos Network

**提供的数据：**
- 社交信誉分数（0-2800）
- 收到的推荐（信任背书）
- 评价（正面/中性/负面）
- 语义信誉等级（不可信 → 著名）

**无需API密钥。**

### Talent Protocol

**提供的数据：**
- **构建者评分**：技术/开发信誉（0-250+）
- **创作者评分**：内容/创意信誉（0-250+）
- 排名（如有提供）
- 语义等级（新手 → 大师 / 新兴 → 精英）

**需要**：`TALENT_API_KEY`

### Farcaster (Neynar)

**提供的数据：**
- 账户质量分数（0-1）
- 质量达标/未达标（默认值：0.5）

**需要**：`NEYNAR_API_KEY`

## 数据可用性状态

每个数据源都会返回以下状态之一：

| 状态 | 含义 |
|-------|---------|
| `available` | 个人资料存在，数据获取成功 |
| `not_found` | 该地址没有个人资料 |
| `error` | API错误或失败 |

即使数据缺失，该技能也不会崩溃。部分响应也是有效且有用的。

## 语义等级

SDK会根据原始分数生成人类可读的等级：

**Ethos信誉等级：**
- 0-799：不可信
- 800-1199：存疑
- 1200-1399：中立
- 1400-1599：知名
- 1600-1799：声誉良好
- 1800-1999：值得信赖
- 2000-2199：典范
- 2200-2399：杰出
- 2400-2599：备受尊敬
- 2600-2800：著名

**Talent构建者等级：**
- 0-39：新手
- 40-79：学徒
- 80-119：从业者
- 120-169：高级
- 170-249：专家
- 250+：大师

**Talent创作者等级：**
- 0-39：新兴
- 40-79：成长中
- 80-119：成熟
- 120-169：成就显著
- 170-249：杰出
- 250+：精英

## 数据更新频率

数据更新频率的指示：

| 分类 | 条件 |
|--------|-----------|
| `recent` | 在30天内更新 |
| `stale` | 31-90天前更新 |
| `dormant` | 超过90天前更新 |

## 测试

使用已知地址运行测试套件：

```bash
npm test
```

测试对象包括：
- Vitalik Buterin（vitalik.eth）
- Mr. Tee（主要钱包）

## 与其他技能的集成

可以在自己的脚本中导入该库：

```javascript
import { checkReputation, getSummary, formatHuman } from './lib/basecred.mjs';

const result = await checkReputation('0x...');
const summary = getSummary(result);
console.log(summary);
```

## 错误处理

该技能采用优雅的错误处理方式：
- 无效地址 → 返回包含错误信息的对象
- 缺少API密钥 → 发出警告但继续使用可用的数据源
- API失败 → 通过`availability`字段显示错误信息
- 网络错误 → 返回包含详细信息的错误对象

**永远不会抛出异常**——始终返回结构化的数据。

## 设计原则

该技能遵循basecred-sdk的设计理念：
- **缺失的数据会明确显示**——绝不会隐藏
- **时间比分数更重要**——时间字段有助于进行连续性分析
- **数据来源是并行的**——没有哪个数据来源比另一个更“优越”
- **数据仅被报告，不进行评判**——由用户自行解读其含义

## 非目标功能

该技能**不**执行以下操作：
- 判断用户的可信度
- 对用户进行排名
- 比较用户
- 计算综合评分
- 替代人类的判断

## 性能

- **平均查询时间：**1-3秒（取决于网络和API的响应时间）
- **API调用：**每个启用的数据源最多同时发送1个请求
- **无速率限制**——但会遵守上游API的限制

## 故障排除

**“TALENT_API_KEY未找到”警告：**
- 在`~/.openclaw/.env`文件中添加`TALENT_API_KEY=xxx`
- 或者接受无法获取Talent评分的情况

**“NEYNAR_API_KEY未找到”警告：**
- 在`~/.openclaw/.env`文件中添加`NEYNAR_API_KEY=xxx`
- 或者接受无法获取Farcaster评分的情况

**所有数据源都返回`not_found`：**
- 可能该地址在任何平台上都没有个人资料
- 这是正常情况——缺失的数据也是一种信息

**意外错误：**
- 检查网络连接
- 验证API密钥的有效性
- 检查上游API的状态

## 相关链接

- **源SDK：**https://github.com/Callmedas69/basecred/tree/main/packages/sdk
- **npm包：**https://www.npmjs.com/package/@basecred/sdk
- **Ethos Network：**https://ethos.network
- **Talent Protocol：**https://talentprotocol.com
- **Neynar (Farcaster)：**https://neynar.com

## 许可证

MIT许可证

## 作者

由**teeclaw**为OpenClaw开发。

---

**版本：** 1.0.1  
**最后更新时间：** 2026-02-10  
**SDK版本：** @basecred/sdk@0.6.2