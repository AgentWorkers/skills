---
name: nlp-pipeline-builder
description: |
  Natural language processing ML pipelines for text classification, NER, sentiment analysis, text generation, and embeddings. Activates for "nlp", "text classification", "sentiment analysis", "named entity recognition", "BERT", "transformers", "text preprocessing", "tokenization", "word embeddings". Builds NLP pipelines with transformers, integrated with SpecWeave increments.
---

# NLP Pipeline Builder

## 概述

专为自然语言处理（NLP）设计的机器学习（ML）管道工具。支持文本预处理、分词、Transformer模型（如BERT、RoBERTa、GPT）的训练以及模型的部署，适用于生产环境中的NLP系统。

## 支持的NLP任务

### 1. 文本分类

```python
from specweave import NLPPipeline

# Binary or multi-class text classification
pipeline = NLPPipeline(
    task="classification",
    classes=["positive", "negative", "neutral"],
    increment="0042"
)

# Automatically configures:
# - Text preprocessing (lowercase, clean)
# - Tokenization (BERT tokenizer)
# - Model (BERT, RoBERTa, DistilBERT)
# - Fine-tuning on your data
# - Inference pipeline

pipeline.fit(train_texts, train_labels)
```

### 2. 命名实体识别（NER）

```python
# Extract entities from text
pipeline = NLPPipeline(
    task="ner",
    entities=["PERSON", "ORG", "LOC", "DATE"],
    increment="0042"
)

# Returns: [(entity_text, entity_type, start_pos, end_pos), ...]
```

### 3. 情感分析

```python
# Sentiment classification (specialized)
pipeline = NLPPipeline(
    task="sentiment",
    increment="0042"
)

# Fine-tuned for sentiment (positive/negative/neutral)
```

### 4. 文本生成

```python
# Generate text continuations
pipeline = NLPPipeline(
    task="generation",
    model="gpt2",
    increment="0042"
)

# Fine-tune on your domain-specific text
```

## NLP最佳实践

### 文本预处理

```python
from specweave import TextPreprocessor

preprocessor = TextPreprocessor(increment="0042")

# Standard preprocessing
preprocessor.add_steps([
    "lowercase",
    "remove_html",
    "remove_urls",
    "remove_emails",
    "remove_special_chars",
    "remove_extra_whitespace"
])

# Advanced preprocessing
preprocessor.add_advanced([
    "spell_correction",
    "lemmatization",
    "stopword_removal"
])
```

### 模型选择

**文本分类**：
- 小型数据集（<10K条数据）：DistilBERT（训练速度比BERT快6倍）
- 中型数据集（10K-100K条数据）：BERT-base
- 大型数据集（>100K条数据）：RoBERTa-large

**命名实体识别（NER）**：
- 通用任务：使用BERT并结合CRF（Conditional Random Field）层
- 领域特定任务：在特定领域的语料库上对BERT进行微调

**情感分析**：
- 产品评论：使用在亚马逊评论数据上微调的DistilBERT模型
- 社交媒体文本：使用在Twitter数据上微调的RoBERTa模型

### 迁移学习

```python
# Start from pre-trained language models
pipeline = NLPPipeline(task="classification")

# Option 1: Use pre-trained (no fine-tuning)
pipeline.use_pretrained("distilbert-base-uncased")

# Option 2: Fine-tune on your data
pipeline.use_pretrained_and_finetune(
    model="bert-base-uncased",
    epochs=3,
    learning_rate=2e-5
)
```

### 处理长文本

```python
# For text longer than 512 tokens
pipeline = NLPPipeline(
    task="classification",
    max_length=512,
    truncation_strategy="head_and_tail"  # Keep start + end
)

# Or use Longformer for long documents
pipeline.use_model("longformer")  # Handles 4096 tokens
```

## 与SpecWeave的集成

```python
# NLP increment structure
.specweave/increments/0042-sentiment-classifier/
├── spec.md
├── data/
│   ├── train.csv
│   ├── val.csv
│   └── test.csv
├── models/
│   ├── tokenizer/
│   ├── model-epoch-1/
│   ├── model-epoch-2/
│   └── model-epoch-3/
├── experiments/
│   ├── distilbert-baseline/
│   ├── bert-base-finetuned/
│   └── roberta-large/
└── deployment/
    ├── model.onnx
    └── inference.py
```

## 命令行工具

```bash
/ml:nlp-pipeline --task classification --model bert-base
/ml:nlp-evaluate 0042  # Evaluate on test set
/ml:nlp-deploy 0042    # Export for production
```

提供快速设置功能，帮助您使用最先进的Transformer模型构建NLP项目。