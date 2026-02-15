---
name: ydc-claude-agent-sdk-integration
description: 将 Claude Agent SDK 与 You.com 的 HTTP MCP 服务器集成，适用于 Python 和 TypeScript 开发环境。当开发者提到 Claude Agent SDK、Anthropic Agent SDK 或将 Claude 与 MCP 工具集成时，请参考此文档。
license: MIT
compatibility: Python 3.10+ or TypeScript 5.2+ (for v2), Node.js 18+
metadata:
  author: youdotcom-oss
  category: sdk-integration
  version: "1.0.0"
  keywords: claude,anthropic,claude-agent-sdk,agent-sdk,mcp,you.com,integration,http-mcp,web-search,python,typescript
---

# 将 Claude Agent SDK 与 You.com MCP 集成

本文档提供了将 Claude Agent SDK 与 You.com 的 HTTP MCP 服务器集成的交互式工作流程。

## 工作流程

1. **询问：语言选择**
   * 选择 Python 还是 TypeScript？

2. **如果选择 TypeScript - 询问：SDK 版本**
   * v1（稳定版，基于生成器）还是 v2（预览版，支持发送/接收请求模式）？
   * 注意：v2 版本需要 TypeScript 5.2 或更高版本才能使用 `await` 语法。

3. **安装包**
   * Python：`pip install claude-agent-sdk`
   * TypeScript：`npm install @anthropic-ai/claude-agent-sdk`

4. **询问：环境变量**
   * 是否使用标准的 `YDC_API_KEY` 和 `ANTHROPIC_API_KEY`？
   * 或者使用自定义名称？
   * 如果尚未设置环境变量，请参考以下链接获取 API 密钥：
     - YDC_API_KEY：https://you.com/platform/api-keys
     - ANTHROPIC_API_KEY：https://console.anthropic.com/settings/keys

5. **询问：文件位置**
   * 如果是新建文件，询问文件的位置和名称；
   * 如果是现有文件，询问需要将哪些配置添加到现有文件中。

6. **创建/更新文件**

   **对于新建文件：**
   * 使用下方“完整模板”部分提供的完整代码模板。
   * 用户可以立即使用已设置的 API 密钥运行程序。

   **对于现有文件：**
   * 将 HTTP MCP 服务器的配置添加到现有代码中。
   * Python 配置示例：
     ```python
     from claude_agent_sdk import query, ClaudeAgentOptions

     options = ClaudeAgentOptions(
         mcp_servers={
             "ydc": {
                 "type": "http",
                 "url": "https://api.you.com/mcp",
                 "headers": {
                     "Authorization": f"Bearer {os.getenv('YDC_API_KEY')}"
                 }
             }
         },
         allowed_tools=[
             "mcp__ydc__you_search",
             "mcp__ydc__you_express",
             "mcp__ydc__you_contents"
         ]
     )
     ```

   * TypeScript 配置示例：
     ```typescript
     const options = {
       mcpServers: {
         ydc: {
           type: 'http' as const,
           url: 'https://api.you.com/mcp',
           headers: {
             Authorization: `Bearer ${process.env.YDC_API_KEY}`
           }
         }
       },
       allowedTools: [
         'mcp__ydc__you_search',
         'mcp__ydc__you_express',
         'mcp__ydc__you_contents'
       ]
     };
     ```

## 完整模板

使用这些完整模板来创建新文件。每个模板都已准备好使用您的 API 密钥进行运行。

### Python 模板（完整示例）

```python
"""
Claude Agent SDK with You.com HTTP MCP Server
Python implementation with async/await pattern
"""

import os
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

# Validate environment variables
ydc_api_key = os.getenv("YDC_API_KEY")
anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")

if not ydc_api_key:
    raise ValueError(
        "YDC_API_KEY environment variable is required. "
        "Get your key at: https://you.com/platform/api-keys"
    )

if not anthropic_api_key:
    raise ValueError(
        "ANTHROPIC_API_KEY environment variable is required. "
        "Get your key at: https://console.anthropic.com/settings/keys"
    )


async def main():
    """
    Example: Search for AI news and get results from You.com MCP server
    """
    # Configure Claude Agent with HTTP MCP server
    options = ClaudeAgentOptions(
        mcp_servers={
            "ydc": {
                "type": "http",
                "url": "https://api.you.com/mcp",
                "headers": {"Authorization": f"Bearer {ydc_api_key}"},
            }
        },
        allowed_tools=[
            "mcp__ydc__you_search",
            "mcp__ydc__you_express",
            "mcp__ydc__you_contents",
        ],
        model="claude-sonnet-4-5-20250929",
    )

    # Query Claude with MCP tools available
    async for message in query(
        prompt="Search for the latest AI news from this week",
        options=options,
    ):
        # Handle different message types
        if message.type == "text":
            print(message.content)
        elif message.type == "tool_use":
            print(f"\n[Tool: {message.name}]")
            print(f"Input: {message.input}")
        elif message.type == "tool_result":
            print(f"Result: {message.content}")


if __name__ == "__main__":
    asyncio.run(main())
```

