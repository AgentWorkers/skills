---
name: crunch-protocol-skill
description: Crunch Protocol CLI的自然语言接口：将用户请求映射为用于管理协调员、比赛（crunches）、奖励和检查点的CLI命令。支持将输出格式化为Slack、Telegram、Discord或纯文本格式。
---

# Crunch Protocol CLI 技能

此技能能够将自然语言查询转换为 `crunch-cli` 命令，并根据不同的输出媒介格式化结果。

## 设置

确保全局安装了 `crunch-cli`：
```bash
npm install -g @crunchdao/crunch-cli
```

验证安装：
```bash
crunch-cli --version
```

## 配置文件

配置文件存储在 `profiles.json` 中（与本文件位于同一目录下）。每个配置文件将一个简短的名字映射到一组 `crunch-cli` 命令参数，这样用户就可以使用类似 “list crunches for m-jeremy” 的命令，而无需每次都输入完整的地址。

### 配置文件格式

```json
{
  "profiles": {
    "m-jeremy": {
      "url": "https://mainnet.helius-rpc.com/?api-key=...",
      "wallet": "/path/to/keypair.json",
      "multisigAddress": "9WzDXwBbmkg8...",
      "coordinatorWallet": "5abc..."
    },
    "devnet": {
      "url": "devnet",
      "wallet": "/path/to/dev-keypair.json",
      "coordinatorWallet": ""
    }
  }
}
```

### 配置字段与 `crunch-cli` 命令参数的对应关系

| 配置字段 | `crunch-cli` 命令参数 | 说明 |
|---------|-----------------|-------------------------|
| `url` | `-u <值>` | RPC 地址或别名（例如：`mainnet-beta`、`devnet`、`testnet`、`localhost`） |
| `wallet` | `-w <值>` | Solana 密钥对路径。仅在多签名模式下，当钱包作为提案者时使用。 |
| `multisigAddress` | `-m <值>` | 多签名地址（非保险库地址）。 |
| `coordinatorWallet` | 附加到 `coordinator get` 命令中 | 协调器所有者地址。设置后，后续命令将使用该地址的上下文（例如：列出该协调器的所有操作）。 |

### 如何解析配置文件

当用户提到一个配置文件名时：

1. 从技能目录中读取 `profiles.json` 文件。
2. 按名称查找对应的配置文件（不区分大小写）。
3. 将每个非空字段映射到相应的 `crunch-cli` 命令参数（参见上表）。
4. 将这些参数添加到要执行的命令前面。

**示例：** 用户输入 “list crunches for m-jeremy”

1. 加载 `mainnet-proposer` 配置文件 → `{ url: "https://mainnet...", wallet: "/path/...", multisigAddress: "9WzDX..." }`
2. 构建命令：`crunch-cli -u "https://mainnet..." -w "/path/..." -m "9WzDX..." crunches list`

**示例：** 用户输入 “show coordinator for devnet”

1. 加载 `devnet` 配置文件 → `{ url: "devnet" }`
2. 构建命令：`crunch-cli -u devnet coordinator get`

### 管理配置文件

- 用户可以请求 **添加**、**更新** 或 **删除** 配置文件。操作完成后，需要读取当前的 `profiles.json` 文件，应用更改并重新写入。
- 如果 `profiles.json` 文件尚不存在，则使用上述结构创建它。
- 当用户输入 “set profile to m-jeremy” 或 “use profile m-jeremy” 时，系统会记住该配置，并在后续所有命令中自动应用这些参数。

## 命令映射规则

### 重要提示：短语的直接映射

为了提高效率和一致性，这些短语会被 **直接** 映射到 `crunch-cli` 命令中，无需通过大型语言模型（LLM）进行解析：

