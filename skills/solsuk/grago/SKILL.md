# Grago

**将研究和数据获取任务委托给免费的本地大型语言模型（LLM），从而节省代币费用。同时充分利用您的本地机器。**

Grago 是一个工具，它能够连接您的 OpenClaw 代理与那些无法直接使用外部工具的本地 LLM（如 Ollama、llama.cpp 等）。它通过运行 shell 脚本来从网页、API 和本地文件中获取实时数据，然后将结果通过特定的提示语句传递给您的本地模型。

这样，您的云模型可以保持高性能运行，而本地机器则负责处理繁琐的数据处理工作，从而降低您的代币使用成本。

## ⚠️ 安全模型

**Grago 会执行 shell 命令。** 这是故意设计的——因为这是让那些没有内置工具的本地 LLM 访问外部数据的唯一方式。

**适用场景：** 可信的、单用户环境（例如您自己的 Mac Mini、VPS 或工作站）  
**不适用场景：** 多租户系统、公共 API 或不受信任的代理

如果您的 OpenClaw 代理因提示注入而受到攻击，Grago 可能会执行任意命令。这是免费使用本地计算资源的必然代价。详情请参阅仓库中的 `SECURITY.md` 文件。

## 何时使用此功能

在以下情况下使用 Grago：
- 需要获取实时数据（网页内容、API 数据、RSS 源、日志文件等）  
- 任务主要涉及研究工作，且不需要使用您的主模型  
- 希望将数据保存在本地机器上（以保护隐私）  
- 希望通过将分析任务委托给本地 LLM 来节省代币费用  

## 工作原理

1. **数据获取**：Shell 脚本用于从目标源获取数据（使用工具如 curl、jq、grep 等）。  
2. **数据分析**：获取到的数据会被传递给您的本地 Ollama 模型，并附带相应的提示语句。  
3. **结果返回**：分析后的结果会以结构化格式返回给您的 OpenClaw 代理。  

## 使用方法

```bash
# Fetch a URL and analyze locally
grago fetch "https://example.com" \
  --analyze "Summarize the key points" \
  --model gemma2

# Multi-source research from a YAML config
grago research \
  --sources sources.yaml \
  --prompt "What are the main themes across these sources?"

# Pipe any shell command into your local model
grago pipe \
  --fetch "curl -s https://api.example.com/data" \
  --transform "jq .results" \
  --analyze "Identify trends and flag outliers"
```

## 配置

配置文件：`~/.grago/config.yaml`

```yaml
default_model: gemma2        # Your preferred Ollama model
timeout: 30                  # Seconds per fetch
max_input_chars: 16000       # Input truncation limit
output_format: markdown      # markdown | json | text
```

## 系统要求

- 必须在本地安装并运行 Ollama（`install.sh` 脚本会完成安装）。  
- 至少需要一个已加载到 Ollama 中的模型（例如 gemma2、mistral、llama3 等）。  
- 系统需要支持 bash、curl 和 jq 命令。  

## 安装方法

```bash
git clone https://github.com/solsuk/grago.git
cd grago && ./install.sh
```

## 对代理用户的提示

- 为确保稳定性，建议使用 `pipe` 模式而非 `fetch --analyze` 模式（这样可以避免 Ollama 在终端界面出现卡顿现象）。  
- 默认使用的模型是 `~/.grago/config.yaml` 文件中设置的那个；您也可以通过 `--model` 参数在每次调用时进行自定义。  
- 在数据发送给本地模型之前，输入内容会被截断至 `max_input_chars` 个字符的长度。  
- 由于硬件和模型规模的不同，本地模型的响应时间可能会较慢（通常需要 5–30 秒），这是正常现象。  
- Grago 仅适用于**研究和数据获取**任务，不适用于需要您主模型进行推理的场景。