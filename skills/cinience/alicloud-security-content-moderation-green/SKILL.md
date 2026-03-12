---
name: alicloud-security-content-moderation-green
description: 通过 OpenAPI/SDK 管理阿里云内容审核（绿色审核）功能。当用户需要执行内容审核资源及策略相关的操作（如列表查询、创建、更新、状态检查，以及解决审核工作流程中的故障）时，均可使用该功能。
version: 1.0.0
---
**类别：服务**  
**# 内容审核（绿色）**  

您可以使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理内容审核相关的资源。  

## 工作流程：  
1. 确认区域、资源标识符以及所需的操作。  
2. 查看 API 列表及所需参数（详见参考资料）。  
3. 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4. 使用 `describe`/`list` API 验证操作结果。  

## AccessKey 的优先级（必须遵循）：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，请根据任务需求选择最合适的区域；如有疑问，请咨询用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

## API 发现：  
- 产品代码：`Green`  
- 默认 API 版本：`2022-09-26`  
- 可通过 OpenAPI 元数据端点来列出 API 并获取其架构信息（详见参考资料）。  

## 常见操作模式：  
1. **资源清单/查询**：优先使用 `List*`/`Describe*` API 获取当前资源信息。  
2. **资源修改/配置**：优先使用 `Create*`/`Update*`/`Modify*`/`Set*` API 进行资源操作。  
3. **状态检查/故障排除**：优先使用 `Get*`/`Query*`/`Describe*Status` API 进行状态查询或故障诊断。  

## 快速入门示例（以元数据发现为先）：  
在调用业务 API 之前，请先使用元数据发现功能来获取 API 信息：  
```bash
python scripts/list_openapi_meta_apis.py
```  

**可选的配置覆盖方式：**  
```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```  

该脚本会将 API 相关的配置信息保存到 `skill_output` 目录下。  

## 输出策略：  
如果需要保存 API 响应或生成的文件，请将它们保存到以下路径：  
`output/alicloud-security-content-moderation-green/`  

## 验证要求：  
- 命令执行成功时（返回代码为 0）且 `output/alicloud-security-content-moderation-green/validate.txt` 文件生成，即表示验证通过。  

## 输出结果与证据：  
- 将所有生成的文件、命令输出结果以及 API 响应摘要保存到 `output/alicloud-security-content-moderation-green/` 目录中。  
- 确保在证据文件中包含关键参数（如区域、资源 ID、时间范围等信息），以便后续复现操作。  

## 先决条件：  
- 在执行前，请配置具有最小权限的 Alibaba Cloud 凭据。  
- 建议使用环境变量 `ALICLOUD_ACCESS_KEY_ID` 和 `ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID` 为可选参数。  
- 如果区域信息不明确，请在执行任何修改操作前咨询用户。  

## 参考资料：  
- 更多信息请参阅 `references/sources.md`。