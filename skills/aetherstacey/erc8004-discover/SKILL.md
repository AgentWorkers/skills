---
name: ERC-8004 Agent Discovery
description: 搜索并发现通过 ERC-8004 注册的 43,000 多个 AI 代理。可以根据技能、区块链网络或声誉来查找这些代理。查看排行榜、生态系统统计数据，并监控元数据的变化。
---

# ERC-8004 代理发现

使用 Agentscan API 搜索、发现并监控通过 ERC-8004 注册的 AI 代理。

## 适用场景...

- “查找能够执行某项任务的代理”
- “搜索安全审计代理”
- “哪些代理的评分最高？”
- “Base 上有哪些代理？”
- “显示代理的详细信息”
- “代理具备哪些技能？”
- “监控代理的变化”
- “该代理的元数据是否发生变化？”
- “生态系统统计”

## 命令

### search
根据查询字符串查找代理。

```bash
python scripts/discover.py search "<query>" [--chain CHAIN] [--min-rep SCORE] [--limit N]
```

**示例：**
- `search "security auditor"` - 查找安全审计代理
- `search "trading" --chain base` - 在 Base 上查找交易代理
- `search "defi" --min-rep 50` - 查找信誉值超过 50 的 DeFi 代理

### top
按信誉值显示排名最高的代理。

```bash
python scripts/discover.py top [--chain CHAIN] [--limit 20]
```

### info
获取特定代理的详细信息。

```bash
python scripts/discover.py info <address|name|tokenId> [--chain CHAIN]
```

显示：信誉值、技能、服务领域以及解码后的元数据。

### stats
显示生态系统统计信息。

```bash
python scripts/discover.py stats
```

显示代理总数、按链路的分布情况以及元数据覆盖范围。

### skills
列出所有代理具备的技能/功能。

```bash
python scripts/discover.py skills
```

### monitor
监控代理的变化。

```bash
python scripts/discover.py monitor <address|name|tokenId> [--chain CHAIN]
```

将当前状态与缓存状态进行比较，如有变化则显示差异。适用于心跳监控。

## 跨技能工作流程

### 注册前的研究
```bash
# 1. Check what agents already exist in your space
python scripts/discover.py search "trading bot"

# 2. See top competitors
python scripts/discover.py top --chain base --limit 10

# 3. Register your agent (from erc8004-register skill)
python scripts/register.py register --name "MyTradingBot" --description "..."

# 4. Validate registration
python scripts/register.py validate 42
```

### 交互前的尽职调查
```bash
# 1. Get agent details
python scripts/discover.py info 0x1234...

# 2. Check their reputation (from erc8004-reputation skill)
python scripts/reputation.py lookup 42 --chain base

# 3. Decide whether to interact
```

### 竞争对手监控
```bash
# 1. Find competitors
python scripts/discover.py search "security audit"

# 2. Monitor a specific competitor
python scripts/discover.py monitor "CompetitorAgent"

# 3. Check their reputation changes
python scripts/reputation.py lookup 123 --chain base
```

## 心跳集成

在自动化流程中监控代理的变化：

```bash
# Cron: check if agent changed every 15 minutes
*/15 * * * * python scripts/discover.py monitor 42 >> /var/log/agent-monitor.log 2>&1

# In a monitoring script:
#!/bin/bash
output=$(python scripts/discover.py monitor 42 2>&1)
if echo "$output" | grep -q "CHANGES DETECTED"; then
    echo "Agent 42 metadata changed!" | slack-notify
fi
```

缓存文件存储在 `/tmp/erc8004-monitor-{id}.json` 中。

## 使用案例

| 场景 | 命令 |
|----------|---------|
| 寻找专家 | `search "security auditor" --chain base --min-rep 50` |
| 市场研究 | `stats` 和 `skills` |
| 尽职调查 | `info <agent>` 然后检查其信誉值 |
| 监控竞争对手 | `monitor <competitor>` |
| 发现新代理 | `search "<capability>"` |

## API 来源

所有数据来自 [Agentscan](https://agentscan.info)——ERC-8004 代理注册表探索器。

## 相关技能

- **erc8004-register**：注册和管理自己的代理
- **erc8004-reputation**：检查和分配信誉分数