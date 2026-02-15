---
name: zotero
description: Zotero集成支持个人库和团队库。用户可以执行以下操作：  
- 搜索项目（通过标题、作者、标签、年份、全文或组合查询）；  
- 创建、更新或删除项目及其元数据；  
- 添加或编辑项目级别的注释；  
- 执行批量操作；  
- 同步附件（上传PDF文件或提供附件的URL链接）。  

当用户请求搜索Zotero中的内容、添加或修改项目/注释、上传附件或管理团队库时，该集成会自动触发相应功能。
metadata:
  clawdbot:
    primaryEnv: ZOTERO_API_KEY
    requires:
      env:
        - ZOTERO_API_KEY
        - ZOTERO_USER_ID
        - ZOTERO_GROUP_ID
    config:
      requiredEnv:
        - ZOTERO_API_KEY
      example: "config = { env = { ZOTERO_API_KEY = \"/run/agenix/zotero-api-key\"; ZOTERO_USER_ID = \"12345\"; }; };"
---

# Zotero（概述）

此技能允许使用Zotero API密钥安全、可靠地以编程方式访问用户的Zotero账户（个人库和组库）。它提供了示例脚本、一个基于pyzotero的Python客户端封装、一个命令行界面（CLI）示例，以及关于如何安全配置该技能并将其打包为AgentSkill的指导。

## 触发条件（描述中必须包含）

当用户提出如下请求时，激活此技能：“在我的Zotero中搜索‘深度学习’并按年份排序”、“向项目<id>添加注释”、“将PDF文件上传到Zotero”、“在组库<id>中创建项目”或任何明确涉及Zotero库管理的请求。

## 先决条件

- 用户需提供Zotero API密钥（开发者密钥）以及目标用户ID和/或组ID。
- **凭据的解析优先级如下**（优先使用第一个匹配项）：
  1. 命令行参数标志（例如：`--user 12345` 或 `--group 99999`）
  2. 环境变量：`ZOTERO_API_KEY`、`ZOTERO_USER_ID`、`ZOTERO_GROUP_ID`

- `ZOTERO_API_KEY`是**必需的**（必须通过环境变量设置或显式传递）。切勿将原始密钥存储在代码仓库中。
- 该技能默认使用pyzotero Python库实现；如有需要，后续也可以添加Node.js版本。
- 如果设置了环境变量，则无需用户输入，技能会使用配置好的凭据自动执行。

## 支持的功能

- 按标题、创建者/作者、标签、年份、全文或任意字段组合搜索项目；支持排序和分页。
- 使用标准的Zotero元数据字段（标题、创建者、日期、摘要注释、标签、出版物标题、DOI、ISBN等）创建新项目（如期刊文章、书籍、会议论文、学位论文等）。
- 通过发送字段级别的更新请求来修改项目元数据。
- 添加/编辑/删除项目级别的注释（Zotero项目注释）。PDF文件内的注释和高亮显示功能不在技能支持范围内（属于高级扩展功能）。
- 上传附件（本地PDF文件）或将外部URL链接的附件添加到项目中；同时记录附件的元数据（标题、内容类型）。
- 删除单个项目或执行批量操作（提供确认提示和预览功能）。
- 列出当前认证用户可使用的组和集合。
- 将操作日志记录到本地日志文件（默认情况下，日志中不包含API密钥或PDF文件的全部内容）。

## 推荐的配套资源

- **脚本：**
  - `pyzotero_client.py`：基于pyzotero的轻量级封装库，包含以下功能：`auth`、`search_items`、`create_item`、`update_item`、`add_note`、`upload_attachment`、`delete_items`、`list_groups`、`list_collections`。
  - `cli.py`：示例CLI脚本，支持`zotero search|create|update|note|upload|delete`等命令，可接受JSON格式的输入或参数。
  - `install.sh`：在虚拟环境中安装pyzotero及其依赖项，并提供设置`ZOTERO_API_KEY`的指导。

- **参考文档：**
  - `zotero-api.md`：Zotero Web API的简洁参考文档（包含使用的端点、速率限制和常见错误代码）。
  - `usage-examples.md`：将自然语言指令映射到API操作的示例。
  - `security.md`：建议将API密钥存储在环境变量或本地密钥管理工具中，切勿将密钥直接提交到代码仓库。

- **资源文件：**
  - `config.example.json`：示例配置文件（不含密钥）：`{ api_key_env: "ZOTERO_API_KEY", user_id: null, group_ids: [] }`

## 设计与实现注意事项

- 默认编程语言为Python（使用pyzotero库）。所有写入操作都需要明确的确认标志（例如`--yes`），以防止意外破坏数据。
- 批量删除操作默认为预览模式；执行前需要再次确认。
- 附件上传流程：通过`POST`请求发送到`/users/<userID>或groupID>/items/<itemKey>/children`，然后根据需要更新父子关系（详见`zotero-api.md`）。
- 错误处理：将API错误转换为易于理解的提示信息，并提供相应的恢复建议（如重试、检查权限、检查速率限制）。
- 日志记录：日志文件存储在`~/.config/zotero-skill/logs/operations.log`中；日志中不包含API密钥或PDF文件的全部内容。

## 示例自然语言指令

当环境变量`ZOTERO_API_KEY`、`ZOTERO_USER_ID`、`ZOTERO_GROUP_ID`已配置时，该技能会自动执行，无需用户额外输入：
- “在我的Zotero中搜索‘深度学习’并按年份排序”
- “向项目12345添加注释：‘扩展方法部分，包含消融研究内容’”
- “将/home/user/papers/foo.pdf作为附件上传到项目67890”
- “在组库99999中创建一篇新的期刊文章，标题为X，作者为Y，DOI为Z”

如果使用CLI时未设置`ZOTERO_USER_ID`或`ZOTERO_GROUP_ID`，可以通过参数进行覆盖：
- `python cli.py search --q "term" --user 12345`（覆盖`ZOTERO_USER_ID`环境变量）

## 安全性

- **执行环境必须设置的必要环境变量：**
  ```bash
  export ZOTERO_API_KEY="<your_api_key_here>"
  export ZOTERO_USER_ID="<your_user_id>"         # For personal library (optional if using groups)
  export ZOTERO_GROUP_ID="<your_group_id>"       # For group library (optional if using personal)
  ```

- 请勿将真实的API密钥提交到代码控制系统中。建议使用操作系统提供的密钥管理工具进行长期存储。
- 一旦环境变量设置完成，该技能将自动使用这些密钥，无需用户再次输入。

## 集成说明

- 如果需要JavaScript/Node.js实现，请创建相应的节点文件夹，并提供相应的封装代码和示例。
- **高级功能：**支持解析和同步PDF文件中的注释或高亮显示内容——这需要下载PDF文件并使用专门的解析工具，目前不在初始版本的开发范围内。