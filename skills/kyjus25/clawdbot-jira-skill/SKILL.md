---
name: jira
description: 通过 Jira Cloud 的 REST API 来管理 Jira 问题、问题状态转换以及工作日志。
homepage: https://developer.atlassian.com/cloud/jira/platform/rest/v3/intro/
metadata:
  {
    "clawdbot":
      {
        "emoji": "🧭",
        "requires":
          {
            "bins": ["curl", "jq", "bc", "python3"],
            "env": ["JIRA_URL", "JIRA_EMAIL", "JIRA_API_TOKEN"],
            "optional_env": ["JIRA_BOARD"],
          },
      },
  }
---

# Jira Skill

通过Clawdbot操作Jira问题和工作日志（搜索、查看状态、创建问题、记录工作内容、查看工作日志摘要）。

## 设置

1. 获取您的API密钥：https://id.atlassian.com/manage-profile/security/api-tokens
2. 点击“创建API密钥”
3. 设置环境变量：
   ```bash
   export JIRA_EMAIL="you@example.com"
   export JIRA_API_TOKEN="your-api-token"
   export JIRA_URL="https://your-domain.atlassian.net"
   # Optional project scope (comma-separated). Empty = search all.
   export JIRA_BOARD="ABC"
   ```

需要`curl`、`jq`、`bc`和`python3`工具。

## 快速命令

所有命令都位于`{baseDir}/scripts/jira.sh`目录下。

- `{baseDir}/scripts/jira.sh search "timeout" [max]` — 根据问题摘要或关键词在Jira中执行模糊搜索
- `{baseDir}/scripts/jira.sh link ABC-123` — 打开问题的浏览器链接
- `{baseDir}/scripts/jira.sh issue ABC-123` — 查看问题的详细信息
- `{baseDir}/scripts/jira.sh status ABC-123 "In Progress"` — 更改问题的状态（仅支持有效的状态转换）
- `{baseDir}/scripts/jira.sh transitions ABC-123` — 列出允许的问题状态转换
- `{baseDir}/scripts/jira.sh assign ABC-123 "name or email"` — 根据用户名或电子邮件分配问题
- `{baseDir}/scripts/jira.sh assign-me ABC-123` — 将问题分配给自己
- `{baseDir}/scripts/jira.sh comment ABC-123 "text"` — 为问题添加评论
- `{baseDir}/scripts/jira.sh create "Title" ["Description"]` — 在Jira中创建新问题
- `{baseDir}/scripts/jira.sh log ABC-123 2.5 [YYYY-MM-DD]` — 记录工作时长（默认为当天UTC时间）
- `{baseDir}/scripts/jira.sh my [max]` — 查看分配给你的问题
- `{baseDir}/scripts/jira.sh hours 2025-01-01 2025-01-07` — 按问题统计你的工作时长（格式为JSON）
- `{baseDir}/scripts/jira.sh hours-day 2025-01-07 [name|email]` — 按用户或问题统计当天的工作时长（可选过滤条件：名称/电子邮件；也可通过accountId查询）
- `{baseDir}/scripts/jira.sh hours-issue ABC-123 [name|email]` — 按问题统计工作时长（可选过滤条件：名称/电子邮件；也可通过accountId查询）

## 命令参考

- **搜索问题**  
  ```bash
  {baseDir}/scripts/jira.sh search "payment failure" [maxResults]
  ```

- **问题链接**  
  ```bash
  {baseDir}/scripts/jira.sh link ABC-321
  ```

- **问题详情**  
  ```bash
  {baseDir}/scripts/jira.sh issue ABC-321
  ```

- **更新问题状态**  
  ```bash
  {baseDir}/scripts/jira.sh status ABC-321 "Done"
  ```

- **列出问题状态转换**  
  ```bash
  {baseDir}/scripts/jira.sh transitions ABC-321
  ```

- **分配问题**  
  ```bash
  {baseDir}/scripts/jira.sh assign ABC-321 "Jane Doe"
  ```

- **将问题分配给自己**  
  ```bash
  {baseDir}/scripts/jira.sh assign-me ABC-321
  ```

- **添加评论**  
  ```bash
  {baseDir}/scripts/jira.sh comment ABC-321 "Deployed to staging"
  ```

- **创建问题**  
  ```bash
  {baseDir}/scripts/jira.sh create "Fix auth timeout" "Users being logged out after 5m"
  ```

- **记录工作时长**  
  ```bash
  {baseDir}/scripts/jira.sh log PB-321 1.5 2025-01-18
  ```

- **查看我的未解决问题**  
  ```bash
  {baseDir}/scripts/jira.sh my [maxResults]
  ```

- **按问题统计我的工作时长**  
  ```bash
  {baseDir}/scripts/jira.sh hours 2025-01-01 2025-01-05
  ```

- **按问题统计所有用户的工作时长**  
  ```bash
  {baseDir}/scripts/jira.sh hours-day 2025-01-05
  ```

- **按用户或问题统计某天的工作时长**  
  ```bash
  {baseDir}/scripts/jira.sh hours-day 2025-01-05 "jane"
  ```

- **按问题统计工作时长**  
  ```bash
  {baseDir}/scripts/jira.sh hours-issue ABC-321 "jane"
  ```

## 注意事项

- 记录工作日志的命令会使用Jira的`worklog/updated`和`worklog/list`接口，大型项目可能需要一些时间来完成。
- `hours`命令通过`JIRA_EMAIL`进行过滤；`hours-day`命令会返回每个用户的问题总时长。
- `hours`命令的输出结果为JSON格式，便于在其他工具中进一步使用。
- 在执行状态转换之前，系统会验证转换是否在Jira支持的转换列表中。