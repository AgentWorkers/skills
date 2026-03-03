---
name: gitlab-cli-skills
description: >
  **GitLab CLI（glab）命令参考及工作流程**  
  本文档提供了通过终端执行的所有GitLab操作的全面命令参考与工作流程。适用于以下场景：用户提及GitLab CLI、glab命令、GitLab自动化、通过CLI进行MR/issue管理、CI/CD管道命令、仓库操作、身份验证设置，以及任何与GitLab终端相关的操作。  
  内容涵盖以下专题：身份验证（auth）、持续集成（CI）、合并请求（MRs）、问题（issues）、发布（releases）、仓库（repos）等，以及30多种其他glab命令。同时，还介绍了与glab、GitLab CLI、GitLab命令及GitLab终端相关的触发机制。
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

本文档提供了 GitLab CLI（glab）的全面命令参考及相关工作流程。

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

GitLab CLI 的各项功能可根据不同的领域进行分类：

**核心工作流程：**
- `glab-mr` - 合并请求（Merge Requests）：创建、审阅、批准、合并
- `glab-issue` - 问题（Issues）：创建、列出、更新、关闭、评论
- `glab-ci` - 持续集成/持续部署（CI/CD）：管道（pipelines）、作业（jobs）、日志（logs）、工件（artifacts）
- `glab-repo` - 仓库（repositories）：克隆（clone）、创建（create）、分支（fork）、管理（manage）

**项目管理：**
- `glab-milestone` - 发布计划和里程碑跟踪
- `glab-iteration` - 斯普林特/迭代管理
- `glab-label` - 标签（labels）的管理与组织
- `glab-release` - 软件发布与版本控制

**认证与配置：**
- `glab-auth` - 登录、登出、Docker 注册表认证
- `glab-config` - CLI 配置与默认设置
- `glab-ssh-key` - SSH 密钥管理
- `glab-gpg-key` - 用于提交签名的 GPG 密钥
- `glab-token` - 个人及项目访问令牌

**CI/CD 管理：**
- `glab-job` - 单个作业的操作
- `glab-schedule` - 计划好的管道和定时任务
- `glab-variable` - CI/CD 变量与秘密信息
- `glab-securefile` - 用于管道的安全文件
- `glab-runner` - 运行器管理：列出、暂停、删除（v1.87.0 新增）
- `glab-runner-controller` - 运行器控制器与令牌管理（仅限管理员使用）

**协作：**
- `glab-user` - 用户信息与配置
- `glab-snippet` - 代码片段（GitLab Gist）
- `glab-incident` - 事件管理
- `glab-workitems` - 工作项：任务（tasks）、关键结果（key results）、下一代史诗级任务（next-gen epics）（v1.87.0 新增）

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
- `glab-version` - 版本信息
- `glab-check-update` - 更新检查工具
- `glab-changelog` - 变更日志生成
- `glab-attestation` - 软件供应链安全检查
- `glab-duo` - GitLab Duo 人工智能助手
- `glab-mcp` - 用于集成人工智能助手的 Model Context Protocol 服务器（仅限测试）

## 何时使用 GitLab CLI 与 Web UI

**适合使用 GitLab CLI 的场景：**
- 在脚本中自动化 GitLab 操作
- 以终端为中心的工作流程
- 批量操作（多个合并请求/问题）
- 与其他 CLI 工具集成
- 持续集成/持续部署管道流程
- 需要快速操作而无需切换浏览器

**适合使用 Web UI 的场景：**
- 复杂的差异对比与内联评论
- 可视化的合并冲突解决
- 配置仓库设置与权限
- 在多个项目中进行高级搜索/过滤
- 查看安全扫描结果
- 管理组级/实例级设置

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

### “我应该先创建合并请求还是先处理问题？”

```
Need to track work?
├─ Yes → Create issue first (glab issue create)
│         Then: glab mr for <issue-id>
└─ No → Direct MR (glab mr create --fill)
```

**当需要先讨论或获得批准后再进行编码时，使用：**
- `glab issue create` + `glab mr`
- 用于跟踪功能请求或错误
- 斯普林特计划与任务分配
- 希望问题在合并请求被批准后自动关闭

**当需要快速修复或修正拼写错误时，直接使用：**
- `glab mr create`
- 从现有问题开始处理
- 紧急修复或临时更改

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
- 工件：`glab ci artifact`（按管道）或通过 `glab job` 查看作业生成的工件

### “应该克隆还是分支？”

```
What's your relationship to the repo?
├─ You have write access → glab repo clone group/project
├─ Contributing to someone else's project:
│   ├─ One-time contribution → glab repo fork + work + MR
│   └─ Ongoing contributions → glab repo fork, then sync regularly
└─ Just reading/exploring → glab repo clone (or view --web)
```

**在以下情况下使用分支：**
- 没有对原始仓库的写入权限
- 贡献于开源项目
- 在不影响原始代码的情况下进行实验
- 需要一个自己的副本用于长期工作

**在以下情况下使用克隆：**
- 是项目成员且具有写入权限
- 在组织/团队仓库上工作
- 不需要个人副本

### “项目标签与组标签的区别？”

**组级标签：**
- 在整个组织中统一使用
- 例如：priority::high、type::bug、status::blocked
- 由中央管理，并被所有项目继承

**项目级标签：**
- 适用于特定项目的工作流程
- 例如：needs-ux-review、deploy-to-staging
- 由项目维护者管理

## 相关技能

**合并请求与问题处理：**
- 首先使用 `glab-issue` 创建/跟踪问题
- 使用 `glab-mr` 创建合并请求并关闭相关问题
- 脚本：`scripts/create-mr-from-issue.sh` 可自动化此过程

**CI/CD 调试：**
- 使用 `glab-ci` 进行管道级别的操作
- 使用 `glab-job` 进行单个作业的操作
- 脚本：`scripts/ci-debug.sh` 用于快速诊断故障

**仓库操作：**
- 使用 `glab-repo` 管理仓库
- 使用 `glab-auth` 设置认证
- 脚本：`scripts/sync-fork.sh` 用于分支同步

**配置：**
- 使用 `glab-auth` 进行初始认证
- 使用 `glab-config` 设置默认值和偏好设置
- 使用 `glab-alias` 创建自定义命令别名