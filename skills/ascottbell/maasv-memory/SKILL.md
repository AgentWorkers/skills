# maasv 内存

这是一个为 OpenClaw 代理设计的结构化长期记忆系统，由 [maasv](https://github.com/ascottbell/maasv) 提供支持。

该系统通过引入认知层来替代默认的内存后端，该认知层支持三信号检索（语义信息 + 关键词 + 知识图谱）、实体提取、时间版本控制以及基于经验的学习功能。所有状态数据都存储在本地 SQLite 数据库中。

## 安装

使用此功能需要 `@maasv/openclaw-memory` 插件以及正在运行的 maasv 服务器。

### 1. 启动服务器

```bash
pip install "maasv[server,anthropic,voyage]"
maasv-server
```

### 2. 安装插件

```bash
openclaw plugins install @maasv/openclaw-memory
```

### 3. 激活插件

```json5
// ~/.openclaw/openclaw.json
{
  plugins: {
    slots: { memory: "memory-maasv" },
    entries: {
      "memory-maasv": {
        enabled: true,
        config: {
          serverUrl: "http://127.0.0.1:18790",
          autoRecall: true,
          autoCapture: true,
          enableGraph: true
        }
      }
    }
  }
}
```

## 功能介绍

- **`memory_search`**：支持在整个内存存储系统中进行三信号检索。
- **`memory_store`**：具备去重功能的记忆存储系统。
- **`memory_forget`**：用于永久删除数据。
- **`memory_graph`**：提供知识图谱功能，支持实体搜索、信息检索及关系分析。
- **`memory_wisdom**：记录推理过程、保存决策结果，并允许查询过去的决策内容。

系统会在每个游戏回合前自动调用相关记忆内容；每次会话结束后会自动提取实体信息。

## 链接

- **插件（npm）：** [@maasv/openclaw-memory](https://www.npmjs.com/package/@maasv/openclaw-memory)
- **服务器及核心组件（PyPI）：** [maasv](https://pypi.org/project/maasv/)
- **源代码：** [github.com/ascottbell/maasv](https://github.com/ascottbell/maasv)