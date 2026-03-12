---
name: alicloud-platform-openapi-product-api-discovery
description: 从 Ticket System、Support & Service 以及 BSS OpenAPI 中获取并整合 Alibaba Cloud 的产品目录；提取 OpenAPI 产品的元数据（包括产品名称、版本信息等）；汇总 API 的覆盖范围，以便规划新的技能培训内容。当您需要完整的产品列表、产品与 API 的对应关系，或用于生成技能培训报告的覆盖范围/差距分析数据时，可以使用此功能。
version: 1.0.0
---
# 阿里云产品与API发现

请按照以下工作流程来收集产品信息、解析API元数据，并为技能规划生成相应的摘要。

## 工作流程

1) 从三个来源获取产品列表：

- 票务系统 (ListProducts)
- 支持与服务系统 (ListProductByGroup)
- BSS OpenAPI (QueryProductList)

运行此技能文件夹中的打包脚本：

```bash
python scripts/products_from_ticket_system.py
python scripts/products_from_support_service.py
python scripts/products_from_bssopenapi.py
```

在每个脚本中提供所需的环境变量（详见参考资料）。

2) 合并产品列表

```bash
python scripts/merge_product_sources.py
```

该脚本会生成 `output/product-scan/merged_products.json` 和 `.md` 文件。

3) 获取OpenAPI元数据及产品列表

```bash
python scripts/products_from_openapi_meta.py
```

该脚本会生成 `output/product-scan/openapi-meta/products.json` 和 `products_normalized.json` 文件。

4) 获取每个产品及其版本的OpenAPI文档

```bash
python scripts/apis_from_openapi_meta.py
```

默认情况下，这个过程可能会生成大量数据。可以使用以下参数进行测试：
- `OPENAPI_META_MAX_products=10`
- `OPENAPI_META_products=Ecs,Ons`
- `OPENAPI_META_VERSIONS=2014-05-26`

5) 将产品信息与API使用情况关联起来

```bash
python scripts/join_products_with_api_meta.py
```

6) 按类别/组别对产品进行汇总

```bash
python scripts/summarize_openapi_meta_products.py
```

6) （可选）将新发现的产品与现有的技能进行对比

```bash
python scripts/analyze_products_vs_skills.py
```

## 输出规范

所有生成的文件必须保存在 `output/` 目录下，切勿将临时文件保存在其他位置。

## 验证

```bash
mkdir -p output/alicloud-platform-openapi-product-api-discovery
for f in skills/platform/openapi/alicloud-platform-openapi-product-api-discovery/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/alicloud-platform-openapi-product-api-discovery/validate.txt
```

验证标准：命令执行成功（退出代码为0），并且 `output/alicloud-platform-openapi-product-api-discovery/validate.txt` 文件被生成。

## 输出结果与证据

- 将所有生成的文件、命令输出结果以及API响应摘要保存在 `output/alicloud-platform-openapi-product-api-discovery/` 目录下。
- 在证据文件中记录关键参数（区域、资源ID、时间范围），以便后续复现操作。

## 先决条件

- 在执行之前，请配置具有最小权限的阿里云访问凭据。
- 建议使用环境变量：`ALICLOUD_ACCESS_KEY_ID`、`ALICLOUD_ACCESS_KEY_SECRET`（可选）以及 `ALICLOUD_REGION_ID`。
- 如果区域信息不明确，请在执行任何修改操作前先询问用户。

## 参考资料

- 产品来源API的详细信息：请参阅 `references/product-sources.md`
- OpenAPI元数据端点的信息：请参阅 `references/openapi-meta.md`