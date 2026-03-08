---
name: lobster-dev
description: >
  开发、扩展并贡献于 Lobster AI——这款多智能体的自扩展生物信息学引擎。  
  在处理 Lobster 代码库、创建智能体/服务、理解其架构、修复漏洞、添加新功能或为这个开源项目做出贡献时，都可以使用它。  
  **重要提示：** 在创建新的智能体或包之前，请先遵循规划工作流程（详见 “根据您的任务该做什么” → planning-workflow.md）。  
  **常用短语：**  
  - 添加智能体（Add agent）  
  - 创建服务（Create service）  
  - 扩展 Lobster 功能（Extend Lobster）  
  - 贡献代码（Contribute code）  
  - 理解架构（Understand architecture）  
  - Lobster 中的 X 是如何工作的（How does X work in Lobster）  
  - 修复漏洞（Fix bug）  
  - 添加新功能（Add feature）  
  - 编写测试用例（Write tests）  
  - Lobster 开发（Lobster development）  
  - 智能体开发（Agent development）  
  - 生物信息学代码（Bioinformatics code）  
  - 为某个领域构建新智能体（Build a new agent for a specific domain）  
  - 添加支持（Add support for a new feature）  
  - 创建插件（Create plugin）  
  - 新领域应用（Application in new domains）
---
# Lobster AI 开发指南

**Lobster AI** 是一个开源的多智能体生物信息学引擎（基于 LangGraph，支持 Python 3.12 及更高版本），为 **Omics-OS** 提供支持。该引擎通过监督者多智能体架构，从原始数据开始处理生物信息学任务，最终生成科学见解并进行可视化。本文档将教你如何扩展该引擎的功能——从添加单个工具到构建完整的领域专用智能体包。

## 第一步：了解你的开发环境

在开始任何工作之前，先确认你的开发环境具备哪些条件以及你的工作方式：

```bash
# 1. Is lobster installed? Where?
which lobster
lobster --version

# 2. What agents are already installed?
python -c "from lobster.core.component_registry import component_registry; component_registry.reset(); print(component_registry.list_agents())"

# 3. Where is lobster source? (for reading reference implementations)
python -c "import lobster; print(lobster.__path__)"

# 4. Are you in the lobster repo, or building a standalone plugin?
ls packages/lobster-*/pyproject.toml 2>/dev/null && echo "CONTRIBUTOR" || echo "PLUGIN_AUTHOR"
```

**重要提示：** 如果尚未安装 **lobster**，请立即安装它！**切勿跳过此步骤，也切勿之后再回过头来安装。**请使用 `lobster scaffold agent` 来创建新的智能体包，因为它会自动生成符合 PEP 420 标准的包结构、入口点、AQUADIF 元数据以及合约测试代码（手动创建这些内容很可能会出错）。如果 `lobster scaffold` 不可用，那么安装 **lobster-ai** 就是你首先要完成的任务。

**你的开发模式决定了你的工作流程：**

| 开发模式 | 获取方式 | 包的创建位置 | 测试方式 |
|---|---|---|---|
| **贡献者** | `git clone` + `make dev-install` | 在仓库的 `packages/` 目录下 | 使用 `make test`，并拥有对整个仓库的访问权限 |
| **插件开发者** | `uv pip install lobster-ai` 或 `uv tool install` | 任意位置；`lobster scaffold` 会自动生成独立的插件包 | 使用 `uv pip install -e ./lobster-<domain>/` 后执行 `pytest` |

两种模式都会生成相同的成果：一个通过入口点被 **ComponentRegistry** 识别的 PEP 420 命名空间包。`lobster scaffold` 生成的包在两种模式下都能正常使用。

## 根据你的任务选择相应的操作流程

