---
name: peft-fine-tuning
description: 使用 LoRA、QLoRA 及 25 种以上方法进行参数高效的 LLM（大型语言模型）微调。适用于在 GPU 内存有限的情况下微调大型模型（70 亿到 700 亿参数规模），或在训练过程中仅需调整不到 1% 的参数同时保持最小的准确率损失，同时也适用于多适配器服务场景。该工具为 HuggingFace 的官方库，已与 Transformers 生态系统深度集成。
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Fine-Tuning, PEFT, LoRA, QLoRA, Parameter-Efficient, Adapters, Low-Rank, Memory Optimization, Multi-Adapter]
dependencies: [peft>=0.13.0, transformers>=4.45.0, torch>=2.0.0, bitsandbytes>=0.43.0]
---

# PEFT（参数高效微调）

通过使用LoRA、QLoRA以及25种以上的适配器方法来微调大型语言模型（LLMs），仅训练模型参数的<1%。

## 何时使用PEFT

**在以下情况下使用PEFT/LoRA：**
- 在消费级GPU（如RTX 4090、A100）上微调7B至70B规模的模型；
- 需要训练的参数占比小于1%（仅训练6MB的适配器，而非整个模型的14GB参数）；
- 希望通过多个特定任务的适配器实现快速迭代；
- 从一个基础模型部署多个微调后的变体。

**在以下情况下使用QLoRA（PEFT + 量化）：**
- 在单块24GB的GPU上微调70B规模的模型；
- 内存是主要限制因素；
- 可以接受质量与完整微调相比有约5%的下降。

**在以下情况下使用完整的微调方法：**
- 训练小型模型（参数量小于10亿）；
- 需要最高的质量，并且有足够的计算资源；
- 领域变化较大，需要更新所有模型权重。

## 快速入门

### 安装

```bash
# Basic installation
pip install peft

# With quantization support (recommended)
pip install peft bitsandbytes

# Full stack
pip install peft transformers accelerate bitsandbytes datasets
```

### LoRA微调（标准方法）

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, TrainingArguments, Trainer
from peft import get_peft_model, LoraConfig, TaskType
from datasets import load_dataset

# Load base model
model_name = "meta-llama/Llama-3.1-8B"
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype="auto", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# LoRA configuration
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,                          # Rank (8-64, higher = more capacity)
    lora_alpha=32,                 # Scaling factor (typically 2*r)
    lora_dropout=0.05,             # Dropout for regularization
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],  # Attention layers
    bias="none"                    # Don't train biases
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# Output: trainable params: 13,631,488 || all params: 8,043,307,008 || trainable%: 0.17%

# Prepare dataset
dataset = load_dataset("databricks/databricks-dolly-15k", split="train")

def tokenize(example):
    text = f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['response']}"
    return tokenizer(text, truncation=True, max_length=512, padding="max_length")

tokenized = dataset.map(tokenize, remove_columns=dataset.column_names)

# Training
training_args = TrainingArguments(
    output_dir="./lora-llama",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_strategy="epoch"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    data_collator=lambda data: {"input_ids": torch.stack([f["input_ids"] for f in data]),
                                 "attention_mask": torch.stack([f["attention_mask"] for f in data]),
                                 "labels": torch.stack([f["input_ids"] for f in data])}
)

trainer.train()

# Save adapter only (6MB vs 16GB)
model.save_pretrained("./lora-llama-adapter")
```

### QLoRA微调（内存高效方法）

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import get_peft_model, LoraConfig, prepare_model_for_kbit_training

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # NormalFloat4 (best for LLMs)
    bnb_4bit_compute_dtype="bfloat16",   # Compute in bf16
    bnb_4bit_use_double_quant=True       # Nested quantization
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-70B",
    quantization_config=bnb_config,
    device_map="auto"
)

# Prepare for training (enables gradient checkpointing)
model = prepare_model_for_kbit_training(model)

# LoRA config for QLoRA
lora_config = LoraConfig(
    r=64,                              # Higher rank for 70B
    lora_alpha=128,
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
# 70B model now fits on single 24GB GPU!
```

## LoRA参数选择

### “Rank”（r）——参数数量与效率的平衡

