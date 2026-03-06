---
name: openclaw-safe-update
description: 通过隔离的侧车（sidecar）检查机制，安全地验证并应用 OpenClaw 的升级。当需要更新 OpenClaw 时，请使用此方法；在升级前先验证目标版本，以避免对全局软件包环境造成影响；或者通过设置默认值为“verify-only”并明确使用 `--apply` 参数，来执行一个适用于生产环境的升级流程。
homepage: https://docs.openclaw.ai/install/updating
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["openclaw", "node", "npm", "curl", "bash"] },
      },
  }
---
# OpenClaw 安全升级

使用“隔离优先”的默认设置来执行生产环境安全的 OpenClaw 升级。

## 工作流程

1. 使用捆绑的脚本：`scripts/openclaw-safe-update.sh`。
2. 首先仅执行验证步骤（默认操作）：
   - `bash scripts/openclaw-safe-update.sh`
   - 可选的目标版本：`--target <version>`
   - 端口会自动从 `18000` 开始的可用端口中选择。
3. 如果验证失败，请检查脚本输出的日志文件，并报告根本原因。
4. 如果验证通过，询问用户是否要应用升级。
5. 仅在用户明确确认后才能应用升级：
   - `bash scripts/openclaw-safe-update.sh --apply`

## 平台参考

首先检测操作系统，然后仅阅读对应平台的文档：
- macOS（`uname` 输出为 `Darwin`） → `references/macos.md`
- Linux（`uname` 输出为 `Linux`） → `references/linux.md`

## 规则

- 默认情况下仅执行验证步骤；未经用户明确同意，切勿应用升级。
- 将候选安装包隔离在指定目录中（`npm --prefix ~/.openclaw/versions/<version>`）。
- 将相关组件（sidecar）也隔离在单独的目录中（使用 `--profile sidecar-verify` 选项，并指定专用端口）。
- 在升级失败时保留日志文件，并在状态更新中包含日志路径。
- 如果验证失败，切勿修改全局安装配置。