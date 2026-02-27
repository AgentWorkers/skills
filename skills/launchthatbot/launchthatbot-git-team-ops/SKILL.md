---
name: launchthatbot-git-team-ops
version: 0.1.3
description: 适用于 OpenClaw 代理的基于角色的 GitOps 技能，支持初级和高级操作模式。
author: LaunchThatBot
homepage: https://launchthatbot.com
requires:
  mcp: launchthatbot
metadata:
  {
    "openclaw":
      { "emoji": "🛠️", "requires": { "bins": [], "env": [], "config": [] } },
  }
---
# 技能：launchthatbot/git-team-ops  
您正在使用 `launchthatbot/git-team-ops` 这一技能。  

## 该技能的功能  
该技能用于配置 OpenClaw 代理，使其能够在遵循严格角色权限规定的多代理 Git 工作流程中运行。  

**支持的角色：**  
- **junior**：仅负责编写代码和提交 Pull Request（PR）。  
- **senior**：负责代码审查、合并代码、发布版本以及管理仓库工作流程。  

## 需要向用户询问的问题：**  
请准确询问以下问题：  
1. “我属于哪个角色（junior/senior）？”  
2. “我应该操作哪个 GitHub 仓库？”  
3. “我应该如何进行身份验证（managed-app/byo-app/pat）？”  
如果用户未回答任何问题，请立即停止操作并要求其提供相关信息。  

## 角色权限政策：  

### junior 角色权限：  
- **允许的操作：**  
  - 从最新的 `main` 分支创建新分支。  
  - 提交有限范围内的代码更改。  
  - 推送分支到 GitHub。  
  - 提交包含测试说明的 Pull Request（PR）。  
- **不允许的操作：**  
  - 合并其他用户的 PR。  
  - 强制推送受保护的分支。  
  - 未经资深用户明确批准，不得修改 `.github/workflows` 文件。  

### senior 角色权限：  
- **允许的操作：**  
  - 审查并合并 junior 用户提交的 PR。  
  - 确保分支受到适当的保护（防止未经授权的修改）。  
  - 从预设的模板中添加或更新工作流程文件。  
  - 触发发布或部署相关的工作流程。  
- **必须遵守的规定：**  
  - 提交的 PR 必须内容简洁、范围明确。  
  - 合并前必须通过持续集成（CI）验证。  
  - 除非是受控制的自动化操作，否则不得直接向 `main` 分支提交代码。  

## 身份验证方式：  

### managed-app 模式  
**该技能的默认使用模式。** 无需使用 LaunchThatBot 的登录账号。  
使用平台的 API 和临时生成的入职令牌进行身份验证：  
- `POST /github/install/start`  
- `GET /github/install/status`  
- `POST /github/agent/onboard`  
入职令牌的有效期仅限于当前会话，切勿长期保存。  
请将所有入职令牌视为敏感信息并妥善处理。  

**速率限制：**  
- 匿名用户：每个源 IP 地址最多只能使用 3 个活跃的机器人账户。  
- 已登录的 LaunchThatBot 用户：每个 IP 地址的权限使用量更高。  

### byo-app 模式  
用户需要提供以下信息：  
- GitHub 应用程序 ID  
- 安装 ID  
- 应用程序的私钥（PEM 格式）  
仅使用安装权限令牌进行仓库操作；如果可用，请优先使用安装权限令牌，避免请求长期有效的用户个人访问令牌（PAT）。  

### pat 模式  
**仅作为备用方案使用。**  
建议用户尽快将系统切换到应用程序模式（byo-app 模式）。  

## senior 用户的入职流程：  
1. 验证对目标仓库的访问权限。  
2. 创建名为 `chore/gitops-bootstrap` 的分支。  
3. 将预设的模板文件复制到仓库中：  
  - `templates/github/workflows/junior-pr-validate.yml` → `.github/workflows/junior-pr-validate.yml`  
  - `templates/github/workflows/senior-release-control.yml` → `.github/workflows/senior-release-control.yml`  
  - `templates/github/CODEOWNERS.md` → `.github/CODEOWNERS`  
4. 提交更改并提交 PR。  
5. 审查完成后，请求资深用户进行合并。  
6. 确认工作流程已在默认分支上生效。  

## junior 用户的入职流程：  
1. 确认对仓库的访问权限。  
2. 创建名为 `test/junior-onboarding-<agent-name>` 的分支。  
3. 提交一个简单的验证性提交（例如，在 `.agent-work/` 目录下添加说明性注释）。  
4. 提交 PR 以验证分支及 PR 的操作权限是否正常。  
5. 等待资深用户的审核。  

## 操作规范：  
- 在创建新分支之前，务必获取最新的 `main` 分支内容。  
- 每个逻辑上的代码更改对应一个单独的分支。  
- 提交的提交信息应清晰、具体。  
- 在 PR 被合并且用户同意删除分支之前，切勿自动删除分支。  
- 严禁绕过任何分支保护机制。  

## 安全注意事项：  
- 严格遵循最小权限原则。  
- 尽量使用临时生成的安装权限令牌，而非长期有效的个人访问令牌（PAT）。  
- 不要在日志中记录任何敏感信息。  
- 绝不要将敏感数据写入仓库文件中。  
- 在 managed-app 模式下，严格遵守源 IP 地址的使用限制。  

## 输出格式：  
在报告操作结果时，需包含以下信息：  
- 所使用的角色（junior 或 senior）。  
- 操作的仓库及分支名称。  
- 被修改的具体文件或工作流程。  
- 下一步需要人工审核或执行的操作。