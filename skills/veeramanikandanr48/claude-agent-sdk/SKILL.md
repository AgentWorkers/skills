---
name: claude-agent-sdk
description: |
  Build autonomous AI agents with Claude Agent SDK. Structured outputs guarantee JSON schema validation, with plugins system and hooks for event-driven workflows. Prevents 14 documented errors.

  Use when: building coding agents, SRE systems, security auditors, or troubleshooting CLI not found, structured output validation, session forking errors, MCP config issues, subagent cleanup.
user-invocable: true
---

# Claude Agent SDK - 结构化输出与错误预防指南

**包**: @anthropic-ai/claude-agent-sdk@0.2.12  
**重大变更**:  
- v0.1.45：引入结构化输出功能（2025年11月）  
- v0.1.0：移除默认系统提示，强制设置数据来源  

---

## v0.1.45及更高版本（2025年11月）的新特性  

**主要功能：**  

### 1. 结构化输出（v0.1.45，2025年11月14日）  
- **JSON模式验证**：确保响应数据符合预设模式。  
- **`outputFormat`参数**：允许使用JSON模式或Zod模式定义输出格式。  
- **访问验证后的结果**：通过`message.structured_output`获取。  
- **必需的Beta头部信息**：`structured-outputs-2025-11-13`。  
- **类型安全**：支持Zod模式的类型推断。  

**示例：**  
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";
import { zodToJsonSchema } from "zod-to-json-schema";

const schema = z.object({
  summary: z.string(),
  sentiment: z.enum(['positive', 'neutral', 'negative']),
  confidence: z.number().min(0).max(1)
});

const response = query({
  prompt: "Analyze this code review feedback",
  options: {
    model: "claude-sonnet-4-5",
    outputFormat: {
      type: "json_schema",
      json_schema: {
        name: "AnalysisResult",
        strict: true,
        schema: zodToJsonSchema(schema)
      }
    }
  }
});

for await (const message of response) {
  if (message.type === 'result' && message.structured_output) {
    // Guaranteed to match schema
    const validated = schema.parse(message.structured_output);
    console.log(`Sentiment: ${validated.sentiment}`);
  }
}
```  

**Zod兼容性（v0.1.71及更高版本）：**  
SDK同时支持Zod v3.24.1及以上版本和Zod v4.0.0及以上版本。无论使用哪个版本，导入方式均为`import { z } from "zod"`。  

### 2. 插件系统（v0.1.27）  
- **`plugins`数组**：用于加载本地插件路径。  
- **支持自定义插件**：扩展代理的功能。  

### 3. 钩子系统（v0.1.0及更高版本）  
**所有12个钩子事件：**  
| 钩子 | 触发时机 | 用途 |  
|------|------------|----------|  
| `PreToolUse` | 工具执行前 | 验证、修改或阻止工具调用。  
| `PostToolUse` | 工具执行后 | 记录结果、触发副作用。  
| `Notification` | 代理通知 | 显示状态更新。  
| `UserPromptSubmit` | 收到用户提示时 | 预处理或验证输入。  
| `SubagentStart` | 子代理启动时 | 跟踪代理分配情况、记录上下文。  
| `SubagentStop` | 子代理停止时 | 整合结果、进行清理。  
| `PreCompact` | 数据压缩前 | 在数据截断前保存状态。  
| `PermissionRequest` | 需要权限时 | 实现自定义审批流程。  
| `Stop` | 代理停止时 | 进行清理、最终日志记录。  
| `SessionStart` | 会话开始时 | 初始化状态。  
| `SessionEnd` | 会话结束时 | 保存状态、进行清理。  
| `Error` | 发生错误时 | 实现自定义错误处理。  

**钩子配置：**  
```typescript
const response = query({
  prompt: "...",
  options: {
    hooks: {
      PreToolUse: async (input) => {
        console.log(`Tool: ${input.toolName}`);
        return { allow: true };  // or { allow: false, message: "..." }
      },
      PostToolUse: async (input) => {
        await logToolUsage(input.toolName, input.result);
      }
    }
  }
});
```  

### 4. 其他选项  
- **`fallbackModel`**：在失败时自动切换备用模型。  
- **`maxThinkingTokens`**：控制代理的思考次数。  
- **`strictMcpConfig`**：严格验证MCP配置。  
- **`continue`**：使用新提示继续会话（与`resume`不同）。  
- **`permissionMode: 'plan'`**：用于规划工作流程的新权限模式。  

**更多文档：**  
https://platform.claude.com/docs/en/agent-sdk/structured-outputs  

---

## 完整的Claude Agent SDK参考文档  

## 目录  
1. [核心查询API](#core-query-api)  
2. [工具集成（内置/自定义）](#tool-integration-built-in--custom)  
3. [MCP服务器（模型上下文协议）](#mcp-servers-model-context-protocol)  
4. [子代理编排](#subagent-orchestration)  
5. [会话管理](#session-management)  
6. [权限控制](#permission-control)  
7. [沙箱设置（安全关键）](#sandbox-settings-security-critical)  
8. [文件检查点](#file-checkpointing)  
9. [文件系统设置](#filesystem-settings)  
10. [查询对象方法](#query-object-methods)  
11. [消息类型与流式传输](#message-types--streaming)  
12. [错误处理](#error-handling)  
13. **已知问题与预防措施**（#known-issues-prevention）  

---

## 核心查询API  
**关键签名：**  
```typescript
query(prompt: string | AsyncIterable<SDKUserMessage>, options?: Options)
  -> AsyncGenerator<SDKMessage>
