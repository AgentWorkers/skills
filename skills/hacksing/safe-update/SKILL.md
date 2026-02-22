---
name: safe-update
description: 从源代码更新 OpenClaw。具体步骤包括：拉取最新的主分支（main branch）的代码，将功能分支（feature branch）重新基线（rebase）到主分支，然后编译并安装更新后的代码，最后重启相关服务。此更新过程会在用户请求更新 OpenClaw、同步源代码、重新基线分支或重新构建软件时自动触发。
---
# 安全更新

从源代码更新 OpenClaw 至最新版本，同时保留本地所做的更改。

## 工作流程

```bash
# 1. 进入项目目录
cd /home/ubuntu/projects/openclaw

# 2. 备份配置文件（更新前的良好实践！）
echo "=== 备份配置文件 ==="
mkdir -p ~/.openclaw/backups
BACKUP_SUFFIX=$(date +%Y%m%d-%H%M%S)

# 备份主配置文件
cp ~/.openclaw/openclaw.json ~/.openclaw/backups/openclaw.json.bak.$BACKUP_SUFFIX
echo "✅ 备份成功：openclaw.json"

# 备份身份验证配置文件（如果存在）
if [ -f ~/.openclaw/agents/main/agent/auth-profiles.json ]; then
  cp ~/.openclaw/agents/main/agent/auth-profiles.json \
     ~/.openclaw/backups/auth-profiles.json.bak.$BACKUP_SUFFIX
  echo "✅ 备份成功：auth-profiles.json"
fi

echo "💡 备份文件保存路径：~/.openclaw/backups/"
echo ""

# 3. 添加上游仓库（如果尚未添加）
git remote add upstream https://github.com/openclaw/openclaw.git 2>/dev/null || true

# 4. 获取上游的更改
git fetch upstream

# 5. 更新主分支
git checkout main
git merge upstream/main

# 6. 查看完整的变更日志
echo "=== 完整的变更日志 ==="
# 获取当前版本和上一个版本的标签
CURRENT_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "v$(node -e 'console.log(require("./package.json").version)')")
PREV_TAG=$(git tag --sort=-creatordate | grep -A1 "^$CURRENT_TAG$" | tail -n1)
if [ "$PREV_TAG" = "$CURRENT_TAG" ]; then
  PREV_TAG=$(git tag --sort=-creatordate | grep -A2 "^$CURRENT_TAG$" | tail -n1)
fi

echo "当前版本：$CURRENT_TAG"
echo "上一个版本：$PREV_TAG"
echo ""
echo "--- Git 提交记录 ---"
if [ -n "$PREV_TAG" ] && [ "$PREV_TAG" != "$CURRENT_TAG" ]; then
  git log "$PREV_TAG..HEAD" --oneline --no-decorate
else
  git log --oneline --no-decorate -50
fi
echo ""
echo "--- 变更日志详情 ---"
# 从变更日志中提取当前版本的信息
if [ -f CHANGELOG.md ]; then
  CHANGELOG_CONTENT=$(awk '/^## [0-9]/{p=0} /^## '${CURRENT_TAG#v}'/{p=1} p' CHANGELOG.md)
  echo "$CHANGELOG_CONTENT"
  echo ""
  echo "--- 主要变更概要 ---"
  # 提取变更日志中的主要变更信息
  echo "$CHANGELOG_CONTENT" | awk '/^## /{p=0} /^### Changes/{p=1} p' | head -100 | sed 's/^- /*/'
fi

# 7. 切换到功能分支并执行 rebase 操作
git checkout feat/allowed-agents-v2
git rebase main

# 8. 构建并安装新版本
npm run build
npm i -g .

# 9. 检查版本信息
NEW_VERSION=$(openclaw --version)
echo "✅ 更新完成！新版本：$NEW_VERSION"
echo ""

# 10. 验证配置文件的迁移情况
echo "=== 验证配置文件的迁移情况 ==="
echo "检查模型配置文件..."
cat ~/.openclaw/openclaw.json | grep -A 10 '"model"' || echo "⚠️ 未找到模型配置文件（可能是正常现象）"
echo ""

# 11. 重启网关
echo "=== 重启网关 ==="
systemctl --user restart openclaw-gateway

# 12. 检查网关的运行状态
echo "=== 检查网关的运行状态 ==="
sleep 3  # 等待网关启动
if command -v openclaw &>/dev/null; then
  openclaw health 2>/dev/null || openclaw status
else
  echo "⚠️ 无法执行 openclaw 命令，请手动检查网关的状态"
fi
echo ""

# 13. 完成提示
echo "=== 更新完成！ ==="
echo ""
echo "✅ 工作区数据、内存设置和身份验证配置文件已自动保留"
echo "✅ 备份只是预防措施——只需 30 秒即可完成备份，而重新构建则需要数小时"
echo "💡 如果更新后出现问题，可以从 ~/.openclaw/backups/ 目录中恢复数据"
echo ""
```

## 快速脚本

运行 `scripts/update.sh` 可以自动完成上述所有步骤。

## 注意事项

- 在执行 rebase 操作后，如果需要将更改推送到分支，请使用 `git push --force`。
- 构建完成后，需要重启网关才能使更改生效。