---
name: snake-game
description: Trifle Snake游戏的持久自动播放守护进程，支持模块化策略系统
version: 2.0.0
metadata:
  clawdhub:
    emoji: "🐍"
    requires:
      bins: ["node"]
    platforms: ["api"]
    depends: ["trifle-auth"]
---

# 蛇游戏技能（Snake Game Skill）

该技能能够通过一个持续运行的守护进程（daemon）以及模块化的策略系统，自动执行“Trifle Snake”游戏。

## 安装方法

### 通过 ClawdHub 安装
```bash
clawdhub install trifle-labs/snake-game
```

### 通过 Git （符号链接方法）安装
```bash
# Clone the skills repo
git clone https://github.com/trifle-labs/skills.git ~/repos/trifle-skills

# Symlink to your openclaw workspace
ln -s ~/repos/trifle-skills/snake-game ~/.openclaw/workspace/skills/snake-game

# Make executable
chmod +x ~/.openclaw/workspace/skills/snake-game/snake.mjs
```

### 手动安装
```bash
# Copy to your skills directory
cp -r snake-game ~/.openclaw/workspace/skills/

# Make executable
chmod +x ~/.openclaw/workspace/skills/snake-game/snake.mjs
```

## 先决条件

- 必须先使用 `trifle-auth` 技能进行身份验证。
- 确保已安装 Node.js 18 及更高版本。
- 拥有足够的游戏积分（可通过游戏获胜、获得认证奖励等方式积累）。

## 快速入门
```bash
# Start daemon in foreground
node snake.mjs start

# Start daemon in background (detached)
node snake.mjs start --detach

# Check status
node snake.mjs status

# Stop daemon
node snake.mjs stop
```

## 命令说明

### 守护进程控制
```bash
snake start [--detach] [--strategy NAME]   # Start the autoplay daemon
snake stop                                  # Stop the running daemon
snake status                                # Show daemon status and stats
snake attach [-f]                           # View daemon logs (-f to follow)
snake pause                                 # Pause voting (daemon keeps running)
snake resume                                # Resume voting
```

### 配置设置
```bash
snake config [key] [value]     # Get/set configuration values
snake strategies               # List available strategies
snake server [live|staging]    # Switch game server
snake telegram [chat_id|off]   # Configure Telegram logging
```

### 服务管理
```bash
snake install-service      # Install systemd (Linux) or launchd (macOS)
snake uninstall-service    # Remove the service
```

### 手动游戏操作命令
```bash
snake state                           # Get current game state
snake vote <dir> <team> [amount]      # Submit a vote manually
snake strategy                        # Analyze current game
snake balance                         # Check ball balance
```

## 策略系统

该技能内置了 5 种策略：

| 策略名称 | 别名 | 描述 |
|---------|-------|-------------|
| expected-value | ev | 优化预期收益，平衡风险与收益。 |
| aggressive | agg | 对领先的队伍进行高额投注。 |
| underdog | und | 支持较小的队伍以获得更高的回报。 |
| conservative | con | 采取保守策略，最小化风险。 |
| random | rand | 随机选择有效的行动方案。 |

### 切换策略
```bash
snake config strategy aggressive
# or
snake start --strategy aggressive
```

### 创建自定义策略

可以在 `lib/strategies/` 目录下扩展 `BaseStrategy` 类来创建自定义策略：
```javascript
import { BaseStrategy } from './base.mjs';

export class MyStrategy extends BaseStrategy {
  constructor(options = {}) {
    super('my-strategy', 'Description', options);
  }

  computeVote(parsed, balance, state) {
    // Return { direction, team, amount, reason } or null
  }
}
```

## 配置参数

| 参数名 | 默认值 | 描述 |
|---------|---------|-------------|
| strategy | expected-value | 使用的策略名称（默认为 `expected-value`） |
| server | live | 运行模式：生产环境（live）或测试环境（staging） |
| minBalance | 5 | 投票所需的最低积分 |
| telegramChatId | null | 使用的 Telegram 聊天室 ID |

## 进程管理

- **防止多个实例**：通过 PID 文件来确保程序仅运行一个实例。
- **持久化设置**：
  - **Linux 系统**：使用 systemd 进行持久化配置。
  - **macOS 系统**：使用 launchd 进行持久化配置。
___CODE_BLOCK_10_, ```bash
snake install-service
launchctl load ~/Library/LaunchAgents/com.openclaw.snake-daemon.plist
```

## 架构说明
```
snake-game/
├── snake.mjs              # Main CLI
├── lib/
│   ├── config.mjs         # Config management
│   ├── api.mjs            # API client
│   ├── telegram.mjs       # Telegram logging
│   ├── game-state.mjs     # State parsing
│   ├── process.mjs        # Process management
│   └── strategies/        # Strategy modules
└── daemon/
    └── autoplay.mjs       # Daemon loop
```