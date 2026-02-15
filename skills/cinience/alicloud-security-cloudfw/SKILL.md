---
name: alicloud-security-cloudfw
description: 通过 OpenAPI/SDK 管理阿里云防火墙（Cloudfw）。支持执行以下操作：列出资源、创建或更新配置、查询状态以及排查该产品的故障。
---

**类别：服务**

# 云防火墙（Cloud Firewall）

您可以使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理云防火墙的资源。

## 工作流程：

1. 确定区域、资源标识符以及所需的操作。
2. 查找可用的 API 列表及所需参数（请参阅相关参考资料）。
3. 通过 SDK 或 OpenAPI Explorer 调用相应的 API。
4. 使用 `describe`/`list` API 验证操作结果。

## AccessKey 的优先级（必须遵循）：

1. 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
   - `ALICLOUD_REGION_ID` 是一个可选的默认值。如果未设置，请根据任务需求选择最合适的区域；如果不确定，请询问用户。
2. 共享配置文件：`~/.alibabacloud/credentials`

## API 发现：

- 产品代码：`Cloudfw`
- 默认 API 版本：`2017-12-07`
- 使用 OpenAPI 元数据端点来列出 API 信息并获取其架构（请参阅相关参考资料）。

## 常见操作模式：

1. 清单/查询：优先使用 `List*` / `Describe*` API 来获取当前资源信息。
2. 修改/配置：优先使用 `Create*` / `Update*` / `Modify*` / `Set*` API 来对资源进行操作。
3. 状态检查/故障排除：优先使用 `Get*` / `Query*` / `Describe*Status` API 来诊断系统状态。

## 最简单的快速入门步骤：

在调用业务 API 之前，请先使用元数据来发现可用的 API（请参见以下代码块）：

```bash
python scripts/list_openapi_meta_apis.py
```

**可选的覆盖设置：**

```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```

该脚本会将 API 相关的清单信息保存到指定的输出目录中。

## 输出策略：

如果您需要保存 API 的响应结果或生成的文件，请将它们保存到以下目录：
`output/alicloud-security-cloudfw/`

## 参考资料：

- 来源文档：`references/sources.md`