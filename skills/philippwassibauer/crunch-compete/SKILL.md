---
name: crunch-compete
description: >
  **使用说明：**  
  适用于参与Crunch竞赛时使用——包括设置工作空间、查看快速入门指南、在本地测试解决方案以及提交参赛作品等操作。
---
# Cruncher 技能

本技能指导用户完成 Crunch 竞赛的整个流程：包括环境搭建、快速入门指南的获取、解决方案的开发、本地测试以及解决方案的提交。

## 先决条件
- Python 3.9 及以上版本，并安装了 `venv` 模块（Python 标准库中包含）
- 安装 `pip` 用于包管理

## 包安装

本技能负责从 [PyPI](https://pypi.org) 安装 Python 包到隔离的虚拟环境中：

| 包名 | 来源 | 用途 |
|---------|--------|---------|
| `crunch-cli` | [PyPI](https://pypi.org/project/crunch-cli/) | CrunchDAO 竞赛所需的命令行工具（用于环境搭建、测试和提交） |
| `jupyter` | [PyPI](https://pypi.org/project/jupyter/) | 支持使用 Jupyter 笔记本（可选） |
| `ipykernel` | [PyPI](https://pypi.org/project/ipykernel/) | 注册 Jupyter 核心（可选） |
| 竞赛专用库（如 `crunch-synth`、`birdgame`） | 来自 PyPI | 根据比赛需求安装的不同库 |

**包安装规则：**
- **必须使用虚拟环境**，切勿将包安装到系统 Python 环境中 |
- **仅安装上述列出的包或竞赛文档（PACKAGES.md）中推荐的包** |
- 在安装任何未列出的包之前，必须先征得用户同意 |
- 所有包均来自 PyPI，禁止使用自定义 URL、`--index-url` 参数，以及来自未知来源的 `.whl` 文件

## 凭据

### 提交令牌（设置和提交必需）

- **获取方式：** 用户登录 [CrunchDAO Hub](https://hub.crunchdao.com)，进入比赛的提交页面（`/competitions/<competition>/submit`），然后复制他们的令牌 |
- **使用方式：** 在执行 `crunch setup` 命令时，通过 `--token <TOKEN>` 参数传递令牌 |
- **令牌存储：** 设置完成后，命令行工具会将令牌保存在项目的 `.crunch/` 配置目录中。后续的所有命令（`crunch test`、`crunch push`、`crunch download`）都会自动使用该令牌进行身份验证，无需再次输入 |
- **令牌过期处理：** 在项目目录中运行 `crunch update-token` 命令即可刷新令牌 |

**令牌使用规则：**
- **必须始终要求用户提供令牌**，严禁猜测或重复使用其他项目的令牌 |
- **严禁将令牌写入源代码文件、脚本、笔记本或任何已提交的文件中** |
- **禁止在 shell 输出中显示令牌内容**（示例中应使用 `--token <TOKEN>` 占位符） |
- 令牌是用户专属的，并且仅适用于当前项目；每次执行 `crunch setup` 需要用户重新提供令牌 |

### GitHub API（可选，无需认证）

- 仅用于通过 `api.github.com` 浏览快速入门指南列表（公共仓库，无需认证）
- 每个 IP 地址每小时请求次数有限制（60 次），足以满足正常使用需求

## 网络访问

| 操作 | 是否需要网络连接 | 接口地址 |
|-----------|-----------------|----------|
| `crunch setup` | 是 | `hub.crunchdao.com` |
| `crunch push` | 是 | `hub.crunchdao.com` |
| `crunch download` | 是 | `hub.crunchdao.com` |
| `crunch test` | **不需要** | 仅在本地执行 |
| `crunch list` | 是 | `hub.crunchdao.com` |
| `pip install` | 是 | `pypi.org` |
| 快速入门指南浏览 | 是 | `api.github.com` |

## 快速搭建

**每个比赛都需要独立的虚拟环境**（因为依赖关系可能相互冲突）。

```bash
mkdir -p ~/.crunch/workspace/competitions/<competition>
cd ~/.crunch/workspace/competitions/<competition>
python -m venv .venv && source .venv/bin/activate 
pip install crunch-cli jupyter ipykernel --upgrade --quiet --progress-bar=off
python -m ipykernel install --user --name <competition> --display-name "Crunch - <competition>"

# Get token from: https://hub.crunchdao.com/competitions/<competition>/submit
crunch setup <competition> <project-name> --token <TOKEN>
cd <competition>-<project-name>
```

有关比赛专用包和完整示例，请参阅 [references/competition-setup.md](references/competition-setup.md)。

## 核心工作流程

### 1. 了解比赛要求
```bash
crunch list                    # List competitions
```

### 2. 解读比赛规则
阅读快速入门指南中的代码（`main.py` 或 Jupyter 笔记本）以及比赛的 SKILL.md/README.md 文件。为用户提供以下方面的讲解：比赛目标、用户界面、数据流程、解决方法、评分标准、限制条件以及改进方案。

### 3. 提出改进方案
分析当前的技术方案，参考比赛文档（SKILL.md、LITERATURE.md、PACKAGES.md），并提出具体的代码改进建议：
- 模型选择：混合密度模型、NGBoost、分位数回归、集成模型
- 特征分析：市场波动性、资产间的相关性、季节性因素
- 架构设计：在线学习算法、贝叶斯更新机制、针对不同时间范围的模型

### 4. 进行测试
```bash
crunch test                    # Test solution locally
```

### 5. 提交解决方案
```bash
crunch test                    # Always test first
crunch push -m "Description"   # Submit
```

## 常用命令映射

| 用户指令 | 对应操作 |
|-----------|--------|
| `显示可参加的比赛` | `crunch list` |
| 查看 <比赛名称> 的快速入门指南` | 从 GitHub API 获取相关信息 |
| 设置 <比赛名称> 的开发环境` | 完整搭建开发环境 |
| 下载数据` | `crunch download` |
| 获取 <比赛名称> 的快速入门示例` | `crunch quickstarter --name` |
| 解释这个快速入门指南` | 提供代码实现的详细讲解 |
| 提出改进方案` | 分析并建议代码优化 |
| 测试我的解决方案` | `crunch test` |
| 与基准方案进行对比` | 同时运行两个方案并对比结果 |
| 提交我的解决方案` | `crunch push` |

## 重要规则
- 必须使用 `main.py` 作为入口文件（`crunch push`/`crunch test` 的默认要求） |
- 模型文件应保存在 `resources/` 目录中 |
- 遵守比赛的接口规范和限制条件（如时间限制、输出格式要求） |
- 在安装新包之前，请务必先征得用户同意

## 参考资料
- 命令行工具使用指南：[references/cli-reference.md](references/cli-reference.md)
- 环境搭建示例：[references/competition-setup.md](references/competition-setup.md)