| 用户输入 | `crunch-cli` 命令 |
|------------------|------------------------|
| `get info about crunch <名称>` | `crunch-cli crunch get "<名称>"` |
| `get crunch <名称>` | `crunch-cli crunch get "<名称>"` |
| `show crunch <名称>` | `crunch-cli crunch get "<名称>"` |
| `crunch details <名称>` | `crunch-cli crunch get "<名称>"` |
| `get coordinator <地址>` | `crunch-cli coordinator get "<地址>"` |
| `show coordinator` | `crunch-cli coordinator get` |
| `my coordinator` | `crunch-cli coordinator get` |
| `list crunches` | `crunch-cli crunches list` |
| `list my crunches` | `crunch-cli crunches list` |
| `show all crunches` | `crunch-cli crunches list` |
| `get config` | `crunch-cli coordinator get-config` |
| `coordinator config` | `crunch-cli coordinator get-config` |
| `checkpoint for <名称>` | `crunch-cli crunch checkpoint-get-current "<名称>"` |
| `current checkpoint <名称>` | `crunch-cli crunch checkpoint-get-current "<名称>"` |
| `set certificate` | `crunch-cli coordinator cert set` |
| `set cert` | `crunch-cli coordinator cert set` |
| `update certificate` | `crunch-cli coordinator cert set` |
| `get certificate` | `crunch-cli coordinator cert get` |
| `get cert` | `crunch-cli coordinator cert get` |
| `show certificate` | `crunch-cli coordinator cert get` |
| `my certificate` | `crunch-cli coordinator cert get` |
| `sweep tokens <名称>` | `crunch-cli crunch sweep-token-accounts "<名称>"` |
| `sweep token accounts <名称>` | `crunch-cli crunch sweep-token-accounts "<名称>"` |
| `check prize accounts <名称>` | `crunch-cli crunch check-prize-atas "<名称>"` |
| `check atas <名称>` | `crunch-cli crunch check-prize-atas "<名称>"` |
| `map cruncher addresses` | `crunch-cli crunch map-cruncher-addresses` |
| `emission checkpoint add` | `crunch-cli crunch emission-checkpoint-add` |

### 名称提取规则

- 当提供 crunch 名称时，需要在 `crunch-cli` 命令中用引号括起来。
- 常见的竞赛名称包括：Crunch、Competition、Tournament、Challenge

## 执行流程

1. **解析** 用户请求，确定以下信息：
   - 操作（获取、创建、开始、结束等）
   - 目标（crunch、协调器、检查点等）
   - 如果适用，还需提供名称/标识符
   - 任何其他参数

2. 使用上述映射表将用户请求转换为 `crunch-cli` 命令。

3. **执行** 命令：
   ```bash
   crunch-cli [options] <command> [arguments]
   ```

4. **格式化** `crunch-cli` 的输出结果。除非用户特别要求，否则应保持原样；但需要根据指定的媒介格式化输出结果（参见下面的输出格式说明）。

## 可用命令参考

### 协调器相关命令
| 命令 | 说明 | 使用方法 |
|---------|-------------|-------------------------|
| `coordinator get [所有者]` | 获取协调器详细信息 | `crunch-cli coordinator get [地址]` |
| `coordinator get-config` | 获取协调器配置 | `crunch-cli coordinator get-config` |
| `coordinator register <名称>` | 注册新协调器 | `crunch-cli coordinator register "名称"` |
| `coordinator reset-hotkey` | 重置 SMP 热键 | `crunch-cli coordinator reset-hotkey` |
| `coordinator set-emission-config` | 设置排放百分比 | `crunch-cli coordinator set-emission-config <排放百分比> <投票者百分比> <资金百分比>` |

### 证书相关命令
| 命令 | 说明 | 使用方法 |
|---------|-------------|-------------------------|
| `coordinator cert set <公钥> [--槽位 N]` | 设置证书哈希 | `crunch-cli coordinator cert set "MIIBIjAN..." [--槽位 0\|1]` |
| `coordinator cert get [所有者]` | 获取证书信息 | `crunch-cli coordinator cert get [地址]` |

