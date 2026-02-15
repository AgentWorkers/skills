---
name: github
description: 查询和管理 GitHub 仓库：列出仓库、检查持续集成（CI）状态、创建问题、搜索仓库以及查看最近的活动。
metadata:
  openclaw:
    emoji: "🐙"
    requires:
      env:
        - GITHUB_TOKEN
        - GITHUB_USERNAME
      config:
        - github.token
        - github.username
---

# GitHub 集成技能

您可以直接通过 AI 助手查询和管理 GitHub 仓库。

## 功能

| 功能 | 描述 |
|------------|-------------|
| `list_repos` | 使用过滤器列出您的仓库 |
| `get_repo` | 获取特定仓库的详细信息 |
| `check_ci_status` | 检查 CI/CD 管道状态 |
| `create_issue` | 在仓库中创建新问题 |
| `create_repo` | 创建新仓库 |
| `search_repos` | 搜索您的仓库 |
| `get_recent_activity` | 获取最近的提交记录 |

## 使用方法

```
You: List my Python repos
Bot: [lists your Python repositories]

You: Check CI status on my main project
Bot: [shows CI/CD status]

You: Create an issue about the bug
Bot: [creates the issue]
```

## 设置

### 1. 生成 GitHub 个人访问令牌

1. 访问 https://github.com/settings/tokens
2. 点击 “Generate new token (classic)”
3. 输入令牌名称：`openclaw-github-skill`
4. 选择权限范围：`repo`（必需），`read:user`（可选）
5. 复制令牌

### 2. 配置凭据

**选项 A：环境变量（推荐）**

在启动 OpenClaw 之前设置环境变量：

```bash
export GITHUB_TOKEN="ghp_your_token_here"
export GITHUB_USERNAME="your_github_username"
```

**选项 B：OpenClaw 配置**

将以下配置添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "github": {
    "token": "ghp_your_token_here",
    "username": "your_username"
  }
}
```

### 3. 重启 OpenClaw

```bash
openclaw gateway restart
```

## 安全注意事项

⚠️ **保护您的令牌：**

- 绝不要将令牌提交到 Git 或公开分享
- 仅使用最低限度的权限范围（私有仓库使用 `repo`，公共仓库使用 `public_repo`）
- 如果怀疑令牌被泄露，请立即更换令牌
- 在生产环境中考虑使用 secrets manager 管理令牌

⚠️ **最佳实践：**

- 不要在共享机器上的 shell 配置文件（如 `~/.zshrc`）中存储令牌
- 本地开发时可以使用环境变量
- 在生产环境中，使用平台的 secrets/credential 管理工具

## 速率限制

- 未认证请求：每小时 60 次
- 认证请求：每小时 5,000 次

## 先决条件

- OpenClaw 代理已运行
- 拥有具有适当权限范围的 GitHub 个人访问令牌