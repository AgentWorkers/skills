---
name: jasper-recall
version: 0.3.1
description: 本地RAG（Retrieval-Augmentation System）用于代理内存管理，该系统基于ChromaDB和sentence-transformers框架实现。版本v0.3.0新增了多代理协同工作模式（多个代理共享内存功能）、支持OpenClaw插件（具备自动召回功能）以及代理特定的数据集合管理机制。可用命令包括：recall（召回数据）、index-digests（索引摘要生成）、digest-sessions（会话摘要处理）、privacy-check（隐私性检查）、sync-shared（数据同步共享）、serve（数据提供服务）以及recall-mesh（多代理协同召回功能）。
---

# Jasper Recall v0.2.3

这是一个用于AI代理记忆的本地RAG（Retrieval-Augmented Generation，检索增强生成）系统，它使您的代理能够记住并搜索之前的对话。

**v0.2.2的新功能：**  
- **共享ChromaDB集合**：为私有内容、共享内容和学习内容分别创建不同的集合，从而更好地实现多代理环境下的数据隔离。

**v0.2.1的新功能：**  
- **回忆服务器（Recall Server）**：为无法直接运行CLI命令的Docker隔离代理提供的HTTP API。

**v0.2.0的新功能：**  
- **共享代理记忆（Shared Agent Memory）**：支持主代理与沙箱代理之间的双向数据交换，并提供隐私控制功能。

## 使用场景  

- **记忆检索**：在回答问题前，从历史会话中查找相关信息。  
- **持续学习**：索引每日笔记和决策，以便将来参考。  
- **会话连续性**：在重启后仍能记住发生的事情。  
- **知识库**：根据代理的经验构建可搜索的文档。  

## 快速入门  

### 设置  

只需一个命令即可完成所有安装：  
```bash
npx jasper-recall setup
```  

安装完成后，系统会创建以下内容：  
- 在`~/.openclaw/rag-env`目录下生成Python虚拟环境（venv）。  
- 在`~/.openclaw/chroma-db`目录下创建ChromaDB数据库。  
- 在`~/.local/bin/`目录下生成CLI脚本。  
- 在`openclaw.json`文件中配置OpenClaw插件。  

### 为什么选择Python？  

核心的搜索和嵌入功能依赖于Python库：  
- **ChromaDB**：用于语义搜索的向量数据库。  
- **sentence-transformers**：用于生成本地嵌入模型的工具（无需API）。  
这些库是本地RAG系统的行业标准，目前没有合适的Node.js替代品能够完全离线运行。  

### 为什么需要单独的虚拟环境（venv）？  

`~/.openclaw/rag-env`虚拟环境具有以下优势：  
- **隔离性**：不会与其他Python项目冲突。  
- **无需root权限**：安装到用户主目录，无需管理员权限。  
- **易于卸载**：删除该虚拟环境即可彻底清除所有相关文件。  
- **可重复性**：确保所有环境中的依赖版本一致。  

### 基本用法  

- **搜索记忆**：使用相应命令查询历史会话内容。  
- **索引文件**：对文件进行索引以便快速查找。  
- **创建会话摘要**：生成会话的摘要文件以供后续使用。  

## 工作原理  

Jasper Recall由三个主要组件构成：  
1. **digest-sessions**：从会话日志中提取关键信息（如主题、使用的工具等）。  
2. **index-digests**：将markdown格式的文件分割并嵌入到ChromaDB数据库中。  
3. **recall**：在索引后的数据中进行语义搜索。  

### 被索引的文件  

默认情况下，以下文件会被索引：  
- `~/.openclaw/workspace/memory/`目录下的所有`.md`文件（包括每日笔记、MEMORY.md文件等）。  
- `session-digests`目录下的`.md`文件（会话摘要）。  
- `repos`目录下的`.md`文件（项目文档）。  
- `founder-logs`目录下的`.md`文件（开发日志，如果存在的话）。  

### 嵌入模型  

Jasper Recall使用`sentence-transformers/all-MiniLM-L6-v2`模型：  
- 该模型生成384维的嵌入向量。  
- 首次运行时需要下载约80MB的数据，但后续运行无需重新下载。  
该模型完全在本地运行，无需外部API支持。  

### 代理集成  

Jasper Recall支持基于记忆的智能响应机制。  

### 自动索引（通过HEARTBEAT脚本实现）  

只需在`HEARTBEAT.md`文件中添加相应的配置即可实现自动索引功能。  

### 定时任务  

