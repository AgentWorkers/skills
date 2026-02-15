---
name: alicloud-security-content-moderation-green
description: 通过 OpenAPI/SDK 管理阿里云内容审核（绿色）功能。该功能支持资源列表查询、配置创建或更新、状态查询以及相关工作流程的故障排除。
---

**类别：服务**  
**# 内容审核（绿色）**  

使用阿里巴巴云OpenAPI（RPC）以及官方SDK或OpenAPI Explorer来管理内容审核相关的资源。  

## 工作流程：  
1) 确认地区、资源标识符以及所需的操作。  
2) 查找API列表及所需参数（详见参考资料）。  
3) 通过SDK或OpenAPI Explorer调用相应API。  
4) 使用`describe`/`list` API验证结果。  

## AccessKey的使用规则（必须遵守）：  
1) 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID`为可选的默认值；如果未设置，则需根据任务需求选择最合适的地区；若不确定，可询问用户。  
2) 共享配置文件：`~/.alibabacloud/credentials`  

## API发现：  
- 产品代码：`Green`  
- 默认API版本：`2022-03-02`  
- 可通过OpenAPI元数据端点来列出API并获取其架构信息（详见参考资料）。  

## 高频操作模式：  
1) 清单/列出资源：优先使用`List*` / `Describe*` API。  
2) 修改/配置资源：优先使用`Create*` / `Update*` / `Modify*` / `Set*` API。  
3) 查看资源状态/排查问题：优先使用`Get*` / `Query*` / `Describe*Status` API。  

## 最简快速入门步骤：  
在调用业务API之前，先使用元数据来发现可用的API接口：  
```bash
python scripts/list_openapi_meta_apis.py
```  

**可选的配置覆盖方式：**  
```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```  

该脚本会将API相关信息写入`skill_output`目录中。  

## 输出文件存放规则：  
如果需要保存响应数据或生成的文件，请将其保存在：  
`output/alicloud-security-content-moderation-green/`  

## 参考资料：  
- 来源：`references/sources.md`