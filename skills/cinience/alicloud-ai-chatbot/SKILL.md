---
name: alicloud-ai-chatbot
description: 通过 OpenAPI/SDK 管理 Alibaba Cloud 的 beebot（聊天机器人）。该接口可用于列出资源、创建或更新配置、查询状态以及解决与该产品相关的工作流程问题。
---

**类别：服务**  
**# 聊天机器人（beebot）**  

使用阿里云OpenAPI（RPC）及其官方SDK或OpenAPI Explorer来管理beebot的相关资源。  

**工作流程：**  
1) 确定区域、资源标识符以及所需执行的操作。  
2) 查找可用的API列表及所需参数（详见参考资料）。  
3) 通过SDK或OpenAPI Explorer调用相应的API。  
4) 使用`describe`/`list` API验证调用结果。  

**访问密钥的使用规则（必须遵守）：**  
1) 环境变量：`ALICLOUD_ACCESS_KEY_ID` / `ALICLOUD_ACCESS_KEY_SECRET` / `ALICLOUD_REGION_ID`  
   - `ALICLOUD_REGION_ID`为可选参数，默认值为空；若未设置，则需根据任务需求选择最合适的区域；若不确定区域，请询问用户。  
2) 共享配置文件：`~/.alibabacloud/credentials`  

**API查找方式：**  
- 产品代码：`Chatbot`  
- 默认API版本：`2022-04-08`  
- 可通过OpenAPI元数据端点来列出API及其接口规范（详见参考资料）。  

**高频操作模式：**  
1) 获取资源列表：优先使用`List*` / `Describe*` API。  
2) 修改/配置资源：优先使用`Create*` / `Update*` / `Modify*` / `Set*` API。  
3) 查看资源状态或进行故障排查：优先使用`Get*` / `Query*` / `Describe*Status` API。  

**最小化执行流程（快速入门）：**  
在调用业务API之前，先通过元数据来查找可用的API（参见**```bash
python scripts/list_openapi_meta_apis.py
```**）。  

**可选的配置覆盖方式：**  
（请根据实际需求填写相应的配置内容，参见**```bash
python scripts/list_openapi_meta_apis.py --product-code <ProductCode> --version <Version>
```**）。  

该脚本会将API相关的信息输出到指定的目录中（默认为`skill/output/alicloud-ai-chatbot/`）。  

**输出文件存放规则：**  
如果需要保存API响应或生成的文件，请将它们保存在`output/alicloud-ai-chatbot/`目录下。  

**参考资料：**  
- 资料来源：`references/sources.md`