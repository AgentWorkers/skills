---
name: chaos-memory
description: 用于AI代理的混合搜索内存系统：支持手动搜索和存储功能，自动捕获功能为可选（仅需用户主动启用）。
homepage: https://github.com/hargabyte/Chaos-mind
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "install":
          [
            {
              "id": "chaos-install",
              "kind": "shell",
              "command": "bash install.sh",
              "label": "Install CHAOS Memory",
            },
          ],
      },
  }
---

# CHAOS Memory

**上下文感知的、分层式的、自主的观察系统**

这是一个专为AI代理设计的混合搜索记忆系统，支持4种检索方式：
- **BM25**：关键词匹配  
- **向量**：语义相似性  
- **图谱**：表示记忆内容之间的关联关系  
- **访问频率**：根据访问模式和优先级来筛选记忆内容  

---

## 🤖 如何使用该工具（针对AI代理）  

**首次使用？** 运行以下命令查看完整的使用指南：  
```bash
chaos-cli --help
```  

**快速操作流程：**  
1. **任务开始前**：`chaos-cli search "关键词" --mode index --limit 10`  
2. **任务进行中**：`chaos-cli store "重要事实" --category decision --priority 0.9`  
3. **任务结束后**：`chaos-cli list 10`  

**节省令牌**：使用`--mode index`模式可节省90%的令牌使用量（每条结果大约节省75个令牌）。  

**更多帮助？** 运行`chaos help-agents`以获取针对AI代理的优化使用指南。  

---

## 快速入门  

安装完成后，使用`chaos-cli`即可开始使用：  
```bash
# Search memories
chaos-cli search "pricing decisions" --limit 5

# Store a memory
chaos-cli store "Enterprise tier: $99/month" --category decision

# List recent
chaos-cli list 10
```  

---

## 搜索记忆内容  

- **快速搜索**（摘要模式）：  
```bash
chaos-cli search "architecture patterns" --mode summary --limit 5
```  
- **快速扫描**（索引模式，节省90%令牌）：  
```bash
chaos-cli search "team decisions" --mode index --limit 10
```  
- **详细信息**：  
```bash
chaos-cli search "model selection" --mode full --limit 3
```  

**模式说明：**  
| 模式 | 令牌消耗/结果数量 | 使用场景 |  
|------|---------------|----------|  
| index | 约75个令牌 | 快速扫描，返回大量结果 |  
| summary | 约250个令牌 | 平衡性较好的搜索方式（默认） |  
| full | 约750个令牌 | 详细信息查询 |  

---

## 存储记忆内容  

记忆内容可按以下类别进行分类：  
- decision（决策）  
- core（核心）  
- semantic（语义）  
- research（研究相关）  

**优先级**：0.0–1.0（数值越高，表示内容越重要）  

---

## 通过ID查询记忆内容  

```bash
chaos-cli get <memory-id>
```  

---

## 列出最近访问的记忆内容  

```bash
chaos-cli list        # Default 10
chaos-cli list 20     # Show 20
```  

---

## 自动捕获功能（可选，需手动启用）  

**⚠️ 为保护隐私，默认情况下此功能是关闭的。**  
若要启用自动捕获功能，请按照以下步骤操作：  
1. 了解隐私相关设置（会读取您的会话记录）  
2. 打开配置文件：`nano ~/.chaos/config/consolidator.yaml`  
3. 设置`auto_capture.enabled`为`true`  
4. 在`auto_capture.sources`中添加您的会话目录路径  
5. 安装Ollama模型（如果尚未安装）：`https://ollama.com`  
6. 下载模型：`ollama pull qwen3:1.7b`  
7. 测试自动捕获功能：`chaos-consolidator --auto-capture --once`  

**自动捕获功能会提取哪些内容？**  
- 决策内容、重要事实、相关见解  
**哪些内容会被忽略？**  
- 问候语、填充性文本、无关信息  

**运行方式：**  
- 100%在本地处理（不使用任何外部API）  
**处理速度：** 每条消息处理耗时约2.6秒（16条消息的会话处理耗时约42秒）  

**隐私保护：**  
- 仅处理您明确配置的文件。详情请参阅SECURITY.md文件。  

---

## 🔗 高级功能  

CHAOS Memory支持与其他工具集成，以提升智能处理能力：  

### Cortex（cx）——语义代码锚定功能  

**功能说明：**  
将记忆内容与具体的代码位置或文件关联起来。  
**使用理由：** 使记忆内容具有上下文关联性（例如：“该决策影响了Auth.tsx文件的第45-67行”。  

**工作原理：**  
- 启动时检测是否安装了Cortex；  
- 自动创建记忆内容与代码位置之间的语义链接；  
- 搜索结果会包含相关的代码片段。  