### TypeScript v1 模板（完整示例）

```typescript
/**
 * Claude Agent SDK with You.com HTTP MCP Server
 * TypeScript v1 implementation with generator-based pattern
 */

import { query } from '@anthropic-ai/claude-agent-sdk';

// Validate environment variables
const ydcApiKey = process.env.YDC_API_KEY;
const anthropicApiKey = process.env.ANTHROPIC_API_KEY;

if (!ydcApiKey) {
  throw new Error(
    'YDC_API_KEY environment variable is required. ' +
      'Get your key at: https://you.com/platform/api-keys'
  );
}

if (!anthropicApiKey) {
  throw new Error(
    'ANTHROPIC_API_KEY environment variable is required. ' +
      'Get your key at: https://console.anthropic.com/settings/keys'
  );
}

/**
 * Example: Search for AI news and get results from You.com MCP server
 */
async function main() {
  // Query Claude with HTTP MCP configuration
  const result = query({
    prompt: 'Search for the latest AI news from this week',
    options: {
      mcpServers: {
        ydc: {
          type: 'http' as const,
          url: 'https://api.you.com/mcp',
          headers: {
            Authorization: `Bearer ${ydcApiKey}`,
          },
        },
      },
      allowedTools: [
        'mcp__ydc__you_search',
        'mcp__ydc__you_express',
        'mcp__ydc__you_contents',
      ],
      model: 'claude-sonnet-4-5-20250929',
    },
  });

  // Process messages as they arrive
  for await (const msg of result) {
    if (msg.type === 'text') {
      console.log(msg.content);
    } else if (msg.type === 'tool_use') {
      console.log(`\n[Tool: ${msg.name}]`);
      console.log(`Input: ${JSON.stringify(msg.input, null, 2)}`);
    } else if (msg.type === 'tool_result') {
      console.log(`Result: ${msg.content}`);
    }
  }
}

main().catch(console.error);
```

### TypeScript v2 模板（完整示例）

```typescript
/**
 * Claude Agent SDK with You.com HTTP MCP Server
 * TypeScript v2 implementation with send/receive pattern
 * Requires TypeScript 5.2+ for 'await using' support
 */

import { unstable_v2_createSession } from '@anthropic-ai/claude-agent-sdk';

// Validate environment variables
const ydcApiKey = process.env.YDC_API_KEY;
const anthropicApiKey = process.env.ANTHROPIC_API_KEY;

if (!ydcApiKey) {
  throw new Error(
    'YDC_API_KEY environment variable is required. ' +
      'Get your key at: https://you.com/platform/api-keys'
  );
}

if (!anthropicApiKey) {
  throw new Error(
    'ANTHROPIC_API_KEY environment variable is required. ' +
      'Get your key at: https://console.anthropic.com/settings/keys'
  );
}

/**
 * Example: Search for AI news and get results from You.com MCP server
 */
async function main() {
  // Create session with HTTP MCP configuration
  // 'await using' ensures automatic cleanup when scope exits
  await using session = unstable_v2_createSession({
    mcpServers: {
      ydc: {
        type: 'http' as const,
        url: 'https://api.you.com/mcp',
        headers: {
          Authorization: `Bearer ${ydcApiKey}`,
        },
      },
    },
    allowedTools: [
      'mcp__ydc__you_search',
      'mcp__ydc__you_express',
      'mcp__ydc__you_contents',
    ],
    model: 'claude-sonnet-4-5-20250929',
  });

  // Send message to Claude
  await session.send('Search for the latest AI news from this week');

  // Receive and process messages
  for await (const msg of session.receive()) {
    if (msg.type === 'text') {
      console.log(msg.content);
    } else if (msg.type === 'tool_use') {
      console.log(`\n[Tool: ${msg.name}]`);
      console.log(`Input: ${JSON.stringify(msg.input, null, 2)}`);
    } else if (msg.type === 'tool_result') {
      console.log(`Result: ${msg.content}`);
    }
  }
}

main().catch(console.error);
```

## HTTP MCP 服务器配置

所有模板均基于 You.com 的 **HTTP MCP 服务器** 进行配置：

**Python：**
```python
mcp_servers={
    "ydc": {
        "type": "http",
        "url": "https://api.you.com/mcp",
        "headers": {
            "Authorization": f"Bearer {ydc_api_key}"
        }
    }
}
```

**TypeScript：**
```typescript
mcpServers: {
  ydc: {
    type: 'http' as const,
    url: 'https://api.you.com/mcp',
    headers: {
      Authorization: `Bearer ${ydcApiKey}`
    }
  }
}
```

