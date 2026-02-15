---
name: openkm-rest
description: 通过 REST API 进行 OpenKM 文档管理（文件夹、文档、元数据、版本控制、搜索、工作流）
metadata:
  openclaw:
    emoji: "📁"
    requires:
      bins: ["python"]
      env:
        - OPENKM_BASE_URL
        - OPENKM_USERNAME
        - OPENKM_PASSWORD
    primaryEnv: OPENKM_BASE_URL
user-invocable: true
disable-model-invocation: false
---

# OpenKM REST 功能

该功能提供了一个 **本地命令行接口（CLI）**，仅通过 REST 协议访问 OpenKM（不支持 SOAP 或 CMIS 协议）。

该功能通过调用 `openkm_cli.py` 脚本来执行相应的操作。

## 环境变量（必需）

```bash
OPENKM_BASE_URL=https://openkm.example.com   # WITHOUT /OpenKM
OPENKM_USERNAME=okm_admin
OPENKM_PASSWORD=secret
```

## 文件夹操作

### 列出文件夹内容
```bash
python3 openkm_cli.py list --folder-path /okm:root
```

### 创建文件夹结构
如果文件夹不存在，则会创建父文件夹：
```bash
python3 openkm_cli.py ensure-structure --parts Folder1 Subfolder
```

## 文档操作

### 上传文档
```bash
python3 openkm_cli.py upload --okm-path /okm:root/Folder/file.pdf --local-path /path/file.pdf
```

### 下载文档
```bash
python3 openkm_cli.py download --doc-id <uuid> --local-path /path/file.pdf
```

### 移动文档
将文档移动到另一个文件夹（使用目标文件夹的 UUID 作为路径）：
```bash
python3 openkm_cli.py move --doc-id <doc-uuid> --target-path <folder-uuid>
```

### 重命名文档
```bash
python3 openkm_cli.py rename --doc-id <uuid> --new-name new_filename.pdf
```

### 删除文档
```bash
python3 openkm_cli.py delete --doc-id <uuid>
```

## 元数据与组织结构

### 获取文档属性
显示文档的标题、描述、关键词、分类等信息：
```bash
python3 openkm_cli.py properties --doc-id <uuid>
```

### 设置标题和描述
```bash
python3 openkm_cli.py set-properties --doc-id <uuid> --title "My Title" --description "My description"
```

### 添加关键词
```bash
python3 openkm_cli.py add-keyword --doc-id <uuid> --keyword "Invoice"
```

### 删除关键词
```bash
python3 openkm_cli.py remove-keyword --doc-id <uuid> --keyword "Invoice"
```

### 添加分类
分类 ID 可以是 UUID 或路径（例如：`/okm:categories/Finance`）：
```bash
python3 openkm_cli.py add-category --doc-id <uuid> --category-id <category-uuid-or-path>
```

### 删除分类
```bash
python3 openkm_cli.py remove-category --doc-id <uuid> --category-id <category-uuid-or-path>
```

## 版本控制

### 获取版本历史记录
```bash
python3 openkm_cli.py versions --doc-id <uuid>
```

### 下载特定版本
```bash
python3 openkm_cli.py download-version --doc-id <uuid> --version 1.0 --local-path /path/file_v1.pdf
```

### 恢复文档到旧版本
将文档恢复到之前的版本：
```bash
python3 openkm_cli.py restore-version --doc-id <uuid> --version 1.0
```

## 搜索

### 按内容搜索（全文搜索）
```bash
python3 openkm_cli.py search-content --content "invoice hosting"
```

### 按文件名搜索
```bash
python3 openkm_cli.py search-name --name "hetzner"
```

### 按关键词搜索
```bash
python3 openkm_cli.py search-keywords --keywords "Invoice,Hosting"
```

### 带过滤条件的通用搜索
```bash
python3 openkm_cli.py search --content "server" --author "john.doe" --path "/okm:root"
```

## 工作流

> **注意：** 使用工作流功能需要先在 OpenKM 中配置相应的工作流。
> 如果未启用工作流功能，这些命令将返回 404 错误。

### 列出可用的工作流
```bash
python3 openkm_cli.py workflows
python3 openkm_cli.py workflows --name "approval"
```

### 启动工作流
```bash
python3 openkm_cli.py start-workflow --workflow-uuid <workflow-uuid> --doc-id <doc-uuid>
```

### 列出任务
```bash
# Tasks for a document
python3 openkm_cli.py tasks --doc-id <uuid>

# Tasks for an actor
python3 openkm_cli.py tasks --actor-id john.doe
```

### 完成任务
```bash
python3 openkm_cli.py complete-task --task-id <task-id> --transition "approve"
```

### 为任务添加注释
```bash
python3 openkm_cli.py comment-task --task-id <task-id> --message "Review complete"
```

### 将任务分配给操作者
```bash
python3 openkm_cli.py assign-task --task-id <task-id> --actor-id john.doe
```

## 注意事项

- API 要求 POST 请求的 `Content-Type` 为 `application/xml`，并且请求体中应包含路径信息。
- 作为查询参数传递的路径必须进行 URL 编码。
- `fldId`、`docId`、`dstId`、`nodeId`、`catId` 参数可以接受 UUID 或路径（例如：`/okm:root/Folder`）。
- 对于移动操作，`target-path` 应为目标文件夹的 UUID。
- 对于重命名操作，只需提供新文件名（不需要完整路径）。
- 关键词是自由形式的文本标签；分类在 OpenKM 中是预定义的。
- 版本号通常为数字格式（如 `1.0`、`1.1`、`2.0` 等）。
- 搜索结果会包含相关性评分。
- 使用工作流功能需要确保 OpenKM 中已正确配置相关的工作流。

## API 参考

该功能使用了 OpenKM 6.3 的 REST API 端点：

**文件夹：**
- `GET /folder/getChildren` - 列出文件夹内容
- `POST /folder/createSimple` - 创建文件夹

**文档：**
- `POST /document/createSimple` - 上传文档
- `GET /document/getContent` - 下载文档
- `GET /document/getProperties` - 获取文档元数据
- `PUT /document/setProperties` - 更新文档的标题/描述
- `PUT /document/move` - 移动文档
- `PUT /document/rename` - 重命名文档
- `DELETE /document/delete` - 删除文档

**版本控制：**
- `GET /document/getVersionHistory` - 获取版本历史记录
- `PUT /document/restoreVersion` - 恢复文档到指定版本
- `GET /document/getContentByVersion` - 下载特定版本的文档内容

**属性/元数据：**
- `POST /property/addKeyword` - 添加关键词
- `DELETE /property/removeKeyword` - 删除关键词
- `POST /property/addCategory` - 添加分类
- `DELETE /property/removeCategory` - 删除分类

**搜索：**
- `GET /search/find` - 带过滤条件的通用搜索
- `GET /search/ findByContent` - 全文搜索
- `GET /search/ findByName` - 按文件名搜索
- `GET /search/findByKeywords` - 按关键词搜索

**工作流：**
- `GET /workflow/getAllProcessDefinitions` - 列出所有工作流
- `GET /workflow/getAllProcessDefinitionsByName` - 按名称查找工作流
- `POST /workflow/runProcessDefinition` - 启动工作流
- `GET /workflow/findTaskInstances` - 根据文档查找任务
- `GET /workflow/findTaskInstancesByActor` - 根据操作者查找任务
- `POST /workflow/setTaskInstanceValues` - 完成任务
- `POST /workflow/addTaskInstanceComment` - 为任务添加注释
- `POST /workflow/setTaskInstanceActor` - 将任务分配给操作者