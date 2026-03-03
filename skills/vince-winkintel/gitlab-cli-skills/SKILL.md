---
name: gitlab-cli-skills
description: >
  **GitLab CLI（glab）命令参考与工作流程**  
  本文档提供了通过终端执行的所有GitLab操作的全面命令参考及工作流程。适用于用户需要了解GitLab CLI、glab命令、GitLab自动化、通过CLI进行MR/issue管理、CI/CD管道命令、仓库操作、身份验证设置等场景。内容涵盖了身份验证（auth）、持续集成（CI）、合并请求（MRs）、问题（issues）、发布（releases）以及仓库（repositories）等相关功能，共计30多种glab命令。同时，文档还介绍了与glab、GitLab CLI、GitLab命令及GitLab自动化相关的触发机制（triggers）。  
  **目录结构：**  
  - 身份验证（Auth）  
  - 持续集成（CI）  
  - 合并请求（MRs）  
  - 问题（Issues）  
  - 仓库（Repositories）  
  - 其他glab命令（Other glab Commands）  
  - 触发机制（Triggers）
requirements:
  binaries:
    - glab
  binaries_optional:
    - cosign
  notes: |
    Requires GitLab authentication via 'glab auth login' (stores token in ~/.config/glab-cli/config.yml).
    Some features may access sensitive files: SSH keys (~/.ssh/id_rsa for DPoP), Docker config (~/.docker/config.json for registry auth).
    Review auth workflows and script contents before autonomous use.
