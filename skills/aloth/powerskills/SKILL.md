---
name: powerskills
description: 这是一个用于AI代理的Windows自动化工具包，支持Outlook邮件/日历功能、Edge浏览器操作（包括内容分发平台CDP）、桌面截图/窗口管理，以及通过PowerShell执行Shell命令。您可以选择安装整个工具包，也可以单独安装其中某个子模块：powerskills-outlook、powerskills-browser、powerskills-desktop或powerskills-system。
license: MIT
metadata:
  author: aloth
  cli: powerskills
---
# PowerSkills

通过 PowerShell 实现 AI 代理在 Windows 系统上的各种功能。`skills/` 目录下的每个技能都可以被独立地发现和使用。

## 设置

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## 使用方法

```powershell
.\powerskills.ps1 <skill> <action> [--param value ...]
.\powerskills.ps1 list                          # Discover available skills
.\powerskills.ps1 outlook inbox --limit 10       # Run an action
```

## 输出格式

所有操作都会以 JSON 格式返回结果：

```json
{"status": "success", "exit_code": 0, "data": {...}, "timestamp": "..."}
```

## 配置

请编辑 `config.json` 文件：

```json
{
  "edge_debug_port": 9222,
  "default_timeout": 30,
  "outlook_body_max_chars": 5000
}
```

## 技能列表

| 技能          | 描述                                      |
|--------------|-----------------------------------------|
| [outlook](skills/outlook/SKILL.md) | 通过 Outlook COM 接口实现电子邮件和日历功能           |
| [browser](skills/browser/SKILL.md) | 通过 CDP 实现 Edge 浏览器的自动化操作             |
| [desktop](skills/desktop/SKILL.md) | 截图、窗口管理、键盘输入等操作                     |
| [system](skills/system/SKILL.md) | 执行 Shell 命令、管理进程、查看系统信息                 |