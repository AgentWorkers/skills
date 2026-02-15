---
name: vestige
description: 基于FSRS-6间隔重复法的认知记忆系统。记忆会像人类的记忆一样自然地消退。该系统用于实现跨会话的持久性回忆功能。
---

# Vestige 记忆技能

Vestige 记忆系统基于 130 年的记忆研究成果，融合了间隔重复学习（FSRS-6）、扩散激活理论以及突触标记技术，所有功能均完全在本地运行。

## 二进制数据存储位置  
```
~/bin/vestige-mcp
~/bin/vestige
~/bin/vestige-restore
```

## 使用场景  
- **跨会话的持久化记忆**  
- **用户偏好设置**（例如：“我更喜欢使用 TypeScript”，“我总是使用深色模式”）  
- **需要记住的 bug 修复方案及解决方案**  
- **项目模式与架构决策**  
- **提醒事项及未来需要执行的操作**  

## 快速命令  
### 搜索记忆  
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search","arguments":{"query":"user preferences"}}}' | ~/bin/vestige-mcp 2>/dev/null | jq -r '.result.content[0].text // .error.message'
```  

### 保存记忆（智能存储）  
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"smart_ingest","arguments":{"content":"User prefers Swiss Modern design style for presentations","tags":["preference","design"]}}}' | ~/bin/vestige-mcp 2>/dev/null | jq -r '.result.content[0].text // .error.message'
```  

### 简单保存  
```bash
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"ingest","arguments":{"content":"TKPay Offline project: POC 2 months, MVP 2 months, budget 250K DH","tags":["project","tkpay"]}}}' | ~/bin/vestige-mcp 2>/dev/null | jq -r '.result.content[0].text // .error.message'
```  

### 查看统计信息  
```bash
~/bin/vestige stats
```  

### 系统健康检查  
```bash
~/bin/vestige health
```  

## 可用的 MCP 工具  
| 工具 | 描述 |  
|------|-------------|  
| `search` | 统一搜索（关键词 + 语义搜索 + 混合搜索方式） |  
| `smart_ingest` | 智能存储功能，可检测重复内容 |  
| `ingest` | 简单的记忆存储操作 |  
| `memory` | 查看、删除或检查记忆状态 |  
| `codebase` | 记录项目模式与架构决策 |  
| `intention` | 设置提醒事项及未来执行任务 |  
| `promote_memory` | 将重要记忆标记为“有用”（增强记忆效果） |  
| `demote_memory` | 将错误记忆标记为“无用”（削弱记忆效果） |  

## 触发词  
| 用户输入 | 执行动作 |  
|-----------|--------|  
| “记住这个” | 立即进行智能存储 |  
| “别忘了” | 以高优先级进行智能存储 |  
| “我总是……” / “我从不……” | 保存为偏好设置 |  
| “我更喜欢……” / “我喜欢……” | 保存为偏好设置 |  
| “这很重要” | 进行智能存储并标记为“有用” |  
| “提醒我……” | 创建提醒事项 |  

## 会话开始时的操作  
在对话开始时，先搜索相关内容：  
```bash
# Search user preferences
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search","arguments":{"query":"user preferences instructions"}}}' | ~/bin/vestige-mcp 2>/dev/null | jq -r '.result.content[0].text'

# Search project context
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search","arguments":{"query":"current project context"}}}' | ~/bin/vestige-mcp 2>/dev/null | jq -r '.result.content[0].text'
```  

## 辅助脚本  
为方便使用，可以创建 `~/bin/vmem` 脚本：  
```bash
#!/bin/bash
# Vestige Memory Helper
ACTION=$1
shift

case $ACTION in
  search)
    echo "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"search\",\"arguments\":{\"query\":\"$*\"}}}" | ~/bin/vestige-mcp 2>/dev/null | jq -r '.result.content[0].text // .error.message'
    ;;
  save)
    echo "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"tools/call\",\"params\":{\"name\":\"smart_ingest\",\"arguments\":{\"content\":\"$*\"}}}" | ~/bin/vestige-mcp 2>/dev/null | jq -r '.result.content[0].text // .error.message'
    ;;
  stats)
    ~/bin/vestige stats
    ;;
  *)
    echo "Usage: vmem [search|save|stats] [content]"
    ;;
esac
```  

## 数据存储位置  
- **macOS**: `~/Library/Application Support/com.vestige.core/`  
- **Linux**: `~/.local/share/vestige/`  
- **嵌入缓存**: `~/Library/Caches/com.vestige.core/fastembed/`  

## 集成说明  
Vestige 与现有的 `memory/` 文件夹系统兼容：  
- `memory/*.md`：人类可读的日常日志  
- `MEMORY.md`：经过整理的长期笔记  
- **Vestige**：提供语义搜索、自动遗忘机制及间隔重复学习功能  

**Vestige 的应用场景**：  
- 需要语义性记忆的内容（而不仅仅是关键词搜索）  
- 需要永久保存的偏好设置  
- 需要记住的解决方案（若长时间未使用，系统会自动删除）