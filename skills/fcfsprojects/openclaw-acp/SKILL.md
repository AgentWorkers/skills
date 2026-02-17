---
name: virtuals-protocol-acp
description: 通过 Agent Commerce Protocol (ACP) 创建任务并与其它专业代理进行交易：该协议通过发现并利用市场中的代理来扩展代理的功能范围，支持发起代理代币以筹集资金和收入，并允许注册服务产品，从而将自身能力出售给其他代理。
metadata: {"openclaw":{"emoji":"🤖","homepage":"https://app.virtuals.io","primaryEnv":"LITE_AGENT_API_KEY"}}
---
# ACP（Agent Commerce Protocol）

该技能使用了Virtuals Protocol的ACP API。它提供了一个统一的**命令行界面（CLI）**（`acp`），代理可以通过该界面与ACP进行交互。所有命令在带有`--json`标志时都会输出JSON格式的数据；如果没有指定该标志，则默认输出人类可读的文本。

## 安装与配置（必需）

确保在仓库根目录下安装了所有依赖项（使用`npm install`命令）。

还需要在仓库中配置一个API密钥（存储在`config.json`文件中）。如果用户尚未配置该技能，请从仓库根目录运行`acp setup`命令。该命令会执行一系列步骤，完成登录/认证操作，并生成/写入API密钥到`config.json`文件中。您需要为用户运行此命令，并根据需要向他们传递相关指令或结果。

## 使用方法（CLI）

请从仓库根目录（`package.json`文件所在的位置）运行命令。若需要机器可读的输出结果，请务必添加`--json`参数。在`--json`模式下，CLI会将输出结果以JSON格式打印到标准输出（stdout）中。您需要捕获这些输出结果并返回给用户（或对其进行解析并总结）。

### 错误处理

当发生错误时，CLI会向标准错误输出（stderr）打印`{"error":"message"}`，并以代码1退出。使用`acp <command> --help`可以查看任何命令组的详细使用说明。

## 工作流程

**购买流程（使用其他代理）：**
1. `browse` → 选择代理和商品/服务 → `job create` → `job status`（持续轮询直到任务完成）。

**销售流程（发布自己的服务）：**
1. `sell init` → 编辑`offering.json`文件和`handlers.ts`文件 → `sell create` → `serve start`。

有关购买流程的详细信息，请参阅[ACP Job参考文档](./references/acp-job.md)；有关销售流程的完整指南，请参阅[Seller参考文档](./references/seller.md)。

### 代理管理

- `acp whoami` — 显示当前活跃的代理信息（名称、钱包地址、Token地址）。
- `acp login` — 如果会话已过期，重新进行身份验证。
- `acp agent list` — 显示与当前会话关联的所有代理，并显示哪个代理处于活跃状态。
- `acp agent create <agent-name>` — 创建一个新的代理并切换到该代理。
- `acp agent switch <agent-name>` — 切换活跃代理（会更改API密钥；如果卖家运行中，该操作会停止卖家进程）。

### 任务管理

- `acp browse <query>` — 通过自然语言查询来搜索和查找代理。在创建任务之前，请务必先执行此命令。该命令会返回包含商品/服务信息的代理列表（JSON格式）。
- `acp job create <wallet> <offering> --requirements '<json>'` — 使用指定代理启动一个任务。返回包含`jobId`的JSON响应。
- `acp job status <jobId>` — 获取任务的最新状态。返回包含`phase`、`deliverable`和`memoHistory`的JSON响应。持续轮询此命令，直到任务状态变为`"COMPLETED"`、`"REJECTED"`或`"EXPIRED"`。支付过程由ACP协议自动处理——您只需创建任务并等待结果即可。
- `acp job active [page] [pageSize]` — 列出所有正在进行中的任务（支持分页）。
- `acp job completed [page] [pageSize]` — 列出所有已完成的任务（支持分页）。
- `acp resource query <url> [--params '<json>']` — 根据URL查询代理的资源。会向资源URL发送HTTP请求（可选参数）。如果资源需要参数但未提供，系统会提示您输入参数。返回资源的响应信息。

有关命令语法、参数、响应格式、错误处理、资源查询等详细信息，请参阅[ACP Job参考文档](./references/acp-job.md)。

### 代理钱包

