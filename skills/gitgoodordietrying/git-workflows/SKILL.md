---
name: git-workflows
description: 高级 Git 操作（超出基本的 add/commit/push 功能）：  
适用于以下场景：  
- 切基（rebase）操作  
- 二分查找（bisecting）错误  
- 使用工作树（worktrees）进行并行开发  
- 通过 reflog 恢复代码历史  
- 管理子树（subtrees）和子模块（submodules）  
- 解决合并冲突（merge conflicts）  
- 在不同分支之间进行选择性合并（cherry-picking）  
- 以及处理单仓库（monorepo）项目。
metadata: {"clawdbot":{"emoji":"🌿","requires":{"bins":["git"]},"os":["linux","darwin","win32"]}}
---

# Git 工作流程

介绍在实际开发中使用的高级 Git 操作，包括交互式 rebase、bisect、worktree、reflog 恢复、子树（subtree）、子模块（submodule）、稀疏检出（sparse checkout）、冲突解决（conflict resolution）以及单仓库模式（monorepo）等。

## 使用场景

- 在合并之前清理提交历史（交互式 rebase）
- 查找引入错误的提交（bisect）
- 同时在多个分支上工作（worktree）
- 恢复丢失的提交或撤销错误操作（reflog）
- 在多个仓库之间管理共享代码（子树/子模块）
- 解决复杂的合并冲突
- 在不同分支或分支之间选择性地应用提交（cherry-pick）
- 处理大型单仓库项目（稀疏检出）

## 交互式 Rebase

### 压缩（Squash）/ 重新排序/ 编辑提交

```bash
# Rebase last 5 commits interactively
git rebase -i HEAD~5

# Rebase onto main (all commits since diverging)
git rebase -i main
```

编辑器会显示一个可选提交列表：

```
pick a1b2c3d Add user model
pick e4f5g6h Fix typo in user model
pick i7j8k9l Add user controller
pick m0n1o2p Add user routes
pick q3r4s5t Fix import in controller
```

可用的命令：
```
pick   = use commit as-is
reword = use commit but edit the message
edit   = stop after this commit to amend it
squash = merge into previous commit (keep both messages)
fixup  = merge into previous commit (discard this message)
drop   = remove the commit entirely
```

### 常见用法

```bash
# Squash fix commits into their parent
# Change "pick" to "fixup" for the fix commits:
pick a1b2c3d Add user model
fixup e4f5g6h Fix typo in user model
pick i7j8k9l Add user controller
fixup q3r4s5t Fix import in controller
pick m0n1o2p Add user routes

# Reorder commits (just move lines)
pick i7j8k9l Add user controller
pick m0n1o2p Add user routes
pick a1b2c3d Add user model

# Split a commit into two
# Mark as "edit", then when it stops:
git reset HEAD~
git add src/model.ts
git commit -m "Add user model"
git add src/controller.ts
git commit -m "Add user controller"
git rebase --continue
```

### 自动压缩提交信息（Automated commit message compression）

```bash
# When committing a fix, reference the commit to squash into
git commit --fixup=a1b2c3d -m "Fix typo"
# or
git commit --squash=a1b2c3d -m "Additional changes"

# Later, rebase with autosquash
git rebase -i --autosquash main
# fixup/squash commits are automatically placed after their targets
```

### 中止或继续操作

```bash
git rebase --abort      # Cancel and restore original state
git rebase --continue   # Continue after resolving conflicts or editing
git rebase --skip       # Skip the current commit and continue
```

## Bisect（查找错误）

### 通过提交历史进行二分查找

```bash
# Start bisect
git bisect start

# Mark current commit as bad (has the bug)
git bisect bad

# Mark a known-good commit (before the bug existed)
git bisect good v1.2.0
# or: git bisect good abc123

# Git checks out a middle commit. Test it, then:
git bisect good   # if this commit doesn't have the bug
git bisect bad    # if this commit has the bug

# Repeat until git identifies the exact commit
# "abc123 is the first bad commit"

# Done — return to original branch
git bisect reset
```

### 使用测试脚本进行自动化 bisect

```bash
# Fully automatic: git runs the script on each commit
# Script must exit 0 for good, 1 for bad
git bisect start HEAD v1.2.0
git bisect run ./test-for-bug.sh

# Example test script
cat > /tmp/test-for-bug.sh << 'EOF'
#!/bin/bash
# Return 0 if bug is NOT present, 1 if it IS
npm test -- --grep "login should redirect" 2>/dev/null
EOF
chmod +x /tmp/test-for-bug.sh
git bisect run /tmp/test-for-bug.sh
```

### 在构建失败时使用 bisect

```bash
# If a commit doesn't compile, skip it
git bisect skip

# Skip a range of known-broken commits
git bisect skip v1.3.0..v1.3.5
```

