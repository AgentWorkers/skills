---
name: github-passwordless-setup
description: 使用 SSH 密钥和个人访问令牌（Personal Access Tokens）完成 GitHub 的无密码认证设置。在进行 Git 操作和 GitHub API 调用时，无需输入密码或重新进行身份验证。
---
# GitHub 无密码登录设置

本指南将详细介绍如何使用 SSH 密钥和个人访问令牌（Personal Access Tokens, PAT）在 GitHub 上实现无密码登录。配置完成后，您将无需再为任何 Git 操作或 GitHub CLI 命令输入密码。

**已验证兼容的系统：**
- ✅ macOS 10.15 及更高版本（在 14.4 上测试通过）
- ✅ Linux（Ubuntu、Debian、Fedora、Arch）
- ✅ Windows（WSL2、Git Bash）

## 🎯 该方案解决的问题

**配置前的问题：**
- ❌ 每次执行推送/拉取操作时都需要输入密码
- ❌ GitHub CLI 需要重新认证
- ❌ 令牌过期会导致工作流程中断
- ❌ HTTPS 需要反复输入凭据

**配置后的优势：**
- ✅ 所有 Git 操作（推送/拉取/克隆）无需密码
- ✅ 创建仓库无需密码
- ✅ 管理问题/拉取请求（Issue/PR）无需密码
- ✅ 认证信息永久有效（无需定期更新）

## 🚀 快速配置

**一键自动化配置：**

```bash
curl -fsSL https://raw.githubusercontent.com/happydog-intj/github-passwordless-setup/master/setup.sh | bash
```

**或按照以下手动步骤操作：**

## 📋 手动配置

### 第 1 部分：SSH 密钥配置

SSH 密钥可实现无需密码的 Git 操作（推送/拉取/克隆）。

#### 第 1 步：检查现有 SSH 密钥

```bash
ls -la ~/.ssh/*.pub
```

如果您看到 `id_ed25519.pub` 或 `id_rsa.pub`，则表示您已经拥有 SSH 密钥。可以直接跳到第 3 步。

#### 第 2 步：生成新的 SSH 密钥

**推荐使用：ED25519（安全性更高）**

```bash
ssh-keygen -t ed25519 -C "your-email@example.com"
```

**如果系统不支持 ED25519，可以使用 RSA：**

```bash
ssh-keygen -t rsa -b 4096 -C "your-email@example.com"
```

**生成密钥时：**
- 按 Enter 键选择默认路径（`~/.ssh/id_ed25519`）
- 选择密码短语（可选，但建议设置）
- macOS 会将密码短语保存到 Keychain 中

#### 第 3 步：复制公钥

```bash
# macOS
cat ~/.ssh/id_ed25519.pub | pbcopy

# Linux (xclip)
cat ~/.ssh/id_ed25519.pub | xclip -selection clipboard

# Linux (xsel)
cat ~/.ssh/id_ed25519.pub | xsel --clipboard

# Or just display and copy manually
cat ~/.ssh/id_ed25519.pub
```

#### 第 4 步：将密钥添加到 GitHub

1. 访问：https://github.com/settings/ssh/new
2. **标题**：输入您的计算机名称（macOS/Linux）
3. **密钥类型**：选择“Authentication Key”
4. **密钥内容**：粘贴您的公钥
5. 点击“Add SSH key”

#### 第 5 步：测试 SSH 连接

```bash
ssh -T git@github.com
```

预期输出：
```
Hi username! You've successfully authenticated, but GitHub does not provide shell access.
```

### 第 2 部分：GitHub 个人访问令牌（Personal Access Tokens, PAT）

PAT 可实现无需密码的 GitHub CLI 操作（创建仓库、管理问题/拉取请求）。

#### 第 1 步：生成令牌

访问：https://github.com/settings/tokens/new

**配置选项：**
- **备注**：选择“OpenClaw CLI Token”或其他合适的描述
- **有效期**：选择“无有效期”或“90 天”
- **选择权限范围**：
  - ✅ **repo**（所有子权限）
  - ✅ **workflow**（如果使用 GitHub Actions）
  - ✅ **delete_repo**（如果需要删除仓库）
  - ✅ **admin:org**（如果需要管理组织）
点击“Generate token”并立即复制令牌（此步骤仅显示一次）。

令牌格式：`ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

#### 第 2 步：安装 GitHub CLI

**macOS：**
```bash
brew install gh
```

**Linux（Debian/Ubuntu）：**
```bash
type -p curl >/dev/null || (sudo apt update && sudo apt install curl -y)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh -y
```

**其他 Linux 发行版：**
请参考：https://github.com/cli/cli/blob/trunk/docs/install_linux.md

#### 第 3 步：配置令牌

```bash
# Method 1: Interactive (paste when prompted)
gh auth login --with-token
# Then paste your token and press Enter

