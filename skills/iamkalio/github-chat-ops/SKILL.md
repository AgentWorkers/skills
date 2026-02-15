---
name: github-chat-ops
description: 通过聊天方式为非技术用户管理单个 GitHub 仓库：在他们提供仓库 URL 和临时个人访问令牌后，使用 GitHub API 获取仓库的拉取状态，汇总谁在何时完成了哪些操作，并直接在 GitHub 上创建或跟进问题。
---

## 概述  
每当非技术人员（通常通过 WhatsApp）需要简单的 GitHub 帮助，且不需要克隆或创建仓库分支时，可以使用此技能。常见的请求包括：  
- “告诉我最近有哪些更改，是谁做的？”  
- “创建一个问题来描述某个具体需求。”  
- “跟进现有的问题或 Pull Request。”  

该工作流程完全依赖于 GitHub 的 REST API，并使用请求者在聊天过程中提供的个人访问令牌（PAT）。  

## 1. 每次会话前收集所需信息  
1. **仓库标识符**：请求完整的仓库 URL 或 `owner/name`。  
2. **个人访问令牌（PAT）**：确认该令牌具有 `repo`（私有仓库）或 `public_repo`（公共仓库）的权限。提醒他们生成一个临时令牌并通过聊天发送给你；使用完毕后请删除该令牌。  
3. **任务概述**：明确他们的需求（例如创建问题、跟进问题等）以及时间范围（例如“过去 7 天内发生的变化”）。  

**在采取任何操作之前，务必再次确认用户提供的所有信息是否完整。如有遗漏，请暂停并询问。**  

## 2. 安全地处理访问令牌  
- 仅将令牌粘贴到当前会话中的临时 shell 变量中：  
  ```bash
  export GITHUB_TOKEN="<token-from-chat>"
  ```  
- 绝不要将令牌保存到磁盘或日志文件中。操作完成后，执行 `unset GITHUB_TOKEN`。  
- 每次 API 调用都必须设置 `Authorization: Bearer $GITHUB_TOKEN` 和 `Accept: application/vnd.github+json`。  

## 3. 在执行操作前获取仓库信息  
1. **仓库状态检查**：`GET /repos/{owner}/{repo}`——确认访问权限并显示默认分支。  
2. **最近的操作记录**（用于生成变更摘要）：  
   - `GET /repos/{owner}/{repo}/commits?since=<ISO8601>&until=<ISO8601>`  
   - 如需按作者分类结果，可添加 `author=<username>`。  
3. **问题与 Pull Request**：`GET /repos/{owner}/{repo}/issues?state=all&since=<ISO8601>`  
   - 通过 `pull_request` 关键字区分 Pull Request。  

如果需要，在生成摘要之前，可以将原始 JSON 响应内容保存到文件中（例如 `/tmp/commits.json`），以便后续使用 `jq` 等工具进行处理。  

## 4. 在不克隆仓库的情况下深入查看仓库内容  
当需要文件级别的信息（例如在问题描述中引用代码或解释某个提交的含义时），可以通过 REST API 查看仓库内容：  
1. **列出目录和文件**：`GET /repos/{owner}/{repo}/contents/<path>?ref=<branch>` 可获取文件元数据及下载链接。  
2. **获取文件内容**：可以使用 `download_url`，或通过 `GET /repos/{owner}/{repo}/contents/<path>` 并设置 `Accept: application/vnd.github.raw` 来获取文件内容。  
3. **处理大型仓库结构**：`GET /repos/{owner}/{repo}/git/trees/<sha>?recursive=1` 可获取整个仓库的结构，然后获取所需的文件。  
4. 将读取的内容缓存起来（例如保存到 `/tmp/github-chat-ops/<repo>/...`），以便后续查询时避免重复调用 API。  
在编写问题描述或摘要时，务必提及文件的路径和相关内容。  

## 5. 为非技术人员生成易于理解的变更摘要  
- 按贡献者分组显示提交记录，并详细说明实际发生了哪些更改（例如功能、测试内容或配置调整）。  
- 对于每个提交，执行 `GET /repos/{owner}/{repo}/commits/{sha}` 以获取文件列表（文件名、新增内容/删除内容、修改内容）。  
- 提取每个贡献者的主要变更内容（例如：“更新了 `quiz_generator.py` 以支持上下文提示，并添加了 3 个 YAML 测试用例”。  
- 以用户所在时区（默认为 Africa/Lagos）显示时间戳。  
- 显示提交的状态（已合并、待处理、已关闭等）以及需要跟进的事项。  
保持摘要简洁、使用项目符号格式，并避免使用专业术语。  

## 6. 创建或更新问题  
1. 在聊天过程中明确问题、预期结果、优先级和负责人。  
2. 在本地使用 Markdown 格式起草问题描述（包括问题背景、重现步骤和验收标准）。  
3. 通过 `POST /repos/{owner}/{repo}/issues` 发送问题请求（使用 JSON 格式的数据）：  
   ```json
   {
     "title": "...",
     "body": "...",
     "assignees": ["username"],
     "labels": ["priority:high"]
   }
   ```  
4. 将创建的问题链接告知用户，并简要总结问题内容。  

**后续操作**：可以使用 `PATCH /repos/{owner}/{repo}/issues/{number}` 更新问题状态或分配负责人，或使用 `POST /repos/{owner}/{repo}/issues/{number}/comments` 添加状态备注。  

## 7. 聊天流程（适用于 WhatsApp）  
1. 询问用户：“我需要仓库 URL 和具有仓库权限的临时令牌——现在可以分享吗？”  
2. 每完成一项操作后，先用自然语言向用户报告结果，再分享相关链接或详细信息。  
3. 在摘要中不要提及访问令牌。如果用户发送了截图或敏感信息，请确认收到后避免在其他地方再次分享。  

## 8. 日常自动化与定时任务  
- 将长期使用的敏感信息（如访问令牌、仓库地址、时区设置）存储在单独的文件中（例如 `.env.github-chat-ops`）。  
- 在 `scripts/` 目录下编写可重用的脚本（例如 `scripts/github_chat_ops_daily.py`），这些脚本会加载环境变量、调用相应的 API 并生成可发送的摘要。  
- 通过 `cron` 定时执行脚本时，从工作区根目录运行脚本，并将输出结果完整记录下来；如果脚本执行失败（返回非零状态码），请记录错误信息。  
- 允许最终用户通过编辑环境文件来自定义仓库地址和时区设置；在技能更新说明中记录这些设置信息，以便后续使用者能够找到相关配置。  

## 9. 参考资料  
请参考 [`references/github-api-cheatsheet.md`](references/github-api-cheatsheet.md)，其中提供了涵盖上述 API 端点的curl 模板以及分页技巧。