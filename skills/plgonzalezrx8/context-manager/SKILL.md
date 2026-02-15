---
name: context-manager
description: 基于人工智能的 OpenClaw 会话上下文管理
user-invocable: true
---

# 上下文管理技能

这是一个基于AI的上下文管理工具，专为OpenClaw会话设计。它利用代理本身生成智能摘要，然后使用压缩后的上下文来重置会话。

## 快速入门

```bash
# List all sessions with usage stats
~/openclaw/skills/context-manager/compress.sh list

# Check status of a specific session
~/openclaw/skills/context-manager/compress.sh status agent:main:main

# Generate AI summary (read-only, safe)
~/openclaw/skills/context-manager/compress.sh summarize agent:main:main

# Compress session: generate summary, reset, inject (DESTRUCTIVE)
~/openclaw/skills/context-manager/compress.sh summarize agent:main:main --replace
```

## 使用场景

- 上下文使用量达到70-80%以上时  
- 会话时间较长且对话记录较多时  
- 在会话变得缓慢或失去连贯性之前  
- 为保持会话的快速性和专注性而主动使用  

## 工作原理

1. **AI摘要生成**：向代理发送请求，让其自行总结当前的上下文。  
2. **备份**：将原始的JSONL会话文件保存到`memory/compressed/`目录中。  
3. **重置**：删除原始的JSONL文件（官方推荐的重置方法）。  
4. **注入新内容**：将AI生成的摘要作为新会话的第一条消息发送。  
5. **结果**：会话键保持不变，但会话ID会更新，同时上下文会被压缩。  

**关键点**：代理能够完全了解自身的上下文，因此生成的摘要最为准确。  

## 命令  

### 会话相关命令  

| 命令 | 描述 |  
|---------|-------------|  
| `list` | 列出所有会话及其对应的令牌使用情况。 |  
| `status [KEY]` | 显示指定会话的详细状态。 |  
| `summarize [KEY]` | 生成AI摘要（仅限查看）。 |  
| `summarize [KEY] --replace` | 生成摘要并同时重置会话（压缩上下文）。 |  
| `compress [KEY]` | 使用传统的grep方法提取会话内容（不推荐）。 |  
| `check [KEY]` | 检查会话是否超过预设的压缩阈值。 |  
| `check-all` | 同时检查所有会话的状态。 |  

### 配置相关命令  

| 命令 | 描述 |  
|---------|-------------|  
| `set-threshold N` | 设置压缩阈值（50-99%，默认值为80%）。 |  
| `set-depth LEVEL` | 设置摘要的详细程度：简略/平衡/全面。 |  
| `set-quiet-hours HH` | 设置安静使用时间（例如：“23:00-07:00”）。 |  
| `help` | 显示帮助信息和使用示例。 |  

## 示例  

### 列出所有会话  

```bash
$ ~/openclaw/skills/context-manager/compress.sh list
📋 Available Sessions (4 total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#    SESSION KEY                              KIND       TOKENS    USAGE
1    agent:main:main                          direct      70188      70%
2    agent:main:slack:channel:c0aaruq2en9     group       20854      20%
3    agent:main:cron:0d02af4b-...             direct      18718      18%
```  

### 检查会话状态  

```bash
$ ~/openclaw/skills/context-manager/compress.sh status agent:main:main
📊 Context Manager Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Session Key: agent:main:main
  Session ID:  fc192a2d-091c-48c7-9fad-12bf34687454
  Kind:        direct
  Model:       gemini-3-flash
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Threshold:   80%
  Tokens:      70188 / 100000
  Usage:       70%
```  

### 生成AI摘要（仅限查看）  

```bash
$ ~/openclaw/skills/context-manager/compress.sh summarize agent:main:main
🧠 Requesting AI summary for session: agent:main:main
  Session ID: fc192a2d-091c-48c7-9fad-12bf34687454

✅ AI Summary generated!
  Saved to: memory/compressed/20260127-123146.ai-summary.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
### Session Summary: January 27, 2026

#### 1. What was accomplished
- System audit completed
- Essay generation with sub-agents
...
```  

