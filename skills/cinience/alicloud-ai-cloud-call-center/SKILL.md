---
name: alicloud-ai-cloud-call-center
description: 通过 OpenAPI/SDK 管理阿里云云呼叫中心（Cloud Call Center, CCC）。该接口可用于列出资源、创建或更新配置、查询状态以及排查该产品的故障。
---

**类别：服务**  
**# 云呼叫中心**  

使用阿里巴巴云OpenAPI（RPC）及其官方SDK或OpenAPI Explorer来管理云呼叫中心的资源。  

**工作流程**：  
1) 确认区域、资源标识符以及所需的操作。  
2) 查找API列表及所需参数（详见参考资料）。  
3) 通过SDK或OpenAPI Explorer调用API。  
4) 使用`describe`/`list` API验证结果。  

**访问密钥优先级（必须遵循）**：  
1) 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - 区域策略：`ALICLOUD_REGION_ID`为可选的默认值；如果未设置，则根据任务需求选择最合适的区域；如不确定，请询问用户。  
2) 共享配置文件：`~/.alibabacloud/credentials`  

**API发现**：  
- 产品代码：`CCC`  
- 默认API版本：`2020-07-01`  
- 使用OpenAPI元数据端点来列出API并获取其架构（详见参考资料）。  

**高频操作模式**：  
1) 清单/列出资源：优先使用`List*` / `Describe*` API。  
2) 修改/配置资源：优先使用`Create*` / `Update*` / `Modify*` / `Set*` API。  
3) 查看资源状态/排查故障：优先使用`Get*` / `Query*` / `Describe*Status` API。  

**最小化执行快速入门步骤**：  
在调用业务API之前，先使用元数据进行API发现：  
```bash
python scripts/list_openapi_meta_apis.py
```  

**可选的覆盖设置**：  
```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```  

该脚本会将API相关信息写入`skill_output`目录中。  

**输出策略**：  
如果需要保存响应或生成的文件，请将它们保存在：  
`output/alicloud-ai-cloud-call-center/`  

**参考资料**：  
- 来源：`references/sources.md`