---
name: alicloud-ai-recommend-airec
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud AIRec (Airec)。该工具可用于列出资源、创建或更新配置、查询状态以及排查该产品的运行问题。
---

**类别：服务**  
# AIRec  

使用阿里云OpenAPI（RPC）及其官方SDK或OpenAPI Explorer来管理AIRec的相关资源。  

## 工作流程：  
1) 确定区域、资源标识符以及所需的操作。  
2) 查找可用的API列表及所需参数（详见参考资料）。  
3) 通过SDK或OpenAPI Explorer调用相应的API。  
4) 使用`describe`/`list` API验证操作结果。  

## AccessKey的使用优先级（必须遵循）：  
1) 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID`为可选的默认值；如果未设置，则需根据任务需求选择最合适的区域；如有疑问，请咨询用户。  
2) 共享配置文件：`~/.alibabacloud/credentials`  

## API发现：  
- 产品代码：`Airec`  
- 默认API版本：`2020-11-26`  
- 可通过OpenAPI元数据端点来列出API及其架构信息（详见参考资料）。  

## 常见操作模式：  
1) 列出资源：优先使用`List*` / `Describe*` API来获取当前资源信息。  
2) 修改配置：优先使用`Create*` / `Update*` / `Modify*` / `Set*` API来对资源进行更新。  
3) 查看状态/排查问题：优先使用`Get*` / `Query*` / `Describe*Status` API来进行诊断。  

## 最简单的快速入门步骤：  
在调用业务API之前，先使用元数据来发现可用的API（参见**```bash
python scripts/list_openapi_meta_apis.py
```**）。  

**可选的配置覆盖方式：**  
（请根据实际需求填写相应的代码块。）  

该脚本会将API相关信息保存在`skill_output`目录下。  

## 输出文件存放规则：  
如果需要保存API响应或生成的文件，请将它们保存在以下路径：  
`output/alicloud-ai-recommend-airec/`  

## 参考资料：  
- 来源文件：`references/sources.md`