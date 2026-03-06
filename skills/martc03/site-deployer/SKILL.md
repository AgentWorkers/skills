---
name: site-deployer
description: 将 Next.js 网站部署到 Netlify 并设置审批流程。目前支持 soilrichbyjohn.com 和 Synergy Salon 网站。
homepage: https://github.com/martc03/openclaw-ultimate
metadata: {"clawdbot":{"emoji":"🚀"}}
version: 1.0.0
author: martc03
tags: [deployment, netlify, nextjs, devops]
permissions:
  fileAccess: [~/soilrich-website, ~/synergy-website]
  commands: [git, npm, npx, netlify]
  network: [api.netlify.com, github.com]
---
# 网站部署工具

通过手机在 Netlify 上部署和管理 Next.js 网站。

## 网站列表

| 网站名 | 域名 | 仓库路径 |
|------|--------|------|
| soilrich | soilrichbyjohn.com | ~/soilrich-website |
| synergy | Synergy salon | ~/synergy-website |

## 命令

### `deploy [网站名]`
构建并部署网站到 Netlify。**执行前需要用户明确批准。**

**执行步骤：**
1. `cd ~/[网站名]-website && git pull`
2. `npm run build`
3. `netlify deploy --prod`
4. 将部署结果记录到 Notion 的 “Deploy History” 数据库中

### `deploy status [网站名]`
查看 Netlify 上的当前部署状态。

**执行命令：**
在网站的仓库目录中运行 `netlify status`。

### `deploy rollback [网站名]`
回滚到之前的部署版本。**执行前需要用户明确批准。**

**执行命令：**
使用 `netlify rollback` 回滚到之前的生产环境部署版本。

### `deploy logs [网站名]`
显示 Netlify 的最近部署日志。

**执行命令：**
运行 `netlify deploy --json | jq '.[-5:]'` 以显示最近的 5 次部署记录。

## 批准机制

所有 `deploy` 和 `rollback` 命令在执行前都需要用户确认。代理必须：
1. 提供即将部署的内容摘要（网站名称、当前分支、最新提交信息）
2. 等待用户明确的 “yes” 或 “confirm” 回应
3. 确认后才能执行部署操作

## 与 Notion 的集成

每次部署完成后，会在 “Deploy History” 数据库中创建一条记录：
- 部署信息：部署内容的简要描述
- 网站名称：soilrich 或 synergy
- 状态：成功、失败或回滚
- 时间戳：当前日期/时间
- 提交哈希：用于标识部署的 Git 提交哈希值
- 备注：任何相关的详细信息

## 设置要求

需要使用 Netlify CLI 进行身份验证：  
```bash
npm install -g netlify-cli
netlify login
```