---
name: context-bridge
description: >
  **恢复多会话项目：保留完整上下文**  
  适用于需要返回之前的工作、查看对话记录、回顾过去的决策，或在不同日期/周之间衔接项目上下文的情况。该功能可解决代理在会话之间丢失数据的问题。
version: 1.0.0
metadata:
  openclaw:
    emoji: "🌉"
    requires:
      anyBins: ["jq", "find"]
    os: ["linux", "darwin", "win32"]
---
# Context Bridge

**再也不用丢失项目上下文了。** Context Bridge 可在代理会话之间创建持久化的记忆存储，让您能够在几天或几周后继续处理复杂的项目，同时保留所有的对话内容、决策记录和项目进度。

## 使用场景

- 继续进行多天的项目工作  
- 回忆之前会话中做出的决定  
- 查找关于某个主题的过往对话记录  
- 在长时间未参与项目后重新建立项目上下文  
- 建立项目的工作记录  
- 避免向代理重复解释相同的内容  
- 跟踪决策历史和背后的思考过程  
- 随时间推移记录项目的发展过程  

## 问题所在  

**代理在会话之间会丢失信息。** 每次执行 `/new` 命令时，所有会话数据都会被清除，导致您需要重新解释项目背景、重新分享决策内容，并重新开始工作。  

**Context Bridge 会为您记住这些信息。** 它会保存对话记录、决策内容、文件变更以及决策背后的思考过程，当您返回时能够快速恢复项目的完整上下文。  

## 快速入门  

### 保存当前会话上下文  
```bash
# Save context with a project name
echo "Save this session as: api-redesign" | openclaw agent

# Or save with description
echo "Save context: api-redesign - Switched from REST to GraphQL" | openclaw agent
```  

### 恢复上一个会话  
```bash
# Resume specific project
echo "Resume context: api-redesign" | openclaw agent

# List available contexts
echo "List saved contexts" | openclaw agent

# Search contexts by keyword
echo "Find contexts about authentication" | openclaw agent
```  

## 核心命令  

### 保存上下文  
```bash
# Save current session
echo "save context as project-name" | openclaw agent

# Save with description
echo "save context as project-name: brief description" | openclaw agent

# Auto-save on /new (if context-bridge hook enabled)
/new  # Automatically prompts to save current context
```  

### 恢复上下文  
```bash
# Resume by project name
echo "resume context: project-name" | openclaw agent

# Resume latest session
echo "resume last context" | openclaw agent

# Resume with date
echo "resume context from yesterday" | openclaw agent
```  

### 查询上下文  
```bash
# List all saved contexts
echo "list contexts" | openclaw agent

# Search by keyword
echo "find contexts about database migration" | openclaw agent

# Show context summary
echo "summarize context: project-name" | openclaw agent

# Show decision history
echo "what decisions were made in: project-name" | openclaw agent
```  

## 保存的内容  

Context Bridge 会捕获以下全面的会话数据：  

### 1. 对话记录  
- 完整的对话历史（用户与代理之间的交流）  
- 每条消息的时间戳  
- 命令的执行顺序  

### 2. 做出的决策  
- 重要的决策点（例如：“我们决定使用 X，因为 Y”）  
- 考虑过的替代方案  
- 讨论过的权衡因素  

### 3. 文件变更  
- 创建、修改或删除的文件  
- 代码变更的差异  
- 文件的路径和描述  

### 4. 任务进度  
- 已完成的任务  
- 待处理的任务  
- 阻碍项目进展的因素  

### 5. 相关会话  
- 链接到相关上下文的链接  
- 引用该项目的对话记录  
- 项目的工作时间线  

## 上下文存储位置  

上下文数据存储在：`~/.openclaw/workspace/memory/contexts/`  

```
contexts/
├── api-redesign.json           # Main context data
├── api-redesign-sessions/      # Individual session logs
│   ├── 2026-03-04.json
│   ├── 2026-03-05.json
│   └── 2026-03-10.json
└── index.json                  # Search index
```  

### 上下文文件格式  