openclaw:
  requires:
    credentials:
      - name: GITLAB_TOKEN
        description: >
          GitLab personal access token with 'api' scope. Used by automation
          scripts (e.g. post-inline-comment.py) to post MR comments via the
          REST API. If not set, scripts fall back to reading the token from
          glab CLI config (~/.config/glab-cli/config.yml).
        required: false
        fallback: glab config (set via glab auth login)
    network:
      - description: Outbound HTTPS to your GitLab instance (default https://gitlab.com)
        scope: authenticated API calls only; HTTPS enforced; token never sent over HTTP
    write_access:
      - description: >
          Scripts in this skill can post comments, resolve threads, and approve
          merge requests on your behalf. Review scripts/post-inline-comment.py
          before use in automated or agentic contexts.
---
# GitLab CLI 技能

本文档提供了全面的 GitLab CLI（glab）命令参考及使用工作流程。

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

GitLab 的各项功能可以通过不同的 CLI 命令进行操作，这些命令按功能领域进行了分类：

**核心工作流程：**
- `glab-mr` - 合并请求（Merge Requests）：创建、审阅、批准、合并请求
- `glab-issue` - 问题（Issues）：创建、列出、更新、关闭、评论问题
- `glab-ci` - 持续集成/持续部署（CI/CD）：管道（pipelines）、作业（jobs）、日志（logs）、工件（artifacts）
- `glab-repo` - 仓库（Repositories）：克隆、创建、分支、管理仓库

**项目管理：**
- `glab-milestone` - 里程碑规划与跟踪
- `glab-iteration` - 斯普林特/迭代管理
- `glab-label` - 标签（Labels）的管理与组织
- `glab-release` - 软件发布与版本控制

**身份验证与配置：**
- `glab-auth` - 登录、登出、Docker 注册表身份验证
- `glab-config` - CLI 配置与默认设置
- `glab-ssh-key` - SSH 密钥管理
- `glab-gpg-key` - 用于提交签名的 GPG 密钥
- `glab-token` - 个人及项目访问令牌

**CI/CD 管理：**
- `glab-job` - 单个作业的操作
- `glab-schedule` - 定时执行的管道与 Cron 作业
- `glab-variable` - CI/CD 变量与敏感信息管理
- `glab-securefile` - 用于管道的安全文件
- `glab-runner` - 运行器管理：列出、暂停、删除（1.87.0 版新增）
- `glab-runner-controller` - 运行器控制器与令牌管理（仅限管理员使用）

**协作：**
- `glab-user` - 用户信息与配置
- `glab-snippet` - 代码片段（GitLab Gist）
- `glab-incident` - 事件管理
- `glab-workitems` - 工作项：任务（tasks）、关键成果（OKRs）、下一代史诗级任务（1.87.0 版新增）

**高级功能：**
- `glab-api` - 直接调用 REST API
- `glab-cluster` - Kubernetes 集群集成
- `glab-deploy-key` - 用于自动化的部署密钥
- `glab-stack` - 堆叠式/依赖性合并请求
- `glab-opentofu` - Terraform/OpenTofu 状态管理

**实用工具：**
- `glab-alias` - 自定义命令别名
- `glab-completion` - Shell 自动补全功能
- `glab-help` - 命令帮助与文档
- `glab-version` - 版本信息查询
- `glab-check-update` - 更新检查工具
- `glab-changelog` - 变更日志生成
- `glab-attestation` - 软件供应链安全检查
- `glab-duo` - GitLab Duo 人工智能助手
- `glab-mcp` - 用于集成人工智能助手的 Model Context Protocol 服务器（仅限测试）

## 何时使用 glab 与 Web UI

**适合使用 glab 的场景：**
- 在脚本中自动化 GitLab 操作
- 以终端为中心的工作流程
- 批量处理多个合并请求/问题
- 与其他 CLI 工具集成
- CI/CD 管道流程
- 需要快速操作而无需切换浏览器

**适合使用 Web UI 的场景：**
- 需要查看带有内联评论的代码差异
- 需要可视化解决合并冲突
- 需要配置仓库设置和权限
- 需要在多个项目中进行高级搜索/过滤
- 需要查看安全扫描结果
- 需要管理团队/实例级别的设置

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

### 代码审阅

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
- 需要在编码前讨论或批准工作内容
- 跟踪功能请求或错误
- 进行冲刺计划与任务分配
- 希望问题在合并请求被批准后自动关闭

**直接使用 `glab mr create` 的情况：**
- 进行快速修复或处理拼写错误
- 在现有问题的基础上进行修改
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
- 工件：`glab ci artifact`（按管道查看）或通过 `glab job` 查看作业生成的工件

### “应该克隆还是分支？”

```
What's your relationship to the repo?
├─ You have write access → glab repo clone group/project
├─ Contributing to someone else's project:
│   ├─ One-time contribution → glab repo fork + work + MR
│   └─ Ongoing contributions → glab repo fork, then sync regularly
└─ Just reading/exploring → glab repo clone (or view --web)
```

**何时使用分支（Fork）：**
- 你没有对原始仓库的写入权限
- 贡献于开源项目
- 在不影响原始代码的情况下进行实验
- 需要为长期工作创建自己的副本

**何时使用克隆（Clone）：**
- 你是具有写入权限的项目成员
- 在组织/团队仓库上工作
- 不需要个人副本

### “项目标签与团队标签的区别？”

```
Where should the label live?
├─ Used across multiple projects → glab label create --group <group>
└─ Specific to one project → glab label create (in project directory)
```

**团队级标签（Group-level Labels）：**
- 在整个组织内统一使用
- 例如：priority::high、type::bug、status::blocked
- 由团队中心管理，并被所有项目继承

**项目级标签（Project-level Labels）：**
- 适用于特定项目的工作流程
- 例如：needs-ux-review、deploy-to-staging
- 由项目维护者管理

## 相关技能

**合并请求与问题处理：**
- 首先使用 `glab-issue` 创建/跟踪问题
- 使用 `glab-mr` 创建合并请求，并在完成合并后关闭问题
- 脚本：`scripts/create-mr-from-issue.sh` 可实现自动化操作

**CI/CD 调试：**
- 使用 `glab-ci` 进行管道级别的操作
- 使用 `glab-job` 进行单个作业的操作
- 脚本：`scripts/ci-debug.sh` 可帮助快速诊断故障

**仓库操作：**
- 使用 `glab-repo` 管理仓库
- 使用 `glab-auth` 设置身份验证
- 脚本：`scripts/sync-fork.sh` 用于同步分支

**配置：**
- 使用 `glab-auth` 进行初始身份验证
- 使用 `glab-config` 设置默认值和偏好设置
- 使用 `glab-alias` 创建自定义命令别名