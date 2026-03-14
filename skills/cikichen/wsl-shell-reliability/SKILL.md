---
name: wsl-shell-reliability
description: 在 Windows 上为 AI 代理选择 shell 时，我们遵循“可靠性优先”的原则：根据执行风险来决定使用 WSL（Windows Subsystem for Linux）还是 PowerShell，而不是个人偏好。
license: MIT
compatibility: Windows (WSL optional; recommended for POSIX-fragile workflows)
metadata:
  author: simon
  version: "2.0"
---
# WSL Shell 可靠性

使用此技巧可提高在 Windows 上执行终端命令的成功率。

此技巧**不会强制**使用 WSL（Windows Subsystem for Linux）；它遵循“可靠性优先”的原则：

- 选择故障风险较低的 Shell；
- 在切换 Shell 时保持命令的原始意图；
- **绝不**在用户不知情的情况下切换 Shell。

## 触发条件

- 在 Windows 上执行的任何终端任务；
- 由 AI 生成的、看起来符合 Bash/POSIX 格式的命令；
- 由于引号、路径或 Shell 不匹配导致的重复失败。

## 一目了然的决策表

| 问题 | 是 | 否 |
| --- | --- | --- |
| 是 Windows 原生任务/工具吗？ | 使用 **PowerShell/CMD** | 继续下一个问题 |
| 需要 POSIX/bash 语法吗？ | 使用 **WSL/bash** | 继续下一个问题 |
| 需要与 Linux 兼容吗？ | 更倾向于使用 **WSL/bash** | 继续下一个问题 |
| Windows Shell 的解析风险较高吗？ | 更倾向于使用 **WSL/bash** | 继续下一个问题 |
| 两个路径的故障风险都较低吗？ | 选择组件更少的 Shell | 无需操作 |

**示例**：

- Windows 原生任务：`winget`、`reg`、`netsh`、`.exe/.msi` 文件操作、服务/系统管理操作。
- 需要大量使用 POSIX 语法的任务：`rm -rf`、`export`、`./script.sh`、`grep/sed/awk`、复杂的管道操作。

## 规则优先级（冲突解决）

当规则之间存在冲突时，按以下优先级顺序应用规则：

1. **Windows 原生任务的强制要求**（必须使用 PowerShell/CMD）；
2. **决策表中的明确指示**（如依赖 POSIX 语法、解析风险较高）；
3. **故障恢复策略 + 命令意图的保持**；
4. **使用上的便利性**（工具的可用性、操作步骤的简洁性）。

如果仍无法确定，应选择故障风险较低的 Shell。

## Windows 原生任务的强制要求（优先使用 PowerShell/CMD）

- `winget`、`scoop`、`choco`；
- PowerShell 的 cmdlet 以及注册表/服务/系统相关命令；
- `.msi`/`.exe` 安装程序；
- 面向 Windows 的 `msbuild`/`.NET` 包装流程。

## 执行流程

1. 根据决策表选择合适的 Shell；
2. 为所选 Shell 生成相应的命令语法（不要混合不同 Shell 的语法）；
3. 执行命令；
4. 如果命令失败且问题出在 Shell 上，切换到另一个 Shell；
5. 确保命令的意图得到准确保留（仅转换语法）；
6. 明确说明切换 Shell 的原因。

## 各 Shell 的语法规则

- **WSL/bash**：允许使用 POSIX 语法；
- **PowerShell**：使用 PowerShell 自带的引号和转义规则；
- **CMD**：仅在任务/工具有特殊要求时使用。

**注意**：不要在 PowerShell/CMD 中直接使用 Bash 语法。

## WSL 的常用命令模板

- `wsl.exe -e bash --noprofile --norc -lc "<command>"`
- `wsl.exe -e bash --noprofile --norc -lc "cd /mnt/<drive>/<path> && <command>"`

## 常见命令的转换规则（Bash -> PowerShell）

- `export FOO=bar` -> `$env:FOO = "bar"`
- `rm -rf <path>` -> `Remove-Item -Recurse -Force <path>`
- `cp -r a b` -> `Copy-Item a b -Recurse`
- `mv a b` -> `Move-Item a b`
- `cat file` -> `Get-Content file`

**仅当需要时才进行转换**。

## 注意事项

- **绝不**在用户不知情的情况下切换 Shell；
- **切换 Shell 时**绝不要改变命令的含义；
- **不要仅仅为了强制使用某种 Shell 而安装额外的工具**；
- **优先使用所选 Shell 中已有的工具链**。

## 故障恢复策略

在以下情况下切换到另一个 Shell：

- WSL 无法使用或不稳定；
- 当前 Shell 无法解析或执行该工具；
- 任务显然是 Windows 原生的；
- 命令因 Shell 的语法或引号问题而失败。

在切换 Shell 时，需报告以下信息：

- 哪个命令失败了；
- 为什么切换 Shell；
- 原始命令的意图是如何被保留的。

## 已知的限制

- 一些企业环境禁止安装或使用 WSL；
- VPN/代理/DNS 设置可能会影响某个 Shell 中的包或网络操作；
- 跨文件系统的操作性能可能不稳定；
- 安全策略可能会阻止在 PowerShell 中执行脚本。

在这些情况下，应明确说明需要切换 Shell 的原因，并详细报告相关限制。

## 参考资料

- [参考资料/REFERENCE.md](references/REFERENCE.md)
- [参考资料/SCENARIOS.md](references/SCENARIOS.md)