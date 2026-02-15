---
name: ERC-8004 Register
description: 通过 ERC-8004 身份注册表，在链上注册 AI 代理、更新元数据、验证注册信息，并自动修复损坏的代理配置。支持 Base、Ethereum、Polygon、Monad、BNB 等区块链平台。
---

# ERC-8004 注册技能

通过 ERC-8004 身份注册表，在链上注册、更新、验证和修复代理。

## 适用场景...

- “在链上注册我的代理”
- “我需要创建一个新的 ERC-8004 代理”
- “更新我的代理的元数据”
- “检查我的代理注册是否有效”
- “修复我的代理注册问题”
- “显示我的代理的链上信息”
- “我拥有哪些代理？”
- “检查我的代理的健康状况”

## 命令

### register
在链上注册一个新的代理。

```bash
python scripts/register.py register --name "AgentName" --description "Description" [--image URL] [--chain base]
```

**选项:**
- `--name`（必填）：代理名称
- `--description`（必填）：代理描述
- `--image`：图片 URL（必须是 https:// 开头的）
- `--chain`：区块链（base、ethereum、polygon、monad、bnb）。默认：base

### update
更新现有代理的元数据。

```bash
python scripts/register.py update <agentId> [--name NAME] [--description DESC] [--image URL] [--add-service name=X,endpoint=Y] [--remove-service NAME] [--chain base]
```

### info
显示代理信息。

```bash
python scripts/register.py info <agentId> [--chain base]
```

### validate
检查注册过程中是否存在常见问题。

```bash
python scripts/register.py validate <agentId> [--chain base]
```

**检查内容:**
- 缺少 `type` 字段
- 使用本地路径的图片（如 /home/...、./、file://）
- 名称/描述为空
- 缺少 `registrations` 数组
- 图片 URL 无法访问

### fix
自动修复常见的注册问题。

```bash
python scripts/register.py fix <agentId> [--chain base] [--dry-run]
```

**自动修复的内容:**
- 缺少 `type` 字段
- 缺少 `registrations` 数组
- 使用本地路径的图片（会自动删除这些图片）

使用 `--dry-run` 选项预览更改，而不会实际应用这些更改。

### self-check
检查你的钱包拥有的所有代理。

```bash
python scripts/register.py self-check
```

使用 Agentscan 查询你的代理，验证每个代理的状态，并打印健康报告。

## 跨技能工作流程

### 注册后流程
```bash
# 1. Register new agent
python scripts/register.py register --name "MyBot" --description "Trading assistant"

# 2. Validate the registration
python scripts/register.py validate 42 --chain base

# 3. Check initial reputation (from erc8004-reputation skill)
python scripts/reputation.py lookup 42 --chain base

# 4. Monitor for discovery (from erc8004-discover skill)
python scripts/discover.py info 42
```

### 定期健康检查
```bash
# Run self-check to validate all your agents
python scripts/register.py self-check

# Fix any issues found
python scripts/register.py fix 42 --chain base
```

## 心跳检测集成

为了实现自动化监控，定期运行自我检查：

```bash
# Cron: check health every hour
0 * * * * cd /path/to/skill && python scripts/register.py self-check >> /var/log/agent-health.log 2>&1

# Or in a script:
#!/bin/bash
python scripts/register.py self-check
if [ $? -ne 0 ]; then
    echo "Agent health check failed!" | notify-send
fi
```

## 钱包配置

设置以下环境变量之一：

```bash
export ERC8004_MNEMONIC="your twelve word mnemonic phrase here"
# OR
export ERC8004_PRIVATE_KEY="0x..."
```

## 合约

身份注册表地址：`0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`（所有链上地址相同）

## 支持的区块链

| 区块链    | ID   | 探索器             |
|----------|------|----------------------|
| Base     | 8453 | basescan.org         |
| Ethereum | 1    | etherscan.io         |
| Polygon  | 137  | polygonscan.com      |
| Monad    | 143  | explorer.monad.xyz   |
| BNB      | 56   | bscscan.com          |

## 依赖项

```bash
pip install web3 eth-account
```

## 相关技能

- **erc8004-discover**：查找和监控代理
- **erc8004-reputation**：对代理进行评分并检查信任度