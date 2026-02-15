---
name: warden-agent-builder
description: "为 Warden 协议构建原创的 LangGraph 代理，并准备好在 Warden Studio 中发布这些代理。当用户需要执行以下操作时，可以使用此技能：  
(1) 创建新的 Warden 代理（非社区提供的示例）；  
(2) 构建基于 LangGraph 的加密/Web3 代理；  
(3) 通过 LangSmith 部署工具或自定义基础设施来部署代理；  
(4) 参与 Warden 代理构建者激励计划（面向 OpenClaw 代理开发者）；  
(5) 将代理集成到 Warden Studio 中以实现代理的发布。"
---

# Warden Agent Builder

用于构建和部署Warden Protocol的Agentic Wallet生态系统所需的LangGraph代理程序。

## ⚠️ 重要提示：关于示例代理程序

Warden社区的仓库中包含的是**用于学习的示例代理程序**，而非可以直接复制的模板：

- **Weather Agent**：通过研究这个代理程序来了解简单的数据获取方式。
- **CoinGecko Agent**：通过研究这个代理程序来学习基于模式的推理（Schema-Guided Reasoning, SGR）技术。
- **Portfolio Agent**：通过研究这个代理程序来学习复杂的多源数据集成方法。

**请勿直接构建这些代理程序**——它们已经存在了。相反，请：
1. **研究**它们的代码以理解其工作模式。
2. **学习**它们的架构和工作流程。
3. **为激励计划构建**全新的、原创的代理程序。

您的代理程序必须**具有独特性，并解决一个不同的问题**，才能符合激励计划的资格。

## 概述

Warden Protocol是一个“Agentic Wallet”，适用于“Do-It-For-Me”经济模式，并为部署到Warden的OpenClaw代理程序提供了一个活跃的代理程序构建激励计划。所有代理程序都必须基于LangGraph构建，并且可以通过API进行访问。

**关键资源：**
- 社区代理程序仓库：https://github.com/warden-protocol/community-agents
- 文档：https://docs.wardenprotocol.org
- Discord：#developers频道（用于获取支持）

## 需求清单

在构建之前，请确保您的代理程序满足以下强制要求：

✓ **框架**：使用LangGraph构建（TypeScript或Python）
✓ **部署方式**：支持LangSmith部署或自定义基础设施
✓ **访问方式**：可以通过API访问（无需用户界面——Warden提供了用户界面）
✓ **隔离性**：每个LangGraph实例只能运行一个代理程序
✓ **安全限制**（第一阶段）：
  - 不能访问用户钱包
  - 不能在Warden的基础设施上存储数据

✓ **功能**：可以实现以下工作流程：
  - Web3/Web2自动化
  - API集成
  - 数据库连接
  - 与外部工具的交互

## 了解示例代理程序

社区代理程序仓库中提供了**参考示例**，供您学习，而非可以直接复制的模板：

### 示例代理程序1：LangGraph快速入门（了解基础知识）
**位置**：`agents/langgraph-quick-start`（TypeScript）或`agents/langgraph-quick-start-py`（Python）
**学习内容**：LangGraph的基础知识、最小化的代理程序结构
**研究内容**：集成OpenAI的单节点聊天机器人

```bash
git clone https://github.com/warden-protocol/community-agents.git
cd community-agents/agents/langgraph-quick-start
```

### 示例代理程序2：Weather Agent（学习结构）
**位置**：`agents/weather-agent`
**学习内容**：简单的数据获取、API集成、用户友好的响应方式
**研究内容**：
- 如何从外部API（如WeatherAPI）获取数据
- 数据的处理和格式化
- 清晰的功能范围和结构
**⚠️ 请勿直接构建**：这个代理程序已经存在。先研究它，然后构建全新的代理程序。

### 示例代理程序3：CoinGecko Agent（学习基于模式的推理）
**位置**：`agents/coingecko-agent`
**学习内容**：基于模式的推理（Schema-Guided Reasoning, SGR）技术
**研究内容**：
- 五步SGR工作流程：验证 → 提取 → 获取 → 验证 → 分析
- 比较分析方法
- 错误处理和数据验证
**⚠️ 请勿直接构建**：这个代理程序已经存在。研究其模式，并将其应用于新的使用场景。

