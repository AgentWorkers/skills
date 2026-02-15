---
name: alicloud-data-analytics-dataanalysisgbi
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud DataAnalysisGBI（DataAnalysisGBI）。该工具可用于列出资源、创建或更新配置、查询状态以及解决与该产品相关的工作流程问题。
---

**类别：服务**  
**# DataAnalysisGBI**  

您可以使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理 DataAnalysisGBI 的资源。  

**工作流程**：  
1. 确认区域、资源标识符以及所需的操作。  
2. 查找 API 列表及所需参数（详见参考资料）。  
3. 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4. 使用 `describe`/`list` API 验证结果。  

**AccessKey 使用优先级（必须遵循）**：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，则需根据任务需求选择最合适的区域；如有疑问，请咨询用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

**API 发现**：  
- **产品代码**：`DataAnalysisGBI`  
- **默认 API 版本**：`2024-08-23`  
- 可通过 OpenAPI 元数据端点来列出 API 信息并获取其架构（详见参考资料）。  

**高频操作模式**：  
1. **资源清单/查询**：建议使用 `List*`/`Describe*` API 来获取当前资源信息。  
2. **资源修改/配置**：建议使用 `Create*`/`Update*`/`Modify*`/`Set*` API 进行资源操作。  
3. **状态检查/故障排除**：建议使用 `Get*`/`Query*`/`Describe*Status` API 进行状态查询或故障诊断。  

**快速入门示例（仅使用元数据进行发现）**：  
在调用业务 API 之前，请先使用元数据来发现可用的 API（参见下方代码块）。  

**可选的配置覆盖方式**：  
（具体配置方式请参见下方代码块。）  

该脚本会将 API 相关的清单信息保存到指定的输出目录中（`output/alicloud-data-analytics-dataanalysisgbi/`）。  

**输出规则**：  
如需保存 API 响应或生成的文件，请将它们保存在以下路径下：  
`output/alicloud-data-analytics-dataanalysisgbi/`  

**参考资料**：  
- **来源**：`references/sources.md`