---
name: openclaw-json-editing
description: OpenClaw配置文件、工具及数据结构的高级JSON编辑功能。支持JSON5格式的配置文件处理，包括模式验证（schema validation）、合并补丁（merge patching）、环境变量替换（env var substitution）以及类型安全的修改（type-safe modifications）。
metadata:
  openclaw:
    emoji: "📝"
    requires:
      bins: ["jq"]
---

# OpenClaw JSON 编辑

本文档提供了在 OpenClaw 生态系统中编辑 JSON 的专业指导。OpenClaw 使用 **JSON5** 格式进行配置（支持注释和数组末尾的逗号），具备先进的配置合并功能，并通过 **Zod** 模式进行验证。

## 快速参考

| 任务 | 命令/模式 |
|------|-----------------|
| 验证配置 | `openclaw config validate` |
| 应用配置补丁 | `openclaw config patch <file.json>` |
| 安全解析 JSON | 使用 `safeParseJson()` 包装器 |
| 检查配置文件位置 | `openclaw config path` |
| 优雅打印 JSON | `JSON.stringify(data, null, 2)` |

## OpenClaw JSON5 配置

OpenClaw 的配置文件使用 **JSON5** 格式（而非严格的 JSON 格式）：

```json5
{
  // Single-line comments are allowed
  "gateway": {
    "mode": "http",  // Trailing commas are allowed
  },
  /* Multi-line comments
     are also supported */
  "agents": {
    "main": {
      "model": "anthropic/claude-opus-4-6",
    },
  },
}
```

### JSON 与 JSON5 的主要区别

- **注释**：支持单行注释（`//`）和多行注释（`/* */`）
- **数组和对象中的尾随逗号**：是允许的
- **键的格式**：`{ key: "value" }` 是有效的
- **字符串引号**：使用单引号（`'string'`）也是有效的

### 配置文件的位置

| 类型 | 路径 |
|------|------|
| 用户配置 | `~/.openclaw/config.json` |
| 项目配置 | `./openclaw.config.json` |
| 代理配置 | `~/.openclaw/agents/<id>/config.json` |
| 会话存储 | `~/.openclaw/sessions/` |
| 状态目录 | `~/.openclaw/`（或 `$OPENCLAW_STATE_DIR`）

## 安全的 JSON 操作

### 读取配置文件

OpenClaw 使用 `JSON5.parse()` 来解析配置文件，并提供安全的解析包装器：

```typescript
// OpenClaw's safeParseJson pattern
function safeParseJson<T>(raw: string): T | null {
  try {
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

// For OpenClaw configs, use JSON5
import JSON5 from "json5";

function loadConfigFile(path: string): unknown {
  try {
    const raw = fs.readFileSync(path, "utf8");
    return JSON5.parse(raw);  // Allows comments, trailing commas
  } catch {
    return undefined;
  }
}
```

### 写入配置文件

OpenClaw 以特定的格式和权限写入配置文件：

```typescript
function saveJsonFile(pathname: string, data: unknown) {
  const dir = path.dirname(pathname);
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
  }
  // 2-space indentation, trailing newline
  fs.writeFileSync(pathname, `${JSON.stringify(data, null, 2)}\n`, "utf8");
  fs.chmodSync(pathname, 0o600);  // User read/write only
}
```

### 类型检查

在假设数据结构之前，务必进行验证：

```typescript
// OpenClaw's isPlainObject (strictest)
function isPlainObject(value: unknown): value is Record<string, unknown> {
  return (
    typeof value === "object" &&
    value !== null &&
    !Array.isArray(value) &&
    Object.prototype.toString.call(value) === "[object Object]"
  );
}

// Less strict version
function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}
```

## 配置合并与补丁

### 合并补丁（RFC 7386）

OpenClaw 使用合并补丁来更新配置：

```typescript
// Apply a merge patch to base config
function applyMergePatch(base: unknown, patch: unknown): unknown {
  if (!isPlainObject(patch)) {
    return patch;
  }

  const result: Record<string, unknown> = isPlainObject(base) ? { ...base } : {};

  for (const [key, value] of Object.entries(patch)) {
    if (value === null) {
      delete result[key];  // null = delete key
      continue;
    }
    if (isPlainObject(value)) {
      const baseValue = result[key];
      result[key] = applyMergePatch(
        isPlainObject(baseValue) ? baseValue : {},
        value
      );
      continue;
    }
    result[key] = value;
  }

  return result;
}
```

