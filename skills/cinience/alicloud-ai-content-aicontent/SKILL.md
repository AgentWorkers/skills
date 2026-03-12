---
name: alicloud-ai-content-aicontent
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud AIContent (AiContent)。当用户需要在 Alibaba Cloud 中生成 AI 内容或执行内容工作流相关操作时，可以使用该服务，包括列出资产、创建/更新生成配置、检查任务状态，以及排查失败的 content 作业。
version: 1.0.0
---
**类别：服务**

# AIContent

您可以使用阿里云OpenAPI（RPC）以及官方SDK或OpenAPI Explorer来管理AIContent相关的资源。

## 工作流程：

1) 确认区域、资源标识符以及所需的操作。
2) 查找API列表及所需参数（详见参考资料）。
3) 通过SDK或OpenAPI Explorer调用相应的API。
4) 使用`describe`/`list` API验证操作结果。

## AccessKey的使用规则（必须遵循）：

1) 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
   - 区域设置：`ALICLOUD_REGION_ID`为可选的默认值。如果未设置，则根据任务需求选择最合适的区域；如果不确定，请询问用户。
2) 共享配置文件：`~/.alibabacloud/credentials`

## API的查找方式：

- 产品代码：`AiContent`
- 默认API版本：`20240611`
- 可通过OpenAPI元数据端点来列出API并获取其接口规范（详见参考资料）。

## 常见的操作模式：

1) 查看资源列表：建议使用`List*` / `Describe*` API来获取当前资源信息。
2) 修改/配置资源：建议使用`Create*` / `Update*` / `Modify*` / `Set*` API来对资源进行操作。
3) 检查资源状态或排查问题：建议使用`Get*` / `Query*` / `Describe*Status` API来进行诊断。

## 快速入门步骤（建议先使用元数据查找API）：

```bash
python scripts/list_openapi_meta_apis.py
```

**可选的配置选项：**

```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```

该脚本会将API相关的信息保存到指定的输出目录中。

## 输出规则：

如果您需要保存API响应或生成的文件，请将它们保存在以下路径：
`output/alicloud-ai-content-aicontent/`

## 验证规则：

```bash
mkdir -p output/alicloud-ai-content-aicontent
for f in skills/ai/content/alicloud-ai-content-aicontent/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/alicloud-ai-content-aicontent/validate.txt
```

验证标准：命令执行成功时返回0，且会生成`output/alicloud-ai-content-aicontent/validate.txt`文件。

## 输出内容与证据：

- 将所有生成的文件、命令输出结果以及API响应摘要保存在`output/alicloud-ai-content-aicontent/`目录下。
- 确保在证据文件中包含关键参数（如区域、资源ID、时间范围等信息），以便后续复现操作。

## 先决条件：

- 在执行操作前，请配置具备最小权限的阿里云访问凭据。
- 建议使用环境变量`ALICLOUD_ACCESS_KEY_ID`和`ALICLOUD_ACCESS_KEY_SECRET`进行身份验证；`ALICLOUD_REGION_ID`为可选参数。
- 如果区域信息不明确，请在执行修改操作前询问用户。

## 参考资料：

- 更多详细信息请参考`references/sources.md`文件。