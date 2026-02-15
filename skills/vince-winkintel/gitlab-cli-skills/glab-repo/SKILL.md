---
name: glab-repo
description: **与 GitLab 仓库和项目进行交互**  
支持以下操作：克隆（clone）、创建（create）、分支（fork）、归档（archive）、查看（view）、更新（update）、删除（delete）、搜索（search）、转移（transfer）以及成员管理（member management）。这些功能可用于管理仓库的生命周期、创建项目分支、克隆仓库、搜索项目、管理协作人员（collaborators），或配置仓库设置。相关操作会触发相应的 GitLab 事件（events），涉及仓库（repository）、项目（project）、克隆操作（clone）、分支操作（fork）、仓库创建（create repo）、项目搜索（search projects）以及协作人员管理（manage collaborators）等场景。
---

# glab 仓库

## 使用 GitLab 仓库和项目

### 快速入门

```bash
# Clone a repository
glab repo clone group/project

# Create new repository
glab repo create my-new-project --public

# Fork a repository
glab repo fork upstream/project

# View repository details
glab repo view

# Search for repositories
glab repo search "keyword"
```

### 常见工作流程

#### 创建新项目

1. **创建仓库：**
   ```bash
   glab repo create my-project \
     --public \
     --description "My awesome project"
   ```

2. **在本地克隆仓库：**
   ```bash
   glab repo clone my-username/my-project
   cd my-project
   ```

3. **为仓库添加初始内容：**
   ```bash
   echo "# My Project" > README.md
   git add README.md
   git commit -m "Initial commit"
   git push -u origin main
   ```

#### 分支仓库的流程

1. **从上游仓库创建分支：**
   ```bash
   glab repo fork upstream-group/project
   ```

2. **克隆你的分支：**
   ```bash
   glab repo clone my-username/project
   cd project
   ```

3. **添加上游仓库作为远程仓库：**
   ```bash
   git remote add upstream https://gitlab.com/upstream-group/project.git
   ```

4. **保持分支与上游仓库同步：**
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

#### 自动同步

使用 `sync` 脚本进行一键式分支更新：
```bash
scripts/sync-fork.sh main
scripts/sync-fork.sh develop upstream
```

该脚本会自动执行以下操作：从上游仓库获取代码 → 合并更改 → 将更改推送到上游仓库。

#### 仓库管理

- **查看仓库信息：**
   ```bash
glab repo view
glab repo view group/project  # Specific repo
glab repo view --web          # Open in browser
```

- **更新仓库设置：**
   ```bash
glab repo update \
  --description "Updated description" \
  --default-branch develop
```

- **归档仓库：**
   ```bash
glab repo archive download main  # Downloads .tar.gz
glab repo archive download main --format zip
```

- **将仓库转移到新的命名空间：**
   ```bash
glab repo transfer my-project --target-namespace new-group
```

- **删除仓库：**
   ```bash
glab repo delete group/project
```

#### 会员管理

- **列出协作成员：**
   ```bash
glab repo members list
```

- **添加新成员：**
   ```bash
glab repo members add @username --access-level maintainer
```

- **删除成员：**
   ```bash
glab repo members remove @username
```

- **更新成员的访问权限：**
   ```bash
glab repo members update @username --access-level developer
```

#### 批量操作

- **克隆一组仓库：**
   ```bash
glab repo clone -g my-group
```

- **搜索并克隆仓库：**
   ```bash
glab repo search "api" --per-page 10
# Then clone specific result
glab repo clone group/api-project
```

- **列出你的所有仓库：**
   ```bash
glab repo list
glab repo list --member          # Only where you're a member
glab repo list --mine            # Only repos you own
```

### 故障排除

- **克隆失败（权限错误）：**
  - 确认你是否有访问权限：`glab repo view group/project`
  - 检查认证状态：`glab auth status`
  - 对于私有仓库，请确保使用正确的账户登录。

- **分支操作失败：**
  - 检查你的命名空间中是否已经存在该分支
  - 确认你是否有分支的权限（某些仓库禁止创建分支）
  - 尝试使用明确的命名空间：`glab repo fork --fork-path username/new-name`

- **转移仓库失败：**
  - 确认你具有仓库的所有者或维护者权限
  - 检查目标命名空间是否存在以及你是否有创建权限
  - 有些项目可能启用了转移保护机制

- **批量克隆失败：**
  - 确认团队组存在且你具有访问权限
  - 检查是否有足够的磁盘空间
  - 大型团队可能会导致克隆操作超时——建议分别克隆每个仓库

### 相关技能

- **认证与访问权限：**
  - 请参阅 `glab-auth` 以了解登录和认证设置
  - 请参阅 `glab-ssh-key` 以管理 SSH 密钥
  - 请参阅 `glab-deploy-key` 以了解部署认证

- **项目配置：**
  - 请参阅 `glab-config` 以了解 CLI 的默认设置和配置选项
  - 请参阅 `glab-variable` 以了解 CI/CD 变量

- **分支同步：**
  - `scripts/sync-fork.sh` 脚本可自动执行与上游仓库的同步操作

### 命令参考

有关所有命令的完整文档和参数，请参阅 [references/commands.md](references/commands.md)。

**可用命令：**
- `clone` - 克隆仓库或仓库组
- `create` - 创建新项目
- `fork` - 创建仓库分支
- `view` - 查看项目详情
- `update` - 更新项目设置
- `delete` - 删除项目
- `search` - 搜索项目
- `list` - 列出仓库
- `transfer` - 将仓库转移到新的命名空间
- `archive` - 下载仓库存档
- `contributors` - 列出项目贡献者
- `members` - 管理项目成员
- `mirror` - 配置仓库镜像
- `publish` - 发布项目资源