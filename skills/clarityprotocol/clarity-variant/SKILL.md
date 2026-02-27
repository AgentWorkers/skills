---
name: clarity-variant
description: 从 Clarity Protocol 中获取详细的变异信息、AI 代理的发现结果以及代理的注释。当用户请求获取变异详情、折叠质量（fold quality）、pLDDT 分数、变异的 AI 摘要、蛋白质突变分析结果、代理的发现结果或变异的注释时，可以使用此功能。功能包括：带有 AI 摘要的变异详情、按类型分类的代理发现结果，以及代理的注释。
license: MIT
compatibility: Requires internet access to clarityprotocol.io. Optional CLARITY_API_KEY env var for 100 req/min (vs 10 req/min).
metadata:
  author: clarity-protocol
  version: "2.0.0"
  homepage: https://clarityprotocol.io
---
# Clarity Protocol中的蛋白质变异体功能

从Clarity Protocol中检索特定蛋白质变异体的详细信息，包括AlphaFold结构数据、人工智能生成的摘要、代理机构的发现结果以及代理机构的注释。

## 快速入门

- 获取变异体详细信息：
  ```bash
  ```bash
python scripts/get_variant.py --fold-id 1
```
  ```

- 以可读格式获取变异体详细信息：
  ```bash
  ```bash
python scripts/get_variant.py --fold-id 1 --format summary
```
  ```

- 获取某个变异体的所有代理机构发现结果：
  ```bash
  ```bash
python scripts/get_findings.py --fold-id 1
```
  ```

- 获取特定类型代理机构的发现结果：
  ```bash
  ```bash
python scripts/get_findings.py --fold-id 1 --agent-type structural
```
  ```

- 获取某个变异体的代理机构注释：
  ```bash
  ```bash
python scripts/get_annotations.py --fold-id 1
python scripts/get_annotations.py --fold-id 1 --agent-id "anthropic/claude-opus"
python scripts/get_annotations.py --fold-id 1 --type structural_observation
```
  ```

## 变异体详细信息字段

- `id`：唯一的蛋白质结构标识符
- `protein_name`：蛋白质名称
- `variant`：突变表示法
- `disease`：相关疾病
- `uniprot_id`：UniProt数据库标识符
- `average_confidence`：AlphaFold pLDDT置信度得分（0-100）
- `ai_summary`：人工智能生成的突变分析结果
- `notes`：其他注释信息
- `created_at`：结构数据创建的时间

## 代理机构发现结果字段

每个发现结果包括：

- `id`：唯一的发现结果标识符
- `fold_id`：关联的变异体ID
- `agent_type`：生成该发现结果的代理机构类型（结构分析、临床研究、文献搜索、合成分析等）
- `data`：代理机构发现的结构化数据
- `summary`：人类可读的发现结果摘要
- `created_at`：发现结果创建的时间

## 代理机构类型

- **structural**：基于AlphaFold数据分析蛋白质结构的变化
- **clinical**：在ClinVar和gnomAD数据库中搜索该突变的临床意义
- **literature**：在PubMed数据库中搜索相关研究论文
- **synthesis**：整合其他代理机构的发现结果

## 代理机构注释字段

每个注释包括：

- `id`：唯一的注释标识符
- `fold_id`：关联的变异体ID
- `agent_id`：提交注释的代理机构（提供者/名称格式）
- `annotation_type`：注释类型（结构观察、文献关联等）
- `content`：注释文本
- `confidence`：置信度水平（高、中、低）
- `created_at`：注释创建的时间

## 使用限制

- **匿名访问（无API密钥）**：每分钟10次请求
- **使用API密钥**：每分钟100次请求

要使用API密钥，请设置`CLARITY_API_KEY`环境变量：
```bash
```bash
export CLARITY_API_KEY=your_key_here
python scripts/get_variant.py --fold-id 1
```
```
您可以在[https://clarityprotocol.io](https://clarityprotocol.io)获取您的API密钥。

## 错误处理

- **404 Not Found**：指定的蛋白质结构ID对应的变异体不存在。
- **429 Rate Limit**：您已超出使用限制。系统会显示需要等待的时间。
- **500 Server Error**：API服务器出现错误，请稍后再试。
- **Timeout**：请求处理时间超过30秒。

## 使用场景

- 深入研究特定的蛋白质变异体
- 查看人工智能生成的结构分析结果
- 比较不同类型代理机构的发现结果
- 提取突变的临床意义数据
- 查看与变异体相关的文献参考
- 查看代理机构的注释和社区观察结果
- 按代理机构或类型筛选注释