**安装Cortex：**  
```bash
# Cortex is a separate tool
# Install from: https://github.com/hargabyte/cortex
```  
**使用示例：**  
```bash
# Without Cortex
chaos-cli search "auth flow"
→ "Changed auth to use JWT tokens"

# With Cortex
chaos-cli search "auth flow"
→ "Changed auth to use JWT tokens"
→ 📍 Auth.tsx:45-67, middleware/auth.js:12
```  

### Beads——任务关联功能  

**功能说明：**  
将记忆内容与具体任务或问题关联起来，便于追踪记忆内容与实际操作之间的关联。  
**使用理由：** 可追踪哪些记忆内容导致了哪些任务或决策的生成。  

**工作原理：**  
- 启动时检测是否安装了Beads或Beads-rust工具；  
- 自动建立记忆内容与任务之间的双向链接；  
- 记忆内容可自动引用相关问题的ID。  

**安装Beads：**  
```bash
# Beads is a separate task management tool
# Install from: https://github.com/hargabyte/beads
```  
**使用示例：**  
```bash
# Store memory with task reference
chaos-cli store "Need to refactor auth" --category decision --task AUTH-123

# Search shows related tasks
chaos-cli search "auth refactor"
→ "Need to refactor auth"
→ 📋 Task: AUTH-123 (In Progress)
```  

### 三款工具协同使用效果  

当**Cortex、Beads和CHAOS Memory**三款工具同时使用时，可大幅提升信息处理效率：  
```bash
chaos-cli search "performance optimization"
→ Memory: "Added Redis caching layer"
→ 📍 Code: cache/redis.js:34-89
→ 📋 Task: PERF-042 (Completed)
→ 🔗 Related: 3 other memories, 2 code files, 1 PR
```  

**状态检测：**  
- Cortex：启动时会自动检测到并记录日志（`[OPT] Cortex Engine: FOUND`）  
- Beads：启动时会自动检测到并记录日志（`[OPT] Beads Task Manager: FOUND`）  
- 查看状态：运行`chaos-mcp`命令可查看详细日志。  

---

## 配置设置  

默认配置文件位置：`~/.chaos/config/consolidator.yaml`  
```yaml
# Auto-capture is DISABLED by default
auto_capture:
  enabled: false  # Change to true after configuring paths
  sources: []     # Add your session paths here
  
# Example (uncomment after reviewing):
# sources:
#   - ~/.openclaw-*/agents/*/sessions/*.jsonl

qwen:
  model: qwen3:1.7b  # Locked default

chaos:
  mode: mcp
  mcp:
    env:
      CHAOS_DB_PATH: "~/.chaos/db"
```  

---

## 环境变量设置  

| 变量 | 默认值 | 说明 |  
|----------|---------|-------------|  
| `CHAOS_HOME` | `~/.chaos` | 安装目录 |  
| `CHAOS_DB_PORT` | `3307` | 数据库端口 |  
| `CHAOS_MODEL` | `qwen3:1.7b` | 使用的模型版本 |  

---

**系统要求：**  
- **Dolt**：用于版本控制的数据库工具  
- **Ollama**：用于本地大语言模型推理（支持自动捕获功能）  
- **Go 1.21及以上版本**：用于从源代码编译（可选）  

安装脚本会自动处理所有依赖关系。  

---

## 常见问题及解决方法：  
- **命令未找到**：请检查命令是否正确输入。  
- **数据库错误**：检查数据库连接是否正常。  
- **无结果**：可能是因为搜索条件不匹配或数据库未找到相关数据。  

---

## 安全性与隐私保护：  
- **数据存储**：所有记忆内容均存储在本地（`~/.chaos/db`）  
- 无数据同步或外部传输行为  
- 数据不会离开您的计算机  
- 数据库采用Dolt版本控制工具进行管理，便于审计  

**自动捕获功能（需手动配置）：**  
- 默认情况下此功能是关闭的；  
- 需在`~/.chaos/config/consolidator.yaml`中配置会话路径；  
- 仅处理您在`auto_capture_sources`中指定的文件；  
- 使用您自己的Ollama实例进行本地处理（不使用外部API）。  

**权限设置：**  
- **读取权限**：仅访问您配置的会话记录文件；  
- **写入权限**：仅写入本地数据库（`~/.chaos/db`）；  
- **网络权限**：无网络请求（所有处理均在本地完成）。  

**透明度说明：**  
- 安装脚本源代码可在仓库中获取（`install.sh`）；  
- 所有二进制文件均通过GitHub Actions构建（可重现安装过程）；  
- 数据库使用Dolt进行管理（可通过`dolt sql`查询）。  

---

## 相关链接：  
- **GitHub仓库**：https://github.com/hargabyte/Chaos-mind  
- **官方文档**：https://github.com/hargabyte/Chaos-mind/blob/main/README.md  
- **问题反馈**：https://github.com/hargabyte/Chaos-mind/issues  

**版本信息：**  
**版本1.0.0 | 由HSA团队开发**