---
name: alicloud-data-lake-dlf
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud Data Lake Formation（DataLake）。支持执行以下操作：列出资源、创建或更新配置、查询状态以及排查该产品的运行问题。
---

**类别：服务**  
**# Data Lake Formation**  

您可以使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理 Data Lake Formation 的资源。  

## 工作流程：  
1. 确认区域、资源标识符以及所需的操作。  
2. 查找可用的 API 列表及所需参数（详见参考资料）。  
3. 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4. 使用 `describe`/`list` API 验证操作结果。  

## AccessKey 的优先级（必须遵循）：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，需根据任务需求选择最合适的区域；若不确定，请询问用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

## API 发现：  
- **产品代码**：`DataLake`  
- **默认 API 版本**：`2020-07-10`  
- 可通过 OpenAPI 元数据端点来列出 API 信息并获取其接口规范（详见参考资料）。  

## 常见操作模式：  
1. **资源清单/查询**：建议使用 `List*`/`Describe*` API 来获取当前资源信息。  
2. **资源修改/配置**：建议使用 `Create*`/`Update*`/`Modify*`/`Set*` API 来对资源进行更新或配置。  
3. **状态检查/故障排除**：建议使用 `Get*`/`Query*`/`Describe*Status` API 来诊断系统状态或解决故障。  

## 快速入门（最小执行步骤）：  
在调用业务 API 之前，建议先使用元数据来进行 API 的发现。  

**可选的覆盖配置：**  
（此处可添加自定义的配置或设置，例如代理设置等。）  

该脚本会将 API 相关的清单信息保存到 `skill/output` 目录下。  

**输出策略：**  
如果需要保存响应数据或生成的文件，请将其保存到以下路径：  
`output/alicloud-data-lake-dlf/`  

**参考资料：**  
- **来源文档**：`references/sources.md`