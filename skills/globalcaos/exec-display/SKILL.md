---
name: exec-display
version: 1.0.0
description: 结构化的命令执行：支持设置安全级别、使用颜色编码来显示输出结果，并为每个命令提供最多4行的摘要。这一功能增强了所有shell命令的执行过程的透明度和可追溯性。在运行任何exec或shell命令时，建议使用该功能，以确保输出结果的一致性和可审计性。
homepage: https://github.com/openclaw/openclaw
repository: https://github.com/openclaw/openclaw
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["python3"] },
      },
  }
---

# 执行显示（Execution Display）

这是一种结构化、注重安全性的命令执行方式，支持彩色编码的输出结果。

## 为什么需要这个功能？

原始的命令执行方式存在以下问题：
- **可见性不足**：输出信息可能过于冗长或难以查看。
- **缺乏分类**：无法判断命令的风险等级。
- **格式不一致**：不同命令的输出格式各不相同。
- **审计困难**：难以追踪执行了哪些命令以及执行的原因。

该功能实现了以下改进：
- **输出结果限制在4行以内**，并包含简要的总结。
- **明确标注安全等级**（🟢 安全 → 🔴 危险）。
- **使用彩色编码的ANSI格式**，便于在终端中查看。
- **为每个命令提供使用说明**。

## 安全等级

| 等级 | 表情符号 | 颜色 | 说明 |
|-------|-------|-------|-------------|
| 安全（SAFE）| 🟢 | 绿色 | 仅用于读取信息 |
| 低风险（LOW）| 🔵 | 蓝色 | 修改项目文件 |
| 中等风险（MEDIUM）| 🟡 | 修改配置设置 |
| 高风险（HIGH）| 🟠 | 影响系统级别 |
| 危险（CRITICAL）| 🔴 | 可能导致数据丢失，需谨慎操作 |

## 使用方法

### 基本格式

```bash
python3 {baseDir}/scripts/cmd_display.py <level> "<command>" "<purpose>" "$(<command>)"
```

### 示例

**安全等级 - 仅用于读取信息：**
```bash
python3 {baseDir}/scripts/cmd_display.py safe "git status --short" "Check repository state" "$(git status --short)"
```

**低风险 - 修改文件：**
```bash
python3 {baseDir}/scripts/cmd_display.py low "touch newfile.txt" "Create placeholder file" "$(touch newfile.txt && echo '✓ Created')"
```

**中等风险 - 修改配置设置：**
```bash
python3 {baseDir}/scripts/cmd_display.py medium "npm config set registry https://registry.npmjs.org" "Set npm registry" "$(npm config set registry https://registry.npmjs.org && echo '✓ Registry set')"
```

**高风险 - 影响系统级别（需手动执行）：**
```bash
# HIGH/CRITICAL commands should be shown, not executed
python3 {baseDir}/scripts/cmd_display.py high "sudo systemctl restart nginx" "Restart web server" "⚠️ Requires manual execution"
```

### 带有警告和提示的功能

```bash
python3 {baseDir}/scripts/cmd_display.py medium "rm -rf node_modules" "Clean dependencies" "✓ Removed" "This will delete all installed packages" "Run npm install after"
```

## 输出格式

```
🟢 SAFE: READ-ONLY INFORMATION GATHERING: git status --short
✓  2 modified, 5 untracked
📋 Check repository state
```

**带有警告的输出：**
```
🟡 MEDIUM: CONFIGURATION CHANGES: npm config set registry
✓  Registry updated
📋 Set npm registry
⚠️  This affects all npm operations
👉 Verify with: npm config get registry
```

## 与代理（Agent）的集成

### 强制性规则：
1. **所有执行命令都必须使用此封装层**，无例外。
2. **在执行前对每个命令进行安全等级分类**。
3. **为每个命令提供使用说明**，解释执行目的。
4. **简化输出内容**，将冗长的输出压缩成一行。
5. **高风险/危险等级的命令**必须显示出来，并要求用户确认后才能执行。

### 分类指南：

**🟢 安全（SAFE）**：可以直接执行
- `ls`, `cat`, `head`, `tail`, `grep`, `find`
- `git status`, `git log`, `git diff`
- `pwd`, `whoami`, `date`, `env`
- 任何仅用于读取信息的命令

**🔵 低风险（LOW）**：可以执行，但需要通知相关人员
- `touch`, `mkdir`, `cp`, `mv`（在项目范围内操作）
- `git add`, `git commit`
- 在项目范围内修改文件

**🟡 中等风险（MEDIUM）**：执行时需谨慎
- `npm install`, `pip install`（安装依赖包）
- 修改配置文件
- `git push`, `git pull`

**🟠 高风险（HIGH）**：执行前需显示警告并请求确认
- 影响系统服务的命令
- 安装全局包
- 修改网络配置
- 任何可能影响系统状态的命令

**🔴 危险（CRITICAL）**：**严禁直接执行**
- 在重要目录上使用 `rm -rf` 命令
- 使用 `sudo` 权限的命令
- 删除数据库数据
- 任何可能造成数据丢失的操作

## 自定义

### 如何将此功能添加到 SOUL.md 文件中

将以下代码添加到你的代理的 SOUL.md 文件中：

```markdown
## Command Execution Protocol

ALL shell commands MUST use the exec-display wrapper:

1. Classify security level (SAFE/LOW/MEDIUM/HIGH/CRITICAL)
2. Use: `python3 <skill>/scripts/cmd_display.py <level> "<cmd>" "<purpose>" "$(<cmd>)"`
3. HIGH/CRITICAL: Show command for manual execution, do not run
4. Summarize verbose output to one line
5. No exceptions - this is for transparency and auditability
```

### 颜色参考

该脚本使用 ANSI 颜色代码来表示终端输出：
- 绿色（32）：成功，安全等级
- 蓝色（34）：低风险
- 黄色（33）：中等风险，需要警告
- 明亮黄色（93）：高风险
- 红色（31）：危险等级，表示错误
- 青色（36）：命令用途说明行

## 限制

该功能提供了统一的命令显示方式和建议的工具，但真正的代码级强制执行需要使用 OpenClaw 插件，并配置 `before_tool_call` 回调函数。

为了实现最严格的控制，还需将相关规则添加到你的 AGENTS.md 文件或工作区配置中。