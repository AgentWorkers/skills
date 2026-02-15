---
name: qlik-cloud
description: **Qlik Cloud 分析平台与 37 种工具的全面集成**  
该集成涵盖了以下功能：健康检查、搜索、应用程序管理、数据重新加载、自然语言查询（Insight Advisor）、自动化处理、AutoML（自动机器学习）、Qlik Answers（人工智能辅助工具）、数据警报、用户管理、许可证管理、数据文件处理以及数据来源追溯（data lineage）。  

**适用场景**：  
当用户咨询关于 Qlik Cloud、Qlik Sense 应用程序、分析仪表板或数据重新加载的相关问题时，或者希望使用自然语言查询业务数据时，该集成可提供强大的支持。
---

# Qlik Cloud 技能

为 Qlik Cloud 完整集成 OpenClaw——涵盖整个平台的 37 个工具。

## 设置

将凭据添加到 `TOOLS.md` 文件中：

```markdown
### Qlik Cloud
- Tenant URL: https://your-tenant.region.qlikcloud.com
- API Key: your-api-key-here
```

获取 API 密钥：进入 Qlik Cloud → 个人资料图标 → 个人资料设置 → API 密钥 → 生成新密钥

## ⚡ 何时使用哪些工具

| 您需要... | 使用的工具 | 示例 |
|-------------|----------|---------|
| **实际数据值**（KPI、数字、趋势） | `qlik-insight.sh` | “总销售额是多少？”、“哪个仓库的库存最低？” |
| **应用程序结构**（字段名称、表格） | `qlik-app-fields.sh` | 了解数据模型 |
| **刷新数据** | `qlik-reload.sh` | 在查询前触发数据刷新 |
| **查找应用程序** | `qlik-search.sh` 或 `qlik-apps.sh` | 通过名称查找应用程序 |

**🚨 决策树：**

```
User asks about data (numbers, KPIs, trends)?
  └─ YES → Use qlik-insight.sh
           └─ Response has 'narrative' or 'data'? 
              └─ YES → Return the results
              └─ NO → Try rephrasing, check drillDownLink
  └─ NO (structure/metadata) → Use qlik-app-fields.sh
```

**重要提示：** `qlik-app-fields.sh` 返回的是 **元数据**（结构），而非实际数据。要获取真实数据，请始终使用 `qlik-insight.sh`（Insight Advisor）。

## 快速参考

所有脚本的格式为：`QLIK_TENANT="https://..." QLIK_API_KEY="..." bash scripts/<script>.sh [args]`

### 核心操作
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-health.sh` | 健康检查/连接测试 | — |
| `qlik-tenant.sh` | 获取租户和用户信息 | — |
| `qlik-search.sh` | 搜索所有资源（返回 `resourceId`） | `"query"` |
| `qlik-license.sh` | 许可证信息和使用情况 | — |

### 应用程序
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-apps.sh` | 列出应用程序（支持空格过滤） | `[--space personal\|spaceId] [--limit n]` |
| `qlik-app-get.sh` | 获取应用程序详情 | `<app-id>` |
| `qlik-app-create.sh` | 创建新应用程序 | `"name" [space-id] [description]` |
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
| `qlik-duplicates.sh` | 查找重复的应用程序（名称相同） | `[limit]` |

### Insight Advisor ⭐ （自然语言查询）
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-insight.sh` | 用自然语言提问，获取 **实际数据值** | `"question" [app-id]` |

**这是获取实际数据的主要工具！** 可以自然地提问：
- “总销售额是多少？”
- “哪些仓库的库存最低？”
- “按地区显示库存数量”
- “哪些商品缺货？”

**重要提示：**
1. **使用搜索结果中的 `resourceId`（UUID 格式）——** 而不是商品 `id`。
2. **检查响应中是否包含 `narrative` 和/或 `data`——** 如果两者都缺失，请重新表述问题。
3. **对于数据查询，请使用 `qlik-insight.sh`，而不是 `fields.sh`——`fields.sh` 提供元数据，`insight.sh` 提供实际数据。

### 用户与权限管理
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-users-search.sh` | 搜索用户 | `"query" [limit]` |
| `qlik-user-get.sh` | 获取用户详情 | `<user-id>` |
| `qlik-spaces.sh` | 列出所有空间（共享空间、管理空间、数据空间） | `[limit]` |

### ⚠️ 个人空间

**Qlik Cloud 中的个人空间是虚拟的**——它不会出现在 `/spaces` API 中！

