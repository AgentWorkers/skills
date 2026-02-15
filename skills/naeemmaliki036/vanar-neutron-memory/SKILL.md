---
name: vanar-neutron-memory
description: 使用 Vanar Neutron API 存储和检索代理的内存数据。该 API 用于保存带有语义搜索功能的信息，并在会话之间保持代理上下文的持久性。
user-invocable: true
metadata: {"openclaw": {"emoji": "🧠", "requires": {"env": ["NEUTRON_API_KEY", "NEUTRON_AGENT_ID"]}, "primaryEnv": "NEUTRON_API_KEY"}}
---

# Vanar Neutron Memory

这是一个专为AI代理设计的持久化内存存储系统，支持语义搜索功能。用户可以将文本保存为“种子”（seeds），通过语义搜索快速查找所需信息，并在会话之间保持代理上下文的一致性。

## 主要特性

- **自动回忆（Auto-Recall）**：在每个AI回合开始前自动查询相关记忆内容，并将其作为上下文信息提供给AI。
- **自动捕获（Auto-Capture）**：在每个AI回合结束后自动保存对话记录。
- **语义搜索（Semantic Search）**：利用Jina Embeddings v4（1024维）技术按语义内容检索记忆。
- **内存类型**：包括情景记忆（episodic memory）、语义记忆（semantic memory）、程序记忆（procedural memory）和工作记忆（working memory）。
- **区块链认证（Blockchain Attestation）**：采用防篡改的内存存储机制，并附带交易哈希值以确保数据完整性。

## 先决条件

请在以下链接获取API密钥：**https://openclaw.vanarchain.com/**  
API凭据可以通过环境变量设置：  
```bash
export NEUTRON_API_KEY=your_key
export NEUTRON_AGENT_ID=your_agent_id
export YOUR_AGENT_IDENTIFIER=your_agent_name_or_id  # agent_id name or defaults to 1
```  
或者将其保存在`~/.config/neutron/credentials.json`文件中：  
```json
{
  "api_key": "your_key_here",
  "agent_id": "your_agent_id_here",
  "your_agent_identifier": "your_agent_name_or_id"
}
```  

## 测试

请按照以下步骤验证您的系统配置：  
```bash
./scripts/neutron-memory.sh test  # Test API connection
```  

## 自动记忆管理钩子（Auto-Capture & Auto-Recall）

该系统内置了OpenClaw钩子以实现自动记忆管理功能：  
- `hooks/pre-tool-use.sh`：在AI回合开始前查询记忆内容并注入上下文。  
- `hooks/post-tool-use.sh`：在AI回合结束后保存对话记录。  

### 配置设置

这两个功能默认都是启用的。如需禁用，请执行相应操作：  
```bash
export VANAR_AUTO_RECALL=false   # Disable auto-recall
export VANAR_AUTO_CAPTURE=false  # Disable auto-capture
```  
或者将配置信息添加到您的凭据文件中：  
```json
{
  "api_key": "your_key_here",
  "agent_id": "your_agent_id_here",
  "your_agent_identifier": "your_agent_name_or_id",
  "auto_recall": true,
  "auto_capture": true
}
```  

## 脚本使用

请使用`scripts/`目录中的bash脚本：  
- `neutron-memory.sh`：主要的命令行工具。  

## 常用操作

- **将文本保存为种子（Save Text as a Seed）**：  
```bash
./scripts/neutron-memory.sh save "Content to remember" "Title of this memory"
```  
- **执行语义搜索（Perform Semantic Search）**：  
```bash
./scripts/neutron-memory.sh search "what do I know about blockchain" 10 0.5
```  
- **创建代理上下文（Create Agent Context）**：  
```bash
./scripts/neutron-memory.sh context-create "my-agent" "episodic" '{"key":"value"}'
```  
- **列出代理上下文（List Agent Contexts）**：  
```bash
./scripts/neutron-memory.sh context-list "my-agent"
```  
- **获取特定上下文（Get Specific Context）**：  
```bash
./scripts/neutron-memory.sh context-get abc-123
```  

## 交互数据的双重存储机制

当NeutronMemoryBot处理用户交互时，数据会被存储在两个地方：  
1. **代理上下文（Agent Context）**：包含结构化元数据和会话跟踪信息的简化版本。  
2. **种子（Seed）**：包含完整对话内容的快照，用于语义搜索。  

每次机器人回复评论时，都会将整个对话记录（原始帖子 + 所有评论 + 机器人的回复）保存为“种子”。这意味着：  
- 每个“种子”都代表了完整的对话记录；  
- 后期的“种子”包含比早期更多的上下文信息；  
- 语义搜索能够找到最相关的对话内容；  
- 数据采用追加-only模式存储：新数据会被添加到现有种子中，旧数据保持不变。  

## 种子格式（Seed Format）：  
```
Thread snapshot - {timestamp}

Post: {full post content}

Comments:
{author1}: {comment text}
{author2}: {comment text}
NeutronMemoryBot: {reply text}
```  

## API接口  

- `POST /seeds`：用于保存文本内容（格式为multipart/form-data）。  
- `POST /seeds/query`：执行语义搜索（请求体为JSON格式）。  
- `POST /agent-contexts`：创建代理上下文。  
- `GET /agent-contexts`：列出所有代理上下文（可选参数：`agentId`）。  
- `GET /agent-contexts/{id}`：获取特定代理的上下文信息。  

**身份验证要求：**  
所有请求必须包含`Authorization: Bearer $NEUTRON_API_KEY`头部，以及`appId`/`externalUserId`查询参数。  

**支持的内存类型：** `episodic`, `semantic`, `procedural`, `working`  
**种子支持的文本格式：** `text`, `markdown`, `json`, `csv`, `claude_chat`, `gpt_chat`, `email`