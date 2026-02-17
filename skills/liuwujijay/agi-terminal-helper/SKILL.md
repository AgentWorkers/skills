---
name: terminal-helper
description: 一份实用的运行手册，用于安全地使用 OpenClaw（遵循“沙箱优先”原则、进行明确确认操作以及使用调试工具）。
user-invocable: true
disable-model-invocation: false
metadata: { "openclaw": { "emoji": "🖥️", "os": ["darwin","linux","win32"] } }
---
# 终端辅助工具——用于 OpenClaw 执行的运行手册

本技能并非通用的终端提示模板，而是一份具体的运行手册，旨在指导如何在实际工作环境中（例如 `/Users/.../clawd` 工作空间）有效使用 OpenClaw 的 `exec` 工具。重点关注以下方面：

- 沙箱环境与主机环境的执行差异
- 可预测的工作目录
- 长时间运行的进程
- macOS 上的权限问题（如 Peekaboo、屏幕录制、UI 自动化）
- 如何避免因误操作导致的脚本执行错误

OpenClaw 相关的技能是从预装的技能包（`~/.openclaw/skills`）或 `<workspace>/skills` 中加载的，其中以工作空间中的技能优先级为准。 :contentReference[oaicite:12]{index=12}

## 运行原则（每次执行时都会遵循的步骤）

### 1) 明确执行意图及具体命令
在调用 `exec` 命令之前，我会说明：
- 该命令的目的
- 命令将在哪个目录中执行
- 命令可能会读取或写入哪些文件
- 我期望的输出结果（以便及时发现异常情况）

### 2) 默认采用只读模式进行探索
在调试或了解系统状态时，我会使用以下命令：
- `pwd`、`ls -la`、`git status`、`rg`、`cat`、`head`、`tail`
- 只有在了解具体情况后，才会进行写入或安装操作

### 3) 对于不可信或变化频繁的操作，优先使用沙箱环境
对于以下操作，建议使用沙箱环境：
- 测试、构建、依赖项安装
- 探索未知的代码仓库
- 运行来自第三方来源的脚本

**重要提示**：
如果当前会话处于沙箱环境中，沙箱环境不会继承主机的 `process.env` 变量。全局环境变量以及 `skills.entries.<skill>.env/apiKey` 仅适用于主机环境；沙箱环境中的环境变量需要单独设置。 :contentReference[oaicite:13]{index=13}

### 4) 对任何高风险操作进行明确确认
在执行以下操作之前，我会要求用户进行确认：
- 删除或覆盖文件
- 安装系统级软件包
- 修改 `~/.ssh` 文件、密钥链或浏览器配置文件
- 更改网络或系统设置
- 运行需要权限的命令（如 `sudo`、`launchctl`）

## 执行方式

### A) 明确指定工作目录
在诊断 OpenClaw 本身的问题时，我会在你的工作空间内进行操作（例如 `/Users/proman/clawd`），并明确指出工作空间的位置。

**常用命令示例**：
- 检查技能列表：
  - `ls -la ./skills`
  - `find ./skills -maxdepth 2 -name SKILL.md -print`
- 检查 Git 仓库状态：
  - `git status`（如果工作空间是 Git 仓库）
- 验证二进制文件的存在：
  - `which peekaboo || echo "peekaboo 未添加到 PATH 中"`

### B) 保持命令的单一用途
尽量使用多个简单的命令，而不是一个能完成所有操作的复杂脚本。这样更便于审查和审批。

### C) 长时间运行的命令：后台执行并定期检查状态
如果支持的话，应使用后台执行方式，并定期检查命令的执行进度。

**可参考的示例**：
- 启动长时间运行的构建任务：
  - `exec: make test`（并设置适当的等待时间）
- 定期检查任务完成情况：
  - `process: poll`（使用返回的会话 ID）

（具体命令参数名称可能因工具而异，但基本思路是：先执行命令，然后定期检查其状态。）

## 实用运行手册示例

### 手册 1：“我的技能无法加载”
1) 确认技能文件的存放位置及加载优先级：
   - OpenClaw 会优先加载 `<workspace>/skills` 中的技能文件。 :contentReference[oaicite:14]{index=14}
2) 确认技能文件夹中是否存在 `SKILL.md` 文件以及有效的文档结构。
3) 如果你修改了相关文件，请确保已启用文件监控功能：
   - 默认情况下，`skills.load.watch: true` 会被启用。 :contentReference[oaicite:15]{index=15}

### 手册 2：“在终端中可以正常使用 Peekaboo，但在 OpenClaw 中却出问题”
这通常是由于 macOS 的 TCC（Terminal Configuration Controller）设置或 OpenClaw 应用的后台进程导致的。常见的解决方法是在 OpenClaw.app 中启用 PeekabooBridge 功能：
- 进入设置 → 启用 Peekaboo Bridge。 :contentReference[oaicite:16]{index=16}
之后，验证 `peekaboo bridge status --verbose` 的输出结果，确保显示的是主机（OpenClaw.app）的相关信息，而不是本地进程。 :contentReference[oaicite:17]{index=17}

### 手册 3：“ClawHub 拒绝接受我的技能文档”
ClawHub 有文档质量检查机制（包括语言检测和内容分析），会拒绝内容过于简单或格式不符合要求的文档。 :contentReference[oaicite:18]
解决方法包括：
- 添加具体的使用示例
- 提供详细的错误排查信息
- 添加关于环境配置（如沙箱环境、PATH 变量、权限设置）的说明
- 明确说明技能的具体用途、适用场景和操作步骤

## 我不会做的操作
- 未经用户明确请求和审核，我不会执行远程安装脚本（例如 `curl | sh`）。
- 我不会在命令中直接输入或显示敏感信息。
- 在未确认文件路径的情况下，我不会进行任何可能破坏系统状态的修改。

## 我经常使用的快捷命令：
- `pwd`
- `ls -la`
- `git status`
- `rg -n "error|warn|TODO" .`
- `uname -a`
- `node -v && python -V`

如果你需要直接执行命令（不涉及任何模型处理），可以使用 `/term` 命令。