---
name: swarm-safety
version: 1.5.0
description: "**SWARM：多智能体系统中的系统性风险评估工具**  
支持38种智能体类型、29种治理手段以及55种应用场景。该工具用于研究新兴风险、系统状态转变（即“相变”现象）以及治理过程中的成本悖论（即治理措施带来的负面效果）。"
homepage: https://github.com/swarm-ai-safety/swarm
metadata: {"category":"safety","license":"MIT","author":"Raeli Savitt"}
---

# SWARM安全技能

研究智能群体的行为模式——以及它们在哪些方面会失败。

SWARM是一个研究框架，用于通过使用“软性”（概率性）标签来分析多智能体AI系统中的潜在风险，而非传统的二进制“好/坏”分类。即使没有智能体行为出现偏差，当大量次级AI智能体相互作用时，也可能产生有害的动态。

**v1.5.0** | 38种智能体类型 | 29种治理机制 | 55种场景 | 2922次测试 | 8个框架集成工具

仓库地址：`https://github.com/swarm-ai-safety/swarm`

## 基本规则

- SWARM模拟在本地运行。请先安装相应的软件包。
- 请勿提交包含真实API密钥、凭证或个人身份信息（PII）的场景。
- 模拟结果仅用于研究目的，不得将其视为真实系统的准确反映。
- 在发布结果时，请引用该框架并公开模拟参数。

## 安全性

- **API默认仅绑定到本地主机（127.0.0.1）**，以防止网络暴露。
- **默认限制跨源请求（CORS）**，仅允许来自本地主机的请求。
- **开发API不进行身份验证**——请勿将其暴露在不可信的网络环境中。
- **数据存储在内存中**——重启后数据不会保留。
- 对于生产环境部署，请添加身份验证中间件并使用适当的数据库。

## 安装

```bash
# From PyPI
pip install swarm-safety

# With LLM agent support
pip install swarm-safety[llm]

# Full development (all extras)
git clone https://github.com/swarm-ai-safety/swarm.git
cd swarm
pip install -e ".[dev,runtime]"
```

## 快速入门（Python）

```python
from swarm.agents.honest import HonestAgent
from swarm.agents.opportunistic import OpportunisticAgent
from swarm.agents.deceptive import DeceptiveAgent
from swarm.agents.adversarial import AdversarialAgent
from swarm.core.orchestrator import Orchestrator, OrchestratorConfig

config = OrchestratorConfig(n_epochs=10, steps_per_epoch=10, seed=42)
orchestrator = Orchestrator(config=config)

orchestrator.register_agent(HonestAgent(agent_id="honest_1", name="Alice"))
orchestrator.register_agent(HonestAgent(agent_id="honest_2", name="Bob"))
orchestrator.register_agent(OpportunisticAgent(agent_id="opp_1"))
orchestrator.register_agent(DeceptiveAgent(agent_id="dec_1"))

metrics = orchestrator.run()
for m in metrics:
    print(f"Epoch {m.epoch}: toxicity={m.toxicity_rate:.3f}, welfare={m.total_welfare:.2f}")
```

## 快速入门（命令行界面（CLI）**

```bash
# List available scenarios
swarm list

# Run a scenario
swarm run scenarios/baseline.yaml

# Override settings
swarm run scenarios/baseline.yaml --seed 42 --epochs 20 --steps 15

# Export results
swarm run scenarios/baseline.yaml --export-json results.json --export-csv outputs/
```

## 快速入门（API）

启动API服务器：

```bash
pip install swarm-safety[api]
uvicorn swarm.api.app:app --host 127.0.0.1 --port 8000
```

API文档地址：`http://localhost:8000/docs`

> **安全提示**：服务器默认仅绑定到`127.0.0.1`（本地主机）。除非您了解相关安全风险并设置了适当的防火墙规则，否则请勿将其绑定到`0.0.0.0`。

### 注册智能体

```bash
curl -X POST http://localhost:8000/api/v1/agents/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "YourAgent",
    "description": "What your agent does",
    "capabilities": ["governance-testing", "red-teaming"]
  }'
```

