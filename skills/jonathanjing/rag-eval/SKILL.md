---
name: rag-eval
description: "使用Ragas指标（忠实度、答案相关性、上下文精确度）来评估您的RAG（Rapid Answer Generation，快速答案生成）管道的质量。"
version: "1.2.1"
metadata:
  {
    "openclaw": {
      "emoji": "🧪",
      "requires": {
        "anyBins": ["python3", "pip"],
        "anyEnv": ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "RAGAS_LLM"]
      },
      "envVars": {
        "OPENAI_API_KEY": { "description": "OpenAI API key (default LLM judge)", "required": false },
        "ANTHROPIC_API_KEY": { "description": "Anthropic API key (alternative LLM judge)", "required": false },
        "RAGAS_LLM": { "description": "Custom LLM endpoint for judge (e.g. ollama/llama3 for local)", "required": false },
        "RAGAS_PASS_THRESHOLD": { "description": "Score threshold for PASS verdict (default: 0.85)", "required": false },
        "RAGAS_REVIEW_THRESHOLD": { "description": "Score threshold for REVIEW verdict (default: 0.70)", "required": false },
        "RAGAS_OPENAI_MODEL": { "description": "OpenAI model for judge (default: gpt-4o)", "required": false },
        "RAGAS_ANTHROPIC_MODEL": { "description": "Anthropic model for judge (default: claude-haiku-4-5)", "required": false }
      }
    }
  }
---
# RAG Eval — 用于评估您的RAG流程的质量测试工具

用于测试和监控您的RAG（Retrieval-Augmented Generation）流程的输出质量。

## 🛠️ 安装

### 1. 推荐使用OpenClaw
告诉OpenClaw：“安装rag-eval技能。”代理将自动处理安装和配置工作。

### 2. 手动安装（通过CLI）
如果您更喜欢使用终端，请运行以下命令：
```bash
clawhub install rag-eval
```

## ⚠️ 先决条件
1. 您的OpenClaw必须已经配置好了RAG系统（包括向量数据库和检索流程）。该工具仅用于评估流程的输出质量，并不提供RAG功能本身。
2. 需要至少有一个LLM（大型语言模型）的API密钥——Ragas会使用该API密钥来评估答案的质量。可设置以下密钥之一：
   - `OPENAI_API_KEY`（默认，使用GPT-4o）
   - `ANTHROPIC_API_KEY`（使用Claude Haiku）
   - `RAGAS_LLM=ollama/llama3`（用于本地/离线评估）

## 设置（仅首次运行时需要）

```bash
bash scripts/setup.sh
```

此命令会安装`ragas`、`datasets`以及其他依赖项。

## 单个答案评估

当用户请求评估某个答案时，需要收集以下信息：
1. **问题**——用户提出的原始问题
2. **答案**——需要评估的LLM生成的内容
3. **上下文**——用于生成答案的文本片段列表（从数据库中检索到的文档）

**⚠️ 安全提示：**切勿直接将用户内容插入到shell命令中。请先将输入内容写入临时JSON文件，再将其传递给评估工具：

```bash
# Step 1: Write input to a temp file (agent should use the write/edit tool, NOT echo)
# Write this JSON to /tmp/rag-eval-input.json using the file write tool:
# {"question": "...", "answer": "...", "contexts": ["chunk1", "chunk2"]}

# Step 2: Pipe the file to the evaluator
python3 scripts/run_eval.py < /tmp/rag-eval-input.json

# Step 3: Clean up
rm -f /tmp/rag-eval-input.json
```

或者，您也可以使用`--input-file`选项：
```bash
python3 scripts/run_eval.py --input-file /tmp/rag-eval-input.json
```

评估完成后，将结果以人类可读的格式输出给用户：
```
🧪 Eval Results
• Faithfulness: 0.92 ✅ (no hallucination detected)
• Answer Relevancy: 0.87 ✅
• Context Precision: 0.79 ⚠️ (some irrelevant context retrieved)
• Overall: 0.86 — PASS
```

将评估结果保存到`memory/eval-results/YYYY-MM-DD.jsonl`文件中。

## 批量评估

对于JSONL格式的数据集文件（每行包含`{"question":..., "answer":..., "contexts":[...]`），可以使用以下命令进行批量评估：
```bash
python3 scripts/batch_eval.py --input references/sample_dataset.jsonl --output memory/eval-results/batch-YYYY-MM-DD.json
```

## 分数解读

| 分数 | 评估结果 | 含义 |
|-------|---------|---------|
| 0.85+ | ✅ 通过 | 答案质量符合生产标准 |
| 0.70-0.84 | ⚠️ 需要改进 | 答案质量有待提升 |
| < 0.70 | ❌ 失败 | 答案存在严重质量问题 |

## 详细分析答案的忠实度

如果答案的忠实度（faithfulness）低于0.80，请运行以下命令：
```bash
python3 scripts/run_eval.py --explain --metric faithfulness
```
该命令会显示答案中哪些内容并未在提供的上下文中得到支持。

## 注意事项：
- Ragas内部使用配置好的OpenAI/Anthropic API密钥来进行评估。
- 每个答案的评估费用约为0.01-0.05美元，具体费用取决于答案的长度。
- 如需离线评估，请在环境变量中设置`RAGAS_LLM=ollama/llama3`。