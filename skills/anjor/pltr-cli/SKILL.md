---
name: pltr-cli
description: **pltr CLI 使用指南**  
pltr CLI（Palantir Foundry Command Line Interface）是用于操作 Palantir Foundry 的命令行工具，可帮助您执行多种任务，如查询数据集、管理编排构建过程、处理本体数据、运行 SQL 查询、管理文件夹/空间/项目以及执行管理操作。  

**主要功能包括：**  
- **查询数据集**：快速检索和访问存储在 Foundry 中的数据集。  
- **管理编排构建**：监控和配置数据集的构建过程。  
- **处理本体数据**：操作与数据集相关的本体信息。  
- **运行 SQL 查询**：在数据库中执行 SQL 语句。  
- **管理文件夹/空间/项目**：创建、删除或重命名文件夹和项目。  
- **执行管理操作**：执行与 Palantir Foundry 系统相关的管理任务。  

**触发词（Trigger Words）：**  
- Foundry  
- pltr  
- dataset  
- SQL query  
- ontology  
- build  
- schedule  
- RID  

**使用说明：**  
请根据具体需求选择相应的命令，并在命令行中输入相应的参数来执行相应的操作。例如：  
- `pltr dataset list`：列出所有可用的数据集。  
- `pltr build start`：启动数据集的构建过程。  
- `pltr ontology update`：更新相关本体数据。  

**注意事项：**  
- 请确保已正确安装 pltr CLI 并配置好环境变量。  
- 对于复杂的操作，建议查阅官方文档或咨询技术支持以获取详细信息。  

通过使用 pltr CLI，您可以更高效地管理 Palantir Foundry 中的各种资源，提高工作效率。
---

# pltr-cli: Palantir Foundry 命令行工具

本技能帮助您有效地使用 pltr-cli 与 Palantir Foundry 进行交互。

## 兼容性

- **技能版本**: 1.1.0
- **pltr-cli 版本**: 0.12.0+
- **Python**: 3.9, 3.10, 3.11, 3.12
- **依赖项**: foundry-platform-sdk >= 1.69.0

## 概述

pltr-cli 是一个功能强大的命令行工具，包含 100 多个命令，可用于执行以下操作：
- **数据集操作**: 获取信息、列出文件、下载文件、管理分支和事务
- **SQL 查询**: 执行查询、导出结果、管理异步查询
- **本体**: 列出本体、对象类型、对象、执行操作和查询
- **编排**: 管理构建、作业和调度
- **文件系统**: 操作文件夹、项目、资源
- **管理**: 用户、组、角色管理
- **连接**: 外部连接和数据导入
- **媒体集**: 管理媒体文件
- **语言模型**: 与 Anthropic Claude 模型和 OpenAI 嵌入式模型交互
- **流式数据集**: 创建和管理流式数据集、发布实时数据
- **函数**: 执行查询并检查数据类型
- **AIP 代理**: 管理 AI 代理、会话和版本
- **模型**: 用于模型和版本管理的机器学习模型注册表

## 关键概念

### 基于 RID 的 API
Palantir Foundry 的 API 是基于 **资源标识符 (Resource Identifier, RID)** 的。大多数命令都需要使用 RID：
- **数据集**: `ri.foundry.main.dataset.{uuid}`
- **文件夹**: `ri.compass.main.folder.{uuid}`（根目录: `ri.compass.mainfolder.0`)
- **构建**: `ri.orchestration.main.build.{uuid}`
- **调度**: `ri.orchestration.main.schedule.{uuid}`
- **本体**: `ri.ontology.main.ontology.{uuid}`

用户必须提前知道这些 RID（可以通过 Palantir Foundry 的 Web 界面或之前的 API 调用获取）。

### 认证
在使用任何命令之前，请确保已配置好认证：
```bash
# Configure interactively
pltr configure configure

# Or use environment variables
export FOUNDRY_TOKEN="your-token"
export FOUNDRY_HOST="foundry.company.com"

# Verify connection
pltr verify
```

### 输出格式
所有命令都支持多种输出格式：
```bash
pltr <command> --format table    # Default: Rich table
pltr <command> --format json     # JSON output
pltr <command> --format csv      # CSV format
pltr <command> --output file.csv # Save to file
```

