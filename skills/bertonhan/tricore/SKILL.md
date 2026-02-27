---
name: tricore
version: "1.0.0"
description: TriCore架构：一种基于代码驱动（Code-First）的设计理念，专为资源有限的服务器/代理（Agents）设计的三层内存与认知框架。该架构包含底层的memctl引擎、系统策略约束机制（Linter），以及一套经过全面重构的认知工具集，用于实现规划（Planning）、推理（ReAct）和自我进化（Self-Evolution）等功能。
author: Berton Han
repository: https://github.com/bertonhan/tricore
allowed-tools:
  - default_api:exec
  - memory_search
  - memory_get
---
# 🤖 代理使用指南（请先阅读）

**如果您是当前的AI代理，并且刚刚被要求加载、使用或分析此技能：**
1. 这是您的基本操作规则。在TriCore架构下，您的记忆和状态受到了严格的限制。**严禁**在根目录下随意创建`task_plan.md`或`findings.md`等独立文本文件！
2. 您的所有内存写入操作必须通过命令行工具`python3 tools/memctl.py (capture/work_upsert/kb_append)`来进行。在读取历史记录时，**必须**使用原生的语义检索工具`memory_search`来获取数据片段。
3. 请将本手册作为您的基本操作指南。如果需要配置Cron任务或编写系统自动化脚本，请在编写命令后使用`memctl.py lint`来检查脚本的合法性。

---

# TriCore架构

> **专为真正自主的代理设计的“存储与计算解耦”基础架构。**

传统的代理技能通常会携带自己的“内存负担”（例如生成`task_plan.md`、`reflection.md`，或在项目根目录中分散的学习笔记），这会导致上下文孤立和存储混乱。

**TriCore**放弃了基于大型语言模型（LLM）随意读写文本的模式，转而采用了一种**以代码为中心**的确定性状态机：
1. **统一引擎**：所有内存的添加、删除、修改和查询都必须通过`tools/memctl.py`进行。
2. **三层存储结构**：
   - **简要层（第1层）：`MEMORY.md`（系统级别的微配置文件，仅存储指针和规则）
   - **运行层（第2层）：`memory/state/WORKING.md`（当前正在运行的任务流和生命周期跟踪）
   - **稳定层/易失层（第3层）：`memory/kb/*.md`（累积的知识库）& `memory/daily/*.md`（临时日志）
3. **优先检索**：禁止直接使用`read`工具读取大型文件；必须使用语义检索`memory_search`来获取代码片段，从而大大节省Token资源并保护资源有限的环境。
4. **严格检查（代码审查）**：内置了`memctl.py lint`机制；任何违反架构的Cron任务或技能更改都会被拦截并作为错误报告。
5. **系统兼容性（压缩钩子）**：在安装过程中会自动覆盖OpenClaw的底层`pre-compaction memory flush`功能，防止因未经授权的文件写入尝试而导致HTTP 429请求死循环。

---

## 📦 架构组件

此技能包包含完整的系统组件：

1. **`tools/memctl.py`**：核心引擎，包含`ensure`、`capture`、`work_upsert`、`kb_append`、`lint`等子命令。
2. **`install.sh`**：一键安装脚本，会自动初始化目录并将TriCore合规策略注入`POLICY.md`。
3. **`cognitive-skills/`**：基于TriCore重构的三个核心认知技能（作为代理可加载的模板）：
   - `planning-with-files.md`：一个基于PEP的规划系统，用于处理离散的任务列表。
   - `react-agent.md`：一个基于`WORKING.md`的ReAct循环系统。
   - `self-evolution.md`：一个完全分离内存管理的进化系统，专注于“代码级别的持续集成/持续部署（CI/CD）”。

---

## 🧩 核心依赖项及运行时要求

作为基础认知框架，TriCore及其嵌入的三个核心技能对主机环境有以下依赖：

