# Jira 与 Confluence 集成技能

## 目的
该技能实现了与 Jira Cloud 和 Confluence 的自动化交互，具体功能包括：
- 查看问题详情、评论以及状态变更。
- 获取页面内容、更新信息，并导出摘要。
- 生成有助于优化用户沟通和文档的实用见解。

## 支持范围
- **支持的平台**：Jira Cloud（REST API）和 Confluence Cloud（REST API）。
- **认证方式**：使用通过环境变量安全存储的 API 令牌进行认证。
- **可执行的操作**：
  - `GET /api/v2/issues/{issueIdOrKey}` – 获取 Jira 问题的元数据。
  - `GET /api/v2/search` – 通过 JQL 搜索问题。
  - `GET /wiki/rsl/{pageIdOrTitle}` – 获取 Confluence 页面内容。
  - `POST /comment` – 向问题或页面添加评论（可选）。
- **输出结果**：问题摘要、改进建议以及用于自动化工作流程的集成点。

## 认证
- 将 Jira 和 Confluence 的 API 令牌存储在环境变量中：
  ```bash
  export JIRA_API_TOKEN=your_jira_token
  export CONFLUENCE_API_TOKEN=your_confluence_token
  ```
- 根据平台 API 的要求，使用这些令牌通过基本认证（basic auth）或承载令牌（bearer token）进行身份验证。

## 安装
```bash
clawhub install jiraandconfluence-skill
```

## 使用方法
安装完成后，可以通过命令行界面（CLI）调用该技能，或通过 OpenClaw 工作流进行集成：
```bash
jira-read --issue-key PROJ-123
confluence-read --title "Project Documentation"
```

## 安全性注意事项
- **切勿** 将凭据硬编码在脚本中。
- 除非明确授予写入权限，否则将令牌的访问权限限制为只读。
- 定期更换令牌并审核使用日志。

## 版本
1.0.0

## 维护者
Arkiant（通过内部渠道联系）