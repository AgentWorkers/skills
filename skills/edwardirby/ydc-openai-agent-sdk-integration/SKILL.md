---
name: ydc-openai-agent-sdk-integration
description: 将 OpenAI Agents SDK 与 You.com MCP 服务器集成——支持 Python 和 TypeScript 的托管及流式传输功能。当开发者提到 OpenAI Agents SDK、OpenAI 代理或将 OpenAI 与 MCP 集成时，请参考此文档。
license: MIT
compatibility: Python 3.10+ or Node.js 18+ with TypeScript
metadata:
  author: youdotcom-oss
  category: sdk-integration
  version: "1.0.0"
  keywords: openai,openai-agents,agent-sdk,mcp,you.com,integration,hosted-mcp,streamable-http,web-search,python,typescript
---

# 将 OpenAI Agents SDK 集成到 You.com 的 MCP 中

本文档提供了将 OpenAI Agents SDK 与 You.com 的 MCP 服务器集成的交互式工作流程。

## 工作流程

1. **选择编程语言：** Python 还是 TypeScript？

2. **选择 MCP 配置类型：**
   - **托管型 MCP**（由 OpenAI 管理，提供服务器地址）：推荐使用，配置简单。
   - **可流式 HTTP**（自定义基础设施）：适用于需要自定义网络配置的场景。

3. **安装相关包：**
   - Python：`pip install openai-agents`
   - TypeScript：`npm install @openai/agents`

4. **设置环境变量：**
   - 两种配置类型都需要以下环境变量：
     - `YDC_API_KEY`（用于生成 bearer token 的 You.com API 密钥）
     - `OPENAI_API_KEY`（OpenAI API 密钥）

   - 确保这些密钥已经设置。如果尚未设置，请参考以下链接获取：
     - `YDC_API_KEY`：https://you.com/platform/api-keys
     - `OPENAI_API_KEY`：https://platform.openai.com/api-keys

5. **确定文件位置：**
   - 如果需要创建新文件，请指定文件的位置和名称。
   - 如果使用现有文件，请指定要添加 MCP 配置的文件。

6. **创建/更新文件：**
   - **对于新文件：** 使用下方提供的完整模板代码，并替换为你的 API 密钥即可运行。
   - **对于现有文件：** 将 MCP 配置添加到现有代码中。

### 托管型 MCP 配置示例（Python）：
```python
   from agents import Agent, Runner
   from agents.mcp import HostedMCPTool

   # Validate: ydc_api_key = os.getenv("YDC_API_KEY")
   agent = Agent(
       name="Assistant",
       instructions="Use You.com tools to answer questions.",
       tools=[
           HostedMCPTool(
               tool_config={
                   "type": "mcp",
                   "server_label": "ydc",
                   "server_url": "https://api.you.com/mcp",
                   "headers": {
                       "Authorization": f"Bearer {ydc_api_key}"
                   },
                   "require_approval": "never",
               }
           )
       ],
   )
   ```

### 托管型 MCP 配置示例（TypeScript）：
```typescript
   import { Agent, hostedMcpTool } from '@openai/agents';

   // Validate: const ydcApiKey = process.env.YDC_API_KEY;
   const agent = new Agent({
     name: 'Assistant',
     instructions: 'Use You.com tools to answer questions.',
     tools: [
       hostedMcpTool({
        serverLabel: 'ydc',
         serverUrl: 'https://api.you.com/mcp',
         headers: {
           Authorization: `Bearer ${ydcApiKey}`,
         },
       }),
     ],
   });
   ```

### 可流式 HTTP 配置示例（Python）：
```python
   from agents import Agent, Runner
   from agents.mcp import MCPServerStreamableHttp

   # Validate: ydc_api_key = os.getenv("YDC_API_KEY")
   async with MCPServerStreamableHttp(
       name="You.com MCP Server",
       params={
           "url": "https://api.you.com/mcp",
           "headers": {"Authorization": f"Bearer {ydc_api_key}"},
           "timeout": 10,
       },
       cache_tools_list=True,
       max_retry_attempts=3,
   ) as server:
       agent = Agent(
           name="Assistant",
           instructions="Use You.com tools to answer questions.",
           mcp_servers=[server],
       )
   ```