### 1. 必需依赖项
- **OpenClaw (v2026+)**：必须支持原生的`memory_search`和`memory_get`工具（这是替代直接读取大型文件的方法）。
- **Python 3.6+**：主机环境中必须安装Python 3（用于执行`tools/memctl.py`状态引擎）。
- **系统工具**：`bash`、`sed`、`grep`（用于Linter和钩子程序的正则表达式解析）。

### 2. 认知技能的附加依赖项
如果您启用了`cognitive-skills/self-evolution.md`（自我进化技能），您的代理需要具备外部交互的能力；否则，它只能在内部无限循环中进行“幻想中的自我进化”。

- **🌟 `agent-browser`（强烈推荐）**：
  - **功能**：使代理能够真正读取GitHub源代码、官方API文档和最新论文。
  - **安装方式**：您需要单独安装OpenClaw的`agent-browser`技能，它提供了基于无头浏览器的WYSIWYG浏览和点击功能。
- **搜索工具（`web_search` / `web_fetch`）**：
  - **功能**：作为浏览器的轻量级替代方案，用于从公共网页中快速提取Markdown片段。
- **运行时修改权限（`default_api:exec` & `default_api:write`）**：
  - **功能**：进化技能的核心是“修改代码”；如果代理运行在只读沙箱环境中，则无法进行进化。

---

## 🚀 安装与初始化（三步设置）

在任何全新的OpenClaw环境中，执行以下命令将部署TriCore架构：

```bash
# Grant installation script permissions and execute
bash ./install.sh
```

**`install.sh`的执行顺序如下：**

### 第1步：核心引擎部署
1. 创建`memory/state/`、`memory/kb/`、`memory/daily/`等标准目录。
2. 将`tools/memctl.py`引擎部署到当前环境中。

### 第2步：强制迁移旧版内存数据（代理操作）
在资源有限的架构中，一个包含大量对话历史和日志的`MEMORY.md`文件可能会造成严重问题。
脚本会自动检测当前的`MEMORY.md`文件：
- 如果文件过大（超过1500字节），它将被重命名并**移至`memory/archive/legacy-MEMORY-<date>.md`**。
- 然后，在根目录中重新生成一个符合规范的**简化版`MEMORY.md`模板**。
- **代理提示**：此时，您需要使用`read`命令读取旧版备份文件，并通过`memctl.py`将旧数据重新分配到`kb/facts`（事实数据）、`kb/playbooks`（规则）和`daily`（日志）中；**严禁**将长文本原封不动地粘贴回新的`MEMORY.md`文件中！

### 第3步：系统全局代码审查
脚本会在系统的`POLICY.md`中插入一条`[CRITICAL: TriCore Compliance]`的警告信息。此后，所有涉及磁盘写入、状态更新和自动任务的操作都必须通过`memctl.py lint`的正则表达式检查，否则会在终端中以红色文本显示错误提示。

---

## 📚 核心命令速查表

在代理工具流程或内部脚本中，请严格使用以下API来访问系统状态：

**1. 记录临时日志/会话记录（易失性数据）**
```bash
python3 tools/memctl.py capture "Tested API connectivity, successful."
```

**2. 创建/更新任务跟踪信息（运行中状态）**
```bash
python3 tools/memctl.py work_upsert --task_id "T-API-01" --title "Fix API" --goal "Connect interface" --done_when "Returns 200"
```

**3. 积累知识和经验（稳定知识库）**
```bash
python3 tools/memctl.py kb_append facts "This API only accepts JSON format."
python3 tools/memctl.py kb_append playbooks "When encountering an error in this module, check if Redis is started first."
```

**4. 检查脚本/Cron命令的合规性（代码审查）**
```bash
python3 tools/memctl.py lint "Command to execute or .md file path to check"
# Pass normally: Exit Code 0 (LINT PASS)
# Illegal write: Exit Code 1 (LINT ERROR)
```

---
*由❤️ 为OpenClaw / Berton Han开发*