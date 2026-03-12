---
name: alicloud-security-kms
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud Key Management Service (KMS)。当用户需要执行密钥生命周期管理、资源操作、策略/配置更改、状态检查或解决 KMS API 相关问题时，均可使用这些工具。
version: 1.0.0
---
**类别：服务**  
**# 密钥管理服务 (Key Management Service)**  

## 验证 (Validation)**  
```bash
mkdir -p output/alicloud-security-kms
python -m py_compile skills/security/key-management/alicloud-security-kms/scripts/list_openapi_meta_apis.py && echo "py_compile_ok" > output/alicloud-security-kms/validate.txt
```  

**通过标准：**  
命令执行成功（返回代码为 0），并且生成了文件 `output/alicloud-security-kms/validate.txt`。  

## 输出与证据 (Output and Evidence)**  
- 将 KMS API 的发现结果及操作结果保存到 `output/alicloud-security-kms/` 目录中。  
- 每种操作类型至少保留一个请求参数的示例。  

**使用方法：**  
使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理 KeyManagementService 的资源。  

## 工作流程 (Workflow)**  
1. 确认区域、资源标识符以及所需执行的操作。  
2. 查找 API 列表及所需的参数（详见参考资料）。  
3. 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4. 使用 `describe`/`list` API 验证操作结果。  

## **访问密钥的优先级（必须遵循） (AccessKey Priority)**  
1. **环境变量：** `ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，则根据任务需求选择最合适的区域；如果不确定，请询问用户。  
2. **共享配置文件：** `~/.alibabacloud/credentials`  

## **API 发现 (API Discovery)**  
- **产品代码：** `Kms`  
- **默认 API 版本：** `2016-01-20`  
- 使用 OpenAPI 元数据端点来列出 API 信息并获取其架构（详见参考资料）。  

## **高频操作模式 (High-Frequency Operation Patterns)**  
1. **资源清单/查询：** 建议使用 `List*`/`Describe*` API 来获取当前资源信息。  
2. **资源修改/配置：** 建议使用 `Create*`/`Update*`/`Modify*`/`Set*` API 来修改资源配置。  
3. **状态检查/故障排除：** 建议使用 `Get*`/`Query*`/`Describe*Status` API 来诊断系统状态或解决故障。  

## **最小化执行步骤的快速入门指南 (Minimal Execution Quickstart)**  
在调用业务 API 之前，先使用元数据信息进行 API 的发现：  
```bash
python scripts/list_openapi_meta_apis.py
```  

**可选的覆盖设置（Optional Overrides）：**  
```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```  

该脚本会将 API 相关的清单信息保存到指定的输出目录中。  

## **输出文件策略 (Output File Policy)**  
如果需要保存响应数据或生成的文件，请将其保存到：  
`output/alicloud-security-kms/`  

## **前置条件 (Prerequisites)**  
- 在执行前，请配置具有最小权限的 Alibaba Cloud 访问凭据。  
- 建议使用环境变量 `ALICLOUD_ACCESS_KEY_ID` 和 `ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID` 为可选参数。  
- 如果区域信息不明确，请在执行资源修改操作前询问用户。  

## **参考资料 (References)**  
- **来源：** `references/sources.md`