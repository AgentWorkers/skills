---
name: aws-agentcore-langgraph
description: 在 AWS Bedrock AgentCore 上部署 LangGraph 代理。这些代理可用于以下场景：  
(1) 需要编排器和专业代理模式的多代理系统；  
(2) 构建具有持久跨会话内存的状态ful 代理；  
(3) 通过 AgentCore Gateway（MCP、Lambda、API）连接外部工具；  
(4) 在分布式代理之间管理共享上下文；  
(5) 通过 CLI 部署复杂的代理生态系统，并具备生产环境的可观测性和扩展性。
---

# AWS AgentCore + LangGraph

基于 AWS Bedrock AgentCore 的多代理系统，采用 LangGraph 进行任务编排。来源：https://github.com/aws/bedrock-agentcore-starter-toolkit

## 安装
```bash
pip install bedrock-agentcore bedrock-agentcore-starter-toolkit langgraph
uv tool install bedrock-agentcore-starter-toolkit  # installs agentcore CLI
```

## 快速入门
```python
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition  # routing + tool execution
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from typing import Annotated
from typing_extensions import TypedDict

class State(TypedDict):
    messages: Annotated[list, add_messages]

builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))  # prebuilt tool executor
builder.add_conditional_edges("agent", tools_condition)  # routes to tools or END
builder.add_edge(START, "agent")
graph = builder.compile()

app = BedrockAgentCoreApp()  # Wraps as HTTP service on port 8080 (/invocations, /ping)
@app.entrypoint
def invoke(payload, context):
    result = graph.invoke({"messages": [("user", payload.get("prompt", ""))]})
    return {"result": result["messages"][-1].content}
app.run()
```

## 命令行接口（CLI）命令
| 命令 | 功能 |
|---------|---------|
| `agentcore configure -e agent.py --region us-east-1` | 进行配置 |
| `agentcore configure -e agent.py --region us-east-1 --name my_agent --non-interactive` | 脚本化配置 |
| `agentcore launch --deployment-type container` | 以容器模式部署 |
| `agentcore launch --disable-memory` | 不使用内存子系统进行部署 |
| `agentcore dev` | 重新加载本地开发服务器 |
| `agentcore invoke '{"prompt": "Hello"}'` | 进行测试 |
| `agentcore destroy` | 清理资源 |

## 核心模式

### 多代理编排
- 编排器将任务分配给各个专业模块（如客户服务、电子商务、医疗保健、金融等） |
- 各专业模块可以是内联函数，也可以是独立部署的代理；所有模块共享 `session_id` 以保持上下文一致性 |

### 内存管理（STM/LTM）
```python
from bedrock_agentcore.memory import MemoryClient
memory = MemoryClient()
memory.create_event(session_id, actor_id, event_type, payload)  # Store
events = memory.list_events(session_id)  # Retrieve (returns list)
```
- **STM**：用于同一会话内的数据存储 |
- **LTM**：用于跨会话/跨代理的数据存储 |
- 数据写入后约 10 秒内可实现最终一致性

### 网关工具
```bash
python -m bedrock_agentcore.gateway.deploy --stack-name my-agents --region us-east-1
```
```python
from bedrock_agentcore.gateway import GatewayToolClient
gateway = GatewayToolClient()
result = gateway.call("tool_name", param1=value1, param2=value2)
```
- 数据传输方式：本地模拟（fallback Mock）、本地 MCP 服务器、生产环境网关（Lambda/REST/MCP） |
- 部署完成后会自动配置 `BEDROCK_AGENTCORE_GATEWAY_URL`

## 决策树
```
Multiple agents coordinating? → Orchestrator + specialists pattern
Persistent cross-session memory? → AgentCore Memory (not LangGraph checkpoints)
External APIs/Lambda? → AgentCore Gateway
Single agent, simple? → Quick Start above
Complex multi-step logic? → StateGraph + tools_condition + ToolNode
```

## 关键概念
- **AgentCore 运行时**：运行在 8080 端口的 HTTP 服务（处理 `/invocations` 和 `/ping` 请求） |
- **AgentCore 内存**：支持跨会话/跨代理的数据管理 |
- **LangGraph 路由**：使用 `tools_condition` 进行代理到工具的路由，`ToolNode` 负责执行 |
- **AgentCore 网关**：将 API/Lambda 请求转换为带有身份验证功能的 MCP 工具

## 命名规则
- 名称以字母开头，只能包含字母、数字和下划线，长度不超过 48 个字符（例如：`my_agent`，而非 `my-agent`）

## 故障排除
| 问题 | 解决方案 |
|-------|-----|
| 不支持按需处理请求 | 使用 `us.anthropic.claude-*` 推理配置文件 |
- 未提交模型使用场景详情 | 在 Bedrock 控制台中填写相关信息 |
- 代理名称无效 | 使用下划线而非连字符 |
- 写入数据后内存为空 | 等待约 10 秒（数据达到最终一致性） |
- 容器无法读取 `.env` 文件 | 需在 Dockerfile 中设置环境变量，而非依赖 `.env` 文件 |
- 部署后内存功能失效 | 查看日志以确认内存是否已启用 |
- `list_events` 返回空结果 | 确保 `actor_id` 与 `session_id` 匹配；`event['payload']` 必须是列表格式 |
- 网关提示“未知工具” | Lambda 需从 `bedrockAgentCoreToolName` 中删除前缀 “___” |
- 平台不匹配警告 | 正常现象——CodeBuild 支持 ARM64 平台之间的构建

## 参考资料
- [agentcore-cli.md](references/agentcore-cli.md)：命令行接口、部署流程、生命周期管理 |
- [agentcore-runtime.md](references/agentcore-runtime.md)：流式处理、异步操作、可观测性相关内容 |
- [agentcore-memory.md](references/agentcore-memory.md)：内存管理机制（STM/LTM）、API 参考 |
- [agentcore-gateway.md](references/agentcore-gateway.md)：工具集成、MCP、Lambda 的使用 |
- [langgraph-patterns.md](references/langgraph-patterns.md)：状态图设计、路由规则 |
- [reference-architecture-advertising-agents-use-case.pdf](references/reference-architecture-advertising-agents-use-case.pdf)：多代理系统架构示例