### 配置配置文件
使用 `--profile` 选项在不同的 Palantir Foundry 实例之间切换：
```bash
pltr <command> --profile production
pltr <command> --profile development
```

## 参考文件
根据用户的任务需求，可以参考以下文件：
| 任务类型 | 参考文件 |
|-----------|----------------|
| 设置、认证、入门 | `reference/quick-start.md` |
| 数据集操作（获取、文件、分支、事务） | `reference/dataset-commands.md` |
| SQL 查询 | `reference/sql-commands.md` |
| 构建、作业、调度 | `reference/orchestration-commands.md` |
| 本体、对象、操作 | `reference/ontology-commands.md` |
| 用户、组、角色、组织 | `reference/admin-commands.md` |
| 文件夹、项目、资源、权限 | `reference/filesystem-commands.md` |
| 连接、导入 | `reference/connectivity-commands.md` |
| 媒体集、媒体文件 | `reference/mediasets-commands.md` |
| Anthropic Claude 模型、OpenAI 嵌入式模型 | `reference/language-models-commands.md` |
| 流式数据集、实时数据发布 | `reference/streams-commands.md` |
| 函数查询、数据类型 | `reference/functions-commands.md` |
| AIP 代理、会话、版本 | `reference/aip-agents-commands.md` |
| 机器学习模型注册表、模型版本 | `reference/models-commands.md` |

## 工作流程文件
对于常见的多步骤任务，可以参考以下文件：
| 工作流程 | 文件 |
|----------|------|
| 数据探索、SQL 分析、本体查询 | `workflows/data-analysis.md` |
| ETL 流程、定时作业、数据质量 | `workflows/data-pipeline.md` |
| 设置权限、资源角色、访问控制 | `workflows/permission-management.md` |

## 常用命令快速参考
```bash
# Verify setup
pltr verify

# Current user info
pltr admin user current

# Execute SQL query
pltr sql execute "SELECT * FROM my_table LIMIT 10"

# Get dataset info
pltr dataset get ri.foundry.main.dataset.abc123

# List files in dataset
pltr dataset files list ri.foundry.main.dataset.abc123

# Download file from dataset
pltr dataset files get ri.foundry.main.dataset.abc123 "/path/file.csv" "./local.csv"

# Copy dataset to another folder
pltr cp ri.foundry.main.dataset.abc123 ri.compass.main.folder.target456

# List folder contents
pltr folder list ri.compass.main.folder.0  # root folder

# Search builds
pltr orchestration builds search

# Interactive shell mode
pltr shell

# Send message to Claude model
pltr language-models anthropic messages ri.language-models.main.model.xxx \
    --message "Explain this concept"

# Generate embeddings
pltr language-models openai embeddings ri.language-models.main.model.xxx \
    --input "Sample text"

# Create streaming dataset
pltr streams dataset create my-stream \
    --folder ri.compass.main.folder.xxx \
    --schema '{"fieldSchemaList": [{"name": "value", "type": "STRING"}]}'

# Publish record to stream
pltr streams stream publish ri.foundry.main.dataset.xxx \
    --branch master \
    --record '{"value": "hello"}'

# Execute a function query
pltr functions query execute myQuery --parameters '{"limit": 10}'

# Get AIP Agent info
pltr aip-agents get ri.foundry.main.agent.abc123

# List agent sessions
pltr aip-agents sessions list ri.foundry.main.agent.abc123

# Get ML model info
pltr models model get ri.foundry.main.model.abc123

# List model versions
pltr models version list ri.foundry.main.model.abc123
```

## 最佳实践

1. **始终先验证认证**: 在开始工作之前运行 `pltr verify`
2. **选择合适的输出格式**: 对于编程用途使用 JSON，对于电子表格使用 CSV，对于便于阅读使用表格格式
3. **对大型查询使用异步处理**: 对于耗时较长的查询，使用 `pltr sql submit` 和 `pltr sql wait`
4. **导出结果**: 使用 `--output` 选项保存结果以供进一步分析
5. **使用 shell 模式进行探索**: `pltr shell` 支持自动补全和历史记录功能

## 获取帮助
```bash
pltr --help                    # All commands
pltr <command> --help          # Command help
pltr <command> <sub> --help    # Subcommand help
```