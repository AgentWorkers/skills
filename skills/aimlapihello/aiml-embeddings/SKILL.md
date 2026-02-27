---
name: aimlapi-embeddings
description: 通过 AIMLAPI 生成文本嵌入。这些嵌入可用于语义搜索、聚类，或与 text-embedding-3-large 等模型结合使用，以实现高维文本表示。
env:
  - AIMLAPI_API_KEY
primaryEnv: AIMLAPI_API_KEY
---
# AIMLAPI 嵌入模型

## 概述

使用 AIMLAPI 的嵌入模型（如 `text-embedding-3-large`）将文本转换为高维数值表示（向量）。

## 快速入门

```bash
export AIMLAPI_API_KEY="sk-aimlapi-..."
python3 {baseDir}/scripts/gen_embeddings.py --input "Laura is a DJ."
```

## 任务

### 生成嵌入向量

使用 `scripts/gen_embeddings.py` 脚本获取文本的向量表示。

```bash
python3 {baseDir}/scripts/gen_embeddings.py \
  --input "Knowledge is power." \
  --model text-embedding-3-large \
  --dimensions 1024 \
  --out-dir ./out/embeddings
```

## 参考资料

- `references/endpoints.md`：API 的架构和参数详情。