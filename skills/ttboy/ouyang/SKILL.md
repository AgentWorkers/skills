---
name: jasper-recall
description: 本地RAG（Retrieval-Augmentation-Generation）系统，用于管理代理的内存数据，该系统基于ChromaDB和sentence-transformers技术实现。它支持对会话日志、每日笔记以及内存文件进行语义搜索。当您需要跨会话保存数据、检索过去的对话内容，或构建能够记住上下文的代理时，可以使用该系统。可用命令包括：recall（查询）、index-digests（索引生成）、digest-sessions（会话摘要生成）。
---

# Jasper Recall

这是一个用于AI代理记忆的本地RAG（Retrieval-Augmented Generation，检索增强生成）系统，它使您的代理能够记住并搜索之前的对话内容。

## 使用场景

- **记忆检索**：在回答问题之前，从过去的会话中搜索相关上下文。
- **持续学习**：索引每日笔记和决策，以供将来参考。
- **会话连续性**：在重启后仍能记住发生的事情。
- **知识库**：从代理的经验中构建可搜索的文档。

## 快速入门

### 设置

只需一个命令即可完成全部安装：
```bash
npx jasper-recall setup
```

安装完成后会创建以下内容：
- 在`~/.openclaw/rag-env`目录下创建一个Python虚拟环境。
- 在`~/.openclaw/chroma-db`目录下创建一个ChromaDB数据库。
- 在`~/.local/bin/`目录下生成CLI脚本。

### 基本用法

- **搜索记忆**：
```bash
recall "what did we decide about the API design"
recall "hopeIDS patterns" --limit 10
recall "meeting notes" --json
```

- **索引文件**：
```bash
index-digests  # Index memory files into ChromaDB
```

- **创建会话摘要**：
```bash
digest-sessions          # Process new sessions
digest-sessions --dry-run  # Preview what would be processed
```

## 工作原理

Jasper Recall由三个主要组件构成：

1. **digest-sessions**：从会话日志中提取关键信息（主题、使用的工具等）。
2. **index-digests**：将这些信息分割成小块，并将其嵌入到ChromaDB数据库中。
3. **recall**：对索引后的记忆内容进行语义搜索。

### 被索引的文件

默认情况下，以下文件会被索引：
- `~/.openclaw/workspace/memory/`目录下的文件：
  - `*.md`：每日笔记
  - `session-digests/*.md`：会话摘要
  - `repos/*.md`：项目文档
  - `founder-logs/*.md`：开发日志（如果存在）

### 嵌入模型

Jasper Recall使用`sentence-transformers/all-MiniLM-L6-v2`模型进行文本嵌入：
- 模型维度为384维。
- 首次运行时需要下载约80MB的数据。
- 该模型在本地运行，无需API支持。

## 代理集成

Jasper Recall可以用于增强代理的响应能力，使其能够基于记忆提供更准确的回答。

### 自动化索引（Heartbeat）

将相关配置添加到`HEARTBEAT.md`文件中：
```markdown
## Memory Maintenance
- [ ] New session logs? → `digest-sessions`
- [ ] Memory files updated? → `index-digests`
```

### 定时任务

使用Cron作业来定期执行索引任务：
```json
{
  "schedule": { "kind": "cron", "expr": "0 */6 * * *" },
  "payload": {
    "kind": "agentTurn",
    "message": "Run index-digests to update the memory index"
  },
  "sessionTarget": "isolated"
}
```

## CLI参考

- **recall**：用于执行记忆检索的CLI命令。
- **index-digests**：用于索引文件的CLI命令。
- **digest-sessions**：用于生成会话摘要的CLI命令。

## 配置

- **自定义路径**：可以通过设置环境变量来修改文件的存储路径。

### 分块设置

`index-digests`组件的默认设置如下：
- 分块大小：500个字符。
- 分块之间的重叠部分：100个字符。

## 常见问题与解决方法

- **“未找到索引”**：请检查文件是否已正确添加到索引中。
- **“集合未找到”**：可能是文件路径错误或文件已被删除。
- **模型下载缓慢**：首次运行时需要下载大量数据，后续运行则很快。

## 链接

- **GitHub仓库**：https://github.com/E-x-O-Entertainment-Studios-Inc/jasper-recall
- **npm包**：https://www.npmjs.com/package/jasper-recall
- **ClawHub文档**：https://clawhub.ai/skills/jasper-recall