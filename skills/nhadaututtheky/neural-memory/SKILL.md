# 神经记忆（Neural Memory）

这是一个基于反射机制的AI代理记忆系统——它将经验存储为相互连接的神经元，并通过“扩散激活”（spreading activation）机制来检索这些记忆，从而模拟人脑的工作方式。

## 功能概述  

神经记忆为AI代理提供了跨会话的持久性记忆功能。该系统不采用关键词搜索的方式，而是通过神经网络图（neural graph）来实现记忆的检索；当某个记忆被激活时，与之相关的记忆也会被同时激活。  

## 主要特性：  

- **39种MCP工具**：用于实现持久性记忆与认知推理功能  
- **扩散激活检索**：通过激活相关记忆来获取信息，而非依赖关键词搜索  
- **认知推理**：支持构建假设、收集证据、进行预测以及更新知识结构  
- **知识库训练**：支持从PDF、DOCX、PPTX、HTML、JSON、XLSX、CSV格式的文件中导入数据  
- **多设备同步**：具备智能冲突解决机制，支持跨设备的数据同步  
- **多种嵌入模型支持**：支持Sentence Transformers、Gemini、Ollama、OpenAI等嵌入模型  
- **检索流程**：结合RRF评分、图谱扩展和个人化PageRank算法来优化检索效果  
- **会话管理**：支持主题跟踪、LRU（Least Recently Used）策略下的数据淘汰机制以及自动过期设置  
- **用户界面**：提供包含状态信息、知识图谱、时间线等内容的React仪表板  
- **VS Code扩展**：为VS Code开发了专用扩展，包括状态栏显示、图谱浏览器和代码辅助功能  
- **数据加密**：使用Fernet算法对敏感数据进行加密  
- **版本控制**：支持创建快照、回滚以及数据的导入/导出  
- **备份机制**：支持将记忆数据通过Telegram发送到聊天频道或群组  

## 安装方法：  

```bash
pip install neural-memory
```  

（如需使用嵌入模型，可添加以下参数：）  
```bash
pip install neural-memory[embeddings]
```  

## MCP配置（MCP Configuration）：  

```json
{
  "mcpServers": {
    "neural-memory": {
      "command": "uvx",
      "args": ["--from", "neural-memory", "nmem-mcp"]
    }
  }
}
```  

## 使用方法：  

配置完成后，神经记忆系统会自动开始工作。代理需要执行以下操作：  

1. **会话开始时**：使用 `nmem_recall("current project context")` 来加载之前的会话上下文。  
2. **完成任务后**：使用 `nmem_remember("Chose X over Y because Z")` 来保存决策内容。  
3. **会话结束时**：使用 `nmem_auto(action="process", text="summary")` 来清除会话中的临时数据。  

## 记忆类型（Memory Types）：  

| 类型          | 用途                                      |
|---------------|-----------------------------------------|
| fact           | 稳定的知识内容                              |
| decision       | 表示“因为Z所以选择了X”这样的决策记录             |
| insight        | 发现的模式或规律                              |
| error          | 错误信息及其根本原因                          |
| workflow       | 任务执行的步骤                            |
| preference      | 用户的偏好设置                            |
| instruction     | 需要遵循的规则或指令                          |

## 相关资源：  

- [GitHub仓库](https://github.com/nhadaututtheky/neural-memory)  
- [官方文档](https://nhadaututtheky.github.io/neural-memory)  
- [VS Code扩展](https://marketplace.visualstudio.com/items?itemName=neuralmem.neuralmemory)