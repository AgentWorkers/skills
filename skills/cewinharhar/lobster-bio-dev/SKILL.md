---
name: lobster-dev
description: |
  Develop, extend, and contribute to Lobster AI — the multi-agent bioinformatics engine.
  Use when working on Lobster codebase, creating agents/services, understanding architecture,
  fixing bugs, adding features, or contributing to the open-source project.
  
  Trigger phrases: "add agent", "create service", "extend lobster", "contribute",
  "understand architecture", "how does X work in lobster", "fix bug", "add feature",
  "write tests", "lobster development", "agent development", "bioinformatics code"
---

# Lobster AI 开发指南

**Lobster AI** 是一个基于 LangGraph 的多智能体生物信息学平台，用于任务的协调与执行。本文档将指导您如何使用、扩展以及为该平台的代码库做出贡献。

## 快速导航

| 任务 | 文档链接 |
|------|---------------|
| **架构概述** | [references/architecture.md](references/architecture.md) |
| **创建新智能体** | [references/creating-agents.md](references/creating-agents.md) |
| **创建新服务** | [references/creating-services.md](references/creating-services.md) |
| **代码布局与文件查找** | [references/code-layout.md](references/code-layout.md) |
| **测试模式** | [references/testing.md](references/testing.md) |
| **命令行接口（CLI）参考** | [references/cli.md](references/cli.md) |

## 重要规则

1. **ComponentRegistry 是核心** — 智能体的注册是通过入口点（entry points）完成的，而非硬编码的。
2. **AGENT_CONFIG 必须位于模块顶部** — 在进行大量导入操作之前定义该配置文件，以确保智能体能够快速被发现（时间小于 50 毫秒）。
3. **所有服务都必须返回一个三元素元组** — 形式为 `(AnnData, Dict, AnalysisStep)`。
4. **始终传递 `ir` 参数** — 使用 `log_tool_usage(..., ir=ir)` 以确保测试结果的可重复性。
5. **禁止使用 `lobster/__init__.py` 文件** — 遵循 PEP 420 规范，避免使用带有 `__init__` 方法的包。

## 包结构

```
lobster/
├── packages/                    # Agent packages (PEP 420)
│   ├── lobster-transcriptomics/ # transcriptomics_expert, annotation_expert, de_analysis_expert
│   ├── lobster-research/        # research_agent, data_expert_agent
│   ├── lobster-visualization/   # visualization_expert
│   ├── lobster-metadata/        # metadata_assistant
│   ├── lobster-structural-viz/  # protein_structure_visualization_expert
│   ├── lobster-genomics/        # genomics_expert
│   ├── lobster-proteomics/      # proteomics_expert
│   └── lobster-ml/              # machine_learning_expert
└── lobster/                     # Core SDK
    ├── agents/supervisor.py     # Supervisor (stays in core)
    ├── agents/graph.py          # LangGraph builder
    ├── core/                    # Infrastructure (registry, data_manager, provenance)
    ├── services/                # Analysis services
    └── tools/                   # Agent tools
```

## 常用命令

```bash
# Setup (development)
make dev-install              # Full dev setup with editable install
make test                     # Run all tests
make format                   # black + isort

# Setup (end-user testing via uv tool)
uv tool install 'lobster-ai[full,anthropic]'   # Install as users see it
uv tool upgrade lobster-ai                      # Upgrade to latest

# Running
lobster chat                  # Interactive mode
lobster query "your request"  # Single-turn

# Testing
pytest tests/unit/            # Fast unit tests
pytest tests/integration/     # Integration tests
```

## 服务模式（必备）

所有服务都必须返回一个三元素元组：

```python
def analyze(self, adata, **params) -> Tuple[AnnData, Dict, AnalysisStep]:
    # Your analysis logic
    stats = {"n_cells": adata.n_obs, "status": "complete"}
    ir = AnalysisStep(
        activity_type="analyze",
        inputs={"n_obs": adata.n_obs},
        outputs=stats,
        params=params
    )
    return processed_adata, stats, ir
```

**工具用于封装服务功能：**

```python
@tool
def analyze_modality(modality_name: str, **params) -> str:
    result, stats, ir = service.analyze(adata, **params)
    data_manager.log_tool_usage("analyze", params, stats, ir=ir)  # IR mandatory!
    return f"Complete: {stats}"
```

## 智能体注册（入口点）

智能体通过 `pyproject.toml` 文件进行注册：

```toml
[project.entry-points."lobster.agents"]
my_agent = "lobster.agents.my_domain.my_agent:AGENT_CONFIG"
```

**注意：** `AGENT_CONFIG` 必须在模块顶部（导入语句之前）被定义。

```python
# lobster/agents/mydomain/my_agent.py
from lobster.config.agent_registry import AgentRegistryConfig

AGENT_CONFIG = AgentRegistryConfig(
    name="my_agent",
    display_name="My Expert Agent",
    description="What this agent does",
    factory_function="lobster.agents.mydomain.my_agent.my_agent",
    handoff_tool_name="handoff_to_my_agent",
    handoff_tool_description="Assign tasks for my domain analysis",
    tier_requirement="free",  # All official agents are free
)

# Heavy imports AFTER config
from lobster.core.data_manager_v2 import DataManagerV2
# ... rest of implementation
```

## 关键文件

| 文件 | 功能 |
|------|---------|
| `lobster/agents/graph.py` | 使用 LangGraph 进行任务协调 |
| `lobster/core/component_registry.py` | 负责智能体的发现与管理 |
| `lobster/core/data_manager_v2.py` | 数据与工作区管理 |
| `lobster/core/provenance.py` | 实现 W3C-PROV 标准的版本追踪功能 |
| `lobster/cli.py` | 提供命令行接口（CLI） |

## 在线文档

完整文档请访问 **docs.omics-os.com**（或本地 `docs-site/`）：

- **入门指南**：`docs/getting-started/`
- **核心 SDK**：`docs/core/`
- **智能体相关文档**：`docs/agents/`
- **开发者指南**：`docs/developer/`
- **API 参考**：`docs/api-reference/`

## 常见任务

### 添加新智能体

1. 创建一个新的包：`packages/lobster-mydomain/`
2. 在智能体对应的文件顶部定义 `AGENT_CONFIG`。
3. 在 `pyproject.toml` 中注册该智能体的入口点。
4. 使用相关工具实现智能体的功能。
5. 在 `tests/unit/agents/` 目录下编写测试用例。

详细步骤请参阅 [references/creating-agents.md](references/creating-agents.md)。

### 添加新服务

1. 在相应的包中创建服务类。
2. 实现服务功能，并确保返回一个三元素元组。
3. 使用 `log_tool_usage` 对服务功能进行封装。
4. 为服务编写单元测试。

详细步骤请参阅 [references/creating-services.md](references/creating-services.md)。

### 理解数据流

```
User Query → CLI → LobsterClientAdapter → AgentClient
                                              ↓
                            LangGraph (supervisor → agents)
                                              ↓
                               Services → DataManagerV2
                                              ↓
                                    Results + Provenance
```

## 测试

```bash
# Unit tests (fast, no external deps)
pytest tests/unit/ -v

# Integration tests (may need env vars)
pytest tests/integration/ -v

# Specific test
pytest tests/unit/test_my_feature.py -v

# With coverage
pytest --cov=lobster tests/
```

## 贡献代码

1. 克隆代码仓库：`git checkout -b feature/my-feature`
2. 根据上述规则进行代码修改。
3. 运行测试：`make test`
4. 格式化代码：`make format`
5. 提交带有清晰说明的 Pull Request（PR）。