```  

**重要选项：**  
- `outputFormat`：支持结构化JSON模式验证（v0.1.45及以上版本）。  
- `settingSources`：指定文件系统数据来源（`user`/`project`/`local`）。  
- `canUseTool`：自定义权限逻辑回调函数。  
- `agents`：用于定义子代理的程序化配置。  
- `mcpServers`：MCP服务器配置。  
- `permissionMode`：权限模式（`default`/`acceptEdits`/`bypassPermissions`/`plan`）。  
- `betas`：启用测试功能（如100万令牌的上下文窗口）。  
- `sandbox`：用于安全执行的沙箱设置。  
- `enableFileCheckpointing`：启用文件状态快照功能。  
- `systemPrompt`：系统提示（字符串或预设对象）。  

### 扩展上下文（100万令牌）  
启用100万令牌的上下文窗口：  
```typescript
const response = query({
  prompt: "Analyze this large codebase",
  options: {
    betas: ['context-1m-2025-08-07'],  // Enable 1M context
    model: "claude-sonnet-4-5"
  }
});
```  

### 系统提示配置  
系统提示有两种形式：  
```typescript
// 1. Simple string
systemPrompt: "You are a helpful coding assistant."

// 2. Preset with optional append (preserves Claude Code defaults)
systemPrompt: {
  type: 'preset',
  preset: 'claude_code',
  append: "\n\nAdditional context: Focus on security."
}
```  
**使用预设形式**：可获取Claude Code的默认行为及自定义内容。  

---

## 工具集成（内置/自定义）  
**工具控制：**  
- `allowedTools`：允许使用的工具列表（优先级最高）。  
- `disallowedTools`：禁止使用的工具列表。  
- `canUseTool`：自定义权限回调函数（详见权限控制部分）。  

**内置工具：**  
读取、写入、编辑、Bash、Grep、Glob、WebSearch、WebFetch、Task、NotebookEdit、BashOutput、KillBash、ListMcpResources、ReadMcpResource、AskUserQuestion  

### AskUserQuestion工具（v0.1.71及更高版本）  
在代理执行过程中支持用户交互：  
```typescript
const response = query({
  prompt: "Review and refactor the codebase",
  options: {
    allowedTools: ["Read", "Write", "Edit", "AskUserQuestion"]
  }
});

// Agent can now ask clarifying questions
// Questions appear in message stream as tool_call with name "AskUserQuestion"
```  
**用途：**  
- 在任务执行过程中澄清模糊要求。  
- 在执行破坏性操作前获取用户批准。  
- 显示选项并获取用户选择。  

**工具配置（v0.1.57及更高版本）**  
**三种工具配置方式：**  
```typescript
// 1. Exact allowlist (string array)
tools: ["Read", "Write", "Grep"]

// 2. Disable all tools (empty array)
tools: []

