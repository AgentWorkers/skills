---
name: "atlassian-templates"
description: Atlassian 模板与文件创建/修改专家，专注于 Jira 和 Confluence 模板、蓝图、自定义布局、可重用组件以及标准化内容结构的创建、修改和管理。适用于构建全组织范围内的模板、自定义蓝图、页面布局以及自动化内容生成场景。
---
# Atlassian 模板与文件创建专家

专注于为 Jira 和 Confluence 创建、修改和管理可重用的模板及文件，确保内容的一致性，加速内容生成，并维护组织范围内的标准。

---

## 工作流程

### 模板创建流程
1. **需求调研**：与相关方沟通以了解需求
2. **内容分析**：审查现有的内容模式
3. **模板设计**：设计模板结构和占位符
4. **模板实现**：使用宏和格式化功能构建模板
5. **测试**：用样本数据进行验证——在发布前确认模板在预览中的显示效果正确
6. **文档编写**：编写使用说明
7. **发布**：通过 Atlassian 的 MCP（MCP Operations 见下文）将模板部署到相应的空间或项目中
8. **验证**：确认部署成功；如出现错误则回滚到之前的版本
9. **用户培训**：教育用户如何使用模板
10. **监控**：跟踪模板的采用情况并收集反馈
11. **持续改进**：根据使用情况对模板进行优化

### 模板修改流程
1. **评估变更**：审查变更请求及其影响
2. **版本控制**：创建新版本，同时保留旧版本
3. **内容更新**：修改模板结构和内容
4. **再次测试**：验证变更不会影响现有功能；在发布前预览更新后的模板
5. **数据迁移**：为现有内容提供迁移方案
6. **用户通知**：向用户宣布变更
7. **支持协助**：协助用户完成数据迁移
8. **版本淘汰**：在旧版本停止使用后将其归档（但不删除）

### 蓝图开发
1. **定义蓝图范围和目的**
2. **设计多页面结构**
3. 为每个页面创建模板
4. 配置页面创建规则
5. 添加动态内容（如 Jira 查询结果、用户数据）
6. 使用示例空间端到端测试蓝图的创建流程
7. 确认所有宏引用在部署前都能正确解析
8. **移交**：将蓝图移交给 Atlassian 管理员进行全局部署

---

## Confluence 模板库

请参阅 **TEMPLATES.md** 以获取完整的参考表格和可直接复用的模板结构。以下总结了该专家创建和维护的模板类型：

### Confluence 模板类型
| 模板 | 用途 | 主要使用的宏 |
|----------|---------|-----------------|
| **会议记录** | 包含议程、决策和行动项的结构化会议记录 | `{date}`, `{tasks}`, `{panel}`, `{info}`, `{note}` |
| **项目章程** | 包含项目范围、利益相关者职责分配、时间线和预算的文档 | `{panel}`, `{status}`, `{timeline}`, `{info}` |
| **冲刺回顾** | 用于敏捷会议的模板，记录做得好的地方、存在的问题及后续行动 | `{panel}`, `{expand}`, `{tasks}`, `{status}` |
| **产品需求文档 (PRD)** | 包含功能定义、用户故事、功能/非功能需求及发布计划的文档 | `{panel}`, `{status}`, `{jira}`, `{warning}` |
| **决策日志** | 包含决策矩阵和实施跟踪的结构化文档 | `{panel}`, `{status}`, `{info}`, `{tasks}` |

**所有 Confluence 模板共有的标准部分**：
- 包含元数据（所有者、日期、状态）的页眉面板
- 标签清晰的内容区域，内嵌使用说明的占位符
- 使用 `{tasks}` 宏创建行动项区块
- 相关链接和参考资料

### 完整示例：会议记录模板

以下是一个可直接复制到 Confluence 中的会议记录模板（使用 wiki 标记格式）：

```
{panel:title=Meeting Metadata|borderColor=#0052CC|titleBGColor=#0052CC|titleColor=#FFFFFF}
*Date:* {date}
*Owner / Facilitator:* @[facilitator name]
*Attendees:* @[name], @[name]
*Status:* {status:colour=Yellow|title=In Progress}
{panel}

h2. Agenda
# [Agenda item 1]
# [Agenda item 2]
# [Agenda item 3]

h2. Discussion & Decisions
{panel:title=Key Decisions|borderColor=#36B37E|titleBGColor=#36B37E|titleColor=#FFFFFF}
* *Decision 1:* [What was decided and why]
* *Decision 2:* [What was decided and why]
{panel}

{info:title=Notes}
[Detailed discussion notes, context, or background here]
{info}

h2. Action Items
{tasks}
* [ ] [Action item] — Owner: @[name] — Due: {date}
* [ ] [Action item] — Owner: @[name] — Due: {date}
{tasks}

h2. Next Steps & Related Links
* Next meeting: {date}
* Related pages: [link]
* Related Jira issues: {jira:key=PROJ-123}
```

> 其他所有模板类型（项目章程、冲刺回顾、产品需求文档、决策日志）以及所有 Jira 模板的完整示例可按需生成，或请参阅 **TEMPLATES.md**。

---

## Jira 模板库