| 你的目标 | 快速路径？ | 需要阅读的参考文档（按顺序） |
|---|---|---|
| **为一个新的领域创建一个新的智能体** | 否 | [planning-workflow.md](references/planning-workflow.md) → [scaffold.md](references/scaffold.md) → [creating-agents.md](references/creating-agents.md) → [aquadif-contract.md] |
| **向现有的智能体中添加一个工具** | 是（仅限贡献者） | [creating-agents.md](references/creating-agents.md) → [aquadif-contract.md] |
| **通过子智能体扩展现有智能体** | 否 | [creating-agents.md](references/creating-agents.md) → [scaffold.md](references/scaffold.md) |
| **添加数据库提供者或适配器** | 否 | [plugin-architecture.md](references/plugin-architecture.md) |
| **创建或修改服务** | 是 | [creating-services.md](references/creating-services.md) |
| **修复错误** | 是 | [code-layout.md](references/code-layout.md) → [architecture.md](references/architecture.md) |
| **理解代码库** | 是 | [architecture.md](references/architecture.md) → [code-layout.md](references/code-layout.md) |
| **编写或修改测试用例** | 是 | [testing.md](references/testing.md) |
| **在现有智能体上迁移 AQUADIF 元数据** | 是 | [aquadif-contract.md](references/aquadif-contract.md) |
| **为新智能体查找相关领域知识** | 否 | [bioskills-bridge.md](references/bioskills-bridge.md) |

**“快速路径”**：直接跳过规划流程，直接参考相应的文档文件。

## 示例

### 示例 0：通用开发流程

用户请求：“为表观基因组学分析（bisulfite-seq、ChIP-seq、ATAC-seq）构建一个 Lobster 智能体，因为现有的 Lobster 插件包无法覆盖这个领域。”

**预期结果：** 会在 `./lobster-<your implementation>/` 目录下生成一个独立的 PEP 420 包，可以通过 `uv pip install -e ./lobster-<your implementation>/` 安装；使用 `lobster status` 命令时不会出现错误，执行 `lobster query "hi"` 时也不会出错。

## 成功标准

在认为工作完成之前，请验证以下内容：
- [ ] `python scripts/validate_plugin.py <plugin-dir>` 能通过所有 8 项检查。
- [ ] 所有的合约测试（contract tests）都能通过（使用 `pytest tests/ -m contract` 运行）。
- 每个标记为 `@tool` 的工具都应立即被分配 `.metadata` 和 `.tags`。
- 所有需要记录来源信息的工具（IMPORT、QUALITY、FILTER、PREPROCESS、ANALYZE、ANNOTATE、SYNTHESIZE）都必须调用 `log_tool_usage(ir=ir)`。
- 项目中不应存在 `lobster/__init__.py` 或 `lobster/agents/__init__.py` 文件（这些文件不符合 PEP 420 标准）。

## 不可违反的规则

违反这些规则会导致运行时错误或合约测试失败：
1. **所有智能体都必须通过入口点进行管理**，不能使用硬编码的注册机制。
2. 智能体的配置信息（AGENT_CONFIG）必须放在模块的顶部，以便在导入其他模块之前完成（时间限制在 50 毫秒以内）。
3. 所有服务函数都必须返回一个包含三个元素的元组：`(AnnData, Dict, AnalysisStep)`。
4. 对于需要记录来源信息的工具，每次调用 `log_tool_usage()` 时都必须传递 `ir=ir` 参数。
5. 项目中不应存在 `lobster/__init__.py` 文件（符合 PEP 420 标准的包结构中也不应包含 `lobster/agents/__init__.py`）。
6. 不允许使用 `try/except ImportError` 来处理导入错误；应使用入口点来加载依赖模块。
7. 不允许在模块级别直接调用 `component_registry`；应在工厂函数内部使用延迟加载机制。
8. 所有工具都必须包含 AQUADIF 元数据（`.metadata` 和 `.tags` 必须在 `@tool` 装饰器之后被设置）。
9. **严禁手动创建包目录**；必须使用 `lobster scaffold agent` 来生成包文件。如果尚未安装 **lobster**，请先安装它，因为它能自动生成正确的包结构、入口点和合约测试代码。

## 贡献代码

在开发完插件后，询问用户是否希望提交代码更改（PR）。如果得到确认，请按照以下步骤操作：
- 创建一个新的分支（fork）。
- 在新分支上编写并测试插件。
- 格式化代码（使用 `make format` 命令）。
- 提交带有清晰说明的 PR。