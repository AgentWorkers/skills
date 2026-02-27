---
name: clarity-submit
description: 将蛋白质变异假设提交到 Clarity Protocol 进行验证和结构预测。当用户请求提交假设、提议蛋白质变异、排队进行结构预测或研究突变时，可以使用此功能。需要使用 CLARITY_WRITE_KEY 环境变量。功能包括：提交假设、检查提交状态。
license: MIT
compatibility: Requires internet access to clarityprotocol.io. Requires CLARITY_WRITE_KEY env var for write access.
metadata:
  author: clarity-protocol
  version: "1.0.0"
  homepage: https://clarityprotocol.io
---
# Clarity：提交蛋白质变异假设以进行自动化验证和ColabFold结构预测

## 快速入门

**提交一个假设：**
```bash
python scripts/submit_hypothesis.py --protein SOD1 --variant A4V --rationale "ALS-linked mutation with unknown structural impact"
```

**可选字段：**
```bash
python scripts/submit_hypothesis.py --protein MAPT --variant P301L --rationale "Tau pathology in frontotemporal dementia" --wallet "YOUR_SOLANA_WALLET"
```

**检查假设状态：**
```bash
python scripts/check_status.py --id 42
```

## 设置

设置您的写入API密钥：
```bash
export CLARITY_WRITE_KEY=your_write_key_here
```

联系Clarity Protocol团队以获取写入API密钥。

## 提交后的流程

1. **可行性验证** 会自动在UniProt、ClinVar、gnomAD和PubMed数据库中进行验证。
2. 如果验证通过，该假设将被自动排队，进入ColabFold结构预测阶段。
3. 四个AI研究代理会持续监控该变异，以发现新的相关信息。
4. 结果将在提交后返回的跟踪URL上提供。

## 必需字段

- `--protein`（必填）：蛋白质名称（例如：SOD1、MAPT、APP、SNCA）
- `--variant`（必填）：变异类型（例如：A4V、P301L、G2019S）
- `--rationale`（必填）：说明为什么该变异值得研究（至少10个字符）
- `--disease`（可选）：疾病相关领域（如果省略，系统会自动从蛋白质名称中推断）
- `--wallet`（可选）：Solana钱包地址（用于获取$FOLD奖励）

## 返回字段

- `id`：唯一的假设标识符
- `protein_name`：标准化后的蛋白质名称
- `variant_notation`：提交的变异类型
- `status`：当前状态（已提交、正在验证、已验证、已排队、预测中、已完成、被拒绝）
- `tracking_url`：在clarityprotocol.io上跟踪进度的URL

## 限制规则

- **写入（POST）**：每个API密钥每天最多10次提交。
- **读取（GET）**：每个API密钥每分钟最多100次请求。

## 大小限制

最多支持1,500个残基的蛋白质进行结构预测。超过1,500个残基的蛋白质（例如LRRK2，含有2,527个残基）将超出硬件处理能力，导致验证失败。

## 错误处理

- **403 Forbidden**：无效或缺失的写入API密钥。请设置CLARITY_WRITE_KEY环境变量。
- **422 Validation Error**：输入无效（例如蛋白质名称为空、理由太短等）。
- **429 Rate Limit**：您已超出每日10次提交的限制，请等待明天再尝试。

## 使用场景

- 通过程序自动提交变异以供研究。
- 将Clarity Protocol集成到研究流程中。
- 批量提交感兴趣的变异。
- 由代理自动生成并提交假设。