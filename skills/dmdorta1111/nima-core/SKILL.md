---
name: nima-core
description: 神经集成内存架构（Neural Integrated Memory Architecture）：一种基于图谱的数据存储系统，结合了LadybugDB数据存储引擎、语义搜索功能以及动态情感分析（dynamic affect）和惰性数据检索（lazy recall）技术。该架构已准备好用于人工智能代理（AI agents）的实际应用。欲了解更多信息，请访问nima-core.ai。
version: 2.0.11
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["python3","node"],"env":["NIMA_DATA_DIR"]},"optional_env":{"NIMA_EMBEDDER":"voyage|openai|local (default: local)","VOYAGE_API_KEY":"Required when NIMA_EMBEDDER=voyage","OPENAI_API_KEY":"Required when NIMA_EMBEDDER=openai"},"permissions":{"reads":["~/.openclaw/agents/*/sessions/*.jsonl"],"writes":["~/.nima/"],"network":["voyage.ai (conditional)","openai.com (conditional)"]}}}
---
# NIMA Core 2.0

**Neural Integrated Memory Architecture** — 专为具备情感智能的AI代理设计的完整内存系统。

**官方网站：** https://nima-core.ai  
**GitHub仓库：** https://github.com/lilubot/nima-core  

## 🚀 快速入门  

```bash
# Install
pip install nima-core

# Or with LadybugDB (recommended for production)
pip install nima-core[vector]

# Set embedding provider
export NIMA_EMBEDDER=voyage
export VOYAGE_API_KEY=your-key

# Install hooks
./install.sh --with-ladybug

# Restart OpenClaw
openclaw restart
```  

## 🔒 隐私与权限设置  

**数据访问权限：**  
- ✅ 从 `~/.openclaw/agents/*/sessions/*.jsonl` 文件中读取会话记录。  
- ✅ 将数据写入 `~/.nima/` 目录下的本地存储（包括数据库、情感历史记录和嵌入数据）。  

**网络调用（取决于所使用的嵌入器）：**  
- 🌐 **Voyage API** — 仅当 `NIMA_EMBEDDER` 设置为 `voyage` 时使用（用于发送文本以获取嵌入数据）。  
- 🌐 **OpenAI API** — 仅当 `NIMA_EMBEDDER` 设置为 `openai` 时使用（用于发送文本以获取嵌入数据）。  
- 🔒 **本地嵌入** — 默认设置（`NIMA_EMBEDDER=local`），不进行外部API调用。  

**可选配置：**  
```json
// openclaw.json
{
  "plugins": {
    "entries": {
      "nima-memory": {
        "enabled": true,
        "skip_subagents": true,      // Exclude subagent sessions (default)
        "skip_heartbeats": true,      // Exclude heartbeat checks (default)
        "noise_filtering": {
          "filter_heartbeat_mechanics": true,
          "filter_system_noise": true
        }
      }
    }
  }
}
```  

**隐私默认设置：**  
- 不包括子代理的会话记录。  
- 过滤掉不必要的系统数据。  
- 使用本地嵌入数据（不进行外部API调用）。  
- 所有数据均存储在本地。  

**如需禁用该插件，请从 `openclaw.json` 文件中的 `plugins.allow` 列表中移除 `nima-memory`。**  

## 2.0版本的新增功能  

### LadybugDB后端  
- **文本搜索速度提升3.4倍**（从31ms缩短至9ms）。  
- **支持HNSW算法的本地向量搜索**（搜索速度提升至18ms）。  
- **数据库大小减少44%**（从91MB缩减至50MB）。  
- **支持使用Cypher查询进行图谱遍历。**  

### 安全性增强：**  
- 对查询内容进行安全处理（防止SQL注入攻击）。  
- 保护路径遍历安全。  
- 清理临时文件。  
- 全程优化错误处理机制。  

### 线程安全性：**  
- 采用双重检查锁机制确保线程安全。  
- API调用超时时间设置：Voyage API为30秒，LadybugDB为10秒。  
- 支持连接池技术。  

### 测试情况：**  
- 完整通过了348项单元测试。  
- 确保了线程安全性。  
- 覆盖了所有可能的边缘情况。  

## 架构概述（略）  

## 性能对比：**  
| 测试指标 | SQLite | LadybugDB |
|--------|--------|-----------|
| 文本搜索 | 31ms | **9ms**（提速3.4倍） |
| 向量搜索 | 外部API | **18ms**（本地算法） |
| 数据库大小 | 91MB | **50MB**（减少44%） |
| 上下文token数量 | 约180个 | **约30个**（减少6倍） |

