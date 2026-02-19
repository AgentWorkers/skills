---
name: exa-tool
description: Exa MCP集成支持高级搜索、研究和爬取功能。
homepage: https://exa.ai
metadata:
  {
    "openclaw": {
      "emoji": "🔍",
      "requires": { "env": ["EXA_API_KEY"] },
      "primaryEnv": "EXA_API_KEY",
      "bins": ["exa-search", "exa-web-search"]
    }
  }
---
# Exa MCP 工具

该技能允许您通过 Exa MCP 服务器访问 Exa 强大的搜索和研究功能。

## 可用工具

### 通用工具
- `exa-search <tool> '{"json":"args"}'` - 任何 Exa MCP 工具的通用封装器

### 专用封装器
- `exa-web-search '{"query":"...", "count":10, "freshness":"pw", ...}'` - 带有可选过滤条件的网络搜索

## 完整工具列表（通过 `exa-search`）

Exa MCP 服务器提供的所有工具如下：

| 工具 | 描述 |
|------|-------------|
| `web_search_exa` | 搜索网络上的任何主题，并获取干净的内容 |
| `web_search_advanced_exa` | 带有过滤条件（域名、日期、内容选项）的高级搜索 |
| `get_code_context_exa` | 查找代码示例、文档和编程解决方案 |
| `crawling_exa` | 从已知 URL 获取特定网页的完整内容 |
| `company_research_exa` | 研究任何公司的业务信息和新闻 |
| `people_search_exa` | 查找人员及其职业资料 |
| `deep_researcher_start` | 启动一个 AI 研究代理，生成详细的报告 |
| `deep_researcher_check` | 检查深度研究任务的进度并获取结果 |

## 设置

1. 从 [https://dashboard.exa.ai/api-keys](https://dashboard.exa.ai/api-keys) 获取您的 Exa API 密钥。

2. 设置环境变量：
   ```bash
   export EXA_API_KEY="your_exa_api_key_here"
   ```

   或将其添加到您的 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）中：
   ```bash
   export EXA_API_KEY="your_exa_api_key_here"
   ```

   或在工作区创建一个 `.env` 文件：
   ```bash
   echo "EXA_API_KEY=your_exa_api_key_here" > ~/.openclaw/workspace/.env
   source ~/.openclaw/workspace/.env
   ```

3. 重新启动 OpenClaw 以加载该技能：
   ```bash
   openclaw gateway restart
   ```

## 使用示例

### 基本网络搜索
```bash
exa-web-search '{"query":"Step-3.5 Flash benchmarks"}'
```

### 带有过滤条件的高级搜索
```bash
exa-search web_search_advanced_exa '{
  "query": "OpenClaw AI",
  "count": 10,
  "freshness": "pw",
  "includeDomains": ["github.com", "docs.openclaw.ai"]
}'
```

### 代码搜索
```bash
exa-search get_code_context_exa '{
  "query": "OpenClaw agent implementation",
  "count": 5
}'
```

### 爬取特定 URL
```bash
exa-search crawling_exa '{
  "url": "https://docs.openclaw.ai/",
  "maxPages": 10
}'
```

### 公司研究
```bash
exa-search company_research_exa '{
  "company": "OpenClaw",
  "includeNews": true,
  "newsDays": 30
}'
```

### 人员搜索
```bash
exa-search people_search_exa '{
  "query": "Phil openclaw creator",
  "count": 10
}'
```

### 深度研究（两步流程）
```bash
# Start research
TASK_ID=$(exa-search deep_researcher_start '{
  "query": "Current state of AI agents in 2026",
  "maxSources": 20
}' | jq -r '.taskId')

# Check status (poll until complete)
while true; do
  exa-search deep_researcher_check '{"taskId":"'"$TASK_ID"'"}'
  sleep 5
done
```

## 输出格式

所有工具返回符合 Exa MCP 响应结构的 JSON 数据。实际内容位于 `result` 字段中，具体内容因工具而异，但通常包括：

- `content`: 包含 `title`、`url`、`text`（片段）的结果项数组
- 有时还包括其他元数据，如 `cost`、`duration`、`sources`

示例网络搜索输出：
```json
{
  "content": [
    {
      "title": "Step 3.5 Flash - MathArena",
      "url": "https://matharena.ai/models/stepfun_3_5_flash",
      "text": "Step 3.5 Flash benchmarks and performance metrics..."
    }
  ]
}
```

## 在 OpenClaw 代理中使用

代理可以直接使用这些工具：

```javascript
// In an agent session
/exec exa-search web_search_exa '{"query":"latest news"}'

// Or via API
{
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Search for recent AI developments using exa-search"
  }
}
```

## 注意事项

- 使用频率受到您的 Exa 计划的限制
- MCP 服务器使用 Server-Sent Events (SSE) 流式传输；封装器负责处理这一过程
- 所有工具都接受各种可选参数；请参阅 Exa 文档以获取完整规范
- 错误会以适当的退出代码和消息形式输出到标准错误流（stderr）

## 故障排除

**“EXA_API_KEY 未设置”**
- 确保环境变量在运行 OpenClaw 的会话中已正确设置
- 如果使用 systemd/systemctl，请在服务文件或 `/etc/environment` 中设置 API 密钥

**“406 Not Acceptable”**
- 该工具已正确设置了 Accept 标头；这种情况不应在封装器中发生

**结果为空或没有结果**
- 验证您的 API 密钥是否有足够的信用额度/配额
- 查看 Exa 仪表板：[https://dashboard.exa.ai](https://dashboard.exa.ai)

## 参考资料

- Exa MCP 文档：[https://exa.ai/docs/reference/exa-mcp](https://exa.ai/docs/reference/exa-mcp)
- MCP 服务器：[https://mcp.exa.ai/mcp](https://mcp.exa.ai/mcp)
- API 密钥：[https://dashboard.exa.ai/api-keys](https://dashboard.exa.ai/api-keys)