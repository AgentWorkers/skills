---
name: llmfit-advisor
description: 检测本地硬件（内存、CPU、GPU/VRAM），并推荐最适合的本地大语言模型（LLM），提供最佳的量化方案、速度估算以及模型适配度评分。
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["llmfit"] },
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "AlexsJones/llmfit",
              "bins": ["llmfit"],
              "label": "Install llmfit (brew tap AlexsJones/llmfit && brew install llmfit)",
            },
            {
              "id": "cargo",
              "kind": "node",
              "bins": ["llmfit"],
              "label": "Install llmfit (cargo install llmfit)",
            },
          ],
      },
  }
---
# llmfit-advisor

这是一个能够感知硬件配置的本地大语言模型（LLM）推荐工具。它会检测用户的系统规格（内存、CPU、GPU/显存），并推荐适合用户硬件的模型，同时提供最佳的量化设置和性能估算。

## 使用场景（触发语句）

当用户提出以下问题时，请立即使用此工具：
- “我可以运行哪些本地模型？”
- “哪些大语言模型适合我的硬件？”
- “推荐一个本地模型”
- “哪个模型最适合我的GPU？”
- “我可以在本地运行Llama 70B吗？”
- “配置本地模型”
- “设置Ollama模型”
- “哪些模型适合我的显存？”
- “帮我选择一个适合编程的本地模型”

此外，在以下情况下也请使用此工具：
- 用户需要配置`modelsProviders.ollama`或`modelsProviders.lmstudio`时
- 用户表示希望在本地运行模型，并且您需要确定哪些模型适合其硬件配置
- 需要模型推荐，并且用户具备本地推理能力（如Ollama、vLLM或LM Studio）

## 快速入门

### 检测硬件配置

```bash
llmfit --json system
```

返回一个JSON对象，其中包含CPU、RAM、GPU名称、显存信息、多GPU配置以及内存是否为统一内存（针对Apple Silicon系统）。

### 获取推荐模型

```bash
llmfit recommend --json --limit 5
```

根据综合评分（质量、速度、适配度、上下文适用性）返回排名前5的模型，并提供这些模型在当前硬件配置下的最佳量化设置。

### 按使用场景筛选模型

```bash
llmfit recommend --json --use-case coding --limit 3
llmfit recommend --json --use-case reasoning --limit 3
llmfit recommend --json --use-case chat --limit 3
```

支持的使用场景包括：`general`（通用）、`coding`（编程）、`reasoning`（推理）、`chat`（聊天）、`multimodal`（多模态）、`embedding`（嵌入）。

### 按适配度筛选模型

### 适配度等级说明

适配度等级从高到低依次为：`perfect`（完美适配）、`good`（良好适配）、`marginal`（勉强适配）。

## 理解输出结果

### 系统配置信息（JSON格式）

```json
{
  "system": {
    "cpu_name": "Apple M2 Max",
    "cpu_cores": 12,
    "total_ram_gb": 32.0,
    "available_ram_gb": 24.5,
    "has_gpu": true,
    "gpu_name": "Apple M2 Max",
    "gpu_vram_gb": 32.0,
    "gpu_count": 1,
    "backend": "Metal",
    "unified_memory": true
  }
}
```

### 模型推荐信息（JSON格式）

`models`数组中的每个模型包含以下字段：
- `name`：HuggingFace模型的ID（例如`meta-llama/Llama-3.1-8B-Instruct`）
- `provider`：模型提供者（Meta、Alibaba、Google等）
- `params_b`：模型参数的数量（以十亿为单位）
- `score`：综合评分（0–100分，分数越高表示模型性能越好）
- `score_components`：评分细分项：`quality`（质量）、`speed`（速度）、`fit`（适配度）、`context`（上下文适用性，每个项0–100分）
- `fit_level`：`Perfect`（完美适配）、`Good`（良好适配）、`Marginal`（勉强适配）或`TooTight`（适配过紧）
- `run_mode`：运行模式（`GPU`、`CPU+GPU Offload`或`CPU Only`）
- `best_quant`：适用于当前硬件的最佳量化设置（例如`Q5_K_M`、`Q4_K_M`）
- `estimated_tps`：预估的每秒处理能力（token数）
- `memory_required_gb`：该模型在当前量化设置下所需的显存/内存容量
- `memory_available_gb`：系统检测到的可用显存/内存容量
- `utilization_pct`：模型占用的可用内存比例
- `use_case`：模型适用的具体场景
- `context_length`：模型支持的最大上下文长度