// 3. Preset with defaults (object form)
tools: { type: 'preset', preset: 'claude_code' }
```  
**注意：**`allowedTools`和`disallowedTools`仍然有效，但`tools`提供了更多灵活性。  

---

## MCP服务器（模型上下文协议）  
**服务器类型：**  
- **进程内**：使用`createSdkMcpServer()`和`tool()`定义服务器。  
- **外部**：支持stdio、HTTP、SSE传输方式。  

**工具定义：**  
```typescript
tool(name: string, description: string, zodSchema, handler)
```  
**处理器返回值：**  
```typescript
{ content: [{ type: "text", text: "..." }], isError?: boolean }
```  

### 外部MCP服务器（stdio）  
```typescript
const response = query({
  prompt: "List files and analyze Git history",
  options: {
    mcpServers: {
      // Filesystem server
      "filesystem": {
        command: "npx",
        args: ["@modelcontextprotocol/server-filesystem"],
        env: {
          ALLOWED_PATHS: "/Users/developer/projects:/tmp"
        }
      },
      // Git operations server
      "git": {
        command: "npx",
        args: ["@modelcontextprotocol/server-git"],
        env: {
          GIT_REPO_PATH: "/Users/developer/projects/my-repo"
        }
      }
    },
    allowedTools: [
      "mcp__filesystem__list_files",
      "mcp__filesystem__read_file",
      "mcp__git__log",
      "mcp__git__diff"
    ]
  }
});
```  
### 外部MCP服务器（HTTP/SSE）  
```typescript
const response = query({
  prompt: "Analyze data from remote service",
  options: {
    mcpServers: {
      "remote-service": {
        url: "https://api.example.com/mcp",
        headers: {
          "Authorization": "Bearer your-token-here",
          "Content-Type": "application/json"
        }
      }
    },
    allowedTools: ["mcp__remote-service__analyze"]
  }
});
```  

### MCP工具命名规范  
**格式：**`mcp__<服务器名称>__<工具名称>`  
**重要提示：**  
- 服务器名称和工具名称必须与配置一致。  
- 使用双下划线（`__`）作为分隔符。  
- 必须将服务器添加到`allowedTools`列表中。  
**示例：**`mcp__weather-service__get_weather`、`mcp__filesystem__read_file`  

---

## 子代理编排  
**AgentDefinition类型：**  
```typescript
type AgentDefinition = {
  description: string;        // When to use this agent
  prompt: string;             // System prompt for agent
  tools?: string[];           // Allowed tools (optional)
  model?: 'sonnet' | 'opus' | 'haiku' | 'inherit';  // Model (optional)
  skills?: string[];          // Skills to load (v0.2.10+)
  maxTurns?: number;          // Maximum turns before stopping (v0.2.10+)
}
```  
**字段详情：**  
- **description**：指定何时使用该子代理（由主代理调用）。  
- **prompt**：系统提示（定义子代理的角色，继承主代理的上下文）。  
- **tools**：允许使用的工具（省略时继承主代理的工具列表）。  
- **model**：子代理使用的模型（`haiku`/`sonnet`/`opus`/`inherit`）。  
- **skills**：子代理需要加载的技能（v0.2.10及更高版本）。  
- **maxTurns**：限制子代理的思考次数（v0.2.10及更高版本）。  
**使用方式：**  
```typescript
agents: {
  "security-checker": {
    description: "Security audits and vulnerability scanning",
    prompt: "You check security. Scan for secrets, verify OWASP compliance.",
    tools: ["Read", "Grep", "Bash"],
    model: "sonnet",
    skills: ["security-best-practices"],  // Load specific skills
    maxTurns: 10  // Limit to 10 turns
  }
}
```  

### ⚠️ 子代理清理警告  
**已知问题：**  
当父代理停止时（无论是取消还是出现错误），子代理会作为孤儿进程继续运行。这可能导致：  
- 资源泄漏。  
- 父代理停止后工具仍继续执行。  
- 在递归场景中导致内存不足（[Claude Code问题#4850](https://github.com/anthropics/claude-code/issues/4850)。  
**解决方法：**  
在`Stop`钩子中实现清理逻辑：  
```typescript
const response = query({
  prompt: "Deploy to production",
  options: {
    agents: {
      "deployer": {
        description: "Handle deployments",
        prompt: "Deploy the application",
        tools: ["Bash"]
      }
    },
    hooks: {
      Stop: async (input) => {
        // Manual cleanup of spawned processes
        console.log("Parent stopped - cleaning up subagents");
        // Implement process tracking and termination
      }
    }
  }
});
```  
**改进计划：**[问题#142](https://github.com/anthropics/claude-agent-sdk-typescript/issues/142)建议实现自动终止机制。  

---

## 会话管理  
**选项：**  
- `resume:sessionId`：继续之前的会话。  
- `forkSession: true`：从现有会话创建新会话。  
- `continue: prompt`：使用新提示继续会话（与`resume`不同）。  
**会话分叉模式（独特功能）：**  
```typescript
// Explore alternative without modifying original
const forked = query({
  prompt: "Try GraphQL instead of REST",
  options: {
    resume: sessionId,
    forkSession: true  // Creates new branch, original session unchanged
  }
});
```  
**捕获会话ID：**  
```typescript
for await (const message of response) {
  if (message.type === 'system' && message.subtype === 'init') {
    sessionId = message.session_id;  // Save for later resume/fork
  }
}
```  

### V2会话API（预览版，v0.1.54及更高版本）  
**更简单的多轮对话模式：**  
```typescript
import {
  unstable_v2_createSession,
  unstable_v2_resumeSession,
  unstable_v2_prompt
} from "@anthropic-ai/claude-agent-sdk";