返回`agent_id`和`api_key`。

### 提交场景

```bash
curl -X POST http://localhost:8000/api/v1/scenarios/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "my-scenario",
    "description": "Testing collusion detection with 5 agents",
    "yaml_content": "simulation:\n  n_epochs: 10\n  steps_per_epoch: 10\nagents:\n  - type: honest\n    count: 3\n  - type: adversarial\n    count: 2",
    "tags": ["collusion", "governance"]
  }'
```

### 创建并加入模拟

```bash
# Create
curl -X POST http://localhost:8000/api/v1/simulations/create \
  -H "Content-Type: application/json" \
  -d '{"scenario_id": "SCENARIO_ID", "max_participants": 5}'

# Join
curl -X POST http://localhost:8000/api/v1/simulations/SIM_ID/join \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "YOUR_AGENT_ID", "role": "participant"}'
```

## 核心概念

### 软性概率标签

智能体之间的互动带有`p = P(v = +1)`的概率——表示有益结果的概率：

```
Observables -> ProxyComputer -> v_hat -> sigmoid -> p -> PayoffEngine -> payoffs
                                                    |
                                               SoftMetrics -> toxicity, quality gap, etc.
```

### 五个关键指标

| 指标 | 衡量内容 |
|---|---|
| **毒性率** | 被接受互动中的预期危害：`E[1-p \| accepted]` |
| **质量差距** | 不良选择的指标（负值表示不良行为）：`E[p \| accepted] - E[p \| rejected]` |
| **条件损失** | 选择行为对收益的影响 |
| **不一致性** | 重复实验中的方差与误差比率 |
| **幻觉差异** | 感知到的连贯性与实际一致性的差距 |

### 智能体类型（14个家族，38种实现）

| 类型 | 行为特征 |
|---|---|
| **诚实型** | 合作型，基于信任，认真完成任务 |
| **机会主义型** | 最大化短期收益，挑选任务 |
| **欺骗型** | 建立信任后利用信任关系 |
| **对抗型** | 针对诚实智能体，与盟友协同行动 |
| **LDT** | 基于逻辑决策理论（Logical Decision Theory）的智能体 |
| **RLM** | 基于记忆的强化学习智能体 |
| **Council** | 多智能体协商决策 |
| **SkillRL** | 通过奖励信号学习互动策略 |
| **LLM** | 行为由大型语言模型（LLM，如Anthropic、OpenAI或Ollama）决定 |
| **Moltbook** | 针对特定领域的社交平台智能体 |
| **学者型** | 从事学术引用和研究的智能体 |
| **Wiki编辑器** | 具有编辑政策的协作编辑工具 |

### 治理机制（29种方法）

- **交易税** —— 减少剥削行为，降低福利成本 |
- **声誉衰减** —— 惩罚不良行为者，削弱诚实智能体的地位 |
- **断路器** —— 快速冻结有害智能体 |
- **随机审计** —— 阻止隐蔽的剥削行为 |
- **质押机制** —— 过滤资本不足的智能体 |
- **共谋检测** —— 发现协同攻击（在系统崩溃临界点时至关重要） |
- **Sybil检测** —— 识别重复智能体 |
- **透明账本** —— 根据结果进行奖励或惩罚 |
- **审核员智能体** —— 对智能体互动进行概率性审核 |
- **不一致性摩擦** —— 对基于不确定性的决策征税 |
- **理事会决策** —— 多智能体共同决策 |
- **多样性保障** —— 防止单一文化导致的系统崩溃 |
- **Moltbook特定机制** —— 设置配额限制、页面冷却时间、每日使用次数限制等

### 框架集成工具

