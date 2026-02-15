---
name: recruitly-mcp
description: "在 Recruitly CRM 中，您可以通过 MCP（Management Console）来搜索候选人、管理职位信息、查看招聘流程（pipelines）、跟踪账单情况以及评估团队绩效。"
homepage: https://recruitly.io
metadata:
  openclaw:
    emoji: "🎯"
    requires:
      bins:
        - mcporter
      env:
        - RECRUITLY_TOKEN
---

# Recruitly CRM

您可以通过 MCP 访问 Recruitly 招聘 CRM 系统——在任何消息应用程序中搜索候选人、管理职位、查看招聘流程以及跟踪团队绩效。

## 设置

### 1. 获取您的令牌

使用您的 Recruitly 账户（Google、Microsoft 或电子邮件）登录 [mcp.recruitly.dev](https://mcp.recruitly.dev)。您的 OAuth 令牌会自动生成。

### 2. 配置 mcporter

将以下代码添加到 `config/mcporter.json` 文件中：

```json
{
  "mcpServers": {
    "recruitly": {
      "baseUrl": "https://mcp.recruitly.dev/mcp",
      "description": "Recruitly CRM",
      "headers": {
        "Authorization": "Bearer ${RECRUITLY_TOKEN}"
      }
    }
  }
}
```

### 3. 设置您的令牌

```bash
export RECRUITLY_TOKEN="your_oauth_token_here"
```

## 可用工具

### 发现（Discovery）

| 工具 | 描述 |
|------|-------------|
| **list_options** | 返回您账户中的所有字段选项（职位状态、候选人状态、活动类型）。在按状态或类型筛选之前，请先调用此工具。 |

### 搜索与列表（Search & List）

| 工具 | 描述 |
|------|-------------|
| **search_candidates** | 根据关键词、位置、技能或职位名称搜索候选人 |
| **search_contacts** | 根据名称、公司或电子邮件搜索联系人（客户、招聘经理） |
| **search_companies** | 根据名称、行业或位置搜索公司 |
| **list_jobs** | 列出职位（支持状态和关键词筛选） |
| **list_pipelines** | 列出招聘流程（招聘环节） |

### 详情（Detail）

| 工具 | 描述 |
|------|-------------|
| **get_record** | 根据 ID 获取特定的候选人、联系人、公司或职位信息 |

## 使用示例

**查找候选人：**
> “在伦敦寻找 React 开发者”

调用 `searchandidates`，查询条件为 “React” 和 “London”。

**查看空缺职位：**
> “显示所有空缺职位”

首先调用 `list_options` 以获取空缺职位的准确状态标签，然后使用该状态调用 `list_jobs`。

**招聘流程概览：**
> “我的招聘流程中有哪些阶段？”

调用 `list_pipelines` 并汇总各阶段的数量。

**公司查询：**
> “查询 Acme Corp 的详细信息”

首先调用 `search_companies`，查询条件为 “Acme Corp”，然后使用 `get_record` 获取公司的完整信息。

**每周报告：**
> “提供本周新候选人的汇总信息”

使用最近日期的筛选条件调用 `search_candidates`，并按技能和位置进行汇总。

## 注意事项

- 所有数据均遵循您的 Recruitly 账户权限和团队可见性规则。
- 状态和类型值由租户配置（可能使用任何语言）——请务必先调用 `list_options`。
- 每次请求的搜索结果数量上限为 50 条；如需查看更多结果，请使用分页功能。
- 该功能支持 Recruitly 的免费计划，无需升级。

## 链接

- [Recruitly](https://recruitly.io)
- [MCP Server](https://recruitly.io/mcp)