可以使用Cron作业来定期执行索引任务。  

## 共享代理记忆（v0.2.0及以上版本）  

在多代理环境中，如果沙箱代理需要访问某些记忆数据，可以使用共享代理记忆功能。  

### 记忆文件标记  

可以在每日笔记中为文件添加标签，以便区分不同类型的数据。  

### ChromaDB集合（v0.2.2及以上版本）  

系统支持将记忆数据存储在不同的集合中，以实现数据隔离：  
| 集合 | 用途 | 访问权限 |  
|------------|---------|--------------|  
| `private_memories` | 主代理的私有内容 | 仅主代理可访问 |  
| `shared_memories` | 公共内容 | 沙箱代理可访问 |  
| `agent_learnings` | 所有代理的学习成果 | 所有代理可访问 |  
| `jasper_memory` | 旧版统一存储方式（向后兼容） | 备用选项 |  

**集合选择方式：**  

### 沙箱代理的访问权限设置  

沙箱代理可以通过特定方式访问共享记忆数据。  

### Moltbook代理的配置（v0.4.0及以上版本）  

对于Moltbook-scanner或任何沙箱代理，可以使用内置的配置方式。  

### 隐私保护机制  

- 主代理可以在日常笔记中为记忆数据添加`[public]`或`[private]`标签。  
- `sync-shared`脚本会将标记为`[public]`的内容同步到`memory/shared/`目录。  
- 沙箱代理只能搜索`shared`集合中的内容。  

### 隐私工作流程  

系统通过明确的规则来保护用户隐私。  

## CLI命令参考  

- `recall`：用于执行搜索操作。  
- `serve`（v0.2.1及以上版本）：用于提供API服务。  

**示例（来自Docker容器）：**  

### 隐私检查（v0.2.0及以上版本）  

### 其他相关命令：**  
- `sync-shared`：用于同步共享数据。  
- `index-digests`：用于生成索引文件。  
- `digest-sessions`：用于处理会话日志数据。  

## 配置选项  

- **自定义路径**：可以通过环境变量来修改系统的行为。  

### 索引设置（index-digests）  

- 默认设置：  
  - 分块大小：500个字符。  
  - 分块之间的重叠部分长度：100个字符。  

### 安全注意事项  

**在生产环境中启用这些设置前，请务必仔细检查！**  

- **服务器绑定**：`serve`命令默认绑定到`127.0.0.1`（本地地址）。除非明确需要公开API并采取了相应的安全措施，否则请勿使用`--host 0.0.0.0`。  
- **私有记忆访问**：服务器默认禁止私有访问（`public_only=true`）。请勿在公共或共享环境中启用此设置，否则会暴露私有数据。  
- **autoRecall插件**：当`autoRecall`设置为`true`时，系统会在每条代理消息发送前自动添加记忆数据。请注意配置`publicOnly`参数以控制搜索范围，并使用`minScore`参数过滤低相关性的数据。  

### 更安全的配置方式（适用于不受信任的环境）：  

通过设置环境变量来进一步强化系统安全性。  

### 环境变量  

以下环境变量会影响Jasper Recall的行为，请根据实际需求进行配置：  
- `RECALLWorkspace`：指定记忆文件的存储路径。  
- `RECALL_CHROMA_DB`：指定ChromaDB数据库的路径。  
- `RECALL_SESSIONS_DIR`：指定会话日志的存储路径。  
- `RECALL_ALLOW_PRIVATE`：控制是否允许私有访问。  
- `RECALL_PORT`：指定服务器端口。  
- `RECALL_HOST`：指定服务器的绑定地址。  

### 预先测试  

在正式部署之前，请使用测试选项预览系统的运行效果。  

### 沙箱环境下的使用建议  

为了最大程度地保护数据安全，建议在容器或专用账户中运行Jasper Recall：  
- 这可以降低数据泄露的风险。  
- 将私有记忆数据与公共数据分开存储。  
- 特别适用于包含不受信任代理的多代理环境。  

### 常见问题及解决方法：  
- “未找到索引”：检查文件是否已被正确添加到索引中。  
- “集合未找到”：确认相关文件存在于指定的路径中。  
- 模型下载缓慢：首次运行时需要下载大量数据，后续运行会更快。  

## 资源链接：  
- **GitHub仓库**：https://github.com/E-x-O-Entertainment-Studios-Inc/jasper-recall  
- **npm包**：https://www.npmjs.com/package/jasper-recall  
- **ClawHub文档**：https://clawhub.ai/skills/jasper-recall