// Create a new session
const session = await unstable_v2_createSession({
  model: "claude-sonnet-4-5",
  workingDirectory: process.cwd(),
  allowedTools: ["Read", "Grep", "Glob"]
});

// Send prompts and stream responses
const stream = unstable_v2_prompt(session, "Analyze the codebase structure");
for await (const message of stream) {
  console.log(message);
}

// Continue conversation in same session
const stream2 = unstable_v2_prompt(session, "Now suggest improvements");
for await (const message of stream2) {
  console.log(message);
}

// Resume a previous session
const resumedSession = await unstable_v2_resumeSession(session.sessionId);
```  
**注意：**V2 API仍处于预览阶段（前缀为`unstable_`）。`.receive()`方法在v0.1.72版本中被重命名为`.stream()`。  

---

## 权限控制  
**权限模式：**  
```typescript
type PermissionMode = "default" | "acceptEdits" | "bypassPermissions" | "plan";
```  
- `default`：标准权限检查。  
- `acceptEdits`：自动批准文件编辑。  
- `bypassPermissions`：跳过所有权限检查（仅用于持续集成/持续部署）。  
- `plan`：规划模式（v0.1.45及更高版本）。  

### 自定义权限逻辑  
```typescript
const response = query({
  prompt: "Deploy application to production",
  options: {
    permissionMode: "default",
    canUseTool: async (toolName, input) => {
      // Allow read-only operations
      if (['Read', 'Grep', 'Glob'].includes(toolName)) {
        return { behavior: "allow" };
      }

      // Deny destructive bash commands
      if (toolName === 'Bash') {
        const dangerous = ['rm -rf', 'dd if=', 'mkfs', '> /dev/'];
        if (dangerous.some(pattern => input.command.includes(pattern))) {
          return {
            behavior: "deny",
            message: "Destructive command blocked for safety"
          };
        }
      }

      // Require confirmation for deployments
      if (input.command?.includes('deploy') || input.command?.includes('kubectl apply')) {
        return {
          behavior: "ask",
          message: "Confirm deployment to production?"
        };
      }

      // Allow by default
      return { behavior: "allow" };
    }
  }
});
```  
**示例：**  
```typescript
type CanUseToolCallback = (
  toolName: string,
  input: any
) => Promise<PermissionDecision>;

type PermissionDecision =
  | { behavior: "allow" }
  | { behavior: "deny"; message?: string }
  | { behavior: "ask"; message?: string };
```  
**示例用法：**  
```typescript
// Block all file writes
canUseTool: async (toolName, input) => {
  if (toolName === 'Write' || toolName === 'Edit') {
    return { behavior: "deny", message: "No file modifications allowed" };
  }
  return { behavior: "allow" };
}

