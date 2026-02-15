---
name: Git
description: 使用常规提交和冲突解决方式的每日 Git 工作流程。
metadata: {"clawdbot":{"emoji":"🌿","requires":{"bins":["git"]},"os":["linux","darwin","win32"]}}
---

# Git 工作流程规则

## 推送安全
- 使用 `git push --force-with-lease` 而不是 `--force`
- 如果推送被拒绝，请先运行 `git pull --rebase` 再重试
- 绝不要强制推送到 main/master 分支

## 提交信息
- 使用常规的提交格式：`类型(范围): 描述`
- 保持第一行不超过 72 个字符
- 仅在项目一致使用某个范围时才包含该范围信息

## 冲突解决
- 编辑有冲突的文件后，验证是否还有未解决的标记：`grep -r "<<<\|>>>\|===" .`
- 在完成合并之前，先测试代码是否能够正常编译
- 如果合并过程变得复杂，使用 `git merge --abort` 中止合并，然后尝试使用 `git rebase`

## 分支管理
- 在本地删除已合并的分支：`git branch -d 分支名`
- 在创建 Pull Request (PR) 之前，将特性分支重新基接到最新的 main 分支上
- 使用 `git rebase -i` 合并杂乱无章的提交，然后再推送

## 恢复操作
- 撤销上一次的提交并保留更改：`git reset --soft HEAD~1`
- 删除未暂存的更改：`git restore 文件名`
- 当提交包含多个更改时，使用 `git add -p` 进行部分暂存

## 常见问题与注意事项
- 在进行重要提交之前，验证 git 用户邮箱是否与预期的提交者匹配
- 空目录不会被跟踪——如有需要，请添加 `.gitkeep` 文件
- 使用子模块时，务必使用 `--recurse-submodules` 选项进行克隆
- 在尝试向远程分支推送之前，先检查该分支是否已被删除