### 适配度等级说明：
- **Perfect**：模型适配得非常完美，还有多余的内存空间。是理想的选择。
- **Good**：模型适配得不错，但会占用大部分可用内存。仍然可以正常使用，但性能可能稍低。
- **Marginal**：模型勉强适配。可能会运行，但性能可能较慢或上下文处理能力受限。
- **TooTight**：模型无法适配当前硬件。不建议使用。

### 运行模式说明：
- **GPU**：使用GPU进行推理。速度最快，模型权重全部加载到显存中。
- **CPU+GPU Offload**：部分计算任务在GPU上完成，其余在系统RAM中处理。速度比纯GPU模式稍慢。
- **CPU Only**：所有计算任务都在CPU上完成，使用系统RAM。速度最慢，但无需GPU。

## 使用推荐结果配置OpenClaw

获取推荐模型后，可以配置用户的本地模型提供者。

### 对于Ollama模型：

将HuggingFace模型的名称映射到对应的Ollama标签。常见映射关系如下：
- `meta-llama/Llama-3.1-8B-Instruct` → `llama3.1:8b`
- `meta-llama/Llama-3.3-70B-Instruct` → `llama3.3:70b`
- `Qwen/Qwen2.5-Coder-7B-Instruct` → `qwen2.5-coder:7b`
- `Qwen/Qwen2.5-72B-Instruct` → `qwen2.5:72b`
- `deepseek-ai/DeepSeek-Coder-V2-Lite-Instruct` → `deepseek-coder-v2:16b`
- `deepseek-ai/DeepSeek-R1-Distill-Qwen-32B` → `deepseek-r1:32b`
- `google/gemma-2-9b-it` → `gemma2:9b`
- `mistralai/Mistral-7B-Instruct-v0.3` → `mistral:7b`
- `microsoft/Phi-3-mini-4k-instruct` → `phi3:mini`
- `microsoft/Phi-4-mini-instruct` → `phi4-mini`

然后更新`openclaw.json`文件：

```json
{
  "models": {
    "providers": {
      "ollama": {
        "models": ["ollama/<ollama-tag>"]
      }
    }
  }
}
```

（具体更新内容根据实际需求填写）

### 对于vLLM/LM Studio模型：

可以直接使用HuggingFace模型的名称作为模型标识符，并加上相应的提供者前缀（`vllm/`或`lmstudio/`）。

## 工作流程示例：

当用户询问“我可以运行哪些本地模型？”时：
1. 运行`llmfit --json system`以获取系统配置概览。
2. 运行`llmfit recommend --json --limit 5`以获取推荐模型列表。
3. 向用户展示推荐结果，包括模型名称、评分和适配度等级。
4. 如果用户需要配置某个模型，将其映射到相应的Ollama/vLLM/LM Studio标签。
5. 提供帮助，指导用户更新`openclaw.json`文件以使用选定的模型。

当用户针对特定场景（如编程）请求模型推荐时：
1. 运行`llmfit recommend --json --use-case coding --limit 3`以获取针对编程场景的推荐模型。
2. 向用户展示推荐结果，并提供通过Ollama或LM Studio进行模型配置的协助。

## 注意事项：
- `llmfit`能够识别NVIDIA GPU（通过nvidia-smi）、AMD GPU（通过rocm-smi）以及Apple Silicon系统（统一内存）。
- 对于多GPU环境，系统会自动汇总所有GPU的显存资源。
- `best_quant`字段表示最佳量化设置；如果显存足够，较高的量化等级（如`Q6_K_M`、`Q8_0`）通常意味着更好的模型性能。
- 性能估算值（`estimated_tps`）仅供参考，实际性能可能因硬件和量化设置而有所不同。
- 对于适配度等级为`TooTight`的模型，切勿推荐给用户使用。