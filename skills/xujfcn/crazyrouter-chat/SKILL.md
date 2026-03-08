---
name: crazyrouter-chat
description: 通过Crazyrouter与627个以上的人工智能模型进行交流。这些模型包括GPT-5、Claude Opus 4.6、Gemini 3、DeepSeek R1、Llama 4、Qwen3和Grok 4。当用户需要查询特定模型、比较不同模型的回答，或从其他AI那里获取第二意见时，可以使用该工具。
---
# 通过Crazyrouter实现的多模型聊天

您可以通过[Crazyrouter](https://crazyrouter.com)与627种以上的人工智能模型进行聊天——只需一个API密钥，即可使用所有模型。

## 支持的模型（部分示例）

| 提供商 | 模型          |
|---------|--------------|
| OpenAI   | gpt-5, gpt-5-mini, gpt-4.1, gpt-4o, o3, o4-mini |
| Anthropic | claude-opus-4-6, claude-sonnet-4, claude-haiku-3.5 |
| Google   | gemini-3-pro, gemini-2.5-flash |
| DeepSeek | deepseek-r1, deepseek-v3     |
| Meta     | llama-4-scout, llama-4-maverick |
| Alibaba | qwen3-235b, qwen3-32b     |
| xAI    | grok-4, grok-3        |
| Mistral  | mistral-large, codestral    |

## 脚本目录

**代理执行方式：**
1. `SKILL_DIR`：当前`SKILL.md`文件所在的目录
2. 脚本路径：`${SKILL_DIR}/scripts/main.ts`

## 第0步：检查API密钥 ⛔ 此步骤会阻止进一步操作

```bash
echo "${CRAZYROUTER_API_KEY:-not_set}"
```

| 检查结果 | 应采取的行动 |
|---------|-------------|
| 密钥找到   | 继续执行       |
| 密钥未找到 | 请用户设置`CRAZYROUTER_API_KEY`。密钥可在[https://crazyrouter.com]获取 |

## 使用方法

```bash
# Ask GPT-5 a question
npx -y bun ${SKILL_DIR}/scripts/main.ts --model gpt-5 --prompt "Explain quantum computing in 3 sentences"

# Compare models
npx -y bun ${SKILL_DIR}/scripts/main.ts --model deepseek-r1 --prompt "Write a sorting algorithm in Python"
npx -y bun ${SKILL_DIR}/scripts/main.ts --model claude-opus-4-6 --prompt "Write a sorting algorithm in Python"

# With system prompt
npx -y bun ${SKILL_DIR}/scripts/main.ts --model gemini-3-pro --system "You are a pirate" --prompt "Tell me about the weather"

# With temperature
npx -y bun ${SKILL_DIR}/scripts/main.ts --model gpt-5-mini --prompt "Write a poem" --temperature 1.2

# Save output to file
npx -y bun ${SKILL_DIR}/scripts/main.ts --model gpt-5 --prompt "Write a README" --output readme.md

# List available models
npx -y bun ${SKILL_DIR}/scripts/main.ts --list-models
```

### 常用选项

| 选项          | 描述           | 默认值       |
|--------------|-----------------|-----------|
| `--prompt <文本>`   | 用户输入的提示信息    |            | |
| `--model <id>`    | 要使用的模型       | `gpt-5-mini`    |
| `--system <文本>`   | 系统提示语       |            | |
| `--temperature <数值>` | 采样温度（0-2）     |            | |
| `--max-tokens <数值>` | 最大响应字符数    |            | |
| `--output <路径>`    | 将响应保存到文件     |            | |
| `--list-models`   | 列出可用模型       |            | |
| `--json`       | 以JSON格式输出     |            | |