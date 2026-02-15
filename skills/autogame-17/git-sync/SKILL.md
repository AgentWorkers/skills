---
name: git-sync
description: 自动将本地工作区的更改同步到远程的 GitHub 仓库。在进行了重大更改后或定期执行此操作。
tags: [git, sync, backup, version-control]
---

# Git同步技能

该技能可自动将本地工作区的更改同步到远程的GitHub仓库。  
设计用于在PCEC循环执行时或发生重大更改后被调用。  

## 工具  

### git_sync  
用于提交并推送更改。  
- **message**（可选）：提交信息。默认值为“Auto-sync: Routine evolution update”。  

## 安全性  
- 使用`.gitignore`和`pre-commit`钩子（符合ADL标准）来防止敏感信息泄露。  
- 在提交前会检查是否有需要同步的更改。  

## 实现方式  
该工具实际上是对以下命令的封装：`git add . && git commit && git push`。