---
name: crunch-compete
description: >
  **使用说明：**  
  适用于参与Crunch竞赛时，用于设置工作区、查看快速入门指南、在本地测试解决方案或提交参赛作品。
---
# Cruncher 技能

本文档指导用户完成 Crunch 竞赛的整个生命周期：包括环境搭建、快速入门示例的学习、解决方案的开发、本地测试以及解决方案的提交。假设用户已经配置好了机器学习工程师所需的本地开发环境。

## 快速搭建

**每个竞赛都需要独立的虚拟环境**（因为不同竞赛可能依赖不同的库，这些依赖可能会产生冲突）。

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

有关特定竞赛所需的包及完整示例，请参阅 [references/competition-setup.md](references/competition-setup.md)。

## 核心工作流程

### 1. 了解竞赛要求
```bash
crunch list                    # List competitions
```

### 2. 学习快速入门示例
阅读快速入门代码（`main.py` 或笔记本文件）以及竞赛相关的 SKILL.md/README.md 文件。了解竞赛的目标、接口、数据流程、解决方法、评分标准、约束条件以及可改进的地方。

### 3. 提出改进方案
分析当前的处理方法，参考竞赛文档（SKILL.md、LITERATURE.md、PACKAGES.md），并提出具体的代码改进建议：
- 模型方面：混合密度模型、NGBoost、分位数回归、集成学习方法
- 特征方面：波动性特征、跨资产相关性、季节性因素
- 架构方面：在线学习算法、贝叶斯更新机制、针对不同时间范围的模型设计

### 4. 进行测试
```bash
crunch test                    # Test solution locally
```

### 5. 提交解决方案
```bash
crunch test                    # Always test first
crunch push -m "Description"   # Submit
```

## 术语对照表

| 用户输入 | 操作指令 |
|-----------|--------|
| `有哪些竞赛可以参加？` | `crunch list` |
| `显示 <名称> 竞赛的快速入门示例` | 从 GitHub API 获取相关资源 |
| `搭建 <名称> 竞赛所需的工作环境` | 完整配置竞赛所需的工作空间 |
| `下载数据` | `crunch download` |
| `获取 <名称> 的快速入门示例` | `crunch quickstarter --name` |
| `解释这个快速入门示例的实现方式` | 提供结构化的代码讲解 |
| `提出改进方案` | 分析现有代码并建议改进 |
| `测试我的解决方案` | `crunch test` |
| `与基准方案进行比较` | 同时运行两种方案并对比结果 |
| `提交我的解决方案` | `crunch push` |

## 重要规则

- 必须使用 `main.py` 作为解决方案的入口文件（`crunch push`/`crunch test` 命令的默认要求）；
- 模型文件应保存在 `resources/` 目录下；
- 遵守竞赛规定的接口要求和约束条件（如时间限制、输出格式等）；
- 在安装新包之前请先咨询相关工作人员。

## 参考资料

- 命令行工具使用指南：[references/cli-reference.md](references/cli-reference.md)
- 竞赛环境搭建示例：[references/competition-setup.md](references/competition-setup.md)