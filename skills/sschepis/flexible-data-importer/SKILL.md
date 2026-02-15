# OpenClaw 数据导入器技能

<!-- SKILL-META
id: flexible-data-importer
version: 1.0.0
author: OpenClaw
description: 一种基于人工智能的数据导入工具，支持 CSV、JSON、XLSX 格式的数据导入，并具备自动生成数据模式的功能，同时支持与 Supabase 数据库的集成。
主要功能：
  - 数据导入
  - 数据模式生成
  - 与 Supabase 数据库的集成
所需条件：
  - 语言模型（LLM）：必须启用
  - 文件系统支持：必须启用
  - 网络连接：必须启用
调用方式：
  - 命令行：`data-importer <文件路径>`
  - API：`UniversalImporter.execute(<文件路径>)`
参数：
  - `name`: `filePath`（字符串类型）：源文件的路径（CSV、JSON、XLSX 格式）。
  - 必填参数。
  - 描述：源文件的路径。
**

该技能利用人工智能技术自动处理多种数据格式（CSV、JSON、XLSX），并构建结构化的 Supabase 数据库。它能够自动识别数据之间的关系、数据类型以及数据模式的名称。

## 输入参数
- `filePath`（字符串类型）：源文件的路径。
- `supabaseUrl`（字符串类型）：您的项目 Supabase 数据库的 URL。
- `supabaseKey`（字符串类型）：用于创建数据模式的 Supabase 服务角色密钥。

## 主要功能
- **自动数据模式生成**：无需预先定义数据库表结构。
- **类型安全**：能够自动将字符串数据转换为日期或数字类型（根据需要）。
- **批量上传**：支持处理大量历史数据集，而不会导致系统崩溃。