---
name: doro-git-essentials
description: 用于版本控制、分支管理和协作的必备 Git 命令和工作流程。
version: 1.0.0
homepage: https://git-scm.com/
metadata: {"clawdbot":{"emoji":"🌳","requires":{"bins":["git"]}}}
---
# Git基础

Git是用于版本控制和协作的必备工具。以下是一些基本的Git命令。

## 初始设置

```bash
# Configure user
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# Initialize repository
git init

# Clone repository
git clone https://github.com/user/repo.git
git clone https://github.com/user/repo.git custom-name
```

## 基本工作流程

### 将文件添加到暂存区（Staging Area）并提交（Committing）
```bash
# Check status
git status

# Add files to staging
git add file.txt
git add .
git add -A  # All changes including deletions

# Commit changes
git commit -m "Commit message"

# Add and commit in one step
git commit -am "Message"

# Amend last commit
git commit --amend -m "New message"
git commit --amend --no-edit  # Keep message
```

### 查看文件更改（Viewing Changes）
```bash
# Show unstaged changes
git diff

# Show staged changes
git diff --staged

# Show changes in specific file
git diff file.txt

# Show changes between commits
git diff commit1 commit2
```

## 分支（Branching）与合并（Merging）

### 分支管理（Branch Management）
```bash
# List branches
git branch
git branch -a  # Include remote branches

# Create branch
git branch feature-name

# Switch branch
git checkout feature-name
git switch feature-name  # Modern alternative

# Create and switch
git checkout -b feature-name
git switch -c feature-name

# Delete branch
git branch -d branch-name
git branch -D branch-name  # Force delete

# Rename branch
git branch -m old-name new-name
```

### 合并（Merging）
```bash
# Merge branch into current
git merge feature-name

# Merge with no fast-forward
git merge --no-ff feature-name

# Abort merge
git merge --abort

# Show merge conflicts
git diff --name-only --diff-filter=U
```

## 远程操作（Remote Operations）

### 管理远程仓库（Managing Remotes）
```bash
# List remotes
git remote -v

# Add remote
git remote add origin https://github.com/user/repo.git

# Change remote URL
git remote set-url origin https://github.com/user/new-repo.git

# Remove remote
git remote remove origin
```

### 与远程仓库同步（Syncing with Remotes）
```bash
# Fetch from remote
git fetch origin

# Pull changes (fetch + merge)
git pull

# Pull with rebase
git pull --rebase

# Push changes
git push

# Push new branch
git push -u origin branch-name

# Force push (careful!)
git push --force-with-lease
```

## 历史记录与日志（History & Logs）

### 查看提交历史（Viewing History）
```bash
# Show commit history
git log

# One line per commit
git log --oneline

# With graph
git log --graph --oneline --all

# Last N commits
git log -5

# Commits by author
git log --author="Name"

# Commits in date range
git log --since="2 weeks ago"
git log --until="2024-01-01"

# File history
git log -- file.txt
```

### 搜索提交记录（Searching History）
```bash
# Search commit messages
git log --grep="bug fix"

# Search code changes
git log -S "function_name"

# Show who changed each line
git blame file.txt

# Find commit that introduced bug
git bisect start
git bisect bad
git bisect good commit-hash
```

## 撤销更改（Undoing Changes）

### 工作目录（Working Directory）
```bash
# Discard changes in file
git restore file.txt
git checkout -- file.txt  # Old way

# Discard all changes
git restore .
```

### 暂存区（Staging Area）
```bash
# Unstage file
git restore --staged file.txt
git reset HEAD file.txt  # Old way

# Unstage all
git reset
```

### 提交（Committing）
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Revert commit (create new commit)
git revert commit-hash

# Reset to specific commit
git reset --hard commit-hash
```

## 隐藏文件（Stashing Files）
```bash
# Stash changes
git stash

# Stash with message
git stash save "Work in progress"

# List stashes
git stash list

# Apply latest stash
git stash apply

# Apply and remove stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Delete stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

## 重新基线（Rebasing）
```bash
# Rebase current branch
git rebase main

# Interactive rebase (last 3 commits)
git rebase -i HEAD~3

# Continue after resolving conflicts
git rebase --continue

# Skip current commit
git rebase --skip

# Abort rebase
git rebase --abort
```

## 标签（Tags）
```bash
# List tags
git tag

# Create lightweight tag
git tag v1.0.0

# Create annotated tag
git tag -a v1.0.0 -m "Version 1.0.0"

# Tag specific commit
git tag v1.0.0 commit-hash

# Push tag
git push origin v1.0.0

# Push all tags
git push --tags

# Delete tag
git tag -d v1.0.0
git push origin --delete v1.0.0
```

## 高级操作

### 选择性地应用更改（Cherry-picking）
```bash
# Apply specific commit
git cherry-pick commit-hash

# Cherry-pick without committing
git cherry-pick -n commit-hash
```

### 子模块（Submodules）
```bash
# Add submodule
git submodule add https://github.com/user/repo.git path/

# Initialize submodules
git submodule init

# Update submodules
git submodule update

# Clone with submodules
git clone --recursive https://github.com/user/repo.git
```

### 清理项目（Cleaning the Project）
```bash
# Preview files to be deleted
git clean -n

# Delete untracked files
git clean -f

# Delete untracked files and directories
git clean -fd

# Include ignored files
git clean -fdx
```

## 常见工作流程

**特性分支工作流程（Feature Branch Workflow）：**
```bash
git checkout -b feature/new-feature
# Make changes
git add .
git commit -m "Add new feature"
git push -u origin feature/new-feature
# Create PR, then after merge:
git checkout main
git pull
git branch -d feature/new-feature
```

**热修复工作流程（Hotfix Workflow）：**
```bash
git checkout main
git pull
git checkout -b hotfix/critical-bug
# Fix bug
git commit -am "Fix critical bug"
git push -u origin hotfix/critical-bug
# After merge:
git checkout main && git pull
```

**同步分支（Syncing Forks）：**
```bash
git remote add upstream https://github.com/original/repo.git
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## 有用的别名（Useful Aliases）

可以将这些别名添加到`~/.gitconfig`文件中：
```ini
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = log --graph --oneline --all
    amend = commit --amend --no-edit
```

## 提示与技巧

- 经常提交代码，后续可以再完善（使用交互式重新基线功能）
- 编写有意义的提交信息
- 使用`.gitignore`文件来排除不需要跟踪的文件
- 绝不要强制推送代码到共享分支
- 在开始工作之前先拉取最新的代码
- 使用特性分支而不是主分支（main branch）进行开发
- 在合并特性分支之前先进行重新基线操作
- 使用`--force-with-lease`代替`--force`进行强制推送

## 常见问题与解决方法

**如何撤销错误的提交？（How to Undo an Accidental Commit？）**
```bash
git reset --soft HEAD~1
```

**如何恢复被删除的分支？（How to Recover a Deleted Branch？）**
```bash
git reflog
git checkout -b branch-name <commit-hash>
```

**如何修改错误的提交信息？（How to Correct a Wrong Commit Message？）**
```bash
git commit --amend -m "Correct message"
```

**如何解决合并冲突？（How to Resolve Merge Conflicts？）**
```bash
# Edit files to resolve conflicts
git add resolved-files
git commit  # Or git merge --continue
```

## 文档资源

官方文档：https://git-scm.com/doc
Pro Git书籍：https://git-scm.com/book
可视化Git教程：https://marklodato.github.io/visual-git-guide/