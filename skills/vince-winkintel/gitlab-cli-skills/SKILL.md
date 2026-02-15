---
name: gitlab-cli-skills
description: **GitLab CLI（glab）命令参考与工作流程**  
本文档提供了通过终端执行的所有GitLab操作的完整命令参考及工作流程。适用于用户提及GitLab CLI、glab命令、GitLab自动化、通过CLI进行MR/issue管理、CI/CD管道命令、仓库操作、身份验证设置等场景。内容涵盖了身份验证（auth）、持续集成（CI）、合并请求（MRs）、问题（issues）、发布（releases）以及仓库（repos）等领域的30多种glab命令。同时，文档还介绍了与glab、GitLab CLI、GitLab命令及GitLab自动化相关的触发机制（triggers）。  

**目录结构：**  
- 身份验证（Auth）  
- 持续集成（CI）  
- 合并请求（MRs）  
- 问题（Issues）  
- 仓库（Repos）  
- 其他glab命令（Other glab Commands）  

**使用说明：**  
- 当用户需要了解如何使用GitLab CLI或相关功能时，请参考相应章节。  
- 文档中的代码示例、命令及URL均保持原样。  
- 技术术语（如OpenClaw、ClawHub、API、CLI等）会保留英文形式。  
- 代码块中的注释仅用于解释相关功能。  

**注意：**  
- 本文档旨在帮助用户更高效地使用GitLab CLI，因此请确保您已具备基本的GitLab使用经验。  

如需进一步了解或使用特定功能，请参阅相关子章节。
requirements:
  binaries:
    - glab
  binaries_optional:
    - cosign
  notes: |
    Requires GitLab authentication via 'glab auth login' (stores token in ~/.config/glab-cli/config.yml).
    Some features may access sensitive files: SSH keys (~/.ssh/id_rsa for DPoP), Docker config (~/.docker/config.json for registry auth).
    Review auth workflows and script contents before autonomous use.
---

# GitLab CLI 技能

全面的 GitLab CLI（glab）命令参考和工作流程。

## 快速入门

```bash
# First time setup
glab auth login

# Common operations
glab mr create --fill              # Create MR from current branch
glab issue create                  # Create issue
glab ci view                       # View pipeline status
glab repo view --web              # Open repo in browser
```

## 技能分类

本技能根据 GitLab 的不同功能领域分为以下子技能：

**核心工作流程：**
- `glab-mr` - 合并请求（Merge Requests）：创建、审核、批准、合并
- `glab-issue` - 问题（Issues）：创建、列出、更新、关闭、评论
- `glab-ci` - 持续集成/持续交付（CI/CD）：管道（pipelines）、作业（jobs）、日志（logs）、工件（artifacts）
- `glab-repo` - 仓库（repositories）：克隆（clone）、创建（create）、分支（fork）、管理（manage）

**项目管理：**
- `glab-milestone` - 发布计划和里程碑跟踪
- `glab-iteration` - 斯普林特/迭代管理
- `glab-label` - 标签（labels）管理和组织
- `glab-release` - 软件发布和版本控制

**身份验证与配置：**
- `glab-auth` - 登录、登出、Docker 注册表身份验证
- `glab-config` - CLI 配置和默认设置
- `glab-ssh-key` - SSH 密钥管理
- `glab-gpg-key` - 用于提交签名的 GPG 密钥
- `glab-token` - 个人和项目访问令牌

**CI/CD 管理：**
- `glab-job` - 单个作业操作
- `glab-schedule` - 定时管道和 Cron 作业
- `glab-variable` - CI/CD 变量和秘密（secrets）
- `glab-securefile` - 管道的安全文件
- `glab-runner-controller` - 运行器控制器和令牌管理（仅限管理员）

**协作：**
- `glab-user` - 用户信息和配置文件
- `glab-snippet` - 代码片段（GitLab Gist）
- `glab-incident` - 事件管理

**高级功能：**
- `glab-api` - 直接进行 REST API 调用
- `glab-cluster` - Kubernetes 集群集成
- `glab-deploy-key` - 自动化部署密钥
- `glab-stack` - 堆叠/依赖合并请求
- `glab-opentofu` - Terraform/OpenTofu 状态管理

**工具：**
- `glab-alias` - 自定义命令别名
- `glab-completion` - Shell 自动补全功能
- `glab-help` - 命令帮助和文档
- `glab-version` - 版本信息
- `glab-check-update` - 更新检查器
- `glab-changelog` - 变更日志生成
- `glab-attestation` - 软件供应链安全
- `glab-duo` - GitLab Duo 人工智能助手
- `glab-mcp` - 用于集成人工智能助手的 Model Context Protocol 服务器（仅限测试）

## 何时使用 glab 与 Web UI

