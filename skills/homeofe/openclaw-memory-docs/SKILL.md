---
name: openclaw-memory-docs
description: "OpenClaw插件：专为文档级内存管理设计，支持显式数据捕获、本地可搜索存储功能，并具备安全的数据编辑（redaction）机制。"
---
# openclaw-memory-docs

这是一个**OpenClaw Gateway插件**（而非代理技能），它提供了一个安全、易于审计的记忆存储系统。该插件专为项目文档和长期使用的笔记设计，重点关注以下几点：
- 对存储内容的明确控制；
- 防止秘密信息被意外存储；
- 采用确定性的、以本地数据为主的数据处理方式；
- 支持使用标签和项目元数据进行内容组织。

## 功能概述

- 提供以下命令：`/remember-doc`、`/search-docs`、`/list-docs`、`/forget-doc`、`/export-docs`、`/import-docs`；
- 配备了搜索工具`docs_memory_search`；
- 将数据存储在本地JSONL文件中（每行记录一条数据）；
- 通过确定性的本地嵌入技术实现语义化搜索，无需依赖外部服务；
- 对常见的秘密信息格式（如API密钥、令牌、私钥等）提供可选的隐藏功能；
- 支持使用标签和项目元数据进行过滤和分类。

## 安装方法

### 在ClawHub中安装

```bash
clawhub install openclaw-memory-docs
```

### 开发者使用方法

```bash
openclaw plugins install -l ~/.openclaw/workspace/openclaw-memory-docs
openclaw gateway restart
```

## 命令说明

### `/remember-doc` - 保存文档信息

```
/remember-doc [--tags t1,t2] [--project name] <text>
```

将笔记保存为文档记录。如果启用了`redactSecrets`选项（默认值为`true`），则会自动隐藏敏感信息。

- `--tags t1,t2` - 以逗号分隔的标签，这些标签会与配置文件中的`defaultTags`合并；
- `--project name` - 将该记录关联到特定项目。

示例：

```
/remember-doc Dubai: decide A vs B, then collect facts, then prepare a tax advisor briefing.
/remember-doc --tags legal,tax --project dubai Tax advisor meeting scheduled for March.
/remember-doc --tags=api --project=backend The /users endpoint requires Bearer auth.
```

### `/search-docs` - 搜索文档记录

```
/search-docs [--tags t1,t2] [--project name] <query> [limit]
```

通过语义相似性搜索已保存的文档记录。返回包含记录ID、标签和项目标识的搜索结果。

- `query` - 搜索文本（必填）；
- `limit` - 最大返回结果数量，1-20条（默认值：5条）；
- `--tags t1,t2` - 仅显示匹配指定标签的记录；
- `--project name` - 仅显示属于指定项目的记录。

示例：

```
/search-docs Dubai plan
/search-docs --project=dubai tax advisor 10
/search-docs --tags=api,backend endpoint auth
```

### `/list-docs` - 列出最近的文档记录

```
/list-docs [--tags t1,t2] [--project name] [limit]
```

列出最新的文档记录，包括记录ID、创建时间、标签和项目标识。

- `limit` - 最多显示的记录数量，1-50条（默认值：10条）；
- `--tags t1,t2` - 仅显示匹配指定标签的记录；
- `--project name` - 仅显示属于指定项目的记录。

示例：

```
/list-docs
/list-docs 20
/list-docs --project=dubai
/list-docs --tags=legal --project=dubai 5
```

### `/forget-doc` - 删除文档记录

```
/forget-doc <id>
```

通过记录的完整ID（可通过`/list-docs`获取）来删除记录。操作需要身份验证。

### `/export-docs` - 将文档记录导出为Markdown文件

```
/export-docs [--tags t1,t2] [--project name] [path]
```

将文档记录导出为单独的Markdown文件，适用于基于Git的工作流程。每个文件包含YAML格式的元数据（id、kind、createdAt、tags、project）以及记录内容。

- `path` - 目标目录（默认值为配置文件中的`exportPath`或`~/.openclaw/workspace/memory/docs-export`）；
- `--tags t1,t2` - 仅导出匹配指定标签的记录；
- `--project name` - 仅导出属于指定项目的记录。

文件命名格式：`YYYY-MM-DD_<shortid>.md`。

示例：

```
/export-docs
/export-docs ~/docs/memories
/export-docs --project=dubai
/export-docs --tags=api --project=backend ~/exports
```

### `/import-docs` - 从Markdown文件导入文档记录

```
/import-docs [path]
```

从导出的Markdown文件目录中导入文档记录。每个`.md`文件必须包含YAML格式的元数据（id、kind、createdAt）。操作需要身份验证。

系统会自动忽略重复的记录（基于ID判断）和无效的文件。

- `path` - 源目录（默认值为配置文件中的`exportPath`或`~/.openclaw/workspace/memory/docs-export`）。

示例：

```
/import-docs
/import-docs ~/docs/memories
/import-docs /path/to/exported/docs
```

## 工具：`docs_memory_search`

该工具可供代理和自动化脚本使用，支持通过查询语句搜索文档记录，并提供可选的标签和项目过滤功能。

**输入参数格式：**

```json
{
  "query": "Dubai plan A vs B",
  "limit": 5,
  "tags": ["legal"],
  "project": "dubai"
}
```

| 参数 | 类型 | 是否必填 | 说明 |
|---------|--------|---------|-------------------|
| `query` | string | 是 | 搜索文本 |
| `limit` | number | 否 | 最大返回结果数量，1-20条（默认值：5条） |
| `tags` | string[] | 否 | 根据这些标签过滤结果 |
| `project` | string | 否 | 根据项目名称过滤结果 |

**返回值**：一个`hits`数组，其中包含每个匹配项的`score`、`id`、`createdAt`、`tags`、`project`和`text`字段。

## 配置选项

```json
{
  "plugins": {
    "entries": {
      "openclaw-memory-docs": {
        "enabled": true,
        "config": {
          "storePath": "~/.openclaw/workspace/memory/docs-memory.jsonl",
          "dims": 256,
          "redactSecrets": true,
          "defaultTags": ["docs"],
          "maxItems": 5000,
          "exportPath": "~/.openclaw/workspace/memory/docs-export"
        }
      }
    }
  }
}
```

| 选项 | 类型 | 默认值 | 说明 |
|---------|--------|-------------------------|-------------------|
| `enabled` | boolean | `true` | 是否启用该插件 |
| `storePath` | string | `~/.openclaw/...docs-memory.jsonl` | JSONL存储文件的路径 |
| `dims` | number | `256` | 嵌入数据的维度（范围：32-2048） |
| `redactSecrets` | boolean | `true` | 存储前是否隐藏敏感信息 |
| `defaultTags` | string[] | `["docs"]` | 自动添加到每个记录中的默认标签 |
| `maxItems` | number | `5000` | 存储的最大记录数量（范围：100-100000） |
| `exportPath` | string | `~/.openclaw/...docs-export` | `/export-docs`和`/import-docs`命令的默认输出目录 |

### 注意事项

- 该插件**不**自动捕获聊天消息。如需自动捕获聊天内容，请使用`openclaw-memory-brain`插件。
- 导出/导入功能采用适合Git的文件格式：每个文档记录对应一个Markdown文件，文件名具有唯一性（格式为`YYYY-MM-DD_<shortid>.md`）。文件中的元数据便于进行版本控制和合并操作。