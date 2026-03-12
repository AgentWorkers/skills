---
name: alicloud-ai-content-aimiaobi
description: 通过 OpenAPI/SDK 管理阿里云 Quan Miao（AiMiaoBi）。当用户需要执行与阿里云 MiaoBi 相关的操作时，可以使用该工具，包括列出资源、创建/更新配置、查询运行时状态以及诊断 API 或工作流程中的故障。
version: 1.0.0
---
**类别：服务**  
**# Quan Miao**  

您可以使用阿里巴巴云的 OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理 Quan Miao 的资源。  

**工作流程**：  
1. 确认区域、资源标识符以及所需的操作。  
2. 查找 API 列表及所需参数（详见参考资料）。  
3. 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4. 使用 `describe`/`list` API 验证操作结果。  

**AccessKey 使用优先级（必须遵循）**：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，请根据任务需求选择最合适的区域；如果不确定，请询问用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

**API 发现**：  
- 产品代码：`AiMiaoBi`  
- 默认 API 版本：`2023-08-01`  
- 可通过 OpenAPI 元数据端点来列出 API 并获取其架构信息（详见参考资料）。  

**高频操作模式**：  
1. **资源清单/查询**：优先使用 `List*`/`Describe*` API 来获取当前资源信息。  
2. **资源修改/配置**：优先使用 `Create*`/`Update*`/`Modify*`/`Set*` API 进行资源操作。  
3. **状态检查/故障排除**：优先使用 `Get*`/`Query*`/`Describe*Status` API 进行状态查询或故障诊断。  

**最小化执行步骤的快速入门指南**：  
在调用业务 API 之前，先使用元数据来发现可用的 API（参见 **```bash
python scripts/list_openapi_meta_apis.py
```**）。  

**可选的配置覆盖方式**：  
（请根据实际需求填写相应的代码块）。  

该脚本会将 API 相关的清单信息保存到指定的输出目录中（`output/alicloud-ai-content-aimiaobi/`）。  

**输出规则**：  
如果需要保存 API 响应或生成的文件，请将它们保存在以下路径：  
`output/alicloud-ai-content-aimiaobi/`  

**验证要求**：  
- 命令执行成功时返回 0；同时会生成 `output/alicloud-ai-content-aimiaobi/validate.txt` 文件以供验证使用。  

**输出与证据**：  
- 将所有生成的文件、命令输出结果以及 API 响应摘要保存在 `output/alicloud-ai-content-aimiaobi/` 目录下。  
- 确保在证据文件中包含关键参数（如区域、资源 ID、时间范围等信息），以便后续复现操作。  

**前提条件**：  
- 在执行前，请配置具有最低权限的阿里巴巴云访问凭据。  
- 建议使用环境变量 `ALICLOUD_ACCESS_KEY_ID` 和 `ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID` 为可选参数。  
- 如果区域信息不明确，请在执行修改操作前询问用户。  

**参考资料**：  
- 更多详细信息请参阅 `references/sources.md`。