| Rank | 可训练参数数量 | 内存占用 | 质量 | 适用场景 |
|------|-----------------|--------|---------|----------|
| 4     | 约300万 | 最小 | 较低 | 简单任务、原型开发 |
| **8**   | 约700万 | 较低 | 良好 | **推荐的首选等级** |
| **16**   | 约1400万 | 中等 | 更好 | **通用微调** |
| 32     | 约2700万 | 较高 | 高质量 | 复杂任务 |
| 64     | 约5400万 | 最高 | 领域适配、70B规模模型 |

### “Alpha”（lora_alpha）——缩放因子

```python
# Rule of thumb: alpha = 2 * rank
LoraConfig(r=16, lora_alpha=32)  # Standard
LoraConfig(r=16, lora_alpha=16)  # Conservative (lower learning rate effect)
LoraConfig(r=16, lora_alpha=64)  # Aggressive (higher learning rate effect)
```

### 不同架构下的目标模块

```python
# Llama / Mistral / Qwen
target_modules = ["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]

# GPT-2 / GPT-Neo
target_modules = ["c_attn", "c_proj", "c_fc"]

# Falcon
target_modules = ["query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"]

# BLOOM
target_modules = ["query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"]

# Auto-detect all linear layers
target_modules = "all-linear"  # PEFT 0.6.0+
```

## 加载和合并适配器

### 加载已训练的适配器

```python
from peft import PeftModel, AutoPeftModelForCausalLM
from transformers import AutoModelForCausalLM

# Option 1: Load with PeftModel
base_model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B")
model = PeftModel.from_pretrained(base_model, "./lora-llama-adapter")

# Option 2: Load directly (recommended)
model = AutoPeftModelForCausalLM.from_pretrained(
    "./lora-llama-adapter",
    device_map="auto"
)
```

### 将适配器合并到基础模型中

```python
# Merge for deployment (no adapter overhead)
merged_model = model.merge_and_unload()

# Save merged model
merged_model.save_pretrained("./llama-merged")
tokenizer.save_pretrained("./llama-merged")

# Push to Hub
merged_model.push_to_hub("username/llama-finetuned")
```

### 多适配器协同工作

```python
from peft import PeftModel

# Load base with first adapter
model = AutoPeftModelForCausalLM.from_pretrained("./adapter-task1")

# Load additional adapters
model.load_adapter("./adapter-task2", adapter_name="task2")
model.load_adapter("./adapter-task3", adapter_name="task3")

# Switch between adapters at runtime
model.set_adapter("task1")  # Use task1 adapter
output1 = model.generate(**inputs)

model.set_adapter("task2")  # Switch to task2
output2 = model.generate(**inputs)

# Disable adapters (use base model)
with model.disable_adapter():
    base_output = model.generate(**inputs)
```

## PEFT方法比较

| 方法 | 可训练参数比例 | 内存占用 | 训练速度 | 适用场景 |
|--------|------------|--------|-------|----------|
| **LoRA** | 0.1-1% | 低 | 快速 | 通用微调 |
| **QLoRA** | 0.1-1% | 非常低 | 中等 | 内存受限的情况 |
| AdaLoRA | 0.1-1% | 低 | 中等 | 自动选择参数等级 |
| IA3   | 0.01% | 最小 | 最快 | 少样本适应 |
| 前缀微调 | 0.1% | 低 | 中等 | 生成式任务控制 |
| 提示微调 | 0.001% | 最小 | 快速 | 简单任务适应 |
| P-Tuning v2 | 0.1% | 低 | 中等 | 自然语言理解（NLU）任务 |

### IA3（参数量极少的情况）

```python
from peft import IA3Config

ia3_config = IA3Config(
    target_modules=["q_proj", "v_proj", "k_proj", "down_proj"],
    feedforward_modules=["down_proj"]
)
model = get_peft_model(model, ia3_config)
# Trains only 0.01% of parameters!
```

### 前缀微调方法

```python
from peft import PrefixTuningConfig

prefix_config = PrefixTuningConfig(
    task_type="CAUSAL_LM",
    num_virtual_tokens=20,      # Prepended tokens
    prefix_projection=True       # Use MLP projection
)
model = get_peft_model(model, prefix_config)
```

## 集成方式

### 与TRL（SFTTrainer）集成

