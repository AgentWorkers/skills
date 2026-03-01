---
name: terminal-killer
description: OpenClaw的智能shell命令检测与执行器：能够自动识别终端命令（系统内置命令、$PATH路径下的可执行文件、历史命令记录中的匹配项以及特定命令模式），并直接执行这些命令，无需依赖大型语言模型（LLM）的额外处理。支持跨平台运行（macOS、Linux、Windows）。当用户输入的内容看起来是shell命令时，该工具会自动跳过AI处理流程，立即执行相应的命令。
author: Cosper
contact: cosperypf@163.com
---
# Terminal Killer

🚀 一个智能的命令路由器，能够直接执行 shell 命令，无需通过大型语言模型（LLM），实现即时终端操作。

## 快速入门

当用户输入的命令与预设的模式匹配时，Terminal Killer 会自动启动。无需特殊语法——只需自然地输入命令即可：

```
ls -la              # → Direct exec
git status          # → Direct exec  
npm install         # → Direct exec
"help me code"      # → LLM handles normally
```

## 工作原理

### 检测流程

```
User Input → Command Detector → Decision
                                      ├── Command → exec (direct)
                                      └── Task → LLM (normal)
```

### 环境加载

在执行命令之前，Terminal Killer 会自动加载你的 shell 环境：
1. **检测你的 shell 类型**（zsh、bash 等）
2. **加载初始化文件**（`~/.zshrc`、`~/.bash_profile` 等）
3. **继承完整的 PATH 环境**——包括自定义路径（如 Android SDK、Homebrew 等）
4. **保留环境变量**——所有 `export VAR=value` 的设置

这样，像 `adb`、`kubectl`、`docker` 等命令就能像在普通终端中一样正常使用了！

### 检测规则（按顺序）

1. **系统内置命令**——检查与操作系统相关的内置命令
2. **PATH 中的可执行文件**——扫描 `$PATH` 中的可执行文件
3. **命令历史记录**——与最近的 shell 命令历史记录进行比对
4. **命令模式**——基于命令特征的启发式分析
5. **置信度评分**——综合多种信息做出最终判断

## 检测细节

### 1. 系统内置命令

检查输入是否为当前操作系统的已知内置命令：

| macOS/Linux | Windows (PowerShell) | Windows (CMD) |
|-------------|---------------------|---------------|
| `cd`、`pwd`、`ls` | `cd`、`pwd`、`ls` | `cd`、`dir`、`cls` |
| `echo`、`cat` | `echo`、`cat` | `echo`、`type` |
| `mkdir`、`rm`、`cp` | `mkdir`、`rm`、`cp` | `mkdir`、`del`、`copy` |
| `grep`、`find` | `grep`、`find` | `findstr` |
| `git`、`npm`、`node` | `git`、`npm`、`node` | `git`、`npm`、`node` |

完整列表请参见 `references/builtins/`。

### 2. PATH 中的可执行文件检查

扫描 `$PATH` 目录，确认命令的第一个单词是否为可执行文件：

```bash
# Uses `which` (Unix) or `Get-Command` (PowerShell)
which <command>    # Returns path if exists
```

### 3. 命令历史记录匹配

将输入与最近的 shell 命令历史记录（`~/.zsh_history`、`~/.bash_history`、PowerShell 历史记录）进行比对：
- 完全匹配 → 高置信度
- 前缀相似 → 中等置信度
- 无匹配 → 继续检测

### 4. 命令模式分析

基于命令特征的启发式评分：

| 模式 | 评分 | 例子 |
|---------|-------|---------|
| 以已知命令开头 | +3 | `git status` |
| 包含 shell 操作符 | +2 | `ls` | `grep` |
| 包含路径引用 | +2 | `cd ~/projects` |
| 包含参数/标志 | +1 | `npm install --save` |
| 包含 `$` 变量 | +2 | `echo $HOME` |
| 包含重定向操作 | +2 | `cat file > out` |
| 类似自然语言 | -3 | "please help me" |
| 包含问号 | -2 | "how do I...?" |

### 5. 置信度阈值

```
Score >= 5  → EXECUTE (high confidence command)
Score 3-4   → ASK (uncertain, confirm with user)
Score < 3   → LLM (likely a task/request)
```

## 使用方法

### 自动激活

当满足以下条件时，Terminal Killer 会自动启动：
- 用户输入以动词开头
- 输入内容较短（通常少于 20 个单词）
- 不包含疑问词（如 what、how、why 等）

### 交互式命令

Terminal Killer 会自动识别并处理交互式 shell 命令：
- `adb shell`：在新窗口中打开 adb shell
- `ssh user@host`：在新窗口中打开 SSH 会话
- `docker exec -it container bash`：打开容器 shell
- `mysql -u root -p`：打开 MySQL 客户端
- `python`、`node`、`bash`：在新窗口中打开交互式 REPL

**行为**：
- ✅ 自动在新终端窗口中打开命令
- ✅ 加载你的完整 shell 环境（`~/.zshrc` 等）
- ✅ 保持主终端窗口可用于其他操作

