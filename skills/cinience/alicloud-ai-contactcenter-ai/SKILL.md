---
name: alicloud-ai-contactcenter-ai
description: 通过 OpenAPI/SDK 管理阿里云 Contact Center AI（ContactCenterAI）。可用于列出资源、创建或更新配置、查询状态以及排查该产品的故障。
---

**类别：服务**  
**# 联络中心AI**  

您可以使用阿里云OpenAPI（RPC）以及官方SDK或OpenAPI Explorer来管理联络中心AI的相关资源。  

## 工作流程：  
1. 确定区域、资源标识符以及所需执行的操作。  
2. 查找可用的API列表及所需的参数（详见参考资料）。  
3. 通过SDK或OpenAPI Explorer调用相应的API。  
4. 使用`describe`/`list` API验证调用结果。  

## AccessKey的使用优先级（必须遵循）：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID`为可选的默认值；如果未设置，请根据任务需求选择最合适的区域；如果不确定，请咨询用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

## API的查找方式：  
- **产品代码**：`ContactCenterAI`  
- **默认API版本**：`2024-06-03`  
- 可通过OpenAPI元数据端点来列出API及其接口规范（详见参考资料）。  

## 常见的操作模式：  
1. **资源查询/列表**：建议使用`List*` / `Describe*` API来获取当前资源信息。  
2. **资源修改/配置**：建议使用`Create*` / `Update*` / `Modify*` / `Set*` API来进行资源操作。  
3. **状态检查/故障排除**：建议使用`Get*` / `Query*` / `Describe*Status` API来进行系统状态查询或故障诊断。  

## 最简化的快速入门步骤：  
在调用业务API之前，请先使用元数据查询API的相关信息：  
```bash
python scripts/list_openapi_meta_apis.py
```  

**可选的配置覆盖方式：**  
```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```  

该脚本会将API相关的信息（如资源列表等）保存到指定的输出目录中（例如：`output/alicloud-ai-contactcenter-ai/`）。  

## 输出文件存放规则：  
如果需要保存API的响应结果或生成的文件，请将它们保存在以下目录中：  
`output/alicloud-ai-contactcenter-ai/`  

**参考资料：**  
- **来源文档**：`references/sources.md`