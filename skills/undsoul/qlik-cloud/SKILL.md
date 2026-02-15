---
name: qlik-cloud
description: **与37种工具实现Qlik Cloud分析平台的全面集成：**  
包括健康检查、搜索功能、应用程序管理、数据重新加载、自然语言查询（Insight Advisor）、自动化流程、AutoML技术、Qlik Answers AI、数据警报系统、用户管理、许可证管理、数据文件管理以及数据溯源功能。  
当用户咨询有关Qlik Cloud、Qlik Sense应用程序、分析仪表板或数据重新加载的相关问题，或者希望使用自然语言查询业务数据时，均可使用该集成方案。
---

# Qlik Cloud 技能

Qlik Cloud 的完整 OpenClaw 集成——涵盖了整个平台的 37 个工具。

## 设置

将凭据添加到 `TOOLS.md` 文件中：

```markdown
### Qlik Cloud
- Tenant URL: https://your-tenant.region.qlikcloud.com
- API Key: your-api-key-here
```

获取 API 密钥：进入 Qlik Cloud → 点击个人资料图标 → 个人资料设置 → API 密钥 → 生成新密钥

## ⚡ 何时使用哪些工具

| 您需要... | 使用的脚本 | 示例 |
|-------------|----------|---------|
| **实际数据值**（KPI、数字、趋势） | `qlik-insight.sh` | “总销售额是多少？”、“哪个仓库的库存最低？” |
| **应用程序结构**（字段名称、表格） | `qlik-app-fields.sh` | 了解数据模型 |
| **刷新数据** | `qlik-reload.sh` | 在查询前触发数据刷新 |
| **查找应用程序** | `qlik-search.sh` 或 `qlik-apps.sh` | 通过名称查找应用程序 |

**重要提示：** `qlik-app-fields.sh` 返回的是 **元数据**（结构信息），而非实际数据。要获取真实数据，请始终使用 `qlik-insight.sh`（Insight Advisor）。

## 快速参考

所有脚本的通用格式为：`QLIK_TENANT="https://..." QLIK_API_KEY="..." bash scripts/<script>.sh [args]`

### 核心操作
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-health.sh` | 健康检查/连接测试 | — |
| `qlik-tenant.sh` | 获取租户和用户信息 | — |
| `qlik-search.sh` | 搜索所有资源 | `"query"` |
| `qlik-license.sh` | 许可证信息和使用情况 | — |

### 应用程序
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-apps.sh` | 列出所有应用程序 | `[limit]` |
| `qlik-app-get.sh` | 获取应用程序详细信息 | `<app-id>` |
| `qlik-app-create.sh` | 创建新应用程序 | `"name" [space-id] [description]"` |
| `qlik-app-delete.sh` | 删除应用程序 | `<app-id>` |
| `qlik-app-fields.sh` | 获取字段和表格（仅元数据，不含数据值） | `<app-id>` |
| `qlik-app-lineage.sh` | 获取应用程序的数据源 | `<app-id>` |

### 数据刷新
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-reload.sh` | 触发应用程序刷新 | `<app-id>` |
| `qlik-reload-status.sh` | 检查刷新状态 | `<reload-id>` |
| `qlik-reload-cancel.sh` | 取消正在进行的刷新 | `<reload-id>` |
| `qlik-reload-history.sh` | 应用程序刷新历史记录 | `<app-id> [limit]` |
| `qlik-reload-failures.sh` | 最近的刷新失败记录 | `[days] [limit]` |

### 监控
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-duplicates.sh` | 查找重复的应用程序（同名应用程序） | `[limit]` |

### Insight Advisor ⭐（自然语言查询）
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-insight.sh` | 用自然语言提问，获取 **实际数据值** | `"question" [app-id]"` |

**这是获取实际数据的主要工具！** 使用自然语言提问：
- “总销售额是多少？”
- “哪个仓库的库存最低？”
- “按地区显示库存数量”
- “哪些商品缺货？”

**注意：** 如果您不知道应用程序 ID，可以先不输入该参数——Qlik 会自动推荐匹配的应用程序。应用程序 ID 为 UUID 格式（例如：`950a5da4-0e61-466b-a1c5-805b072da128`）。

