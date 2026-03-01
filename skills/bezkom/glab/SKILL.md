---
name: glab
description: GitLab CLI for managing issues, merge requests, CI/CD pipelines, and repositories. Use when: (1) Creating, reviewing, or merging MRs, (2) Managing GitLab issues, (3) Monitoring or triggering CI/CD pipelines, (4) Working with self-hosted GitLab instances, (5) Automating GitLab workflows from the command line. Requires GITLAB_TOKEN (recommend minimal scopes). The `glab api` command enables arbitrary API calls - use read-only tokens when possible.
homepage: https://github.com/bezko/openclaw-skills/tree/main/skills/glab
metadata:
  openclaw:
    requires:
      bins: [glab, jq]
      envs:
        - name: GITLAB_TOKEN
          description: GitLab personal access token. Recommend minimal scopes (read_api for read-only).
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

GitLab 的官方命令行工具（CLI），允许您通过终端管理问题、合并请求（Merge Requests）、持续集成/持续交付（CI/CD）流程等。

> **来源：** 受 [NikiforovAll/glab-skill](https://github.com/NikiforovAll/claude-code-rules/tree/main/plugins/handbook-glab/skills/glab-skill) 的启发，该资源来自 Smithery。

## ⚠️ 安全提示

`glab api` 命令会使用您的 GitLab 个人访问令牌（Token）提供不受限制的 API 访问权限。  
- 如果令牌被泄露或权限设置过于宽松，可能会导致项目被删除、配置被修改或敏感信息被泄露。  
**建议：** 使用权限范围尽可能小的令牌：  
  - `read_api`：仅限读取操作  
  - `api`：全权限（仅在需要写入操作时使用）  
- 对于自动化脚本，建议使用具有有限权限范围的项目级令牌。  
- 除非必要，否则切勿使用具有 `sudo` 权限范围的令牌。

## 先决条件

**必备软件：**  
- `glab`：GitLab CLI 工具  
- `jq`：JSON 处理工具（用于脚本编写和 API 数据解析）  

**必备凭据：**  
- `GITLAB_TOKEN`：GitLab 个人访问令牌  

**可选配置：**  
- `GITLAB_HOST`：自托管的 GitLab 服务器地址（默认值：gitlab.com）

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

- **合并请求（Merge Requests）：**  
```bash
glab mr create --title "Fix" --description "Closes #123"
glab mr list --reviewer=@me          # MRs awaiting your review
glab mr checkout 123                  # Test MR locally
glab mr approve 123 && glab mr merge 123
```

- **问题（Issues）：**  
```bash
glab issue create --title "Bug" --label=bug
glab issue list --assignee=@me
glab issue close 456
```

- **持续集成/持续交付（CI/CD）：**  
```bash
glab ci status                        # Current pipeline status
glab pipeline ci view                 # Watch pipeline live
glab ci lint                          # Validate .gitlab-ci.yml
glab ci retry                         # Retry failed pipeline
```

- **在非 GitLab 仓库中操作：**  
```bash
glab mr list -R owner/repo            # Specify repository
```

## 高级 API 访问

有关 `glab api` 的使用方法，请参阅 **references/api-advanced.md**。该命令允许执行任意 GitLab API 调用，必须使用权限范围适当的令牌。

## 核心工作流程

### 创建并合并合并请求（Create and Merge MR）  
```bash
# 1. Push branch
git push -u origin feature-branch

# 2. Create MR
glab mr create --title "Add feature" --description "Implements X" --reviewer=alice,bob --label="enhancement"

# 3. After approval, merge
glab mr approve 123
glab mr merge 123 --remove-source-branch
```

### 审查合并请求（Review MR）  
```bash
# List MRs for review
glab mr list --reviewer=@me

# Checkout and test
glab mr checkout 123

# Approve or comment
glab mr approve 123
glab mr note 123 -m "Looks good, just one suggestion..."
```

### 监控管道（Monitor Pipelines）  
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

## 自托管 GitLab  

```bash
# Set default host
export GITLAB_HOST=gitlab.example.org

# Or per-command
glab mr list -R gitlab.example.org/owner/repo
```

## 脚本（Scripts）  

| 脚本名 | 说明 |
|--------|-------------|
| `glab-mr-await.sh` | 等待合并请求获得批准并完成管道执行 |
| `glab-pipeline-watch.sh` | 监控管道的执行情况（通过退出代码判断 CI 进度） |

```bash
# Wait for MR to be approved and merged
./scripts/glab-mr-await.sh 123 --timeout 600

# Watch pipeline, exit 0 on success, 1 on failure
./scripts/glab-pipeline-watch.sh --timeout 300
```

**脚本环境变量：**  
- `TIMEOUT`：最大等待时间（单位：秒，具体取决于脚本）  
- `INTERVAL`：轮询间隔（单位：秒，默认为 5-10 秒）

## 故障排除

| 错误信息 | 解决方案 |
|-------|-----|
| “命令未找到：glab” | 安装 glab 工具 |
| “命令未找到：jq” | 安装 jq 工具 |
| “401 Unauthorized” | 设置正确的 `GITLAB_TOKEN` 或执行 `glab auth login` 命令进行登录 |
| “404 项目未找到” | 确认仓库名称和权限设置 |
| “当前分支已存在合并请求” | 使用 `glab mr list` 命令查看现有合并请求 |

有关详细的故障排除信息，请参阅 **references/troubleshooting.md**。

## 额外资源

- **references/api-advanced.md**：包含 `glab api` 的安全使用指南  
- **references/commands-detailed.md**：包含所有命令及其参数的完整参考  
- **references/troubleshooting.md**：详细说明各种错误情况及其解决方法  

在需要了解特定命令参数或调试问题时，请查阅这些文档。

## 最佳实践：  
1. 始终验证用户身份：执行 `glab auth status` 命令  
2. 对于读取操作，使用权限范围最小的令牌  
3. 在合并请求的描述中注明关联的问题编号（例如：“关闭问题 #123”）  
4. 在推送代码前检查 CI 配置：执行 `glab ci lint`  
5. 使用 `--output=json` 选项生成 JSON 格式的输出结果  
6. 大多数命令都支持 `--web` 选项，可将其结果在浏览器中查看