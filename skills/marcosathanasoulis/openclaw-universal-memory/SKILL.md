---
name: openclaw-universal-memory
description: 支持多种连接方式的Postgres数据库与pgvector的交互：数据的内存读取与写入，同时支持增量式游标历史记录（incremental cursor history）的功能。
---

# OpenClaw通用内存管理功能

该功能提供了一个通用的内存管理层，适用于处理异构数据：
- 支持规范的数据实体/数据块结构；
- 采用连接器方式导入数据，并支持使用游标进行数据操作；
- 支持在Postgres数据库中进行数据搜索。

## 使用场景

- 将来自多个系统的记录统一到同一个数据模型中；
- 保留每个连接器/账户的增量同步历史记录（通过游标进行管理）；
- 在pgvector中构建可用于RAG（Retrieval-Aggregation-Processing）的数据存储结构。

## 先决条件

- 需要安装带有`vector`扩展的Postgres数据库；
- 需要在本地安装相关软件包：`pip install -e .`；
- 需要安装用于数据库I/O操作的Python库：`pip install "psycopg[binary]>=3.2"`；
- 数据源连接信息（DSN）应通过环境变量`DATABASE_DSN`提供（默认值）。

## 安全注意事项

- 不要在命令行参数中传递原始密码或令牌；
- 建议使用操作系统提供的秘密存储机制或进程环境变量来管理DSN信息；
- 该功能仅用于读取和写入配置好的Postgres数据库，不会直接调用外部API；
- 使用最低权限的数据库访问权限（仅允许对`um_*`表执行`SELECT/INSERT/UPDATE/DELETE`操作）；
- 在运行任何自定义连接器之前，请仔细检查其代码并确保其安全性。

## 负责任使用提示

- 仅将此功能用于您合法控制或被授权处理的账户和数据；
- 您需对数据的隐私性、存储期限以及合规性负责；
- 本项目遵循Apache 2.0许可证，不提供任何运营保障；
- 该实现主要由AI生成，但经过了有经验的工程师审核；在生产环境中使用前请务必进行验证。

## 命令说明

- 一次性配置数据库访问凭据（推荐操作）：```bash
python skills/openclaw-universal-memory/scripts/run_memory.py \
  --action configure-dsn
```

- 初始化数据模型：```bash
python skills/openclaw-universal-memory/scripts/run_memory.py \
  --action init-schema \
  --dsn-env DATABASE_DSN
```

- 导入JSON/NDJSON数据：```bash
python skills/openclaw-universal-memory/scripts/run_memory.py \
  --action ingest-json \
  --dsn-env DATABASE_DSN \
  --source gmail \
  --account marcos@athanasoulis.net \
  --entity-type email \
  --input /path/to/records.ndjson
```

- 通过内置连接器导入数据：```bash
python skills/openclaw-universal-memory/scripts/run_memory.py \
  --action ingest-connector \
  --connector google \
  --account you@example.com \
  --dsn-env DATABASE_DSN \
  --limit 300
```

- 在导入数据前验证连接器的认证信息和配置：```bash
python skills/openclaw-universal-memory/scripts/run_memory.py \
  --action validate-connector \
  --connector google \
  --account you@example.com \
  --dsn-env DATABASE_DSN \
  --limit 1
```

- 数据搜索：```bash
python skills/openclaw-universal-memory/scripts/run_memory.py \
  --action search \
  --dsn-env DATABASE_DSN \
  --query "Deryk" \
  --limit 20
```

- 查看最近的导入记录：```bash
python skills/openclaw-universal-memory/scripts/run_memory.py \
  --action events \
  --dsn-env DATABASE_DSN \
  --limit 20
```

- 进行故障排查：```bash
python skills/openclaw-universal-memory/scripts/run_memory.py \
  --action doctor
```

## 调度参考

- 详细调度配置请参考`docs/SCHEDULING.md`（包含cron调度示例，默认间隔为15分钟，支持通过连接器进行配置调整）。

## 连接器接口规范（针对自定义适配器）

自定义连接器需要返回以下格式的标准化数据记录以及下一个可操作的游标：
- `external_id`
- `entity_type`
- `title`
- `body_text`
- `raw_json`
- `meta_json`
- `next_cursor`

这样的设计使得数据导入过程具有通用性，能够支持各种数据源系统。

- 提供了连接器模板文件：`src/openclaw_memory/connectors/templates.py`
- 详细的设置指南请参考`docs/CONNECTOR SETUP_WALKTHROUGH.md`（涵盖Gmail、Slack、Asana、iMessage等平台的配置步骤）。

## 社区贡献

我们欢迎开发者通过提交Pull Request（PR）来贡献代码。有关贡献要求、测试规范及设置指南，请参阅`docs/CONNECTOR_CONTRIBUTING.md`。