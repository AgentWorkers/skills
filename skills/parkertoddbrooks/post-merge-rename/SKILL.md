---
name: post-merge-rename
description: 合并后的分支重命名规则：在分支名称后添加 `--merged-YYYY-MM-DD` 以保留合并历史记录。
license: MIT
interface: [cli, skill]
metadata:
  display-name: "Post-Merge Branch Naming"
  version: "1.3.0"
  homepage: "https://github.com/wipcomputer/wip-ai-devops-toolbox"
  author: "Parker Todd Brooks"
  category: dev-tools
  capabilities:
    - branch-rename
    - history-preservation
  requires:
    bins: [git, bash]
  openclaw:
    requires:
      bins: [git, bash]
    emoji: "🏷️"
compatibility: Requires git, bash.
---
# 合并后重命名（Post-Merge Rename）

该脚本会扫描所有已被合并但尚未重命名的分支，并在分支名称后添加 `--merged-YYYY-MM-DD` 以保留合并历史记录。我们永远不会删除分支，只会对它们进行重命名。

## 适用场景

**适用于以下情况：**
- 合并 Pull Request（PR）后，需要重命名源分支；
- 清理那些已被合并但未重命名的分支；
- 作为 `wip-release` 脚本的第 10 步骤自动执行。

### 不适用场景

- 未合并的分支；
- 当前正在使用的分支。

## API 参考

### 命令行接口（CLI）

```bash
bash scripts/post-merge-rename.sh              # scan + rename all merged branches
bash scripts/post-merge-rename.sh --dry-run     # preview only
bash scripts/post-merge-rename.sh <branch>      # rename specific branch
```

## 功能说明

1. 列出所有被合并到 `main` 分支中的本地分支；
2. 跳过那些已经被重命名的分支（其名称中包含 `--merged-`）；
3. 从 Git 历史记录中获取合并日期；
4. 将分支名称从 `feature-branch` 重命名为 `feature-branch--merged-2026-03-09`；
5. 将重命名后的分支推送到远程仓库（origin）；
6. 从远程仓库中删除旧的分支名称。