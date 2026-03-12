---
name: governed-agents
description: "针对AI子代理的确定性验证与声誉评分机制：通过4个代码检查环节（文件检查、测试、代码风格检查、抽象语法树分析）以及一个三层处理流程（结构分析 → 实际效果验证 → LLM委员会评估），有效防止虚假的成功结果。该流程适用于开放式任务。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🛡️",
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "script",
              "kind": "script",
              "command": "bash install.sh",
              "label": "Install governed-agents (copy to workspace)",
            },
          ],
      },
  }
---
# 受监管的智能体（Governed Agents）

针对AI子智能体，采用确定性验证（Deterministic Verification）和声誉评分（Reputation Scoring）机制。通过在更新智能体评分之前独立验证其成果，防止其虚假宣称“任务已完成”。

**仅使用Python标准库，无任何外部依赖。**

## 使用场景

当您需要以下功能时，请使用此技能：
- **生成子智能体**并自动验证其输出；
- **根据任务表现评估智能体的可靠性**（基于EMA的声誉系统）；
- **检测虚假的成功声明**——智能体声称任务已完成，但实际上文件缺失或测试失败；
- **通过LLM Council验证开放式任务（如研究、分析、策略制定）；
- **根据智能体的过往表现设定不同的监管级别**。

## 快速入门

### 确定性验证（Deterministic Verification）

```python
from governed_agents.contract import TaskContract
from governed_agents.orchestrator import GovernedOrchestrator

contract = TaskContract(
    objective="Add JWT auth endpoint",
    acceptance_criteria=["POST /api/auth returns JWT", "Tests pass"],
    required_files=["api/auth.py", "tests/test_auth.py"],
    run_tests="pytest tests/test_auth.py -v",
)

g = GovernedOrchestrator(contract, model="openai/gpt-5.2-codex")
# After agent completes:
result = g.record_success()  # runs gates, updates reputation
```

### 开放式任务（三层验证流程 + LLM Council）

```python
contract = TaskContract(
    objective="Write architecture decision record for auth module",
    acceptance_criteria=["Trade-offs documented", "Decision stated"],
    verification_mode="council",
    task_type="analysis",
    council_size=3,
)

g = GovernedOrchestrator(contract, model="openai/gpt-5.2-codex")
prompts = g.generate_council_tasks(worker_output)
result = g.record_council_verdict(raw_reviewer_outputs)
# → "Council: 2/3 approved (score=0.67, PASS ✅)"
```

### 通过CLI生成子智能体（使用Codex/OpenClaw）

```python
from governed_agents.openclaw_wrapper import spawn_governed

contract = TaskContract(
    objective="Build a REST API for todos",
    acceptance_criteria=["CRUD endpoints work", "Tests pass"],
    required_files=["api.py", "tests/test_api.py"],
)

# Uses Codex 5.3 CLI by default
result = spawn_governed(contract, engine="codex53")
# Or via OpenClaw agent CLI:
result = spawn_governed(contract, engine="openclaw")
```

## 验证模式

### 确定性验证（Deterministic Verification）

系统会自动运行4个验证环节，所有环节都必须通过：
| 验证环节 | 需要检查的内容 | 失败后果 |
|--------|----------------|------------|
| **文件检查** | 所需文件存在且非空 | 直接判定失败 |
| **测试执行** | 测试命令返回0（成功） | 直接判定失败 |
| **代码质量检查** | 代码无语法错误 | 直接判定失败 |
| **AST解析** | Python文件能正常解析（无SyntaxError） | 直接判定失败 |

如果智能体声称任务成功，但任何环节未通过 → 评分将被重置为-1.0（视为虚假成功）。

### LLM Council（开放式任务）

采用三层验证流程：
1. **结构验证**（<1秒）：检查文件字数、是否包含必要部分、是否有空白部分；
2. **内容真实性验证**（5–30秒）：检查链接是否可访问、引用是否正确；
3. **LLM评审**（30–120秒）：由多名独立评审员进行投票。

如果第一层验证失败 → 不会触发LLM评审，系统立即给出结果，且不产生额外费用。

## 声誉系统（Reputation System）

```
R(t+1) = (1 − α) · R(t) + α · s(t),   α = 0.3
```

| 评分 | 含义 |
|------|--------|
| +1.0 | 成功验证（首次尝试） |
| +0.7 | 成功验证（重试后） |
| +0.5 | 报告真实情况（无虚假陈述） |
| 0.0 | 尝试过但失败 |
| -1.0 | 虚假成功 |

## 监管级别（Supervision Levels）

| 声誉评分 | 监管级别 | 后果 |
|--------|-----------|------------|
| > 0.8 | 自主运行 | 完全信任 |
| > 0.6 | 标准监管 | 常规监督 |
| > 0.4 | 强化监管 | 需要设置检查点 |
| > 0.2 | 严格监管 | 智能体行为将被Opus模型接管 |
| ≤ 0.2 | 暂停运行 | 任务将被阻止 |

## 任务类型配置（Task-Type Profiles）

预配置的验证环节组合：
| 任务类型 | 第一层验证 | 第二层验证 | 最小字数要求 |
|---------|------------|----------------|----------------|
| `research` | 字数检查、引用列表 | 链接可用性、引用验证 | 200字 |
| `analysis` | 字数检查、必要部分检查 | 数据一致性 | 150字 |
| `strategy` | 必要部分检查、字数检查 | 引用交叉验证 | 100字 |
| `writing` | 字数检查 | — | 50字 |
| `planning` | 必要部分检查、步骤完整性 | 日期有效性 | 50字 |

## 安装说明（Installation）

```bash
bash install.sh
# → Copies governed_agents/ to $OPENCLAW_WORKSPACE/governed_agents/
# → Runs verification suite (37 tests)
```

## 测试流程（Tests）

```bash
python3 -m pytest governed_agents/test_verification.py \
                   governed_agents/test_council.py \
                   governed_agents/test_profiles.py -v
# 37 passed
```