---
name: claude-sdk
description: Claude Code SDK - 包含用于读写、编辑代码的工具（支持Bash命令），以及用于执行任务和技能的代理工具（agent tools）。此外，还支持钩子（hooks）机制和与MCP（Management Console Platform）的集成。该SDK专为Claude Code的扩展开发而设计。
---

# Claude SDK 专家

具备对 Claude Code SDK、相关工具以及扩展开发的深入理解。

## 核心工具

**文件操作**：
```typescript
// Read files
Read({ file_path: '/absolute/path/file.ts' });

// Write files (creates new or overwrites)
Write({
  file_path: '/absolute/path/file.ts',
  content: 'export const hello = () => "world";'
});

// Edit files (precise replacements)
Edit({
  file_path: '/absolute/path/file.ts',
  old_string: 'const x = 1;',
  new_string: 'const x = 2;'
});
```

**搜索**：
```typescript
// Find files by pattern
Glob({ pattern: '**/*.ts' });

// Search file contents
Grep({
  pattern: 'TODO',
  output_mode: 'files_with_matches'
});

// Search with context
Grep({
  pattern: 'function.*export',
  output_mode: 'content',
  '-C': 3, // 3 lines before/after
  '-n': true // Line numbers
});
```

**执行**：
```typescript
// Run commands
Bash({
  command: 'npm test',
  description: 'Run test suite'
});

// Background processes
Bash({
  command: 'npm run dev',
  run_in_background: true
});
```

## 代理工具

**子代理**：
```typescript
// Invoke specialized sub-agent
Task({
  subagent_type: 'plugin:agent-folder:agent-name',
  prompt: 'Analyze this architecture'
});
```

**技能**：
```typescript
// Activate skill explicitly
Skill({ skill: 'skill-name' });

// Or let auto-activation handle it
```

**命令**：
```typescript
// Execute slash command
SlashCommand({ command: '/plugin:command arg1 arg2' });
```

## 插件钩子

**可用的钩子事件**：
```typescript
type HookEvent =
  | 'PostToolUse'        // After tool executes
  | 'PreToolUse'         // Before tool executes
  | 'PermissionRequest'  // User permission dialog
  | 'Notification'       // System notification
  | 'UserPromptSubmit'   // After user submits prompt
  | 'Stop'               // Conversation stopped
  | 'SubagentStop'       // Sub-agent stopped
  | 'PreCompact'         // Before context compaction
  | 'SessionStart'       // Session started
  | 'SessionEnd';        // Session ended
```

**钩子配置**：
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "TodoWrite",
        "hooks": [{
          "type": "command",
          "command": "${CLAUDE_PLUGIN_ROOT}/hooks/post-task.sh",
          "timeout": 10
        }]
      }
    ]
  }
}
```

## MCP（模型上下文协议）

> **优先使用代码实现**：Anthropic 的研究表明，与 MCP 相比，代码执行方式可以减少 98% 的通信开销（[参考链接：https://www.anthropic.com/engineering/code-execution-with-mcp】）。仅在以下情况下使用 MCP：快速调试、Claude Desktop 集成，或那些没有代码实现方式的工具。对于自动化、持续集成/持续部署（CI/CD）以及生产环境，建议直接编写代码。

**MCP 服务器集成**（如需使用）：
```typescript
// Connect to MCP server
const mcp = await connectMCP({
  name: 'filesystem',
  transport: 'stdio',
  command: 'node',
  args: ['mcp-server-filesystem.js']
});

// Use MCP tools
mcp.call('read_file', { path: '/path/to/file' });
```

## 最佳实践

**工具使用**：
- 使用绝对路径（而非相对路径）
- 优雅地处理错误
- 提供清晰的文档说明
- 批量执行独立操作

**性能优化**：
- 尽量减少工具调用次数
- 在读取数据前先使用 grep 进行搜索
- 并行执行独立操作
- 可能的情况下缓存搜索结果

**安全性**：
- 验证文件路径的合法性
- 对用户输入进行安全处理
- 避免使用硬编码的敏感信息
- 使用环境变量来存储配置信息

构建强大的 Claude Code 扩展吧！