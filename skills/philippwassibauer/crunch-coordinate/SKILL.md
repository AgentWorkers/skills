---
name: crunch-coordinate
description: **使用说明：**  
通过 `crunch-cli` 工具来管理 Crunch 协调员、竞赛（crunches）、奖励、检查点（checkpoints）、质押（staking）以及参与竞赛的用户（cruncher accounts）的相关操作。
---

# Crunch Protocol CLI 技能

该技能可以将自然语言查询转换为 `crunch-cli` 命令，支持不同的输出格式（Slack、Telegram、Discord 或纯文本），并支持配置不同的工作区（profiles）。

## 设置

```bash
npm install -g @crunchdao/crunch-cli
crunch-cli --version
```

## 配置文件（profiles）

该 CLI 通过 `~/.crunch/config.json` 文件来实现内置的配置管理功能：

```bash
crunch-cli config show                    # Show current config
crunch-cli config active                  # Show resolved active values
crunch-cli config list-profiles           # List available profiles
crunch-cli config save-profile <name>     # Save current config as profile
crunch-cli config use <profile>           # Switch profile
crunch-cli config set <key> <value>       # Set config value
```

全局标志可以覆盖每个命令的配置：

| 标志 | 描述 |
|------|-------------|
| `-n, --network` | Solana 网络：`mainnet-beta`、`devnet`、`localhost` |
| `-u, --url` | 自定义 RPC URL |
| `-w, --wallet` | Solana 密钥对的路径 |
| `-o, --output` | 输出格式：`json`、`table`、`yaml` |

## 语句映射表

| 用户语句 | CLI 命令 |
|-------------|-------------|
| `get/show crunch <名称>` | `crunch-cli crunch get "<名称>"` |
| `list crunches` | `crunch-cli crunch list` |
| `get/show coordinator [地址]` | `crunch-cli coordinator get [地址]` |
| `list coordinators` | `crunch-cli coordinator list` |
| `get config` | `crunch-cli coordinator get-config` |
| `checkpoint for <名称>` | `crunch-cli crunch checkpoint-get-current "<名称>"` |
| `create checkpoint <名称>` | `crunch-cli crunch checkpoint-create "<名称>" prizes.json` |
| `deposit reward <名称> <金额>` | `crunch-cli crunch deposit-reward "<名称>" <金额>` |
| `drain <名称>` | `crunch-cli crunch drain "<名称>"` |
| `create/register cruncher` | `crunch-cli cruncher create` |
| `register for <名称>` | `crunch-cli cruncher register "<名称>"` |
| `claim rewards <名称>` | `crunch-cli cruncher claim "<名称>"` |
| `show staking positions` | `crunch-cli staking positions` |
| `stake/deposit <金额>` | `crunch-cli staking deposit <金额>` |
| `delegate to <协调器>` | `crunch-cli staking delegate "<协调器>" <金额>` |
| `show staking rewards` | `crunch-cli staking rewards` |
| `claim staking rewards` | `crunch-cli staking claim` |
| `undelegate from <协调器>` | `crunch-cli staking undelegate "<协调器>" <金额>` |
| `withdraw stake <金额>` | `crunch-cli staking withdraw <金额>` |
| `init workspace <名称>` | `crunch-cli init-workspace "<名称>"` |
| `list scenarios/simulations` | `crunch-cli model list` |
| `run simulation <场景>` | `crunch-cli model run "<场景>"` |
| `register coordinator <名称>` | `crunch-cli coordinator register "<名称>"` |
| `create crunch <名称>` | `crunch-cli crunch create "<名称>" <金额> [maxModels]` |
| `start/end crunch <名称>` | `crunch-cli crunch start/end "<名称>"` |

## 执行流程

1. **解析**：识别用户请求的动作、目标、名称/标识符以及参数。
2. **配置文件解析**：如果用户指定了配置文件，根据文件内容切换工作区或应用相应的标志。
3. **语句映射**：使用预定义的语句映射表将用户请求转换为对应的 CLI 命令。
4. **执行命令**：运行相应的 `crunch-cli` 命令。
5. **输出格式化**：根据用户请求的格式（Slack、Telegram、Discord 或纯文本）生成输出结果。

## 输出格式

根据用户请求的格式（例如 “for slack” 或 “telegram format”）进行输出格式化：
- **Slack**：使用 `*bold*` 标记、`•` 项目符号以及 `━` 分隔符。
- **Telegram**：使用 `<b>bold</b>` 标记和表情符号前缀。
- **Discord**：使用 `##` 标题和 `**bold** 字体。
- **纯文本**：以简单的键值对形式输出信息。

## 错误处理

如果命令执行失败，会提示可能的解决方法：
- 网络设置错误？添加 `-n mainnet-beta` 或 `-n devnet`。
- 未找到钱包文件？添加 `-w /path/to/wallet.json`。
- 未找到相关资源？可以使用 `crunch-cli crunch list` 命令列出所有可用资源。

## 协调器节点设置

该技能用于创建协调器节点（竞赛的后端基础设施）：

```bash
crunch-cli init-workspace my-challenge
```

该命令会生成一个完整的节点工作区。如需自定义配置，请参考 ` coordinator-node-starter` 技能。

## 参考资料

完整的 CLI 文档请参阅：[references/cli-reference.md](references/cli-reference.md)