// Require confirmation for specific files
canUseTool: async (toolName, input) => {
  const sensitivePaths = ['/etc/', '/root/', '.env', 'credentials.json'];
  if ((toolName === 'Write' || toolName === 'Edit') &&
      sensitivePaths.some(path => input.file_path?.includes(path))) {
    return {
      behavior: "ask",
      message: `Modify sensitive file ${input.file_path}?`
    };
  }
  return { behavior: "allow" };
}

// Log all tool usage
canUseTool: async (toolName, input) => {
  console.log(`Tool requested: ${toolName}`, input);
  await logToDatabase(toolName, input);
  return { behavior: "allow" };
}
```  

---

## 沙箱设置（安全关键）  
**为Bash命令启用沙箱执行：**  
```typescript
const response = query({
  prompt: "Run system diagnostics",
  options: {
    sandbox: {
      enabled: true,
      autoAllowBashIfSandboxed: true,  // Auto-approve bash in sandbox
      excludedCommands: ["rm", "dd", "mkfs"],  // Never auto-approve these
      allowUnsandboxedCommands: false  // Deny unsandboxable commands
    }
  }
});
```  
**沙箱设置类型：**  
```typescript
type SandboxSettings = {
  enabled: boolean;
  autoAllowBashIfSandboxed?: boolean;  // Default: false
  excludedCommands?: string[];
  allowUnsandboxedCommands?: boolean;  // Default: false
  network?: NetworkSandboxSettings;
  ignoreViolations?: SandboxIgnoreViolations;
};

type NetworkSandboxSettings = {
  enabled: boolean;
  proxyUrl?: string;  // HTTP proxy for network requests
};
```  
**关键选项：**  
- `enabled`：启用沙箱隔离。  
- `autoAllowBashIfSandboxed`：对安全的Bash命令跳过权限提示。  
- `excludedCommands`：始终需要权限的命令。  
- `allowUnsandboxedCommands`：允许在沙箱外执行的命令（风险较高）。  
- `network.proxyUrl`：通过代理路由网络请求（用于监控）。  
**最佳实践：**  
在生产环境中处理不可信输入时，始终使用沙箱。  

## 文件检查点  
**启用文件状态快照功能：**  
```typescript
const response = query({
  prompt: "Refactor the authentication module",
  options: {
    enableFileCheckpointing: true  // Enable file snapshots
  }
});

// Later: rewind file changes to a specific point
for await (const message of response) {
  if (message.type === 'user' && message.uuid) {
    // Can rewind to this point later
    const userMessageUuid = message.uuid;

    // To rewind (call on Query object)
    await response.rewindFiles(userMessageUuid);
  }
}
```  
**用途：**  
- 撤销失败的重构操作。  
- 进行A/B测试。  
- 安全地探索替代方案。  

## 文件系统设置  
**数据来源设置：**  
```typescript
type SettingSource = 'user' | 'project' | 'local';
```  
- `user`：`~/.claude/settings.json`（全局设置）。  
- `project`：`.claude/settings.json`（团队共享设置）。  
- `local`：`.claude/settings.local.json`（Git忽略的本地设置）。  
**默认设置：**不加载任何设置（`settingSources: []`）。  

**设置优先级：**  
当加载多个数据来源时，设置按以下顺序合并：  
1. **程序化选项**（通过`query()`传递）。  
2. **本地设置`(.claude/settings.local.json)`。  
3. **项目设置`(.claude/settings.json)`。  
4. **用户设置`(~/.claude/settings.json)`。  
**示例：**  
```typescript
// .claude/settings.json
{
  "allowedTools": ["Read", "Write", "Edit"]
}

// .claude/settings.local.json
{
  "allowedTools": ["Read"]  // Overrides project settings
}

// Programmatic
const response = query({
  options: {
    settingSources: ["project", "local"],
    allowedTools: ["Read", "Grep"]  // ← This wins
  }
});

// Actual allowedTools: ["Read", "Grep"]
```  
**最佳实践：**在持续集成/持续部署环境中使用`settingSources: ["project"]`以确保一致性。  

## 查询对象方法  
`query()`函数返回一个`Query`对象，其中包含以下方法：  
```typescript
const q = query({ prompt: "..." });

// Async iteration (primary usage)
for await (const message of q) { ... }

// Runtime model control
await q.setModel("claude-opus-4-5");           // Change model mid-session
await q.setMaxThinkingTokens(4096);            // Set thinking budget

