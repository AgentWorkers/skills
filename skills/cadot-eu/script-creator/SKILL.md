---
name: script-git-manager
description: 在 `~/.nanobot/workspace/test` 目录下创建和修改脚本时，需严格遵循 Git 版本控制规范。每个脚本都应保存在其自己的目录中，并且该目录应拥有独立的 Git 仓库。在执行任何脚本之前，请务必确认创建计划，并在每个执行步骤中报告进度。Python 环境及包管理通过 `~/.nanobot/workspace/venv` 来实现。
---
# 脚本 Git 管理技能

该技能遵循严格的、确定性的工作流程来创建和修改脚本，仅使用 Git 作为状态存储工具。其设计目的是防止意外创建文件、无控制的代码重构以及历史记录的丢失。

---

## 范围

- 基本目录：`~/.nanobot/workspace/test`
- Python 虚拟环境：`~/.nanobot/workspace/venv`
- 每个脚本对应一个目录，每个目录对应一个 Git 仓库
- 必须使用 Git，并且 Git 是唯一的存储机制

---

## Python 环境

所有与 Python 相关的操作（如 `pip install`、脚本执行）都必须使用虚拟环境：

**在执行任何 `pip` 或 `python` 命令之前，务必激活虚拟环境。**

---

## 创建流程

**仅当用户明确要求创建新脚本时，才使用此流程。**

### 第 1 阶段：计划确认

在创建任何内容之前，向用户展示详细的创建计划：

**在继续之前，请等待用户的明确确认。**

### 第 2 阶段：逐步执行

按顺序执行每个步骤，并在每个步骤完成后报告进度：

**步骤 1：创建目录**
```bash
cd ~/.nanobot/workspace/test
mkdir <script_name>
```
输出：`✓ 创建目录： ~/.nanobot/workspace/test/<script_name>`

**步骤 2：初始化 Git**
```bash
cd <script_name>
git init
```
输出：`✓ 初始化 Git 仓库`

**步骤 3：创建脚本文件**
```bash
touch <script_name>.<extension>
```
输出：`✓ 创建文件：<script_name>.<extension>`

**步骤 4：安装依赖项（如果脚本依赖于某些包）**
```bash
source ~/.nanobot/workspace/venv/bin/activate
pip install <package1> <package2> ...
deactivate
```
输出：`✓ 安装了 Python 包：<package_list>`

**步骤 5：编写脚本内容**
```bash
# Write the actual script code to the file
```
输出：`✓ 脚本内容已编写（<X> 行）`

**步骤 6：创建初始提交**
```bash
git add .
git commit -m "Initial commit: <script_name>"
```
输出：`✓ 创建了初始 Git 提交`

**最终总结：**
```
✅ Script created successfully!

Location: ~/.nanobot/workspace/test/<script_name>/<script_name>.<extension>
Git status: Clean (1 commit)
[If Python] Virtual environment: ~/.nanobot/workspace/venv
```

---

## 修改流程

**仅当用户要求修改现有脚本时，才使用此流程。**

### 第 1 阶段：计划确认

在修改之前，向用户展示修改计划：

**在继续之前，请等待用户的明确确认。**

### 第 2 阶段：逐步执行

**步骤 1：进入脚本目录**
```bash
cd ~/.nanobot/workspace/test/<script_name>
```
输出：`✓ 进入了脚本目录`

**步骤 2：创建检查点**
```bash
git add .
git commit -m "Checkpoint before modification"
```
输出：`✓ 创建了检查点提交`

**步骤 3：应用修改**
```bash
# Modify the script file as requested
```
输出：`✓ 修改已应用于 <script_file>`

**步骤 4：安装新的依赖项（如适用）**
```bash
source ~/.nanobot/workspace/venv/bin/activate
pip install <new_package>
deactivate
```
输出：`✓ 安装了新包：<package_list>`

**步骤 5：提交更改**
```bash
git add .
git commit -m "<concise description of the change>"
```
输出：`✓ 更改已提交："<commit_message>"`

**最终总结：**
```
✅ Script modified successfully!

Location: ~/.nanobot/workspace/test/<script_name>/<script_file>
Changes: <brief summary>
Git commits: 2 new commits (checkpoint + modification)
```

---

## 绝对不能违反的规则

- 除非明确收到指令，否则不得创建新的脚本。
- 未经用户确认计划，不得开始任何操作。
- 每个步骤完成后都必须报告进度。
- 除非明确收到指令，否则不得创建额外的文件。
- 严禁跳过修改前的 Git 提交。
- 严禁修改目标脚本之外的文件。
- 严禁篡改 Git 的历史记录。
- 严禁使用系统自带的 Python 解释器，必须使用 `~/.nanobot/workspace/venv` 中的 Python 解释器。
- 严禁假设用户的意图是模糊的或未明确的。

---

## 决策规则

- 如果脚本目录不存在 → 使用创建流程。
- 如果脚本目录已经存在 → 使用修改流程。
- 如果用户的意图不明确 → 请请求澄清，否则不要进行任何操作。
- 如果计划未得到确认 → 停止操作并等待用户的确认。

---

## 进度报告格式

使用以下符号来保持一致性：

- `📋` 计划展示
- `✓` 步骤成功完成
- `✅` 最终成功总结
- `⚠️` 需要警告或进一步澄清
- `❌` 出现错误或失败

每个步骤的输出应简洁（1-2 行），但信息要准确。

---

## 哲学原则

Git 是我们的“记忆系统”。
文件系统是我们之间的“契约”。
确认步骤可以防止错误。
透明度有助于建立信任。
虚拟环境（`venv`）用于隔离各个脚本的依赖关系。