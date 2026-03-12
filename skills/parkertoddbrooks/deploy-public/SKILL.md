---
name: deploy-public
description: >
  **私有仓库到公共仓库的同步流程：**  
  1. 将除 `ai/` 目录外的所有内容复制到公共仓库。  
  2. 创建一个 Pull Request（PR），并提交更改。  
  3. 合并这些更改到公共仓库。  
  4. 同步公共仓库中的发布版本（releases）。
license: MIT
interface: [cli, skill]
metadata:
  display-name: "Private-to-Public Sync"
  version: "1.3.0"
  homepage: "https://github.com/wipcomputer/wip-ai-devops-toolbox"
  author: "Parker Todd Brooks"
  category: dev-tools
  capabilities:
    - repo-sync
    - release-sync
  requires:
    bins: [git, gh, bash]
  openclaw:
    requires:
      bins: [git, gh, bash]
    emoji: "🚢"
compatibility: Requires git, gh (GitHub CLI), bash.
---
# deploy-public

该脚本用于将私有仓库（private repo）的内容同步到对应的公共仓库（public repo）。它执行以下操作：
- 复制私有仓库中的所有文件
- 在公共仓库中创建一个 Pull Request (PR)
- 合并该 PR
- 同步公共仓库中的发布信息（release notes）

## 适用场景

**使用 `deploy-public` 的场景：**
- 将私有仓库的代码发布到对应的公共仓库
- 在私有仓库中执行 `wip-release` 命令后（请确保公共仓库中已存在相应的发布记录）
- 将私有仓库中的发布信息同步到公共仓库

**重要提示：** 发布顺序至关重要：
1. 首先将 PR 合并到私有仓库的主分支（main branch）
2. 接着执行 `wip-release` 命令（在私有仓库中创建带有发布信息的 GitHub 发布记录）
3. 最后执行 `deploy-public.sh` 命令（从私有仓库的发布记录中获取信息并更新公共仓库）

**不适用场景：**
- 不包含 `-private` 前缀的仓库
- 首次设置仓库时（请先在 GitHub 上创建公共仓库）

## API 参考（API Reference）（此处为示例，实际 API 可能需要根据实际情况提供）

## 命令行接口（CLI）（Command Line Interface, CLI）（```bash
bash scripts/deploy-public.sh /path/to/private-repo org/public-repo
```）

## 使用示例（Examples）（```bash
# Deploy memory-crystal
bash scripts/deploy-public.sh /path/to/memory-crystal-private wipcomputer/memory-crystal

# Deploy wip-dev-tools
bash scripts/deploy-public.sh /path/to/wip-ai-devops-toolbox-private wipcomputer/wip-ai-devops-toolbox
```）

## 功能说明：**
1. 将公共仓库克隆到一个临时目录中。
2. 从私有仓库中复制所有文件（`ai/` 和 `.git/` 目录除外）。
3. 创建一个新的分支，提交更改，然后推送到公共仓库。
4. 合并该分支的更改。
5. 将公共仓库中的发布信息（release notes）与私有仓库中的信息同步。