### 示例代理程序4：Portfolio Analysis Agent（学习高级功能）
**位置**：`agents/portfolio-agent`
**学习内容**：多源数据合成、生产级架构
**研究内容**：
- 集成多个API（如CoinGecko和Alchemy）
- 支持多种区块链（EVM和Solana）
- 复杂的SGR工作流程
- 综合报告功能
**⚠️ 请勿直接构建**：这个代理程序已经存在。研究其架构，然后为您自己的代理程序开发新的功能。

## 重要提示：构建全新的代理程序

这些示例程序的目的是为了传授工作模式和最佳实践。为了符合激励计划的要求，您必须创建一个**原创的、独特的代理程序**，解决一个不同的问题。请不要简单地复制Weather Agent、CoinGecko Agent或Portfolio Agent。

## 构建您的原创代理程序

### 第一步：研究示例程序并选择您的开发方法

**请勿直接克隆示例程序进行修改**。相反，请：
1. **研究示例程序**以了解工作模式：
   - 简单的数据获取 → 学习Weather Agent
   - 复杂的分析 → 学习CoinGecko Agent
   - 多源数据合成 → 学习Portfolio Agent
2. **确定您的独特使用场景**：
   - 您的代理程序将解决什么问题？
   - 它将使用哪些API或数据源？
   - 它与现有的代理程序有何不同？
3. **规划您的代理程序的工作流程**：
   - 是简单的请求-响应模式？
   - 基于模式的推理（SGR）？
   - 多步骤分析？

### 第二步：初始化您的新代理程序

使用初始化脚本创建一个新的项目：

```bash
# Create your unique agent
python scripts/init-agent.py my-unique-agent \
  --template typescript \
  --description "Description of what YOUR agent does"

# Navigate to project
cd my-unique-agent

# Install dependencies
npm install  # TypeScript
# OR
pip install -r requirements.txt  # Python
```

这将创建一个干净的起点，而不是现有代理程序的副本。

### 第三步：了解LangGraph代理程序的结构

每个LangGraph代理程序都遵循以下基本结构：

```
your-agent/
├── src/
│   ├── agent.ts/py          # Main agent logic (YOUR CODE)
│   ├── graph.ts/py          # LangGraph workflow definition (YOUR CODE)
│   └── tools.ts/py          # Tool implementations (YOUR CODE)
├── package.json / requirements.txt
├── langgraph.json           # LangGraph configuration
└── README.md
```

**需要实现的关键文件**：
- `graph.ts/py`：定义您的工作流程（验证 → 处理 → 响应）
- `agent.ts/py`：实现您的核心逻辑
- `tools.ts/py`：集成与您的代理程序功能相关的外部API

### 第四步：实现您的自定义代理逻辑

**从示例程序中学习模式，并将其应用于您的使用场景**：

**如果构建的是简单的数据获取程序**（如Weather Agent的模式）：
```typescript
// Define workflow
const workflow = new StateGraph({
  channels: agentState
})
  .addNode("fetch", fetchYourData)      // YOUR API
  .addNode("process", processYourData)  // YOUR logic
  .addNode("respond", generateResponse);

workflow
  .addEdge(START, "fetch")
  .addEdge("fetch", "process")
  .addEdge("process", "respond")
  .addEdge("respond", END);
```

**如果构建的是复杂的分析程序**（如CoinGecko Agent的模式，使用SGR）：
```typescript
// Define 5-step SGR workflow
const workflow = new StateGraph({
  channels: agentState
})
  .addNode("validate", validateYourInput)     // YOUR validation
  .addNode("extract", extractYourParams)      // YOUR extraction
  .addNode("fetch", fetchYourData)            // YOUR APIs
  .addNode("analyze", analyzeYourData)        // YOUR analysis
  .addNode("generate", generateYourResponse); // YOUR formatting

workflow
  .addEdge(START, "validate")
  .addEdge("validate", "extract")
  .addEdge("extract", "fetch")
  .addEdge("fetch", "analyze")
  .addEdge("analyze", "generate")
  .addEdge("generate", END);
```

**关键原则**：
1. 保持工作流程的线性和可预测性。
2. 在每个阶段验证输入数据。
3. 优雅地处理错误。
4. 使用OpenAI进行自然语言生成。
5. 保持响应的一致性。

**重要提示**：这应该是您自己为解决问题而开发的实现，而不是复制示例程序。