## 使用示例

```javascript
// Add/update nested field
const patch = {
  agents: {
    main: {
      model: "anthropic/claude-opus-4-6"
    }
  }
};

// Delete a field (set to null)
const deletePatch = {
  agents: {
    main: {
      temperature: null  // Removes temperature
    }
  }
};

// Replace entire section
const replacePatch = {
  channels: {
    telegram: null,  // Delete old
    discord: { token: "new-token" }  // Add new
  }
};
```

## 环境变量替换

OpenClaw 的配置文件支持 `${VAR}` 和 `${VAR:-default}` 语法：

```json5
{
  "auth": {
    "profiles": {
      "openai": {
        "apiKey": "${OPENAI_API_KEY}"  // Substituted at load time
      },
      "anthropic": {
        "apiKey": "${ANTHROPIC_API_KEY:-fallback-key}"
      }
    }
  }
}
```

### 代码中的处理方式

```typescript
// Check if string contains env var reference
function containsEnvVarReference(value: string): boolean {
  return /\$\{[^}]+\}/.test(value);
}

// Collect all env var paths in an object
function collectEnvRefPaths(
  value: unknown,
  path: string,
  output: Map<string, string>
): void {
  if (typeof value === "string") {
    if (containsEnvVarReference(value)) {
      output.set(path, value);
    }
    return;
  }
  if (Array.isArray(value)) {
    value.forEach((item, index) => {
      collectEnvRefPaths(item, `${path}[${index}]`, output);
    });
    return;
  }
  if (isPlainObject(value)) {
    for (const [key, child] of Object.entries(value)) {
      const childPath = path ? `${path}.${key}` : key;
      collectEnvRefPaths(child, childPath, output);
    }
  }
}
```

## 模式验证

### Zod 模式

OpenClaw 使用 Zod 在运行时进行验证：

```typescript
import { z } from "zod";

// Define schema
const AgentConfigSchema = z.object({
  model: z.string().optional(),
  temperature: z.number().min(0).max(2).optional(),
  maxTokens: z.number().positive().optional(),
  enabled: z.boolean().default(true),
});

// Validate
type AgentConfig = z.infer<typeof AgentConfigSchema>;

function validateConfig(data: unknown): AgentConfig {
  return AgentConfigSchema.parse(data);
}

// Safe validation
function safeValidateConfig(data: unknown): AgentConfig | null {
  const result = AgentConfigSchema.safeParse(data);
  return result.success ? result.data : null;
}
```

### 常见的 OpenClaw 模式类型

```typescript
// Model reference: "provider/model-name"
const ModelRefSchema = z.string().regex(/^[a-z0-9-]+\/[a-z0-9-]+$/i);

// Channel ID
const ChannelIdSchema = z.enum([
  "telegram", "discord", "slack", "whatsapp",
  "signal", "imessage", "irc", "web"
]);

// Duration string: "30s", "5m", "1h"
const DurationSchema = z.string().regex(/^\d+[smhd]$/);
```

## 配置包含

OpenClaw 支持在配置文件中包含其他文件：

```json5
{
  "include": [
    "./base-config.json",
    "~/.openclaw/shared-channels.json"
  ],
  "agents": {
    // Local overrides
  }
}
```

### 处理顺序

1. 递归加载包含的文件（深度有限）
2. 按顺序合并配置文件（后面的文件会覆盖之前的配置）
3. 应用环境变量替换
4. 根据模式验证配置
5. 应用运行时的配置覆盖

## OpenClaw 的 jq 操作模式

### 常见操作

```bash
# Pretty print OpenClaw config
jq . ~/.openclaw/config.json

# Get gateway mode
jq '.gateway.mode' ~/.openclaw/config.json

# List all agent IDs
jq '.agents | keys[]' ~/.openclaw/config.json

# Find agent using specific model
jq '.agents | to_entries[] | select(.value.model == "anthropic/claude-opus-4-6") | .key' ~/.openclaw/config.json

# Get all channel types
jq '.channels | keys[]' ~/.openclaw/config.json

# Check if Telegram is configured
jq '.channels.telegram != null' ~/.openclaw/config.json

# Extract all model references
jq '.. | objects | select(has("model")) | .model' ~/.openclaw/config.json

# Merge patch using jq
jq '.agents.main.model = "anthropic/claude-opus-4-6"' ~/.openclaw/config.json > tmp.json \
  && mv tmp.json ~/.openclaw/config.json
```