```python
from trl import SFTTrainer, SFTConfig
from peft import LoraConfig

lora_config = LoraConfig(r=16, lora_alpha=32, target_modules="all-linear")

trainer = SFTTrainer(
    model=model,
    args=SFTConfig(output_dir="./output", max_seq_length=512),
    train_dataset=dataset,
    peft_config=lora_config,  # Pass LoRA config directly
)
trainer.train()
```

### 与Axolotl（YAML配置文件）集成

```yaml
# axolotl config.yaml
adapter: lora
lora_r: 16
lora_alpha: 32
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - v_proj
  - k_proj
  - o_proj
lora_target_linear: true  # Target all linear layers
```

### 与vLLM（推理阶段）集成

```python
from vllm import LLM
from vllm.lora.request import LoRARequest

# Load base model with LoRA support
llm = LLM(model="meta-llama/Llama-3.1-8B", enable_lora=True)

# Serve with adapter
outputs = llm.generate(
    prompts,
    lora_request=LoRARequest("adapter1", 1, "./lora-adapter")
)
```

## 性能基准测试

### 内存使用情况（Llama 3.1 8B模型）

| 方法 | GPU内存占用 | 可训练参数数量 |
|--------|-----------|------------------|
| 完整微调 | 60GB以上 | 80亿参数（100%） |
| LoRA（r=16） | 18GB | 1400万参数（0.17%） |
| QLoRA（r=16） | 6GB | 1400万参数（0.17%） |
| IA3   | 16GB | 800万参数（0.01%） |

### 训练速度（A100 80GB GPU）

| 方法 | 每秒处理令牌数 | 与完整微调相比 |
|--------|-----------|------------|
| 完整微调 | 2,500个令牌/秒 |  |
| LoRA   | 3,200个令牌/秒 | 1.3倍 |
| QLoRA   | 2,100个令牌/秒 | 0.84倍 |

### 质量评估（MMLU基准测试）

| 模型 | 完整微调 | LoRA | QLoRA |
|-------|---------|------|-------|
| Llama 2-7B | 45.3 | 44.8 | 44.1 |
| Llama 2-13B | 54.8 | 54.2 | 53.5 |

## 常见问题

### 训练过程中出现CUDA Out of Memory（OOM）错误

```python
# Solution 1: Enable gradient checkpointing
model.gradient_checkpointing_enable()

# Solution 2: Reduce batch size + increase accumulation
TrainingArguments(
    per_device_train_batch_size=1,
    gradient_accumulation_steps=16
)

# Solution 3: Use QLoRA
from transformers import BitsAndBytesConfig
bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4")
```

### 适配器未能正确应用

```python
# Verify adapter is active
print(model.active_adapters)  # Should show adapter name

# Check trainable parameters
model.print_trainable_parameters()

# Ensure model in training mode
model.train()
```

### 模型质量下降

```python
# Increase rank
LoraConfig(r=32, lora_alpha=64)

# Target more modules
target_modules = "all-linear"

# Use more training data and epochs
TrainingArguments(num_train_epochs=5)

# Lower learning rate
TrainingArguments(learning_rate=1e-4)
```

## 最佳实践：
1. **初始时选择r=8-16**，如果质量不足再增加参数比例；
2. **初始时设置alpha=2 * rank**作为参数比例的参考值；
3. **选择目标注意力层和MLP层以实现最佳的质量与效率平衡**；
4. **启用梯度检查点功能以节省内存**；
5. **频繁保存适配器文件**（文件体积小，便于回滚）；
6. **在合并适配器之前在独立数据集上进行模型评估**；
7. **在消费级硬件上使用QLoRA来微调70B以上的模型**。

## 参考资料：
- **[高级使用方法](references/advanced-usage.md)** - DoRA、LoftQ、参数等级稳定性、自定义模块的配置；
- **[故障排除](references/troubleshooting.md)** - 常见问题、调试技巧及优化方法。

## 资源：
- **GitHub仓库**：https://github.com/huggingface/peft
- **官方文档**：https://huggingface.co/docs/peft
- **LoRA相关论文**：arXiv:2106.09685
- **QLoRA相关论文**：arXiv:2305.14314
- **相关模型**：https://huggingface.co/models?library=peft