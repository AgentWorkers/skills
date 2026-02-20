---
name: exa
description: >
  **使用场景：**  
  当任务需要使用 Exa MCP 进行网络或人员信息搜索，或者需要使用固定的工具集来配置 Exa MCP 服务器时。该功能可用于触发执行 Exa 搜索、高级 Exa 搜索、人员搜索，以及基于 Exa 的搜索结果汇总（包括相关来源链接）。
---
# Exa MCP 技能

## 工作流程
1. 明确研究目标、范围和输出格式。
2. 根据以下指南选择一个可用的工具：`web_search_exa`、`web_search_advanced_exa`、`people_search_exa`。
3. 建议使用托管的 Exa MCP 端点，该端点的 URL 查询中包含固定的工具名称。
4. 返回简洁的搜索结果，并标明未知的信息。
5. 如果遇到速率限制（如 429 错误），请缩小搜索范围或使用 API 密钥。

## 工具政策
- 目前可使用的工具：`web_search_exa`、`web_search_advanced_exa`、`people_search_exa`。
- 除非用户明确要求扩展功能，否则其他 Exa 工具均保持禁用状态。

## 工具选择指南
- 当用户需要进行一般性的网络搜索时，使用 `web_search_exa` 以获得快速且广泛的搜索结果。
  例如：查找关于 X 的最新文档和公告。
- 当需要根据域名、更新频率、搜索深度或更复杂的查询条件进行精确搜索时，使用 `web_search_advanced_exa`。
  例如：仅搜索与 X 相关的官方文档和最新来源。
- 当任务涉及识别人员、角色、背景或个人资料信息时，使用 `people_search_exa`。
  例如：查找在 Y 公司从事 X 工作的人员。

## 选择规则
- 当速度和覆盖范围比严格过滤更重要时，优先选择 `web_search_exa`。
- 如果 `web_search_exa` 返回的结果包含大量无关信息或不够精确时，选择 `web_search_advanced_exa`。
- 仅当任务与人员信息相关时，才使用 `people_search_exa`，而不适用于通用主题的搜索。

## 配置参考
- 请阅读 `references/exa-mcp-setup.md` 以获取 URL 模板和通用的 MCP 代码片段。