### 高级 jq 操作

```bash
# Deep search for all API keys (for audit)
jq '.. | objects | .apiKey? // .token? // .password? | select(.)' ~/.openclaw/config.json

# Collect all environment variable references
jq -r '.. | strings | select(contains("${"))' ~/.openclaw/config.json

# Validate JSON structure (returns true/false)
jq 'if has("gateway") and has("agents") then true else false end' ~/.openclaw/config.json

# Create minimal config from full config
jq '{ gateway: .gateway, agents: { main: .agents.main } }' ~/.openclaw/config.json
```

## 常见的配置模式

### 网关配置

```json5
{
  "gateway": {
    "mode": "http",  // "http", "disabled", "process"
    "http": {
      "bind": "127.0.0.1",
      "port": 3000,
    },
    "auth": {
      "token": "${OPENCLAW_GATEWAY_TOKEN}",
    },
  },
}
```

### 代理配置

```json5
{
  "agents": {
    "main": {
      "model": "anthropic/claude-opus-4-6",
      "temperature": 0.7,
      "maxTokens": 4096,
      // System prompt or reference to file
      "systemPrompt": "You are a helpful assistant.",
      "systemPromptFile": "~/.openclaw/agents/main/prompt.md",
    },
    "coder": {
      "model": "anthropic/claude-sonnet-4-5",
      "temperature": 0.2,
      // Inherit from main with overrides
      "inherits": "main",
    },
  },
}
```

### 通道配置

```json5
{
  "channels": {
    "telegram": {
      "botToken": "${TELEGRAM_BOT_TOKEN}",
      "allowFrom": ["@username"],
    },
    "discord": {
      "botToken": "${DISCORD_BOT_TOKEN}",
      "applicationId": "123456789",
    },
    "slack": {
      "botToken": "${SLACK_BOT_TOKEN}",
      "appToken": "${SLACK_APP_TOKEN}",
    },
  },
}
```

### 工具配置

```json5
{
  "tools": {
    "alsoAllow": ["web_search", "browser"],
    "deny": ["exec"],
    "config": {
      "web_search": {
        "provider": "brave",
        "apiKey": "${BRAVE_API_KEY}",
      },
    },
  },
}
```

## 验证与错误处理

### 常见的验证错误

```typescript
// Schema validation errors provide detailed paths
const result = schema.safeParse(data);
if (!result.success) {
  for (const error of result.error.errors) {
    console.log(`${error.path.join('.')}: ${error.message}`);
    // e.g., "agents.main.temperature: Number must be less than or equal to 2"
  }
}
```

### 配置文件恢复

```bash
# If config is corrupted, OpenClaw keeps backups
ls -la ~/.openclaw/config.json.*

# Restore from backup
cp ~/.openclaw/config.json.2024-01-15T10-30-00.bak ~/.openclaw/config.json

# Or use OpenClaw's built-in rotation
openclaw config restore
```

## 最佳实践

### 1. 编辑后务必进行验证

```bash
# Validate config syntax and schema
openclaw config validate

# Test config loading
openclaw config get
```

### 2. 修改前先备份配置

```bash
# Create timestamped backup
cp ~/.openclaw/config.json ~/.openclaw/config.json.$(date +%Y%m%d_%H%M%S).bak
```

### 3. 使用类型检查

```typescript
// Never assume structure - always validate
if (!isPlainObject(config.agents)) {
  throw new Error("Invalid agents configuration");
}
```

### 4. 小心处理环境变量

```typescript
// Preserve env var references when editing
const originalValue = "${API_KEY}";
const newValue = process.env.API_KEY || originalValue;
```

### 5. 使用结构化克隆进行深度复制

```typescript
// Preferred for deep cloning
deepCopy = structuredClone(original);

// Fallback for older environments
deepCopy = JSON.parse(JSON.stringify(original));
```

### 6. 原子化写入操作