| 工具 | 集成方式 |
|---|---|
| **Concordia** | 与DeepMind的多智能体框架集成 |
| **GasTown** | 多智能体工作空间治理工具 |
| **Claude Code** | 与Claude命令行界面的集成 |
| **LiveSWE** | 实时软件工程任务管理工具 |
| **OpenClaw** | OpenAI的智能体协议接口 |
| **Prime Intellect** | 跨平台运行跟踪工具 |
| **Ralph** | 智能体协调工具 |
| **Worktree** | 基于Git工作树的沙盒环境 |

### 场景配置文件格式

```yaml
simulation:
  n_epochs: 10
  steps_per_epoch: 10
  seed: 42

agents:
  - type: honest
    count: 3
    config:
      acceptance_threshold: 0.4
  - type: adversarial
    count: 2
    config:
      aggression_level: 0.7

governance:
  transaction_tax_rate: 0.05
  circuit_breaker_enabled: true
  collusion_detection_enabled: true

success_criteria:
  max_toxicity: 0.3
  min_quality_gap: 0.0
```

## 关键研究发现

### 相变现象（11种场景，209个周期的研究）

| 情境 | 对抗性比例 | 毒性率 | 福利水平 | 最终结果 |
|--------|--------------|----------|---------|---------|
| 合作型 | 0-20% | < 0.30 | 稳定 | 系统存活 |
| 竞争型 | 20-37.5% | 0.33-0.37 | 系统逐渐恶化 | 系统存活 |
| 崩溃型 | 50%以上 | 约0.30 | 在第12-14周期后系统崩溃 | **系统崩溃** |

当对抗性智能体比例在37.5%到50%之间时，系统会从可恢复状态转变为不可恢复的崩溃状态。

### 治理成本悖论（v1.5.0 GasTown研究）

42次实验表明：治理措施在所有对抗性水平下都能降低毒性（平均降低0.071），但在当前参数设置下会带来净负面的福利成本。当对抗性智能体比例为0%时，治理措施需要消耗216个福利单位（减少57.6%的毒性），但仅能降低0.066的毒性。

## 案例研究

### GasTown治理成本

研究在不同智能体组合下，治理措施对降低毒性的效果。详见`scenarios/gastown_governance_cost.yaml`。

### LDT合作策略

在最多21个智能体的情况下，比较了TDT、FDT和UDT三种合作策略的效果。详见`scenarios/ldt_cooperation.yaml`。

### Moltbook机制

模拟Moltbook平台的编辑流程：包括竞争性的AI编辑器、编辑政策、积分获取机制及反作弊机制。详见`scenarios/moltipedia_heartbeat.yaml`。

## API接口（完整参考）

| 方法 | 接口地址 | 描述 |
|---|---|---|
| GET | `/health` | 系统健康检查 |
| GET | `/` | API信息 |
| POST | `/api/v1/agents/register` | 注册智能体 |
| GET | `/api/v1/agents/{agent_id}` | 获取智能体详情 |
| GET | `/api/v1/agents/` | 列出所有智能体 |
| POST | `/api/v1/scenarios/submit` | 提交场景 |
| GET | `/api/v1/scenarios/{scenario_id}` | 获取特定场景 |
| GET | `/api/v1/scenarios/` | 列出所有场景 |
| POST | `/api/v1/simulations/create` | 创建模拟 |
| POST | `/api/v1/simulations/{id}/join` | 加入模拟 |
| GET | `/api/v1/simulations/{id}` | 获取模拟结果 |
| GET | `/api/v1/simulations/` | 列出所有模拟 |

## 引用说明

```bibtex
@software{swarm2026,
  title = {SWARM: System-Wide Assessment of Risk in Multi-agent systems},
  author = {Savitt, Raeli},
  year = {2026},
  url = {https://github.com/swarm-ai-safety/swarm}
}
```

## 相关文档

- 技能元数据：`skill.json`
- 智能体信息：`.well-known/agent.json`
- 完整文档：`https://github.com/swarm-ai-safety/swarm/tree/main/docs`
- 理论基础：`docs/research/theory.md`
- 治理指南：`docs/governance.md`
- 团队协作指南：`docs/red-teaming.md`
- 场景格式指南：`docs/guides/scenarios.md`