```json
{
  "project": "api-redesign",
  "created": "2026-03-04T10:30:00Z",
  "updated": "2026-03-10T14:20:00Z",
  "description": "Migrating from REST to GraphQL API",
  "sessions": [
    {
      "date": "2026-03-04",
      "summary": "Initial GraphQL schema design",
      "messages": 45,
      "decisions": ["Use Apollo Server", "Code-first schema approach"],
      "files_changed": ["schema.ts", "resolvers.ts"]
    }
  ],
  "decisions": [
    {
      "decision": "Use Apollo Server over graphql-yoga",
      "reasoning": "Better TypeScript support and caching",
      "date": "2026-03-04T11:15:00Z",
      "alternatives": ["graphql-yoga", "express-graphql"]
    }
  ],
  "related_contexts": ["authentication-refactor", "database-migration"],
  "tags": ["graphql", "backend", "api"]
}
```  

## 高级功能  

### 自动保存上下文  

安装 `context-bridge` 插件，以便在会话内容发生变化时自动保存：  
```bash
openclaw hooks enable context-bridge-autosave
```  

现在，每次执行 `/new` 命令时，系统都会提示您保存当前会话内容。  

### 上下文模板  

为重复出现的项目类型创建上下文模板：  
```bash
# Save current context as template
echo "save as template: feature-development" | openclaw agent

# Use template for new project
echo "new context from template: feature-development, name: user-profiles" | openclaw agent
```  

### 合并相关会话  

将多个相关的会话合并为一个完整的上下文：  
```bash
echo "merge contexts: api-redesign, auth-refactor into: backend-overhaul" | openclaw agent
```  

### 决策时间线  

按时间顺序查看所有决策记录：  
```bash
# Show all decisions for project
echo "decision timeline for: api-redesign" | openclaw agent

# Export decisions as markdown
echo "export decisions: api-redesign to decisions.md" | openclaw agent
```  

### 上下文差异  

查看不同会话之间的变化内容：  
```bash
echo "diff contexts: api-redesign from 2026-03-04 to 2026-03-10" | openclaw agent
```  

## 搜索与发现  

### 语义搜索  

Context Bridge 支持基于语义的搜索功能：  
```bash
# Find contexts by topic
echo "find contexts about error handling" | openclaw agent

# Search within specific context
echo "search api-redesign for: rate limiting" | openclaw agent
```  

### 基于标签的文件管理  

```bash
# Add tags to context
echo "tag api-redesign with: backend, graphql, production" | openclaw agent

# Find all contexts with tag
echo "list contexts tagged: backend" | openclaw agent
```  

## 与工作区的集成  

Context Bridge 可与 OpenClaw 的工作区集成：  
```bash
# Link context to workspace files
echo "associate api-redesign with ./src/api/" | openclaw agent

# Show context for current directory
echo "show context for current project" | openclaw agent
```  

## 手动管理上下文  

### 通过命令行  
```bash
# View context file
cat ~/.openclaw/workspace/memory/contexts/api-redesign.json | jq

# Search contexts with jq
find ~/.openclaw/workspace/memory/contexts/ -name "*.json" | \
  xargs jq -r '. | select(.tags | contains(["graphql"])) | .project'

# Backup contexts
tar -czf contexts-backup.tar.gz ~/.openclaw/workspace/memory/contexts/
```  

### 通过代理技能  

Context Bridge 为代理提供了辅助命令：  
```bash
# Agent can call these internally
context-bridge save <project-name>
context-bridge load <project-name>
context-bridge list
context-bridge search <query>
context-bridge decisions <project-name>
```  

## 使用案例  

### 多天项目开发  
```bash
# Day 1: Start feature
echo "I'm building a user authentication system" | openclaw agent
# ... work happens ...
echo "save context as: user-auth" | openclaw agent

# Day 3: Resume work
echo "resume context: user-auth" | openclaw agent
# Agent loads full conversation history, decisions, files changed
```  

### 项目回顾  
```bash
# Generate project summary
echo "summarize context: user-auth including all decisions and challenges" | openclaw agent

# Export for team review
echo "export context: user-auth to user-auth-retrospective.md" | openclaw agent
```  

### 构建知识库  
```bash
# Find all authentication-related work
echo "find contexts about authentication" | openclaw agent

# Create knowledge base entry
echo "create knowledge base entry from contexts: user-auth, oauth-integration, 2fa-setup" | openclaw agent
```  

## 配置  

