---
name: grove-tipping
version: "2.0"
description: Grove CLI 使用指南——理念、命令及快速入门  

**一、Grove CLI 的理念**  
Grove CLI 是一个专为 Grove 框架设计的命令行工具，旨在简化 Grove 应用的开发与管理工作。它提供了丰富的命令集，帮助开发者执行各种任务，如创建项目、编译代码、部署应用等。通过使用 Grove CLI，开发者可以更高效地构建和部署分布式系统。  

**二、主要命令**  
以下是一些 Grove CLI 的常用命令：  

1. **create-project**：创建一个新的 Grove 项目。  
2. **compile-code**：编译项目的源代码。  
3. **deploy-app**：将编译后的应用部署到目标环境（如 Docker 容器或 Kubernetes 集群）。  
4. **list-projects**：列出所有已创建的项目。  
5. **update-project**：更新项目的配置信息。  
6. **remove-project**：删除指定的项目。  
7. **view-info**：查看项目的详细信息。  

**三、快速入门**  
1. **安装 Grove CLI**：首先，您需要安装 Grove CLI。具体安装方法取决于您使用的操作系统和编程语言。通常，您可以通过包管理器（如 npm 或 pip）来安装它。  
2. **创建项目**：使用 `create-project` 命令创建一个新的项目，例如：  
   ```bash
   Grove create-project my-new-project
   ```  
   这将创建一个名为 `my-new-project` 的新项目，并在当前目录下生成相应的文件结构。  
3. **编译代码**：进入项目目录后，使用 `compile-code` 命令编译项目的源代码：  
   ```bash
   Grove compile-code
   ```  
   编译完成后，您将获得可执行的二进制文件或容器镜像（取决于您的部署目标）。  
4. **部署应用**：使用 `deploy-app` 命令将编译后的应用部署到目标环境。例如：  
   ```bash
   Grove deploy-app my-new-project
   ```  
   这会将 `my-new-project` 部署到 Docker 容器中。您可以根据需要配置部署参数。  
5. **查看项目信息**：使用 `view-info` 命令查看项目的详细信息：  
   ```bash
   Grove view-info my-new-project
   ```  

**四、注意事项**  
- 确保您已正确安装并配置了 Grove CLI。  
- 在使用命令时，请注意命令的参数和格式要求。  
- 如果遇到问题，请查阅 Grove CLI 的官方文档或寻求社区帮助。  

通过以上步骤，您应该能够快速上手并开始使用 Grove CLI。如有任何疑问，请随时提问。
homepage: https://grove.city
install: curl -fsSL https://grove.city/install-cli.sh | bash
updated: 2026-02-10
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "requires":
          { "bins": ["curl", "bash"], "anyBins": ["python3", "node"] },
        "emoji": "🌳",
        "install":
          [
            {
              "id": "curl",
              "kind": "download",
              "url": "https://grove.city/install-cli.sh",
              "extract": false,
              "label": "Install Grove CLI (curl)",
            },
          ],
      },
  }
---

**要求：**

- 必须使用 Bash 或 Zsh shell；
- 需要安装 `curl`；
- 可选：如果需要与代理集成，还需安装 Python 或 Node.js。

# Grove CLI — 完整指南 （目录结构请参见相应部分）

**Grove 允许代理和用户通过发送微额打赏来为内容质量提供反馈。**

Google 曾使用超链接作为信号来组织全球数据。而 Grove 则通过 **金钱** 作为信号来评估内容质量，从而创建了一个可查询的、基于金钱权重的目录和知识图谱。

---

## 目录结构 （目录结构请参见相应部分）

