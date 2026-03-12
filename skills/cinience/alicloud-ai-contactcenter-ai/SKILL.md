---
name: alicloud-ai-contactcenter-ai
description: 通过 OpenAPI/SDK 管理阿里云智能客服（ContactCenterAI）。在需要执行与智能客服资源相关的生命周期操作、配置更改、状态查询，或排查失败的智能客服 API 调用时，均可使用该工具。
version: 1.0.0
---
**类别：服务**  
**# 联络中心AI**  

您可以使用阿里云OpenAPI（RPC）以及官方SDK或OpenAPI Explorer来管理联络中心AI的相关资源。  

**工作流程**：  
1. 确定区域、资源标识符以及所需的操作。  
2. 查找可用的API列表及所需参数（详见参考资料）。  
3. 通过SDK或OpenAPI Explorer调用相应的API。  
4. 使用`describe`/`list` API验证操作结果。  

**AccessKey的使用优先级（必须遵循）**：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID`为可选的默认值；如果未设置，请根据任务需求选择最合适的区域；如果不确定，请咨询用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

**API发现**：  
- **产品代码**：`ContactCenterAI`  
- **默认API版本**：`2024-06-03`  
- 可通过OpenAPI元数据端点来列出API并获取其接口规范（详见参考资料）。  

**高频操作模式**：  
1. **资源清单/查询**：优先使用`List*` / `Describe*` API来获取当前资源信息。  
2. **资源修改/配置**：优先使用`Create*` / `Update*` / `Modify*` / `Set*` API进行资源操作。  
3. **状态检查/故障排除**：优先使用`Get*` / `Query*` / `Describe*Status` API进行诊断。  

**最小化执行步骤的快速入门指南**：  
在调用业务API之前，请先使用元数据来发现可用的API（参见**```bash
python scripts/list_openapi_meta_apis.py
```**）。  

**可选的配置覆盖方式**：  
（请根据实际需求添加相应的配置覆盖内容。）  

**脚本执行结果输出**：  
脚本会将API相关的输出文件保存在`skill/output`目录下。  

**验证要求**：  
- 命令执行成功时（返回0码），系统会在`output/alicloud-ai-contactcenter-ai/`目录下生成`validate.txt`文件。  

**输出与证据保留**：  
- 将所有生成的文件、命令输出结果以及API响应摘要保存在`output/alicloud-ai-contactcenter-ai/`目录下。  
- 确保在证据文件中记录关键参数（如区域、资源ID、时间范围等），以便后续复现操作。  

**前置条件**：  
- 在执行前，请配置具备最小权限的阿里云访问凭据。  
- 建议使用环境变量`ALICLOUD_ACCESS_KEY_ID`和`ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID`为可选参数。  
- 如果区域信息不明确，请在执行任何修改操作前咨询用户。  

**参考资料**：  
- 详细信息请参阅`references/sources.md`。