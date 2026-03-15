---
name: alicloud-ai-translation-anytrans
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud TongyiTranslate（AnyTrans）。当用户在 Alibaba Cloud 中需要执行翻译服务相关的资源操作时，可以随时使用该工具，包括列表查看、创建、更新资源、检查任务状态以及排查 AnyTrans API 工作流程中的问题。
version: 1.0.0
---
**类别：服务**  
# TongyiTranslate  

使用阿里巴巴云的OpenAPI（RPC）以及官方SDK或OpenAPI Explorer来管理TongyiTranslate的相关资源。  

**工作流程**：  
1. 确认区域、资源标识符以及所需的操作。  
2. 查找API列表及所需参数（详见参考资料）。  
3. 通过SDK或OpenAPI Explorer调用相应的API。  
4. 使用`describe`/`list` API验证操作结果。  

**AccessKey的使用优先级（必须遵循）**：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID`为可选的默认值；如果未设置，则根据任务需求选择最合适的区域；如果不确定区域，请询问用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

**API发现**：  
- **产品代码**：`AnyTrans`  
- **默认API版本**：`2025-07-07`  
- 可通过OpenAPI元数据端点来列出API并获取其架构信息（详见参考资料）。  

**高频操作模式**：  
1. **资源清单/查询**：优先使用`List*` / `Describe*` API来获取当前资源信息。  
2. **资源修改/配置**：优先使用`Create*` / `Update*` / `Modify*` / `Set*` API进行资源操作。  
3. **状态检查/故障排除**：优先使用`Get*` / `Query*` / `Describe*Status` API进行诊断。  

**最小化执行步骤的快速入门指南**：  
在调用业务API之前，先使用元数据来发现可用的API（参见**```bash
python scripts/list_openapi_meta_apis.py
```**）。  

**可选的配置覆盖方式**：  
（具体配置内容请参见**```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```**）。  

该脚本会将API相关信息写入到指定的输出目录中（`skill/output/alicloud-ai-translation-anytrans/`）。  

**输出策略**：  
如果需要保存API响应或生成的文件，请将它们保存在`output/alicloud-ai-translation-anytrans/`目录下。  

**验证要求**：  
- 命令执行成功时返回0；同时会生成`output/alicloud-ai-translation-anytrans/validate.txt`文件作为验证结果。  

**输出内容与证据**：  
- 将所有生成的文件、命令输出结果以及API响应摘要保存在`output/alicloud-ai-translation-anytrans/`目录下。  
- 确保在证据文件中包含关键参数（如区域、资源ID、时间范围等），以便后续复现操作。  

**前提条件**：  
- 在执行前，请配置好具有最小权限的阿里巴巴云访问凭据。  
- 建议使用环境变量`ALICLOUD_ACCESS_KEY_ID`和`ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID`为可选参数。  
- 如果区域信息不明确，请在执行资源修改操作前询问用户。  

**参考资料**：  
- 详细信息请参阅`references/sources.md`。