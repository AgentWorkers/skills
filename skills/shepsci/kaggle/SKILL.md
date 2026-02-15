---
name: kaggle
description: "**统一Kaggle技能**：  
当用户提到Kaggle（kaggle.com）、Kaggle竞赛、数据集、模型、笔记本（notebooks）、GPU、TPU（Tensor Processing Unit）、徽章（badges）或任何与Kaggle相关的内容时，可使用此技能。该技能涵盖以下功能：  
- 账户设置  
- 竞赛报告生成  
- 数据集/模型下载  
- 笔记本执行  
- 竞赛提交  
- 徽章收集  
- 以及所有与Kaggle相关的一般性问题解答。"
license: MIT
compatibility: "Python 3.9+, pip packages kagglehub, kaggle, requests, python-dotenv. Optional: playwright for browser badges. Playwright MCP tools for competition reports."
homepage: https://github.com/shepsci/kaggle-skill
metadata: {"author": "shepsci", "version": "1.0.1", "primaryEnv": "KAGGLE_KEY", "openclaw": {"requires": {"bins": ["python3", "pip3"], "env": ["KAGGLE_USERNAME", "KAGGLE_KEY", "KAGGLE_API_TOKEN"]}}}
allowed-tools: Bash Read WebFetch
---

# Kaggle — 统一技能

该技能实现了与Kaggle的全面集成，适用于任何大型语言模型（LLM）或代理编码系统（如Claude Code、gemini-cli、Cursor等），包括账户设置、竞赛报告、数据集/模型下载、笔记本执行、竞赛提交、徽章收集以及Kaggle相关操作。整个系统由四个相互协作的模块组成。

> **注意事项：** 对于黑客马拉松的评分评估和对齐分析，请使用**kaggle-hackathon-grading**技能。

**网络要求：** 需要向`api.kaggle.com`、`www.kaggle.com`和`storage.googleapis.com`发送HTTPS请求。

## 模块说明

| 模块 | 功能 |
|--------|---------|
| **registration** | 账户创建、API密钥生成、凭证存储 |
| **comp-report** | 使用Playwright抓取工具生成竞赛概览报告 |
| **kllm** | 提供与Kaggle的核心交互功能（包括kagglehub、CLI、MCP和UI） |
| **badge-collector** | 通过五个阶段系统化地获取Kaggle徽章 |

## 凭证设置

**务必先运行凭证检查工具：**

```bash
python3 skills/kaggle/shared/check_all_credentials.py
```

为了实现完整的功能，需要以下三种凭证：

| 变量 | 格式 | 用途 |
|----------|--------|---------|
| `KAGGLE_USERNAME` | Kaggle用户名 | 所有工具的识别凭证 |
| `KAGGLE_KEY` | 32位十六进制字符串 | 旧版API（CLI、kagglehub、大部分MCP）所需的密钥 |
| `KAGGLE_API_TOKEN` | 以`KGAT_`开头的字符串 | 部分MCP端点所需的权限令牌 |

如果缺少任何凭证，请参考`modules/registration/README.md`中的逐步指南进行设置。

**安全提示：** **切勿** 将凭证值显示在控制台或日志中，也**切勿** 将其提交到代码仓库。

## 模块：Registration（账户注册）

该模块指导用户创建Kaggle账户并生成所需的三种API凭证。凭证信息会保存在`.env`文件和`~/.kaggle/kaggle.json`中。

**关键命令：**
```bash
python3 skills/kaggle/modules/registration/scripts/check_registration.py
bash skills/kaggle/modules/registration/scripts/setup_env.sh
```

详细步骤请参阅`modules/registration/README.md`。

## 模块：Competition Reports（竞赛报告）

该模块生成Kaggle近期竞赛活动的全面报告。使用Python API获取元数据，并通过Playwright工具生成用户界面（SPA）所需的内容。

**六步工作流程：**
1. 验证凭证
2. 获取所有竞赛的列表
3. 获取每项竞赛的详细信息（文件、排行榜、代码内核）
4. 使用Playwright抓取竞赛问题描述、评估指标和报告内容
5. 生成包含方法分析和见解的Markdown报告
6. 在用户界面中展示报告内容

```bash
python3 skills/kaggle/modules/comp-report/scripts/list_competitions.py --lookback-days 30 --output json
python3 skills/kaggle/modules/comp-report/scripts/competition_details.py --slug SLUG
```

