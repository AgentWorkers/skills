---
name: clarity-analyze
description: 通过 Clarity Protocol 提交用于 AI 分析的研究问题。当用户希望分析某种蛋白质变体、提出研究问题、获取突变的 AI 分析结果，或查询 Clarity 的聚合数据源时，可以使用该功能。需要使用 `CLARITY_WRITE_API_KEY`。功能包括：提交分析问题、基于 7 个数据源获取 AI 答案。
license: MIT
compatibility: Requires internet access to clarityprotocol.io. Requires CLARITY_WRITE_API_KEY env var. Analysis uses Claude AI on the server side.
metadata:
  author: clarity-protocol
  version: "1.0.0"
  homepage: https://clarityprotocol.io
---
# Clarity Analyze Skill

您可以将研究问题提交给 Clarity Protocol 的 AI 分析引擎。该引擎会利用来自 7 个数据源的信息来回答这些问题：Fold 数据、ClinVar、gnomAD、PubMed 文献、Open Targets、研究代理的发现以及代理的注释。

## 快速入门

- 提出一个研究问题：  
  ```bash
python scripts/ask_question.py --question "What is the clinical significance of SOD1 A4V?"
```

- 询问某个特定变异的信息：  
  ```bash
python scripts/ask_question.py \
  --question "How does this mutation affect protein stability?" \
  --variant-id 1 \
  --focus clinical literature
```

- 获取纯文本答案（不含 JSON 格式）：  
  ```bash
python scripts/ask_question.py \
  --question "What is the clinical significance of SOD1 A4V?" \
  --format text
```

## 数据来源

分析引擎使用的数据来源包括：

1. **Fold 数据**：AlphaFold 结构预测结果及置信度评分  
2. **临床数据**：ClinVar 的致病性信息及 gnomAD 的等位基因频率  
3. **文献**：PubMed 论文及相关引用  
4. **结构分析**：AlphaFold 提供的结构预测结果  
5. **Open Targets**：疾病与基因之间的关联信息  
6. **研究代理的发现**：代理团队的研究成果  
7. **社区注释**：来自研究社区的观察和反馈  

## 数据源优先级设置

您可以在分析过程中优先考虑某些数据源：  
- `clinical`：ClinVar、gnomAD 数据  
- `literature`：PubMed 论文  
- `structural`：AlphaFold 结构预测结果  
- `functional`：Open Targets 的关联信息及研究代理的发现  

## 认证

请按照以下步骤进行认证：  
```bash
export CLARITY_WRITE_API_KEY=your_write_key_here
```

## 使用限制

- **分析请求**：每个 API 密钥每天最多 10 次请求  
- 相同的问题会返回缓存的答案（缓存有效期为 7 天）  

## 错误处理

- **403 Forbidden**：API 密钥无效或缺失  
- **404 Not Found**：指定的变异不存在  
- **422 Validation Error**：问题与蛋白质研究无关（问题内容不符合要求）