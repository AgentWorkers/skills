---
name: alicloud-database-analyticdb-mysql
description: 通过 OpenAPI/SDK 管理阿里云 AnalyticDB for MySQL (ADB)。当用户需要执行 AnalyticDB 资源的生命周期管理、配置操作、状态检查，或解决 ADB API 及集群工作流程相关问题时，均可使用这些工具。
version: 1.0.0
---
**类别：服务**  
**# AnalyticDB for MySQL**  

您可以使用阿里云OpenAPI（RPC）以及官方SDK或OpenAPI Explorer来管理AnalyticDB for MySQL的资源。  

## 工作流程：  
1. 确认区域、资源标识符以及所需的操作。  
2. 查找API列表及所需参数（详见参考资料）。  
3. 使用SDK或OpenAPI Explorer调用相应的API。  
4. 通过`describe`/`list` API验证操作结果。  

## AccessKey的使用优先级（必须遵循）：  
1. **环境变量**：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - **区域设置**：`ALICLOUD_REGION_ID`为可选的默认值；如果未设置，请根据任务需求选择最合适的区域；如有疑问，请咨询用户。  
2. **共享配置文件**：`~/.alibabacloud/credentials`  

## API发现：  
- **产品代码**：`adb`  
- **默认API版本**：`2021-12-01`  
- **使用OpenAPI元数据端点**来列出API并获取其架构信息（详见参考资料）。  

## 常见操作模式：  
1. **资源清单/查询**：优先使用`List*` / `Describe*` API来获取当前资源信息。  
2. **资源修改/配置**：优先使用`Create*` / `Update*` / `Modify*` / `Set*` API进行资源操作。  
3. **状态检查/故障排除**：优先使用`Get*` / `Query*` / `Describe*Status` API进行诊断。  

## 快速入门示例（以元数据优先的方式实现操作）：  
在调用业务API之前，请先使用元数据来发现可用的API。  
**示例代码块：**  
```bash
python scripts/list_openapi_meta_apis.py
```  

**可选的配置覆盖方式：**  
**示例代码块：**  
```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```  

该脚本会将API相关的资源信息保存到指定的输出目录中。  

## 输出策略：  
如果您需要保存API响应或生成的文件，请将它们保存在以下路径：  
`output/alicloud-database-analyticdb-mysql/`  

## 验证要求：  
- 命令执行成功时（返回0），系统会生成`output/alicloud-database-analyticdb-mysql/validate.txt`文件作为验证结果。  

## 输出内容与证据：  
- 将所有生成的文件、命令输出结果以及API响应摘要保存在`output/alicloud-database-analyticdb-mysql/`目录下。  
- 确保在证据文件中包含关键参数（如区域、资源ID、时间范围等信息），以便后续复现操作。  

## 先决条件：  
- 在执行操作前，请配置具备最低权限的阿里云访问凭据。  
- 建议使用环境变量`ALICLOUD_ACCESS_KEY_ID`和`ALICLOUD_ACCESS_KEY_SECRET`；`ALICLOUD_REGION_ID`为可选参数。  
- 如果区域信息不明确，请在执行任何资源修改操作前咨询用户。  

## 参考资料：  
- 更多详细信息请参阅`references/sources.md`。