---
name: alicloud-ai-pai-aiworkspace
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud PAI AIWorkSpace。当用户需要操作 AIWorkSpace 的资源（如工作空间/项目清单、创建/更新操作、状态查询、权限或配置问题排查，或围绕 PAI 工作空间的生命周期进行自动化处理时，均可使用该功能。
version: 1.0.0
---
**类别：服务**  
**# PAI AIWorkspace**  

使用阿里巴巴云的OpenAPI（RPC）以及官方SDK或OpenAPI Explorer来管理PAI（Platform for Artificial Intelligence）- AIWorkspace的资源。  

**工作流程**：  
1. 确认区域、资源标识符以及所需的操作。  
2. 查找API列表及所需参数（详见参考资料）。  
3. 通过SDK或OpenAPI Explorer调用API。  
4. 使用`describe`/`list` API验证结果。  

**访问密钥优先级（必须遵循）**：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - 区域策略：`ALICLOUD_REGION_ID`为可选的默认值。如果未设置，则根据任务需求选择最合适的区域；如果不确定，请询问用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

**API发现**：  
- 产品代码：`AIWorkSpace`  
- 默认API版本：`2021-02-04`  
- 使用OpenAPI元数据端点来列出API并获取其架构（详见参考资料）。  

**高频操作模式**：  
1. **资源清单/查询**：优先使用`List*` / `Describe*` API来获取当前资源信息。  
2. **资源修改/配置**：优先使用`Create*` / `Update*` / `Modify*` / `Set*` API进行资源操作。  
3. **状态检查/故障排除**：优先使用`Get*` / `Query*` / `Describe*Status` API进行诊断。  

**最小化执行快速入门步骤**：  
在调用业务API之前，先使用元数据进行API发现：  
```bash
python scripts/list_openapi_meta_apis.py
```  

**可选的覆盖配置**：  
```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```  

该脚本会将API资源信息写入`skill_output`目录下。  

**输出策略**：  
如果需要保存响应或生成的文件，请将它们保存在：  
`output/alicloud-ai-pai-aiworkspace/`  

**验证**：  
```bash
mkdir -p output/alicloud-ai-pai-aiworkspace
for f in skills/ai/platform/alicloud-ai-pai-aiworkspace/scripts/*.py; do
  python3 -m py_compile "$f"
done
echo "py_compile_ok" > output/alicloud-ai-pai-aiworkspace/validate.txt
```  
验证标准：命令执行成功（退出代码为0），并且生成`output/alicloud-ai-pai-ai workspace/validate.txt`文件。  

**输出与证据**：  
- 将生成的文件、命令输出结果以及API响应摘要保存在`output/alicloud-ai-pai-ai workspace/`目录下。  
- 在证据文件中包含关键参数（区域、资源ID、时间范围），以便后续复现操作。  

**前提条件**：  
- 在执行前配置具有最低权限的阿里巴巴云访问凭据。  
- 建议使用环境变量`ALICLOUD_ACCESS_KEY_ID`和`ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID`为可选参数。  
- 如果区域信息不明确，请在执行资源修改操作前询问用户。  

**参考资料**：  
- 来源：`references/sources.md`