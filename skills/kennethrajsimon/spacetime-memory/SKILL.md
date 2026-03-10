---
name: spacetime-memory
description: 高性能的 SpacetimeDB 内存集成方案，专为 OpenClaw 设计。该方案用基于 WebAssembly 的高速数据处理引擎替代了传统的静态文件内存模型，该引擎运行在本地 SpacetimeDB 实例上。新版本支持完整的 CRUD 操作（创建、读取、更新、删除），同时兼容旧版本的文件导入功能，并提供了数据整合工具。
acceptLicenseTerms: true
metadata: {"openclaw":{"emoji":"🧠","tools":["tools/stdb_search.json","tools/stdb_store.json","tools/stdb_edit.json","tools/stdb_forget.json"],"install":[{"id":"npm-deps","kind":"script","sh":"npm install","label":"Install npm dependencies"}],"env":{"SPACETIMEDB_URL":{"description":"URL of the SpacetimeDB instance (default: http://127.0.0.1:3001)","optional":true},"SPACETIMEDB_NAME":{"description":"Name of the database (default: stdb-memory-1vgys)","optional":true}}}}
---
# SpacetimeDB内存集成

该技能为OpenClaw提供了一个基于WebAssembly的低延迟内存系统，该系统使用了[SpacetimeDB](https://spacetimedb.com/)。它可以直接连接到本地运行的SpacetimeDB实例，以存储、查询、更新和删除长期存储的数据。

## 可用工具
- **stdb_store**：用于存储新的内存数据及其可选的标签。
- **stdb_search**：根据标签或文本内容查询本地内存。
- **stdb_edit**：通过内存ID更新其内容和标签。
- **stdb_forget**：根据内存ID彻底删除指定的内存数据。

## 环境变量
这些工具支持以下可选的环境变量来定制连接设置：
- `SPACETIMEDB_URL`：数据库的端点（默认值：`http://127.0.0.1:3001`）
- `SPACETIMEDB_NAME`：数据库的名称（默认值：`stdb-memory-1vgys`）

## 旧版数据导入
提供了一个旧版数据导入脚本，用于帮助迁移旧的平面文件格式的数据（如`MEMORY.md`、`IDENTITY.md`等）。

**⚠️ 重要提示：** 旧版数据导入脚本具有破坏性。它会修改工作区中的核心用户文件，并创建备份文件（`.bak`），然后用迁移通知覆盖原始文件。为防止用户数据被意外或未经授权地删除，该脚本设置了严格的运行时保护机制：除非您明确提供了`--confirm`标志和目标路径，否则脚本将不会执行。在执行此脚本之前，**必须**获得用户的明确批准。

请通过以下命令运行该脚本：
`node ~/.openclaw/workspace/skills/spacetime-memory/legacy-import.js --confirm ~/.openclaw/workspace`