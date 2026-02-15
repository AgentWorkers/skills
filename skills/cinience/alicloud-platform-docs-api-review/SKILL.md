---
name: alicloud-platform-docs-api-review
description: **自动审查最新的阿里云产品文档和OpenAPI文档**  
根据产品名称，自动筛选并审查这些文档，然后针对每个文档提供详细的、按优先级排序的改进建议，同时附上相应的证据和评分结果。该功能适用于用户需要审核产品文档或API文档的质量，或希望获得可操作的文档/API优化建议的场景。
---

# 阿里云产品文档 + API文档审核工具

当用户提供产品名称并请求进行端到端的文档/API质量审核时，请使用此工具。

## 该工具的功能

1. 从最新的OpenAPI元数据中获取产品信息。
2. 获取该产品的默认版本的API文档。
3. 从官方产品页面中提取产品帮助文档的链接。
4. 生成结构化的审核报告，内容包括：
   - 评分
   - 审核依据
   - 按优先级排序的建议（P0/P1/P2）

## 工作流程

运行捆绑的脚本：

```bash
python skills/platform/docs/alicloud-platform-docs-api-review/scripts/review_product_docs_and_api.py --product "<产品名或产品代码>"
```

示例：

```bash
python skills/platform/docs/alicloud-platform-docs-api-review/scripts/review_product_docs_and_api.py --product "ECS"
```

## 输出规范

所有生成的文件必须保存在以下目录中：

`output/alicloud-platform-docs-api-review/`

每次运行脚本后，会生成以下文件：
- `review_evidence.json`
- `review_report.md`

## 报告指南

在回复用户时，请按照以下步骤进行：
1. 首先说明审核的产品及其版本。
2. 总结评分以及最突出的问题（前3个）。
3. 列出P0/P1/P2级别的建议及具体的处理措施。
4. 提供报告中使用的所有来源链接。

## 参考资料

- 审核标准：`references/review-rubric.md`