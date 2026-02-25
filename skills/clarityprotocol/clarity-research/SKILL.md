---
name: clarity-research
description: 从 Clarity Protocol 中搜索蛋白质折叠研究数据。当用户需要搜索蛋白质变体、查询蛋白质研究信息、查找蛋白质折叠结果或探索特定疾病的蛋白质数据时，可以使用此功能。主要功能包括：按疾病或蛋白质名称列出变体、获取 API 信息。
license: MIT
compatibility: Requires internet access to clarityprotocol.io. Optional CLARITY_API_KEY env var for 100 req/min (vs 10 req/min).
metadata:
  author: clarity-protocol
  version: "1.0.0"
  homepage: https://clarityprotocol.io
---
# Clarity Research Skill

您可以使用 Clarity Protocol 来搜索蛋白质折叠研究数据。该平台是一个基于社区的合作平台，支持通过 ColabFold 使用 AlphaFold2 进行蛋白质突变分析。

## 快速入门

- 列出所有可用的蛋白质变异体：
  ```bash
  ```bash
python scripts/query_variants.py
```
  ```

- 按疾病筛选：
  ```bash
  ```bash
python scripts/query_variants.py --disease Alzheimer
```
  ```

- 按蛋白质名称筛选：
  ```bash
  ```bash
python scripts/query_variants.py --protein-name MAPT
```
  ```

## 输出字段

每个变异体结果包含以下信息：
- `id`：唯一的蛋白质折叠标识符
- `protein_name`：蛋白质名称（例如：“tau”、“APP”）
- `variant`：突变类型（例如：“P301L”、“A246E”）
- `disease`：相关疾病
- `uniprot_id`：UniProt 数据库标识符
- `average_confidence`：AlphaFold 的置信度评分（0-100）
- `created_at`：蛋白质折叠结果创建的时间

## 速率限制

- **匿名用户（无 API 密钥）**：每分钟 10 次请求
- **使用 API 密钥**：每分钟 100 次请求

要使用 API 密钥，请设置 `CLARITY_API_KEY` 环境变量：
```bash
```bash
export CLARITY_API_KEY=your_key_here
python scripts/query_variants.py
```
```
您可以在 [https://clarityprotocol.io](https://clarityprotocol.io) 获取您的 API 密钥。

## 错误处理

- **404 Not Found**：端点或资源不存在。
- **429 Rate Limit**：您已超出请求速率限制。脚本会显示需要等待多久才能重新尝试。
- **500 Server Error**：API 服务器出现错误，请稍后再试。
- **Timeout**：请求耗时超过 30 秒。可能是服务器负载过重。

## 分页

结果采用分页方式显示。如果还有更多结果，API 会返回 `next_cursor` 字段。脚本会自动处理常见查询的分页逻辑。

## 使用场景

- 探索特定疾病的可用蛋白质变异体
- 查找某种蛋白质的所有已折叠突变类型
- 查看 Clarity Protocol 中可用的研究数据概览
- 获取用于进一步分析的蛋白质折叠标识符