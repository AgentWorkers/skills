---
name: openclaw-warden
user-invocable: true
metadata: {"openclaw":{"emoji":"🛡️","requires":{"bins":["python3"]},"os":["darwin","linux","win32"]}}
---

# OpenClaw Warden

该工具会监控您的工作区文件，以防止未经授权的修改和注入攻击。现有的安全工具会在安装前扫描相关文件，而OpenClaw Warden则在安装后持续监控工作区文件本身，从而发现其他工具可能遗漏的篡改行为。

## 重要性

每当会话启动时，您的代理程序会读取SOUL.md、AGENTS.md、IDENTITY.md、USER.md以及内存文件，并对这些文件**默认予以信任**。如果这些文件被恶意篡改，可能会发生以下情况：
- 被注入隐藏指令，从而改变代理程序的行为；
- 在Markdown图片中嵌入数据窃取的URL；
- 被篡改的身份信息和安全设置；
- 在内存文件中被植入持久性的后门程序。

OpenClaw Warden能够检测到所有这些恶意行为。

## 命令

### 建立基准

创建或重置文件的完整性基准。在设置好工作区环境或确认所有文件状态后，可以运行此命令。

```bash
python3 {baseDir}/scripts/integrity.py baseline --workspace /path/to/workspace
```

### 验证文件完整性

将所有被监控的文件与存储的基准进行对比，报告任何修改、删除或新出现的未被跟踪的文件。

```bash
python3 {baseDir}/scripts/integrity.py verify --workspace /path/to/workspace
```

### 扫描注入攻击

检查工作区文件中是否存在注入攻击的迹象，包括隐藏指令、Base64编码的恶意数据、Unicode字符的滥用、通过Markdown图片进行的数据窃取、HTML注入以及可疑的系统提示信息。

```bash
python3 {baseDir}/scripts/integrity.py scan --workspace /path/to/workspace
```

### 全面检查（验证+扫描）

同时执行文件完整性的验证和注入攻击的扫描。

```bash
python3 {baseDir}/scripts/integrity.py full --workspace /path/to/workspace
```

### 快速状态检查

提供工作区安全状况的简短摘要。

```bash
python3 {baseDir}/scripts/integrity.py status --workspace /path/to/workspace
```

### 接受文件变更

在确认变更合法后，可以更新特定文件的完整性基准。

```bash
python3 {baseDir}/scripts/integrity.py accept SOUL.md --workspace /path/to/workspace
```

## 自动检测工作区路径

如果省略了`--workspace`参数，脚本会尝试以下路径来查找工作区：
1. `OPENCLAW_WORKSPACE`环境变量；
2. 当前目录（如果存在AGENTS.md文件）；
3. `~/.openclaw/workspace`（默认路径）。

## 监控的文件类型及对应的警报级别

| 文件类别 | 监控文件 | 变更时的警报级别 |
|----------|-------|-----------------------|
| **关键文件** | SOUL.md, AGENTS.md, IDENTITY.md, USER.md, TOOLS.md, HEARTBEAT.md | 警告（WARNING） |
| **内存文件** | memory/*.md, MEMORY.md | 信息（INFO，因为这些文件可能会发生变化） |
| **配置文件** | 工作区根目录下的*.json文件 | 警告（WARNING） |
| **技能文件** | skills/*/SKILL.md | 警告（WARNING） |

无论文件属于哪种类别，如果检测到注入攻击，系统都会发出**严重警告（CRITICAL）**。

## 常见的注入攻击模式

- **指令篡改**：如“ignore previous instructions”、“disregard above”、“you are now”、“new system prompt”等；
- **Base64编码的恶意数据**：代码块之外的过长Base64字符串；
- **Unicode字符的滥用**：零宽度字符、文本方向（RTL）的篡改、同形异义词的恶意使用；
- **通过Markdown图片窃取数据**：图片标签中包含数据窃取的URL；
- **HTML注入**：脚本标签、iframe元素、隐藏的HTML内容；
- **系统提示信息**：`<system>`, `[SYSTEM]`, `<<SYS>>`等标记；
- **Shell命令注入**：代码块之外的`$(...)`表达式。

## 结果代码

- `0`：文件安全，无问题；
- `1`：检测到修改，需要进一步检查；
- `2`：检测到注入攻击，需要采取行动。

## 依赖关系

仅依赖Python标准库，无需安装额外的第三方库（如pip），也不进行网络请求，所有操作都在本地完成。

## 跨平台兼容性

适用于OpenClaw、Claude Code、Cursor以及任何遵循Agent Skills规范的工具。