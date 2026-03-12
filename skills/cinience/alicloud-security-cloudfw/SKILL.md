---
name: alicloud-security-cloudfw
description: 通过 OpenAPI/SDK 管理阿里云防火墙（Cloudfw）。当用户需要执行防火墙策略/资源操作、变更管理、状态检查或故障排除等任务时，均可使用该接口。
version: 1.0.0
---
**类别：服务**

# 云防火墙

使用阿里巴巴云的OpenAPI（RPC）以及官方提供的SDK或OpenAPI Explorer来管理云防火墙的相关资源。

## 工作流程

1. 确定区域、资源标识符以及所需的操作。
2. 查找可用的API列表及所需的参数（详见参考资料）。
3. 通过SDK或OpenAPI Explorer调用相应的API。
4. 使用`describe`或`list` API来验证操作结果。

## AccessKey的使用优先级（必须遵循）

1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`
   - `ALICLOUD_REGION_ID`为可选字段，默认值为当前区域。如果未设置，则需根据任务需求选择最合适的区域；如果不确定区域信息，应询问用户。
2. **共享配置文件**：`~/.alibabacloud/credentials`

## API的查找方式

- **产品代码**：`Cloudfw`
- **默认API版本**：`2017-12-07`
- 可通过OpenAPI元数据端点来列出API及其接口规范（详见参考资料）。

## 常见的操作模式

- **资源清单/查询**：优先使用`List*`或`Describe*` API来获取当前资源信息。
- **资源修改/配置**：优先使用`Create*`、`Update*`、`Modify*`或`Set*` API来进行资源操作。
- **状态检查/故障排除**：优先使用`Get*`、`Query*`或`Describe*Status` API来诊断系统状态或解决问题。

## 最简单的快速上手指南

在调用业务API之前，先使用元数据来查找可用的API（参见**```bash
python scripts/list_openapi_meta_apis.py
```**）。

**可选的配置覆盖方式：**（参见**```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```**）

该脚本会将API相关的输出文件保存到指定的输出目录中。

## 输出策略

如果需要保存API的响应结果或生成的文件，请将它们保存到以下路径：
`output/alicloud-security-cloudfw/`

## 验证规则

- 命令执行成功时（返回0代码），系统会生成`output/alicloud-security-cloudfw/validate.txt`文件作为验证依据。

## 输出内容与证据

- 将所有生成的文件、命令输出结果以及API响应摘要保存到`output/alicloud-security-cloudfw/`目录下。
- 确保在证据文件中包含关键参数（如区域、资源ID、时间范围等信息），以便后续复现操作。

## 先决条件

- 在执行操作前，请确保已配置最低权限的阿里巴巴云访问凭据。
- 建议使用环境变量`ALICLOUD_ACCESS_KEY_ID`和`ALICLOUD_ACCESS_KEY_SECRET`进行身份验证；`ALICLOUD_REGION_ID`为可选字段。
- 如果区域信息不明确，请在执行修改操作前询问用户。

## 参考资料

- 更多详细信息请参阅`references/sources.md`。