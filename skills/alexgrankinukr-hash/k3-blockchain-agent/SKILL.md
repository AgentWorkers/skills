---
name: k3-blockchain-agent
description: 在 K3 上构建自动化区块链分析工作流：从接收自然语言请求开始，到部署并运行自动化脚本，这些脚本会从区块链上获取数据，利用人工智能进行分析，并通过电子邮件、Telegram 或 Slack 提供分析结果。每当用户提到区块链工作流、链上分析、DeFi 监控、代币追踪、钱包警报、矿池分析、协议仪表板、NFT 跟踪、自动化交易、智能合约监控，或任何涉及区块链数据自动化处理的需求时，都可以使用这项技能。此外，当用户提到 K3、工作流构建工具，或希望生成定期的加密货币/DeFi 报告时，该技能也同样适用。即使用户只是简单地说“监控这个钱包”或“追踪这个代币”，这项技能也同样适用。
---
# K3区块链代理

将诸如“每天发送关于Uniswap上WETH/USDC池的更新”这样的请求，转换为已完全部署的工作流程，这些流程能够自动获取数据、运行AI分析并生成报告。

## 设置

使用此技能需要连接**K3开发MCP**。MCP提供了`generateWorkflow`、`executeWorkflow`、`findAgentByFunctionality`等工具，允许你以编程方式创建和管理区块链工作流程。

如果K3 MCP尚未连接，请告知用户在进行下一步操作之前先进行连接。连接成功后，通过调用`listTeamMcpServerIntegrations()`来验证连接情况——这将显示用户团队已集成的数据源（如TheGraph、CoinGecko等）。每个团队的集成方案可能不同，因此请先了解可用的集成资源，而不是盲目猜测。

## 工作流程构建方式

K3的编排器采用**对话式**交互方式。你用简单的语言描述需求，编排器会提出澄清问题，然后构建并部署工作流程。你的任务是提供准确的信息，以确保对话高效进行。

**常见错误：**跳过“测试”步骤——这会导致部署的工作流程返回空数据。

## 第一步：理解请求

当用户请求创建一个工作流程时，需要明确以下参数：
- **数据目标**：他们需要哪些区块链数据（例如：池指标、代币价格、钱包余额、NFT数据）。
- **协议**：使用的是哪种DeFi协议或链特性（例如：Uniswap、Aave、SushiSwap）。
- **链**：使用的是哪个区块链（例如：Ethereum、Arbitrum、Polygon、Base、Stellar）。
- **调度**：工作流程的运行频率或触发条件（例如：每日、每小时、按需、基于钱包活动、合同事件、Telegram聊天机器人）。
- **分析**：需要哪种类型的分析结果（例如：性能总结、异常警报、趋势报告、交易信号）。
- **交付方式**：结果应如何发送（例如：电子邮件、Telegram、Slack、Google Sheets）。
- **操作**：工作流程是否需要执行某些操作（例如：执行交易、转移代币、写入合约）。
- **具体信息**：是否需要特定的地址或ID（例如：池地址、代币合约地址、钱包地址）。

如果用户是DeFi新手，在讲解过程中简要解释相关概念（例如：TVL的含义、流动性池的作用等）。不要假设用户了解这些专业术语。

## 第二步：找到合适的数据来源

这是关键步骤。K3提供了多种方式将数据导入工作流程，你需要根据用户的具体需求选择合适的方法。

### K3的数据获取函数

以下是用于将数据导入工作流程的内置函数。详细信息请参阅`references/node-types.md`：

| 函数 | 功能 |
|---------|--------|
| **Read API** | 调用任何REST/GraphQL API（最灵活的选择） |
| **Read Smart Contract** | 直接在链上查询智能合约 |
| **Read Market Data** | 获取代币价格、交易量、市场指标 |
| **Read Wallet** | 获取钱包余额、交易记录 |
| **Read NFT** | 获取NFT集合、底价、属性、持有者信息 |
| **Read Graph** | 使用自定义GraphQL查询TheGraph子图 |
| **Read Deployment** | 从K3上部署的代码中获取输出 |
| **AI Web Scraper** | 从网页中提取结构化数据 |
| **AI Agent with tools** | 由AI动态决定获取的数据内容 |

### 如何找到所需数据

目标是找到获取用户所需数据的最佳方法。可以将这视为问题解决过程——通常有多种有效的方法，你可以尝试以下几种：
1. **查看团队已有的集成**：调用`listTeamMcpServerIntegrations()`，了解已连接的MCP数据源。如果他们使用了TheGraph、CoinGecko等集成，这些通常是较简单的途径。
2. **搜索现有模板**：使用`findAgentByFunctionality()`根据用户的需求查找类似的模板。如果有人已经构建过类似的工作流程，可以以此作为起点。
3. **选择合适的K3函数**：
   - 需要链上合约数据？→ 使用`Read Smart Contract`直接查询。
   - 需要代币价格或市场数据？→ `Read Market Data`内置了这些功能。
   - 需要复杂的DeFi指标（如TVL、交易量、费用）？→ 使用`Read Graph`或`Read API`调用相应的分析端点。
   - 需要钱包信息？→ 使用`Read Wallet`获取余额和交易记录。
   - 需要NFT数据？→ 使用`Read NFT`获取集合和元数据。
   - 需要从公共API获取数据？→ `Read API`可以调用任何API。
   - 需要抓取网站数据？→ `AI Web Scraper`可以提取并整理数据。