```typescript
// Write to temp file, then rename
fs.writeFileSync(tempPath, data);
fs.renameSync(tempPath, finalPath);
```

## 安全考虑

- **文件权限**：配置文件的权限应设置为 `0o600`（用户仅具有读写权限）
- **避免在 JSON 中存储敏感信息**：使用 `${ENV_VAR}` 替换敏感内容
- **验证输入数据**：始终使用模式对外部 JSON 数据进行验证
- **清理路径**：使用 `path.resolve()` 并检查路径遍历逻辑
- **审计日志**：OpenClaw 会将配置更改记录到 `config-audit.jsonl` 文件中

## 故障排除

### 常见问题及解决方法

| 问题 | 原因 | 解决方案 |
|-------|-------|----------|
| JSON 中出现意外字符 `/` | JSON 中包含注释 | 使用 JSON5 解析器 |
| 数组中存在尾随逗号 | 使用 JSON5 解析器 |
| 环境变量未替换 | 缺少相应的环境变量 | 检查 `${VAR:-default}` 的使用 |
| 验证失败 | 模式不匹配 | 运行 `openclaw config validate` |
| 权限问题 | 文件权限设置错误 | 将 `config.json` 的权限设置为 `600` |

### 调试命令

```bash
# Check raw config (before env substitution)
cat ~/.openclaw/config.json

# Check effective config (after all processing)
openclaw config get --json

# List all env var references
openclaw config env-refs

# Trace config loading
OPENCLAW_DEBUG=config openclaw config get
```

## 编辑提供者与模型配置

在 `openclaw.config.json` 中添加或更新 AI 提供者时，必须从提供者的 API 中获取实际的模型名称，并正确处理模型的不同变体。

### 模型发现流程

```bash
# 1. Fetch available models from provider API
# xAI example - requires XAI_API_KEY
XAI_API_KEY="your-key"
curl -s -H "Authorization: Bearer $XAI_API_KEY" \
  https://api.x.ai/v1/models | jq '.data[] | {id: .id, name: .object}'

# OpenAI example
curl -s -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models | jq '.data[] | select(.id | contains("gpt")) | .id'

# Together AI example
curl -s -H "Authorization: Bearer $TOGETHER_API_KEY" \
  https://api.together.xyz/v1/models | jq '.[] | {id: .id, name: .display_name}'
```

### 提供者配置模式

OpenClaw 使用 `ModelProviderConfig` 模式进行配置：

```typescript
type ModelProviderConfig = {
  baseUrl: string;           // API endpoint base URL
  apiKey?: string;           // Optional: API key (prefer env vars)
  auth?: "api-key" | "aws-sdk" | "oauth" | "token";
  api?: "openai-completions" | "openai-responses" | 
        "anthropic-messages" | "google-generative-ai" |
        "github-copilot" | "bedrock-converse-stream" | "ollama";
  headers?: Record<string, string>;  // Custom headers
  models: ModelDefinitionConfig[];   // Model definitions
};

type ModelDefinitionConfig = {
  id: string;                // Model ID (e.g., "grok-4")
  name: string;              // Display name (e.g., "Grok 4")
  api?: ModelApi;            // Override API type per model
  reasoning: boolean;        // Whether model supports reasoning/thinking
  input: Array<"text" | "image">;  // Supported input types
  cost: {
    input: number;           // Cost per 1M input tokens
    output: number;          // Cost per 1M output tokens
    cacheRead: number;       // Cost per 1M cached tokens read
    cacheWrite: number;      // Cost per 1M cached tokens written
  };
  contextWindow: number;     // Max context window size
  maxTokens: number;         // Max output tokens
  headers?: Record<string, string>;
  compat?: ModelCompatConfig;
};
```

### 推理模型家族

**注意**：某些模型具有特殊的推理变体。例如，xAI 的 `grok-4-1-fast` 有三个变体：

| 模型 ID | 类型 | 说明 |
|----------|------|-------|
| `grok-4-1-fast` | 基础模型 | 默认模型 |
| `grok-4-1-fast-reasoning` | 具有推理功能的模型 |
| `grok-4-1-fast-non-reasoning` | 无推理功能的模型 | 更快，但不支持推理 |

在 OpenClaw 中，通常只需配置基础模型（`grok-4-1-fast`）。系统会根据 `thinking` 指令或配置自动切换使用推理模型或非推理模型。

