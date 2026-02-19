---
name: crunch-coordinate
description: >
  **使用说明：**  
  通过 `crunch-cli` 工具来管理 Crunch 协调员、竞赛（crunches）、奖励、检查点（checkpoints）、质押（staking）以及参与竞赛的用户（cruncher accounts）时，请参考以下说明。
---
# Crunch Protocol CLI 技能

该技能可将自然语言查询转换为 `crunch-cli` 命令，支持配置输出格式（Slack、Telegram、Discord 或纯文本）以及使用不同的工作区（profiles）。

## 先决条件
- 安装了 Node.js 18 及以上版本，并且已安装 `npm`。
- 拥有 Solana 钱包的密钥对（用于链上操作）。

## 包安装

该技能通过 npm（全局安装）来安装相关包：

| 包名 | 来源 | 用途 |
|---------|--------|---------|
| `@crunchdao/crunch-cli` | [npm](https://www.npmjs.com/package/@crunchdao/crunch-cli) | CrunchDAO 协议的 CLI 工具（用于协调器管理、竞赛组织和质押操作） |

**包安装的规则：**
- **仅从官方 npm 注册表中安装 `@crunchdao/crunch-cli`**。
- **禁止使用自定义注册表地址**（不允许使用 `--registry` 参数）。
- **在安装前需询问用户是否已安装该包**。

## 凭据

### Solana 钱包密钥对（链上操作必需）
- **定义：** 一个包含 Solana 私钥的 JSON 文件，用于签署交易。
- **配置方式：** 通过 `crunch-cli config set wallet /path/to/wallet.json` 命令或命令行参数 `-w` 进行设置。
- **存储位置：** 存储在用户指定的文件中（通常位于 `~/.crunch/config.json`）。

**关于钱包的处理规则：**
- **除非用户明确要求并了解相关安全风险，否则绝不创建或生成新的钱包密钥对**。
- **绝不读取或显示钱包密钥对文件的内容**。
- **绝不将钱包文件提交到 Git 仓库**（确保 `.gitignore` 文件中包含了这些文件）。
- **在安装前必须获取用户的钱包路径**，切勿自行查找密钥对文件。

### 配置文件（`~/.crunch/config.json`）
- 该文件用于存储每个工作区的网络设置、钱包路径以及 RPC 请求的 URL。
- 可通过 `crunch-cli config` 命令进行管理，无需手动编辑。
- **除非用户明确要求，否则不得修改或删除现有配置文件**。

## 设置

```bash
npm install -g @crunchdao/crunch-cli
crunch-cli --version
```

## 工作区（Profiles）

该 CLI 支持通过 `~/.crunch/config.json` 文件进行工作区配置管理：

```bash
crunch-cli config show                    # Show current config
crunch-cli config active                  # Show resolved active values
crunch-cli config list-profiles           # List available profiles
crunch-cli config save-profile <name>     # Save current config as profile
crunch-cli config use <profile>           # Switch profile
crunch-cli config set <key> <value>       # Set config value
```

某些全局命令参数可以覆盖配置文件中的设置：

| 参数 | 说明 |
|------|-------------|
| `-n, --network` | Solana 网络：`mainnet-beta`、`devnet`、`localhost` |
| `-u, --url` | 自定义 RPC 请求的 URL |
| `-w, --wallet` | Solana 钱包密钥对的路径 |
| `-o, --output` | 输出格式：`json`、`table`、`yaml` |

## 语句与命令的映射关系

| 用户输入 | 对应的 CLI 命令 |
|-------------|-------------|
| `get/show crunch <name>` | `crunch-cli crunch get "<name>"` |
| `list crunches` | `crunch-cli crunch list` |
| `get/show coordinator [address]` | `crunch-cli coordinator get [address]` |
| `list coordinators` | `crunch-cli coordinator list` |
| `get config` | `crunch-cli coordinator get-config` |
| `checkpoint for <name>` | `crunch-cli crunch checkpoint-get-current "<name>"` |
| `create checkpoint <name>` | `crunch-cli crunch checkpoint-create "<name>" prizes.json` |
| `deposit reward <name> <amount>` | `crunch-cli crunch deposit-reward "<name>" <amount>` |
| `drain <name>` | `crunch-cli crunch drain "<name>"` |
| `create/register cruncher` | `crunch-cli cruncher create` |
| `register for <name>` | `crunch-cli cruncher register "<name>"` |
| `claim rewards <name>` | `crunch-cli cruncher claim "<name>"` |
| `show staking positions` | `crunch-cli staking positions` |
| `stake/deposit <amount>` | `crunch-cli staking deposit <amount>` |
| `delegate to <coordinator>` | `crunch-cli staking delegate "<coordinator>" <amount>` |
| `show staking rewards` | `crunch-cli staking rewards` |
| `claim staking rewards` | `crunch-cli staking claim` |
| `undelegate from <coordinator>` | `crunch-cli staking undelegate "<coordinator>" <amount>` |
| `withdraw stake <amount>` | `crunch-cli staking withdraw <amount>` |
| `init workspace <name>` | `crunch-cli init-workspace "<name>"` |
| `list scenarios/simulations` | `crunch-cli model list` |
| `run simulation <scenario>` | `crunch-cli model run "<scenario>"` |
| `register coordinator <name>` | `crunch-cli coordinator register "<name>"` |
| `create crunch <name>` | `crunch-cli crunch create "<name>" <amount> [maxModels]` |
| `start/end crunch <name>` | `crunch-cli crunch start/end "<name>"` |

## 执行流程
1. **解析用户输入**：确定要执行的操作、目标对象、名称/标识符以及相关参数。
2. **选择相应的工作区配置**：如果需要，根据用户输入切换工作区或使用相应的参数。
3. **查找对应的命令**：根据用户输入的语句，在预定义的映射表中找到对应的 CLI 命令。
4. **执行命令**。
5. **格式化输出**：根据用户指定的输出格式（Slack、Telegram、Discord 或纯文本）生成结果。

## 输出格式
根据用户的请求（例如 “for slack” 或 “telegram format”）来决定输出格式：
- **Slack**：使用 `*bold*` 标记、`•` 项目符号和 `━` 分隔符。
- **Telegram**：使用 `<b>bold</b>` 标记和表情符号。
- **Discord**：使用 `##` 标题和 `**bold** 字体。
- **纯文本**：以键值对的形式显示信息。

## 错误处理
如果命令执行失败，会提供相应的解决方法：
- 如果网络设置错误，建议添加 `-n mainnet-beta` 或 `-n devnet` 参数。
- 如果缺少钱包信息，建议添加 `-w /path/to/wallet.json` 参数。
- 如果找不到所需的信息，可以使用 `crunch-cli crunch list` 命令列出所有可用的工作区。

## 协调器节点设置

该技能可用于创建一个新的竞赛工作区：

```bash
crunch-cli init-workspace my-challenge
```

该命令会生成一个完整的节点工作区。如需自定义配置，请参考 ` coordinator-node-starter` 技能。

## 参考资料
完整的 CLI 文档请参阅：[references/cli-reference.md](references/cli-reference.md)