**在以下情况下使用 glab：**
- 在脚本中自动化 GitLab 操作
- 在以终端为中心的工作流程中
- 批量操作（多个合并请求/问题）
- 与其他 CLI 工具集成
- CI/CD 管道工作流程
- 需要快速导航且无需切换浏览器

**在以下情况下使用 Web UI：**
- 需要复杂差异对比和内联评论
- 需要可视化合并冲突解决
- 需要配置仓库设置和权限
- 需要在多个项目中进行高级搜索/过滤
- 需要查看安全扫描结果
- 需要管理组/实例级别的设置

## 常见工作流程

### 日常开发

```bash
# Start work on issue
glab issue view 123
git checkout -b 123-feature-name

# Create MR when ready
glab mr create --fill --draft

# Mark ready for review
glab mr update --ready

# Merge after approval
glab mr merge --when-pipeline-succeeds --remove-source-branch
```

### 代码审查

```bash
# List your review queue
glab mr list --reviewer=@me --state=opened

# Review an MR
glab mr checkout 456
glab mr diff
npm test

# Approve
glab mr approve 456
glab mr note 456 -m "LGTM! Nice work on the error handling."
```

### CI/CD 调试

```bash
# Check pipeline status
glab ci status

# View failed jobs
glab ci view

# Get job logs
glab ci trace <job-id>

# Retry failed job
glab ci retry <job-id>
```

## 决策树

### “我应该先创建合并请求（MR）还是先处理问题？”

```
Need to track work?
├─ Yes → Create issue first (glab issue create)
│         Then: glab mr for <issue-id>
└─ No → Direct MR (glab mr create --fill)
```

**当以下情况时，使用 `glab issue create` + `glab mr`：**
- 需要在编码前进行讨论或获得批准
- 跟踪功能请求或错误
- 进行冲刺计划和任务分配
- 希望问题在合并请求被合并后自动关闭

**当以下情况时，直接使用 `glab mr create`：**
- 进行快速修复或处理拼写错误
- 在现有问题上进行修改
- 进行紧急修复或更改

### “应该使用哪个 CI 命令？”

```
What do you need?
├─ Overall pipeline status → glab ci status
├─ Visual pipeline view → glab ci view
├─ Specific job logs → glab ci trace <job-id>
├─ Download build artifacts → glab ci artifact <ref> <job-name>
├─ Validate config file → glab ci lint
├─ Trigger new run → glab ci run
└─ List all pipelines → glab ci list
```

**快速参考：**
- 管道级别：`glab ci status`、`glab ci view`、`glab ci run`
- 作业级别：`glab ci trace`、`glab job retry`、`glab job view`
- 工件：通过 `glab ci artifact` 查看管道级别的工件，或通过 `glab job` 查看作业级别的工件

### “应该克隆还是分支？”

```
What's your relationship to the repo?
├─ You have write access → glab repo clone group/project
├─ Contributing to someone else's project:
│   ├─ One-time contribution → glab repo fork + work + MR
│   └─ Ongoing contributions → glab repo fork, then sync regularly
└─ Just reading/exploring → glab repo clone (or view --web)
```

**在以下情况下分支：**
- 你没有对原始仓库的写入权限
- 贡献于开源项目
- 在不影响原始仓库的情况下进行实验
- 需要自己的副本进行长期工作

**在以下情况下克隆：**
- 你是具有写入权限的项目成员
- 在组织/团队仓库上工作
- 不需要个人副本

### “项目标签与组标签？”

```
Where should the label live?
├─ Used across multiple projects → glab label create --group <group>
└─ Specific to one project → glab label create (in project directory)
```

**组级标签：**
- 在整个组织中保持标签的一致性
- 例如：priority::high、type::bug、status::blocked
- 由中央管理，并被项目继承

**项目级标签：**
- 项目特定的工作流程
- 例如：needs-ux-review、deploy-to-staging
- 由项目维护者管理

## 相关技能

**合并请求和问题工作流程：**
- 首先使用 `glab-issue` 创建/跟踪任务
- 使用 `glab-mr` 创建会关闭问题的合并请求
- 脚本：`scripts/create-mr-from-issue.sh` 可自动化此过程

**CI/CD 调试：**
- 使用 `glab-ci` 进行管道级别的操作
- 使用 `glab-job` 进行单个作业的操作
- 脚本：`scripts/ci-debug.sh` 用于快速诊断故障

**仓库操作：**
- 使用 `glab-repo` 进行仓库管理
- 使用 `glab-auth` 进行身份验证设置
- 脚本：`scripts/sync-fork.sh` 用于分支同步

**配置：**
- 使用 `glab-auth` 进行初始身份验证
- 使用 `glab-config` 设置默认值和偏好设置
- 使用 `glab-alias` 创建自定义快捷键