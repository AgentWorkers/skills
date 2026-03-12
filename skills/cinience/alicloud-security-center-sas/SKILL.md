---
name: alicloud-security-center-sas
description: 通过 OpenAPI/SDK 管理阿里云安全中心（SAS）。当用户需要执行安全中心资源操作、配置更新、状态查询或解决与 SAS API 或安全工作流程相关的问题时，均可使用该方式。
version: 1.0.0
---
**类别：服务**  
**# 安全中心**  

您可以使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理安全中心的资源。  

## 工作流程：  
1. 确认区域、资源标识符以及所需的操作。  
2. 查找可用的 API 列表及所需参数（详见参考资料）。  
3. 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4. 使用 `describe`/`list` API 验证操作结果。  

## AccessKey 的优先级（必须遵循）：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，请根据任务需求选择最合适的区域；如果不确定，请询问用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

## API 发现：  
- 产品代码：`Sas`  
- 默认 API 版本：`2021-01-14`  
- 可通过 OpenAPI 元数据端点来列出 API 并获取其接口规范（详见参考资料）。  

## 常见操作模式：  
1. **资源清单/查询**：优先使用 `List*`/`Describe*` API 来获取当前资源信息。  
2. **资源修改/配置**：优先使用 `Create*`/`Update*`/`Modify*`/`Set*` API 来对资源进行操作。  
3. **状态检查/故障排除**：优先使用 `Get*`/`Query*`/`Describe*Status` API 来诊断系统状态。  

## 快速入门（最小执行步骤）：  
在调用业务 API 之前，请先使用元数据来发现可用的 API（参见 **```bash
python scripts/list_openapi_meta_apis.py
```**）。  

**可选的配置覆盖选项：**  
（请根据实际需求添加相应的代码块。）  

该脚本会将 API 相关的清单信息保存到 `skill_output` 目录下。  

## 输出策略：  
如果您需要保存响应数据或生成的文件，请将它们保存到以下路径：  
`output/alicloud-security-center-sas/`  

## 验证规则：  
- 命令执行成功时（返回代码为 0），系统会生成 `output/alicloud-security-center-sas/validate.txt` 文件以供验证使用。  

**输出内容与证据：**  
- 将所有生成的文件、命令输出结果以及 API 响应摘要保存到 `output/alicloud-security-center-sas/` 目录中。  
- 确保在证据文件中记录关键参数（如区域、资源 ID、时间范围等信息），以便后续复现操作。  

**前置条件：**  
- 在执行操作前，请确保已配置最低权限的 Alibaba Cloud 凭据。  
- 建议使用环境变量 `ALICLOUD_ACCESS_KEY_ID` 和 `ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID` 为可选参数。  
- 如果区域信息不明确，请在执行修改操作前询问用户。  

**参考资料：**  
- 更多详细信息请参阅 `references/sources.md`。