# Method 2: One-line (replace YOUR_TOKEN)
echo "ghp_YOUR_TOKEN_HERE" | gh auth login --with-token
```

#### 第 4 步：将 Git 协议设置为 SSH

```bash
gh config set git_protocol ssh
```

这样，`gh` 命令将使用 SSH 而非 HTTPS 进行 Git 操作。

### 第 3 部分：验证配置

#### 验证 SSH 配置

```bash
# Test SSH connection
ssh -T git@github.com

# Expected: Hi username! You've successfully authenticated...
```

#### 验证 GitHub CLI

```bash
# Check authentication status
gh auth status

# Expected: ✓ Logged in to github.com account username

# Test API access
gh api user --jq '.login'

# Expected: your-username
```

#### 验证整个工作流程

```bash
# Test creating a repository (will create and delete)
gh repo create test-auth-$(date +%s) --public --description "Test" \
  && echo "✅ Create: SUCCESS" \
  && gh repo delete $(gh repo list --limit 1 --json name --jq '.[0].name') --yes \
  && echo "✅ Delete: SUCCESS"
```

所有操作都应无需输入密码即可完成。

## 🔄 将现有仓库转换为 SSH 协议

如果您使用的是 HTTPS 协议的仓库，请按照以下步骤操作：

```bash
# Check current remote
git remote -v

# If it shows https://github.com/...
# Convert to SSH
git remote set-url origin git@github.com:username/repo.git

# Verify
git remote -v
# Should show: git@github.com:username/repo.git
```

**批量转换目录中的所有仓库：**

```bash
find . -name ".git" -type d | while read gitdir; do
  cd "$gitdir/.."
  if git remote get-url origin 2>/dev/null | grep -q "https://github.com"; then
    REPO=$(git remote get-url origin | sed 's|https://github.com/|git@github.com:|')
    git remote set-url origin "$REPO"
    echo "✅ Converted: $(pwd)"
  fi
  cd - > /dev/null
done
```

## 🛠️ 自动化配置脚本

将以下代码保存为 `setup.sh` 文件：

```bash
#!/bin/bash
set -e

echo "🔐 GitHub Passwordless Setup"
echo "============================"
echo ""

# Check for existing SSH key
if [ -f ~/.ssh/id_ed25519.pub ]; then
    echo "✅ SSH key already exists"
    SSH_KEY=$(cat ~/.ssh/id_ed25519.pub)
elif [ -f ~/.ssh/id_rsa.pub ]; then
    echo "✅ SSH key already exists (RSA)"
    SSH_KEY=$(cat ~/.ssh/id_rsa.pub)
else
    echo "📝 Generating new ED25519 SSH key..."
    ssh-keygen -t ed25519 -C "$(whoami)@$(hostname)" -f ~/.ssh/id_ed25519 -N ""
    SSH_KEY=$(cat ~/.ssh/id_ed25519.pub)
    echo "✅ SSH key generated"
fi

echo ""
echo "🔑 Your public SSH key:"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "$SSH_KEY"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📋 Next steps:"
echo "1. Copy the key above"
echo "2. Visit: https://github.com/settings/ssh/new"
echo "3. Paste the key and save"
echo "4. Come back and press Enter to continue"
read -p "Press Enter after adding the key to GitHub..."

# Test SSH
echo ""
echo "🧪 Testing SSH connection..."
if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated"; then
    echo "✅ SSH authentication successful!"
else
    echo "❌ SSH authentication failed. Please check your key on GitHub."
    exit 1
fi

# Check for GitHub CLI
echo ""
if ! command -v gh &> /dev/null; then
    echo "📦 GitHub CLI not found. Install it from:"
    echo "   macOS: brew install gh"
    echo "   Linux: https://github.com/cli/cli/blob/trunk/docs/install_linux.md"
    exit 1
fi

# Configure GitHub CLI
echo "🎫 Configuring GitHub CLI..."
echo "Please enter your GitHub Personal Access Token:"
echo "(Visit https://github.com/settings/tokens/new if you don't have one)"
echo ""
gh auth login --with-token

# Set git protocol to SSH
gh config set git_protocol ssh

# Verify
echo ""
echo "🔍 Verifying configuration..."
if gh auth status &> /dev/null; then
    echo "✅ GitHub CLI authenticated"
    USERNAME=$(gh api user --jq '.login')
    echo "✅ Username: $USERNAME"
else
    echo "❌ GitHub CLI authentication failed"
    exit 1
fi

echo ""
echo "🎉 Setup complete!"
echo ""
echo "You can now:"
echo "  • Push/pull without passwords: git push"
echo "  • Create repos instantly: gh repo create my-project --public"
echo "  • Manage issues/PRs: gh issue create, gh pr list"
echo ""
```

使其可执行并运行：

```bash
chmod +x setup.sh
./setup.sh
```

## 🔍 故障排除

### SSH 相关问题

**问题：“Permission denied (publickey)”**

```bash
# Check SSH agent
ssh-add -l

# If empty or error, add your key
ssh-add ~/.ssh/id_ed25519

# macOS: Add to Keychain permanently
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```

**问题：“Host key verification failed”**

```bash
# Remove old host key
ssh-keygen -R github.com

