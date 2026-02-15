---
name: smalltalk
version: 1.7.0
description: 与实时的 Smalltalk 实例（Cuis 或 Squeak）进行交互。可用于评估 Smalltalk 代码、浏览类、查看方法源代码、定义类/方法、查询类层次结构及分类等信息。
metadata: {"clawdbot":{"emoji":"💎","requires":{"bins":["python3","xvfb-run"]}}}
---

# Smalltalk 技能

通过 MCP 执行 Smalltalk 代码并浏览实时的 Squeak/Cuis 映像。

## 先决条件

**首先获取 ClaudeSmalltalk 仓库：**

```bash
git clone https://github.com/CorporateSmalltalkConsultingLtd/ClaudeSmalltalk.git
```

该仓库包含：
- 用于 Squeak 的 MCP 服务器代码（`MCP-Server-Squeak.st`）
- 设置文档（`SQUEAK-SETUP.md`、`CLAWDBOT-SETUP.md`）
- 本 Clawdbot 技能（`clawdbot/`）

## 设置

1. **使用 MCP 服务器设置 Squeak** — 请参阅 [SQUEAK-SETUP.md](https://github.com/CorporateSmalltalkConsultingLtd/ClaudeSmalltalk/blob/main/SQUEAK-SETUP.md)
2. **配置 Clawdbot** — 请参阅 [CLAWDBOT-SETUP.md](https://github.com/CorporateSmalltalkConsultingLtd/ClaudeSmalltalk/blob/main/CLAWDBOT-SETUP.md)

## 使用方法

```bash
# Check setup
python3 smalltalk.py --check

# Evaluate code
python3 smalltalk.py evaluate "3 factorial"
python3 smalltalk.py evaluate "Date today"

# Browse a class
python3 smalltalk.py browse OrderedCollection

# View method source (instance side)
python3 smalltalk.py method-source String asUppercase

# View method source (class side)
python3 smalltalk.py method-source "MCPServer class" version
python3 smalltalk.py method-source MCPServer version --class-side

# List classes (with optional prefix filter)
python3 smalltalk.py list-classes Collection

# Get class hierarchy
python3 smalltalk.py hierarchy OrderedCollection

# Get subclasses  
python3 smalltalk.py subclasses Collection

# List all categories
python3 smalltalk.py list-categories

# List classes in a category
python3 smalltalk.py classes-in-category "Collections-Sequenceable"

# Define a new class
python3 smalltalk.py define-class "Object subclass: #Counter instanceVariableNames: 'count' classVariableNames: '' poolDictionaries: '' category: 'MyApp'"

# Define a method
python3 smalltalk.py define-method Counter "increment
    count := (count ifNil: [0]) + 1.
    ^ count"

# Delete a method
python3 smalltalk.py delete-method Counter increment

# Delete a class
python3 smalltalk.py delete-class Counter
```

## 操作模式

### 游戏场模式（默认）
使用默认的临时图像。当守护进程停止时，所做的更改将被丢弃。
用户输入：`load Smalltalk skill` 或 `invoke Smalltalk` — 无需特殊参数。

```bash
# Start playground daemon
nohup python3 smalltalk-daemon.py start > /tmp/daemon.log 2>&1 &
```

### 开发模式
用户提供自己的图像和更改文件对。更改会在会话之间保持持久。
用户输入：`load Smalltalk skill in dev mode with ~/MyProject.image`

```bash
# Start dev daemon with custom image
nohup python3 smalltalk-daemon.py start --dev --image ~/MyProject.image > /tmp/daemon.log 2>&1 &
```

开发模式会将 `SMALLTALK_DEV_MODE` 设置为 1，这样 MCP 服务器会保留 `.changes` 文件（而不是将其重定向到 `/dev/null`）。提供的图像必须有一个对应的 `.changes` 文件。

### 常用命令
```bash
# Check status
python3 smalltalk.py --daemon-status

# Stop daemon
python3 smalltalk-daemon.py stop

# Restart in dev mode
python3 smalltalk-daemon.py restart --dev --image ~/MyProject.image
```

## 命令

| 命令 | 描述 |
|---------|-------------|
| `--check` | 验证虚拟机/图像路径及依赖关系 |
| `--daemon-status` | 检查守护进程是否正在运行 |
| `--debug` | 调试挂起的系统（发送 SIGUSR1 并捕获堆栈跟踪） |
| `evaluate <code>` | 执行 Smalltalk 代码并返回结果 |
| `browse <class>` | 获取类元数据（超类、实例方法 `methods` 和 `classMethods`） |
| `method-source <class> <selector> [--class-side]` | 查看方法源代码（支持 `"Class class"` 语法或 `--class-side` 标志） |
| `define-class <definition>` | 创建或修改类 |
| `define-method <class> <source>` | 添加或更新方法 |
| `delete-method <class> <selector>` | 删除方法 |
| `delete-class <class>` | 删除类 |
| `list-classes [prefix]` | 列出类（可选过滤） |
| `hierarchy <class>` | 获取超类链 |
| `subclasses <class>` | 获取直接子类 |
| `list-categories` | 列出所有系统类别 |
| `classes-in-category <cat>` | 列出某个类别中的类 |
| `explain <code>` | 解释 Smalltalk 代码（需要 `ANTHROPIC_API_KEY` 或 `OPENAI_API_KEY`） |
| `explain-method <class> <sel> [--class-side] [--source <code>]` | 从图像中获取方法并解释它（或使用 `--source`/`--source-file`/`--source-stdin` 绕过守护进程） |
| `audit-comment <class> <sel> [--class-side] [--source <code>]` | 审计方法注释与实现（或使用 `--source`/`--source-file`/`--source-stdin` 绕过守护进程） |
| `audit-class <class>` | 审计类中的所有方法（实例和类方法） |
| `generate-sunit <targets> [--force] [--class-name <name>]` | 为方法生成 SUnit 测试并将其保存到图像中 |

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `SQUEAK_VM_PATH` | Squeak/Cuis 虚拟机可执行文件的路径 |
| `SQUEAK_IMAGE_PATH` | 包含 MCP 服务器的 Smalltalk 图像路径 |
| `ANTHROPIC_API_KEY` | Anthropic Claude 的 API 密钥（推荐用于 LLM 工具） |
| `ANTHROPIC_MODEL` | Anthropic 模型（默认：`claude-opus-4-20250514`） |
| `OPENAI_API_KEY` | OpenAI 的 API 密钥（LLM 工具的备用选项） |
| `OPENAI_MODEL` | OpenAI 模型（默认：`gpt-4o`） |
| `LLM_PROVIDER` | 强制指定 LLM 提供者：`anthropic` 或 `openai`（未设置时自动检测） |

## 与 Claude Code 一起使用（MCP 模式）

当 Claude Code 通过 MCP 连接到实时 Smalltalk 图像时，`explain-method` 和 `audit-comment` 可以使用预先获取的源代码，而无需运行守护进程。可以使用 `--source`、`--source-file` 或 `--source-stdin` 直接传递方法源代码：

```bash
# Inline source (fetched via MCP, passed on command line)
python3 smalltalk.py explain-method SmallInteger + --source "+ aNumber <primitive: 1> ^ super + aNumber"

# Source from a file
python3 smalltalk.py audit-comment Integer factorial --source-file /tmp/factorial.st

# Source piped via stdin
echo "printString ^ self printStringLimitedTo: 50000" | python3 smalltalk.py explain-method Object printString --source-stdin
```

这三个源代码相关参数是互斥的。如果未提供任何参数，系统将像之前一样使用守护进程。

## 生成 SUnit 测试

`generate-sunit` 命令使用 LLM 为 Smalltalk 方法生成 SUnit 测试用例，并将它们直接保存到正在运行的图像中：

```bash
# Generate tests for a single method
python3 smalltalk.py generate-sunit "String>>asUppercase"

# Generate tests for multiple methods
python3 smalltalk.py generate-sunit "Random>>next" "Random>>nextInt:" "Random>>seed:"

# Generate tests for an entire class (all instance methods)
python3 smalltalk.py generate-sunit "OrderedCollection"

# Generate tests for class-side methods
python3 smalltalk.py generate-sunit "Date class>>today"

# Custom test class name
python3 smalltalk.py generate-sunit "String>>asUppercase" --class-name MyStringTests

# Overwrite existing test class
python3 smalltalk.py generate-sunit "String>>asUppercase" --force

# Run the generated tests
python3 smalltalk.py evaluate "StringGeneratedTest buildSuite run printString"
```

生成的测试用例使用标准的 SUnit 断言（`assert:`, `assert:equals:`, `deny:`, `should:raise:`），并保存到 `GeneratedSUnit-*` 目录中。

## 注意事项

- 在 Linux 服务器上无头操作需要 xvfb
- 使用 Squeak 6.0 MCP 服务器（如果有显示设备，GUI 仍然可以响应）
- 为安全考虑，故意排除了 `saveImage` 命令 |
- 需要 MCPServer 7.0 或更高版本（v7 版本支持类级方法） |
- 游戏场模式：临时性，.changes 文件会被丢弃到 `/dev/null` |
- 开发模式：更改会持久保存，需要使用 `--dev --image PATH` 参数