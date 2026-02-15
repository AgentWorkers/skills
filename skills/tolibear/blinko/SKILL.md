---
name: blinko
version: 1.1.0
description: 在Abstract链上无头地运行Blinko（基于Plinko技术的游戏）。当代理需要玩Blinko游戏、查看游戏统计数据、排行榜或追踪奖励信息时，可以使用该功能。该系统涵盖了整个流程，包括API认证、链上游戏创建、游戏模拟以及结算等环节。
author: Bearish (@BearishAF)
metadata: {"clawdbot":{"env":["WALLET_PRIVATE_KEY"]}}
---

# Blinko

在Abstract平台上无头运行[Blinko](https://blinko.gg)。这是一个经过验证的公平游戏，支持链上结算。

## 重要提示

- **此技能会在链上签署实际消耗ETH的交易。**请使用仅包含您愿意承担风险的资金的专用热钱包。
- 每局游戏除了您的投注金额外，还需要支付抽象链（Abstract Chain）的Gas费用。
- 您的私钥仅用于在本地签署消息和交易。它会被以签名后的形式发送到Abstract RPC和Blinko API，绝不会以明文形式传输。
- 安装了相关代理后，代理可以自动调用此技能。

## 快速入门

### 进行游戏
```bash
export WALLET_PRIVATE_KEY=0x...
node scripts/play-blinko.js 0.001
```

### 查看统计数据
```bash
node scripts/stats.js 0xYourAddress profile
```

## 脚本

| 脚本 | 用途 |
|--------|---------|
| `play-blinko.js` | 进行一局完整的游戏（包括登录、创建游戏、提交结果、游戏进行和结算） |
| `stats.js` | 查看个人资料、游戏记录、排行榜以及您的“Honey”积分余额 |

## 游戏玩法

```bash
export WALLET_PRIVATE_KEY=0x...
node scripts/play-blinko.js [betETH] [--hard] [--v2]
```

| 标志 | 效果 |
|------|--------|
| `--hard` | 恶搞模式（主游戏的胜率降为0%，必须触发奖励才能获胜） |
| `--v2` | 使用V2算法和配置 |

示例：
```bash
node scripts/play-blinko.js 0.001                # Normal, 0.001 ETH
node scripts/play-blinko.js 0.005 --hard          # Hard mode
node scripts/play-blinko.js 0.002 --v2            # V2 algorithm
node scripts/play-blinko.js 0.003 --hard --v2     # V2 hard mode
```

**投注范围：** 0.0001至0.1 ETH

## 统计数据

```bash
node scripts/stats.js <address> [command] [limit]
```

| 命令 | 显示内容 |
|---------|-------|
| `profile` | 显示个人资料、Honey积分、游戏记录以及连赢/连败次数 |
| `games [N]` | 显示最近N局游戏的详细结果 |
| `leaderboard` | 显示前10名玩家以及您的排名 |
| `honey` | 显示您的Honey积分余额 |

## 工作原理

1. **登录** — 使用钱包签署消息以获取JWT（JSON Web Token）。
2. **创建游戏** — API生成游戏种子，并返回服务器签名。
3. **提交游戏** — 使用ETH进行投注，并添加随机盐值，通过链上调用`createGame()`方法创建游戏。
4. **进行游戏** — API结合生成的种子值和物理模拟规则，返回游戏结果。
5. **结算** — 通过链上调用`cashOut()`（获胜时）或`markGameAsLost()`（失败时）完成结算。

所有游戏都采用“提交-展示”（commit-reveal）机制，确保游戏的公平性。

## 游戏规则

- **10个球从8排钉子中落下**。
- **奖励倍数**：2倍、1.5倍、0.5倍、0.2倍、0.1倍、0.1倍、0.2倍、0.5倍、1.5倍、2倍。
- **奖励机制**：收集字母“B-O-N-U-S”可以触发奖励轮次（最多可触发9轮奖励）。
- **Honey积分**：通过击中特殊钉子获得积分（需要引荐者）。

## 关键信息

| 项目 | 详细信息 |
|------|-------|
| 链路** | Abstract（区块号2741） |
| RPC接口** | `https://api.abs.xyz`（硬编码） |
| 合同地址** | `0x1859072d67fdD26c8782C90A1E4F078901c0d763` |
| API接口** | `https://api.blinko.gg` |
| 游戏官网** | [blinko.gg](https://blinko.gg) |

## 环境变量

| 变量 | 是否必需 | 说明 |
|----------|----------|-------------|
| `WALLET_PRIVATE_KEY` | 是（用于游戏） | 用于签署交易的私钥。请使用热钱包。 |

## 依赖项
```bash
npm install ethers@6
```