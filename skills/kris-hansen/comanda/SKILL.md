---
name: comanda
version: 1.0.1
description: 使用 comanda CLI 生成、可视化并执行声明式 AI 工作流。该工具适用于从自然语言创建大型语言模型（LLM）工作流、查看工作流图表、编辑 YAML 格式的工作流文件，以及处理/运行 comanda 工作流。支持多模型编排（OpenAI、Anthropic、Google、Ollama、Claude Code、Gemini CLI、Codex）。
homepage: https://comanda.sh
repository: https://github.com/kris-hansen/comanda
---

# Comanda - 声明式AI工作流工具

🌐 **官方网站:** [comanda.sh](https://comanda.sh) | 📦 **GitHub仓库:** [kris-hansen/comanda](https://github.com/kris-hansen/comanda)

Comanda允许用户使用YAML格式定义AI工作流，并通过命令行来执行这些工作流。这些工作流可以串联多个AI模型，同时运行多个步骤，并将数据传递给不同的处理阶段。

## 安装

```bash
# macOS
brew install kris-hansen/comanda/comanda

# Or via Go
go install github.com/kris-hansen/comanda@latest
```

随后配置API密钥：
```bash
comanda configure
```

## 命令

### 生成工作流

根据自然语言描述创建YAML格式的工作流文件：

```bash
comanda generate <output.yaml> "<prompt>"

# Examples
comanda generate summarize.yaml "Create a workflow that summarizes text input"
comanda generate review.yaml "Analyze code for bugs, then suggest fixes" -m claude-sonnet-4-20250514
```

### 可视化工作流

以ASCII图表的形式展示工作流的结构：

```bash
comanda chart <workflow.yaml>
comanda chart workflow.yaml --verbose
```

图表会显示步骤之间的关系、使用的模型、输入/输出流程以及工作流的有效性。

### 运行/执行工作流

直接运行工作流文件：

```bash
comanda process <workflow.yaml>

# With input
cat file.txt | comanda process analyze.yaml
echo "Design a REST API" | comanda process multi-agent.yaml

# Multiple workflows
comanda process step1.yaml step2.yaml step3.yaml
```

### 查看/编辑工作流

工作流文件采用YAML格式，可以直接阅读以了解或修改其内容：

```bash
cat workflow.yaml
```

## 工作流YAML格式

### 基本步骤

```yaml
step_name:
  input: STDIN | NA | filename | $VARIABLE
  model: gpt-4o | claude-sonnet-4-20250514 | gemini-pro | ollama/llama2 | claude-code | gemini-cli
  action: "Instruction for the model"
  output: STDOUT | filename | $VARIABLE
```

### 并行执行

```yaml
parallel-process:
  analysis-one:
    input: STDIN
    model: claude-sonnet-4-20250514
    action: "Analyze for security issues"
    output: $SECURITY

  analysis-two:
    input: STDIN
    model: gpt-4o
    action: "Analyze for performance"
    output: $PERF
```

### 串联步骤

```yaml
extract:
  input: document.pdf
  model: gpt-4o
  action: "Extract key points"
  output: $POINTS

summarize:
  input: $POINTS
  model: claude-sonnet-4-20250514
  action: "Create executive summary"
  output: STDOUT
```

### 生成与处理（元工作流）

```yaml
create_workflow:
  input: NA
  generate:
    model: gpt-4o
    action: "Create a workflow that analyzes sentiment"
    output: generated.yaml

run_it:
  input: NA
  process:
    workflow_file: generated.yaml
```

## 可用的模型

运行`comanda configure`命令来配置API密钥。常见的模型包括：

| 提供商 | 模型            |
|----------|-------------------|
| OpenAI   | `gpt-4o`, `gpt-4o-mini`, `o1`, `o1-mini` |
| Anthropic | `claude-sonnet-4-20250514`, `claude-opus-4-20250514` |
| Google   | `gemini-pro`, `gemini-flash`     |
| Ollama   | `ollama/llama2`, `ollama/mistral`     |
| Agentic | `claude-code`, `gemini-cli`, `openai-codex` |

## 示例位置

工作流示例位于`~/clawd/comanda/examples/`目录下：
- `agentic-loop/`：自主代理模式示例
- `claude-code/`：Claude Code集成示例
- `gemini-cli/`：Gemini CLI工作流示例
- `document-processing/`：PDF文档处理示例
- `database-connections/`：数据库查询工作流示例

## 故障排除

- **“模型未配置”**：运行`comanda configure`命令来添加API密钥。
- **工作流验证错误**：使用`comanda chart workflow.yaml`命令来可视化并检查工作流的有效性。
- **调试模式**：添加`--debug`参数以启用详细日志记录。