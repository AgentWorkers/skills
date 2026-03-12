---
name: gitlab-cli-skills
description: >
  **GitLab CLI（glab）命令参考及工作流程**  
  本文档提供了通过终端执行的所有GitLab操作的全面命令参考和工作流程。适用于用户需要了解GitLab CLI、glab命令、GitLab自动化、通过CLI进行MR/issue管理、CI/CD管道命令、仓库操作、身份验证设置以及任何GitLab终端操作的场景。  
  **涵盖的内容包括：**  
  - 身份验证（Authentication）  
  - 持续集成与持续部署（Continuous Integration/Deployment, CI/CD）  
  - 代码审查请求（Merge Requests, MRs）与问题（Issues）管理  
  - 仓库（Repos）操作  
  - 以及其他30多种glab命令  
  **相关子技能链接：**  
  - 身份验证（Authentication）  
  - 持续集成与持续部署（CI/CD）  
  - 代码审查请求（Merge Requests, MRs）与问题（Issues）管理  
  - 仓库（Repos）操作  
  **触发条件：**  
  - glab命令  
  - GitLab CLI命令  
  - GitLab终端操作  
  - GitLab自动化流程  
  请根据实际需求查阅相应子技能文档，以获取更详细的信息和操作指南。
metadata: {"openclaw": {"requires": {"bins": ["glab"], "anyBins": ["cosign"]}, "install": [{"id": "brew", "kind": "brew", "formula": "glab", "bins": ["glab"], "label": "Install glab (brew)"}, {"id": "download", "kind": "download", "url": "https://gitlab.com/gitlab-org/cli/-/releases", "label": "Download glab binary"}]}}
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

这些技能根据 GitLab 的不同功能领域进行了分类：

**核心工作流程：**
- `glab-mr` - 合并请求（Merge Requests）：创建、审核、批准、合并
- `glab-issue` - 问题（Issues）：创建、列出、更新、关闭、评论
- `glab-ci` - 持续集成/持续部署（CI/CD）：管道（Pipelines）、作业（Jobs）、日志（Logs）、工件（Artifacts）
- `glab-repo` - 仓库（Repositories）：克隆（Clone）、创建（Create）、分叉（Fork）、管理（Manage）

**项目管理：**
- `glab-milestone` - 发布计划和里程碑跟踪（Release Planning and Milestone Tracking）
- `glab-iteration` - 断裂/迭代管理（Sprint/Iteration Management）
- `glab-label` - 标签管理（Label Management）
- `glab-release` - 软件发布和版本控制（Software Releases and Versioning）

**认证与配置：**
- `glab-auth` - 登录（Login）、登出（Logout）、Docker 注册表认证（Docker Registry Auth）
- `glab-config` - CLI 配置和默认设置（CLI Configuration and Defaults）
- `glab-ssh-key` - SSH 密钥管理（SSH Key Management）
- `glab-gpg-key` - 用于提交签名的 GPG 密钥（GPG Keys for Commit Signing）
- `glab-token` - 个人和项目访问令牌（Personal and Project Access Tokens）

**CI/CD 管理：**
- `glab-job` - 单个作业操作（Individual Job Operations）
- `glab-schedule` - 定时管道和 Cron 作业（Scheduled Pipelines and Cron Jobs）
- `glab-variable` - CI/CD 变量（CI/CD Variables and Secrets）
- `glab-securefile` - 用于管道的安全文件（Secure Files for Pipelines）
- `glab-runner` - 运行器管理：列出、暂停、删除（新增于 v1.87.0）
- `glab-runner-controller` - 运行器控制器和令牌管理（实验性，仅限管理员使用，EXPERIMENTAL, admin-only）

**协作：**
- `glab-user` - 用户资料和信息（User Profiles and Information）
- `glab-snippet` - 代码片段（GitLab Gists）
- `glab-incident` - 事件管理（Incident Management）
- `glab-workitems` - 工作项：任务（Tasks）、OKR（OKRs）、关键结果（Key Results）、下一代史诗任务（Next-Gen Epics）（新增于 v1.87.0）

**高级功能：**
- `glab-api` - 直接调用 REST API（Direct REST API Calls）
- `glab-cluster` - Kubernetes 集群集成（Kubernetes Cluster Integration）
- `glab-deploy-key` - 自动化部署密钥（Deploy Keys for Automation）
- `glab-quick-actions` - GitLab 命令快捷操作（GitLab Command Quick Actions）
- `glab-stack` - 堆叠/依赖合并请求（Stacked/Dependent Merge Requests）
- `glab-opentofu` - Terraform/OpenTofu 状态管理（Terraform/OpenTofu State Management）

