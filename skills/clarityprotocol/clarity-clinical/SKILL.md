---
name: clarity-clinical
description: 通过 Clarity 协议从 ClinVar 和 gnomAD 查询临床变异数据。当用户询问基因的 ClinVar 分类、临床意义、致病性、gnomAD 发生频率、群体遗传学信息或临床数据时，可以使用此功能。功能包括：按基因搜索临床变异、获取详细的变异注释。
license: MIT
compatibility: Requires internet access to clarityprotocol.io. Optional CLARITY_API_KEY env var for 100 req/min (vs 10 req/min).
metadata:
  author: clarity-protocol
  version: "1.0.0"
  homepage: https://clarityprotocol.io
---
# Clarity Clinical Skill

通过 Clarity Protocol 的集成数据库，可以访问来自 ClinVar 的临床变异注释以及来自 gnomAD 的群体频率数据。

## 快速入门

- 列出所有临床变异：
  ```bash
python scripts/query_clinical.py
```

- 按基因符号过滤：
  ```bash
python scripts/query_clinical.py --gene-symbol MAPT
```

- 获取特定变异的详细信息：
  ```bash
python scripts/query_clinical.py --gene MAPT --variant NM_005910.6:c.926C>T
```

- 以可读格式获取变异详细信息：
  ```bash
python scripts/query_clinical.py --gene MAPT --variant NM_005910.6:c.926C>T --format summary
```

## 临床变异字段

每个临床变异包含以下信息：

- `gene_symbol`：HGNC 基因符号
- `variant_notation`：完整的 HGVS 表示法（基于转录本）
- `clinvar_significance`：临床意义分类（例如：“致病性”、“良性”）
- `clinvar_review_status`：审查状态（例如：“提供了评估标准，有多个提交者”）
- `clinvar_last_evaluated`：最后一次 ClinVar 评估的日期
- `gnomad_af`：gnomAD 中的等位基因频率（群体患病率）
- `gnomad_ac`：gnomAD 中的等位基因计数
- `gnomad_an`：gnomAD 中的总等位基因数量
- `fetched_at`：从 ClinVar/gnomAD 获取数据的日期

## ClinVar 的临床意义分类

- **致病性（Pathogenic）**：有强有力的证据表明该变异会导致疾病
- **可能致病性（Likely pathogenic）**：有中等程度的证据表明该变异会导致疾病
- **良性（Benign）**：有强有力的证据表明该变异不会导致疾病
- **可能良性（Likely benign）**：有中等程度的证据表明该变异不会导致疾病
- **意义不确定（Uncertain significance）**：证据不足
- **解释不一致（Conflicting interpretations）**：不同提交者之间存在意见分歧

## gnomAD 的频率解释

- **af < 0.0001**：非常罕见（< 0.01%）
- **af < 0.001**：罕见（< 0.1%）
- **af < 0.01**：不常见（< 1%）
- **af >= 0.01**：常见（≥ 1%）

## 速率限制

- **匿名用户（无 API 密钥）**：每分钟 10 次请求
- **使用 API 密钥**：每分钟 100 次请求

要使用 API 密钥，请设置 `CLARITY_API_KEY` 环境变量：
  ```bash
export CLARITY_API_KEY=your_key_here
python scripts/query_clinical.py --gene-symbol MAPT
```

您可以在 [https://clarityprotocol.io](https://clarityprotocol.io) 获取您的 API 密钥。

## 错误处理

- **404 Not Found**：指定的基因/变异组合在临床数据库中不存在。
- **429 Rate Limit**：您已超出速率限制。脚本会显示需要等待的时间。
- **500 Server Error**：API 服务器出现错误。请稍后再试。
- **Timeout**：请求耗时超过 30 秒。

## 分页

临床变异列表是分页显示的。如果还有更多结果，API 会返回 `next_cursor` 字段。

## 使用场景

- 在 ClinVar 中检查某个变异是否具有致病性
- 获取某个突变的群体频率数据
- 比较同一基因中不同变异的临床意义
- 评估变异的审查状态质量
- 使用 gnomAD 过滤常见变异和罕见变异