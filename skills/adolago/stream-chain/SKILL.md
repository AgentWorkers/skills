---
name: stream-chain
description: **Stream-JSON 链式处理：用于多代理管道、数据转换及顺序工作流**  

Stream-JSON 提供了一种灵活的链式处理机制，适用于需要处理多个代理（agents）的数据流、执行数据转换操作以及管理顺序工作流程的场景。该技术允许开发者将多个处理步骤串联起来，形成一个连续的数据处理链，确保数据在各个处理环节之间能够高效、准确地传递。  

**核心特点：**  
1. **多代理支持**：支持与多个代理协同工作，每个代理可以执行特定的数据处理任务。  
2. **数据转换能力**：提供丰富的转换函数，能够对数据进行格式化、过滤、聚合等操作。  
3. **顺序控制**：确保处理步骤按照预定的顺序执行，保证数据处理的一致性和准确性。  
4. **可扩展性**：通过模块化设计，易于扩展新的处理功能或代理。  

**应用场景：**  
- **数据采集与处理**：从多个数据源采集数据，然后通过 Stream-JSON 进行统一处理（如清洗、转换、存储）。  
- **自动化工作流**：构建自动化测试、部署等流程，确保每个步骤按顺序执行。  
- **分布式系统**：在分布式环境中实现高效的数据处理和协调。  

**示例：**  
假设我们有一个包含多个代理的数据处理流程：  
- **代理 1**：从数据库中读取数据。  
- **代理 2**：对数据进行过滤（例如，删除重复记录）。  
- **代理 3**：将数据转换为 JSON 格式。  
通过 Stream-JSON，这些代理可以依次执行这些任务，而无需手动编写复杂的协调代码。  

**优势：**  
- **简化开发**：通过链式处理，开发者可以更专注于业务逻辑，无需关心底层的数据传输和协调问题。  
- **提高效率**：自动化的流程控制减少了人为错误，提高了处理速度。  
- **灵活性**：易于根据需求添加或修改处理步骤。  

**总结：**  
Stream-JSON 为多代理管道、数据转换及顺序工作流提供了强大的支持，有助于提升数据处理的效率和可靠性。它通过链式处理机制，简化了开发流程，同时保持了系统的灵活性和可扩展性。
version: 1.0.0
category: workflow
tags: [streaming, pipeline, chaining, multi-agent, workflow]
---

# Stream-Chain 技能

Stream-Chain 可执行复杂的多步骤工作流程，其中每个代理的输出都会传递给下一个代理，从而实现复杂的数据转换和顺序处理流程。

## 概述

Stream-Chain 提供了两种强大的模式来编排多代理工作流程：

1. **自定义链**（`run`）：以完全可控的方式执行自定义的提示序列。
2. **预定义的流程**（`pipeline`）：使用经过验证的工作流程来处理常见任务。

链中的每个步骤都会接收前一步的输出，通过数据流实现复杂的多代理协调。

---

## 快速入门

### 运行自定义链

```bash
claude-flow stream-chain run \
  "Analyze codebase structure" \
  "Identify improvement areas" \
  "Generate action plan"
```

### 执行流程

```bash
claude-flow stream-chain pipeline analysis
```

---

## 自定义链（`run`）

使用您自己的提示来运行自定义的流式链，以实现最大的灵活性。

### 语法

```bash
claude-flow stream-chain run <prompt1> <prompt2> [...] [options]
```

**要求：**
- 至少需要 2 个提示。
- 每个提示都成为链中的一个步骤。
- 输出会按顺序传递给所有步骤。

### 选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--verbose` | 显示详细的执行信息 | `false` |
| `--timeout <秒>` | 每步的超时时间 | `30` |
| `--debug` | 启用带有完整日志的调试模式 | `false` |

### 上下文如何传递

每个步骤都会接收前一步的输出作为上下文：

```
Step 1: "Write a sorting function"
Output: [function implementation]

Step 2 receives:
  "Previous step output:
  [function implementation]

  Next task: Add comprehensive tests"

Step 3 receives:
  "Previous steps output:
  [function + tests]

  Next task: Optimize performance"
```

### 示例

#### 基本开发链

```bash
claude-flow stream-chain run \
  "Write a user authentication function" \
  "Add input validation and error handling" \
  "Create unit tests with edge cases"
```

#### 安全审计工作流程

```bash
claude-flow stream-chain run \
  "Analyze authentication system for vulnerabilities" \
  "Identify and categorize security issues by severity" \
  "Propose fixes with implementation priority" \
  "Generate security test cases" \
  --timeout 45 \
  --verbose
```

#### 代码重构链

```bash
claude-flow stream-chain run \
  "Identify code smells in src/ directory" \
  "Create refactoring plan with specific changes" \
  "Apply refactoring to top 3 priority items" \
  "Verify refactored code maintains behavior" \
  --debug
```

