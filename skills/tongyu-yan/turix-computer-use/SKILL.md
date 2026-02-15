---
name: turix-mac
description: **Computer Use Agent (CUA)：使用 TuriX 实现 macOS 自动化**  
当您需要在桌面上执行视觉任务（如打开应用程序、点击按钮或浏览没有 CLI 或 API 的用户界面）时，可以使用 Computer Use Agent (CUA)。
---

# TuriX-Mac 技能

该技能允许 Clawdbot 通过 TuriX 计算机使用代理（Computer Use Agent）来可视化地控制 macOS 桌面。

## 使用场景

- 当需要用户在 macOS 桌面上执行某些操作时（例如：“打开 Spotify 并播放我喜欢的歌曲”）。
- 在没有命令行界面的应用程序中进行导航时。
- 在需要多步骤可视化操作的工作流程中（例如：“在我的电子邮件中找到最新的发票并将其上传到公司门户”）。

## 工作流程

1. **准备工作**：确保用户在系统设置中已授予 `/opt/homebrew/bin/node` “屏幕录制”权限。
2. **执行任务**：将用户的任务直接传递给辅助脚本。

### 运行 TuriX

通过 `exec` 命令调用辅助脚本，并将完整的任务描述作为参数传递。脚本会自动更新 TuriX 的 `config.json` 文件以记录任务信息。

```bash
skills/local/turix-mac/scripts/run_turix.sh "Open System Settings and switch to Dark Mode"
```

**💡 代理使用技巧：**
- **任务描述**：请尽可能具体。例如，不要只写“打开 Chrome”，而应写“打开 Chrome 并导航到 google.com”。
- **动态配置**：无需手动编辑 `config.json` 文件；脚本会自动处理 JSON 配置的更新。
- **监控**：由于这是一个基于图形界面的任务，请保持会话处于打开状态，并使用 `process log` 工具来查看状态更新或错误信息（如 “NoneType” 表示权限问题）。

**注意**：该进程在后台运行。如果进程没有立即响应，请使用 `process` 工具来查看输出信息。

## 故障排除

- **NoneType 错误**：如果 TuriX 抛出 “AttributeError: ‘NoneType’ object has no attribute ‘save’” 错误，通常表示缺少屏幕录制权限或进程需要重新启动。
- **路径问题**：脚本会显式设置 `PATH` 环境变量，以便能够找到 `screencapture` 工具。