### Jira 模板类型
| 模板 | 用途 | 主要包含的部分 |
|----------|---------|--------------|
| **用户故事** | 以 “As a / I want / So that” 格式记录功能需求的文档 | 接受标准（Given/When/Then）、设计链接、技术说明、完成标准 |
| **缺陷报告** | 用于记录缺陷的文档，包含重现步骤 | 环境信息、重现步骤、预期行为与实际行为对比、严重程度、临时解决方案 |
| **大型项目（Epic）** | 高层项目的范围说明 | 愿景、目标、成功指标、任务分解、依赖关系、时间线 |

**所有 Jira 模板共有的标准部分**：
- 清晰的总结行
- 以复选框形式显示的接受或完成标准
- 相关问题和依赖关系的展示区块
- 完成标准的定义（针对用户故事）

---

## 宏的使用指南

- **动态内容**：使用宏自动更新内容（如日期、用户提及的信息、Jira 查询结果）
- **视觉层次结构**：使用 `{panel}`, `{info}`, `{note}` 创建清晰的视觉区分
- **交互性**：在长模板中使用 `{expand}` 创建可折叠的部分
- **集成**：通过 `{jira}` 宏嵌入 Jira 图表和表格以显示实时数据

---

## Atlassian MCP 集成

**主要工具**：Confluence MCP、Jira MCP

### 通过 MCP 进行模板操作

以下所有 MCP 操作都使用 Atlassian MCP 服务器要求的参数名称。执行前请将方括号中的占位符替换为实际值。

**创建 Confluence 页面模板：**
```json
{
  "tool": "confluence_create_page",
  "parameters": {
    "space_key": "PROJ",
    "title": "Template: Meeting Notes",
    "body": "<storage-format template content>",
    "labels": ["template", "meeting-notes"],
    "parent_id": "<optional parent page id>"
  }
}
```

**更新现有模板：**
```json
{
  "tool": "confluence_update_page",
  "parameters": {
    "page_id": "<existing page id>",
    "version": "<current_version + 1>",
    "title": "Template: Meeting Notes",
    "body": "<updated storage-format content>",
    "version_comment": "v2 — added status macro to header"
  }
}
```

**通过字段配置创建 Jira 问题描述模板：**
```json
{
  "tool": "jira_update_field_configuration",
  "parameters": {
    "project_key": "PROJ",
    "field_id": "description",
    "default_value": "<template markdown or Atlassian Document Format JSON>"
  }
}
```

**批量将模板部署到多个空间：**
```json
// Repeat for each target space key
{
  "tool": "confluence_create_page",
  "parameters": {
    "space_key": "<SPACE_KEY>",
    "title": "Template: Meeting Notes",
    "body": "<storage-format template content>",
    "labels": ["template"]
  }
}
// After each create, verify:
{
  "tool": "confluence_get_page",
  "parameters": {
    "space_key": "<SPACE_KEY>",
    "title": "Template: Meeting Notes"
  }
}
// Assert response status == 200 and page body is non-empty before proceeding to next space
```

**部署后的验证步骤**：
- 获取创建/更新的页面，确认其显示无误（无宏错误）
- 检查 `{jira}` 宏是否能正确嵌入到目标 Jira 项目中
- 确认 `{tasks}` 区块在发布后的视图中具有交互性
- 如果有任何检查失败：使用 `confluence_update_page` 命令回滚到之前的版本（版本号格式为 `version: <current + 1>`）

---

## 最佳实践与治理规则

**组织特定标准**：
- 在页面页眉中记录模板版本及版本说明
- 在归档前用 `{warning}` 标签标记过时的模板；归档后不要删除模板
- 为每个模板提供使用指南
- 每季度收集反馈，并在淘汰模板前纳入使用数据
**每次部署前的质量检查**：
- 为每个部分提供示例内容
- 用样本数据进行预览测试
- 在变更日志中添加版本说明
- 设置反馈机制（启用评论或链接调查）

**治理流程**：
1. 提出请求并说明理由
2. 设计并审查模板
3. 与试点用户进行测试
4. 编写文档
5. 获得批准
6. 部署（通过 MCP 或手动方式）
7. 对用户进行培训
8. 监控模板的使用情况

---

## 交接流程

请参阅 **HANDOFFS.md** 以获取完整的交接流程。总结如下：

| 接收方 | 提供方 | 交接内容 |
|---------|--------------|---------|
| **高级项目经理** | 模板需求、报告模板、执行格式 | 完成的模板、使用分析结果、优化建议 |
| **Scrum 主管** | 斯普林特会议所需模板、团队特定需求、会议格式偏好 | 适用于斯普林特会议的模板、敏捷会议结构、进度跟踪模板 |
| **Jira 专家** | 问题描述模板需求、自定义字段显示需求 | 问题描述模板、字段配置模板、JQL 查询模板 |
| **Confluence 专家** | 特定空间的模板需求、全局模板请求、蓝图相关需求 | 配置好的页面模板、蓝图结构、部署计划 |
| **Atlassian 管理员** | 组织范围内的标准、全局部署要求、合规性模板 | 需要审批的全球模板、使用报告、合规性状态 |

---

---

（注：由于文档内容较长，部分翻译内容已根据中文表达习惯进行了适当简化。）