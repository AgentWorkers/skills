---
name: openclaw-router
description: 从 OpenClaw 的公共 GitHub 仓库中安装、更新或修复 OpenClaw Router 插件，并将其安装到 `~/.openclaw` 目录中。之后，验证路由功能、命令行接口（CLI）命令以及相关统计数据。
---
# OpenClaw Router

当用户需要在本地 OpenClaw 环境中安装、更新、修复或验证 `openclaw-router` 插件时，请使用此技能。

在 ClawHub 上发布的技能名称：`local-openclaw-router`

## 该技能的功能

- 克隆或更新公开的 `openclaw-router` 仓库
- 将插件同步到 `~/.openclaw/extensions/openclaw-router` 目录中
- 运行插件的测试套件
- 刷新运行时状态
- 重启本地 OpenClaw 网关
- 验证插件的健康状况、`openclaw-router` 命令行接口（CLI）的可用性以及相关统计信息

## 默认工作流程

使用此技能时，请按照以下步骤操作：

1. 将 `https://github.com/xucheng/openclaw-router.git` 克隆到 `~/.openclaw/local-plugins/openclaw-router` 目录中。
2. （如果存在）删除旧的 `~/.openclaw/extensions/openclaw-main-router` 目录。
3. 将克隆的仓库同步到 `~/.openclaw/extensions/openclaw-router` 目录中。
4. 确保 `~/.openclaw/openclaw.json` 文件包含以下内容：
   - `plugins.allow` 中包含 `openclaw-router`
   - `plugins.entries.openclaw-router.enabled = true`
   - `plugins.installs.openclaw-router` 指向本地插件的安装路径
   - 不存在过时的 `openclaw-main-router` 安装记录或条目
5. 在仓库目录中运行 `node --test` 命令以执行插件测试。
6. 使用 `lib/runtime-state.js` 文件刷新运行时状态。
7. 重启本地 OpenClaw 网关。
8. 验证 `/health` 状态、`openclaw router show medium` 命令的输出结果以及 `~/.openclaw/scripts/openclaw-router-stats.sh` 脚本的运行情况。

## 安装后的验证步骤

请执行以下检查：

```bash
curl -sS http://127.0.0.1:43111/health
openclaw router show medium
~/.openclaw/scripts/openclaw-router-stats.sh
```

**预期结果**：

- `/health` 命令返回 `openclaw-router` 作为可用插件提供者。
- `openclaw router show medium` 命令能够正确显示当前的链层状态（MEDIUM 级别）。
- `openclaw-router-stats.sh` 脚本能够无错误地运行。

## 注意事项**

- 该技能从 GitHub 安装插件，但不会上传任何代码到服务器。
- 建议直接执行安装/更新操作，而不是依赖嵌入的辅助脚本。
- 如果重启后网关短暂显示错误代码 `1006`，请稍后重试一次。
- 如果系统中仍存在旧的 `openclaw-main-router` 目录，请将其迁移至 `openclaw-router` 目录下。