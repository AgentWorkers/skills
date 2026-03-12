---
name: alicloud-platform-docs-api-review
description: >
  **自动审查最新的阿里云产品文档和OpenAPI文档**  
  根据产品名称，自动审查这些文档的内容，然后针对存在的问题提出详细的、按优先级排序的改进建议，并提供相应的证据和评分。该功能适用于用户需要审核产品文档或API文档的质量，或希望获得可操作的文档/API优化建议时使用。
version: 1.0.0
---
# 阿里云产品文档 + API文档审核工具

当用户提供产品名称并请求进行端到端的文档/API质量审核时，请使用此工具。

## 该工具的功能

1. 从最新的OpenAPI元数据中获取产品信息。
2. 下载该产品的默认版本的API文档。
3. 从官方产品页面中提取产品帮助文档的链接。
4. 生成结构化的审核报告，内容包括：
   - 评分
   - 审核依据
   - 分类为不同优先级的建议（P0/P1/P2）

## 工作流程

运行捆绑好的脚本：

```bash
python skills/platform/docs/alicloud-platform-docs-api-review/scripts/review_product_docs_and_api.py --product "<product name or product code>"
```

示例：

```bash
python skills/platform/docs/alicloud-platform-docs-api-review/scripts/review_product_docs_and_api.py --product "ECS"
```

## 输出策略

所有生成的文件必须保存在以下目录中：

`output/alicloud-platform-docs-api-review/`

每次运行脚本后，会生成以下文件：
- `review_evidence.json`
- `review_report.md`

## 回答用户的指导原则

在回复用户时，请按照以下步骤进行：
1. 首先说明审核的产品及其版本。
2. 总结评分以及最突出的问题（前3个）。
3. 列出分类为P0/P1/P2的建议，并说明具体的处理措施。
4. 提供报告中使用的所有来源链接。

## 验证

```bash
mkdir -p output/alicloud-platform-docs-api-review
for f in skills/platform/docs/alicloud-platform-docs-api-review/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/alicloud-platform-docs-api-review/validate.txt
```

验证标准：脚本运行成功后应返回0，并生成`output/alicloud-platform-docs-api-review/validate.txt`文件。

## 输出结果与审核依据

- 将所有生成的文件、脚本输出结果以及API响应摘要保存在`output/alicloud-platform-docs-api-review/`目录下。
- 在审核依据文件中包含关键参数（区域/资源ID/时间范围），以便他人能够重现审核过程。

## 先决条件

- 在执行脚本之前，请配置具有最小权限的阿里云访问凭据。
- 建议使用环境变量：`ALICLOUD_ACCESS_KEY_ID`、`ALICLOUD_ACCESS_KEY_SECRET`（可选）以及`ALICLOUD_REGION_ID`。
- 如果区域信息不明确，请在运行脚本前先询问用户。

## 参考资料

- 审核标准：`references/review-rubric.md`