---
name: alicloud-ai-content-aimiaobi
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud Quan Miao (AiMiaoBi)。该工具可用于列出资源、创建或更新配置、查询状态以及排查该产品的故障。
---

**类别：服务**  
**Quan Miao**

您可以使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理 Quan Miao 的资源。

**工作流程：**  
1. 确定区域、资源标识符以及所需的操作。  
2. 查找 API 列表及所需参数（请参阅相关参考资料）。  
3. 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4. 使用 `describe`/`list` API 验证操作结果。  

**AccessKey 使用优先级（必须遵循）：**  
1. 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - 区域策略：`ALICLOUD_REGION_ID` 是可选的默认值。如果未设置，请根据任务需求选择最合适的区域；如果不确定，请询问用户。  
2. 共享配置文件：`~/.alibabacloud/credentials`  

**API 发现：**  
- 产品代码：`AiMiaoBi`  
- 默认 API 版本：`2023-08-01`  
- 使用 OpenAPI 元数据端点来列出 API 信息并获取其架构（请参阅相关参考资料）。  

**高频操作模式：**  
1. 清单/列出资源：优先使用 `List*`/`Describe*` API。  
2. 修改/配置资源：优先使用 `Create*`/`Update*`/`Modify*`/`Set*` API。  
3. 查看资源状态或进行故障排除：优先使用 `Get*`/`Query*`/`Describe*Status` API。  

**最小化执行快速入门步骤：**  
在调用业务 API 之前，先使用元数据来发现可用的 API（请参见下方代码示例）。  

**可选的覆盖设置：**  
（请根据实际需求添加相应的代码示例。）  

该脚本会将 API 相关的清单信息保存到指定的输出目录中：  
`output/alicloud-ai-content-aimiaobi/`  

**输出策略：**  
如果您需要保存响应数据或生成的文件，请将它们保存到以下目录：  
`output/alicloud-ai-content-aimiaobi/`  

**参考资料：**  
- 来源：`references/sources.md`