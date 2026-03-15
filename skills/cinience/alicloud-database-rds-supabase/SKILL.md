---
name: alicloud-database-rds-supabase
description: 通过 OpenAPI 管理 Alibaba Cloud RDS Supabase（RDS AI Service，版本：2025-05-07）。支持执行以下操作：创建实例、启动/停止/重启实例、重置密码、查询端点/身份验证/存储信息、配置身份验证/随机访问组（RAG）/SSL/IP 白名单，以及查看实例详情或相关日志记录。
version: 1.0.0
---
**类别：服务**  
**# 阿里云 RDS Supabase（RDS AI 服务，2025-05-07）**  

通过 RDS AI 服务的 OpenAPI 管理 RDS Supabase 应用程序实例及其相关配置，包括生命周期管理、身份验证、存储设置、RAG（Rapid Application Generation，快速应用程序生成）、IP 白名单和 SSL 配置。  

## 先决条件**  
- 使用具有最小权限的 RAM 用户/角色访问密钥（AccessKey），并优先使用环境变量来存储访问密钥（AK/SK）。  
- OpenAPI 支持 RPC 签名；建议使用官方 SDK 或 OpenAPI Explorer。  

## 工作流程**  
1) 确认资源类型：实例（Instance）、身份验证（Auth）、存储（Storage）、RAG、安全配置（Security）。  
2) 查阅 `references/api_overview.md` 以获取相关操作信息。  
3) 选择调用方式：SDK、OpenAPI Explorer 或自定义签名方式。  
4) 修改配置后，使用查询 API 验证状态和配置是否正确。  

## 访问密钥的优先级（必需）  
1) 环境变量（优先使用）：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，请选择最合适的区域并询问用户。  
2) 标准凭据文件：`/.alibabacloud/credentials`  

## 默认区域策略**  
- 如果未指定区域，请选择最合适的区域；如果用户不确定，请询问用户。  
- 仅在明确需要或获得用户批准的情况下执行跨区域查询（先调用 `ListRegions`，再查询每个区域）。  
- 如果用户指定了区域，则仅查询该区域。  

## 常见操作列表**  
- 实例：`CreateAppInstance` / `DeleteAppInstance` / `StartInstance` / `StopInstance` / `RestartInstance`  
- 连接性和身份验证：`DescribeInstanceEndpoints` / `DescribeInstanceAuthInfo` / `ModifyInstanceAuthConfig`  
- 存储：`DescribeInstanceStorageConfig` / `ModifyInstanceStorageConfig`  
- 安全：`ModifyInstanceIpWhitelist` / `DescribeInstanceIpWhitelist` / `ModifyInstanceSSL` / `DescribeInstanceSSL`  
- RAG：`ModifyInstanceRAGConfig` / `DescribeInstanceRAGConfig`  

## 需要澄清的问题（在不确定时询问）  
1. 目标的实例 ID 和区域是什么？  
2. 这是进行实例生命周期管理还是配置更改（身份验证/存储/RAG/IP 白名单/SSL）？  
3. 是否需要批量操作，还是先进行初始状态查询？  

## 输出策略**  
如果需要保存结果或响应，请将输出文件保存到：`output/database-rds-supabase/`  

## 验证规则**  
**通过标准：**命令执行成功时返回 0，且会生成 `output/alicloud-database-rds-supabase/validate.txt` 文件。  

## 输出和证据保存**  
- 将所有生成的艺术品（artifact）、命令输出和 API 响应摘要保存在 `output/alicloud-database-rds-supabase/` 目录下。  
- 在证据文件中包含关键参数（区域、资源 ID、时间范围），以便后续复现操作。  

## 其他注意事项**  
- 在执行操作之前，请先配置具有最小权限的阿里云凭据。  
- 建议使用环境变量 `ALICLOUD_ACCESS_KEY_ID` 和 `ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID` 为可选参数。  
- 如果区域信息不明确，请在执行任何修改操作前询问用户。  

## 工作流程（补充）  
1) 确认用户的操作意图、目标区域、相关标识符，以及操作是只读还是修改操作。  
2) 先执行一个最小的只读查询以验证连接性和权限。  
3) 使用明确的参数和有限的操作范围执行目标操作。  
4) 验证结果并保存输出文件和证据文件。  

## 参考资料**  
- API 概述和操作组：`references/api_overview.md`  
- 核心 API 参数快速参考：`references/api_reference.md`  
- 跨区域查询示例：`references/query-examples.md`  
- 官方资源列表：`references/sources.md`