详细信息请参阅`modules/comp-report/README.md`，其中包含针对黑客马拉松的特殊处理方式。

## 模块：Kaggle Interaction (kllm)

提供了四种与kaggle.com交互的方式：

| 方法 | 适用场景 |
|--------|----------|
| **kagglehub** | 用Python快速下载数据集/模型 |
| **kaggle-cli** | 完整的工作流程脚本编写 |
| **MCP Server** | 用于AI代理的集成 |
| **Kaggle UI** | 账户设置和验证 |

**功能对比表：**

| 功能 | kagglehub | kaggle-cli | MCP | UI |
|------|-----------|------------|-----|-----|
| 下载数据集 | `dataset_download()` | `datasets download` | 是 | 是 |
| 下载模型 | `model_download()` | `models instances versions download` | 是 | 是 |
| 执行笔记本 | — | `kernels push/status/output` | 是 | 是 |
| 提交竞赛 | — | `competitions submit` | 是 | 是 |
| 发布数据集 | `dataset_upload()` | `datasets create` | 是 | 是 |
| 发布模型 | `model_upload()` | `models create` | 是 | 是 |

**已知问题：**
- 在kagglehub v0.4.3版本中，`dataset_load()`功能失效——请使用`dataset_download()`结合`pd.read_csv()` |
- 自1.8版本起，`competitions download`命令的`--unzip`参数不再可用 |
- 通过竞赛链接下载的数据集可能会返回403错误——请使用独立的数据集副本

详细信息和完整的工作流程请参阅`modules/kllm/README.md`。

## 模块：Badge Collector（徽章收集）

通过五个阶段系统化地获取Kaggle徽章：

| 阶段 | 名称 | 徽章类型 | 需要时间 |
|-------|------|--------|------|
| 1 | 即时API请求 | 约16个徽章 | 5-10分钟 |
| 2 | 参加竞赛 | 约7个徽章 | 10-15分钟 |
| 3 | 使用管道处理 | 约3个徽章 | 15-30分钟 |
| 4 | 浏览器操作 | 约8个徽章 | 5-10分钟 |
| 5 | 连续完成任务 | 约4个徽章 | 仅需设置 |

**更多详细信息请参阅**`modules/badge-collector/README.md`。

## 整合工作流程

该技能主要作为**参考**使用——根据用户的需求选择相应的模块和脚本。当用户明确要求执行**完整的Kaggle工作流程**时，请按照以下步骤操作：

### 第一步：检查凭证

```bash
python3 skills/kaggle/shared/check_all_credentials.py
```

如果缺少任何凭证，请重新执行账户注册流程。**切勿** 将凭证值显示在控制台或日志中。

### 第二步：生成竞赛概览报告

运行`comp-report`模块，列出所有竞赛、获取详细信息，并使用Playwright抓取数据，然后生成报告。报告内容会在用户界面中直接显示。

### 第三步：总结Kaggle交互方式

向用户展示四种与Kaggle交互的方式（kagglehub、kaggle-cli、MCP Server、UI），并附上`kllm`模块提供的功能对比表。

### 第四步：提供交互式菜单

询问用户下一步想做什么：
- **获取Kaggle徽章**——运行徽章收集脚本（共五个阶段，可自动获取约38个徽章）
- **探索近期竞赛**——深入查看报告中的具体竞赛
- **参加Kaggle竞赛**——注册账户、下载数据、构建提交内容并提交
- **下载Kaggle数据集**——搜索并下载任何公开的数据集
- **下载Kaggle模型**——下载预训练的模型（如LLM、CV模型等）
- **在Kaggle上运行笔记本**——在Kaggle Kernel Backend（KKB）上运行笔记本（支持免费GPU/TPU）
- **在Kaggle上发布内容**——上传数据集、模型或笔记本
- **了解Kaggle的等级体系**——了解等级、奖牌以及提升等级的方法
- **其他操作**——提供其他相关的Kaggle帮助

### 第五步：执行用户选择的内容

根据用户的选择使用相应的模块，并循环提供更多选项。

## 安全注意事项

