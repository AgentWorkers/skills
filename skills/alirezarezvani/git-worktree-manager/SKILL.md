---
name: "git-worktree-manager"
description: "Git Worktree Manager"
---
# Git 工作树管理器

**级别：** 高级  
**类别：** 工程  
**领域：** 并行开发与分支隔离  

## 概述  

使用此工具，您可以借助 Git 工作树安全地并行执行功能开发任务。该工具标准化了分支隔离、端口分配、环境同步和清理流程，确保每个工作树都能像独立的本地应用程序一样运行，而不会干扰其他分支。  

该工具专为多代理工作流程进行了优化，每个代理或终端会话都拥有自己的工作树。  

## 核心功能  

- 从新的或现有的分支创建工作树，并为它们分配唯一的名称。  
- 自动为每个工作树分配不会冲突的端口，并保持这些分配的持久性。  
- 将主仓库中的本地环境文件（`.env*`）复制到新的工作树中。  
- 根据锁文件（lockfile）的检测结果，可选地安装依赖项。  
- 在清理之前检测过时的工作树和未提交的更改。  
- 识别已合并的分支，并安全地移除过时的工作树。  

## 适用场景  

- 需要在本地同时打开两个或多个分支。  
- 需要为功能开发、热修复和 Pull Request（PR）验证创建隔离的开发环境。  
- 需要多个代理协同工作，且这些代理不能共享同一个分支。  
- 当当前分支处于阻塞状态时，但仍需要快速发布修复代码。  
- 希望进行可重复的清理操作，而不是随意使用 `rm -rf` 命令。  

## 关键工作流程  

### 1. 创建一个准备齐全的工作树  

1. 选择一个分支名称和工作树名称。  
2. 运行管理器脚本（如果分支不存在，则会创建该分支）。  
3. 查看生成的端口映射信息。  
4. 使用分配的端口启动应用程序。  

```bash
python scripts/worktree_manager.py \
  --repo . \
  --branch feature/new-auth \
  --name wt-auth \
  --base-branch main \
  --install-deps \
  --format text
```  

（如果使用 JSON 自动化输入：）  
```bash
cat config.json | python scripts/worktree_manager.py --format json
# or
python scripts/worktree_manager.py --input config.json --format json
```  

### 2. 运行并行会话  

推荐的使用规则：  
- 主仓库：使用默认端口（`main`/`develop`）作为集成分支。  
- 工作树 A：使用特定的分支名称及对应的端口。  
- 工作树 B：使用另一个分支名称及对应的端口。  
每个工作树都包含一个名为 `.worktree-ports.json` 的文件，其中记录了分配的端口信息。  

### 3. 带有安全检查的清理操作  

1. 扫描所有工作树及其使用时间。  
2. 检查状态异常的工作树及其合并状态。  
3. 仅移除已合并且状态正常的工作树，或根据需要强制删除它们。  

```bash
python scripts/worktree_cleanup.py --repo . --stale-days 14 --format text
python scripts/worktree_cleanup.py --repo . --remove-merged --format text
```  

### 4. Docker Compose 模式  

使用根据分配的端口生成的配置文件来配置 Docker Compose。该脚本会生成一个固定的端口映射表，将其应用到 `docker-compose.worktree.yml` 文件中。  
具体模板请参考 [docker-compose-patterns.md](references/docker-compose-patterns.md)。  

### 5. 端口分配策略  

默认策略为 `base + (index * stride)`，并会进行冲突检查：  
- 应用程序：`3000`  
- PostgreSQL：`5432`  
- Redis：`6379`  
- 步长（stride）：`10`  
完整策略及特殊情况请参见 [port-allocation-strategy.md](references/port-allocation-strategy.md)。  

## 脚本接口  

- `python scripts/worktree_manager.py --help`  
  - 创建/列出工作树  
  - 分配/保存端口  
  - 复制 `.env*` 文件  
  - 可选地安装依赖项  

- `python scripts/worktree_cleanup.py --help`  
  - 检测工作树的过期状态  
  - 检测状态异常的工作树  
  - 选择性地安全删除工作树  

这两个工具都支持通过标准输入（stdin）或 `--input` 文件进行自动化操作。  

## 常见问题  

- 在主仓库目录内创建工作树。  
- 在所有分支中重复使用相同的端口（例如 `localhost:3000`）。  
- 在隔离的工作树之间共享数据库地址。  
- 移除包含未提交更改的工作树。  
- 删除分支后忘记清理旧的元数据。  
- 未检查目标分支的状态就假设分支已合并。  

## 最佳实践  

- 每个工作树对应一个分支，每个代理对应一个工作树。  
- 将工作树设置为临时性使用，在合并完成后立即删除。  
- 使用统一的命名规则（例如 `wt-<topic>`）。  
- 将端口映射信息保存在文件中，而不是内存或终端笔记中。  
- 每周对活跃的工作树进行一次清理检查。  
- 对于自动化流程使用 `--format json` 格式，对人工审核使用 `--format text` 格式。  
- 除非明确放弃更改，否则不要强制删除状态异常的工作树。  

## 验证步骤  

在确认设置完成之前，请检查以下内容：  
- `git worktree list` 显示的路径和分支名称是否正确。  
- `.worktree-ports.json` 文件是否存在，并且其中包含唯一的端口信息。  
- 如果源仓库中有 `.env` 文件，它们是否已成功复制。  
- 安装依赖项的命令是否以 `0` 代码退出（如果启用了该功能）。  
- 清理操作是否未报告任何异常情况。  

## 参考资料  

- [port-allocation-strategy.md](references/port-allocation-strategy.md)  
- [docker-compose-patterns.md](references/docker-compose-patterns.md)  
- [README.md](README.md)（包含快速入门和安装说明）  

## 决策指南  

在创建新的工作树之前，请参考以下判断标准：  
- 需要隔离的依赖项和服务器端口？ → 创建一个新的工作树。  
- 只需要快速查看本地代码差异？ → 保持使用当前的工作树。  
- 在功能分支处于修改状态时需要发布热修复？ → 创建专门的热修复工作树。  
- 需要临时创建分支用于问题排查？ → 创建临时工作树并在当天完成清理。  

## 操作流程  

### 创建前的准备  

1. 确认主仓库具有干净的基线或正在进行的开发提交。  
2. 确认目标分支的命名规则。  
3. 确认所需的基线分支（`main`/`develop`）是否存在。  
4. 确认没有本地端口被非仓库服务占用。  

### 创建后的检查  

1. 确认 `git status` 显示的分支名称与预期一致。  
2. 确认 `.worktree-ports.json` 文件存在。  
3. 确认应用程序能够使用分配的端口正常启动。  
4. 确认数据库和缓存服务使用的是正确的端口。  

### 删除前的检查  

1. 确认目标分支已合并到上游分支。  
2. 确认没有未提交的文件残留。  
3. 确认没有正在运行的容器或进程依赖于该工作树。  

## 集成与团队协作  

- 使用与任务 ID 对应的工作树路径（例如 `wt-1234-auth`）。  
- 在终端标题中包含工作树路径，以避免误操作。  
- 在自动化设置中，将创建元数据保存在 CI 文档/日志中。  
- 在定时任务中触发清理操作，并将结果发送给团队。  

## 故障恢复措施  

- 如果 `git worktree add` 因路径冲突而失败：检查路径，避免覆盖现有文件。  
- 如果依赖项安装失败：保留已创建的工作树，标记其状态并手动恢复。  
- 如果环境配置文件复制失败：继续执行操作，并提供缺失文件的列表。  
- 如果端口分配与外部服务冲突：调整端口后重新尝试。