### 可流式 HTTP 配置示例（TypeScript）：
```typescript
   import { Agent, MCPServerStreamableHttp } from '@openai/agents';

   // Validate: const ydcApiKey = process.env.YDC_API_KEY;
   const mcpServer = new MCPServerStreamableHttp({
     url: 'https://api.you.com/mcp',
     name: 'You.com MCP Server',
     requestInit: {
       headers: {
         Authorization: `Bearer ${ydcApiKey}`,
       },
     },
   });

   const agent = new Agent({
     name: 'Assistant',
     instructions: 'Use You.com tools to answer questions.',
     mcpServers: [mcpServer],
   });
   ```

## 完整模板

使用这些模板来创建新文件。每个模板都已准备好，只需替换为你的 API 密钥即可运行。

### Python 托管型 MCP 模板（完整示例）：
```python
"""
OpenAI Agents SDK with You.com Hosted MCP
Python implementation with OpenAI-managed infrastructure
"""

import os
import asyncio
from agents import Agent, Runner
from agents.mcp import HostedMCPTool

# Validate environment variables
ydc_api_key = os.getenv("YDC_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not ydc_api_key:
    raise ValueError(
        "YDC_API_KEY environment variable is required. "
        "Get your key at: https://you.com/platform/api-keys"
    )

if not openai_api_key:
    raise ValueError(
        "OPENAI_API_KEY environment variable is required. "
        "Get your key at: https://platform.openai.com/api-keys"
    )


async def main():
    """
    Example: Search for AI news using You.com hosted MCP tools
    """
    # Configure agent with hosted MCP tools
    agent = Agent(
        name="AI News Assistant",
        instructions="Use You.com tools to search for and answer questions about AI news.",
        tools=[
            HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "ydc",
                    "server_url": "https://api.you.com/mcp",
                    "headers": {
                        "Authorization": f"Bearer {ydc_api_key}"
                    },
                    "require_approval": "never",
                }
            )
        ],
    )

    # Run agent with user query
    result = await Runner.run(
        agent,
        "Search for the latest AI news from this week"
    )

    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
```

### Python 可流式 HTTP 模板（完整示例）：
```python
"""
OpenAI Agents SDK with You.com Streamable HTTP MCP
Python implementation with self-managed connection
"""

import os
import asyncio
from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp

# Validate environment variables
ydc_api_key = os.getenv("YDC_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

if not ydc_api_key:
    raise ValueError(
        "YDC_API_KEY environment variable is required. "
        "Get your key at: https://you.com/platform/api-keys"
    )

if not openai_api_key:
    raise ValueError(
        "OPENAI_API_KEY environment variable is required. "
        "Get your key at: https://platform.openai.com/api-keys"
    )


async def main():
    """
    Example: Search for AI news using You.com streamable HTTP MCP server
    """
    # Configure streamable HTTP MCP server
    async with MCPServerStreamableHttp(
        name="You.com MCP Server",
        params={
            "url": "https://api.you.com/mcp",
            "headers": {"Authorization": f"Bearer {ydc_api_key}"},
            "timeout": 10,
        },
        cache_tools_list=True,
        max_retry_attempts=3,
    ) as server:
        # Configure agent with MCP server
        agent = Agent(
            name="AI News Assistant",
            instructions="Use You.com tools to search for and answer questions about AI news.",
            mcp_servers=[server],
        )

        # Run agent with user query
        result = await Runner.run(
            agent,
            "Search for the latest AI news from this week"
        )

        print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
```

