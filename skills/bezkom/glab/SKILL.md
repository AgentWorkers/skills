---
name: glab
description: GitLab CLI for managing issues, merge requests, CI/CD pipelines, and repositories. Use when: (1) Creating, reviewing, or merging MRs, (2) Managing GitLab issues, (3) Monitoring or triggering CI/CD pipelines, (4) Working with self-hosted GitLab instances, (5) Automating GitLab workflows from the command line.
homepage: https://gitlab.xqqx.xyz/bezko/xicotencatl/-/tree/main/skills/glab
metadata:
  openclaw:
    requires:
      bins: [glab, jq]
      envs:
        - name: GITLAB_TOKEN
          description: GitLab personal access token (glpat-xxx). Required for API access.
          secret: true
          required: true
        - name: GITLAB_HOST
          description: GitLab instance hostname (e.g., gitlab.example.org). Defaults to gitlab.com.
          required: false
        - name: TIMEOUT
          description: Pipeline/MR wait timeout in seconds. Defaults vary by script.
          required: false
        - name: INTERVAL
          description: Polling interval in seconds for watch scripts. Default 5-10s.
          required: false
    install:
      - id: brew
        kind: brew
        package: glab
        label: Install glab via Homebrew
      - id: apt
        kind: apt
        package: glab
        label: Install glab via apt
      - id: jq-brew
        kind: brew
        package: jq
        label: Install jq via Homebrew
      - id: jq-apt
        kind: apt
        package: jq
        label: Install jq via apt
---

# GitLab CLI (glab)

GitLab的官方命令行工具（CLI），用于通过终端管理问题、合并请求、流水线等操作。

> **来源：** 受[NikiforovAll/glab-skill](https://github.com/NikiforovAll/claude-code-rules/tree/main/plugins/handbook-glab/skills/glab-skill)的启发，该资源来自Smithery平台。

## 先决条件

**必需的二进制文件：**
- `glab` - GitLab CLI工具
- `jq` - JSON处理工具（用于脚本编写和API解析）

**必需的凭证：**
- `GITLAB_TOKEN` - 具有`api`权限范围的GitLab个人访问令牌

**可选配置：**
- `GITLAB_HOST` - 自托管的GitLab实例（默认值：gitlab.com）

```bash
# Verify installation
glab --version
jq --version

# Authenticate (interactive)
glab auth login

# Or via environment
export GITLAB_TOKEN="glpat-xxxxxxxxxxxxxxxxxxxx"
export GITLAB_HOST="gitlab.example.org"  # for self-hosted

# Verify auth
glab auth status
```

## 快速参考

**合并请求：**
```bash
glab mr create --title "Fix" --description "Closes #123"
glab mr list --reviewer=@me          # MRs awaiting your review
glab mr checkout 123                  # Test MR locally
glab mr approve 123 && glab mr merge 123
```

**问题：**
```bash
glab issue create --title "Bug" --label=bug
glab issue list --assignee=@me
glab issue close 456
```

**持续集成/持续部署（CI/CD）：**
```bash
glab ci status                        # Current pipeline status
glab pipeline ci view                 # Watch pipeline live
glab ci lint                          # Validate .gitlab-ci.yml
glab ci retry                         # Retry failed pipeline
```

**在仓库外部工作：**
```bash
glab mr list -R owner/repo            # Specify repository
glab api projects/:id/merge_requests  # Direct API access
```

## 核心工作流程

### 创建并合并合并请求（Merge Requests）

```bash
# 1. Push branch
git push -u origin feature-branch

# 2. Create MR
glab mr create --title "Add feature" --description "Implements X" --reviewer=alice,bob --label="enhancement"

# 3. After approval, merge
glab mr approve 123
glab mr merge 123 --remove-source-branch
```

### 审查合并请求（Review Merge Requests）

```bash
# List MRs for review
glab mr list --reviewer=@me

# Checkout and test
glab mr checkout 123

# Approve or comment
glab mr approve 123
glab mr note 123 -m "Looks good, just one suggestion..."
```

### 监控流水线（Monitor Pipelines）

```bash
# Watch current branch pipeline
glab pipeline ci view

# Check specific pipeline
glab ci view 456

# View failed job logs
glab ci trace

# Retry
glab ci retry
```

### 使用API

```bash
# GET with pagination (use query params, NOT flags)
glab api "projects/:id/merge_requests?per_page=100&state=opened"

# Paginate all results
glab api --paginate "projects/:id/jobs?per_page=100"

# POST
glab api --method POST projects/:id/issues --field title="Bug" --field description="Details"
```

### 回复讨论帖子（Reply to Discussion Threads）

`glab mr note`用于创建独立的评论。若要在讨论帖子中回复，请使用以下命令：

```bash
# 1. Find discussion_id
glab api "projects/:id/merge_requests/123/discussions" | jq '.[] | select(.notes[].id == 456) | .id'

# 2. Reply
glab api --method POST "projects/:id/merge_requests/123/discussions/{discussion_id}/notes" --field body="Reply text"
```

## 自托管GitLab

```bash
# Set default host
export GITLAB_HOST=gitlab.example.org

# Or per-command
glab mr list -R gitlab.example.org/owner/repo
```

## 脚本（Scripts）

| 脚本 | 描述 |
|--------|-------------|
| `glab-mr-await.sh` | 等待合并请求的审批以及流水线的成功执行 |
| `glab-pipeline-watch.sh` | 监控流水线的执行情况（通过退出码判断CI状态） |

```bash
# Wait for MR to be approved and merged
./scripts/glab-mr-await.sh 123 --timeout 600

# Watch pipeline, exit 0 on success, 1 on failure
./scripts/glab-pipeline-watch.sh --timeout 300
```

**脚本环境变量：**
- `TIMEOUT` - 最大等待时间（以秒为单位，具体取决于脚本）
- `INTERVAL` - 轮询间隔（以秒为单位，默认为5-10秒）

## 故障排除

| 错误 | 解决方案 |
|-------|-----|
| `命令未找到：glab` | 安装glab工具 |
| `命令未找到：jq` | 安装jq工具 |
| `401未经授权` | 设置`GITLAB_TOKEN`或运行`glab auth login`命令 |
| `404项目未找到` | 核实仓库名称和权限 |
| 该目录不是Git仓库 | 使用`-R owner/repo`参数 |
| 源代码分支已存在合并请求 | 使用`glab mr list`命令查看现有合并请求 |

有关详细的故障排除信息，请参阅**references/troubleshooting.md**。

## 附加资源

- **references/commands-detailed.md** - 包含所有命令参数的完整参考文档 |
- **references/troubleshooting.md** - 详细的错误场景及解决方法 |

在需要了解特定命令参数或调试问题时，请参考这些资源。

## 最佳实践

1. 始终验证身份认证：`glab auth status`
2. 将合并请求与问题关联：在描述中注明“关闭问题#123”
3. 在推送之前检查CI配置：`glab ci lint`
4. 使用`--output=json`参数进行脚本编写
5. 大多数命令都支持`--web`参数，可点击链接在浏览器中查看结果