## Worktree（并行分支）

### 同时在多个分支上工作

```bash
# Add a worktree for a different branch
git worktree add ../myproject-hotfix hotfix/urgent-fix
# Creates a new directory with that branch checked out

# Add a worktree with a new branch
git worktree add ../myproject-feature -b feature/new-thing

# List worktrees
git worktree list

# Remove a worktree when done
git worktree remove ../myproject-hotfix

# Prune stale worktree references
git worktree prune
```

### 使用场景

```bash
# Review a PR while keeping your current work untouched
git worktree add ../review-pr-123 origin/pr-123

# Run tests on main while developing on feature branch
git worktree add ../main-tests main
cd ../main-tests && npm test

# Compare behavior between branches side by side
git worktree add ../compare-old release/v1.0
git worktree add ../compare-new release/v2.0
```

## Reflog（恢复提交历史）

### 查看 Git 记录的所有信息

```bash
# Show reflog (all HEAD movements)
git reflog
# Output:
# abc123 HEAD@{0}: commit: Add feature
# def456 HEAD@{1}: rebase: moving to main
# ghi789 HEAD@{2}: checkout: moving from feature to main

# Show reflog for a specific branch
git reflog show feature/my-branch

# Show with timestamps
git reflog --date=relative
```

### 从错误中恢复

```bash
# Undo a bad rebase (find the commit before rebase in reflog)
git reflog
# Find: "ghi789 HEAD@{5}: checkout: moving from feature to main" (pre-rebase)
git reset --hard ghi789

# Recover a deleted branch
git reflog
# Find the last commit on that branch
git branch recovered-branch abc123

# Recover after reset --hard
git reflog
git reset --hard HEAD@{2}   # Go back 2 reflog entries

# Recover a dropped stash
git fsck --unreachable | grep commit
# or
git stash list  # if it's still there
git log --walk-reflogs --all -- stash  # find dropped stash commits
```

## Cherry-Pick

### 将特定提交复制到另一个分支

```bash
# Pick a single commit
git cherry-pick abc123

# Pick multiple commits
git cherry-pick abc123 def456 ghi789

# Pick a range (exclusive start, inclusive end)
git cherry-pick abc123..ghi789

# Pick without committing (stage changes only)
git cherry-pick --no-commit abc123

# Cherry-pick from another remote/fork
git remote add upstream https://github.com/other/repo.git
git fetch upstream
git cherry-pick upstream/main~3   # 3rd commit from upstream's main
```

### 在执行 cherry-pick 时处理冲突

```bash
# If conflicts arise:
# 1. Resolve conflicts in the files
# 2. Stage resolved files
git add resolved-file.ts
# 3. Continue
git cherry-pick --continue

# Or abort
git cherry-pick --abort
```

## 子树（Subtree）和子模块（Submodule）

### 子树（Subtree）：将代码复制到当前仓库

```bash
# Add a subtree
git subtree add --prefix=lib/shared https://github.com/org/shared-lib.git main --squash

# Pull updates from upstream
git subtree pull --prefix=lib/shared https://github.com/org/shared-lib.git main --squash

# Push local changes back to upstream
git subtree push --prefix=lib/shared https://github.com/org/shared-lib.git main

# Split subtree into its own branch (for extraction)
git subtree split --prefix=lib/shared -b shared-lib-standalone
```

### 子模块（Submodule）：指向另一个仓库中的特定提交

```bash
# Add a submodule
git submodule add https://github.com/org/shared-lib.git lib/shared

# Clone a repo with submodules
git clone --recurse-submodules https://github.com/org/main-repo.git

# Initialize submodules after clone (if forgot --recurse)
git submodule update --init --recursive

# Update submodules to latest
git submodule update --remote

# Remove a submodule
git rm lib/shared
rm -rf .git/modules/lib/shared
# Remove entry from .gitmodules if it persists
```

### 何时使用哪种方式

```
Subtree: Simpler, no special commands for cloners, code lives in your repo.
         Use when: shared library, vendor code, infrequent upstream changes.

Submodule: Pointer to exact commit, smaller repo, clear separation.
           Use when: large dependency, independent release cycle, many contributors.
```

## 稀疏检出（Sparse Checkout）

### 只检出需要的目录

```bash
# Enable sparse checkout
git sparse-checkout init --cone

# Select directories
git sparse-checkout set packages/my-app packages/shared-lib

# Add another directory
git sparse-checkout add packages/another-lib

# List what's checked out
git sparse-checkout list

# Disable (check out everything again)
git sparse-checkout disable
```

### 使用稀疏检出克隆大型单仓库