### TypeScript 托管型 MCP 模板（完整示例）：
```typescript
/**
 * OpenAI Agents SDK with You.com Hosted MCP
 * TypeScript implementation with OpenAI-managed infrastructure
 */

import { Agent, run, hostedMcpTool } from '@openai/agents';

// Validate environment variables
const ydcApiKey = process.env.YDC_API_KEY;
const openaiApiKey = process.env.OPENAI_API_KEY;

if (!ydcApiKey) {
  throw new Error(
    'YDC_API_KEY environment variable is required. ' +
      'Get your key at: https://you.com/platform/api-keys'
  );
}

if (!openaiApiKey) {
  throw new Error(
    'OPENAI_API_KEY environment variable is required. ' +
      'Get your key at: https://platform.openai.com/api-keys'
  );
}

/**
 * Example: Search for AI news using You.com hosted MCP tools
 */
async function main() {
  // Configure agent with hosted MCP tools
  const agent = new Agent({
    name: 'AI News Assistant',
    instructions:
      'Use You.com tools to search for and answer questions about AI news.',
    tools: [
      hostedMcpTool({
        serverLabel: 'ydc',
        serverUrl: 'https://api.you.com/mcp',
        headers: {
          Authorization: `Bearer ${ydcApiKey}`,
        },
      }),
    ],
  });

  // Run agent with user query
  const result = await run(
    agent,
    'Search for the latest AI news from this week'
  );

  console.log(result.finalOutput);
}

main().catch(console.error);
```

### TypeScript 可流式 HTTP 模板（完整示例）：
```typescript
/**
 * OpenAI Agents SDK with You.com Streamable HTTP MCP
 * TypeScript implementation with self-managed connection
 */

import { Agent, run, MCPServerStreamableHttp } from '@openai/agents';

// Validate environment variables
const ydcApiKey = process.env.YDC_API_KEY;
const openaiApiKey = process.env.OPENAI_API_KEY;

if (!ydcApiKey) {
  throw new Error(
    'YDC_API_KEY environment variable is required. ' +
      'Get your key at: https://you.com/platform/api-keys'
  );
}

if (!openaiApiKey) {
  throw new Error(
    'OPENAI_API_KEY environment variable is required. ' +
      'Get your key at: https://platform.openai.com/api-keys'
  );
}

/**
 * Example: Search for AI news using You.com streamable HTTP MCP server
 */
async function main() {
  // Configure streamable HTTP MCP server
  const mcpServer = new MCPServerStreamableHttp({
    url: 'https://api.you.com/mcp',
    name: 'You.com MCP Server',
    requestInit: {
      headers: {
        Authorization: `Bearer ${ydcApiKey}`,
      },
    },
  });

  try {
    // Connect to MCP server
    await mcpServer.connect();

    // Configure agent with MCP server
    const agent = new Agent({
      name: 'AI News Assistant',
      instructions:
        'Use You.com tools to search for and answer questions about AI news.',
      mcpServers: [mcpServer],
    });

    // Run agent with user query
    const result = await run(
      agent,
      'Search for the latest AI news from this week'
    );

    console.log(result.finalOutput);
  } finally {
    // Clean up connection
    await mcpServer.close();
  }
}

main().catch(console.error);
```

## MCP 配置类型

### 托管型 MCP（推荐）

**特点：** OpenAI 负责管理 MCP 连接和工具路由。

**优势：**
- ✅ 配置简单（无需处理连接细节）
- ✅ OpenAI 负责身份验证和重试机制
- ✅ 低延迟（工具在 OpenAI 的基础设施上运行）
- ✅ 工具会自动被发现和列出
- ✅ 无需管理异步上下文或进行资源清理

**适用场景：**
- 构建生产级应用程序
- 需要最少的样板代码
- 需要可靠的工具执行
- 不需要自定义传输层

**配置方式：**
（具体配置代码见上述模板）

### 可流式 HTTP MCP

**特点：** 你需要自己管理 MCP 连接和传输层。