- **切勿** 将`.env`、`kaggle.json`或任何凭证文件提交到代码仓库
- **切勿** 在终端输出中显示或记录凭证值
- `.gitignore`文件会排除`.env`、`kaggle.json`及相关文件
- 设置文件权限：`chmod 600 .env ~/.kaggle/kaggle.json`
- 如果凭证信息意外泄露，请立即在[https://www.kaggle.com/settings](https://www.kaggle.com/settings)更新凭证信息

## 操作范围

该技能支持在kaggle.com上进行读写操作：

**读写操作：**
- 列出/搜索竞赛、数据集、模型、笔记本
- 下载数据集、模型、竞赛数据
- 查看排行榜、竞赛详情和徽章获取进度
- 生成竞赛概览报告

**写操作：**
- 在用户账户上创建或修改资源：
  - 创建/发布数据集、笔记本、模型（默认为私密状态）
- 向竞赛提交预测结果
- 在Kaggle Kernel Backend（KKB）上运行和执行笔记本
- 通过API操作获取徽章（徽章会显示在用户个人资料中）

**第五阶段（连续完成任务）**会生成一个用于每日自动执行的本地Shell脚本，但**不会**自动设置定时任务或启动服务。用户如需自动执行，需自行配置调度。

## 脚本索引

**通用脚本：**
- `shared/check_all_credentials.py` — 统一的凭证检查工具（支持三种凭证类型）

**账户注册相关脚本：**
- `modules/registration/scripts/check_registration.py` — 检查所有三种凭证
- `modules/registration/scripts/setup_env.sh` — 从环境变量文件自动配置凭证

**竞赛报告相关脚本：**
- `modules/comp-report/scripts/utils.py` — 凭证检查、API初始化、速率限制
- `modules/comp-report/scripts/list_competitions.py` — 获取所有类别的竞赛列表
- `modules/comp-report/scripts/competition_details.py` — 获取每项竞赛的文件、排行榜和代码内核信息

**Kaggle交互相关脚本：**
- `modules/kllm/scripts/setup_env.sh` — 使用`.env`文件自动配置凭证
- `modules/kllm/scripts/check_credentials.py` — 验证并自动映射凭证
- `modules/kllm/scripts/network_check.sh` — 检查Kaggle API的可用性
- `modules/kllm/scripts/cli_download.sh` — 通过CLI下载数据集/模型
- `modules/kllm/scripts/cli_execute.sh` — 在KKB上运行笔记本
- `modules/kllm/scripts/cli_competition.sh` — 竞赛相关操作（列表/下载/提交）
- `modules/kllm/scripts/cli_publish.sh` — 发布数据集/笔记本/模型
- `modules/kllm/scripts/poll_kernel.sh` — 查询代码内核状态并下载结果
- `modules/kllm/scripts/kagglehub_download.py` — 通过kagglehub下载资源
- `modules/kllm/scripts/kagglehub_publish.py` — 通过kagglehub发布资源

**徽章收集相关脚本：**
- `modules/badge-collector/scripts/orchestrator.py** — 主入口脚本
- `modules/badge-collector/scripts/badgeRegistry.py` — 定义59种徽章
- `modules/badge-collector/scripts/badge_tracker.py** — 记录徽章获取进度
- `modules/badge-collector/scripts/utils.py` — 公共辅助脚本
- `modules/badge-collector/scripts/phase_1_instant_api.py` — 通过即时API获取徽章
- `modules/badge-collector/scripts/phase_2_competition.py` — 通过竞赛获取徽章
- `modules/badge-collector/scripts/phase_3_pipeline.py` — 通过管道处理获取徽章
- `modules/badge-collector/scripts/phase_4_browser.py` — 通过浏览器操作获取徽章
- `modules/badge-collector/scripts/phase_5_streaks.py` — 自动完成连续任务相关的徽章获取

## 参考资料索引

- `modules/registration/references/kaggle-setup.md` — 完整的凭证设置指南及故障排除方法
- `modules/comp-report/references/competition-categories.md` — 竞赛类型及API映射信息
- `modules/kllm/references/kaggle-knowledge.md** — 关于Kaggle平台的全面信息
- `modules/kllm/references/kagglehub-reference.md` — kagglehub Python API的完整参考文档
- `modules/kllm/references/cli-reference.md` — kaggle-cli命令的完整参考手册
- `modules/kllm/references/mcp-reference.md` — Kaggle MCP服务器的参考资料
- `modules/badge-collector/references/badge-catalog.md** — 完整的徽章目录