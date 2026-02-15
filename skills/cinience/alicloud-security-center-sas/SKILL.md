---
name: alicloud-security-center-sas
description: 通过 OpenAPI/SDK 管理阿里云安全中心（SAS）。可用于列出资源、创建或更新配置、查询状态以及排查该产品的故障。
---

**类别：服务**

# 安全中心

您可以使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理安全中心的资源。

## 工作流程

1) 确认区域、资源标识符以及所需的操作。
2) 查找 API 列表及所需参数（请参阅参考资料）。
3) 使用 SDK 或 OpenAPI Explorer 调用相应的 API。
4) 通过 `describe`/`list` API 验证结果。

## AccessKey 的优先级（必须遵循）

1) 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
   - 区域策略：`ALICLOUD_REGION_ID` 是可选的默认值。如果未设置，则需根据任务需求选择最合适的区域；如果不确定，请询问用户。
2) 共享配置文件：`~/.alibabacloud/credentials`

## API 发现

- 产品代码：`Sas`
- 默认 API 版本：`2018-12-03`
- 使用 OpenAPI 元数据端点来列出 API 并获取其架构（请参阅参考资料）。

## 高频操作模式

1) 清单/列出资源：建议使用 `List*` / `Describe*` API 来获取当前资源信息。
2) 修改/配置资源：建议使用 `Create*` / `Update*` / `Modify*` / `Set*` API 来对资源进行操作。
3) 查看资源状态/排查问题：建议使用 `Get*` / `Query*` / `Describe*Status` API 来诊断问题。

## 最简单的快速入门步骤

在调用业务 API 之前，先使用元数据来发现可用的 API：

```bash
python scripts/list_openapi_meta_apis.py
```

**可选的覆盖设置：**

```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```

该脚本会将 API 相关的清单信息保存到 `skill_output` 目录下。

## 输出策略

如果您需要保存响应或生成的文件，请将它们保存到以下路径：
`output/alicloud-security-center-sas/`

## 参考资料

- 来源：`references/sources.md`