# Wreckit Skill（基于jmanhype分支的版本）

> **首次使用？** 请先阅读[SETUP.md](./SETUP.md)，以从jmanhype分支安装Wreckit CLI。

该技能将Clawdbot连接到**Wreckit的jmanhype分支**，即Autonomic Software Factory。此版本针对**Cattle架构**（临时Sprite虚拟机）和高并发循环进行了优化。

**脚本：** `skills/wreckit/scripts/run-wreckit.mjs`  
**引擎：** `wreckit`（来自jmanhype/wreckit的全球CLI）

---

## 触发语句

当用户发出以下指令时，机器人将执行相应的操作：

| 语句 | 操作 |
|--------|--------|
| **"Wreckit status"** | 列出所有项目及其当前状态 |
| **"Wreckit run [ID]"** | 启动项目的自动执行循环（默认模式：Cattle模式） |
| **"Wreckit run [ID] mode pet"** | 以无Sprite模式在本地运行项目（速度更快，但安全性较低） |
| **"Wreckit dream"** | 自主创意生成（自我规划） |
| **"Wreckit doctor"** | 自动诊断和修复问题 |
| **"Wreckit rollback [ID]"** | 将项目回滚到合并前的状态 |
| **"Wreckit next"** | 按顺序处理下一个未完成的项目 |
| **"Wreckit learn"** | 从已完成的项目中提取模式并生成技能 |
| **"Wreckit summarize"** | 为已完成的项目生成可视化视频 |
| **"Wreckit geneticist"** | 分析故障模式并优化系统提示 |

---

## “Cattle”模式的优势（默认设置）
与标准代理循环不同，此版本的Wreckit使用**临时Sprite虚拟机**。每个任务都会启动一个新的Firecracker微虚拟机，独立执行代码后立即销毁，从而避免状态污染，确保最高安全性。

## “Pet”模式（本地模式）
如果您需要快速执行或进行本地调试，可以输入**"mode pet"**。该模式会在主机上直接运行RLM代理。

---

## 使用指南

### 1. 检查状态
> **用户：** "Wreckit status"
> **机器人：** 列出所有活跃的项目（创意中、计划中、进行中、已完成）。

### 2. 运行任务
> **用户：** "Wreckit run 096"
> **机器人：** "正在为项目096启动自动执行循环... [显示日志] ... 完成。"

### 3. 自主创意生成（Dream模式）
> **用户：** "Wreckit dream"
> **机器人：** 扫描代码库中的问题，并自动生成新项目。

### 回滚
> **用户：** "Wreckit rollback 096"
> **机器人：** 使用git操作将项目096回滚到合并前的状态。
>
> **强制回滚：** "Wreckit rollback 096 force" - 即使项目未完成也会强制回滚。

### 处理下一个项目
> **用户：** "Wreckit next"
> **机器人：** 按顺序处理下一个可执行的项目。

### 提取模式（Learn模式）
> **用户：** "Wreckit learn all"
> **机器人：** 从所有已完成的项目中提取模式并生成技能。
>
> **针对特定项目：** "Wreckit learn item 096"
> **按阶段：** "Wreckit learn phase done"

### 生成可视化视频（Summarize模式）
> **用户：** "Wreckit summarize all"
> **机器人：** 为所有已完成的项目生成30秒的可视化视频。
>
> **针对特定项目：** "Wreckit summarize item 096"
> **按阶段：** "Wreckit summarize phase done"

### 优化系统提示（Geneticist模式）
> **用户：** "Wreckit geneticist"
> **机器人：** 分析过去48小时的日志，识别并修复重复出现的错误模式。
>
> **自定义时间窗口：** "Wreckit geneticist time-window 24 min-errors 5"

---

## 高级参数

### 全局参数（适用于所有命令）
- **`--cwd <路径>`** - 更改工作目录
- **`--parallel <数量>`** - 并行处理N个项目（默认值：1）
- **`--verbose`** - 显示详细输出
- **`--dry-run`** - 显示执行过程（不进行实际修改）

### 模式选择
- **`--mode cattle`**（默认）** - 使用临时Sprite虚拟机
- **`--mode pet`** **- 以无Sprite模式在本地运行**

### 命令特定参数

#### 回滚
- **`--force`** - 即使项目未完成也会强制回滚

#### 提取模式
- **`--item <ID>`** - 从特定项目提取模式
- **`--phase <状态>`** - 从处于特定状态的项目中提取模式
- **`--all`** - 从所有已完成的项目中提取模式
- **`--output <路径>`** - 技能文件的输出路径（默认：.wreckit/skills.json）
- **`--merge <策略>`** - 合并策略：追加|替换|询问（默认：追加）
- **`--review`** - 保存前预览提取的技能

#### 生成可视化视频
- **`--item <ID>`** - 为特定项目生成视频
- **`--phase <状态>`** - 为处于特定状态的项目生成视频
- **`--all`** - 为所有已完成的项目生成视频

#### 优化系统提示
- **`--auto-merge`** - 自动提交优化后的代码请求
- **`--time-window <小时数>`** - 分析过去N小时的日志（默认：48小时）
- **`--min-errors <错误次数>`** - 识别重复错误模式的阈值（默认：3次）

---

## 配置要求
该技能假设`wreckit`已全局安装或在指定路径下可用。
如果在Docker中运行，请确保容器能够访问项目目录。

### 并行处理
当使用`--parallel`参数处理多个项目（如`learn --all`或`summarize --all`）时，系统会同时处理N个项目。为确保机器人安全，默认设置为1（顺序处理）。

### 更改工作目录
使用`--cwd`参数可以指定不同于当前工作目录的路径。这有助于管理多个项目或在容器化环境中操作。