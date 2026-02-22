---
name: github-release-workflow
description: "专业的 GitHub 发布工作流程。适用于以下场景：  
(1) 发布新版本；  
(2) 管理版本和标签；  
(3) 遵循常规的提交流程；  
(4) 更新 README 文件和文档；  
(5) 为发布过程设置持续集成/持续部署（CI/CD）机制。"
metadata:
  {
    openclaw: { emoji: "🚀" },
  }
---
# GitHub 发布工作流程（GitHub Release Workflow）

这是一个标准化的专业 GitHub 发布流程。

**重要提示：** 在发布之前，请务必更新 `README.md` 和相关文档！

## 先决条件（Prerequisites）

- 安装了 Git
- 已经登录 GitHub CLI（`gh`）
- 已初始化 Git 仓库

## 快速命令（Quick Commands）

### 完整发布流程（Full Release Flow）

```bash
# 1. Ensure clean working tree
git status

# 2. Run tests and format
pip install -e ".[dev]"
pytest
black lib/ tests/

# 3. Update version in pyproject.toml
# Edit: version = "2.1.0"

# 4. Update CHANGELOG.md
# Add new section with today's date

# 5. Update README.md (IMPORTANT!)
# - Update version badge
# - Update features list
# - Update project structure if changed
# - Update roadmap table

# 6. Update other docs as needed
# - docs/*.md
# - API documentation
# - Examples

# 7. Stage and commit
git add .
git commit -m "release: v2.1.0 - Description"

# 8. Create tag
git tag -a v2.1.0 -m "Version 2.1.0"

# 9. Push
git push
git push origin v2.1.0
```

### 更新 `README.md` 的检查清单（README Update Checklist）

在发布新版本时，务必更新 `README.md`，包括以下内容：

| 项目项 | 说明 |
|------|-------------|
| 版本标识 | 将版本号更新为 `version-x.x.x-blue` |
| 新功能列表 | 添加新功能，移除已弃用的功能 |
| 项目结构 | 确保文件和目录结构与最新版本一致 |
| 安装说明 | 如果依赖项发生变化，请更新安装步骤 |
| 使用说明 | 如有需要，添加新的使用示例 |
| 项目路线图 | 将当前版本的状态更新为“已完成”，并添加下一个开发阶段 |
| API 文档 | 如果 API 发生变化，请更新相关文档 |

### 常规提交格式（Conventional Commits Format）

```
<type>(<scope>): <description>

Types: feat, fix, docs, style, refactor, test, chore, release
```

示例：
- `feat(memory)`：添加 SQLite 支持
- `fix(vitality)`：修复能量计算相关的错误
- `docs: update README`：更新 `README.md` 文件

### 版本格式（Version Format）

```
MAJOR.MINOR.PATCH
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes
```

## 分支策略（Branch Strategy）

```
main (stable)
  ↑
develop (integration)
  ↑
feature/* (new features)
```

## GitHub 发布（GitHub Release，可选）

```bash
gh release create v2.1.0 \
  --title "Version 2.1.0" \
  --notes "Release notes"
```

## 参考资料（See Also）

- 完整规范：`github-release-workflow/SPEC.md`
- 保持版本变更记录：https://keepachangelog.com/
- 语义化版本控制：https://semver.org/
- 常规提交规范：https://www.conventionalcommits.org/