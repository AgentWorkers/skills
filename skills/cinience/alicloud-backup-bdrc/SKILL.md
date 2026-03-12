---
name: alicloud-backup-bdrc
description: 通过 OpenAPI/SDK 管理阿里云备份与灾难恢复中心（BDRC）。当用户需要执行备份/灾难恢复相关操作时，可以使用该功能，包括资源清单管理、策略/配置更改、状态检查以及故障排除等 BDRC 相关工作流程。
version: 1.0.0
---
**类别：服务**  
**# 备份与灾难恢复中心**  

您可以使用 Alibaba Cloud OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理备份与灾难恢复中心的资源。  

**工作流程：**  
1) 确认区域、资源标识符以及所需的操作。  
2) 查找可用的 API 列表及所需的参数（详见参考资料）。  
3) 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4) 使用 `describe`/`list` API 验证操作结果。  

**访问密钥优先级（必须遵循）：**  
1) 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - 区域策略：`ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，请根据任务需求选择最合适的区域；如果不确定，请询问用户。  
2) 共享配置文件：`~/.alibabacloud/credentials`  

**API 发现：**  
- 产品代码：`BDRC`  
- 默认 API 版本：`2023-08-08`  
- 使用 OpenAPI 元数据端点来列出 API 信息并获取其架构（详见参考资料）。  

**高频操作模式：**  
1) 清单/列出资源：优先使用 `List*`/`Describe*` API。  
2) 修改/配置资源：优先使用 `Create*`/`Update*`/`Modify*`/`Set*` API。  
3) 查看资源状态/排查问题：优先使用 `Get*`/`Query*`/`Describe*Status` API。  

**最小化执行步骤的快速入门指南：**  
在调用业务 API 之前，请先使用元数据进行 API 的发现。  

**可选的覆盖配置：**  
（此处可添加自定义的配置或规则。）  

该脚本会将 API 相关的清单信息保存到指定的输出目录中。  

**输出策略：**  
如果需要保存响应数据或生成的文件，请将其保存到以下路径：  
`output/alicloud-backup-bdrc/`  

**验证要求：**  
- 命令执行成功时返回 0；同时应生成 `output/alicloud-backup-bdrc/validate.txt` 文件。  

**输出结果与证据：**  
- 将所有生成的文件、命令输出结果以及 API 响应摘要保存到 `output/alicloud-backup-bdrc/` 目录中。  
- 确保在证据文件中包含关键参数（如区域、资源 ID、时间范围等信息），以便后续复现操作。  

**先决条件：**  
- 在执行操作前，请先配置最低权限级别的 Alibaba Cloud 认证信息。  
- 建议使用环境变量 `ALICLOUD_ACCESS_KEY_ID` 和 `ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID` 为可选参数。  
- 如果区域信息不明确，请在执行任何修改操作前询问用户。  

**参考资料：**  
- 更多详细信息请参阅 `references/sources.md`。