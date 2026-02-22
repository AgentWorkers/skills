# 🔍 Sightglass — 代理供应链智能

您的 AI 编码代理刚刚为项目添加了 47 个依赖项。您知道它为什么选择这些依赖项吗？

**Sightglass** 通过监控 AI 编码代理的行为，记录下所有的工具选择、依赖项安装以及架构决策，从而揭示出您可能未曾注意到的风险、偏见以及更好的替代方案。

## 为什么这很重要

当人类开发者选择依赖项时，背后通常有明确的理由：他们会阅读相关博客文章、比较不同的选项，并参与团队讨论。然而，当 AI 代理做出选择时，这些决策过程对开发者来说是不可见的。AI 代理只是根据训练数据来决定使用哪些依赖项，这可能导致以下问题：
- 选择那些在训练数据收集时流行的依赖项；
- 选择在 Stack Overflow 上被频繁提及的依赖项（但不一定是最好的选择）；
- 选择在类似项目中使用过的依赖项（但这些依赖项可能并不适合当前项目的需求）。

Sightglass 能让这些隐性的决策过程变得透明化。

## 发现方式的分类

Sightglass 会对代理获取依赖项的方式进行分析，并给出相应的分类：

| 分类 | 含义 | 风险等级 |
|---|---|---|
| **TRAINING_RECALL** | 代理仅根据训练数据做出选择（未进行任何搜索） | 🟡 中等风险 |
| **CONTEXT_INHERITANCE** | 依赖项存在于现有的项目文件中（如 `package.json`、导入语句等） | 🟢 低风险 |
| **REACTIVE_SEARCH** | 代理在遇到问题后主动搜索解决方案 | 🟡 中等风险 |
| **PROACTIVE_SEARCH** | 代理在选择依赖项前主动比较了多个选项 | 🟢 低风险 |
| **USERDIRECTED** | 人类明确指定了代理应使用的依赖项 | ⚪ 无风险 |

如果 `TRAINING_RECALL` 的比例过高，这可能是一个危险信号，说明代理在自动运行，缺乏自主思考的能力。

## 快速入门

### 1. 设置

```bash
./skills/sightglass/setup.sh
```

此步骤用于安装 Sightglass 的命令行工具 (`@sightglass/cli`)，进行初始配置，并启动监控守护进程。

### 2. 登录

```bash
sightglass login
```

通过 [sightglass.dev](https://sightglass.dev) 进行登录，以启用云分析和历史数据记录功能。

### 3. 监控

```bash
sightglass watch
```

启动后台监控进程，实时跟踪代理的会话活动（文件更改、依赖项安装、工具调用等）。

### 4. 分析

```bash
sightglass analyze
# or
./skills/sightglass/analyze.sh --since "1 hour ago" --format json
```

## 与 OpenClaw 的集成

Sightglass 支持对编码代理会话进行预处理和后处理：

**会话开始前** — `hooks/pre-spawn.sh`：
- 记录会话开始时间和项目上下文；
- 确保监控守护进程正在运行。

**会话结束后** — `hooks/post-session.sh`：
- 分析会话中发生的所有操作；
- 输出分析结果：发现的风险、依赖项的来源（是来自训练数据还是搜索结果）、以及错过的替代方案。

### 与编码代理结合使用

当您通过 OpenClaw 启动编码代理时，可以将其与 Sightglass 配合使用：

```bash
# Before spawning
source ./skills/sightglass/hooks/pre-spawn.sh /path/to/project

# ... agent does its work ...

# After session ends
./skills/sightglass/hooks/post-session.sh
```

会话结束后的分析输出示例：

```
📊 Session Summary
  Dependencies added: 12
  Risks found: 3
  Training recall: 67%
  Alternatives missed: 5

  ⚠️  Run 'sightglass analyze --since ...' for details
```

如果 `TRAINING_RECALL` 的比例为 67%，这意味着有三分之二的依赖项是直接从训练数据中选取的，而没有经过任何比较。Sightglass 会显示这些依赖项的其他可用替代方案。

## 命令参考

### 命令行工具 (`@sightglass/cli`)

| 命令 | 功能 |
|---|---|
| `sightglass init` | 在项目目录中初始化 Sightglass |
| `sightglass login` | 通过 sightglass.dev 进行登录 |
| `sightglass setup` | 进行首次配置 |
| `sightglass watch` | 启动监控守护进程 |
| `sightglass analyze` | 分析代理的会话行为和依赖项选择 |

### 技能脚本

| 脚本 | 功能 |
|---|---|
| `setup.sh` | 安装 Sightglass 命令行工具、进行配置并验证监控功能 |
| `analyze.sh` | 独立分析会话数据（支持 `--since`、`--session`、`--format`、`--push` 等参数） |
| `hooks/pre-spawn.sh` | 会话开始前的预处理脚本 |
| `hooks/post-session.sh` | 会话结束后的分析脚本 |

### `analyze.sh` 的参数说明

```
--since <time>     Analysis window start (ISO timestamp or relative like "1 hour ago")
--session <id>     Analyze a specific session by ID
--format <fmt>     Output format: text (default), json, markdown
--push             Push results to https://sightglass.dev
```

## Sightglass 提供的信息

对于每个代理会话，您将获得以下信息：
- **依赖项清单**：所有被添加、删除或升级的依赖项；
- **发现方式**：代理获取依赖项的具体途径（是来自训练数据还是通过搜索）；
- **风险提示**：存在的安全漏洞、未维护的依赖项以及更好的替代方案；
- **替代方案建议**：代理本可以选用但实际未选择的选项；
- **偏见指标**：显示训练数据对代理决策的影响程度。

## API

所有数据会在登录后自动同步到 [sightglass.dev](https://sightglass.dev)。您可以使用 `--push` 参数将分析结果推送至该平台，或在配置时设置自动推送功能。

---

*您的代理使用的依赖项实际上就是您项目的依赖项。了解这些依赖项的来源至关重要。*