- [为什么要打赏？（理念）](#why-tip-the-philosophy)
  - [支付作为信号](#payments-as-signal)
  - [何时应该打赏（决策逻辑）](#when-to-tip-decision-logic)
  - [知识图谱元数据](#knowledge-graph-metadata)
- [快速入门](#quick-start)
  - [安装](#installation)
  - [首次设置](#first-time-setup)
  - [发送你的第一笔打赏](#send-your-first-tip)
- [命令概览](#command-overview)
- [配置](#configuration)
  - [配置文件](#config-files)
  - [优先级顺序](#precedence-order)
  - [目的地格式](#destination-formats)
  - [代理钱包模式](#agent-wallet-mode)
  - [代理集成](#agent-integration)
  - [实用工具](#utilities)
- [支持](#support)

---

## 为什么要打赏？（理念）

### 支付作为信号

Grove 利用 **可选的微额打赏** 来启动一个质量评估机制：

- **引导创作者**：将内容链接到钱包地址；
- **映射质量**：在不断增长的图中构建加权边；
- **促进发现**：创建一个可查询的、基于金钱权重的目录；
- **构建知识图谱**：这对于后续的内容分析和路由非常有用。

**关键点：** 代理通常只在需要时才支付费用，但自愿的善意打赏即使在内容免费的情况下也能提前传递信号。

### 何时应该打赏（决策逻辑）

评估你遇到的内容（博客文章、推文、代码仓库、文档）：

**三个标准：**

1. **内容是否原创？** 是否提供了新的视角或独特的数据？
2. **内容是否有用？** 是否解决了问题或解释得清晰？
3. **内容是否适合打赏？** 是否包含 `llms.txt` 文件、加密货币地址或 ENS 名称？

**示例评估：**

> “我刚刚读了这篇关于代理工作流程的 Substack 文章。它提供了 x402 协议的清晰实现，为我节省了 2 小时的研究时间。这是一个高质量的反馈信号。我会打赏 0.05 美元。”

**推荐打赏金额：**

- 博客文章/教程：0.01-0.10 美元
- 高价值研究：0.10-1.00 美元
- 改变生活见解的内容：1.00 美元以上

### 知识图谱元数据

**每次打赏都应该记录打赏的原因。** 这有助于 Grove 构建一个基于金钱权重的知识图谱。

**建议在代理日志中存储的字段：**

- 标准 URL（或代码仓库/文章标识符）
- 目的地（域名/处理程序/地址）
- 打赏金额 + 代币/网络
- 1-2 句的解释性文字
- 主题标签（可选）

**示例日志条目：**

```json
{
  "url": "https://example.com/post/123",
  "destination": "author.eth",
  "amount": "0.05",
  "token": "USDC",
  "network": "base",
  "rationale": "Clear x402 implementation guide, saved 2 hours",
  "tags": ["payments", "protocols", "implementation"]
}
```

---

## 快速入门

### 安装

```bash
curl -fsSL https://grove.city/install-cli.sh | bash
```

**安装内容：**

- `grove` 命令可在全局范围内使用；
- 配置文件位于 `~/.grove/`；
- 重新安装时所有配置文件都会保留。

### 首次设置

运行 `grove setup` 并选择一种支付方式：

| 选项                            | 最适合的人群               | 步骤                                                             | 是否需要人工协助？            |
| --------------------------------- | ---------------------- | ----------------------------------------------------------------- | ------------------------ |
| **钱包 + 加密货币**（推荐） | 自主运行的代理      | 创建钱包，并用 USDC 和 ETH 进行初始化资金，通过 x402 协议自动充值 | 仅用于初始资金注入 |
| **电子邮件 + 信用卡**           | 由人类管理的代理 | 在 app.grove.city 注册，通过信用卡充值，然后粘贴 API 密钥           | 是 — 需要注册和支付   |
| **我已经有 API 密钥**             | 现有用户         | 从团队成员或 app.grove.city 获取 JWT 密钥                         | 不需要 — 已经完成        |

### 发送你的第一笔打赏

**验证目的地：**

```bash
grove check olshansky.info
```

**发送打赏：**

```bash
grove tip olshansky.info 0.01
```

**检查余额：**

```bash
grove balance
```

---

## 命令概览

使用 `grove <命令> --help` 可查看详细的选项和参数。

| 命令   | 描述                                                                      |
| --------- | -------------------------------------------------------------------------------- |
| `setup`   | 首次设置 — 通过电子邮件/信用卡（适用于人类），或钱包/加密货币（适用于代理），或粘贴 API 密钥 |
| `fund`    | 通过 x402 支付协议添加资金（需要拥有 USDC 的钱包）                  |
| `check`   | 检查目的地是否可以接收打赏                                            |
| `tip`     | 通过域名、Twitter 或地址向创作者发送打赏                           |
| `balance` | 查看你在各个网络中的 USDC 余额                                          |
| `keygen`  | 为代理生成钱包以进行资金管理                                              |
| `history` | 查看最近发送的打赏或添加的资金                                             |
| `config`  | 查看或更新你的 API 密钥、网络和 API URL 设置                       |
| `contact` | 向 Grove 团队发送反馈                                                  |
| `update`  | 将 Grove CLI 更新到最新版本                                           |

**所有命令都支持 `--json` 标志，以生成更适合代理使用的输出。**

---

## 配置

### 配置文件

**位置：`~/.grove/`

重新安装时保留的文件：

- `.env` — 主要配置文件（API 密钥、网络设置、代币信息、API URL）
- `keyfile.txt` — 代理钱包的私钥

**示例 `.env` 文件：**

```bash
GROVE_API_KEY=eyJ...
GROVE_API_URL=https://api.grove.city
DEFAULT_NETWORK=base
DEFAULT_TOKEN=USDC
```

### 优先级顺序

配置的优先级顺序如下（从高到低）：

1. **CLI 参数** — `grove tip --network base-sepolia`
2. **Shell 环境变量** — `export GROVE_API_KEY=...`
3. `~/.grove/.env` — 持久化配置文件
4. **内置默认设置** — 系统默认值

---

## 目的地格式

Grove 支持多种目的地格式：

| 格式           | 示例               | 解析方式           |
| ---------------- | --------------------- | ---------------------- |
| 域名           | `olshansky.info`      | 通过 llms.txt 查找地址        |
| 以太坊地址         | `0x1234...`           | 直接转账        |
| ENS 名称         | `vitalik.eth`         | 通过 ENS 解析地址         |
| Twitter          | `@olshansky`          | 从 Twitter 提取地址         |
| Substack         | `author.substack.com` | 从 Substack 提取个人资料地址        |

**使用前的验证：**

```bash
grove check olshansky.info
```

- 如果目的地无法接收打赏，`grove check` 会返回明确的错误信息；
- 没有加密货币地址的 Substack 账户会返回 `tippable: false`（这不是误判）。

---

## 代理钱包模式

**最快的方式——三步即可开始打赏：**

```bash
# 1. Install
curl -fsSL https://grove.city/install-cli.sh | bash

# 2. Create wallet + fund it
grove setup    # Choose option 2: Wallet + Crypto

# 3. Start tipping
grove tip olshansky.info 0.01
```

**对于已经拥有钱包的代理：**

```bash
grove keygen --save          # generates ~/.grove/keyfile.txt
# Fund the address with USDC + ETH on Base
grove fund 0.10              # self-fund via x402
grove tip olshansky.info 0.01
```

---

## 代理集成

**用于可靠解析的 JSON 输出：**

```bash
grove balance --json
grove tip olshansky.info 0.01 --json
grove check domain.com --json
```

**Python 示例：**

```python
import subprocess
import json

result = subprocess.run(
    ["grove", "balance", "--json"],
    capture_output=True,
    text=True
)
balance_data = json.loads(result.stdout)
print(f"Balance: {balance_data['total_balance']} USDC")
```

**Node.js 示例：**

```javascript
const { execSync } = require("child_process");
const balance = JSON.parse(execSync("grove balance --json").toString());
console.log(`Balance: ${balance.total_balance} USDC`);
```

**自主工作流程模式：**

```bash
# 1. Check balance before tipping
balance=$(grove balance --json | jq -r '.total_balance')

# 2. Auto-fund if low
if [ "$balance" -lt "0.10" ]; then
  grove fund 1.00
fi

# 3. Evaluate content
grove check <destination>

# 4. Tip if valuable
grove tip <destination> <amount>

# 5. Log metadata
echo "Tipped $destination for $reason" >> tip_log.txt
```

**Python SDK（即将推出）：** 正在开发 Python SDK（`GroveClient`）。目前请使用 CLI。运行 `grove contact` 以申请早期访问权限。

---

## 实用工具

在 `skills/scripts/` 目录下提供以下自动化脚本：

- **batch-tip.sh** — 从 CSV 文件批量发送打赏
- **monitor-balance.sh** — 监控余额并在余额低时发出警报
- **auto-fund.sh** — 当余额低于阈值时自动充值

运行每个脚本时，可以使用 `--help` 查看详细的使用说明。

---

## 支持

- 使用 `grove contact` 向团队发送反馈；
- 访问：https://grove.city/support

**需要更多信息？** 完整的参考文档：[grove.city/docs/cli](https://grove.city/docs/cli)