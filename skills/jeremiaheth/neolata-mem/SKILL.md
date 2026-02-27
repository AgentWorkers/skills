---
name: neolata-mem
version: 0.8.4
description: 专为AI代理设计的图形化内存引擎——支持混合向量搜索与关键词搜索功能，具备生物衰减模型、Zettelkasten链接机制、基于信任度的冲突解决机制，以及数据可解释性功能。同时支持数据压缩与整合。完全无需依赖任何第三方库或服务，只需通过`npm install`即可立即使用。
metadata:
  openclaw:
    requires:
      bins:
        - node
    optionalEnv:
      - OPENAI_API_KEY           # For OpenAI embeddings/extraction (read by code)
      - OPENCLAW_GATEWAY_TOKEN   # For OpenClaw LLM gateway routing (read by code)
      - NVIDIA_API_KEY           # For NVIDIA NIM embeddings (passed via config)
      - AZURE_API_KEY            # For Azure OpenAI embeddings (passed via config)
      - SUPABASE_URL             # For Supabase storage backend (passed via config)
      - SUPABASE_KEY             # Supabase anon key — prefer over service key (passed via config)
    dataFlow:
      local:
        - "Default: JSON files in ./neolata-mem-data/ (configurable dir)"
        - "In-memory mode: storage.type='memory' — nothing written to disk"
      remote:
        - "Supabase: if storage.type='supabase', memories are stored/read from your Supabase project"
        - "Embeddings: if configured, text is sent to OpenAI/NVIDIA/Azure/Ollama for vectorization"
        - "LLM: if configured, text sent to OpenAI/OpenClaw/Ollama for extraction/compression/evolution"
        - "Webhooks: if webhookWritethrough is enabled, each store event POSTs to the configured URL"
      note: "No data leaves the host unless you explicitly configure a remote backend, embedding provider, LLM, or webhook. Default config is fully local (JSON storage + no embeddings)."
    securityNotes:
      - "Prefer Supabase anon key + RLS over service key — service key bypasses row-level security"
      - "Webhook URLs are an explicit exfiltration surface — only configure trusted endpoints"
      - "Test with storage.type='memory' first to evaluate without persisting any data"
      - "All env vars except OPENAI_API_KEY and OPENCLAW_GATEWAY_TOKEN are passed via config objects, not read from env directly"
    license: Elastic-2.0
    homepage: https://github.com/Jeremiaheth/neolata-mem
    repository: https://github.com/Jeremiaheth/neolata-mem
---
# neolata-mem — 代理内存引擎

专为AI代理设计的图形化内存引擎，支持混合搜索、数据衰减功能，并且完全无需依赖任何外部基础设施。