// Introspection
const models = await q.supportedModels();     // List available models
const commands = await q.supportedCommands(); // List available commands
const account = await q.accountInfo();        // Get account details

// MCP status
const status = await q.mcpServerStatus();     // Check MCP server status
// Returns: { [serverName]: { status: 'connected' | 'failed', error?: string } }

// File operations (requires enableFileCheckpointing)
await q.rewindFiles(userMessageUuid);         // Rewind to checkpoint
```  
**用途：**  
- 根据任务复杂性动态切换模型。  
- 监控MCP服务器状态。  
- 调整代理的思考次数。  

## 消息类型与流式传输  
**消息类型：**  
- `system`：会话初始化/结束（包含`session_id`）。  
- `assistant`：代理响应。  
- `tool_call`：工具执行请求。  
- `tool_result`：工具执行结果。  
- `error`：错误信息。  
- `result`：最终结果（v0.1.45及更高版本包含结构化输出）。  
**流式传输方式：**  
```typescript
for await (const message of response) {
  if (message.type === 'system' && message.subtype === 'init') {
    sessionId = message.session_id;  // Capture for resume/fork
  }
  if (message.type === 'result' && message.structured_output) {
    // Structured output available (v0.1.45+)
    const validated = schema.parse(message.structured_output);
  }
}
```  

## 错误处理  
**错误代码：**  
| 错误代码 | 原因 | 解决方案 |  
|------------|-------|----------|  
| `CLI_NOT_FOUND` | 未安装Claude Code CLI | 安装：`npm install -g @anthropic-ai/claude-code`。  
| `AUTHENTICATION_FAILED` | API密钥无效 | 确保`ANTROPIC_API_KEY`环境变量已设置。  
| `RATE_LIMIT_EXCEEDED`：请求过多 | 实现重试机制。  
| `CONTEXT_LENGTH_EXCEEDED`：提示信息过长 | 使用会话压缩功能减少上下文长度。  
| `PERMISSION_DENIED`：工具被阻止 | 检查`permissionMode`和`canUseTool`设置。  
| `TOOL_EXECUTION_FAILED`：工具执行失败 | 检查工具实现。  
| `SESSION_NOT_FOUND`：会话ID无效 | 验证会话ID。  
| `MCP_SERVER_FAILED`：服务器错误 | 检查服务器配置。  

## 已知问题与预防措施  
本文档介绍了14个常见问题的预防方法：  

### 问题#1：CLI未找到  
**错误**：`Claude Code CLI未安装`  
**原因**：SDK需要Claude Code CLI。  
**预防措施**：在使用SDK之前先安装：`npm install -g @anthropic-ai/claude-code`。  

### 问题#2：身份验证失败  
**错误**：`API密钥无效`  
**原因**：`ANTROPIC_API_KEY`环境变量未设置。  
**预防措施**：务必设置`export ANTHROPIC_API_KEY="sk-ant-..."`。  

### 问题#3：权限被拒绝  
**错误**：工具执行被阻止  
**原因**：工具被权限限制。  
**预防措施**：使用`allowedTools`或自定义`canUseTool`回调函数。  

### 问题#4：上下文长度超出限制  
**错误**：提示信息过长**  
**原因**：输入内容超过了模型的上下文限制（[问题#138](https://github.com/anthropics/claude-agent-sdk-typescript/issues/138)）。  
**注意事项：**  
- 一旦达到上下文限制：  
  - 该会话的所有后续请求都会返回“提示信息过长”的错误。  
  - `/compact`命令会失败。  
  - 会话将永久中断，必须终止。  

**预防策略：**  
```typescript
// 1. Proactive session forking (create checkpoints before hitting limit)
const checkpoint = query({
  prompt: "Checkpoint current state",
  options: {
    resume: sessionId,
    forkSession: true  // Create branch before hitting limit
  }
});

// 2. Monitor time and rotate sessions proactively
const MAX_SESSION_TIME = 80 * 60 * 1000;  // 80 minutes (before 90-min crash)
let sessionStartTime = Date.now();

function shouldRotateSession() {
  return Date.now() - sessionStartTime > MAX_SESSION_TIME;
}