### 用户与权限管理
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-users-search.sh` | 搜索用户 | `"query" [limit]` |
| `qlik-user-get.sh` | 获取用户详细信息 | `<user-id>` |
| `qlik-spaces.sh` | 列出所有空间 | `[limit]` |

### 数据文件与数据来源
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-datafiles.sh` | 列出上传的数据文件 | `[space-id] [limit]` |
| `qlik-datafile.sh` | 获取数据文件详细信息 | `<file-id>` |
| `qlik-datasets.sh` | 列出管理的数据集* | `[space-id] [limit]` |
| `qlik-dataset-get.sh` | 获取管理的数据集详细信息* | `<dataset-id>` |
| `qlik-lineage.sh` | 数据来源图谱 | `<secure-qri> [direction] [levels]` |

*管理的数据集仅在 Qlik Cloud 中可用。

### 自动化流程
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-automations.sh` | 列出自动化流程 | `[limit]` |
| `qlik-automation-get.sh` | 获取自动化流程详细信息 | `<automation-id>` |
| `qlik-automation-run.sh` | 运行自动化流程 | `<automation-id>` |
| `qlik-automation-runs.sh` | 自动化流程运行历史记录 | `<automation-id> [limit]` |

### AutoML
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-automl-experiments.sh` | 列出机器学习实验 | `[limit]` |
| `qlik-automl-experiment.sh` | 实验详细信息 | `<experiment-id>` |
| `qlik-automl-deployments.sh` | 列出机器学习部署 | `[limit]` |

### Qlik Answers（AI 助手）
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-answers-assistants.sh` | 列出 AI 助手 | `[limit]` |
| `qlik-answers-ask.sh` | 向 AI 助手提问 | `<assistant-id> "question" [thread-id]"` |

### 数据警报
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-alerts.sh` | 列出数据警报 | `[limit]` |
| `qlik-alert-get.sh` | 获取警报详细信息 | `<alert-id>` |
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

### 查看应用程序的数据来源
```bash
# Simple: see what files/connections an app uses
bash scripts/qlik-app-lineage.sh "950a5da4-0e61-466b-a1c5-805b072da128"
# Returns: QVD files, Excel files, databases, etc.
```

### 数据刷新管理
```bash
bash scripts/qlik-reload.sh "abc-123"
bash scripts/qlik-reload-status.sh "reload-id"
bash scripts/qlik-reload-history.sh "abc-123"
```

### 自然语言查询（Insight Advisor）
```bash
# Find apps that match your question
bash scripts/qlik-insight.sh "show me sales trend"

# Query specific app with UUID
bash scripts/qlik-insight.sh "ciro trend" "950a5da4-0e61-466b-a1c5-805b072da128"
# Returns: "Total Ciro is 9,535,982. Max is 176,447 on 2025-01-02"
```

### Qlik Answers（AI 助手）
```bash
# List available AI assistants
bash scripts/qlik-answers-assistants.sh

# Ask a question (creates thread automatically)
bash scripts/qlik-answers-ask.sh "27c885e4-85e3-40d8-b5cc-c3e20428e8a3" "What products do you sell?"
```

## 输出格式

所有脚本的输出格式为 JSON：
```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2026-02-04T12:00:00Z"
}
```

## 环境变量

**必需的凭据**（请添加到 `TOOLS.md` 文件中或设置为环境变量）：

- **QLIK_TENANT** — 您的租户 URL（例如：`https://company.eu.qlikcloud.com`）
- **QLIK_API_KEY** — 来自 Qlik Cloud 个人资料设置的 API 密钥

## 仅限云端的特性

以下特性是 **Qlik Cloud 独有的**（在 Windows 上的 Qlik Sense Enterprise 中不可用）：

- ⚙️ **自动化流程** — 低代码工作流自动化
- 🤖 **AutoML** — 机器学习实验与部署
- 💬 **Qlik Answers** — 基于 AI 的问答助手
- 🔔 **数据警报** — 基于阈值的通知
- 🔗 **数据来源图谱（QRI）** — 数据流可视化
- 📊 **管理数据集** — 集中式数据管理