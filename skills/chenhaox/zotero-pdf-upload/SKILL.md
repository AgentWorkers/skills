---
name: zotero-pdf-upload
description: 上传 PDF 文件并管理 Zotero 网络图书馆中的项目。支持个人图书馆和小组图书馆。当用户需要向 Zotero 添加论文或 PDF 文件、整理收藏夹，或通过 API 管理他们的 Zotero 图书馆时，可以使用该工具。
primaryEnv: ZOTERO_API_KEY
requiredConfig: config.json
---# zotero-pdf-upload  
此技能用于需要确保安全性、明确性及可重用性的Zotero工作流程。  

## 首次设置检查（在任何Zotero操作之前执行）  

在运行任何命令之前，请检查`config.json`文件是否存在于技能根目录中。  

**如果`config.json`文件不存在**，请停止操作并通知用户：  
> 该技能尚未配置完成，您需要先进行设置。  
> **所需准备的内容：**  
> 1. **Zotero API密钥** — 在 [zotero.org/settings/keys](https://www.zotero.org/settings/keys) 创建一个API密钥：  
>   - 进入“设置” → “安全” → “创建新的私钥”  
>   - 启用“允许访问图书馆”、“允许访问笔记”以及“允许写入权限”  
>   - 如果使用组库，请将“默认组权限”设置为“读/写”  
>   - 点击“保存密钥”并复制生成的密钥  
> 2. **Zotero库URL** — 在浏览器中打开您的库并复制URL：  
>   - 个人库：`https://www.zotero.org/<your-username>/library`  
>   - 组库：`https://www.zotero.org/groups/<group-id>/<group-name>/library`  
> **从技能目录中运行以下命令进行设置：**  
> ```bash  
> python scripts/setup.py "<YOUR_LIBRARY_URL>" "<YOUR_API_KEY>"  
> ```  
在`config.json`文件创建完成之前，请勿继续任何Zotero操作。  

## 包含的资源  
- `scripts/zotero_workflow.py`：用于解析、检查、匹配和创建Zotero资源的命令行入口点。  
- `scripts/zotero_client.py`：Zotero API客户端，负责处理URL解析、加载秘钥、匹配集合、创建项目以及上传PDF文件。  
- `tests/smoke_test_zotero_pdf_upload.py`：用于测试无网络环境下的功能是否正常运行的测试脚本。  
- `references/config.example.json`：运行时配置模板（统一使用`url`字段来存储组库和个人库的URL）。  
- `references/item.example.json`：项目元数据示例文件。  
- `references/approval-flow.md`：包含审批流程及数据写入安全策略的文档。  

## 必须遵守的操作规则  
1. 首先执行只读操作（`parse-url`、`list-collections`、`choose-collection`）。  
2. 如果无法匹配到合适的集合，返回`pending-new-collection-approval`状态。  
3. 只有在明确用户操作的情况下才能创建集合（使用`create-collection --approve-create`命令）。  
4. 只有在明确用户操作的情况下才能创建项目（使用`create-item --approve-write`命令）。  
5. 仅当用户明确请求且配置允许时，才上传PDF文件。  

## 秘钥管理  
Zotero API密钥的加载顺序如下（优先级从高到低）：  
1. 环境变量：`zotero.apiKeyEnv`（默认值为`ZOTERO_API_KEY`）  
2. 秘钥文件路径：`zotero.apiKeyPath`  
3. 内联配置值：`zotero.apiKey`（最低优先级）  

**注意**：切勿在输出中显示完整的API密钥。  

**安全提示**：在解析个人库URL时（基于用户名，而非数字ID），该技能会调用`GET https://api.zotero.org/keys/{apiKey}`来获取用户ID。这是Zotero的标准API模式；密钥会显示在URL中，也可能出现在服务器访问日志中。因此，请使用权限最低的密钥，并优先使用环境变量或配置文件来存储密钥。  

## 核心命令  
从技能目录中运行以下命令：  

### 1) 解析Zotero URL  
```bash  
python scripts/zotero_workflow.py parse-url --url "https://www.zotero.org/groups/6320165/my-group/library"  
```  
**个人库URL示例：**  
```bash  
python scripts/zotero_workflow.py parse-url --url "https://www.zotero.org/myusername/library"  
```  

### 2) 列出集合（仅限读取）  
```bash  
python scripts/zotero_workflow.py list-collections --config ./tmp.config.json  
```  

**可选的匹配条件：**  
```bash  
python scripts/zotero_workflow.py list-collections \
  --config ./tmp.config.json \
  --title "Practical Alignment Evaluation for LLM Agents" \
  --tags alignment llm  
```  

### 3) 选择集合（仅限读取，不自动创建）  
```bash  
python scripts/zotero_workflow.py choose-collection \
  --config ./tmp.config.json \
  --item-json references/item.example.json  
```  
- 如果找到匹配的集合，状态为`matched-existing-collection`；  
- 否则，状态为`pending-new-collection-approval`，并提示用户选择集合名称。  

### 4) 显式创建集合（需要用户确认）  
```bash  
python scripts/zotero_workflow.py create-collection \
  --config ./tmp.config.json \
  --name "LLM Safety" \
  --approve-create  
```  

### 5) 显式创建项目元数据（需要用户确认）  
```bash  
python scripts/zotero_workflow.py create-item \
  --config ./tmp.config.json \
  --item-json references/item.example.json \
  --auto-match-collection \
  --approve-write  
```  

**可选的PDF附件上传：**  
```bash  
python scripts/zotero_workflow.py create-item \
  --config ./tmp.config.json \
  --item-json references/item.example.json \
  --collection-key ABCD1234 \
  --attach-pdf /path/to/paper.pdf \
  --approve-write  
```  

## 必须执行的审批步骤  
- 未经用户明确确认，不得执行任何写入操作。  
- 在匹配过程中，不得自动创建缺失的集合。  
- 如果匹配结果的置信度较低，应停止操作并询问用户是否需要创建或选择集合。  
- 如果PDF附件上传失败，必须记录错误信息，不得忽略该错误。  

## 测试脚本  
```bash  
python tests/smoke_test_zotero_pdf_upload.py  
```