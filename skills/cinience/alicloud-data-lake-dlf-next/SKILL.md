---
name: alicloud-data-lake-dlf-next
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud Data Lake Formation (DlfNext)。该工具可用于列出资源、创建或更新配置、查询状态以及排查该产品的运行问题。
---

**类别：服务**  
# 数据湖构建（下一步）  

使用阿里巴巴云的 OpenAPI（RPC）以及官方 SDK 或 OpenAPI Explorer 来管理数据湖构建相关的资源。  

## 工作流程：  
1) 确认区域、资源标识符以及所需的操作。  
2) 查找 API 列表及所需参数（详见参考资料）。  
3) 通过 SDK 或 OpenAPI Explorer 调用相应的 API。  
4) 使用 `describe`/`list` API 验证结果。  

## AccessKey 的优先级（必须遵循）：  
1) 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - 区域策略：`ALICLOUD_REGION_ID` 是可选的默认值；如果未设置，则需根据任务需求选择最合适的区域；如果不确定，可询问用户。  
2) 共享配置文件：`~/.alibabacloud/credentials`  

## API 发现：  
- 产品代码：`DlfNext`  
- 默认 API 版本：`2025-03-10`  
- 使用 OpenAPI 元数据端点来列出 API 信息及获取其架构（详见参考资料）。  

## 高频操作模式：  
1) 清单/列出资源：优先使用 `List*`/`Describe*` API。  
2) 修改/配置资源：优先使用 `Create*`/`Update*`/`Modify*`/`Set*` API。  
3) 查看资源状态/排查问题：优先使用 `Get*`/`Query*`/`Describe*Status` API。  

## 最简快速入门步骤：  
在调用业务 API 之前，先使用元数据进行 API 的发现。  

**可选的覆盖设置：**  
（请在此处添加自定义的配置或规则。）  

该脚本会将 API 相关的清单信息保存到指定的输出目录中。  

## 输出策略：  
如果需要保存响应或生成的文件，请将它们保存在以下路径：  
`output/alicloud-data-lake-dlf-next/`  

## 参考资料：  
- 来源：`references/sources.md`