---
name: linear-agent
description: Full Linear project management via native GraphQL API. Superior to shell-script alternatives — auto-resolves identifiers (ENG-42), moves issues by state name, generates plain-English backlog summaries, syncs git commits to issue states, zero dependencies.

⚠️ This is an unofficial community skill and is not affiliated with or endorsed by Linear, Inc.
---

# linear-agent

通过GraphQL API实现全面的线性项目管理功能。

## 功能概述
- 创建、更新和搜索问题
- 按名称将问题推进到不同的工作流程阶段
- 管理项目周期和冲刺计划
- 用简洁的英文总结团队待办事项
- 将Git提交信息同步到问题状态（例如：“fixes ENG-42”）
- 创建和管理项目
- 在问题上发表评论

## 设置要求
需要设置 `LINEAR_API_KEY` 环境变量。  
获取API密钥的步骤：
1. 登录 Linear 系统 → 设置 → 安全与访问 → API 密钥  
2. 将获取到的API密钥设置为 `LINEAR_API_KEY`  

## 使用方法
该工具既可作为 OpenClaw 的扩展技能使用，也可作为独立的命令行工具（CLI）使用：  
```
node index.js list-teams
node index.js create-issue --title "My issue" --teamId ENG
node index.js backlog-summary --teamId ENG
```