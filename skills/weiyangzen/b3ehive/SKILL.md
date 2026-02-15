# b3ehive 技能规范  
## 符合 PCTF 标准的多智能体竞赛系统  

---

## 1. 目的（PCTF: Purpose）  
该系统旨在实现一个竞争性的代码生成环境，其中三个独立的 AI 智能体各自实现相同的功能，通过客观评估相互竞争，并最终通过数据驱动的方式选出最优解。  

---

## 2. 任务定义（PCTF: Task）  
### 输入  
- **task_description**：描述编码任务的字符串  
- **constraints**：可选的约束条件（如时间复杂度、空间复杂度、编程语言等）  

### 输出  
- **final_solution**：包含获胜者实现的代码目录  
- **comparison_report**：关于所有三种实现方式的 Markdown 分析报告  
- **decision_rationale**：选择获胜者的理由说明  

### 成功标准  
```yaml
assertions:
  - final_solution/implementation exists and is runnable
  - comparison_report.md exists with objective metrics
  - decision_rationale.md explains selection logic
  - all three agent implementations are documented
  - evaluation scores are numeric and justified
```  

---

## 3. 任务流程（PCTF: Chain）  
```mermaid
graph TD
    A[User Task] --> B[Phase 1: Parallel Spawn]
    B --> C[Agent A: Simplicity]
    B --> D[Agent B: Speed]
    B --> E[Agent C: Robustness]
    C --> F[Phase 2: Cross-Evaluation]
    D --> F
    E --> F
    F --> G[6 Evaluation Reports]
    G --> H[Phase 3: Self-Scoring]
    H --> I[3 Scorecards]
    I --> J[Phase 4: Final Delivery]
    J --> K[Best Solution]
```  

### 第一阶段：并行实现  
**智能体提示模板**：  
```yaml
role: "Expert Software Engineer"
focus: "{{agent_focus}}"  # Simplicity / Speed / Robustness
task: "{{task_description}}"
constraints:
  - Complete runnable code in implementation/
  - Checklist.md with ALL items checked
  - SUMMARY.md with competitive advantages
  - Must differ from other agents' approaches

linter_rules:
  - code_compiles: true
  - tests_pass: true
  - no_todos: true
  - documented: true

assertions:
  - implementation/main.* exists
  - tests exist and pass
  - Checklist.md is complete
  - SUMMARY.md explains unique approach
```  

### 第二阶段：交叉评估  
**评估提示模板**：  
```yaml
evaluator: "Agent {{from}}"
target: "Agent {{to}}"
task: "Objectively prove your solution is superior"

dimensions:
  simplicity:
    weight: 20
    metrics:
      - lines_of_code: count
      - cyclomatic_complexity: calculate
      - readability_score: 1-10
  
  speed:
    weight: 25
    metrics:
      - time_complexity: big_o
      - space_complexity: big_o
      - benchmark_results: run_if_possible
  
  stability:
    weight: 25
    metrics:
      - error_handling_coverage: percentage
      - resource_cleanup: check
      - fault_tolerance: test
  
  corner_cases:
    weight: 20
    metrics:
      - input_validation: comprehensive
      - boundary_conditions: covered
      - edge_cases: tested
  
  maintainability:
    weight: 10
    metrics:
      - documentation_quality: 1-10
      - code_structure: logical
      - extensibility: easy/hard

assertions:
  - evaluation is objective with data
  - specific code snippets cited
  - numeric scores provided
  - persuasion argument is data-driven
```  

### 第三阶段：客观评分  
**评分提示模板**：  
```yaml
agent: "Agent {{name}}"
task: "Fairly score yourself and competitors"

self_evaluation:
  - dimension: simplicity
    max: 20
    score: "{{self_score}}"
    justification: "{{why}}"
  
  - dimension: speed
    max: 25
    score: "{{self_score}}"
    justification: "{{why}}"
  
  - dimension: stability
    max: 25
    score: "{{self_score}}"
    justification: "{{why}}"
  
  - dimension: corner_cases
    max: 20
    score: "{{self_score}}"
    justification: "{{why}}"
  
  - dimension: maintainability
    max: 10
    score: "{{self_score}}"
    justification: "{{why}}"

peer_evaluation:
  - target: "Agent {{other}}"
    scores: "{{numeric_scores}}"
    comparison: "{{objective_comparison}}"

final_conclusion:
  best_implementation: "[A/B/C/Mixed]"
  reasoning: "{{data_driven_justification}}"
  recommendation: "{{delivery_strategy}}"

assertions:
  - all scores are numeric
  - justifications are specific
  - no inflation or bias
  - conclusion is evidence-based
```  

