---
name: alicloud-data-lake-dlf
description: 通过 OpenAPI/SDK 管理阿里云数据湖 formation（DataLake）。当用户需要执行 DataLake 目录资源操作、配置更新、状态查询或排查 DataLake API 工作流程问题时，均可使用该功能。
version: 1.0.0
---
**类别：服务**

# 数据湖构建（Data Lake Formation）

使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理数据湖构建相关的资源。

## 工作流程

1) 确定区域、资源标识符以及所需执行的操作。
2) 查找可用的 API 列表及所需参数（详见参考资料）。
3) 通过 SDK 或 OpenAPI Explorer 调用相应的 API。
4) 使用 `describe`/`list` API 验证操作结果。

## AccessKey 的优先级（必须遵循）

1) 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
   - 区域设置：`ALICLOUD_REGION_ID` 是可选的默认值。如果未设置，需根据任务需求选择最合适的区域；如果不确定区域，请询问用户。
2) 共享配置文件：`~/.alibabacloud/credentials`

## API 发现

- 产品代码：`DataLake`
- 默认 API 版本：`2020-07-10`
- 可通过 OpenAPI 元数据端点来列出 API 信息并获取其接口规范（详见参考资料）。

## 常见操作模式

1) 清单/列出资源：建议使用 `List*` / `Describe*` API 来获取当前资源信息。
2) 修改/配置资源：建议使用 `Create*` / `Update*` / `Modify*` / `Set*` API 来对资源进行操作。
3) 查看资源状态/排查问题：建议使用 `Get*` / `Query*` / `Describe*Status` API 来诊断资源状态或解决问题。

## 最简快速入门步骤

在调用业务 API 之前，先使用元数据来发现可用的 API 接口：

```bash
python scripts/list_openapi_meta_apis.py
```

**可选的配置覆盖选项：**

```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```

该脚本会将 API 相关的清单信息保存到指定的输出目录中。

## 输出策略

如果需要保存 API 的响应结果或生成的文件，请将它们保存到以下路径：
`output/alicloud-data-lake-dlf/`

## 验证规则

- 命令执行成功时（返回状态码 0），系统会生成 `output/alicloud-data-lake-dlf/validate.txt` 文件以供验证使用。

## 输出内容与证据记录

- 将所有生成的文件、命令输出结果以及 API 响应摘要保存到 `output/alicloud-data-lake-dlf/` 目录下。
- 确保在证据文件中记录关键参数（如区域、资源 ID、时间范围等），以便后续复现操作。

## 先决条件

- 在执行操作前，请配置好具有最小权限的 Alibaba Cloud 访问凭据。
- 建议使用环境变量 `ALICLOUD_ACCESS_KEY_ID` 和 `ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID` 为可选参数。
- 如果区域信息不明确，请在执行任何修改操作前询问用户。

## 参考资料

- 更多详细信息请参阅：`references/sources.md`