# SKILL.md - OpenClaw 迁移指南

## 目的  
当工作区正在将 Clawd 项目重命名为 OpenClaw 时，本文档会存储在仓库中，以便所有人员（包括人类开发者和辅助工具）都能遵循统一的迁移流程。文档详细说明了在代码库、文档和工具进行更新时，哪些内容需要被移动、重命名或进行测试。

## 使用场景  
- 当有人询问迁移进度、计划或需要迁移检查清单时（例如：“我们如何将 Clawd 迁移到 OpenClaw？”）；  
- 当您准备重命名目录、更新配置文件或解释旧文件的存放位置时；  
- 当新贡献者需要明确的操作步骤，以确保重命名不会影响构建或自动化流程时。

## 迁移步骤  
1. **分析当前项目结构**：  
   - `clawdbot/` 是现有的应用程序根目录，包含 `src/`、`apps/`、`docs/`、`skills/`、`package.json`、测试文件以及相关工具。  
   - 仓库根目录还存放着代理元数据文件（`AGENTS.md`）、角色描述文件（`SOUL.md`、`MEMORY.md` 等）以及 `skills.json` 等资源文件。  

2. **创建 OpenClaw 的根目录**：  
   - 将 `clawdbot/` 重命名为 `openclaw/`，或将其内容复制到一个新的 `openclaw/` 分支中。  
   - 保留隐藏文件（如 `.github`、`.agent`、`.ox` 配置文件等），并确保 `package.json`、`pnpm-workspace.yaml` 和 `lockfile` 保持同步。  

3. **更新引用**：  
   - 在文档、`README.md`、技能定义文件、配置文件以及持续集成（CI）工作流中查找所有包含 “Clawd” 的地方，并将其全部替换为 “OpenClaw”。  
   - 特别注意 `README-header.png`、`docs/*.md`、`AGENTS.md` 和 `SOUL.md`（这些文件中可能仍会使用旧名称）。  
   - 更新所有引用 `clawdbot` 路径的 CLI/`npm run` 脚本。  

4. **迁移通用元数据**：  
   - 确定 `AGENTS.md`、`SOUL.md`、`MEMORY.md`、`skills.json` 等文件在新应用程序根目录中的位置。  
   - 将对用户有帮助的文件（如角色介绍、系统状态信息等）保留在仓库根目录中。  

5. **验证工具配置**：  
   - 从 `openclaw/` 目录重新运行 `pnpm test`、`pnpm lint` 以及所有文档构建脚本，确保新结构能够正常与现有的持续集成系统配合使用。  

6. **更新文档**：  
   - 在 `README.md` 中说明迁移已完成，并告知贡献者仓库现在包含的是 OpenClaw 项目的所有内容。  
   - 文档中还需说明如何从新的目录启动应用程序。  

7. **清理旧文件**：  
   - 在新结构稳定后，删除或归档旧的 `clawdbot/` 目录；  
   - 或者保留一个说明性的 `README.md` 文件，以便日后追溯迁移过程。  

## 验证标准：  
- `package.json` 中的脚本（`dev`、`build`、`bootstrap`）仍能正确指向目标文件夹。  
- `pnpm` 工作区的引用路径和 `tsconfig` 文件中的路径应指向新的 `openclaw/` 目录。  
- `skills.json` 中列出的技能目录和版本信息保持正确。  
- 持续集成/持续交付（CI/CD）工作流（如 GitHub Actions、Fly、Render）的配置文件中应使用新的项目名称。  

## 沟通方式：  
- 在迁移审查过程中与评审人员分享本文档，以便他们确认每个迁移步骤的正确性。  
- 在向 Ivan 发送迁移总结时，附上已移动文件的列表以及新的 `openclaw/` 目录的入口信息。  

## 触发条件：  
- 当 Ivan 提出与迁移相关的任何问题（如 “迁移”、“重命名” 或 “将 Clawd 迁移到 OpenClaw”）时；  
- 在准备发布使用 OpenClaw 品牌的新版本时。