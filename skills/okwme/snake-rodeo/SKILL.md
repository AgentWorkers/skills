---
name: snake-rodeo
description: Trifle Snake Rodeo游戏的自动播放守护进程。该进程会连接到实时游戏服务器，通过用户的钱包进行身份验证，并使用可插拔的AI策略来决定蛇的移动方向。适用于用户想要进行游戏体验、运行游戏模拟或开发自定义策略的场景。
license: MIT
compatibility: Requires Node.js 18+. Depends on trifle-auth skill for initial authentication.
metadata:
  author: trifle-labs
  version: "3.0.0"
  homepage: https://agentskills.io/okwme/snake-rodeo
---
# Snake Rodeo 技能

该技能能够通过一个持续运行的守护进程（daemon）和模块化的策略系统，自动执行 [Trifle Snake Rodeo](https://trifle.life) 游戏。该技能基于 [snake-rodeo-agents](https://github.com/trifle-labs/snake-rodeo-agents) 库开发。

## 工作原理

这款游戏是一个多人参与的蛇形游戏，游戏场景设置在一个六边形网格上。每轮游戏中，各团队会竞标游戏中的移动方向——出价最高的团队将获得该方向的移动权。所有出价会进入一个奖金池，由获胜团队平分。守护进程通过 SSE（Simple WebSocket Engine）实时监控游戏进程，根据预设的策略选择最佳移动方向，并自动提交投票结果。

## 先决条件

- 需要通过 `trifle-auth` 技能进行身份验证。
- 确保使用 Node.js 18 及更高版本。
- 拥有足够的游戏积分（可以通过游戏胜利、认证奖励等方式获得）。

## 守护进程命令

```bash
# Start/stop
node snake.mjs start [--detach] [--strategy NAME]
node snake.mjs stop
node snake.mjs status
node snake.mjs attach [-f]

# Pause/resume voting (daemon keeps running)
node snake.mjs pause
node snake.mjs resume

# Configuration
node snake.mjs config [key] [value]
node snake.mjs strategies
node snake.mjs server [live|staging]
node snake.mjs telegram [chat_id|off]

# Manual play
node snake.mjs state
node snake.mjs vote <direction> <team> [amount]
node snake.mjs strategy    # Analyze current game
node snake.mjs balance

# System service (auto-restart on boot)
node snake.mjs install-service
node snake.mjs uninstall-service
```

## 可用的策略

系统提供了五种内置策略，每种策略都继承自 `snake-rodeo-agents` 中的 `BaseStrategy` 类：

| 策略 | 别名 | 描述 |
|---------|-------|-------------------|
| `expected-value` | `ev`, `default` | 使用广度优先搜索（BFS）算法进行路径规划，避免死胡同，并基于博弈论选择团队；策略较为平衡。 |
| `aggressive` | `agg` | 支持领先的团队，并积极进行反竞标。 |
| `underdog` | `und` | 支持资金较少的团队，以获得更高的奖金回报。 |
| `conservative` | `con` | 选择最低出价，优先考虑安全性。 |
| `random` | `rand` | 随机选择有效的移动方向。 |

## 自定义策略的实现方法

可以通过继承 `snake-rodeo-agents` 中的 `BaseStrategy` 类来创建自定义策略：

```javascript
import { BaseStrategy } from 'snake-rodeo-agents';

export class MyStrategy extends BaseStrategy {
  constructor(options = {}) {
    super('my-strategy', 'My custom strategy', options);
  }

  computeVote(parsed, balance, state) {
    // parsed: ParsedGameState — hex grid, teams, scores, valid directions
    // balance: number — current ball balance
    // state: AgentState — round tracking, team assignment, vote history

    // Return a vote:
    return { direction: 'ne', team: 'A', amount: 1, reason: 'chasing fruit' };

    // Or skip:
    return { skip: true, reason: 'too risky' };
  }

  // Optional: counter-bid when outbid
  shouldCounterBid(parsed, balance, state, ourVote) {
    return null; // or return a new VoteAction
  }
}
```

**策略开发所需的关键数据类型：**

- **`ParsedGameState`**：解析后的游戏状态数据，包含蛇的位置、团队信息、有效移动方向、网格范围、奖金池、最低出价以及获胜所需的水果数量。 |
- **`AgentState`**：包含当前所属团队、当前轮次已花费的积分、本轮投票次数、已进行的游戏次数以及投票记录。 |
- **`VoteAction`**：包含投票方向、所属团队以及投票金额及投票理由。

## snake-rodeo-agents 库

游戏的核心逻辑实现位于 [snake-rodeo-agents](https://github.com/trifle-labs/snake-rodeo-agents) 这个独立的 TypeScript 库中。该技能通过添加守护进程管理、配置持久化功能以及 OpenClaw 的集成，实现了对库的封装。

### API 客户端

**SnakeClient 提供的方法：**

| 方法 | 描述 |
|--------|-------------------|
| `getGameState()` | 获取当前游戏状态（蛇的位置、玩家得分、投票信息）。 |
| `getBalance()` | 获取当前玩家的积分余额。 |
| `submitVote(dir, team, amount)` | 提交投票（指定移动方向、所属团队及投票金额）。 |
| `getRodeos()` | 获取所有正在进行的蛇形游戏列表。 |
| `getUserStatus()` | 获取用户个人信息和游戏统计数据。 |

### 使用 SIWE（基于以太坊的登录系统）进行身份验证

支持使用一次性生成的以太坊钱包（throwaway wallets）进行身份验证。

### 游戏状态辅助工具

该库提供了用于策略开发的六边形网格相关辅助函数。

### 锦标赛模拟器

支持离线运行锦标赛，以便快速比较不同策略的表现：

```bash
# CLI
npm run simulate -- ev,aggressive --games 100 --seed 42
npm run simulate -- ev,aggressive,conservative --config small --verbose
npm run simulate -- ev,aggressive --json   # machine-readable output
```

**模拟器配置选项：**

| 选项 | 描述 |
|------|-------------------|
| `-g, --games N` | 每个配置文件对应的游戏数量（默认：100 场）。 |
| `-c, --config NAME` | 游戏难度级别（`small`、`medium`、`large` 或 `all`；默认：所有难度级别）。 |
| `-s, --seed N` | 用于保证结果可复现性的随机数种子。 |
| `-v, --verbose` | 打印每轮游戏的详细信息。 |
| `--json` | 以机器可读的 JSON 格式输出游戏数据。 |

### 通过 Telegram 发送游戏事件

支持将游戏事件实时发送到指定的 Telegram 群组。

## 配置设置

| 配置项 | 默认值 | 描述 |
|---------|-------------------|-------------------|
| `strategy` | `expected-value` | 当前使用的策略名称。 |
| `server` | `live` | 运行模式（`live` 或 `staging`）。 |
| `minBalance` | `5` | 提交投票所需的最低积分余额。 |
| `telegramChatId` | `null` | 用于日志记录的 Telegram 聊天群组 ID。 |

## 架构设计

```
snake-game/                             # OpenClaw skill wrapper
├── SKILL.md                            # This file
├── snake.mjs                           # CLI entry point
├── clawdhub.json                       # ClawHub registry metadata
├── package.json                        # Dependencies (snake-rodeo-agents)
├── lib/
│   ├── config.mjs                      # OpenClaw config/paths
│   ├── api.mjs                         # Token-based API (uses OpenClaw auth)
│   ├── process.mjs                     # Daemon PID management
│   └── telegram.mjs                    # Telegram bridge
├── daemon/
│   └── autoplay.mjs                    # Game loop: SSE → strategy → vote
└── node_modules/
    └── snake-rodeo-agents/             # Core library (TypeScript)
        └── dist/
            ├── lib/game-state.js       # Hex grid, BFS, flood-fill
            ├── lib/strategies/         # Strategy implementations
            ├── lib/client.js           # Standalone API client
            ├── lib/auth.js             # Wallet SIWE auth
            ├── lib/simulator.js        # Offline game simulator
            ├── lib/telegram.js         # Telegram logger
            └── bin/play.js             # Standalone CLI runner
```

## 升级说明

如果该技能作为系统服务运行，相关的升级步骤请参考相应的文档或指南。

```bash
# Linux
systemctl --user restart snake-daemon

# macOS
launchctl unload ~/Library/LaunchAgents/com.openclaw.snake-daemon.plist
launchctl load ~/Library/LaunchAgents/com.openclaw.snake-daemon.plist
```