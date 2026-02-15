---
name: alicloud-ai-content-aicontent
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud AIContent (AiContent)。该功能可用于列出资源、创建或更新配置、查询状态以及解决与此产品相关的工作流程问题。
---

**类别：服务**  
**# AIContent**  

您可以使用阿里巴巴云的 OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理 AIContent 相关的资源。  

## 工作流程：  
1. 确认区域、资源标识符以及所需的操作。  
2. 查找可用的 API 列表及所需的参数（详见参考资料）。  
3. 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4. 使用 `describe`/`list` API 验证操作结果。  

## AccessKey 的优先级（必须遵守）：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，请根据任务需求选择最合适的区域；如果不确定，请询问用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

## API 发现：  
- **产品代码**：`AiContent`  
- **默认 API 版本**：`20240611`  
- 可通过 OpenAPI 元数据端点来列出 API 信息并获取其接口规范（详见参考资料）。  

## 高频操作模式：  
1. **资源清单/查询**：建议使用 `List*`/`Describe*` API 来获取当前资源信息。  
2. **资源修改/配置**：建议使用 `Create*`/`Update*`/`Modify*`/`Set*` API 来对资源进行修改或配置。  
3. **状态检查/故障排除**：建议使用 `Get*`/`Query*`/`Describe*Status` API 来诊断系统状态或解决故障。  

## 最简单的快速入门步骤：  
在调用业务 API 之前，请先使用元数据来发现可用的 API（参见 **```bash
python scripts/list_openapi_meta_apis.py
```**）。  

**可选的配置覆盖方式：**  
（请根据实际需求添加相应的配置代码。）  

该脚本会将 API 相关的清单信息保存到 `skill_output` 目录下。  

## 输出文件存放规则：  
如果需要保存 API 的响应结果或生成的文件，请将它们保存在以下路径：  
`output/alicloud-ai-content-aicontent/`  

**参考资料：**  
- **来源文档**：`references/sources.md`