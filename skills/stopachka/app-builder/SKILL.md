---
name: app-builder
description: 使用 `npx instant-cli`、`create-instant-app`（Next.js + Codex）、GitHub（gh）以及 Vercel（vercel）来构建、编辑和部署基于 Instant 的应用程序。当需要创建新应用程序、修改现有应用程序、修复错误、添加新功能或部署/更新应用程序时，请使用这些工具。所有项目都存储在 `~/apps` 目录下；请始终在相应的应用程序文件夹内进行操作。
---

# 应用构建器（App Builder）

您可以使用以下工具：
- `npx instant-cli`
- `gh`（GitHub 命令行工具）
- `vercel`（Vercel 部署工具）

如果您发现这些工具未安装或未登录，请提示用户先安装并登录。

所有应用程序都存储在 `~/apps` 目录下。

## 基本规则
- 请始终在 `~/apps/<app-name>` 目录下创建或编辑项目。
- 在进行任何更改之前，请阅读仓库根目录下的 `AGENTS.md` 文件；如果存在 `~/apps/<app-name>/AGENTS.md` 文件，请也一并阅读。
- 目前，所有更改都必须推送到 `main` 分支。
- 每个应用程序都必须满足以下要求：
  1) 被推送至 GitHub
  2) 在 Vercel 上部署

## 工作流程：创建新应用程序
1. **选择应用程序文件夹名称**
   - 确保 `~/apps` 目录存在。
   - 项目最终会存储在 `~/apps/<app-name>` 目录下。
2. **生成应用程序 ID（appId）和访问令牌（token）**
   - 运行以下命令：
     - `npx instant-cli init-without-files`
   - 记录返回的 `appId` 和 `token` 值。
3. **生成 Next.js 应用程序**
   - 在 `~/apps` 目录下运行以下命令（该命令会创建项目文件夹）：
     - `cd ~/apps`
     - `npx create-instant-app <app-name> --next --codex --app <appId> --token <token>`
4. **初始化 Git 仓库和 GitHub 账户（如需要）**
   - 在 `~/apps/<app-name>` 目录下执行以下操作：
     - `git init`（如果尚未初始化）
     - `git add -A && git commit -m "初始化"`（如果需要）
     - `gh repo create <repo-name> --private --source . --remote origin --push`
       - 如果用户要求，可以使用 `--public` 选项将仓库设置为公开。
5. **使用 Vercel 部署应用程序**
   - 在 `~/apps/<app-name>` 目录下执行以下命令：
     - `vercel link`（或根据提示使用 `vercel project add` 或 `vercel`）
     - `vercel --prod`（部署到生产环境）

## 工作流程：编辑现有应用程序
1. 进入 `~/apps/<app-name>` 目录。
2. 阅读相关的 `AGENTS.md` 文件。
3. 拉取最新代码：
   - `git checkout main && git pull`
4. 通过编码工具（如 Codex CLI）或常规编辑方式对应用程序进行修改。
5. 根据需要测试和构建应用程序。
6. 提交更改并推送到 `main` 分支：
   - `git add -A`
   - `git commit -m "<清晰的提交信息>"
   - `git push -u origin main`
7. 将更改部署到 Vercel：
   - `vercel --prod`

## 环境变量（.env 文件）
   - 首次将应用程序部署到 Vercel 时，环境变量可能尚未配置。请使用 CLI 将本地 `.env` 文件中的环境变量上传到服务器。

## 注意事项
- 如果 `create-instant-app` 命令已经创建了仓库和远程仓库，请不要重复操作——只需确保 `origin` 仓库存在并且代码已推送到 `main` 分支即可。
- 如果应用程序已经通过 Vercel 部署过，请不要重新链接——直接进行部署即可。

## 交流方式
- 开始使用此功能时，请发送消息：“好的，我正在准备使用我的应用程序构建器功能。”
- 在完成每个步骤后，请发送更新消息。构建应用程序可能需要一些时间，请让用户保持耐心。

希望这些说明能帮助您顺利使用应用程序构建器！