```json5
{
  "models": {
    "providers": {
      "xai": {
        "baseUrl": "https://api.x.ai/v1",
        "api": "openai-completions",
        "apiKey": "${XAI_API_KEY}",
        "models": [
          {
            "id": "grok-4-1-fast",
            "name": "Grok 4.1 Fast",
            "reasoning": false,  // Base model is non-reasoning
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 128000,
            "maxTokens": 8192
          }
          // NOTE: Do NOT add -reasoning or -non-reasoning variants separately
          // OpenClaw handles these automatically via model family resolution
        ]
      }
    }
  }
}
```

### 模型家族的解析

OpenClaw 在 `src/agents/model-families.ts` 中定义了推理模型家族：

```typescript
const REASONING_MODEL_FAMILIES = [
  {
    provider: "xai",
    members: [
      "grok-4-1-fast",
      "grok-4-1-fast-reasoning",
      "grok-4-1-fast-non-reasoning"
    ],
    reasoningModel: "grok-4-1-fast-reasoning",
    nonReasoningModel: "grok-4-1-fast-non-reasoning",
  },
];
```

当用户请求特定模型时（例如 `thinking: "on"` 或 `thinking: "off"`），OpenClaw 会：

1. 检查请求的模型是否属于某个推理模型家族
2. 如果 `thinking: "on"`，则使用对应的推理模型
3. 如果 `thinking: "off"`，则使用非推理模型
4. 如果没有 `thinking` 指令，则使用基础模型

### 完整的提供者配置示例

```json5
{
  "models": {
    "mode": "merge",  // "merge" or "replace"
    "providers": {
      // xAI - Grok models with reasoning variants
      "xai": {
        "baseUrl": "https://api.x.ai/v1",
        "api": "openai-completions",
        "apiKey": "${XAI_API_KEY}",
        "models": [
          {
            "id": "grok-4-1-fast",
            "name": "Grok 4.1 Fast",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 128000,
            "maxTokens": 8192
          },
          {
            "id": "grok-4",
            "name": "Grok 4",
            "reasoning": false,
            "input": ["text", "image"],  // Vision-capable
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 128000,
            "maxTokens": 8192,
            "compat": {
              "supportsReasoningEffort": false,
              "maxTokensField": "max_completion_tokens"
            }
          }
        ]
      },
      
      // OpenAI - with response API and reasoning
      "openai": {
        "baseUrl": "https://api.openai.com/v1",
        "api": "openai-responses",
        "apiKey": "${OPENAI_API_KEY}",
        "models": [
          {
            "id": "gpt-5.2",
            "name": "GPT-5.2",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 2.5, "output": 10, "cacheRead": 0.5, "cacheWrite": 1.25 },
            "contextWindow": 200000,
            "maxTokens": 16384,
            "compat": {
              "supportsReasoningEffort": true,
              "thinkingFormat": "openai"
            }
          },
          {
            "id": "o3-mini",
            "name": "o3 Mini",
            "reasoning": true,  // Built-in reasoning model
            "input": ["text", "image"],
            "cost": { "input": 1.1, "output": 4.4, "cacheRead": 0.275, "cacheWrite": 0.55 },
            "contextWindow": 200000,
            "maxTokens": 100000,
            "compat": {
              "supportsReasoningEffort": true,
              "requiresAssistantAfterToolResult": true
            }
          }
        ]
      },
      
      // Anthropic - Messages API
      "anthropic": {
        "baseUrl": "https://api.anthropic.com",
        "api": "anthropic-messages",
        "apiKey": "${ANTHROPIC_API_KEY}",
        "models": [
          {
            "id": "claude-opus-4-6",
            "name": "Claude Opus 4.6",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 15, "output": 75, "cacheRead": 1.88, "cacheWrite": 7.5 },
            "contextWindow": 200000,
            "maxTokens": 8192,
            "compat": {
              "supportsStore": false,
              "supportsDeveloperRole": false
            }
          }
        ]
      },
      
      // Google Gemini
      "google": {
        "baseUrl": "https://generativelanguage.googleapis.com/v1beta",
        "api": "google-generative-ai",
        "apiKey": "${GEMINI_API_KEY}",
        "models": [
          {
            "id": "gemini-3-pro-preview",
            "name": "Gemini 3 Pro Preview",
            "reasoning": false,
            "input": ["text", "image"],
            "cost": { "input": 1.25, "output": 10, "cacheRead": 0.31, "cacheWrite": 1.25 },
            "contextWindow": 1000000,
            "maxTokens": 8192,
            "compat": {
              "thinkingFormat": "qwen"
            }
          }
        ]
      },
      
      // Ollama - local models (auto-discovered)
      "ollama": {
        "baseUrl": "http://localhost:11434/v1",
        "api": "ollama",
        "models": []  // Auto-populated from /api/tags
      }
    }
  }
}
```

