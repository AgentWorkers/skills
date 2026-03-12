---
name: alicloud-ai-recommend-airec
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud AIRec (Airec)。当用户需要在 Alibaba Cloud 中执行推荐引擎相关的资源操作时（包括列出/创建/更新流程、检查状态以及排查 AIRec 的配置或运行时问题），均可使用该功能。
version: 1.0.0
---
**类别：服务**

# AIRec

您可以使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理 AIRec 的资源。

## 工作流程

1. 确认区域、资源标识符以及所需的操作。
2. 查找 API 列表和所需的参数（请参阅参考资料）。
3. 使用 SDK 或 OpenAPI Explorer 调用 API。
4. 通过 `describe`/`list` API 验证结果。

## AccessKey 的优先级（必须遵循）

1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
   - 区域策略：`ALICLOUD_REGION_ID` 是一个可选的默认值。如果未设置，请根据任务选择最合适的区域；如果不确定，请询问用户。
2. **共享配置文件**：`~/.alibabacloud/credentials`

## API 发现

- 产品代码：`Airec`
- 默认 API 版本：`2020-11-26`
- 使用 OpenAPI 元数据端点来列出 API 和获取其架构（请参阅参考资料）。

## 高频操作模式

1. **资源清单/查询**：建议使用 `List*` / `Describe*` API 来获取当前资源信息。
2. **资源修改/配置**：建议使用 `Create*` / `Update*` / `Modify*` / `Set*` API 来对资源进行修改或配置。
3. **状态检查/故障排除**：建议使用 `Get*` / `Query*` / `Describe*Status` API 来诊断系统状态或解决故障。

## 最小化可执行的快速入门流程

在调用业务 API 之前，先使用元数据来发现可用的 API（请参见 **```bash
python scripts/list_openapi_meta_apis.py
```**）。

**可选的覆盖设置：**

**```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```**

该脚本会将 API 相关的清单信息保存到 `skill_output` 目录下。

## 输出策略

如果您需要保存响应或生成的文件，请将它们保存在以下路径：
`output/alicloud-ai-recommend-airec/`

## 验证

**```bash
mkdir -p output/alicloud-ai-recommend-airec
for f in skills/ai/recommendation/alicloud-ai-recommend-airec/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/alicloud-ai-recommend-airec/validate.txt
```**

验证标准：命令执行成功（退出代码为 0），并且会生成 `output/alicloud-ai-recommend-airec/validate.txt` 文件。

## 输出与证据

- 将生成的文件、命令输出结果以及 API 响应摘要保存在 `output/alicloud-ai-recommend-airec/` 目录下。
- 在证据文件中包含关键参数（区域、资源 ID、时间范围），以便后续复现操作。

## 先决条件

- 在执行之前，请配置具有最小权限的 Alibaba Cloud 凭据。
- 建议使用环境变量 `ALICLOUD_ACCESS_KEY_ID` 和 `ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID` 为可选参数。
- 如果区域信息不明确，请在执行修改操作之前询问用户。

## 参考资料

- 来源：`references/sources.md`