### 竞赛相关命令
| 命令 | 说明 | 使用方法 |
|---------|-------------|-------------------------|
| `crunch get <名称>` | 获取竞赛详情 | `crunch-cli crunch get "Synth"` |
| `crunches list [钱包]` | 列出所有竞赛 | `crunch-cli crunches list` |
| `crunch create` | 创建新竞赛 | `crunch-cli crunch create "名称" <奖励金额> [最大模型数量>` |
| `crunch start <名称>` | 启动竞赛 | `crunch-cli crunch start "名称"` |
| `crunch end <名称>` | 结束竞赛 | `crunch-cli crunch end "名称"` |
| `crunch deposit-reward` | 存入 USDC | `crunch-cli crunch deposit-reward "名称" <金额>` |
| `crunch margin <名称>` | 执行保证金支付 | `crunch-cli crunch margin "名称"` |
| `crunch drain <名称>` | 提取剩余 USDC | `crunch-cli crunch drain "名称"` |
| `crunch get-cruncher` | 获取竞赛管理者信息 | `crunch-cli crunch get-cruncher "竞赛名称" <钱包>` |
| `crunch sweep-token-accounts` | 将代币转移到保险库 | `crunch-cli crunch sweep-token-accounts "名称"` |
| `crunch check-prize-atas` | 检查 USDC 账户状态 | `crunch-cli crunch check-prize-atas "名称"` |
| `crunch map-cruncher-addresses` | 映射竞赛管理者地址 | `crunch-cli crunch map-cruncher-addresses "协调器名称"` |
| `crunch emission-checkpoint-add` | 添加排放检查点 | `crunch-cli crunch emission-checkpoint-add "协调器名称" <金额>` |

### 检查点相关命令
| 命令 | 说明 | 使用方法 |
|---------|-------------|-------------------------|
| `crunch checkpoint-create` | 创建检查点 | `crunch-cli crunch checkpoint-create "名称" prizes.json [--dryrun]` |
| `crunch checkpoint-get-current` | 获取当前检查点 | `crunch-cli crunch checkpoint-get-current "名称"` |
| `crunch checkpoint-get` | 通过索引获取检查点 | `crunch-cli crunch checkpoint-get "名称" <索引>` |

### 全局选项
- `-u, --url <网络>` - 网络：mainnet-beta、devnet、localhost（默认值：从配置文件中获取） |
- `-w, --wallet <路径>` - 密钥对文件路径 |
- `-o, --output json` - 输出格式：JSON（便于解析） |
- `-m, --multisig <地址>` - 创建多签名提案（而非直接执行）

## 输出格式

### 媒介检测

根据用户请求检测输出格式：
- “for slack” / “slack format” → Slack 格式 |
- “for telegram” / “telegram format” → Telegram 格式 |
- “for discord” / “discord format” → Discord 格式 |
- 默认格式：纯文本 / Markdown 格式

### Slack 格式
```
*🏆 Crunch: Synth*
━━━━━━━━━━━━━━━━━
• *Status:* Active
• *Participants:* 142
• *Prize Pool:* 10,000 USDC
• *Checkpoint:* 5
* *Funds:* 3000USDC
```

### Telegram 格式
```
🏆 <b>Crunch: Synth</b>

📊 Status: Active
👥 Participants: 142  
💰 Prize Pool: 10,000 USDC
📍 Checkpoint: 5
💰 Funds: 3000USDC
```

### Discord 格式
```
## 🏆 Crunch: Synth
**Status:** Active
**Participants:** 142
**Prize Pool:** 10,000 USDC
**Checkpoint:** 5
```

### 纯文本 / 默认格式
```
Crunch: Synth
Status: Active
Participants: 142
Prize Pool: 10,000 USDC
Checkpoint: 5
Funds: 3000USDC
```

## 错误处理

如果命令执行失败：

1. 显示用户友好的错误信息。
2. 提供可能的解决方法：
   - 网络错误？添加 `-u devnet` 或 `-u mainnet-beta` |
   - 未找到钱包？使用 `crunches list` 命令列出所有可用的竞赛。

## 示例用法

### “获取关于 Synth 竞赛的详细信息”
```bash
crunch-cli crunch get "Synth"
```

### “显示 mainnet 上的协调器信息”
```bash
crunch-cli -u mainnet-beta coordinator get
```

### “为 Slack 显示所有竞赛列表”
```bash
crunch-cli crunches list
```

### “获取 Chaos 竞赛的当前检查点信息”
```bash
crunch-cli crunch checkpoint-get-current "Chaos"
```

## 参考文档

有关完整的 `crunch-cli` 命令文档，请参阅 [references/cli-reference.md](references/cli-reference.md)。