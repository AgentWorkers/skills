---
name: skill-release-manager
description: 该脚本自动化了 OpenClaw 技能的发布流程：通过一个命令即可完成版本更新、与 GitHub（子树）的同步、GitHub 发布物的创建以及内容的发布到 ClawHub 的操作。
---

# 技能发布管理器

OpenClaw 技能的统一发布工具。

## 主要功能
1. **版本升级**：自动更新 `package.json` 文件中的版本号（patch、minor、major）。
2. **Git 操作**：将版本升级信息提交到本地工作区。
3. **GitHub 发布**：使用 `skill-publisher` 将代码同步到远程仓库，并在 GitHub 上创建一个新的发布版本。
4. **ClawHub 发布**：将技能发布到 ClawHub 注册表中。

## 使用方法

```bash
node skills/skill-release-manager/index.js \
  --path skills/private-evolver \
  --remote https://github.com/autogame-17/evolver.git \
  --bump patch \
  --notes "Release notes here"
```

## 常用参数
*   `--path`：技能目录的路径（必需）。
*   `--remote`：目标 GitHub 仓库的 URL（必需）。
*   `--bump`：版本升级类型（`patch`、`minor`、`major`）或具体版本号（例如 `1.2.3`）。默认值：`patch`。
*   `--notes`：用于 GitHub 的发布说明。

## 先决条件
- 必须安装 `skill-publisher` 工具。
- 必须完成 `clawhub` 命令行工具的认证。