### 手动覆盖

强制执行命令：
```
!ls -la          # Force exec even if uncertain
```

强制使用大型语言模型处理命令：
```
?? explain git   # Force LLM even if looks like command
```

## 安全特性

### 危险命令检测

自动标记潜在的危险操作：
- `rm -rf /` 或类似具有破坏性的命令
- 需要明确授权的 `sudo` 命令
- `dd`、`mkfs`、`chmod 777`
- 对可疑主机的网络操作
- 修改系统文件的命令

### 审批流程

```
Dangerous command detected!

Command: rm -rf ./important-folder
Risk: HIGH - Recursive delete

[Approve] [Deny] [Edit]
```

### 日志记录

所有执行的命令都会被记录到：
```
~/.openclaw/logs/terminal-killer.log
```

日志格式：
```json
{
  "timestamp": "2026-02-28T12:00:00Z",
  "command": "ls -la",
  "confidence": 8,
  "execution_time_ms": 45,
  "output_lines": 12,
  "status": "success"
}
```

## 配置

### 设置

将 Terminal Killer 添加到你的 OpenClaw 配置文件中：

```yaml
terminal-killer:
  enabled: true
  confidence_threshold: 5
  require_approval_for:
    - "rm -rf"
    - "sudo"
    - "dd"
    - "mkfs"
  log_executions: true
  max_history_check: 100  # How many history entries to check
```

### 平台检测

自动检测操作系统并调整检测规则：

```bash
# Auto-detected at runtime
uname -s  # Darwin, Linux, etc.
```

## 实现细节

### 核心脚本

主要检测逻辑位于 `scripts/detect-command.js` 中。

### 辅助脚本

- `scripts/check-path.js`：检查 `$PATH` 中是否存在可执行文件
- `scripts/check-history.js`：与 shell 历史记录进行比对
- `scripts/score-command.js`：计算置信度评分
- `scripts/safety-check.js`：检测危险命令模式

## 测试

详细测试指南请参见 `references/TESTING.md`。

快速测试示例：
```bash
# Run the test suite
node scripts/test-detector.js

# Test specific commands
node scripts/detect-command.js "ls -la"
node scripts/detect-command.js "help me write code"
```

## 限制

- 需要 shell 访问权限（无法在沙箱环境中使用）
- 检查历史记录时需要读取 shell 历史文件
- Windows 版本需要 PowerShell 或 WSL 才能完全使用该功能
- 有些命令可能会被误判为有效命令（因为它们看起来像正常的 shell 命令）

## 贡献方式

若要为你的平台添加新的内置命令：
1. 编辑 `references/builtins/<platform>.txt`
2. 使用 `scripts/test-detector.js` 进行测试
3. 提交包含平台验证的 Pull Request

---

## 👤 关于开发者

**作者：** Cosper  
**联系方式：** [cosperypf@163.com](mailto:cosperypf@163.com)  
**许可证：** MIT

### 📬 联系我们

对这个工具感兴趣？有建议或发现漏洞？或者想参与开发？

- 📧 **电子邮件：** cosperypf@163.com
- 💡 **建议：** 欢迎随时提出！
- 🐛 **漏洞报告：** 请提供平台信息、OpenClaw 版本及示例输入
- 🤝 **合作：** 欢迎贡献和提出改进意见

### 🙏 致谢

这个工具是为 OpenClaw 社区开发的。感谢所有为这个生态系统做出贡献的人！

---

## 📝 更新日志

### v1.1.0 (2026-02-28)

**核心改进：**
1. **✅ 命令执行准确性**：
   - 命令会严格按照输入内容执行
   - 不进行任何修改、优化或添加新功能
   - 保留原始输出（包括进度条、特殊字符等）
2. **🪟 交互式命令识别**：
   - 自动识别交互式命令（如 `adb shell`、`ssh`、`docker exec -it` 等）
   - 在新窗口中打开交互式会话
   - 保持主终端窗口可用于其他操作
   - 加载完整的 shell 环境（`~/.zshrc` 等）
3. **📜 长输出处理**：
   - 能识别超过 2000 字节的输出
   - 显示 200 个字符的预览
   - 提示用户在新窗口中查看完整输出
   - 避免长内容导致界面显示问题

**更新的文件：**
- `scripts/index.js`：长输出处理和交互式命令处理逻辑
- `scripts/interactive.js`：新终端窗口打开器
- `SKILL.md`：更新后的文档
- `README.md`：使用示例
- `clawhub.json`：版本号更新至 1.1.0

---

### v1.0.0 (2026-02-28)

**初始版本发布：**
- 智能命令检测（系统内置命令、PATH、历史记录、模式匹配）
- 跨平台支持（macOS/Linux/Windows）
- 环境变量加载功能
- 危险命令检测机制
- 置信度评分系统

---

**版本：** 1.1.0  
**创建日期：** 2026-02-28  
**最后更新日期：** 2026-02-28