**npm包:** `@jeremiaheth/neolata-mem`  
**仓库:** [github.com/Jeremiaheth/neolata-mem](https://github.com/Jeremiaheth/neolata-mem)  
**许可证:** Elastic-2.0  
**测试覆盖率:** 367/367（34个文件全部通过）  
**兼容Node.js版本:** ≥18

## 适用场景

在以下情况下使用neolata-mem：
- 需要**跨会话的持久化内存**，且该内存能够在上下文压缩后仍然保持完整；
- 需要对存储的事实、决策和发现结果进行**语义搜索**；
- 需要实现**数据衰减机制**，使过时信息自动失效；
- 需要支持**多代理间的内存共享**以及代理间的数据链接；
- 需要处理**数据冲突**，检测并解决矛盾信息。

**不适用场景**：
- 仅需要OpenClaw内置的`memorySearch`功能（基于工作区文件中的关键词和向量进行搜索）；
- 需要使用云托管的内存服务（请使用Mem0）；
- 需要完整的知识图谱数据库（建议使用Graphiti和Neo4j）。

## 安装方法

```bash
npm install @jeremiaheth/neolata-mem
```

**注意：** 该工具不依赖Docker、Python或Neo4j，也不需要任何云API。

**供应链验证：**  
该包没有任何运行时依赖项，也没有安装脚本。安装前请进行以下验证：
```bash
# 检查是否有安装脚本（应仅显示“test”）
npm view @jeremiaheth/neolata-mem scripts
# 检查是否有运行时依赖项（应为空）
npm view @jeremiaheth/neolata-mem dependencies
# 查看tarball文件内容（15个文件，约40KB）
npm pack @jeremiaheth/neolata-mem --dry-run
```
**源代码可在此处查看：** [github.com/Jeremiaheth/neolata-mem](https://github.com/Jeremiaheth/neolata-mem)

## 安全性与数据流

**默认配置** 为完全本地化模式：数据存储在磁盘上的JSON文件中，不进行网络请求，也不使用外部服务。

只有当您**明确配置**以下功能时，数据才会离开本地服务器：
| 功能 | 数据传输内容 | 传输目标 | 避免方法 |
|---------|------------|---------------|-------------|
| 嵌入（OpenAI/NVIDIA/Azure） | 内存中的文本数据 | 嵌入API端点 | 使用`noop`嵌入或本地Ollama服务 |
| LLM（OpenAI/OpenClaw/Ollama） | 用于提取/压缩的内存文本数据 | LLM API端点 | 不要配置`llm`选项，或使用Ollama服务 |
| Supabase存储 | 所有内存数据 | 您的Supabase项目 | 使用`json`或`memory`存储方式（默认） |
| Webhook事件传输 | 存储/衰减事件的数据内容 | 您的Webhook地址 | 不要配置`webhookWritethrough`选项 |

**关键安全特性：**
- 代码仅直接读取两个环境变量：`OPENAI_API_KEY`和`OPENCLAW_GATEWAY_TOKEN`。其他所有配置项（如Supabase、NVIDIA、Azure）均通过配置对象传递。
- 所有服务提供商的URL均经过SSRF验证（阻止访问私有IP地址和云服务元数据）。
- Supabase建议使用匿名密钥和行级安全（RLS）机制，而非服务密钥（服务密钥可能会绕过安全限制）。
- JSON存储采用原子写操作（临时文件 + 重命名）以防止数据损坏。
- 发送给LLM的所有用户数据均经过XML封装处理，以防止注入攻击。
- 可通过`storage: { type: 'memory' }`安全地进行测试——确保数据不会写入磁盘或网络。

详细的安全模型请参阅`docs/guide.md`。

## 快速入门（无需配置）

```javascript
import { createMemory } from '@jeremiaheth/neolata-mem';
const mem = createMemory();
await mem.store('agent-1', '用户偏好暗模式');
const results = await mem.search('agent-1', 'UI偏好');
```

该工具支持本地JSON存储和关键词搜索，无需任何API密钥。

## 支持语义搜索

```javascript
const mem = createMemory({
  embeddings: {
    type: 'openai',
    apiKey: process.env.OPENAI_API_KEY,
    model: 'text-embedding-3-small',
  },
});
// 代理ID（如'kuro'和'maki'仅为示例，可使用任意字符串）
await mem.store('kuro', '在登录表单中发现XSS漏洞', { category: 'finding', importance: 0.9 });
const results = await mem.search('kuro', '安全漏洞');
```

**支持的嵌入服务提供商：** OpenAI、NVIDIA NIM、Ollama、Azure、Together或任何兼容OpenAI的API。

## 主要特性

### 混合搜索（嵌入 + 关键词搜索）

当配置了嵌入模型时，使用语义相似度进行搜索；如果没有嵌入模型，则使用分词后的关键词进行匹配：
```javascript
// 使用嵌入模型时 → 基于向量余弦相似度的搜索
// 不使用嵌入模型时 → 基于标准化关键词的匹配（去除停用词、转换为小写、去重）
const results = await mem.search('agent', '安全漏洞');
```

关键词搜索使用倒排索引实现O(1)级别的快速查找。当存在500条以上记忆记录时，系统会先通过关键词匹配筛选候选记录，再使用向量相似度进行进一步筛选。

### 数据衰减

除非主动更新，否则记忆记录会随时间逐渐失效。过时且未被访问的记忆会自动失去相关性：
```javascript
await mem.decay();        // 运行维护操作，归档/删除过时的记忆记录
await mem.reinforce(id);  // 提升记忆记录的可靠性，防止其被遗忘
```

### 内存图谱（Zettelkasten链接）

系统会自动根据语义相似性将记忆记录相互关联：
```javascript
const links = await mem-links(memoryId);     // 获取记忆记录之间的直接链接
const path = await mem.path(idA, idB);       // 获取记忆记录之间的最短路径
const clusters = await mem.clusters();        // 检测主题簇
```

### 冲突解决与隔离

在存储数据前会检测矛盾之处，可通过结构化检测或基于LLM的语义检测来识别矛盾：
```javascript
// 结构化检测（无需LLM）：基于声明的冲突检测
await mem.store('agent', '服务器使用端口443', {
  claim: { subject: 'server', predicate: 'port', value: '443' },
  provenance: { source: 'user_explicit', trust: 1.0 },
  onConflict: 'quarantine',  // 低信任度的冲突记录会被隔离以供审查
});
// 语义检测（需要LLM）：LLM会判断记录是冲突、需要更新还是新信息
await mem.evolve('agent', '服务器现在使用端口8080');
```

### 谓词模式配置

允许自定义用于处理冲突、数据规范化和去重的规则：
```javascript
const mem = createMemory({
  predicateSchemas: {
    'preferred_language': { cardinality: 'single', conflictPolicy: 'supersede', normalize: 'lowercase_trim' },
    'spoken_languages':   { cardinality: 'multi', dedupPolicy: 'corroborate' },
    'salary':             { cardinality: 'single', conflictPolicy: 'require_review', normalize: 'currency' },
  },
});
```

**可选配置：**
- `cardinality`（单值/多值）
- `conflictPolicy`（替换/需要审核/保留两者）
- `normalize`（不处理/转换为小写/转换为小写并去除空格/转换为货币格式）
- `dedupPolicy`（去重/保留/存储）

### 可解释性API

可以了解搜索结果或筛选结果的具体原因：
```javascript
const results = await mem.search('agent', 'query', { explain: true });
console.log(results.meta);        // 查询参数和结果数量
console.log(results[0].explain);  // 获取结果详情、重新排序信息及状态过滤信息
const detail = await mem.explainMemory(memoryId);  // 获取记忆记录的详细信息
```

### 多代理支持

```javascript
await mem.store('kuro', '在API网关中发现漏洞');
await mem.store('maki', 'API网关已部署到生产环境');
const all = await mem.searchAll('API网关');  // 进行跨代理搜索
```

### 时间序列分组

可以将相关记忆记录分组到指定的时间序列中：
```javascript
const ep = await mem.createEpisode('部署v2.0', [id1, id2, id3], { tags: ['deploy'] });
const ep2 = await mem.captureEpisode('kuro', '站立会议', { start: '...", end: '...' });
const results = await mem.searchEpisode(ep.id, '数据库迁移');
const { summary } = await mem.summarizeEpisode(ep.id);  // 需要LLM支持
```

### 数据压缩与整合

可以将冗余的记忆记录整合为摘要：
```javascript
await mem.compress([id1, id2, id3], { method: 'llm', archiveOriginals: true });
await mem.compressEpisode(episodeId);
await mem.autoCompress({ minClusterSize: 3, maxDigests: 5 });
// 完整维护流程：去重 → 冲突检测 → 核实 → 压缩 → 删除
await mem.consolidate({ dedupThreshold: 0.95, compressAge: 30, pruneAge: 90 });
```

### 带标签的簇

可以创建具有名称的簇结构：
```javascript
await mem.createCluster('安全发现', [id1, id2]);
await mem.autoLabelClusters();  // 使用LLM为簇添加标签
```

### 事件监听

可以监听内存操作的生命周期：
```javascript
mem.on('store', ({ agent, content, id }) => { /* ... */ });
mem.on('search', ({ agent, query, results }) => { /* ... */ });
mem.on('decay', ({ archived, deleted, dryRun }) => { /* ... */ });
```

### 批量操作

可以通过批量操作来优化嵌入调用和I/O性能：
```bash
// 一次性存储多个记忆记录
const result = await mem.storeMany('agent', [
  { text: '事实一', category: '事实', importance: 0.8 },
  { text: '事实二', tags: ['基础设施'] },
  // ... },
]);
// 结果：{ total: 3, stored: 3, results: [{ id, links }, ... }
// 一次性搜索多个查询
const results = await mem.searchMany('agent', ['查询一', '查询二']);
// 结果：{ query: '查询一', results: [...] }, { query: '查询二', results: [...] }
```

批量操作包括：
- 在存储失败时进行原子级回滚（所有记忆记录、索引和链接都会被恢复）
- 在同一批次内实现链接操作
- 可配置参数：`maxBatchSize`（默认1000）、`maxQueryBatchSize`（默认100）

### 基于LLM的事实提取

可以使用LLM从文本中提取关键信息，然后通过A-MEM进行存储：
```javascript
const mem = createMemory({
  embeddings: { type: 'openai', apiKey: process.env.OPENAI_API_KEY },
  extraction: { type: 'llm', apiKey: process.env.OPENAI_API_KEY },
});
const result = await mem.ingest('agent', longText);
// 结果：{ total: 12, stored: 10, results: [...] }
```

## 命令行接口（CLI）

```bash
npx neolata-mem store myagent "重要事实"
npx neolata-mem search myagent "查询"
npx neolata-mem decay --dry-run
npx neolata-mem health
npx neolata-mem clusters
```

## 与OpenClaw的集成

neolata-mem补充了OpenClaw内置的`memorySearch`功能：
- `memorySearch`：用于搜索工作区中的`.md`文件（基于BM25模型和向量计算）
- `neolata-mem`：提供结构化的内存存储服务，支持数据衰减、记忆记录的更新和多代理间的数据共享

建议同时使用这两种工具：`memorySearch`用于检索工作区文件内容，`neolata-mem`用于管理代理间的知识库。

### 推荐使用方式

在代理的日常任务脚本或心跳任务中执行以下操作：
```javascript
// 存储当天的关键决策
await mem.store(agentId, '关键决策：已迁移到Postgres', {
  category: '决策',
  importance: 0.8,
  tags: ['基础设施'],
});
// 运行数据衰减维护
await mem.decay();
```

## 对比分析

| 功能        | neolata-mem    | Mem0       | OpenClaw memorySearch |
|------------|-----------:|:------------:|:---------------------:|
| 优先使用本地数据   | ✅          | ❌          | ✅          |
| 混合搜索（嵌入 + 关键词） | ✅          | ❌          | ✅          |
| 数据衰减功能    | ✅          | ❌          | ❌          |
| 内存图谱/链接    | ✅          | ❌          | ❌          |
| 冲突解决      | ✅          | 部分支持      | ❌          |
| 冲突隔离机制    | ✅          | ❌          | ❌          |
| 谓词模式配置    | ✅          | ❌          | ❌          |
| 可解释性API    | ✅          | ❌          | ❌          |
| 时间序列管理   | ✅          | ❌          | ❌          |
| 带标签的簇     | ✅          | ❌          | ❌          |
| 多代理支持    | ✅          | ✅          | （每个代理独立存储）   |
| 无需外部基础设施 | ✅          | ❌          | ✅          |
| 事件监听     | ✅          | ❌          | ❌          |
| 批量操作     | ✅          | ❌          | ✅          |

## 安全性

neolata-mem具备多种安全防护机制，防止常见的代理内存攻击：
- 对用户输入内容进行XML封装处理，防止注入攻击；
- 对代理名称（仅允许字母数字字符，长度限制为64个字符）、文本长度（最多10KB）和记忆记录数量（最多50条）进行严格验证；
- 批量操作失败时，会原子级地恢复所有记忆记录、索引和链接；
- 通过`validateBaseUrl()`验证所有服务提供商的URL，阻止访问私有IP地址和特定协议；
- 对Supabase的查询参数进行验证，对错误信息进行处理；
- 采用原子写操作（临时文件 + 重命名）防止文件损坏；
- 对存储路径进行严格检查；
- 使用`crypto.randomUUID()`生成随机ID，避免内存引用被预测；
- 实现指数级重试机制，最多尝试3次；
- 在检测到冲突时，会返回错误信息而非直接忽略错误。

**关于Supabase密钥的使用建议：** 建议使用匿名密钥和行级安全（RLS）机制，而非服务密钥（服务密钥可能会绕过安全限制）。仅将服务密钥用于管理员或数据迁移操作。

更多安全细节请参阅`docs/guide.md#security`。

## 数据存储与外部API使用

**默认设置**：所有数据仅存储在本地（`./neolata-mem-data/graph.json`文件中）。关键词搜索无需任何API密钥。

**使用嵌入/提取/LLM功能时**：如果配置了外部服务（如OpenAI、NIM、Ollama等），系统会将内存中的文本数据发送到相应服务的API进行嵌入或提取。这些功能为可选配置，必须提供API密钥和基础URL。

| 模式          | 数据是否传输到外部？ | 存储位置         |
|------------------|------------------|------------------|
| 默认（未配置）       | ❌           | `./neolata-mem-data/graph.json` |
| Ollama嵌入       | ❌           | 不传输（数据存储在本地）     |
| OpenAI/NIM嵌入     | ⚠️ 数据传输至Ollama服务 | `./neolata-mem-data/graph.json` |
| Supabase存储     | ⚠️ 所有数据传输至Supabase数据库 | Supabase PostgreSQL |

**保持数据本地化**：建议使用Ollama进行嵌入处理，并使用JSON格式存储数据。仅进行关键词搜索时无需API密钥。

## 其他资源链接**

- **npm包页面：** [@jeremiaheth/neolata-mem](https://www.npmjs.com/package/@jeremiaheth/neolata-mem)  
- **GitHub仓库：** [Jeremiaheth/neolata-mem](https://github.com/Jeremiaheth/neolata-mem)  
- **完整文档：** 请参阅包内的`docs/guide.md`文件