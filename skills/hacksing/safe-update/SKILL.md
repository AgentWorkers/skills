---
name: safe-update
description: 从源代码更新 OpenClaw。支持自定义项目路径和分支。包括拉取最新分支、重新基线（rebase）、构建和安装，以及重启服务。当用户请求更新 OpenClaw、同步源代码、重新基线分支或重新构建时，该流程会被触发。
---
# 安全更新

将 OpenClaw 从源代码更新到最新版本，同时保留本地所做的修改。

## ⚠️ 重要警告

- 本脚本会执行 **git rebase** 和 **git push --force** 操作——如果未正确提交更改，可能会导致本地修改丢失。
- 使用 **npm i -g .** 进行全局安装，可能需要管理员权限（sudo）。
- 使用 **systemctl --user restart** 重启 OpenClaw 服务。
- **在运行前请备份配置文件！**（详见下方说明）

## 必需条件

必须安装以下软件：
- `git`
- `npm` 或 `node`
- `systemctl`（用于重启服务）

## 配置

### 环境变量（可选）

```bash
# 设置自定义项目路径
export OPENCLAW_PROJECT_DIR="/path/to/openclaw"

# 设置自定义分支（默认值：main）
export OPENCLAW.Branch="your-feature-branch"

# 启用 dry-run 模式（不进行实际更改）
export DRY_RUN="true"
```

### 或者通过命令行参数传递参数

```bash
./update.sh --dir /path/to/openclaw --branch your-branch
```

## 工作流程

### 第一步：分析当前状态（必须先执行）

在执行任何更新之前，请检查：
1. 当前分支是否有未提交的更改。
2. 当前分支是否有本地修改。
3. 上游代码库是否有新的提交。
4. 根据情况推荐最合适的更新策略。

**推荐策略：**

| 情况 | 推荐方法 | 原因 |
|---------|-------------------|---------|
| 有未提交的本地更改 | 先提交或暂存更改，然后执行 **合并** | 安全，不会丢失任何更改 |
| 只有干净的本地更改 | 执行 **合并** 或 **rebase** | 合并更安全，rebase 可保持版本历史记录的整洁 |
| 准备提交 Pull Request (PR) | 推荐使用 **rebase** | 可使版本历史记录更清晰 |
| 常规开发更新 | 推荐使用 **合并** | 更简单，出错几率更低 |

### 第二步：获取用户确认

在展示推荐选项后，**必须等待用户确认**后再继续执行。

### 第三步：执行更新

```bash
# 1. 进入项目目录
cd "${OPENCLAWPROJECT_DIR:-$HOME/projects/openclaw}"

# 2. 备份配置文件（更新前的良好实践！）
echo "=== 备份配置文件 ==="
mkdir -p ~/.openclaw/backups
BACKUP_SUFFIX=$(date +%Y%m%d-%H%M%S)

# 备份主配置文件
cp ~/.openclaw/openclaw.json ~/.openclaw/backups/openclaw.json.bak.$BACKUP_SUFFIX
echo "✅ 已备份：openclaw.json"

# 备份认证配置文件（如果存在）
if [ -f ~/.openclaw/agents/main/agent/auth-profiles.json ]; then
  cp ~/.openclaw/agents/main/agent/auth-profiles.json \
     ~/.openclaw/backups/auth-profiles.json.bak.$BACKUP_SUFFIX
  echo "✅ 已备份：auth-profiles.json"
fi

echo "💡 备份文件保存路径：/.openclaw/backups/"
echo ""

# 3. 添加上游代码库（如果尚未添加）
git remote add upstream https://github.com/openclaw/openclaw.git 2>/dev/null || true

# 4. 获取上游代码库的更改
git fetch upstream

# 5. 更新目标分支（根据用户选择执行合并或 rebase）
git checkout $BRANCH
# 合并：git merge upstream/$BRANCH
# rebase：git rebase upstream/$BRANCH

# 6. 查看变更日志
echo "=== 完整的变更日志 ==="
CURRENT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v$(node -e 'console.log(require("./package.json").version)')")
echo "当前版本：$CURRENT_TAG"
echo ""

# 7. 构建并安装新版本
npm run build
npm i -g .

# 8. 重新安装 systemd 服务（以更新版本号）
echo "=== 重新安装 Gateway 服务 ==="
openclaw daemon install --force

# 9. 检查版本
NEW_VERSION=$(openclaw --version)
echo "✅ 更新完成！新版本：$NEW_VERSION"
echo ""

# 10. 询问用户是否需要重启服务
echo "=== 需要重启 Gateway 以应用更新 ==="
echo "确认是否重启？(y/N)"
```

## 快速脚本

运行 `scripts/update.sh` 可自动完成上述所有步骤。

### 命令行选项

```bash
./update.sh [OPTIONS]
```

**选项说明：**
- `--dir PATH`：OpenClaw 项目目录（默认值：$HOME/projects/openclaw）
- `--branch NAME`：要更新的分支名称（默认值：main）
- `--mode MODE`：更新模式（合并或 rebase；如果未指定，系统会自动分析并推荐）
- `--dry-run`：仅显示操作内容，不实际执行更新
- `--help`：显示此帮助信息

### 示例

```bash
# 使用默认参数进行更新（系统会自动分析并推荐最佳方式）
./update.sh

# 更新特定分支
./update.sh --branch feat/my-branch

# 强制使用合并模式
./update.sh --mode merge

# 强制使用 rebase 模式
./update.sh --mode rebase

# 仅进行预览（不执行实际更新）
./update.sh --dry-run

# 设置自定义项目路径
./update.sh --dir /opt/openclaw --branch main
```

## 注意事项

- **rebase 可能会导致冲突**——如果发生冲突，请手动解决后再继续。
- **强制推送**——在 rebase 后，如果要将更改推送到分支仓库，请使用 `git push --force`。
- **重新安装服务**：更新后会更新 systemd 服务中的版本信息。
- **需要用户确认重启**——在确认之前，Gateway 服务不会自动重启。
- **务必先备份**——更新前请务必备份所有数据！

## 故障排除

### 在 rebase 过程中遇到 Git 冲突

```bash
# 手动解决冲突后，继续执行：
git add .
git rebase --continue
# 然后继续执行后续构建步骤
```

### 构建失败

```bash
# 清除旧文件并重新尝试：
rm -rf node_modules dist
npm install
npm run build
```

### Gateway 无法启动

```bash
# 检查服务状态：
systemctl --user status openclaw-gateway

# 查看日志：
journalctl --user -u openclaw-gateway -n 50
```