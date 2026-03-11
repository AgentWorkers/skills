---
name: "jira-expert"
description: Atlassian Jira专家，擅长项目的创建与管理、规划、产品发现、JQL查询、工作流设计、自定义字段的设置、自动化流程的实现以及报告功能的运用。具备丰富的Jira项目配置经验，能够进行高级搜索、仪表板定制、工作流设计以及相关的Jira技术操作。
---
# Atlassian Jira 专家

具备 Jira 配置、项目管理、JQL 查询、工作流自动化及报告编制方面的高级技能。能够处理 Jira 的所有技术和运营相关问题。

## 快速入门 — 常见操作

**创建项目**：
```
mcp jira create_project --name "My Project" --key "MYPROJ" --type scrum --lead "user@example.com"
```

**运行 JQL 查询**：
```
mcp jira search_issues --jql "project = MYPROJ AND status != Done AND dueDate < now()" --maxResults 50
```

有关完整命令参考，请参阅 [Atlassian MCP 集成](#atlassian-mcp-integration)。JQL 函数的详细信息请参见 [JQL 函数参考](#jql-functions-reference)。报告模板的详细信息请参见 [报告模板](#reporting-templates)。

---

## 工作流

### 项目创建
1. 确定项目类型（Scrum、Kanban、问题跟踪等）
2. 使用合适的模板创建项目
3. 配置项目设置：
   - 名称、键、描述
   - 项目负责人和默认分配者
   - 通知方案
   - 权限方案
4. 设置问题类型和工作流
5. 如有需要，配置自定义字段
6. 创建初始看板/待办事项列表视图
7. **交接给**：Scrum Master 进行团队培训

### 工作流设计
1. 规划流程状态（待办 → 进行中 → 完成）
2. 定义转换规则和条件
3. 添加验证器、后处理函数和条件
4. 配置工作流方案
5. **验证**：首先在测试项目中部署工作流；确保所有转换规则、条件和后处理函数按预期运行，然后再应用于生产项目
6. 将工作流关联到项目
7. 使用示例问题测试工作流

### JQL 查询构建
**基本结构**：`字段 操作符 值`

**常用操作符**：
- `=, !=`：等于、不等于
- `~, !~`：包含、不包含
- `>, <, >=, <=`：比较
- `in, not in`：列表成员关系
- `is empty, is not empty`：是否为空
- `was, was in, was not`：过去的状态
- `changed`：是否发生变化

**强大的 JQL 示例**：
- 查找逾期问题：
```jql
dueDate < now() AND status != Done
```

- 查看冲刺进度问题：
```jql
sprint = 23 AND status changed TO "Done" DURING (startOfSprint(), endOfSprint())
```

- 查找长期未解决的问题：
```jql
updated < -30d AND status != Done
```

- 跟踪跨项目的大型任务（Epic）：
```jql
"Epic Link" = PROJ-123 ORDER BY rank
```

- 计算团队工作量（Velocity）：
```jql
sprint in closedSprints() AND resolution = Done
```

- 分析团队容量：
```jql
assignee in (user1, user2) AND sprint in openSprints()
```

### 仪表板创建
1. 创建新的仪表板（个人或共享）
2. 添加相关插件：
   - 基于 JQL 的结果筛选器
   - 冲刺进度图表
   - 工作量图表
   - 已创建问题与已解决的问题对比
   - 饼图（问题状态分布）
3. 调整布局以提高可读性
4. 配置自动刷新功能
5. 与相关团队共享仪表板
6. **交接给**：高级项目经理（Senior PM）或 Scrum Master 使用

### 自动化规则
1. 定义触发条件（问题创建、字段更改、定时触发）
2. 添加条件（如适用）
3. 定义操作：
   - 更新字段
   - 发送通知
   - 创建子任务
   - 转换问题状态
   - 发布评论
4. 使用示例数据测试自动化规则
5. 启用并监控自动化规则

## 高级功能

### 自定义字段
**何时创建自定义字段**：
- 当需要跟踪标准字段中不存在的数据时
- 当需要记录特定流程的信息时
- 当需要支持高级报告功能时

**字段类型**：文本、数字、日期、选择（单选/多选/级联）、用户选择器

**配置步骤**：
1. 创建自定义字段
2. 配置字段的适用范围（哪些项目/问题类型可以使用该字段）
3. 将自定义字段添加到相应的界面中
4. 如有需要，更新搜索模板

### 问题关联
**关联类型**：
- 阻碍问题（Blocks / Is blocked by）
- 相关问题（Relates to）
- 复制问题（Duplicates / Is duplicated by）
- 克隆问题（Clones / Is cloned by）
- Epic 与 Story 的关联

**最佳实践**：
- 使用 Epic 关联来分组功能
- 使用阻碍关系来显示问题之间的依赖关系
- 在评论中记录关联原因

### 权限与安全
**权限方案**：
- 查看项目信息
- 创建/编辑/删除问题
- 管理项目
- 管理冲刺计划

**安全级别**：
- 控制问题信息的可见性
- 保护敏感数据
- 审计权限变更

### 批量操作
**批量修改**：
1. 使用 JQL 查找目标问题
2. 选择批量修改操作
3. 选择要更新的字段
4. **验证**：在执行前预览所有更改；确保 JQL 过滤器仅匹配目标问题（批量修改难以撤销）
5. 执行并确认更改
6. 监控后台任务进度

## JQL 函数参考

> **提示**：将常用的查询保存为命名过滤器，避免重复运行复杂的 JQL 语句。有关性能优化建议，请参阅 [最佳实践](#best-practices)。

**日期相关函数**：
`startOfDay()`, `endOfDay()`, `startOfWeek()`, `endOfWeek()`, `startOfMonth()`, `endOfMonth()`, `startOfYear()`, `endOfYear()`

**冲刺相关函数**：
`openSprints()`, `closedSprints()`, `futureSprints()`

**用户相关函数**：
`currentUser()`, `membersOf("group")`

**高级函数**：
`issueHistory()`, `linkedIssues()`, `issuesWithFixVersions()`

## 报告模板

> **提示**：这些 JQL 代码片段可以保存为共享过滤器，或直接用于仪表板插件（详见 [仪表板创建](#dashboard-creation)。

| 报告类型 | JQL 语句 |
|---|---|
| 冲刺报告 | `project = PROJ AND sprint = 23` |
| 团队工作量 | `assignee in (team) AND sprint in closedSprints() AND resolution = Done` |
| 问题趋势 | `type = Bug AND created >= -30d` |
| 阻碍问题分析 | `priority = Blocker AND status != Done` |

## 决策流程

**何时需要联系 Atlassian 管理员**：
- 需要新的项目权限方案
- 需要在整个组织范围内应用自定义工作流方案
- 用户的添加或删除
- 许可证或计费问题
- 系统级配置更改

**何时需要与 Scrum Master 协作**：
- 冲刺看板配置
- 待办事项列表的优先级排序
- 针对特定团队的筛选条件
- 冲刺报告需求

**何时需要与高级项目经理（Senior PM）协作**：
- 项目组合级别的报告
- 跨项目的数据展示
- 需要高层管理人员查看的数据
- 多项目之间的依赖关系分析

## 交接流程

**从高级项目经理（Senior PM）接收到**：
- 项目结构需求
- 工作流和字段设置需求
- 报告需求
- 集成需求

**向高级项目经理（Senior PM）提供**：
- 跨项目的数据指标
- 问题趋势和模式分析
- 工作流中的瓶颈
- 数据质量分析

**从 Scrum Master 接收到**：
- 冲刺看板配置需求
- 工作流优化建议
- 待办事项列表的筛选需求
- 工作量跟踪相关帮助

## 最佳实践

**数据质量**：
- 通过字段验证规则强制填写必填字段
- 按项目类型统一问题键的命名规则
- 定期清理长期未解决或孤立的问题

**性能优化**：
- 在 JQL 中避免使用通配符（在大型文本字段中使用 `~` 会导致性能下降）
- 使用保存的过滤器，避免重复运行复杂的 JQL 语句
- 限制仪表板插件的数量以减少页面加载时间
- 将已完成的项目归档而不是直接删除，以保留历史记录

**管理规范**：
- 为自定义工作流状态和转换规则编写文档说明
- 在进行更改前对权限和工作流方案进行版本控制
- 对组织范围内的权限更改进行变更管理审查
- 在用户角色变更后进行权限审计

## Atlassian MCP 集成

**主要工具**：Jira MCP 服务器

**常用操作及示例命令**：
- 创建项目：
```
mcp jira create_project --name "My Project" --key "MYPROJ" --type scrum --lead "user@example.com"
```

- 运行 JQL 查询：
```
mcp jira search_issues --jql "project = MYPROJ AND status != Done AND dueDate < now()" --maxResults 50
```

- 更新问题字段：
```
mcp jira update_issue --issue "MYPROJ-42" --field "status" --value "In Progress"
```

- 创建冲刺计划：
```
mcp jira create_sprint --board 10 --name "Sprint 5" --startDate "2024-06-01" --endDate "2024-06-14"
```

- 创建看板筛选器：
```
mcp jira create_filter --name "Open Blockers" --jql "priority = Blocker AND status != Done" --shareWith "project-team"
```

**集成功能**：
- 为高级项目经理提供数据报表
- 为 Scrum Master 配置冲刺看板
- 为 Confluence 专家创建文档页面
- 为模板创建者提供模板支持

## 相关技能

- **Confluence 专家**（`project-management/confluence-expert/`）：Confluence 文档有助于完善 Jira 的工作流程
- **Atlassian 管理员**（`project-management/atlassian-admin/`）：负责 Jira 项目的权限和用户管理