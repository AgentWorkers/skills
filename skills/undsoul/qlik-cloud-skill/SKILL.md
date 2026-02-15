---
name: qlik-cloud
description: **与37种工具实现Qlik Cloud分析平台的全面集成：**  
包括健康检查、搜索功能、应用程序管理、数据重新加载、自然语言查询（Insight Advisor）、自动化流程、AutoML（自动机器学习）、Qlik Answers AI（智能问答系统）、数据警报、用户管理、许可证管理、数据文件管理以及数据源追踪功能。  

**适用场景：**  
当用户咨询有关Qlik Cloud、Qlik Sense应用程序、分析仪表板或数据重新加载的相关问题时；或者希望使用自然语言查询业务数据时，均可使用该集成方案。
---

# Qlik Cloud Skill

本技能提供了对Qlik Cloud的全面OpenClaw集成支持，涵盖了平台上的37种工具。

## 设置

请将您的凭据添加到`TOOLS.md`文件中：

```markdown
### Qlik Cloud
- Tenant URL: https://your-tenant.region.qlikcloud.com
- API Key: your-api-key-here
```

获取API密钥：进入Qlik Cloud → 点击个人资料图标 → 个人资料设置 → API密钥 → 生成新密钥

## 快速参考

所有脚本的通用格式如下：
```
QLIK_TENANT="https://..." QLIK_API_KEY="..." bash scripts/<script>.sh [args]
```

### 核心操作
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-health.sh` | 健康检查/连接测试 | — |
| `qlik-tenant.sh` | 获取租户和用户信息 | — |
| `qlik-search.sh` | 搜索所有资源 | `"query"` |
| `qlik-license.sh` | 获取许可证信息及使用情况 | — |

### 应用程序
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-apps.sh` | 列出所有应用程序 | `[limit]` |
| `qlik-app-get.sh` | 获取应用程序详情 | `<app-id>` |
| `qlik-app-create.sh` | 创建新应用程序 | `"name" [space-id] [description]"` |
| `qlik-app-delete.sh` | 删除应用程序 | `<app-id>` |
| `qlik-app-fields.sh` | 获取应用程序中的字段和表格 | `<app-id>` |
| `qlik-app-lineage.sh` | 获取应用程序的数据源 | `<app-id>` |

### 重新加载
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-reload.sh` | 触发应用程序重新加载 | `<app-id>` |
| `qlik-reload-status.sh` | 检查重新加载状态 | `<reload-id>` |
| `qlik-reload-cancel.sh` | 取消正在进行的重新加载 | `<reload-id>` |
| `qlik-reload-history.sh` | 查看应用程序重新加载历史记录 | `<app-id> [limit]"` |
| `qlik-reload-failures.sh` | 查看最近的失败重新加载记录 | `[days] [limit]"` |

### 监控
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-duplicates.sh` | 查找重复的应用程序（名称相同） | `[limit]"` |

### Insight Advisor ⭐（自然语言查询）
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-insight.sh` | 提出问题并获取实时数据 | `"question" [app-id]"` |

**注意：** 如果您不知道应用程序ID，可以不提供该参数——Qlik会自动推荐匹配的应用程序。Insight Advisor的应用程序ID为UUID格式（例如：`950a5da4-0e61-466b-a1c5-805b072da128`）。

### 用户与权限管理
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-users-search.sh` | 搜索用户 | `"query" [limit]"` |
| `qlik-user-get.sh` | 获取用户详情 | `<user-id>` |
| `qlik-spaces.sh` | 列出所有工作区 | `[limit]"` |

### 数据文件与数据源
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-datafiles.sh` | 列出上传的数据文件 | `[space-id] [limit]"` |
| `qlik-datafile.sh` | 获取数据文件详情 | `<file-id>` |
| `qlik-datasets.sh` | 列出管理的数据集* | `[space-id] [limit]"` |
| `qlik-dataset-get.sh` | 获取管理的数据集详情* | `<dataset-id>` |
| `qlik-lineage.sh` | 数据源追踪图 | `<secure-qri> [direction] [levels]"` |

*管理数据集需要Qlik Data Integration许可证。

### 自动化任务
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-automations.sh` | 列出自动化任务 | `[limit]"` |
| `qlik-automation-get.sh` | 获取自动化任务详情 | `<automation-id>` |
| `qlik-automation-run.sh` | 运行自动化任务 | `<automation-id>` |
| `qlik-automation-runs.sh` | 查看自动化任务运行历史 | `<automation-id> [limit]"` |

### AutoML
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-automl-experiments.sh` | 列出机器学习实验 | `[limit]"` |
| `qlik-automl-experiment.sh` | 查看实验详情 | `<experiment-id>` |
| `qlik-automl-deployments.sh` | 列出机器学习部署 | `[limit]"` |

### Qlik Answers（AI助手）
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-answers-assistants.sh` | 列出AI助手 | `[limit]"` |
| `qlik-answers-ask.sh` | 向AI助手提问 | `<assistant-id> "question" [thread-id]"` |

### 数据警报
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-alerts.sh` | 列出数据警报 | `[limit]"` |
| `qlik-alert-get.sh` | 获取警报详情 | `<alert-id>` |
| `qlik-alert-trigger.sh` | 触发警报评估 | `<alert-id>` |

## 示例工作流程

### 检查环境配置
```bash
bash scripts/qlik-health.sh
bash scripts/qlik-tenant.sh
bash scripts/qlik-license.sh
```

### 查找并查询应用程序
```bash
bash scripts/qlik-search.sh "Sales"
bash scripts/qlik-app-get.sh "abc-123"
bash scripts/qlik-app-fields.sh "abc-123"
bash scripts/qlik-insight.sh "What were total sales last month?" "abc-123"
```

### 查看应用程序的数据源
```bash
# Simple: see what files/connections an app uses
bash scripts/qlik-app-lineage.sh "950a5da4-0e61-466b-a1c5-805b072da128"
# Returns: QVD files, Excel files, databases, etc.
```

### 管理应用程序的重新加载
```bash
bash scripts/qlik-reload.sh "abc-123"
bash scripts/qlik-reload-status.sh "reload-id"
bash scripts/qlik-reload-history.sh "abc-123"
```

### 使用Insight Advisor进行自然语言查询
```bash
# Find apps that match your question
bash scripts/qlik-insight.sh "show me sales trend"

# Query specific app with UUID
bash scripts/qlik-insight.sh "ciro trend" "950a5da4-0e61-466b-a1c5-805b072da128"
# Returns: "Total Ciro is 9,535,982. Max is 176,447 on 2025-01-02"
```

### 使用Qlik Answers（AI助手）
```bash
# List available AI assistants
bash scripts/qlik-answers-assistants.sh

# Ask a question (creates thread automatically)
bash scripts/qlik-answers-ask.sh "27c885e4-85e3-40d8-b5cc-c3e20428e8a3" "What products do you sell?"
```

## 输出格式

所有脚本的输出均为JSON格式：
```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2026-02-04T12:00:00Z"
}
```

## 环境变量

| 变量 | 是否必填 | 描述 |
|----------|----------|-------------|
| `QLIK_TENANT` | 是 | 完整的租户URL（格式：https://...） |
| `QLIK_API_KEY` | 是 | 来自Qlik Cloud的API密钥 |

## 仅适用于云端的功能

以下功能仅支持Qlik Cloud环境（不支持本地部署）：
- 自动化任务
- AutoML
- Qlik Answers
- 数据警报
- 数据源追踪（QRI）
- 管理数据集（需要Qlik Data Integration许可证）