#### 数据处理流程

```bash
claude-flow stream-chain run \
  "Extract data from API responses" \
  "Transform data into normalized format" \
  "Validate data against schema" \
  "Generate data quality report"
```

---

## 预定义的流程（`pipeline`）

执行经过验证的工作流程，专为常见的开发任务优化。

### 语法

```bash
claude-flow stream-chain pipeline <type> [options]
```

### 可用的流程

#### 1. 分析流程

全面的代码库分析和改进点识别。

```bash
claude-flow stream-chain pipeline analysis
```

**工作流程步骤：**
1. **结构分析**：映射目录结构并识别组件。
2. **问题检测**：发现潜在的改进点和问题。
3. **建议**：生成可操作的改进报告。

**使用场景：**
- 新代码库的入职培训。
- 技术债务评估。
- 架构审查。
- 代码质量审计。

#### 2. 重构流程

系统化的代码重构，并进行优先级排序。

```bash
claude-flow stream-chain pipeline refactor
```

**工作流程步骤：**
1. **候选项识别**：找到需要重构的代码。
2. **优先级排序**：创建优先级排序的重构计划。
3. **实施**：为最高优先级的任务提供重构后的代码。

**使用场景：**
- 减少技术债务。
- 提高代码质量。
- 旧代码现代化。
- 设计模式实现。

#### 3. 测试流程

生成全面的测试，并进行覆盖分析。

```bash
claude-flow stream-chain pipeline test
```

**工作流程步骤：**
1. **覆盖分析**：识别缺乏测试的部分。
2. **测试设计**：为关键功能创建测试用例。
3. **实施**：生成带有断言的单元测试。

**使用场景：**
- 提高测试覆盖率。
- 支持测试驱动开发（TDD）工作流程。
- 创建回归测试。
- 质量保证。

#### 4. 优化流程

通过性能分析和实施来优化性能。

```bash
claude-flow stream-chain pipeline optimize
```

**工作流程步骤：**
1. **性能分析**：识别性能瓶颈。
2. **策略**：分析并建议优化方法。
3. **实施**：提供优化后的代码。

**使用场景：**
- 性能提升。
- 资源优化。
- 可扩展性增强。
- 延迟减少。

### 流程选项

| 选项 | 描述 | 默认值 |
|--------|-------------|---------|
| `--verbose` | 显示详细的执行信息 | `false` |
| `--timeout <秒>` | 每步的超时时间 | `30` |
| `--debug` | 启用调试模式 | `false` |

### 流程示例

#### 快速分析

```bash
claude-flow stream-chain pipeline analysis
```

#### 扩展重构

```bash
claude-flow stream-chain pipeline refactor --timeout 60 --verbose
```

#### 调试测试生成

```bash
claude-flow stream-chain pipeline test --debug
```

#### 全面优化

```bash
claude-flow stream-chain pipeline optimize --timeout 90 --verbose
```

### 流程输出

每个流程的执行都会提供：
- **进度**：逐步的执行状态。
- **结果**：每步的成功/失败情况。
- **时间**：总执行时间和每步的执行时间。
- **总结**：汇总的结果和建议。

---

## 定义自定义流程

在 `.claude-flow/config.json` 中定义可重用的流程：

### 配置格式

```json
{
  "streamChain": {
    "pipelines": {
      "security": {
        "name": "Security Audit Pipeline",
        "description": "Comprehensive security analysis",
        "prompts": [
          "Scan codebase for security vulnerabilities",
          "Categorize issues by severity (critical/high/medium/low)",
          "Generate fixes with priority and implementation steps",
          "Create security test suite"
        ],
        "timeout": 45
      },
      "documentation": {
        "name": "Documentation Generation Pipeline",
        "prompts": [
          "Analyze code structure and identify undocumented areas",
          "Generate API documentation with examples",
          "Create usage guides and tutorials",
          "Build architecture diagrams and flow charts"
        ]
      }
    }
  }
}
```

### 执行自定义流程

```bash
claude-flow stream-chain pipeline security
claude-flow stream-chain pipeline documentation
```

---

## 高级用法

### 多代理协调

将不同类型的代理链接起来，以执行复杂的工作流程：

```bash
claude-flow stream-chain run \
  "Research best practices for API design" \
  "Design REST API with discovered patterns" \
  "Implement API endpoints with validation" \
  "Generate OpenAPI specification" \
  "Create integration tests" \
  "Write deployment documentation"
```

### 数据转换流程

通过多个阶段处理和转换数据：

```bash
claude-flow stream-chain run \
  "Extract user data from CSV files" \
  "Normalize and validate data format" \
  "Enrich data with external API calls" \
  "Generate analytics report" \
  "Create visualization code"
```

### 代码迁移工作流程

系统化的代码迁移，并进行验证：

