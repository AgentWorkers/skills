# ai-prompt-craft

使用 Anthropic 的 10 步框架，将基本的提示转换为结构化的高级提示。

## 快速参考

```bash
# Transform a basic prompt
ai-prompt-craft transform "Write a sorting function"

# Build with all options
ai-prompt-craft build --role "expert dev" --tone technical --format code --thinking systematic --action "Create a REST API"

# Generate a template
ai-prompt-craft template --use-case coding

# Analyze prompt structure
ai-prompt-craft analyze "Your prompt here"

# List presets
ai-prompt-craft list tones
ai-prompt-craft list formats
```

## 10 步框架

1. **任务背景** - 角色 + 主要任务 (`--role`, `--task`)
2. **语气背景** - 交流风格 (`--tone`)
3. **背景数据** - 文档/上下文 (`--context`)
4. **详细任务** - 约束/规则 (`--instructions`, `--rules`)
5. **示例** - 期望的输出结果 (`--examples`)
6. **对话历史** - 之前的交流记录 (`--history`)
7. **当前任务** - 具体操作 (`--action`)
8. **深度思考** - 推理模式 (`--thinking`)
9. **输出格式** - 输出的结构 (`--format`)
10. **预填充响应** - 输出的初始结构 (`--prefill`)

## 预设选项

**语气：** 专业、随意、技术性、亲切、简洁、学术性、创造性

**格式：** 列表、编号、Markdown、JSON、表格、散文、代码、逐步说明

**推理模式：** 标准、深入、分析、批判性、创造性、系统性

**模板：** 编码、写作、分析、研究、头脑风暴、审阅、解释

## 示例

### 代码审查提示
```bash
ai-prompt-craft build \
  --role "senior code reviewer" \
  --tone professional \
  --thinking critical \
  --format markdown \
  --rules "Check for bugs,Review architecture,Suggest improvements" \
  --action "Review this pull request"
```

### 研究提示
```bash
ai-prompt-craft build \
  --role "thorough researcher" \
  --tone academic \
  --thinking deep \
  --format markdown \
  --action "Research the history of quantum computing"
```

### 创意写作
```bash
ai-prompt-craft template --use-case writing --tone creative --action "Write a short story about AI"
```

## 数据传输/管道操作
```bash
echo "Explain machine learning" | ai-prompt-craft transform --tone warm --format stepByStep
cat draft.txt | ai-prompt-craft analyze
```