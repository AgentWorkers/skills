---
name: vector-memory
description: 智能内存搜索功能，具备自动向量回退机制。在支持语义嵌入的情况下，会优先使用语义嵌入进行搜索；否则会切换到内置的搜索方式。无需任何配置——安装 ClawHub 后即可立即使用该功能。无需额外设置，只需安装即可，内存搜索功能会立即生效；通过可选的同步操作后，性能会进一步提升。
---

# 向量内存（Vector Memory）

智能内存搜索功能，能够**自动选择最佳搜索方法**：
- **向量搜索**（基于语义理解，搜索质量高）：在数据同步后启用
- **内置搜索**（基于关键词，搜索速度快）：作为备用方案

**无需任何配置**。安装完成后即可立即使用。

## 快速入门

### 从 ClawHub 安装
```bash
npx clawhub install vector-memory
```

安装完成！`memory_search` 现在支持自动选择搜索方法。

### 可选：同步数据以获得更精确的结果
```bash
node vector-memory/smart_memory.js --sync
```

同步数据后，搜索会利用神经嵌入技术进行语义理解。

## 工作原理

### 智能搜索方法选择
```javascript
// Same call, automatic best method
memory_search("James principles values") 

// If vector ready: finds "autonomy, competence, creation" (semantic match)
// If not ready: uses keyword search (fallback)
```

### 动作流程
1. **检查**：向量索引是否已准备好？
2. **如果准备好了**：使用基于语义的搜索（支持同义词和概念搜索）
3. **如果没有**：使用内置的关键词搜索
4. **如果向量搜索失败**：自动切换到内置搜索方式

## 工具

### `memory_search`
**自动选择最佳搜索方法**

参数：
- `query`（字符串）：搜索查询
- `max_results`（整数）：最大返回结果数量（默认值：5）

返回结果：包含文件路径、相关行、匹配分数以及搜索片段

### `memory_get`
用于获取文件的完整内容。

### `memory_sync`
用于同步内存文件以支持向量搜索。建议在文件修改后执行此操作。

### `memory_status`
用于查看当前正在使用的搜索方法。

## 功能对比

| 功能        | 内置搜索（Built-in） | 向量搜索（Vector） | 智能搜索框架（Smart Wrapper） |
|------------|--------------|-----------------|---------------------|
| 支持同义词    | 不支持         | 支持             | 支持（数据同步后）           |
| 设置配置    | 需要手动配置     | 需要数据同步       | 无需配置             |
| 备用方案    | 无            | 需要手动切换       | 自动切换             |

## 使用方法

**立即使用（无需额外操作）：**
```bash
node vector-memory/smart_memory.js --search "query"
```

**同步数据后（搜索质量更佳）：**
```bash
# One-time setup
node vector-memory/smart_memory.js --sync

# Now all searches use vector
node vector-memory/smart_memory.js --search "query"
```

## 文件结构

| 文件名        | 功能        |
|------------|------------|
| `smart_memory.js` | 主程序文件，负责自动选择搜索方法 |
| `vector_memory_local.js` | 向量搜索的实现代码 |
| `memory.js`    | OpenClaw 框架的封装文件 |

## 配置要求

**无需任何配置**。

可选的环境变量：
```bash
export MEMORY_DIR=/path/to/memory
export MEMORY_FILE=/path/to/MEMORY.md
```

## 扩展性

- **数据块数量 < 1000 个**：使用内置搜索和 JSON 格式的数据存储方式
- **数据块数量 > 1000 个**：建议使用 `pgvector`（详见参考文档：`pgvector.md`）

## 参考资料

- [集成指南](references/integration.md)：详细的使用配置方法
- [pgvector](references/pgvector.md)：适用于大规模数据集的部署方案