// 3. Start new sessions before hitting context limits
if (shouldRotateSession()) {
  const summary = await getSummary(currentSession);
  const newSession = query({
    prompt: `Continue with context: ${summary}`
  });
  sessionStartTime = Date.now();
}
```  
**注意：**SDK会自动压缩数据，但达到限制后会话将无法恢复。  

### 问题#5：工具执行超时  
**错误**：工具执行时间过长（默认超时为5分钟）。  
**预防措施**：在工具实现中加入超时处理逻辑。  

### 问题#6：会话未找到  
**错误**：会话ID无效。  
**原因**：会话已过期或无效。  
**预防措施**：从`system`初始化消息中捕获`session_id`。  

### 问题#7：MCP服务器连接失败  
**错误**：服务器未响应。  
**原因**：服务器未运行或配置错误。  
**预防措施**：独立测试MCP服务器，检查命令/URL是否正确。  

### 问题#8：子代理定义错误  
**错误**：`AgentDefinition`无效。  
**原因**：缺少必要字段。  
**预防措施**：务必包含`description`和`prompt`字段。  

### 问题#9：设置文件未找到  
**错误**：无法读取设置文件。  
**原因**：设置的文件不存在。  
**预防措施**：在包含设置文件之前先检查文件是否存在。  

### 问题#10：工具名称重复  
**错误**：存在同名工具。  
**原因**：多个MCP服务器定义了相同的工具名称。  
**预防措施**：使用唯一的工具名称，并在名称前加上服务器名称前缀。  

### 问题#11：Zod模式验证错误  
**错误**：输入数据不符合Zod模式。  
**原因**：提供的数据类型不正确。  
**预防措施**：使用带有`describe()`方法的描述性Zod模式。  

### 问题#12：文件系统权限问题  
**错误**：无法访问指定路径。  
**原因**：访问路径超出允许范围或权限不足。  
**预防措施**：设置正确的`workingDirectory`，检查文件权限。  

### 问题#13：MCP服务器配置缺失`type`字段  
**错误**：`Claude Code进程以代码1退出`（含义不明确）。  
**原因**：基于URL的MCP服务器需要指定`type: "http"`或`type: "sse"`字段。  
**预防措施**：为基于URL的MCP服务器指定传输类型。  
**诊断提示：**如果看到“进程以代码1退出”且没有其他错误信息，请检查MCP服务器配置中是否缺少`type`字段。  

### 问题#14：MCP工具结果中的Unicode分隔符  
**错误**：JSON解析错误，代理卡顿。  
**原因**：JSON中允许使用Unicode字符U+2028（换行符）和U+2029（段落分隔符），但这会导致JavaScript解析错误。  
**预防措施：**在MCP工具结果中转义这些字符。  
**相关问题：**[MCP Python SDK问题#1356](https://github.com/modelcontextprotocol/python-sdk/issues/1356)  

---

## 官方文档：  
- **Agent SDK概述**：https://platform.claude.com/docs/en/api/agent-sdk/overview  
- **TypeScript API**：https://platform.claude.com/docs/en/api/agent-sdk/typescript  
- **结构化输出**：https://platform.claude.com/docs/en/agent-sdk/structured-outputs  
- **GitHub（TypeScript版本）**：https://github.com/anthropics/claude-agent-sdk-typescript  
- **变更日志**：https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/CHANGELOG.md  

## 令牌效率：**  
- **未使用技能时**：约15,000个令牌（包括MCP设置、权限模式、会话API、沙箱配置、钩子、结构化输出、错误处理）。  
- **使用技能时**：约4,500个令牌（涵盖v0.2.12的所有功能及错误预防机制）。  
- **节省效果**：约70%（节省约10,500个令牌）。  

**预防的错误：**  
14个已知问题及其对应的解决方案（包括2个社区反馈的常见问题）。  
**关键特性：**  
- V2会话API、沙箱设置、文件检查点、查询方法、AskUserQuestion工具、结构化输出（v.1.45及更高版本）、会话分叉功能、`canUseTool`回调、完整的钩子系统（12个事件）、Zod v4支持、子代理清理机制。  

**最后验证日期**：2026-01-20  
**技能版本**：3.1.0  
**更新内容**：新增问题#13（MCP类型字段）、问题#14（Unicode字符问题）、问题#4的详细说明、添加了通过`Stop`钩子进行子代理清理的提示。