4. **在网上查找正确的API端点**：如果需要特定协议的数据，可以搜索`{protocol name} API`、`{protocol name} subgraph`或`{protocol name} GraphQL endpoint`。许多协议都会公开API和子图。
5. **询问用户**：他们可能知道API端点、API密钥，或者知道要从哪个智能合约获取数据。

**重要提示**：获取数据的方法通常不止一种。例如，Uniswap池的TVL可以通过`Read Graph`（子图查询）、`Read API`（调用分析端点）或`Read Smart Contract`（直接读取合约）来获取。选择最可靠且能提供所需数据格式的方法。

### 在构建之前进行测试

在构建完整的工作流程之前，先验证数据源是否确实能返回预期的数据：

**测试步骤**可以节省后续大量的调试时间。一个返回错误数据的工作流程比没有工作流程更糟糕。

## 第三步：构建工作流程

向K3编排器提供所有所需的信息。使用`generateWorkflow()`并提供详细的说明，包括：
- **触发类型和调度**（例如：“每天运行”或“在钱包活动时触发”）。
- **数据来源及查询方式**（例如：“使用Read Graph查询X池”或“使用Read Smart Contract获取代币对的信息”）。
- **AI需要分析的内容**（例如：“突出显示TVL变化超过5%的情况”）。
- **需要执行的操作**（例如：“如果满足条件，在Uniswap上执行交易”）。
- **结果交付方式**（例如：“发送Telegram警报”或“通过电子邮件发送报告”）。
- **编排器所需的MCP集成ID**（来自团队的集成资源）。

首次调用时将`deployWorkflow`设置为`false`，以便在部署前进行审查。编排器可能会进一步提问，使用`editGeneratedWorkflow()`和相同的`generatedWorkflowId`进行回复。这种来回沟通是正常的，通常需要2-4轮交流。

确认配置无误后，最后一次调用`editGeneratedWorkflow()`并设置`deployWorkflow`为`true`。

有关可用函数、触发器、AI模型和输出选项的完整列表，请参阅`references/node-types.md`。

## 第四步：部署和验证

部署完成后：
1. 使用`executeWorkflow()`手动运行工作流程以进行即时测试。
2. 使用`getWorkflowRuns()`或`getWorkflowRunById()`检查运行情况。
3. **验证整个流程**：数据是否成功获取？AI是否完成了分析？通知是否已发送？

如果出现问题，使用`editGeneratedWorkflow()`进行修复——无需重新开始。有关常见问题的解决方法，请参阅`references/troubleshooting.md`。

告知用户工作流程已上线并会每天运行：“你的工作流程已启动，我刚刚进行了测试——这是第一份报告的内容：[报告摘要]。”

## K3 MCP工具参考

| 工具 | 功能 |
|------|--------|
| `generateWorkflow` | 从自然语言开始构建工作流程 |
| `editGeneratedWorkflow` | 继续与编排器进行交流 |
| `executeWorkflow` | 手动运行工作流程 |
| `getWorkflowById` | 获取工作流程详情和配置 |
| `getWorkflowRuns` | 查看执行历史记录 |
| `getWorkflowRunById` | 获取特定执行的详情和输出 |
| `updateWorkflow` | 暂停/恢复计划中的工作流程 |
| `findAgentByFunctionality` | 查找现有的工作流程模板 |
| `listAgentTemplates` | 浏览所有可用模板 |
| `getAgentTemplateById` | 获取特定模板的详细信息 |
| `listTeamMcpServerIntegrations` | 查看团队已连接的数据源 |
| `listMcpServerIntegrations` | 浏览所有可用的MCP数据源 |

## 重要规则：
1. **在构建完整工作流程之前务必测试数据来源**。快速测试可以节省大量调试时间。
2. **编排器采用对话式交互**——预计会通过`editGeneratedWorkflow`进行多次沟通。
3. **如果需要查询信息，请向用户询问**——不要猜测电子邮件地址、Telegram处理方式或钱包地址。
4. **了解团队的集成情况**：调用`listTeamMcpServerIntegrations()`查看可用的集成资源。每个团队的集成方案可能不同。
5. **在告知用户工作流程完成之前，先验证其是否正常运行**。运行工作流程，检查输出结果，确认通知是否已发送。
6. **注意使用场景**——不要同时调用多个K3 MCP工具或一次性传输大量数据。只获取所需的数据，检查后继续下一步。
7. **使用网络搜索**来查找API端点、子图URL和智能合约地址。网络是你的研究工具。

## 更深入的学习资源：
- `references/node-types.md`：所有触发类型、数据函数、AI函数、DeFi/交易操作和通知选项。
- `references/data-sources.md`：如何发现和评估不同区块链数据来源。
- `references/workflow-patterns.md`：常见的工作流程架构及其适用场景。
- `references/troubleshooting.md`：诊断和解决工作流程中的常见问题。