# Reconnect (will prompt to add new key)
ssh -T git@github.com
```

### GitHub CLI 相关问题

**问题：“Requires authentication”**

```bash
# Check token validity
gh auth status

# Re-authenticate
gh auth logout
gh auth login --with-token
```

**问题：“Token scopes insufficient”**

**解决方法：**创建权限更广泛的令牌：**
- 访问：https://github.com/settings/tokens
- 删除旧令牌
- 重新生成令牌，并确保选择所需的权限范围（如 `repo`、`workflow`、`delete_repo`）

### 其他常见问题

**检查配置文件：**

```bash
# SSH config
cat ~/.ssh/config

# GitHub CLI config
cat ~/.config/gh/hosts.yml

# Git config
git config --global --list
```

## 🔒 安全最佳实践

### SSH 密钥

1. **使用 ED25519 密钥**（比 RSA 更安全）
2. **设置密码短语**（可选，但建议设置）
3. **使用 ssh-agent**（macOS 使用 Keychain，Linux 使用 gnome-keyring）
4. **切勿共享私钥**（特别是 `id_ed25519` 文件）
5. **一旦发现密钥被泄露，立即在 https://github.com/settings/keys 上撤销该密钥**

### 个人访问令牌

1. **仅选择必要的权限范围**
2. **设置合理的有效期**（建议设置为 90 天以确保安全，或选择“无有效期”以方便使用）
3. **在不再需要时，在 https://github.com/settings/tokens 上撤销令牌**
4. **切勿将令牌提交到仓库中**
5. **定期更新令牌（建议每 90 天更新一次）

## 📚 高级配置

### SSH 配置文件

创建 `~/.ssh/config` 文件以自定义配置：

```ssh
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519
  AddKeysToAgent yes
  UseKeychain yes
```

### 多个 GitHub 账户

如何使用多个 GitHub 账户进行操作：

```ssh
# ~/.ssh/config
Host github-personal
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_personal

Host github-work
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519_work
```

**使用特定账户克隆仓库：**

```bash
git clone git@github-personal:username/repo.git
git clone git@github-work:company/repo.git
```

### Git 别名

在 `~/.gitconfig` 文件中添加别名：

```ini
[alias]
  pushf = push --force-with-lease
  undo = reset --soft HEAD~1
  amend = commit --amend --no-edit
  sync = !git fetch --all && git pull
```

## 🌐 环境变量

用于自动化操作的可选环境变量：

```bash
# GitHub CLI
export GH_TOKEN="ghp_xxxxx"  # Auto-auth for gh commands

# Git
export GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519"  # Force specific key
```

将这些变量添加到您的 shell 配置文件（`~/.bashrc` 或 `~/.zshrc`）中：

```bash
# GitHub CLI auto-auth (optional)
if [ -f ~/.config/gh/token ]; then
  export GH_TOKEN=$(cat ~/.config/gh/token)
fi
```

## 🔄 维护

### 更新 SSH 密钥

```bash
# Generate new key
ssh-keygen -t ed25519 -C "new-email@example.com"

# Add to GitHub
cat ~/.ssh/id_ed25519.pub | pbcopy
# Visit: https://github.com/settings/ssh/new

# Update old repos (if using specific key in config)
git config core.sshCommand "ssh -i ~/.ssh/id_ed25519"
```

### 更新 GitHub 令牌

```bash
# Create new token at https://github.com/settings/tokens/new
# Configure it
echo "ghp_NEW_TOKEN" | gh auth login --with-token

# Revoke old token at https://github.com/settings/tokens
```

## 📊 HTTPS 与 SSH 的对比

| 特性 | HTTPS | SSH |
|---------|-------|-----|
| **认证方式** | 用户名 + 令牌 | SSH 密钥 |
| **是否需要密码** | 每次操作都需要 | 无需 |
| **配置难度** | 较低 | 中等 |
| **安全性** | 一般 | 非常高 |
| **企业防火墙** | 通常允许通过 | 有时会被阻止 |
| **推荐人群** | 初学者 | 日常使用用户 |

## 🎯 常见工作流程

### 创建新项目

```bash
# Create repo and push in one go
gh repo create my-project --public --source=. --push

# Or step by step
gh repo create my-project --public
git remote add origin git@github.com:username/my-project.git
git push -u origin main
```

### 克隆私有仓库

```bash
# SSH (no password)
git clone git@github.com:username/private-repo.git

# Check access
gh repo view username/private-repo
```

### 管理问题/拉取请求

```bash
# Create issue
gh issue create --title "Bug found" --body "Description"

# List issues
gh issue list

# Close issue
gh issue close 123
```

## 🤝 贡献代码

发现问题或改进点？欢迎提交拉取请求！

## 📄 许可证

本文档采用 MIT 许可协议。

## 🔗 相关链接

- [GitHub SSH 文档](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [GitHub CLI 手册](https://cli.github.com/manual/)
- [OpenClaw](https://github.com/openclaw/openclaw)

---

**本文档专为重视自动化开发的开发者编写。**