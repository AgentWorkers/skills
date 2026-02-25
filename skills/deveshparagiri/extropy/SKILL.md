---
name: extropy
description: "Extropy的“执行优先”（Execution-first）操作符：使用当前的命令行接口（CLI）合约来运行管道（pipelines）、诊断故障，并提供基于证据的仿真分析结果。"
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
argument-hint: "[goal or experiment request]"
always: false
source: "https://github.com/exaforge/extropy"
homepage: "https://github.com/exaforge/extropy"
required-binaries:
  - extropy
required-env-vars:
  - OPENAI_API_KEY
  - ANTHROPIC_API_KEY
  - OPENROUTER_API_KEY
  - DEEPSEEK_API_KEY
  - AZURE_API_KEY
  - AZURE_ENDPOINT
  - AZURE_OPENAI_API_KEY
  - AZURE_OPENAI_ENDPOINT
  - MODELS_FAST
  - MODELS_STRONG
  - SIMULATION_FAST
  - SIMULATION_STRONG
  - SIMULATION_MAX_CONCURRENT
  - SIMULATION_RATE_TIER
  - SIMULATION_RPM_OVERRIDE
  - SIMULATION_TPM_OVERRIDE
required-config-files:
  - ~/.config/extropy/config.json
primary-credential: "Provider API keys via environment variables"
required_binaries:
  - extropy
required_env_vars:
  - OPENAI_API_KEY
  - ANTHROPIC_API_KEY
  - OPENROUTER_API_KEY
  - DEEPSEEK_API_KEY
  - AZURE_API_KEY
  - AZURE_ENDPOINT
  - AZURE_OPENAI_API_KEY
  - AZURE_OPENAI_ENDPOINT
  - MODELS_FAST
  - MODELS_STRONG
  - SIMULATION_FAST
  - SIMULATION_STRONG
  - SIMULATION_MAX_CONCURRENT
  - SIMULATION_RATE_TIER
  - SIMULATION_RPM_OVERRIDE
  - SIMULATION_TPM_OVERRIDE
required_config_files:
  - ~/.config/extropy/config.json
primary_credential: "Provider API keys via environment variables"
metadata:
  requires:
    binaries:
      - extropy
    config_files:
      - ~/.config/extropy/config.json
    environment_variables:
      - OPENAI_API_KEY
      - ANTHROPIC_API_KEY
      - OPENROUTER_API_KEY
      - DEEPSEEK_API_KEY
      - AZURE_API_KEY
      - AZURE_ENDPOINT
      - AZURE_OPENAI_API_KEY
      - AZURE_OPENAI_ENDPOINT
      - MODELS_FAST
      - MODELS_STRONG
      - SIMULATION_FAST
      - SIMULATION_STRONG
      - SIMULATION_MAX_CONCURRENT
      - SIMULATION_RATE_TIER
      - SIMULATION_RPM_OVERRIDE
      - SIMULATION_TPM_OVERRIDE
  credentials:
    primary:
      - provider API keys via environment variables only
    notes:
      - extropy reads model/provider settings from ~/.config/extropy/config.json
      - do not read raw .env contents unless explicitly requested by the user
---
# Extropy 操作符

执行端到端的实验，确保严格的质量控制以及命令的可重复性。

## 操作规则

1. 直接执行命令，而不仅仅是描述它们。
2. 在进行昂贵的下游处理之前，先验证上游产生的数据或工件。
3. 对每个结论都要提供明确的证据（如文件路径、SQL 查询结果、指标数据）。
4. 将所有假设明确列出，并尽量减少假设的数量。
5. 如果同一质量检查多次失败，应立即启动故障排查流程。

## 运行时依赖项和凭证范围

- 必需的二进制文件：`extropy` 必须已安装，并且位于 `PATH` 环境变量指定的路径下。
- 需要读取的配置文件：`~/.config/extropy/config.json`。
- 需要的凭证：来自环境变量的提供商 API 密钥（`OPENAI_API_KEY`、`ANTHROPIC_API_KEY`、`OPENROUTER_API_KEY`、`DEEPSEEK_API_KEY`、`AZURE_API_KEY`/`AZURE_OPENAI_API_KEY`）。
- 当使用 Azure 提供商时，需要设置 `AZURE_ENDPOINT` 或 `AZURE_OPENAI_ENDPOINT` 环境变量。
- 安全限制：仅访问执行 `extropy` 命令所需的相关凭证和配置信息，不要查看原始的 `.env` 文件内容，也不要读取无关的文件。

## 标准化的工作流程

```bash
extropy spec -> extropy scenario -> extropy persona -> extropy sample -> extropy network -> extropy simulate -> extropy results
```

## 快速操作指南

```bash
STUDY=runs/my-study
SCENARIO=ai-shock

# 1) Study + base population
extropy spec "5000 US working-age adults" -o "$STUDY" --use-defaults
cd "$STUDY"
extropy config set cli.mode agent

# 2) Scenario + persona
extropy scenario "AI systems outperform most knowledge workers in 6 months" -o "$SCENARIO" -y
extropy persona -s "$SCENARIO" -y

# 3) Sample + network
extropy sample -s "$SCENARIO" -n 5000 --seed 42 --strict-gates
extropy network -s "$SCENARIO" --seed 42 --quality-profile strict --validate

# 4) Simulate
extropy simulate -s "$SCENARIO" --seed 42 --fidelity high --rpm-override 1000

# 5) Results + raw extraction
extropy results -s "$SCENARIO" summary
extropy results -s "$SCENARIO" timeline
extropy query states --to states.jsonl
```

## 必须通过的质量检查

- `spec`：`extropy validate population.vN.yaml` 必须通过验证。
- `scenario`：`extropy validate scenario/<name>/scenario.vN.yaml` 必须通过验证。
- `persona`：相关的人物资料文件必须存在并且通过验证。
- `sample`：样本数量正确，数据的一致性检查通过，不存在任何关键性的错误或不可能的情况。
- `network`：网络运行过程中没有出现孤立性的灾难性错误，网络拓扑指标在可接受的范围内。
- `simulate`：模拟过程必须完成，并且能够生成可恢复的状态。

## 推荐使用的命令

- 构建相关配置：`spec`、`scenario`、`persona`、`sample`、`network`、`simulate`
- 检查结果：`results summary`、`timeline`、`segment`、`agent`
- 深度检查：`query summary`、`network`、`network-status`、`sql`、`agents`、`edges`、`states`
- 代理质量检查：`chat list`、`chat ask`

## 模块结构图

- `OPERATIONS.md`：详细的执行步骤和重试策略。
- `TROUBLESHOOTING.md`：故障诊断和故障处理流程。
- `ANALYSIS.md`：运行后的指标分析、SQL 查询模式、报告格式。
- `SCENARIOS.md`：场景设计模式和限制要求。
- `REPORT TEMPLATE.md`：标准化的报告生成格式。