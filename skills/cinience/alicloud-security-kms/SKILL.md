---
name: alicloud-security-kms
description: 通过 OpenAPI/SDK 管理阿里云 KeyManagementService (KMS)。该服务支持资源列表查询、配置创建/更新、状态查询以及故障排查等功能。
---

**类别：服务**  
**# 密钥管理服务**  

您可以使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理 KeyManagementService 的资源。  

**工作流程**：  
1. 确定区域、资源标识符以及所需执行的操作。  
2. 查看 API 列表及所需参数（详见参考资料）。  
3. 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4. 使用 `describe`/`list` API 验证操作结果。  

**AccessKey 的优先级（必须遵循）**：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，请根据任务需求选择最合适的区域；如果不确定，请询问用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

**API 发现**：  
- **产品代码**：`Kms`  
- **默认 API 版本**：`2016-01-20`  
- 可通过 OpenAPI 元数据端点来列出 API 并获取其架构信息（详见参考资料）。  

**高频操作模式**：  
1. **资源清单/查询**：建议使用 `List*`/`Describe*` API 来获取当前资源信息。  
2. **资源修改/配置**：建议使用 `Create*`/`Update*`/`Modify*`/`Set*` API 来对资源进行修改或配置。  
3. **状态检查/故障排除**：建议使用 `Get*`/`Query*`/`Describe*Status` API 来诊断资源状态或解决问题。  

**最小化执行快速入门步骤**：  
在调用业务 API 之前，请先使用元数据来发现可用的 API（参见 **```bash
python scripts/list_openapi_meta_apis.py
```**）。  

**可选的覆盖设置**：  
（请在此处添加自定义的配置或覆盖规则。）  

**脚本执行结果输出**：  
脚本会将 API 相关的清单信息输出到指定的目录中（例如：`output/alicloud-security-kms/`）。  

**参考资料**：  
- **来源文档**：`references/sources.md`