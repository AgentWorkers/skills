# MacPilot 技能

这些技能适用于 [MacPilot](https://github.com/adhikjoshi/macpilot)——一个通过辅助功能 API 实现 macOS 自动化的 CLI 工具。MacPilot 可帮助 AI 编程代理（如 Claude Code、Cursor、Codex 等）执行各种 macOS 任务，例如点击按钮、输入文本、管理窗口、处理文件对话框、截图等。

## 安装

```bash
npx skills add adhikjoshi/macpilot-skills
```

您可以使用 [skills](https://github.com/vercel-labs/skills) CLI 将这些技能安装到您选择的代理中。

## 可用技能

| 技能 | 描述 |
|-------|-------------|
| **macpilot-automation** | 基本的 macOS 自动化功能：鼠标操作、键盘输入、应用程序控制、菜单操作、剪贴板（支持历史记录和搜索）、通知处理、 shell 命令以及系统控制 |
| **macpilot-ui-inspector** | 通过辅助功能 API 检查和交互 UI 元素：查找、点击、读取和修改控件内容 |
| **macpilot-dialog-handler** | 处理原生文件对话框（打开、保存、打印）：导航文件夹、选择文件、关闭警告框、等待操作并执行点击操作 |
| **macpilot-screenshot-ocr** | 截取屏幕截图，并使用 OCR 技术识别屏幕上的文本；支持暂停/恢复屏幕录制功能 |
| **macpilot-window-manager** | 管理窗口：列出窗口、移动窗口、调整窗口大小、将窗口固定到屏幕边缘、切换全屏显示模式、保存/恢复窗口布局 |

## 先决条件

1. **已安装 MacPilot**：可以从源代码编译安装，或从 [官方发布版本](https://github.com/adhikjoshi/macpilot/releases) 下载。
2. **辅助功能权限**：需要在系统设置 > 隐私与安全 > 辅助功能中允许 MacPilot.app 访问相关功能。
3. **屏幕录制权限**（适用于截图/OCR 功能）：需要在系统设置 > 隐私与安全 > 屏幕录制中启用该权限。

## 快速入门

```bash
# Install MacPilot skills into Claude Code
npx skills add adhikjoshi/macpilot-skills

# Now ask Claude Code to automate macOS:
# "Open Safari and navigate to example.com"
# "Take a screenshot of the Finder window"
# "Snap VS Code to the left half and Terminal to the right"
# "Save this file to my Desktop"
```

## 手动安装

如果您不希望使用 `npx skills`，可以将任何 `SKILL.md` 文件复制到代理的技能目录中：

```bash
# Claude Code (project scope)
mkdir -p .claude/skills/macpilot-automation
cp skills/macpilot-automation/SKILL.md .claude/skills/macpilot-automation/

# Claude Code (global scope)
mkdir -p ~/.claude/skills/macpilot-automation
cp skills/macpilot-automation/SKILL.md ~/.claude/skills/macpilot-automation/
```

## 许可证

MIT 许可证