### 第五步：配置环境

创建`.env`文件：

```bash
# Required
OPENAI_API_KEY=your_openai_key

# Required for LangSmith Deployments (cloud)
LANGSMITH_API_KEY=your_langsmith_key

# Optional - based on your tools
WEATHER_API_KEY=your_weather_key
COINGECKO_API_KEY=your_coingecko_key
ALCHEMY_API_KEY=your_alchemy_key
```

**获取LangSmith API密钥**：
1. 在https://smith.langchain.com创建账户。
2. 转到设置 → API密钥。
3. 创建新的API密钥。
4. 将密钥添加到`.env`文件中。

更新`langgraph.json`文件：

```json
{
  "agent_id": "[YOUR-AGENT-NAME]",
  "python_version": "3.11",  // or omit for TypeScript
  "dependencies": ["."],
  "graphs": {
    "agent": "./src/graph.ts"  // or .py
  },
  "env": ".env"
}
```

### 第六步：进行本地测试

```bash
# TypeScript
npm run dev

# Python
langgraph dev
```

测试您的代理程序的API接口：

```bash
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{"input": "test query"}'
```

## 部署选项

### 选项1：使用LangSmith进行部署（推荐）

**优点**：最快、最简单、基础设施由LangSmith管理
**要求**：需要LangSmith API密钥

**步骤**：

```bash
1. Push your agent repository to GitHub.
2. Create a new deployment in LangSmith Deployments.
3. Connect the repo, set environment variables, and deploy.
```

您的代理程序将获得：
- API端点URL
- 自动认证（使用您的LangSmith API密钥）
- 自动扩展和监控

**API调用时的认证**：
在调用部署的代理程序时，请包含您的LangSmith API密钥：

```bash
curl AGENT_URL/runs/wait \
  --request POST \
  --header 'Content-Type: application/json' \
  --header 'x-api-key: [YOUR-LANGSMITH-API-KEY]' \
  --data '{
    "assistant_id": "[YOUR-AGENT-ID]",
    "input": {
      "messages": [{"role": "user", "content": "test query"}]
    }
  }'
```

### 选项2：自托管基础设施

**优点**：对运行时环境有完全的控制权
**要求**：
- 需要Docker容器进行托管
- 提供API端点
- 需要SSL证书（HTTPS）
- 需要监控和日志记录

**基本的Docker配置**：

```dockerfile
FROM node:18
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 8000
CMD ["npm", "start"]
```

部署完成后，请记录以下信息：
- API URL：`https://your-domain.com/agent`
- API密钥：用于认证

## 在Warden Studio中注册

一旦您的代理程序通过HTTPS可访问，请在Warden Studio中注册它：

1. **提供API详细信息**：
   - API URL
   - API密钥
2. **添加元数据**：
   - 代理程序名称
   - 描述
   - 技能/功能列表
   - 头像图片

3. **发布**：您的代理程序将在Warden的Agent Hub中展示给数百万用户看到。

无需额外设置——您的代理程序现在已经可以通过API访问了！

**下一步（单独的技能）**：
如果用户请求在Warden Studio中发布代理程序或需要指导性步骤，请参阅OpenClaw技能**“在Warden Studio中部署代理程序”**：
https://www.clawhub.ai/Kryptopaid/warden-studio-deploy

## 最佳实践

### 1. 代理程序设计
- 学习Weather Agent的结构以了解工作模式。
- 对于复杂的工作流程，使用基于模式的推理（SGR）。
- 保持响应简洁且易于操作。
- 优雅地处理API错误。
- 验证所有输入数据。

### 2. API集成
- 使用环境变量存储API密钥。
- 实现速率限制。
- 在适当的情况下缓存响应。
- 记录错误以方便调试。
- 返回结构化的JSON响应。

### 3. 测试
- 在部署前进行本地测试。
- 验证所有API端点是否正常工作。
- 测试边缘情况和错误处理。
- 确保响应对用户友好。
- 验证是否符合Warden的要求。

### 4. 文档编写
- 编写清晰的README文件，内容包括：
  - 代理程序的目的和功能
  - 所需的API密钥
  - 设置说明
  - 示例查询方法
  - 已知的限制

## 常见模式

### 模式1：简单的数据获取程序
```typescript
// Fetch → Format → Respond
async function agent(input: string) {
  const data = await fetchAPI(input);
  const formatted = formatData(data);
  return generateResponse(formatted);
}
```

