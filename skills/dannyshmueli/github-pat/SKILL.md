---
name: github-pat
description: 使用个人访问令牌（Personal Access Tokens）与 GitHub 交互。这种访问方式安全且由用户自行控制，无需 OAuth 或完整的账户权限。支持克隆（clone）、推送（push）、创建分支（branch）、提交 Pull Request（PR）以及处理问题（issues）。适用于用户需要操作 GitHub 仓库的场景。
---

# GitHub Personal Access Tokens (PAT)

使用个人访问令牌（Personal Access Tokens, PAT）与 GitHub 进行交互。用户通过 PAT 的权限范围（scopes）来控制访问权限。

## 设置

用户提供他们的 PAT：
```
1. Create PAT at github.com/settings/tokens
2. Select scopes (repo for full, public_repo for public only)
3. Provide token to agent
```

将 PAT 保存在 `TOOLS.md` 文件中，或通过 `--token` 参数传递。

## 命令

```bash
# List repos you have access to
python3 scripts/gh.py repos [--token TOKEN]

# Clone a repo
python3 scripts/gh.py clone owner/repo [--token TOKEN]

# Create branch
python3 scripts/gh.py branch <branch-name> [--repo owner/repo]

# Commit and push
python3 scripts/gh.py push "<message>" [--branch branch] [--repo owner/repo]

# Open a pull request
python3 scripts/gh.py pr "<title>" [--body "description"] [--base main] [--head branch]

# Create an issue
python3 scripts/gh.py issue "<title>" [--body "description"] [--repo owner/repo]

# View repo info
python3 scripts/gh.py info owner/repo
```

## 安全模型

- **用户通过 PAT 的权限范围来控制访问权限**
- **不使用 OAuth** – 因此不会出现“允许完全访问”的提示
- **最小权限原则** – 用户创建 PAT 时仅授予所需的最低权限范围
- **支持针对特定仓库的细粒度访问权限设置**

## 令牌存储

代理将令牌存储在 `TOOLS.md` 文件的 `### GitHub` 部分中。切勿在日志或消息中泄露令牌信息。