---
name: alicloud-ai-cloud-call-center
description: 通过 OpenAPI/SDK 管理阿里云呼叫中心（Cloud Call Center, CCC）。当用户需要进行 CCC 操作（如实例/资源管理、配置更新、状态检查以及故障排除等）时，可以使用这些工具。
version: 1.0.0
---
**类别：服务**  
**# 云呼叫中心**  

您可以使用阿里巴巴云的 OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理云呼叫中心的资源。  

## 工作流程：  
1) 确定区域、资源标识符以及所需的操作。  
2) 查找可用的 API 列表及所需参数（详见参考资料）。  
3) 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4) 使用 `describe`/`list` API 验证操作结果。  

## AccessKey 的优先级（必须遵循）：  
1) 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - 区域策略：`ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，请根据任务需求选择最合适的区域；如果不确定，请询问用户。  
2) 共享配置文件：`~/.alibabacloud/credentials`  

## API 发现：  
- 产品代码：`CCC`  
- 默认 API 版本：`2020-07-01`  
- 可通过 OpenAPI 元数据端点来列出 API 信息并获取其接口规范（详见参考资料）。  

## 高频操作模式：  
1) 清单/查询：优先使用 `List*` / `Describe*` API 来获取当前资源信息。  
2) 修改/配置：优先使用 `Create*` / `Update*` / `Modify*` / `Set*` API 来对资源进行操作。  
3) 状态检查/故障排除：优先使用 `Get*` / `Query*` / `Describe*Status` API 来诊断系统状态。  

## 最小化执行步骤的快速入门指南：  
在调用业务 API 之前，请先使用元数据来发现可用的 API（参见 **```bash
python scripts/list_openapi_meta_apis.py
```**）。  

**可选的配置覆盖方式：**  
（请在此处添加自定义的配置选项或覆盖规则。）  

该脚本会将 API 相关的配置信息保存到 `skill_output` 目录下。  

## 输出策略：  
如果需要保存 API 的响应结果或生成的配置文件，请将其保存到以下路径：  
`output/alicloud-ai-cloud-call-center/`  

## 验证规则：  
- 命令执行成功时（返回状态码 0），系统会生成 `output/alicloud-ai-cloud-call-center/validate.txt` 文件作为验证结果。  

**输出内容与证据：**  
- 将所有生成的文件、命令输出结果以及 API 响应摘要保存到 `output/alicloud-ai-cloud-call-center/` 目录中。  
- 确保在证据文件中包含关键参数（如区域、资源 ID、时间范围等），以便后续复现操作。  

**前置要求：**  
- 在执行操作前，请先配置最低权限的阿里巴巴云访问凭据。  
- 建议使用环境变量 `ALICLOUD_ACCESS_KEY_ID` 和 `ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID` 为可选参数。  
- 如果区域信息不明确，请在执行任何修改操作前询问用户。  

**参考资料：**  
- 详细信息请参阅 `references/sources.md` 文件。