## API接口（略）  

## 配置选项：**  
| 参数 | 默认值 | 说明 |
|----------|---------|-------------|
| `NIMA_DATA_DIR` | `~/.nima` | 内存存储路径 |
| `NIMA_EMBEDDER` | `voyage` | 可选值：`voyage`、`openai` 或 `local` |
| `VOYAGE_API_KEY` | — | 使用Voyage API时必填 |
| `NIMA_LADYBUG` | `0` | 设置为`1`时使用LadybugDB后端 |

## 插件功能说明：  

### nima-memory（数据捕获模块）：**  
- 在每个代理动作中捕获输入数据、处理过程及输出结果。  
- 将数据存储至SQLite或LadybugDB数据库中，并计算生成嵌入信息。  

### nima-recall-live（回忆模块）：**  
- 在代理启动前加载相关记忆数据。  
- 实现延迟加载机制，仅返回最相关的N条结果。  
- 通过上下文信息消除数据重复。  

### nima-affect（情感处理模块）：**  
- 实时检测文本中的情感信息。  
- 维护Panksepp模型定义的7种情感状态。  
- 调节代理的响应方式。  

## 安装指南：  

### SQLite版本（开发环境）：**  
```bash
pip install nima-core
./install.sh
```  

### LadybugDB版本（生产环境）：**  
```bash
pip install nima-core[vector]
./install.sh --with-ladybug
```  

## 文档资料：**  
- [README.md]：系统概述  
- [SETUP_GUIDE.md]：安装步骤  
- [docs/DATABASE_OPTIONS.md]：SQLite与LadybugDB的比较  
- [docs/EMBEDDING_PROVIDERS.md]：支持的嵌入器（Voyage、OpenAI、本地）  
- [MIGRATION_GUIDE.md]：版本迁移指南  

## 安全性与隐私政策：**  
- 该插件会访问以下文件：  
  - `~/.openclaw/agents/.../*.jsonl`（会话记录文件）  
  - `~/.nima/`（本地数据库文件，支持SQLite或LadybugDB）  
  - `~/.openclawextensions/`（插件安装目录）  

**网络调用说明：**  
- 嵌入数据会发送至以下外部API：  
  - **Voyage AI**（`api.voyageai.com`）：默认嵌入服务提供商  
  - **OpenAI**（`api.openai.com`）：可选的嵌入服务提供商  
  - **本地处理**：使用内置的句子转换器时不会进行外部API调用。  

### 必需的环境变量：**  
- `NIMA_EMBEDDER`：指定嵌入服务的类型（`voyage`、`openai`或`local`，默认为`voyage`）。  
- `VOYAGE_API_KEY`：使用Voyage API时需要输入的认证密钥。  
- `OPENAI_API_KEY`：使用OpenAI API时需要输入的认证密钥。  
- `NIMA_DATA_DIR`：内存存储路径（默认为`~/.nima`）。  
- `NIMA_LADYBUG`：指定是否使用LadybugDB后端（默认值为0）。  

### 安装脚本：**  
`install.sh`脚本会：  
- 检查系统是否安装了Python 3和Node.js。  
- 创建`~/.nima/`目录。  
- 通过pip安装相关Python包。  
- 将插件模块复制至`~/.openclaw/extensions/`目录。  
**所有依赖包均来自PyPI仓库。**  

## 更新日志：**  
### v2.0.3（2026年2月15日）：**  
- **安全性增强：** 修复了`affect_history.py`中的路径遍历漏洞（严重级别）。  
- **安全性改进：** 修复了3个文件中的临时文件泄漏问题。  
- **代码优化：** 更正了错误处理逻辑，提高了错误信息的可见性和可调试性。  

### v2.0.1：**  
- **线程安全性提升：** 采用双重检查锁机制确保线程安全。  
- **安全性增强：** 明确了元数据的使用要求。  
- **文档更新：** 添加了关于API密钥使用的安全说明。  

### v2.0.0：**  
- **新增功能：**  
  - 引入了支持HNSW算法的LadybugDB后端。  
  - 支持使用Cypher进行图谱遍历。  
  - 新增了`nima-query`命令行工具，用于统一查询操作。  
- **安全性改进：** 防止SQL注入和FTS5攻击。  
- **其他安全优化：** 加强了路径遍历保护和临时文件管理。  

### 其他版本更新：**  
- **v1.2.1**：新增了8种意识状态模型和稀疏块VSA内存模型。  
- **v1.1.9**：优化了`nima-recall`模块的线程效率。  
- **v1.2.0**：新增了多层情感处理引擎和异步情感处理功能。