### 模式2：多步骤分析
```typescript
// Validate → Extract → Fetch → Analyze → Generate
async function agent(input: string) {
  const validated = await validateInput(input);
  const params = await extractParams(validated);
  const data = await fetchData(params);
  const analysis = await analyzeData(data);
  return generateReport(analysis);
}
```

### 模式3：比较分析
```typescript
// Parse → Fetch Multiple → Compare → Summarize
async function agent(input: string) {
  const items = await parseItems(input);
  const dataArray = await Promise.all(
    items.map(item => fetchData(item))
  );
  const comparison = compareData(dataArray);
  return generateComparison(comparison);
}
```

## 故障排除

### 常见问题

**“无法通过API访问代理程序”**
- 确认部署是否成功完成。
- 检查防火墙/安全组设置。
- 确保API端点可以公开访问。
- 使用curl或Postman进行测试。

**“构建过程中出现LangGraph错误”**
- 确认Node.js版本（18+）或Python版本（3.11+）。
- 检查所有依赖项是否已安装。
- 验证`langgraph.json`的语法是否正确。
- 查看部署控制台中的错误日志。

**“OpenAI API错误”**
- 确认API密钥是否有效。
- 检查是否超过了速率限制。
- 确保有足够的信用额度。
- 查看错误消息以获取详细信息。

**“代理程序响应速度慢”**
- 优化API调用（尽可能实现并行处理）。
- 对重复的查询实现缓存。
- 减少LLM（Large Language Model）的 token 使用量。
- 考虑升级基础设施。

## 激励计划提示

激励计划面向部署到Warden的OpenClaw代理程序。

1. **保持原创性**：创建全新的、尚未存在的代理程序。
   - 不要复制Weather Agent、CoinGecko Agent或Portfolio Agent。
   - 学习它们的模式，并将其应用于不同的问题。
2. **解决实际问题**：专注于实用且独特的功能。
   - Warden生态系统中存在哪些问题？
   - 用户真正需要什么？
3. **从简单开始**：最好先专注于做好一件事。
   - 不要试图一次性构建所有功能。
   - 简单、专注的代理程序往往更受欢迎。
4. **质量优先于功能**：可靠性比复杂性更重要。
   - 彻底测试。
   - 优雅地处理错误。
   - 提供清晰、有帮助的响应。
5. **仔细阅读文档**：编写清晰的README文件，包括代理程序的目的和功能、所需的API密钥、设置说明、示例查询方法以及已知的限制。

## 常见模式

### 模式1：简单的数据获取程序
```typescript
// Fetch → Format → Respond
async function agent(input: string) {
  const data = await fetchAPI(input);
  const formatted = formatData(data);
  return generateResponse(formatted);
}
```

### 模式2：多步骤分析
```typescript
// Validate → Extract → Fetch → Analyze → Generate
async function agent(input: string) {
  const validated = await validateInput(input);
  const params = await extractParams(validated);
  const data = await fetchData(params);
  const analysis = await analyzeData(data);
  return generateReport(analysis);
}
```

### 模式3：比较分析
```typescript
// Parse → Fetch Multiple → Compare → Summarize
async function agent(input: string) {
  const items = await parseItems(input);
  const dataArray = await Promise.all(
    items.map(item => fetchData(item))
  );
  const comparison = compareData(dataArray);
  return generateComparison(comparison);
}
```

## 故障排除

### 常见问题

**“无法通过API访问代理程序”**
- 确认部署是否成功完成。
- 检查防火墙/安全组设置。
- 确保API端点可以公开访问。
- 使用curl或Postman进行测试。

**“构建过程中出现LangGraph错误”**
- 确认Node.js版本（18+）或Python版本（3.11+）。
- 检查所有依赖项是否已安装。
- 验证`langgraph.json`的语法是否正确。
- 查看部署控制台中的错误日志。

**“OpenAI API错误”**
- 确认API密钥是否有效。
- 检查是否超过了速率限制。
- 确保有足够的信用额度。
- 查看错误消息以获取详细信息。

**“代理程序响应速度慢”**
- 优化API调用（尽可能实现并行处理）。
- 对重复的查询实现缓存。
- 减少LLM token的使用量。
- 考虑升级基础设施。

