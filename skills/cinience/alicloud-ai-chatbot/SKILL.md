---
name: alicloud-ai-chatbot
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud 的 beebot（聊天机器人）。当用户需要配置、查询或排查 Alibaba Cloud 聊天机器人资源的问题时，可以使用该功能，包括机器人库存管理、配置更改、状态检查以及 API 层面的诊断等操作。
version: 1.0.0
---
**类别：服务**  
**# Chatbot (beebot)**  

您可以使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理 beebot 的相关资源。  

**工作流程：**  
1. 确定区域、资源标识符以及所需的操作。  
2. 查找可用的 API 列表及所需参数（详见参考资料）。  
3. 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4. 使用 `describe`/`list` API 验证操作结果。  

**AccessKey 使用优先级（必须遵循）：**  
1. **环境变量：** `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，请根据任务需求选择最合适的区域；如果不确定，请询问用户。  
2. **共享配置文件：** `~/.alibabacloud/credentials`  

**API 发现：**  
- **产品代码：** `Chatbot`  
- **默认 API 版本：** `2022-04-08`  
- **使用 OpenAPI 元数据端点来列出 API 并获取其架构信息（详见参考资料）。  

**高频操作模式：**  
1. **资源清单/查询：** 建议使用 `List*`/`Describe*` API 来获取当前资源信息。  
2. **资源修改/配置：** 建议使用 `Create*`/`Update*`/`Modify*`/`Set*` API 来对资源进行修改或配置。  
3. **状态检查/故障排除：** 建议使用 `Get*`/`Query*`/`Describe*Status` API 来诊断系统状态或解决问题。  

**最小化执行步骤的快速入门指南：**  
在调用业务 API 之前，请先使用元数据信息进行 API 的发现和验证：  
```bash
python scripts/list_openapi_meta_apis.py
```  

**可选的覆盖设置：**  
```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```  

该脚本会将 API 相关的清单信息保存到指定的输出目录中。  

**输出策略：**  
如果您需要保存 API 的响应结果或生成的文件，请将它们保存在以下路径：  
`output/alicloud-ai-chatbot/`  

**验证要求：**  
- 命令执行成功时返回 0；同时应生成 `output/alicloud-ai-chatbot/validate.txt` 文件。  

**输出内容与证据：**  
- 将所有生成的文件、命令输出结果以及 API 响应摘要保存在 `output/alicloud-ai-chatbot/` 目录下。  
- 确保在证据文件中包含关键参数（如区域、资源 ID、时间范围等），以便后续复现操作。  

**前提条件：**  
- 在执行操作前，请先配置具有最低权限的 Alibaba Cloud 访问凭据。  
- 建议使用环境变量 `ALICLOUD_ACCESS_KEY_ID` 和 `ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID` 为可选参数。  
- 如果区域信息不明确，请在执行修改操作前询问用户。  

**参考资料：**  
- 详细信息请参阅 `references/sources.md` 文件。