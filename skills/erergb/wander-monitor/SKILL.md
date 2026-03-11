---
name: wander-monitor
description: "本文档为用户提供了使用 Wander 监控 GitHub Actions 工作流的指南。适用于用户询问如何查看 CI/CD 运行情况、避免频繁轮询 Actions 页面、在工作流完成时接收通知，或希望将 Wander 与项目集成时的场景。内容涵盖了智能推送（smart-push）功能、前台/后台/分离（foreground/background/detached）运行模式、特殊使用场景（edge cases），以及项目集成的具体方法。"
---
# Wander — CI/CD 监控工具

**无需持续监控，只需“漫游”即可。** 这是一款优雅的自动化工具，用于在无需轮询的情况下监控 GitHub Actions 的执行情况。

## 适用场景

- 用户希望在提交代码后实时监控 GitHub Actions 的执行过程。
- 用户希望了解 CI 测试何时完成，并接收通知。
- 用户希望避免频繁刷新 GitHub Actions 的页面。
- 用户希望将 CI 监控功能集成到项目中（例如，与 ClawHub 集成）。

---

## 安装

```bash
git clone https://github.com/ERerGB/wander.git
cd wander
chmod +x *.sh
```

**前置条件**：已安装 `gh` CLI（并登录），`jq` 工具；建议在 macOS 系统上使用（以便接收通知）。

---

## 使用方法

### 1. 智能推送（推荐用于 Wander 本身的仓库）

```bash
cd wander
./smart-push.sh
```

根据文件变更情况，自动选择执行 `smoke`、`e2e` 或 `skip` 等操作模式，同时持续监控仓库的更新。

### 2. 手动控制（适用于任意仓库）

```bash
# From target repo (e.g. openclaw-uninstall)
git push

# Choose monitoring mode:
../wander/watch-workflow.sh publish.yml      # Foreground, block until done
../wander/watch-workflow-bg.sh publish.yml  # Background, macOS notify when done
../wander/watch-workflow-detached.sh publish.yml  # Detached, can close terminal
```

### 3. 项目集成

在项目中添加一个封装脚本：

```bash
#!/bin/bash
# scripts/watch-publish.sh
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WANDER_DIR="${WANDER_DIR:-$(dirname "$REPO_ROOT")/wander}"
cd "$REPO_ROOT"
exec "$WANDER_DIR/watch-workflow-bg.sh" publish.yml "$@"
```

然后执行：`git push && ./scripts/watch-publish.sh`

---

## 注意事项（基于实际使用经验）

| 情况 | 行为 | 提示 |
|----------|----------|-----|
| 工作流在 30 秒内完成 | 显示“已完成”并立即发送通知 | 使用 `watch-workflow-bg` 脚本，它能检测到工作流的快速完成 |
| 提交代码后立即开始监控 | 工作流可能需要 5–10 秒才能启动 | 脚本会等待最多 30 秒以确保工作流正常启动 |
| 使用错误的分支 | 30 秒后仍未检测到工作流 | 确保工作流配置正确，且针对的是当前分支 |
| 仓库中不存在 `package-lock.json` 文件 | `setup-node cache: npm` 命令会失败 | 如果仓库中没有 `package-lock.json`，请删除工作流配置中的 `cache: npm` 选项 |

---

## 工作流注册

如需自定义 `check_window` 或 `expected_duration` 的参数，可以在项目根目录下创建 `.workflows.yml` 文件，或设置 `WORKFLOW_REGISTRY_FILE` 环境变量：

```yaml
workflows:
  - name: "publish.yml"
    description: "Publish to ClawHub"
    check_window: 120
    expected_duration: 30
    category: "publish"
```

默认设置：当工作流未在注册表中时，`check_window` 为 300 秒。

---

## 参考资料

- [Wander 的官方文档](https://github.com/ERerGB/wander)
- [边缘使用案例](https://github.com/ERerGB/wander/blob/main/EDGE_CASES.md)
- [其他相关文档](https://github.com/ERerGB/wander/blob/main/COFFEE_BREAK.md)