```bash
# ❌ WRONG: qlik-spaces.sh will NOT show personal space
bash scripts/qlik-spaces.sh

# ✅ CORRECT: Use qlik-apps.sh with --space personal
bash scripts/qlik-apps.sh --space personal
```

Qlik Cloud 中的空间类型：
- **personal** — 虚拟空间，用户的私有应用程序（使用 `--space personal`）
- **shared** — 团队协作空间
- **managed** — 具有发布工作流程的管理空间
- **data** — 数据存储空间

### 数据文件与数据源
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-datafiles.sh` | 列出上传的数据文件 | `[space-id] [limit]` |
| `qlik-datafile.sh` | 获取数据文件详情 | `<file-id>` |
| `qlik-datasets.sh` | 列出管理的数据集* | `[space-id] [limit]` |
| `qlik-dataset-get.sh` | 获取管理的数据集详情* | `<dataset-id>` |
| `qlik-lineage.sh` | 数据源追踪图 | `<secure-qri> [direction] [levels]` |

*管理的数据集在 Qlik Cloud 中可用。

### 自动化
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-automations.sh` | 列出自动化脚本 | `[limit]` |
| `qlik-automation-get.sh` | 获取自动化脚本详情 | `<automation-id>` |
| `qlik-automation-run.sh` | 运行自动化脚本 | `<automation-id>` |
| `qlik-automation-runs.sh` | 自动化脚本运行历史记录 | `<automation-id> [limit]` |

### AutoML
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-automl-experiments.sh` | 列出机器学习实验 | `[limit]` |
| `qlik-automl-experiment.sh` | 实验详情 | `<experiment-id>` |
| `qlik-automl-deployments.sh` | 列出机器学习部署 | `[limit]` |

### Qlik Answers（AI 助手）
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-answers-assistants.sh` | 列出 AI 助手 | `[limit]` |
| `qlik-answers-ask.sh` | 向助手提问 | `<assistant-id> "question" [thread-id]` |

### 数据警报
| 脚本 | 描述 | 参数 |
|--------|-------------|------|
| `qlik-alerts.sh` | 列出数据警报 | `[limit]` |
| `qlik-alert-get.sh` | 获取警报详情 | `<alert-id>` |
| `qlik-alert-trigger.sh` | 触发警报评估 | `<alert-id>` |

## 示例工作流程

### 检查环境
```bash
bash scripts/qlik-health.sh
bash scripts/qlik-tenant.sh
bash scripts/qlik-license.sh
```

### 查找并查询应用程序
```bash
# Search returns resourceId (UUID) — use this for all app operations
bash scripts/qlik-search.sh "Sales"
# Output: { "resourceId": "950a5da4-0e61-466b-a1c5-805b072da128", ... }

# Use the resourceId for app operations
bash scripts/qlik-app-get.sh "950a5da4-0e61-466b-a1c5-805b072da128"
bash scripts/qlik-app-fields.sh "950a5da4-0e61-466b-a1c5-805b072da128"
bash scripts/qlik-insight.sh "What were total sales last month?" "950a5da4-0e61-466b-a1c5-805b072da128"
```

### 查看应用程序的数据源
```bash
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
bash scripts/qlik-insight.sh "revenue by region" "950a5da4-0e61-466b-a1c5-805b072da128"
```

### Qlik Answers（AI）
```bash
# List available AI assistants
bash scripts/qlik-answers-assistants.sh

# Ask a question (creates thread automatically)
bash scripts/qlik-answers-ask.sh "27c885e4-85e3-40d8-b5cc-c3e20428e8a3" "What products do you sell?"
```

## 响应格式

所有脚本的输出格式为 JSON：
```json
{
  "success": true,
  "data": { ... },
  "timestamp": "2026-02-04T12:00:00Z"
}
```

## 环境变量

**所需凭据**（请添加到 `TOOLS.md` 或设置为环境变量）：
- **QLIK_TENANT** — 您的租户 URL（例如：`https://company.eu.qlikcloud.com`）
- **QLIK_API_KEY** — 来自 Qlik Cloud 个人资料设置的 API 密钥

## 仅限云端的功能

以下功能是 **Qlik Cloud 独有的**（在 Windows 上的 Qlik Sense Enterprise 中不可用）：
- ⚙️ **自动化** — 低代码工作流自动化
- 🤖 **AutoML** — 机器学习实验与部署
- 💬 **Qlik Answers** — 基于 AI 的问答助手
- 🔔 **数据警报** — 基于阈值的通知
- 🔗 **数据源追踪（QRI）** — 数据流可视化
- 📊 **管理数据集** — 集中式数据管理