### 第四阶段：最终交付  
**决策逻辑**：  
```python
def select_winner(scores):
    """
    Select final solution based on competitive scores
    """
    margins = calculate_score_margins(scores)
    
    if margins.winner - margins.second > 15:
        # Clear winner
        return SingleWinner(scores.winner)
    elif margins.winner - margins.second > 5:
        # Close competition, consider hybrid
        return HybridSolution(scores.top_two)
    else:
        # Very close, pick simplest
        return SimplestImplementation(scores.all)

assertions:
  - final_solution is runnable
  - comparison_report explains all approaches
  - decision_rationale is transparent
  - attribution is given to winning agent
```  

---

## 4. 格式规范（PCTF: Format）  
### 目录结构  
```
workspace/
├── run_a/
│   ├── implementation/      # Agent A code
│   ├── Checklist.md         # Completion checklist
│   ├── SUMMARY.md           # Approach summary
│   ├── evaluation/          # Evaluations of B, C
│   └── SCORECARD.md         # Self-scoring
├── run_b/                   # Same structure
├── run_c/                   # Same structure
├── final/                   # Winning solution
├── COMPARISON_REPORT.md     # Full analysis
└── DECISION_RATIONALE.md    # Why winner selected
```  

### 文件格式  
- **Checklist.md**：包含复选框的 Markdown 文件  
- **SUMMARY.md**：分节的 Markdown 文件  
- **EVALUATION_*.md**：包含表格的 Markdown 文件  
- **SCORECARD.md**：包含评分表的 Markdown 文件  
- **Implementation**：可执行的代码文件  

---

## 5. 代码检查与验证  
### 提交前的检查（Pre-commit Checks）  
```bash
#!/bin/bash
# scripts/lint.sh

lint_agent_output() {
    local agent_dir="$1"
    local errors=0
    
    # Check required files exist
    for file in Checklist.md SUMMARY.md implementation/main.*; do
        if [[ ! -f "${agent_dir}/${file}" ]]; then
            echo "ERROR: Missing ${file}"
            ((errors++))
        fi
    done
    
    # Check Checklist is complete
    if grep -q "\[ \]" "${agent_dir}/Checklist.md"; then
        echo "ERROR: Checklist has unchecked items"
        ((errors++))
    fi
    
    # Check code compiles (language-specific)
    # ... implementation-specific checks
    
    return $errors
}

# Run on all agents
for agent in a b c; do
    lint_agent_output "workspace/run_${agent}" || exit 1
done
```  

### 运行时断言（Runtime Assertions）  
```python
def assert_phase_complete(phase_name):
    """Assert that a phase has completed successfully"""
    assertions = {
        "phase1": [
            "workspace/run_a/implementation exists",
            "workspace/run_b/implementation exists", 
            "workspace/run_c/implementation exists",
            "All Checklist.md are complete"
        ],
        "phase2": [
            "6 evaluation reports exist",
            "All evaluations have numeric scores"
        ],
        "phase3": [
            "3 scorecards exist",
            "All scores are numeric",
            "Conclusions are provided"
        ],
        "phase4": [
            "final/solution exists",
            "COMPARISON_REPORT.md exists",
            "DECISION_RATIONALE.md exists"
        ]
    }
    
    for assertion in assertions[phase_name]:
        assert evaluate(assertion), f"Assertion failed: {assertion}"
```  

---

## 6. 配置（Configuration）  
```yaml
b3ehive:
  # Agent configuration
  agents:
    count: 3
    model: openai-proxy/gpt-5.3-codex
    thinking: high
    focuses:
      - simplicity
      - speed
      - robustness
  
  # Evaluation weights (must sum to 100)
  evaluation:
    dimensions:
      simplicity: 20
      speed: 25
      stability: 25
      corner_cases: 20
      maintainability: 10
  
  # Delivery strategy
  delivery:
    strategy: auto  # auto / best / hybrid
    threshold: 15   # Point margin for clear winner
  
  # Quality gates
  quality:
    lint: true
    test: true
    coverage_threshold: 80
```  

---

## 7. 使用方法（Usage）  
```bash
# Basic usage
b3ehive "Implement a thread-safe rate limiter"

# With constraints
b3ehive "Implement quicksort" --lang python --max-lines 50

# Using OpenClaw CLI
openclaw skills run b3ehive --task "Your task"
```  

---

## 8. 许可证  
MIT © Weiyang ([@weiyangzen](https://github.com/weiyangzen))