**工具：**
- `glab-alias` - 自定义命令别名（Custom Command Aliases）
- `glab-completion` - Shell 自动补全（Shell Autocompletion）
- `glab-help` - 命令帮助和文档（Command Help and Documentation）
- `glab-version` - 版本信息（Version Information）
- `glab-check-update` - 更新检查器（Update Checker）
- `glab-changelog` - 变更日志生成（Changelog Generation）
- `glab-attestation` - 软件供应链安全（Software Supply Chain Security）
- `glab-duo` - GitLab Duo 人工智能助手（GitLab Duo AI Assistant）
- `glab-mcp` - 用于 AI 助手集成的模型上下文协议服务器（Model Context Protocol Server, EXPERIMENTAL）

## v1.89.0 更新

> **v1.89.0+**：12 个子技能中的 18 个命令现在支持 `--output json` / `-F json` 选项，以输出结构化的数据，非常适合代理/自动化脚本解析。受影响的子技能包括：`glab-release`、`glab-ci`、`glab-milestone`、`glab-schedule`、`glab-mr`、`glab-repo`、`glab-label`、`glab-deploy-key`、`glab-ssh-key`、`glab-gpg-key`、`glab-cluster`、`glab-opentofu`。

其他 v1.89.0 的变更：
- **`glab-auth`**：在自托管实例上，`glab auth login` 现在会分别提示 SSH 主机和 API 主机名。
- **`glab-stack`**：新增了 `glab stack sync --update-base` 标志，用于将堆栈重新基接到更新后的基础分支。
- **`glab-release`**：`--notes` / `--notes-file` 选项现在在 `glab release create` 和 `glab release update` 命令中是可选的。

## 何时使用 glab 与 Web UI

**在以下情况下使用 glab：**
- 在脚本中自动化 GitLab 操作
- 在以终端为中心的工作流程中
- 批量操作（多个合并请求/问题）
- 与其他 CLI 工具集成
- CI/CD 管道工作流程
- 需要在不切换浏览器的情况下快速导航

**在以下情况下使用 Web UI：**
- 需要查看带有内联评论的复杂差异
- 需要可视化解决合并冲突
- 需要配置仓库设置和权限
- 需要在项目间进行高级搜索/过滤
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

### “我应该先创建合并请求还是先处理问题？”

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
- 进行快速修复或修正拼写错误
- 基于现有问题进行修改
- 进行紧急修复或更改

### “我应该使用哪个 CI 命令？”

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
- 工件：`glab ci artifact`（按管道）或通过 `glab job` 查看作业工件

### “应该克隆还是分叉？”

```
What's your relationship to the repo?
├─ You have write access → glab repo clone group/project
├─ Contributing to someone else's project:
│   ├─ One-time contribution → glab repo fork + work + MR
│   └─ Ongoing contributions → glab repo fork, then sync regularly
└─ Just reading/exploring → glab repo clone (or view --web)
```

**在以下情况下分叉：**
- 你没有对原始仓库的写入权限
- 贡献于开源项目
- 在不影响原始代码的情况下进行实验
- 需要一个自己的副本进行长期工作

**在以下情况下克隆：**
- 你是具有写入权限的项目成员
- 在组织/团队仓库上工作
- 不需要个人副本

### “项目标签和组标签的区别？”

```
Where should the label live?
├─ Used across multiple projects → glab label create --group <group>
└─ Specific to one project → glab label create (in project directory)
```

**组级标签：**
- 在整个组织中保持标签的一致性
- 例如：priority::high, type::bug, status::blocked
- 由中央管理，并被所有项目继承

**项目级标签：**
- 适用于特定项目的工作流程
- 例如：needs-ux-review, deploy-to-staging
- 由项目维护者管理

## 相关技能

**合并请求和问题工作流程：**
- 首先使用 `glab-issue` 创建/跟踪问题
- 使用 `glab-mr` 创建合并请求，并在完成后关闭问题
- 脚本：`scripts/create-mr-from-issue.sh` 可自动化此过程

**CI/CD 调试：**
- 使用 `glab-ci` 进行管道级别的操作
- 使用 `glab-job` 进行单个作业的操作
- 脚本：`scripts/ci-debug.sh` 可用于快速诊断故障

**仓库操作：**
- 使用 `glab-repo` 进行仓库管理
- 使用 `glab-auth` 进行认证设置
- 脚本：`scripts/sync-fork.sh` 用于分叉同步

**配置：**
- 使用 `glab-auth` 进行初始认证
- 使用 `glab-config` 设置默认值和偏好设置
- 使用 `glab-alias` 创建自定义快捷命令