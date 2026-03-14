---
name: auto-updater
description: "在 Windows、macOS 和 Linux 上设置并维护 OpenClaw 及相关技能（skills）的自动更新。当用户请求定期更新、手动执行更新、进行更新状态检查或查看更新摘要时，可使用此功能。在 Windows 上，应遵循 Windows 的原生操作流程及 Git Bash 的使用规范，避免使用 WSL（Windows Subsystem for Linux）中的 Bash 路径。"
---
# 自动更新功能（优先支持 Windows，跨平台）

配置 OpenClaw 及已安装技能的安全、定期更新机制。

## 核心规则

1. 优先使用 OpenClaw 自带的更新功能以及 `npx clawhub` 命令。
2. 在 **Windows** 上，通过 **原生的 Windows Shell** 运行更新操作。
3. 在 Windows 系统中，确保 `bash` 指向 **Git Bash 或 MSYS**，而不是 `C:\Windows\System32\bash.exe`（WSL 启动器）。
4. 绝不在公开文档或发布的技能内容中包含用户特定的本地路径或用户名。
5. 必须输出简洁的更新结果：更新成功、未更改或更新失败。

## 仅适用于 Windows 的额外规则（非常重要）

- **禁止** 使用 WSL 来执行更新操作。
- 如果构建步骤需要使用 `bash`，请在当前 Shell 会话的 `PATH` 中添加 Git Bash 的路径。
- 验证当前使用的 bash 是否为 GNU bash（来自 MSYS/Git，**而非** WSL 启动器）。

## 路径占位符（请使用这些占位符）

- `<openclaw-repo>`：源代码仓库的根目录（示例：`%USERPROFILE%\\dev\\openclaw`）
- `<openclaw-home>`：OpenClaw 的运行时目录（示例：`%USERPROFILE%\.openclaw`）

## 手动更新流程

### 1) 更新 OpenClaw（源代码安装）

```powershell
git -C <openclaw-repo> pull --ff-only
pnpm -C <openclaw-repo> install
pnpm -C <openclaw-repo> build
```

### 2) 重启网关

在构建成功后，使用 OpenClaw 的网关重启工具或命令来重启网关。

### 3) 更新技能

```powershell
npx clawhub update --all --workdir <openclaw-home> --no-input
```

如果存在本地修改且用户确认要覆盖原有文件，请执行以下操作：

```powershell
npx clawhub update <slug> --force --workdir <openclaw-home> --no-input
```

## 成功的 Windows 命令模板（已优化）

```powershell
git -C <openclaw-repo> pull --ff-only
pnpm -C <openclaw-repo> install
pnpm -C <openclaw-repo> build
openclaw gateway restart
openclaw --version
```

## 安排更新任务（可选）

当用户要求自动化更新时，可以创建 cron 作业，确保 `agentTurn` 在隔离的环境中运行，并在完成后发送更新总结。除非用户另有要求，否则建议将更新任务安排在较为保守的时间（例如每天凌晨 04:00）。

## 参考资料

- `references/agent-guide.md`
- `references/summary-examples.md`