```bash
# Partial clone + sparse checkout (fastest for huge repos)
git clone --filter=blob:none --sparse https://github.com/org/monorepo.git
cd monorepo
git sparse-checkout set packages/my-service

# No-checkout clone (just metadata)
git clone --no-checkout https://github.com/org/monorepo.git
cd monorepo
git sparse-checkout set packages/my-service
git checkout main
```

## 冲突解决

### 理解冲突标记

```
<<<<<<< HEAD (or "ours")
Your changes on the current branch
=======
Their changes from the incoming branch
>>>>>>> feature-branch (or "theirs")
```

### 解决冲突的策略

```bash
# Accept all of ours (current branch wins)
git checkout --ours path/to/file.ts
git add path/to/file.ts

# Accept all of theirs (incoming branch wins)
git checkout --theirs path/to/file.ts
git add path/to/file.ts

# Accept ours for ALL files
git checkout --ours .
git add .

# Use a merge tool
git mergetool

# See the three-way diff (base, ours, theirs)
git diff --cc path/to/file.ts

# Show common ancestor version
git show :1:path/to/file.ts   # base (common ancestor)
git show :2:path/to/file.ts   # ours
git show :3:path/to/file.ts   # theirs
```

### Rebase 冲突处理流程

```bash
# During rebase, conflicts appear one commit at a time
# 1. Fix the conflict in the file
# 2. Stage the fix
git add fixed-file.ts
# 3. Continue to next commit
git rebase --continue
# 4. Repeat until done

# If a commit is now empty after resolution
git rebase --skip
```

### 重用之前的冲突解决方式（Rerere）

```bash
# Enable rerere globally
git config --global rerere.enabled true

# Git remembers how you resolved conflicts
# Next time the same conflict appears, it auto-resolves

# See recorded resolutions
ls .git/rr-cache/

# Forget a bad resolution
git rerere forget path/to/file.ts
```

## Git Stash 的使用技巧

```bash
# Stash with a message
git stash push -m "WIP: refactoring auth flow"

# Stash specific files
git stash push -m "partial stash" -- src/auth.ts src/login.ts

# Stash including untracked files
git stash push -u -m "with untracked"

# List stashes
git stash list

# Apply most recent stash (keep in stash list)
git stash apply

# Apply and remove from stash list
git stash pop

# Apply a specific stash
git stash apply stash@{2}

# Show what's in a stash
git stash show -p stash@{0}

# Create a branch from a stash
git stash branch new-feature stash@{0}

# Drop a specific stash
git stash drop stash@{1}

# Clear all stashes
git stash clear
```

## 查找代码修改的来源（Blame）和日志分析

```bash
# Who changed each line (with date)
git blame src/auth.ts

# Blame a specific line range
git blame -L 50,70 src/auth.ts

# Ignore whitespace changes in blame
git blame -w src/auth.ts

# Find when a line was deleted (search all history)
git log -S "function oldName" --oneline

# Find when a regex pattern was added/removed
git log -G "TODO.*hack" --oneline

# Follow a file through renames
git log --follow --oneline -- src/new-name.ts

# Show the commit that last touched each line, ignoring moves
git blame -M src/auth.ts

# Show log with file changes
git log --stat --oneline -20

# Show all commits affecting a specific file
git log --oneline -- src/auth.ts

# Show diff of a specific commit
git show abc123
```

## 标签（Tags）和发布版本（Releases）

```bash
# Create annotated tag (preferred for releases)
git tag -a v1.2.0 -m "Release 1.2.0: Added auth module"

# Create lightweight tag
git tag v1.2.0

# Tag a past commit
git tag -a v1.1.0 abc123 -m "Retroactive tag for release 1.1.0"

# List tags
git tag -l
git tag -l "v1.*"

# Push tags
git push origin v1.2.0      # Single tag
git push origin --tags       # All tags

# Delete a tag
git tag -d v1.2.0            # Local
git push origin --delete v1.2.0  # Remote
```

## 提示：

- `git rebase -i` 是最实用的高级 Git 命令，建议先学习它。
- 绝不要对已推送到共享分支的提交进行 rebase，仅在本地或特性分支上进行 rebase。
- `git reflog` 是你的安全保障：如果丢失了提交记录，通常可以在 90 天内恢复。
- 使用 `git bisect run` 并结合自动化测试可以加快问题定位速度，并避免人为错误。
- Worktree 比多个克隆版本更高效，因为它们共享 `.git` 存储空间。
- 除非有特殊原因，否则优先使用 `git subtree` 而不是 `git submodule`，因为子树对协作者来说更易于理解。
- 全局启用 `rerere` 功能，它可以记录冲突解决过程，避免重复解决相同的冲突。
- `git stash push -m "描述信息"` 比简单的 `git stash` 更实用，尤其是在存储多个临时修改时。
- `git log -S "关键字"` 是快速查找函数或变量添加/删除时间的最快方法。