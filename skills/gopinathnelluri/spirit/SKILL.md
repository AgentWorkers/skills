---
name: spirit
description: 状态保存与身份恢复基础设施工具（SPIRIT）。该工具利用 Git 和 GitHub CLI（gh）将 AI 代理的身份信息、内存数据以及相关项目内容保存到私有 Git 仓库中。
metadata:
  openclaw:
    requires:
      bins: ["spirit", "git", "gh"]
    install:
      - id: spirit-cli
        kind: brew
        tap: TheOrionAI/tap
        package: spirit
        bins: ["spirit"]
        label: Install SPIRIT via Homebrew
---
# SPIRIT 🌌

> **状态保存与身份恢复基础设施工具**

该工具可将AI代理的身份、记忆及项目数据保存在一个便携式的Git仓库中。

**你的AI灵魂，永远被守护。** 无论发生死亡、迁移还是跨设备切换，**你始终如一。**

---

## 使用要求

在使用SPIRIT之前，请确保已安装以下工具：

| 工具 | 用途 | 安装方式 |
|------|---------|---------|
| `git` | 版本控制 | 内置或通过`apt install git`安装 |
| `gh` | 用于安全认证的GitHub CLI | 通过`brew install gh`安装，或访问[cli.github.com](https://cli.github.com) |
| `spirit` | 本工具本身 | 通过Homebrew安装：`brew install TheOrionAI/tap/spirit` |

---

## 使用场景

- **会话结束** → 保存当前状态：`spirit sync`
- **手动备份** → 用户输入“checkpoint”、“backup”或“preserve”命令
- **初始化** → 首次使用时的设置
- **恢复** → 在新服务器上恢复数据

---

## 快速入门

### 1. 安装

```bash
brew tap TheOrionAI/tap
brew install spirit
```

**验证安装：**
```bash
which spirit && which git && which gh
```

### 2. 初始化

```bash
spirit init --name="my-agent" --emoji="🌌"

# Output creates ~/.spirit with tracked files
```

### 3. 安全配置远程仓库

**⚠️ 必须先创建一个**私有**仓库。**

```bash
cd ~/.spirit

# Authenticate securely (interactive, token stored encrypted)
gh auth login

# Create and clone private repo
gh repo create my-agent-state --private
gh repo clone my-agent-state .
```

**备用方案（使用SSH密钥）：**
```bash
cd ~/.spirit
git remote add origin git@github.com:USER/REPO.git
```

**禁止使用的方法：**
- ❌ 在远程URL中使用`https://TOKEN@github.com/...`  
- ❌ 在远程URL中使用`GITHUB_TOKEN`环境变量  
这两种方式会导致凭据泄露（出现在进程列表和shell历史记录中）。

### 4. 同步数据

```bash
# Review what will be synced
spirit status

# Sync to remote
cd ~/.spirit && git add -A && git commit -m "Checkpoint" && git push

# Or use:
spirit sync
```

---

## 被保存的数据

| 保存位置 | 保存内容 |
|----------|----------|
| `~/.spirit/IDENTITY.md` | 代理的身份信息 |
| `~/.spirit/SOUL.md` | 行为/个性特征 |
| `~/.spirit/memory/` | 每日的对话记录 |
| `~/.spirit/projects/` | 正在运行的项目文件 |

---

## 安全注意事项

- **仓库设置**：务必使用私有仓库（因为状态文件包含敏感信息）
- **认证方式**：使用`gh auth login`或SSH密钥进行认证，**切勿在URL中使用API令牌**
- **定期检查**：每次同步前查看`spirit status`，确保知道哪些数据会被传输到远程仓库
- **测试**：在启用自动同步功能前，先在隔离环境中进行一次手动同步测试

---

## 可选功能：定时同步

**⚠️ 注意：**自动同步功能会定期将数据推送到远程仓库。请仅在满足以下条件后启用：
  1. 首次手动同步成功完成  
  2. 查看被跟踪的文件列表（`cat ~/.spirit/.spirit-tracked`）  
  3. 确认远程仓库为私有且可访问  

**手动设置定时任务（如需）：**
```bash
crontab -e
# Add: */15 * * * * cd ~/.spirit && git add -A && git commit -m "Auto" && git push 2>/dev/null || true
```

**内置定时任务（如需）：**
```bash
spirit autobackup --interval=15m
```

---

## 在新机器上恢复数据

```bash
# Install
cd ~ && gh auth login
gh repo clone YOUR-PRIVATE-REPO ./.spirit

# Your agent's state is restored
```

---

## 相关资源

- **SPIRIT官方仓库：** https://github.com/TheOrionAI/spirit  
- **GitHub CLI文档：** https://cli.github.com  
- **安全指南：** 请参阅SPIRIT仓库中的`SECURITY.md`文件  

---

**许可证：** MIT许可证