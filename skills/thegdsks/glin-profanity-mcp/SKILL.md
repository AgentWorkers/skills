---
name: glin-profanity-mcp
description: MCP服务器提供了用于检测AI助手中脏话的工具。这些工具可用于审查大量用户内容、审核评论以生成 moderation 报告、在发布前分析文本中是否存在脏话，或者在AI的工作流程中实现内容审核功能。
---

# Glin Profanity MCP 服务器

MCP（模型上下文协议，Model Context Protocol）服务器提供脏话检测功能，可作为 Claude Desktop、Cursor 和 Windsurf 等 AI 助手的工具。

**适用场景：**  
- AI 辅助的内容审核工作流程  
- 批量审核  
- 审计报告  
- 发布前的内容验证  

## 安装  

### Claude Desktop  
将以下代码添加到 `~/Library/Application Support/Claude/claude_desktop_config.json` 文件中：  
```json
{
  "mcpServers": {
    "glin-profanity": {
      "command": "npx",
      "args": ["-y", "glin-profanity-mcp"]
    }
  }
}
```  

### Cursor  
将以下代码添加到 `.cursor/mcp.json` 文件中：  
```json
{
  "mcpServers": {
    "glin-profanity": {
      "command": "npx",
      "args": ["-y", "glin-profanity-mcp"]
    }
  }
}
```  

## 可用工具  

### 核心检测工具  
| 工具 | 描述 |  
|------|-------------|  
| `check_profanity` | 检查文本中是否存在脏话，并提供详细结果 |  
| `censor_text` | 对脏话进行审查，并支持自定义替换内容 |  
| `batch_check` | 同时检查多条文本（最多 100 条） |  
| `validate_content` | 计算内容的安全性得分（0-100 分），并提供处理建议 |  

### 分析工具  
| 工具 | 描述 |  
|------|-------------|  
| `analyze_context` | 基于上下文（医疗、游戏等领域）进行分析 |  
| `detect_obfuscation` | 检测文本中的缩写和特殊字符技巧 |  
| `explain_match` | 解释为何某段文本被标记为脏话 |  
| `compare_strictness` | 比较不同检测规则的严格程度 |  

### 实用工具  
| 工具 | 描述 |  
| `suggest_alternatives` | 提供干净的替代文本建议 |  
| `analyze_corpus` | 分析最多 500 条文本以获取统计信息 |  
| `create_regex_pattern` | 生成用于自定义检测的正则表达式 |  
| `get_supported_languages` | 列出所有支持的 24 种语言 |  

### 用户跟踪工具  
| 工具 | 描述 |  
| `track_user_message` | 跟踪用户的违规行为 |  
| `get_user_profile` | 获取用户的审核历史记录 |  
| `get_high_risk_users` | 列出违规率较高的用户 |  

## 示例提示  

### 内容审核  
```
"Check these 50 user comments and tell me which ones need moderation"
"Validate this blog post before publishing - use high strictness"
"Analyze this medical article with medical domain context"
```  

### 批量操作  
```
"Batch check all messages in this array and return only flagged ones"
"Generate a moderation audit report for these comments"
```  

### 理解标记  
```
"Explain why 'f4ck' was detected as profanity"
"Compare strictness levels for this gaming chat message"
```  

### 内容清理  
```
"Suggest professional alternatives for this flagged text"
"Censor the profanity but preserve first letters"
```  

## 使用场景  

**在以下情况下使用 MCP 服务器：**  
- 当 AI 辅助内容审核工作流程时  
- 需要批量检查用户提交的内容时  
- 在发布前验证内容时  
- 需要进行人工审核时  

**在以下情况下使用核心库：**  
- 需要自动实时过滤内容（通过钩子或中间件实现）  
- 每条消息都需要进行人工审核时  
- 对性能要求极高的应用（响应时间需小于 1 毫秒）  

## 资源链接：  
- npm: https://www.npmjs.com/package/glin-profanity-mcp  
- GitHub: https://github.com/GLINCKER/glin-profanity/tree/release/packages/mcp  
- 核心库: https://www.npmjs.com/package/glin-profanity