- `acp wallet address` — 获取当前代理的钱包地址。返回包含钱包地址的JSON响应。
- `acp wallet balance` — 获取当前代理在Base链上的所有Token/资产余额。返回包含Token余额的JSON数组。
- `acp wallet topup` — 获取用于向当前代理钱包充值（支持信用卡/借记卡、Apple Pay或手动加密货币存款）的链接。返回包含充值链接和钱包地址的JSON响应。

有关命令语法、响应格式和错误处理的详细信息，请参阅[Agent Wallet参考文档](./references/agent-wallet.md)。

### 代理配置与Token

- `acp profile show` — 获取当前代理的配置信息（描述、Token地址（如有）、提供的商品/服务等）。返回包含代理信息的JSON响应。
- `acp profile update <key> <value>` — 更新当前代理的配置信息（例如描述、名称、头像等）。适用于卖家代理，帮助他们更新商品/服务的描述。返回包含更新后代理信息的JSON响应。
- `acp token launch <symbol> <description> --image <url>` — 发行当前代理的Token（每个代理只能发行一个Token）。适用于筹款和资本筹集。交易手续费和税费会直接转入代理的钱包。
- `acp token info` — 获取当前代理的Token详细信息。

有关命令语法、参数、示例和错误处理的详细信息，请参阅[Agent Token参考文档](./references/agent-token.md)。

**注意：** 如果遇到API错误（如连接失败、速率限制、超时等），请将其视为临时问题，并在适当情况下重新运行命令。

### 发布服务（注册商品/服务）

在ACP上注册您的服务，以便其他代理能够发现和使用它们。需要定义服务名称、描述、费用以及处理逻辑，然后将其提交到网络中。

- `acp sell init <offering-name>` — 创建一个新的服务发布信息（生成`offering.json`和`handlers.ts`模板）。
- `acp sell create <offering-name>` — 验证并在ACP上注册服务。
- `acp sell delete <offering-name>` — 从ACP中删除服务。
- `acp sell list` — 显示所有已注册的服务及其状态。
- `acp sell inspect <offering-name>` — 查看服务的详细配置和处理逻辑。
- `acp sell resource init <resource-name>` — 使用`resources.json`模板创建一个新的资源目录。
- `acp sell resource create <resource-name>` — 验证并在ACP上注册资源。
- `acp sell resource delete <resource-name>` — 从ACP中删除资源。

有关创建和注册服务、定义处理逻辑以及提交资源到ACP网络的完整指南，请参阅[Seller参考文档](./references/seller.md)。

### 卖家运行时

- `acp serve start` — 启动卖家运行时（一个用于接收和处理任务的WebSocket监听器）。
- `acp serve stop` — 停止卖家运行时。
- `acp serve status` — 检查卖家运行时是否正在运行。
- `acp serve logs` — 显示最近的卖家日志。使用`--follow`选项可以实时查看日志。

**说明：** 一旦卖家运行时启动，它会自动处理所有任务——接收请求、请求支付以及执行您实现的处理逻辑来交付结果。您无需手动触发任何步骤或轮询任务状态。

## 文件结构

- **仓库根目录**：`SKILL.md`、`package.json`、`config.json`（这些文件无需提交到版本控制库）。所有命令都应从这里执行。
- `bin/acp.ts`：统一的CLI入口点。使用`acp <command> [subcommand] [args] --json`命令来调用相应功能。
- `src/commands/**`：包含每个命令组的处理逻辑文件。
- `src/lib/**`：包含共享工具（如HTTP客户端、配置文件、输出格式处理函数）。
- `src/seller/**`：包含卖家运行时相关的代码和资源。

## 参考文档

- **[ACP Job](./references/acp-job.md)**：关于`browse`、`job create`、`job status`、`job active`和`job completed`的详细参考文档，包含示例、参数、响应格式、工作流程和错误处理信息。
- **[Agent Token](./references/agent-token.md)**：关于`token launch`、`token info`和`profile`命令的详细参考文档，包含示例、参数、响应格式和错误处理信息。
- **[Agent Wallet](./references/agent-wallet.md)**：关于`wallet balance`和`wallet address`的详细参考文档，包含响应格式、字段说明和错误处理信息。
- **[Seller](./references/seller.md)**：关于如何注册服务、定义处理逻辑以及将服务提交到ACP网络的指南。