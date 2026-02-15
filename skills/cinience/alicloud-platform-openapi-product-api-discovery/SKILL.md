---
name: alicloud-platform-openapi-product-api-discovery
description: 从 Ticket System、Support & Service 以及 BSS OpenAPI 中获取并整合阿里巴巴云的产品目录；提取 OpenAPI 产品的详细信息（包括版本、API 元数据等）；汇总 API 的覆盖范围，以便规划新的技能培训内容。当您需要完整的产品列表、产品与 API 的对应关系，或用于生成技能培训计划的覆盖范围/差距分析报告时，可以使用此功能。
---

# 阿里云产品与API信息收集

请按照以下工作流程来收集产品信息、解析API元数据，并为技能规划生成相应的摘要。

## 工作流程

1) 从三个来源获取产品列表：
   - 工单系统 (ListProducts)
   - 客户服务与支持 (ListProductByGroup)
   - BSS OpenAPI (QueryProductList)

   运行该技能文件夹中的捆绑脚本：

   ```bash
python scripts/products_from_ticket_system.py
python scripts/products_from_support_service.py
python scripts/products_from_bssopenapi.py
```

   在每个脚本中提供所需的环境变量（详见参考文档）。

2) 合并产品列表：
   ```bash
python scripts/merge_product_sources.py
```

   该脚本会将合并后的产品列表保存到 `output/product-scan/merged_products.json` 和 `.md` 文件中。

3) 获取OpenAPI元数据及产品列表：
   ```bash
python scripts/products_from_openapi_meta.py
```

   该脚本会将OpenAPI元数据及产品列表保存到 `output/product-scan/openapi-meta/products.json` 和 `products_normalized.json` 文件中。

4) 获取每个产品及其版本的OpenAPI文档：
   ```bash
python scripts/apis_from_openapi_meta.py
```

   默认情况下，该步骤可能会生成大量数据。可以通过设置过滤器来进行测试：
   - `OPENAPI_META_MAX_products=10`
   - `OPENAPI_META_products=Ecs,Ons`
   - `OPENAPI_META_VERSIONS=2014-05-26`

5) 将产品信息与对应的API数量关联起来：
   ```bash
python scripts/join_products_with_api_meta.py
```

6) 按类别或组别对产品进行汇总：
   ```bash
python scripts/summarize_openapi_meta_products.py
```

6) （可选）将收集到的产品信息与现有的技能进行对比：
   ```bash
python scripts/analyze_products_vs_skills.py
```

## 输出规范

所有生成的文件必须保存在 `output/` 目录下。请勿将临时文件保存在其他位置。

## 参考文档

- 产品来源API的详细信息：请参阅 `references/product-sources.md`
- OpenAPI元数据端点的详细信息：请参阅 `references/openapi-meta.md`