### 完整压缩（生成摘要 + 重置 + 注入新内容）  

```bash
$ ~/openclaw/skills/context-manager/compress.sh summarize agent:main:main --replace
🧠 Requesting AI summary for session: agent:main:main
  Session ID: fc192a2d-091c-48c7-9fad-12bf34687454
  Mode: REPLACE (will reset session after summary)

✅ AI Summary generated!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[AI-generated summary displayed]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔄 Resetting session and injecting compressed context...
  Backing up session file...
  Backup saved: memory/compressed/20260127-123146.session-backup.jsonl
  Deleting session JSONL to reset...
  Injecting compressed context into fresh session...
✅ Session compressed successfully!
  Old session ID: fc192a2d-091c-48c7-9fad-12bf34687454
  New session ID: a1b2c3d4-...
  Session is ready to continue with compressed context
```  

**压缩效果**：70,000个令牌 → 16,000个令牌（减少了77%）  

## 输出文件  

压缩完成后，相关文件会被保存在`memory/compressed/`目录中：  

| 文件名 | 描述 |  
|------|-------------|  
| `{timestamp}.ai-summary.md` | AI生成的会话摘要。 |  
| `{timestamp}.session-backup.jsonl` | 原始会话的完整备份（需要时可恢复）。 |  
| `{timestamp}.transcript.md` | 原始的聊天记录（传统格式）。 |  
| `{timestamp}.summary.md` | 基于grep的摘要（传统方法）。 |  

## 系统要求  

- **openclaw**：必须运行中。  
- **jq**：用于解析JSON数据（可通过`brew install jq`安装）。  
- **访问权限**：脚本需要`openclaw agent`和`openclaw sessions`的权限。  

## 技术细节  

### 会话重置方式  

脚本通过删除JSONL文件来实现会话重置（官方推荐的方法）：  
1. 将原始JSONL文件备份到`memory/compressed/`。  
2. 删除`~/.openclaw/agents/{agent}/sessions/{sessionId}.jsonl`文件。  
3. 通过`openclaw agent --to main`命令发送压缩后的上下文。  
4. 系统会自动创建新会话，并将AI生成的摘要作为第一条消息发送。  

### 为什么不用`/reset`命令？  

`/reset`命令仅在聊天界面有效。如果通过`openclaw agent --session-id`发送该命令，系统会将其视为普通消息并尝试执行相应的操作。  

### AI摘要生成提示  

脚本要求代理提供以下信息：  
1. 完成的主要任务。  
2. 做出的关键决策及其理由。  
3. 当前的会话状态。  
4. 未完成的任务。  
5. 需要记住的重要信息。  

## 故障排除  

### AI摘要为空  

如果AI摘要生成失败，请检查`stderr`的输出。  
```bash
# The script uses 2>/dev/null to avoid Node deprecation warnings breaking JSON
openclaw agent --session-id $ID -m "..." --json 2>/dev/null
```  

### 会话未成功重置  

请确认JSONL文件的路径是否正确。  
```bash
ls ~/.openclaw/agents/main/sessions/
```  

### 从备份中恢复会话  

如果出现故障，可以使用备份文件恢复会话。  
```bash
cp memory/compressed/{timestamp}.session-backup.jsonl \
   ~/.openclaw/agents/main/sessions/{sessionId}.jsonl
```  

### 查看日志  

使用`openclaw logs`进行故障排查。  
```bash
openclaw logs --limit 50 --json | grep -i "error\|fail"
```  

## 最佳实践：  

1. **先备份**：脚本会自动备份会话数据，但你也可以在测试前手动备份。  
2. **先在非关键会话上测试**：先在Slack频道或定时任务中测试该功能。  
3. **验证摘要质量**：先运行`summarize`命令（不使用`--replace`选项）来检查摘要的准确性。  
4. **监控令牌数量**：使用`status`命令确认压缩是否成功。  

## 相关文档：  
- `openclaw sessions --help`  
- `openclaw agent --help`