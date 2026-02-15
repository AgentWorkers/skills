---
name: git-pushing
description: 使用常规的提交信息来阶段化（stage）、提交（commit）以及推送（push）Git变更。当用户希望提交并推送变更、提及将更改推送到远程仓库，或者请求保存并推送自己的工作时，应使用此功能。此外，当用户输入“push changes”、“commit and push”、“push this”、“push to github”或类似的Git工作流程命令时，该功能也会被激活。
---

# Git 推送工作流程

将所有更改暂存到仓库中，创建一个常规的提交（commit），然后将其推送到远程分支。

## 使用场景

当用户执行以下操作时，该流程会自动触发：
- 明确要求推送更改（例如：“push these changes”或“commit and push”）
- 提到需要将工作保存到远程仓库（例如：“save to github”或“push to remote”）
- 完成一个功能并希望与他人共享
- 说出类似“let’s push this up”或“commit these changes”这样的话

## 工作流程

**务必使用脚本**，**切勿使用手动 Git 命令**：

```bash
bash skills/git-pushing/scripts/smart_commit.sh
```

如果需要自定义提交信息，可以这样做：
```bash
bash skills/git-pushing/scripts/smart_commit.sh "feat: add feature"
```

该脚本负责完成以下操作：暂存更改、生成常规的提交信息、添加 Claude 页脚（用于记录提交信息），以及使用 `-u` 标志执行推送操作。