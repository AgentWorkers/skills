---
name: memory-lancedb-hybrid
description: LanceDB长期记忆插件：结合BM25与向量混合搜索技术（支持RRF或线性重排序算法）。
---

# LanceDB混合搜索（内存插件）

该插件提供了一个即用的OpenClaw内存插件，可为LanceDB的内存功能添加混合搜索功能：

- **向量搜索**（基于语义理解）
- **BM25全文搜索**（用于精确匹配术语）
- 支持可配置的重新排序算法：
  - `rrf`（互惠排名融合算法，推荐使用）
  - `linear`（基于权重组合的排序算法）

该插件基于OpenClaw的PR **openclaw/openclaw#7636**进行开发，并对其进行了相应的修改和优化。

## 插件内容

该插件是一个本地插件（扩展文件），位于以下路径：
`plugin/`  
该插件会 **覆盖** 内置的`memory-lancedb`插件，从而为LanceDB的内存功能添加混合搜索功能。

启用该插件后，您将可以使用与内置LanceDB内存插件相同的功能：
- `memory_store`  
- `memory_recall`  
- `memory_forget`  

不过，当混合搜索功能被启用时，`memory_recall`、`auto-recall` 和 `forget` 方法将使用混合搜索算法进行数据检索。

## 安装/启用方法

1. 确保`skills/memory-lancedb-hybrid`文件夹存在（ClawHub的安装过程会将其放置在您的工作空间中）：
   - `~/.openclaw/workspace/skills/memory-lancedb-hybrid/plugin`

2. 一次性安装插件所需的依赖项：
   ```bash
cd ~/.openclaw/workspace/skills/memory-lancedb-hybrid/plugin
npm install --omit=dev
```

3. 将该插件添加到OpenClaw的插件加载路径中。由于该插件的ID仍为`memory-lancedb`，因此在通过`plugins.load_paths`加载插件时，它会覆盖内置的`memory-lancedb`插件（优先级更高）。

请编辑`~/.openclaw/openclaw.json`文件以配置插件：
```json5
{
  plugins: {
    load: {
      // Point at the plugin directory inside this skill
      paths: ["~/.openclaw/workspace/skills/memory-lancedb-hybrid/plugin"]
    },

    // Ensure the memory slot points at LanceDB memory
    slots: {
      memory: "memory-lancedb"
    },

    // Configure LanceDB memory (this override adds the `hybrid` config block)
    entries: {
      "memory-lancedb": {
        enabled: true,
        config: {
          embedding: {
            apiKey: "${OPENAI_API_KEY}",
            model: "text-embedding-3-small"
          },

          // Optional
          dbPath: "~/.openclaw/memory/lancedb",

          // Optional
          autoCapture: true,
          autoRecall: true,

          // Hybrid search options
          hybrid: {
            enabled: true,
            reranker: "rrf"

            // If using reranker: "linear", you can also set:
            // vectorWeight: 0.7,
            // textWeight: 0.3,
          }
        }
      }
    }
  }
}
```

4. 重启Gateway服务。

混合搜索功能需要`text`列上存在FTS（Full-Text Search）索引；该插件会尝试自动创建该索引。如果由于任何原因FTS索引创建失败，插件会记录错误日志并切换回仅使用向量搜索的模式。

## 配置参考

所有配置信息都存储在`plugins.entries.memory-lancedb.config`文件中：
- `hybrid.enabled`（布尔值，默认为`true`）：是否启用混合搜索功能
- `hybrid.reranker`（`rrf` | `linear`，默认为`rrf`）：用于重新排序的算法
- `hybrid.vectorWeight`（数值范围0–1，默认为0.7，仅适用于`linear`排序算法）：向量搜索的权重
- `hybrid.textWeight`（数值范围0–1，默认为0.3，仅适用于`linear`排序算法）：文本搜索的权重

## 注意事项/故障排除

- 该插件不会修改OpenClaw在磁盘上的安装文件；它仅在运行时覆盖内置的`memory-lancedb`插件。如需恢复原设置，请删除`plugins.loadpaths`文件。
- 如果您已经在磁盘上存储了LanceDB数据，可以继续使用原有的`dbPath`路径。
- 如果未看到混合搜索的效果，请确认`hybrid.enabled`设置为`true`，并检查Gateway的日志以确认FTS索引是否已成功创建。

## 相关文件

- `plugin/index.ts`：插件实现代码（包含混合搜索逻辑）
- `plugin/config.ts`：配置文件解析及用户界面相关代码
- `plugin/openclaw.plugin.json`：插件元数据文件及JSON格式规范（用于验证配置内容）