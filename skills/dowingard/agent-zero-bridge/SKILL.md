---
name: agent-zero-bridge
description: 将复杂的编码任务、研究工作或自主执行的任务委托给 Agent Zero 框架。当用户输入“询问 Agent Zero”、“将任务委托给 A0”或需要 Agent Zero 进行长时间运行的自主编码（包含自我修正循环）时，可以使用该框架。该框架支持双向通信、文件附件传输、任务分解以及进度报告功能。
---

# Agent Zero Bridge

用于实现Clawdbot与[Agent Zero](https://github.com/frdel/agent-zero)之间的双向通信。

## 使用场景

- 需要迭代或自我修正的复杂编码任务  
- 长时间运行的构建、测试或基础设施维护工作  
- 需要持续使用Docker执行环境的任务  
- 包含多个顺序工具调用的研究项目  
- 用户明确要求使用Agent Zero的功能  

## 设置（仅首次使用）

### 1. 先决条件  
- Node.js 18及以上版本（用于内置的`fetch`函数）  
- Agent Zero已运行（建议使用Docker，端口为50001）  
- Clawdbot Gateway已启用HTTP端点  

### 2. 安装  
```bash
# Copy skill to Clawdbot skills directory
cp -r <this-skill-folder> ~/.clawdbot/skills/agent-zero-bridge

# Create config from template
cd ~/.clawdbot/skills/agent-zero-bridge
cp .env.example .env
```  

### 3. 配置`.env`文件  
```env
# Agent Zero (get token from A0 settings or calculate from runtime ID)
A0_API_URL=http://127.0.0.1:50001
A0_API_KEY=your_agent_zero_token

# Clawdbot Gateway
CLAWDBOT_API_URL=http://127.0.0.1:18789
CLAWDBOT_API_TOKEN=your_gateway_token

# For Docker containers reaching host (use your machine's LAN IP)
CLAWDBOT_API_URL_DOCKER=http://192.168.1.x:18789
```  

### 4. 获取Agent Zero令牌  
```python
# Calculate from A0's runtime ID
import hashlib, base64
runtime_id = "your_A0_PERSISTENT_RUNTIME_ID"  # from A0's .env
hash_bytes = hashlib.sha256(f"{runtime_id}::".encode()).digest()
token = base64.urlsafe_b64encode(hash_bytes).decode().replace("=", "")[:16]
print(token)
```  

### 5. 启用Clawdbot Gateway端点  
在`~/.clawdbot/clawdbot.json`文件中添加以下内容：  
```json
{
  "gateway": {
    "bind": "0.0.0.0",
    "auth": { "mode": "token", "token": "your_token" },
    "http": { "endpoints": { "chatCompletions": { "enabled": true } } }
  }
}
```  
然后执行`clawdbot gateway restart`命令重启Gateway。  

### 6. 将客户端部署到Agent Zero容器中  
```bash
docker exec <container> mkdir -p /a0/bridge/lib
docker cp scripts/lib/. <container>:/a0/bridge/lib/
docker cp scripts/clawdbot_client.js <container>:/a0/bridge/
docker cp .env <container>:/a0/bridge/
docker exec <container> sh -c 'echo "DOCKER_CONTAINER=true" >> /a0/bridge/.env'
```  

## 使用方法

### 向Agent Zero发送任务  
```bash
node scripts/a0_client.js "Build a REST API with JWT authentication"
node scripts/a0_client.js "Review this code" --attach ./file.py
node scripts/a0_client.js "New task" --new  # Start fresh conversation
```  

### 检查任务状态  
```bash
node scripts/a0_client.js status
node scripts/a0_client.js history
node scripts/a0_client.js reset  # Clear conversation
```  

### 任务分解（创建可追踪的项目）  
```bash
node scripts/task_breakdown.js "Build e-commerce platform"
# Creates notebook/tasks/projects/<name>.md with checkable steps
```  

### 从Agent Zero到Clawdbot的通信  
在Agent Zero的容器内部：  
```bash
# Report progress
node /a0/bridge/clawdbot_client.js notify "Working on step 3..."

# Ask for input
node /a0/bridge/clawdbot_client.js "Should I use PostgreSQL or SQLite?"

# Invoke Clawdbot tool
node /a0/bridge/clawdbot_client.js tool web_search '{"query":"Node.js best practices"}'
```  

## 故障排除  

| 错误 | 解决方法 |
|-------|-----|
| 401 / API密钥错误 | 确保`A0_API_KEY`与Agent Zero的`mcp_server_token`匹配 |
| Docker连接失败 | 在`CLAWDBOT_API_URL_DOCKER`中使用主机的局域网IP地址，并确保Gateway监听0.0.0.0地址 |
| Agent Zero出现500错误 | 检查Agent Zero的LLM API密钥（Gemini/OpenAI）是否有效 |