Context Bridge 的配置文件位于：`~/.openclaw/config.yaml`：  
```yaml
contextBridge:
  enabled: true
  autoSave: true  # Prompt to save on /new
  maxContexts: 100  # Keep last 100 contexts
  compressionThreshold: 30  # Compress contexts older than 30 days
  retentionDays: 365  # Delete contexts after 1 year
  indexing:
    enabled: true
    updateInterval: 3600  # Reindex every hour
  storage:
    directory: "~/.openclaw/workspace/memory/contexts/"
    format: "json"  # json or yaml
```  

## 隐私与安全  

### 本地存储  

所有上下文数据仅存储在您的本地机器上，不会发送到任何外部服务。  

### 敏感数据处理  

Context Bridge 可以过滤敏感数据：  
```yaml
contextBridge:
  filters:
    - "API_KEY"
    - "password"
    - "token"
    - "secret"
```  

在保存的上下文中，敏感信息会被替换为占位符（例如：`API_KEY="[REDACTED]"`）。  

### 加密  

对于敏感项目，可以启用加密功能：  
```bash
# Encrypt specific context
echo "encrypt context: api-redesign with password" | openclaw agent

# Decrypt when loading
echo "resume context: api-redesign" | openclaw agent
# Prompts for password
```  

## 故障排除  

### 上下文未保存  
```bash
# Check permissions
ls -la ~/.openclaw/workspace/memory/contexts/

# Verify jq is installed
which jq

# Test manual save
echo '{"test": "context"}' > ~/.openclaw/workspace/memory/contexts/test.json
```  

### 上下文无法加载  
```bash
# Check context exists
ls ~/.openclaw/workspace/memory/contexts/ | grep project-name

# Validate JSON
jq . ~/.openclaw/workspace/memory/contexts/project-name.json

# Check logs
tail -f ~/.openclaw/logs/gateway.log | grep context-bridge
```  

### 大型上下文  

如果上下文数据量过大：  
```bash
# Compress old sessions
echo "compress context: project-name older than 30 days" | openclaw agent

# Archive completed contexts
echo "archive context: project-name" | openclaw agent
```  

## 性能优化  

- 上下文数据会在 30 天后自动压缩（可配置）  
- 支持全文搜索，以加快查询速度  
- 懒加载机制：仅将当前活跃的上下文加载到内存中  

### 性能指标  

- 保存会话数据：约 100 毫秒  
- 加载会话数据（含历史记录）：约 200 毫秒  
- 搜索：在 100 个上下文中搜索约 50 毫秒  
- 每个上下文的存储空间：约 50 KB（压缩后）  

## 使用建议  

- **经常保存会话内容**：使用描述性强的文件名（例如 `payment-integration-stripe` 而不是 `project1`）  
- **添加描述**：简短的摘要有助于后续搜索  
- **使用标签**：用标签来组织相关上下文  
- **链接相关上下文**：方便快速查找相关内容  
- **定期回顾决策记录**：了解工作模式  
- **归档已完成的工作**：保持活跃上下文的有序性  
- **导出重要上下文**：生成 Markdown 格式的文档  
- **使用模板**：为重复出现的项目类型标准化上下文结构  
- **进行语义搜索**：使用自然语言查询，而不仅仅是关键词  
- **合并相关会话**：将分散的工作内容整合成一个完整的上下文  

## 与 `session-memory` 的对比  

**session-memory**：仅保存原始的会话数据  
**Context Bridge**：提供智能化的上下文管理功能，包括：  
- 对对话内容的语义理解  
- 决策的提取和跟踪  
- 跨会话的关联功能  
- 搜索和发现功能  
- 项目时间线的可视化展示  

Context Bridge 基于 `session-memory` 构建，但增加了更多的智能功能。  

## 未来计划  

即将推出的功能：  
- 根据当前工作内容自动建议上下文保存方式  
- 项目发展的可视化时间线  
- 团队上下文共享（可选）  
- 与外部项目管理工具的集成  
- 基于人工智能的上下文摘要生成  
- 自动化的决策记录功能  

## 贡献方式  

Context Bridge 是开源项目，欢迎贡献代码：  
- GitHub：[context-bridge 仓库]  
- 问题报告：提交功能请求或bug报告  
- 文档贡献：帮助改进本指南  

---

**技能版本**：1.0.0  
**最后更新时间**：2026 年 3 月  
**作者**：HY  
**许可证**：MIT  
**分类**：代理框架 / 提高工作效率  

**相关技能**：session-memory, skill-creator, obsidian