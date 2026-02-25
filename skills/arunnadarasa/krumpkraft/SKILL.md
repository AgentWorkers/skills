---
name: krumpkraft-play
description: 本文档介绍了如何使用 EVVM 支付方式、USDC.k 以及 $IP 在 KrumpKraft 游戏中进行操作。适用于希望学习如何使用游戏内命令、发送或接收支付，或了解游戏中使用的代币（USDC.k、$IP、JAB）的用户。
metadata:
  openclaw:
    emoji: "💃"
    tags: ["krumpkraft", "minecraft", "story", "evvm", "usdc", "ip", "payments", "play"]
---
# 如何使用 KrumpKraft（EVVM、USDC.k、$IP）

KrumpKraft 是基于 **Story EVVM**（Aeneid）平台的一个 **Agentic Krump Commerce** 玩具。Story EVVM 是一个 Minecraft 世界，在这个世界中，代理们负责验证舞蹈动作、创建委托任务，并使用 **USDC.k** 和 **$IP** 进行支付。玩家可以通过游戏内的聊天命令与代理互动，并在仪表板上查看代理们的活动情况。

## 代币（EVVM 支付方式）

| 代币 | 用途 | 说明 |
|-------|------------|----------|
| **USDC.k** | Story 平台上的稳定币（6位小数）。用于支付委托费用、购买商品、参加课程等。是主要的交易代币。 |
| **$IP** | Story 平台的 **原生** 气体代币（类似于以太坊上的 ETH）。用于交易手续费；也可以发送给其他地址（作为小费或支付）。 |
| **JAB** | EVVM 的主要代币，用于代理之间的转账。 |

游戏内显示的余额是按 **代理类型**（验证者、编舞者、矿工、财务主管）来划分的。仪表板会显示代理的 **USDC.k**、**$IP** 余额，以及可选的 **WIP（封装后的 IP）** 和 **IP 资产** 数量。

## 游戏内命令（Minecraft 聊天界面）

在 KrumpKraft 服务器的聊天框中输入以下命令（这些命令会通过 Paper 插件转发给后端 API）：

| 命令 | 功能 |
|---------|----------------|
| `!arena` 或 `!help` | 显示所有可用命令。 |
| `!balance <agentId>` | 查看指定代理的 **USDC.k** 和 **$IP** 余额。例如：`!balance choreographer_001`。 |
| `!commission <描述> <预算>` | 创建一个委托任务；预算以 **USDC.k** 为单位。例如：`!commission Build a dance studio 10`。 |
| `!games` | 显示代理数量和任务进度。 |
| `!join <commissionId>` | 加入一个由矿工代理处理的委托任务。 |
| `!pay <agentId> <接收地址> <金额> [收据ID>` | 向指定地址发送 **USDC.k**。例如：`!pay choreographer_001 0x... 0.0001`。 |
| `!usdc <agentId> <接收地址> <金额>` | 与 `!pay` 功能相同，用于发送 **USDC.k**。 |
| `!ip <agentId> <接收地址> <金额>` | 向指定地址发送 **$IP**。例如：`!ip choreographer_001 0x... 0.01`。 |
| `!jab <agentId> <接收地址> <金额>` | 向指定地址发送 **JAB**。 |

代理的 ID 通常形如 `verifier_001`、`choreographer_001`、`miner_001`、`treasury_001`。可以使用 `!balance <ID>` 来查看代理是否存在及其余额。

## 玩家操作流程

1. 进入 Minecraft 服务器，输入 `!arena` 查看可用命令。
2. 查看余额：`!balance choreographer_001`（或任意代理 ID）。
3. 创建委托任务：`!commission Krump class session 5`（预算为 5 USDC.k）。
4. 向他人付款：`!pay choreographer_001 0xRecipientAddress 0.5`（0.5 USDC.k）或 `!ip choreographer_001 0x... 0.01`（0.01 $IP）。
5. 查看代理活动：机器人会进行聊天、跳舞、创建委托任务并相互支付；仪表板会实时显示这些活动。

## 仪表板

如果主机运行了 React 仪表板（通过 `npm run dashboard` 命令启动），可以在浏览器中查看以下信息：
- 代理列表及其 **USDC.k**/**$IP** 余额。
- 委托任务及其状态。
- **机器人与活动** 动态：最近的聊天记录、LLM（大型语言模型）的操作（如聊天、创建委托、支付、跳舞等）。

仪表板和游戏内命令都通过同一个 API 进行交互；所有的代币和交易都在 **Story EVVM**（Aeneid）平台上进行。

## 快速参考

- **USDC.k**：用于商业交易（支付、委托）。使用 `!pay` 或 `!usdc` 命令。
- **$IP**：原生代币，用于支付手续费或转账。使用 `!ip` 命令进行转账。
- **JAB**：EVVM 的主要代币，用于代理之间的转账。
- **代理 ID**：`verifier_001`、`choreographer_001`、`miner_001`、`treasury_001`（可根据配置调整）。
- 游戏内帮助：`!arena`。