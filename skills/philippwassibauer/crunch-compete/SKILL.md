---
name: crunch-compete
description: >
  **使用说明：**  
  适用于参与Crunch竞赛时——用于设置工作空间、查看快速入门指南、在本地测试解决方案或提交参赛作品。
---
# Cruncher 技能

本文档指导用户完成 Crunch 竞赛的整个生命周期：包括环境搭建、快速入门工具的发现、解决方案的开发、本地测试以及解决方案的提交。

## 先决条件

请安装 [uv](https://docs.astral.sh/uv/)，用于管理 Python 环境：
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 快速搭建

**每个竞赛都需要独立的虚拟环境**（因为依赖关系可能会产生冲突）。
```bash
mkdir -p ~/.crunch/workspace/competitions/<competition>
cd ~/.crunch/workspace/competitions/<competition>
uv venv && source .venv/bin/activate
uv pip install crunch-cli jupyter ipykernel --upgrade --quiet --progress-bar off
python -m ipykernel install --user --name <competition> --display-name "Crunch - <competition>"

# Get token from: https://hub.crunchdao.com/competitions/<competition>/submit
crunch setup <competition> <project-name> --token <TOKEN>
cd <competition>-<project-name>
```

有关竞赛特定所需的包及完整示例，请参阅 [references/competition-setup.md](references/competition-setup.md)。

## 核心工作流程

### 1. 发现
```bash
crunch list                    # List competitions
```
可以通过 GitHub API 获取快速入门工具：
```bash
curl -s "https://api.github.com/repos/crunchdao/competitions/contents/competitions/<name>/quickstarters"
```

### 2. 了解竞赛规则
阅读快速入门工具的代码（`main.py` 或笔记本文件）以及竞赛的 SKILL.md/README.md 文件。提供以下方面的讲解：
- 竞赛目标
- 界面设计
- 数据流
- 解决方案的设计思路
- 评分标准
- 约束条件
- 可改进的地方

### 3. 提出改进方案
分析当前的解决方案，参考竞赛的相关文档（SKILL.md、LITERATURE.md、PACKAGES.md），并提出具体的代码改进建议：
- 模型方面：混合密度模型、NGBoost、分位数回归、集成模型
- 特征方面：市场波动性、资产间的相关性、季节性因素
- 架构方面：在线学习算法、贝叶斯更新机制、针对不同时间范围的模型设计

### 4. 测试解决方案
```bash
crunch test                    # Test solution locally
```

### 5. 提交解决方案
```bash
crunch test                    # Always test first
crunch push -m "Description"   # Submit
```

## 术语对照表

| 用户输入 | 操作建议 |
|-----------|--------|
| “有哪些竞赛可以参加？” | 查看可用竞赛列表（`crunch list`） |
| “显示 <名称> 竞赛的快速入门工具” | 从 GitHub API 获取相关信息 |
| “搭建 <名称> 竞赛所需的工作环境” | 完整配置竞赛环境 |
| “下载数据” | 执行 `crunch download` 命令 |
| “获取 <名称> 的快速入门工具” | 使用 `crunch quickstarter --name` 命令 |
| “解释这个快速入门工具的实现原理” | 提供结构化的代码讲解 |
| “提出改进方案” | 分析现有代码并建议改进 |
| “测试我的解决方案” | 使用 `crunch test` 命令进行测试 |
| “与基准方案进行比较” | 同时运行两个方案并对比结果 |
| “提交我的解决方案” | 使用 `crunch push` 命令提交解决方案 |

## 重要规则

- 解决方案的核心文件必须是 `main.py`（这是 `crunch push` 和 `crunch test` 命令的默认要求）。
- 模型文件应保存在 `resources/` 目录下。
- 严格遵守竞赛的界面规范和约束条件（如时间限制、输出格式等）。
- 在安装新包之前，请先征得许可。

## 参考资料

- 命令行工具使用指南：[references/cli-reference.md](references/cli-reference.md)
- 竞赛环境搭建示例：[references/competition-setup.md](references/competition-setup.md)