```bash
claude-flow stream-chain run \
  "Analyze legacy codebase dependencies" \
  "Create migration plan with risk assessment" \
  "Generate modernized code for high-priority modules" \
  "Create migration tests" \
  "Document migration steps and rollback procedures"
```

### 质量保证流程

全面的代码质量工作流程：

```bash
claude-flow stream-chain pipeline analysis
claude-flow stream-chain pipeline refactor
claude-flow stream-chain pipeline test
claude-flow stream-chain pipeline optimize
```

---

## 最佳实践

### 1. 清晰具体的提示

**好的做法：**
```bash
"Analyze authentication.js for SQL injection vulnerabilities"
```

**避免的做法：**
```bash
"Check security"
```

### 2. 逻辑顺序

按照逻辑顺序排列提示，以便基于之前的输出进行操作：

```bash
1. "Identify the problem"
2. "Analyze root causes"
3. "Design solution"
4. "Implement solution"
5. "Verify implementation"
```

### 3. 适当的超时设置

- 简单任务：30 秒（默认值）。
- 分析任务：45-60 秒。
- 实施任务：60-90 秒。
- 复杂工作流程：90-120 秒。

### 4. 验证步骤

在流程中包含验证步骤：

```bash
claude-flow stream-chain run \
  "Implement feature X" \
  "Write tests for feature X" \
  "Verify tests pass and cover edge cases"
```

### 5. 迭代改进

使用流程进行迭代改进：

```bash
claude-flow stream-chain run \
  "Generate initial implementation" \
  "Review and identify issues" \
  "Refine based on issues found" \
  "Final quality check"
```

---

## 与 Claude Flow 的集成

### 与 Swarm 协调结合使用

```bash
# Initialize swarm for coordination
claude-flow swarm init --topology mesh

# Execute stream chain with swarm agents
claude-flow stream-chain run \
  "Agent 1: Research task" \
  "Agent 2: Implement solution" \
  "Agent 3: Test implementation" \
  "Agent 4: Review and refine"
```

### 内存集成

流式链会自动将上下文存储在内存中，以实现跨会话的持久性：

```bash
# Execute chain with memory
claude-flow stream-chain run \
  "Analyze requirements" \
  "Design architecture" \
  --verbose

# Results stored in .claude-flow/memory/stream-chain/
```

### 神经模式训练

成功的流程可以训练神经模式，以提高性能：

```bash
# Enable neural training
claude-flow stream-chain pipeline optimize --debug

# Patterns learned and stored for future optimizations
```

---

## 故障排除

### 流程超时

如果步骤超时，请增加超时值：

```bash
claude-flow stream-chain run "complex task" --timeout 120
```

### 上下文丢失

如果上下文传递不正常，请使用 `--debug`：

```bash
claude-flow stream-chain run "step 1" "step 2" --debug
```

### 流程未找到

验证流程名称和自定义定义：

```bash
# Check available pipelines
cat .claude-flow/config.json | grep -A 10 "streamChain"
```

---

## 性能特性

- **吞吐量**：每分钟 2-5 步（根据复杂度而异）。
- **上下文大小**：每步最多 100K 个标记。
- **内存使用**：每个活动流程大约使用 50MB 内存。
- **并发性**：支持并行执行流程。

---

## 相关技能

- **SPARC 方法论**：系统化的开发工作流程。
- **Swarm 协调**：多代理编排。
- **内存管理**：持久化上下文存储。
- **神经模式**：自适应学习。

---

## 示例仓库

### 完整的开发工作流程

```bash
# Full feature development chain
claude-flow stream-chain run \
  "Analyze requirements for user profile feature" \
  "Design database schema and API endpoints" \
  "Implement backend with validation" \
  "Create frontend components" \
  "Write comprehensive tests" \
  "Generate API documentation" \
  --timeout 60 \
  --verbose
```

### 代码审查流程

```bash
# Automated code review workflow
claude-flow stream-chain run \
  "Analyze recent git changes" \
  "Identify code quality issues" \
  "Check for security vulnerabilities" \
  "Verify test coverage" \
  "Generate code review report with recommendations"
```

### 迁移助手

```bash
# Framework migration helper
claude-flow stream-chain run \
  "Analyze current Vue 2 codebase" \
  "Identify Vue 3 breaking changes" \
  "Create migration checklist" \
  "Generate migration scripts" \
  "Provide updated code examples"
```

---

## 结论

Stream-Chain 通过以下方式实现复杂的多步骤工作流程：

- **顺序处理**：每个步骤都基于之前的结果进行操作。
- **上下文保留**：完整的输出历史会传递给整个流程。
- **灵活的编排**：支持自定义链或预定义的流程。
- **代理协调**：自然的多代理协作模式。
- **数据转换**：通过简单的步骤实现复杂的数据处理。

对于自定义工作流程，请使用 `run`；对于经过验证的解决方案，请使用 `pipeline`。