**HTTP MCP 的优势：**
- ✅ 无需本地安装
- ✅ 无状态请求/响应模型
- ✅ 始终使用最新版本
- ✅ 在所有环境中保持一致性
- ✅ 适合生产环境且可扩展
- ✅ 与现有的 HTTP 基础设施兼容

## 可用的 You.com 工具

配置完成后，Claude 可以使用以下工具：
- `mcp__ydc__you_search` - 网页和新闻搜索
- `mcp__ydc__you_express` - 基于 AI 的回答（包含网页上下文）
- `mcp__ydc__you_contents` - 网页内容提取

## 环境变量

需要设置以下两个 API 密钥：

```bash
# Add to your .env file or shell profile
export YDC_API_KEY="your-you-api-key-here"
export ANTHROPIC_API_KEY="your-anthropic-api-key-here"
```

**获取 API 密钥：**
- You.com：https://you.com/platform/api-keys
- Anthropic：https://console.anthropic.com/settings/keys

## 验证清单

在完成集成之前，请确保：
- [ ] 已安装 `claude-agent-sdk`（Python）或 `@anthropic-ai/claude-agent-sdk`（TypeScript）
- [ ] 已设置 `YDC_API_KEY` 和 `ANTHROPIC_API_KEY`
- [ ] 已将模板复制到文件中或已向现有文件中添加配置
- [ ] 已配置 HTTP MCP 服务器（地址：`https://api.you.com/mcp`）
- [ ] 请求头中的 `Authorization` 字段包含 `Bearer ${YDC_API_KEY}`
- [ ] 允许使用的工具列表中包含 You.com 提供的工具
- [ ] 文件可执行（Python）或可编译（TypeScript）
- [ ] 可以使用示例查询进行测试

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

<details>
<summary><strong>无法找到模块 @anthropic-ai/claude-agent-sdk</strong></summary>

请安装相应的包：
```bash
# NPM
npm install @anthropic-ai/claude-agent-sdk

# Bun
bun add @anthropic-ai/claude-agent-sdk

# Yarn
yarn add @anthropic-ai/claude-agent-sdk

# pnpm
pnpm add @anthropic-ai/claude-agent-sdk
```

</details>

<details>
<summary><strong>需要设置 YDC_API_KEY 环境变量</strong></summary>

请设置您的 You.com API 密钥：
```bash
export YDC_API_KEY="your-api-key-here"
```

您可以在以下链接获取 API 密钥：https://you.com/platform/api-keys

</details>

<details>
<summary><strong>需要设置 ANTHROPIC_API_KEY 环境变量</strong></summary>

请设置您的 Anthropic API 密钥：
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

您可以在以下链接获取 API 密钥：https://console.anthropic.com/settings/keys

</details>

<details>
<summary><strong>连接 HTTP MCP 服务器时出现 401 Unauthorized 错误</strong></summary>

请检查：
1. 确保 `YDC_API_KEY` 是有效的。
2. 确保环境变量中没有多余的空格或引号。
3. 确保 `Authorization` 头部的格式正确：`Bearer ${YDC_API_KEY}`

</details>

<details>
<summary>某些工具无法使用或未被调用</summary>

请确保 `allowedTools` 列表中包含正确的工具名称：
- `mcp__ydc__you_search`（而非 `you_search`）
- `mcp__ydc__you_express`（而非 `you_express`）
- `mcp__ydc__you_contents`（而非 `you_contents`）
工具名称必须以 `mcp__ydc__` 为前缀。

</details>

<details>
<summary>TypeScript 错误：无法使用 `await using` 语法</summary>

v2 版本的 SDK 需要 TypeScript 5.2 或更高版本才能支持 `await using` 语法。

**解决方案 1：更新 TypeScript 版本**
```bash
npm install -D typescript@latest
```

**解决方案 2：手动清理项目文件**
```typescript
const session = unstable_v2_createSession({ /* options */ });
try {
  await session.send('Your query');
  for await (const msg of session.receive()) {
    // Process messages
  }
} finally {
  session.close();
}
```

**解决方案 3：改用 v1 版本的 SDK**
在设置过程中选择 v1 版本以获得更好的 TypeScript 兼容性。

</details>

## 额外资源

- You.com MCP 服务器：https://documentation.you.com/developer-resources/mcp-server
- Claude Agent SDK（Python）：https://platform.claude.com/docs/en/agent-sdk/python
- Claude Agent SDK（TypeScript v1）：https://platform.claude.com/docs/en/agent-sdk/typescript
- Claude Agent SDK（TypeScript v2）：https://platform.claude.com/docs/en/agent-sdk/typescript-v2-preview
- API 密钥：
  - You.com：https://you.com/platform/api-keys
  - Anthropic：https://console.anthropic.com/settings/keys