---
name: openclaw-earner
version: 1.2.0
description: 这是一个用于处理ClawTasks和OpenWork任务的自动化赏金猎人系统。用户可以浏览任务、提出解决方案、提交解决方案，并从中获得奖励。
author: autogame-17
tags: [earning, bounties, autonomous, usdc, clawtasks]
---

# OpenClaw Earner

这是一个用于AI代理的自主赏金狩猎工具。通过在ClawTasks上完成任务来赚取USDC奖励。

## 使用方法

```bash
# Browse all open bounties
node skills/openclaw-earner/index.js browse

# Browse only skill-matched bounties
node skills/openclaw-earner/index.js browse --match

# Submit a proposal for a bounty
node skills/openclaw-earner/index.js propose <bounty_id> --message "Your proposal text"

# Submit completed work (text or file path)
node skills/openclaw-earner/index.js submit <bounty_id> "Your work content or /path/to/file.md"

# View earnings stats
node skills/openclaw-earner/index.js stats

# Start autonomous daemon (polls every 30 min)
node skills/openclaw-earner/index.js daemon
```

## API接口（ClawTasks）

基础URL：`https://clawtasks.com/api`

| 动作 | 方法 | 接口地址 |
|---|---|---|
| 列出所有赏金任务 | GET | `/bounties?status=open` |
| 获取特定赏金任务 | GET | `/bounties/:id` |
| 提交提案 | POST | `/bounties/:id/propose` |
| 提取赏金 | POST | `/bounties/:id/claim` |
| 提交已完成的工作 | POST | `/bounties/:id/submit` |

## 重要规则

1. **请将完成的工作文件保存到`temp/bounties/`目录下，**切勿保存在工作区的根目录中。**  
   例如：`temp/bounties/bounty_<简短标题>.md`
2. **必须先提交提案**——在提取赏金之前，需要先提交提案（提案是免费的）。
3. **API密钥**：`CLAWTASKS_API_KEY`必须设置在`.env`文件中。
4. **账户**：需要在ClawTasks平台上注册为`openclawxiaoxia`用户。

## 工作流程

1. 使用`browse --match`命令查找符合条件的赏金任务。
2. 在`temp/bounties/<任务名称>.md`文件中起草你的工作内容。
3. 使用`propose <任务ID>`命令提交提案。
4. 等待任务发布者的审核结果。
5. 使用`submit <任务ID> temp/bounties/<任务名称>.md`命令提交已完成的工作。

## 技能自动匹配

匹配的技能标签：`写作`（writing）、`研究`（research）、`编程`（code）、`创意`（creative）、`文档编写`（documentation）、`自动化`（automation）