### 模型兼容性标志

```typescript
type ModelCompatConfig = {
  // OpenAI-specific features
  supportsStore?: boolean;                    // Use 'store' parameter
  supportsDeveloperRole?: boolean;            // Use 'developer' vs 'system' role
  supportsReasoningEffort?: boolean;          // Support reasoning_effort param
  supportsUsageInStreaming?: boolean;         // Usage in streaming responses
  supportsStrictMode?: boolean;               // Strict tool mode
  
  // Token handling
  maxTokensField?: "max_completion_tokens" | "max_tokens";
  
  // Thinking/reasoning format
  thinkingFormat?: "openai" | "zai" | "qwen";
  
  // Tool calling quirks
  requiresToolResultName?: boolean;           // Must include tool result name
  requiresAssistantAfterToolResult?: boolean; // Assistant message after tool
  requiresThinkingAsText?: boolean;           // Thinking blocks as text
  requiresMistralToolIds?: boolean;           // Mistral-style tool IDs
};
```

### 验证提供者配置

```bash
# Validate the full config including models
openclaw config validate

# Check if models.json is correctly generated
openclaw models list

# Test a specific model provider
openclaw models test --provider xai --model grok-4-1-fast

# Debug model resolution
OPENCLAW_DEBUG=models openclaw models list
```

### 常见的问题及解决方法

| 问题 | 发生原因 | 解决方案 |
|---------|---------------|----------|
| 误添加了推理模型变体 | 不要手动添加推理模型变体 | 只需配置基础模型（如 `grok-4-1-fast`） |
| `reasoning` 值设置错误 | 可能导致模型功能混淆 | 应根据基础模型设置 `reasoning` 值 |
| `api` 字段缺失 | 可能导致配置不匹配 | 明确设置 `api` 的正确值 |
| API 键硬编码 | 存在安全风险 | 应始终使用 `${ENV_VAR}` 替换 API 键 |
| API 地址错误 | 可能导致请求失败 | 请检查提供者的文档 |
| 成本值不正确 | 可能影响费用计算 | 请核实每个提供者的定价信息 |

### 各提供者的特定说明

#### xAI (Grok)
- 使用 `openai-completions` API
- 模型家族会自动匹配相应的推理变体
- 视觉模型的支持情况因模型而异

#### OpenAI
- 对于 o-series 和 GPT-5，使用 `openai-responses` API
- 对于 GPT-4，使用 `openai-completions` API
- 可通过 `supportsReasoningEffort` 参数调整推理能力

#### Anthropic
- 使用 `anthropic-messages` API
- 所有模型都支持推理功能
- 提示缓存的成本结构有所不同

#### Google (Gemini)
- 使用 `google-generative-ai` API
- 支持较大的上下文窗口（100 万个令牌）
- 与 OpenAI/Anthropic 的内容格式不同

#### Ollama
- 使用 `api: "ollama"` 进行模型发现
- 模型会自动从 `/api/tags` 中识别
- 无需 API 密钥即可进行本地推理

### 模型别名

为常见的模型在代理配置中定义别名：

```json5
{
  "agents": {
    "defaults": {
      "models": {
        "fast": { "alias": "Grok Fast", "id": "xai/grok-4-1-fast" },
        "smart": { "alias": "Claude Opus", "id": "anthropic/claude-opus-4-6" },
        "vision": { "alias": "GPT Vision", "id": "openai/gpt-5.2" }
      }
    }
  }
}
```

在代理配置中引用这些别名：

```json5
{
  "agents": {
    "main": {
      "model": "fast"  // Resolves to xai/grok-4-1-fast
    }
  }
}
```