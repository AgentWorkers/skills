---
name: openclaw-bastion-pro
description: "**全套提示注入防御方案：**  
能够检测注入尝试、清除恶意内容、对隐藏的 Unicode 字符进行清洗、部署“金丝雀令牌”（canary tokens）以监控系统状态、隔离被感染的文件，并通过钩子（hooks）强制执行内容策略。这些功能全部包含在 openclaw-bastion（免费版本）中，同时还提供了自动化防御措施。"
user-invocable: true
metadata: {"openclaw":{"emoji":"🏛️","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Bastion Pro

[openclaw-bastion](https://github.com/AtlasPA/openclaw-bastion) 的所有功能（免费版本）再加上自动化防御措施。

**免费版本仅提供检测功能；Pro版本具备入侵拦截、文件隔离和防御功能。**

## 检测命令（免费版本也提供）

```bash
python3 {baseDir}/scripts/bastion.py scan --workspace /path/to/workspace
python3 {baseDir}/scripts/bastion.py scan path/to/file.md --workspace /path/to/workspace
python3 {baseDir}/scripts/bastion.py check path/to/file.md --workspace /path/to/workspace
python3 {baseDir}/scripts/bastion.py boundaries --workspace /path/to/workspace
python3 {baseDir}/scripts/bastion.py allowlist --workspace /path/to/workspace
python3 {baseDir}/scripts/bastion.py status --workspace /path/to/workspace
```

## Pro 版本的防御措施

### 阻止注入攻击

通过将恶意代码包裹在警告注释中来中和文件中的注入攻击。系统会先创建一个备份文件（`.bak`）。被检测到的恶意代码会被标记为 `<!-- [BLOCKED by openclaw-bastion-pro] -->`。

```bash
python3 {baseDir}/scripts/bastion.py block path/to/file.md --workspace /path/to/workspace
```

### 清理隐藏的 Unicode 字符

从文件中删除零宽度字符、RTL（Right-to-Left）文本方向设置以及隐藏的 Unicode 字符，并生成备份文件。系统会详细记录被删除的内容及其位置。

```bash
python3 {baseDir}/scripts/bastion.py sanitize path/to/file.md --workspace /path/to/workspace
python3 {baseDir}/scripts/bastion.py sanitize path/to/directory/ --workspace /path/to/workspace
```

### 隔离被入侵的文件

将含有恶意代码的文件移动到 `.quarantine/bastion/` 目录，并附上相关证据信息。该文件在未明确恢复之前对系统代理不可访问。

```bash
python3 {baseDir}/scripts/bastion.py quarantine path/to/file.md --workspace /path/to/workspace
```

### 恢复被隔离的文件

在调查完成后，将文件恢复到原来的位置。

```bash
python3 {baseDir}/scripts/bastion.py unquarantine path/to/file.md --workspace /path/to/workspace
```

### 部署“金丝雀”标记

在受监控的文件中部署唯一的“金丝雀”字符串。如果发生注入攻击并导致这些文件被泄露，这些标记会出现在泄露的数据中，从而证明攻击的发生。所有“金丝雀”标记都会被记录在一个安全的日志文件中。

```bash
python3 {baseDir}/scripts/bastion.py canary --workspace /path/to/workspace
python3 {baseDir}/scripts/bastion.py canary path/to/specific/file.md --workspace /path/to/workspace
```

### 通过钩子实现自动化防护

生成 Claude Code 钩子配置，以便在文件读取时自动执行安全扫描（针对 Read 工具的 PreToolUse 钩子），并验证命令是否符合安全策略（针对 Bash 工具的 PreToolUse 钩子）。同时还会添加 SessionStart 钩子以进行自动化的安全扫描。

```bash
python3 {baseDir}/scripts/bastion.py enforce --workspace /path/to/workspace
```

### 全自动防御扫描

执行全自动的安全扫描：扫描所有文件，清理隐藏的 Unicode 字符，隔离含有严重威胁的文件，部署“金丝雀”标记，并生成报告。这是启动会话时的推荐操作。

```bash
python3 {baseDir}/scripts/bastion.py protect --workspace /path/to/workspace
```

## 推荐的集成方式

### 会话启动钩子（Claude Code）

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 scripts/bastion.py protect",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### 定期安全检查（OpenClaw）

将相关配置添加到 HEARTBEAT.md 文件中，以实现定期安全检查：
```
- Run injection defense sweep (python3 {skill:openclaw-bastion-pro}/scripts/bastion.py protect)
```

## 可检测的威胁类型

| 类型 | 具体特征 | 危险等级 |
|----------|----------|----------|
| **系统指令篡改** | “ignore previous”、“disregard above”、“you are now”、“new system prompt”、“forget your instructions”、“override safety”、“entering developer mode” | 严重（CRITICAL） |
| **系统提示信息** | `<system>`, `[SYSTEM]`, `<<SYS>>`, `<\|im_start\|>system`, `[INST]`, `### System:` | 严重（CRITICAL） |
| **隐藏的恶意指令** | 用于操控用户的隐藏指令 | 严重（CRITICAL） |
| **HTML 注入** | `<script>`, `<iframe>`, `<img onerror=>` 等元素 | 严重（CRITICAL） |
| **Markdown 数据泄露** | URL 中包含编码数据的图片标签 | 严重（CRITICAL） |
| **危险命令** | `curl \| bash`, `wget \| sh`, `rm -rf /`, 分支炸弹（fork bombs） | 严重（CRITICAL） |
| **Unicode 欺骗手段** | 零宽度字符、RTL 文本方向设置、不可见的格式化内容 | 警告（WARNING） |
| **同形异义词** | 在 ASCII 文本中混入西里尔文/拉丁文字符 | 警告（WARNING） |
| **Base64 编码的恶意数据** | 代码块外的大型编码数据 | 警告（WARNING） |
| **Shell 注入** | 代码块外的 `$(command)` 子shell 执行语句 | 警告（WARNING） |
| **伪造的代码块** | 用恶意代码伪造的代码块边界 | 警告（WARNING） |

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 文件安全，未发现问题 |
| 1 | 检测到警告（建议查看日志） |
| 2 | 发现严重安全问题（需要采取行动） |

## 无需外部依赖

仅依赖 Python 标准库，无需安装任何第三方库（如 pip），也不进行网络请求。所有操作都在本地完成。

## 跨平台兼容性

支持 OpenClaw、Claude Code、Cursor 以及任何遵循 Agent Skills 规范的工具。