## 激励计划提示

激励计划面向部署到Warden的OpenClaw代理程序。

1. **保持原创性**：创建全新的、尚未存在的代理程序。
   - 不要复制Weather Agent、CoinGecko Agent或Portfolio Agent。
   - 学习它们的模式，并将其应用于不同的问题。
2. **解决实际问题**：专注于实用且独特的功能。
   - Warden生态系统中存在哪些问题？
   - 用户真正需要什么？
3. **从简单开始**：最好先专注于做好一件事。
   - 不要试图一次性构建所有功能。
   - 简单、专注的代理程序往往更受欢迎。
4. **质量优先于功能**：可靠性比复杂性更重要。
   - 彻底测试。
   - 优雅地处理错误。
   - 提供清晰、有帮助的响应。
5. **仔细阅读文档**：编写清晰的README文件，包括代理程序的目的和功能、所需的API密钥、设置说明以及示例查询方法。

## 示例代理程序创意（请尝试构建这些！）

这些是Warden生态系统中还不存在的新代理程序创意。尝试构建其中一个（或创建您自己的独特创意）：

**Web3应用场景**：
- 气体价格优化器（预测最佳交易时机）
- NFT稀有性分析器（评估NFT的特性和稀有性评分）
- DeFi收益比较器（比较不同协议的收益）
- 钱包健康检查器（分析钱包的安全性和多样性）
- 交易解释器（解码并解释复杂的交易）
- 代币价格提醒器（自定义价格变动通知）
- 智能合约审计器（基本的安全性检查）
- 流动性池查找器（寻找最佳的跨链桥接服务）
- Airdrop跟踪器（查找并跟踪Airdrop资格）

**通用应用场景**：
- 加密新闻聚合器（过滤和总结加密新闻）
- 研究助手（收集和分析加密相关的研究资料）
- 监管跟踪器（按地区跟踪加密法规）
- 数据可视化工具（从链上数据生成图表）
- API编排器（整合多个加密数据源）
- 工作流程自动化工具（自动化常见的加密任务）

**记住**：这些只是新代理程序的创意。请研究示例程序（Weather Agent、CoinGecko Agent、Portfolio Agent）以了解工作模式，然后根据这些创意构建新的代理程序或开发您自己的独特概念。

## 其他资源

**文档**：
- LangGraph TypeScript指南：`community-agents/docs/langgraph-quick-start-ts.md`
- LangGraph Python指南：`community-agents/docs/langgraph-quick-start-py.md`
- 部署指南：`community-agents/docs/deploy.md`

**示例代理程序**：
- Weather Agent的README文件：`agents/weather-agent/README.md`
- CoinGecko Agent的README文件：`agents/coingecko-agent/README.md`
- Portfolio Agent的README文件：`agents/portfolio-agent/README.md`

**支持**：
- Discord：#developers频道
- GitHub问题反馈：https://github.com/warden-protocol/community-agents/issues
- 文档：https://docs.wardenprotocol.org

## 快速参考命令

```bash
# Study example agents (DON'T BUILD THESE)
git clone https://github.com/warden-protocol/community-agents.git
cd community-agents/agents/weather-agent  # Study the code
cd community-agents/agents/coingecko-agent  # Study the patterns

# Create YOUR new agent
python scripts/init-agent.py my-unique-agent \
  --template typescript \
  --description "YOUR unique agent description"

# Install dependencies (TypeScript)
npm install

# Install dependencies (Python)
pip install -r requirements.txt

# Test locally
npm run dev  # or: langgraph dev

# Deploy (LangSmith Deployments)
# Use the LangSmith Deployments UI after pushing to GitHub

# Build Docker image (for self-hosting)
docker build -t my-warden-agent .

# Run Docker container
docker run -p 8000:8000 my-warden-agent
```

## 成功提交前的检查清单

- [ ] 代理程序使用LangGraph构建完成。
- [ ] API可访问且已通过测试。
- [ ] 每个LangGraph实例只运行一个代理程序。
- [ ] 不允许访问用户钱包或存储数据（第一阶段）。
- [ ] README文件中有清晰的文档。
- [ ] 环境变量配置正确。
- [ ] 已实现错误处理。
- [ ] 使用多种输入进行了测试。
- [ ] 功能独特且实用。
- [ ] 准备好在Warden Studio中注册。