**优势：**
- ✅ 对网络连接有完全的控制权
- 可以自定义基础设施
- 可以添加自定义头部、超时设置和重试逻辑
- 可以在自己的环境中运行 MCP 服务器
- 更适合测试和开发场景

**配置方式：**
（具体配置代码见上述模板）

## You.com 提供的工具

配置完成后，你可以使用以下工具：
- `mcp__ydc__you_search` - 进行网页和新闻搜索
- `mcp__ydc__you_express` - 提供带有网页上下文的人工智能回答
- `mcp__ydc__you_contents` - 提取网页内容

## 环境变量

两种配置类型都需要以下 API 密钥：
```bash
# Add to your .env file or shell profile
export YDC_API_KEY="your-you-api-key-here"
export OPENAI_API_KEY="your-openai-api-key-here"
```

**获取 API 密钥：**
- You.com：https://you.com/platform/api-keys
- OpenAI：https://platform.openai.com/api-keys

## 验证步骤

在完成配置之前，请确保：
- 已安装 `openai-agents`（Python）或 `@openai/agents`（TypeScript）包。
- 已设置 `YDC_API_KEY` 和 `OPENAI_API_KEY` 环境变量。
- 模板已复制或配置已添加到现有文件中。
- 选择了正确的 MCP 配置类型（托管型或可流式 HTTP）。
- 使用正确的身份验证头（Bearer token）。
- 文件可执行（Python）或可编译（TypeScript）。
- 准备使用示例查询进行测试。

## 测试集成

**Python：**
```bash
python your-file.py
```

**TypeScript：**
```bash
# With tsx (recommended for quick testing)
npx tsx your-file.ts

# Or compile and run
tsc your-file.ts && node your-file.js
```

## 常见问题

- **错误提示：** “无法找到模块 @openai/agents”
  请安装 `openai-agents` 包。

**解决方案：**
```bash
# NPM
npm install @openai/agents

# Bun
bun add @openai/agents

# Yarn
yarn add @openai/agents

# pnpm
pnpm add @openai/agents
```

- **错误提示：** “需要设置 YDC_API_KEY 环境变量**
  请确保已设置 You.com 的 API 密钥。

**解决方案：**
```bash
export YDC_API_KEY="your-api-key-here"
```

- **错误提示：** “需要设置 OPENAI_API_KEY 环境变量**
  请确保已设置 OpenAI 的 API 密钥。

**解决方案：**
```bash
export OPENAI_API_KEY="your-api-key-here"
```

- **错误提示：** “MCP 连接失败（401 Unauthorized）**
  请检查：
  1. 确保 `YDC_API_KEY` 有效。
  2. 确保环境变量中没有多余的空格或引号。
  3. 确认身份验证头的格式为 `Bearer ${YDC_API_KEY}`。

- **工具无法使用或未被调用**
  **通用提示：**
  - 确保 `server_url` 的值为 `https://api.you.com/mcp`。
  - 确认身份验证头中包含 `Bearer` 前缀。
  - 确保 `require_approval` 的值为 `"never"` 以启用自动执行。

- **针对可流式 HTTP：**
  - 在创建代理之前，请确保 MCP 服务器已连接成功。
  - 在运行代理之前，请确认连接正常。

- **连接超时或网络错误**
  **针对可流式 HTTP：**
    - 增加超时时间或重试次数。

## 额外资源

- **OpenAI Agents SDK（Python）：** https://openai.github.io/openai-agents-python/
- **OpenAI Agents SDK（TypeScript）：** https://openai.github.io/openai-agents-js/
- **MCP 配置（Python）：** https://openai.github.io/openai-agents-python/mcp/
- **MCP 配置（TypeScript）：** https://openai.github.io/openai-agents-js/guides/mcp/
- **You.com MCP 服务器：** https://documentation.you.com/developer-resources/mcp-server
- **API 密钥：**
  - You.com：https://you.com/platform/api-keys
  - OpenAI：https://platform.openai.com/api-keys