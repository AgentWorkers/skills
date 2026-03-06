---
name: gws-drive
version: 1.0.0
description: "**Google Drive：管理文件、文件夹和共享驱动器。**"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws drive --help"
---
# drive (v3)

> **前提条件：** 请阅读 `../gws-shared/SKILL.md` 以了解认证、全局参数和安全规则。如果文件缺失，请运行 `gws generate-skills` 来生成它。

```bash
gws drive <resource> <method> [flags]
```

## 帮助命令

| 命令 | 描述 |
|---------|-------------|
| [`+upload`](../gws-drive-upload/SKILL.md) | 上传文件并自动添加元数据 |

## API 资源

### about

  - `get` — 获取有关用户、用户的 Drive 以及系统功能的信息。更多信息，请参阅 [返回用户信息](https://developers.google.com/workspace/drive/api/guides/user-info)。**要求：** 必须设置 `fields` 参数。要返回所需的特定字段，请参阅 [返回特定字段](https://developers.google.com/workspace/drive/api/guides/fields-parameter)。

### accessproposals

  - `get` — 通过 ID 获取访问请求。更多信息，请参阅 [管理待处理的访问请求](https://developers.google.com/workspace/drive/api/guides/pending-access)。
  - `list` — 列出文件的访问请求。更多信息，请参阅 [管理待处理的访问请求](https://developers.google.com/workspace/drive/api/guides/pending-access)。**注意：** 只有审批者才能列出文件的访问请求。如果用户不是审批者，将返回 403 错误。
  - `resolve` — 批准或拒绝访问请求。更多信息，请参阅 [管理待处理的访问请求](https://developers.google.com/workspace/drive/api/guides/pending-access)。

### approvals

  - `get` — 通过 ID 获取批准信息。
  - `list` — 列出文件的批准记录。

### apps

  - `get` — 获取特定应用。更多信息，请参阅 [返回用户信息](https://developers.google.com/workspace/drive/api/guides/user-info)。
  - `list` — 列出用户安装的应用。更多信息，请参阅 [返回用户信息](https://developers.google.com/workspace/drive/api/guides/user-info)。

### changes

  - `getStartPageToken` — 获取用于列出未来更改的起始页面令牌。更多信息，请参阅 [检索更改](https://developers.google.com/workspace/drive/api/guides/manage-changes)。
  - `list` — 列出用户或共享 Drive 的更改记录。更多信息，请参阅 [检索更改](https://developers.google.com/workspace/drive/api/guides/manage-changes)。
  - `watch` — 订阅用户的更改通知。更多信息，请参阅 [资源更改通知](https://developers.google.com/workspace/drive/api/guides/push)。

### channels

  - `stop` — 停止通过此渠道接收资源更改通知。更多信息，请参阅 [资源更改通知](https://developers.google.com/workspace/drive/api/guides/push)。

### comments

  - `create` — 在文件上创建评论。更多信息，请参阅 [管理评论和回复](https://developers.google.com/workspace/drive/api/guides/manage-comments)。**要求：** 必须设置 `fields` 参数。要返回所需的特定字段，请参阅 [返回特定字段](https://developers.google.com/workspace/drive/api/guides/fields-parameter)。
  - `delete` — 删除评论。更多信息，请参阅 [管理评论和回复](https://developers.google.com/workspace/drive/api/guides/manage-comments)。
  - `get` — 通过 ID 获取评论信息。更多信息，请参阅 [管理评论和回复](https://developers.google.com/workspace/drive/api/guides/manage-comments)。**要求：** 必须设置 `fields` 参数。要返回所需的特定字段，请参阅 [返回特定字段](https://developers.google.com/workspace/drive/api/guides/fields-parameter)。
  - `list` — 列出文件的评论。更多信息，请参阅 [管理评论和回复](https://developers.google.com/workspace/drive/api/guides/manage-comments)。**要求：** 必须设置 `fields` 参数。要返回所需的特定字段，请参阅 [返回特定字段](https://developers.google.com/workspace/drive/api/guides/fields-parameter)。
  - `update` — 使用补丁语义更新评论。更多信息，请参阅 [管理评论和回复](https://developers.google.com/workspace/drive/api/guides/manage-comments)。**要求：** 必须设置 `fields` 参数。要返回所需的特定字段，请参阅 [返回特定字段](https://developers.google.com/workspace/drive/api/guides/fields-parameter)。

### drives

  - `create` — 创建共享 Drive。更多信息，请参阅 [管理共享 Drive](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives)。
  - `get` — 通过 ID 获取共享 Drive 的元数据。更多信息，请参阅 [管理共享 Drive](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives)。
  - `hide` — 从默认视图中隐藏共享 Drive。更多信息，请参阅 [管理共享 Drive](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives)。
  - `list` — 列出用户的共享 Drive。此方法接受 `q` 参数，该参数是一个或多个搜索词的组合。更多信息，请参阅 [搜索共享 Drive](/workspace/drive/api/guides/search-shareddrives) 文档。
  - `unhide` — 将共享 Drive 恢复到默认视图。更多信息，请参阅 [管理共享 Drive](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives)。
  - `update` — 更新共享 Drive 的元数据。更多信息，请参阅 [管理共享 Drive](https://developers.google.com/workspace/drive/api/guides/manage-shareddrives)。

### files

  - `copy` — 创建文件的副本，并应用任何请求的更新（使用补丁语义）。更多信息，请参阅 [创建和管理文件](https://developers.google.com/workspace/drive/api/guides/create-file)。
  - `create` — 创建文件。更多信息，请参阅 [创建和管理文件](/workspace/drive/api/guides/create-file)。此方法支持 `*/upload*` URI，并接受具有以下特性的上传媒体：  
    - **最大文件大小：** 5,120 GB  
    - **接受的媒体 MIME 类型：** `*/*`（请指定有效的 MIME 类型，而不是字面值 `*/*`。字面值 `*/*` 仅表示可以上传任何有效的 MIME 类型。）
  - `download` — 下载文件的内容。更多信息，请参阅 [下载和导出文件](https://developers.google.com/workspace/drive/api/guides/manage-downloads)。操作在文件创建后的 24 小时内有效。
  - `export` — 将 Google Workspace 文档导出为请求的 MIME 类型，并返回导出的字节内容。更多信息，请参阅 [下载和导出文件](https://developers.google.com/workspace/drive/api/guides/manage-downloads)。请注意，导出的内容大小限制为 10 MB。
  - `generateIds` — 生成一组文件 ID，可以在创建或复制请求中使用。更多信息，请参阅 [创建和管理文件](https://developers.google.com/workspace/drive/api/guides/create-file)。
  - `get` — 通过 ID 获取文件的元数据或内容。更多信息，请参阅 [搜索文件和文件夹](/workspace/drive/api/guides/search-files)。如果提供 `alt=media` 参数，响应中将包含文件内容。使用 `alt=media` 下载内容仅适用于存储在 Drive 中的文件。要下载 Google Docs、Sheets 和 Slides，请使用 [`files.export`](/workspace/drive/api/reference/rest/v3/files/export)。
  - `list` — 列出用户的文件。更多信息，请参阅 [搜索文件和文件夹](/workspace/drive/api/guides/search-files)。此方法接受 `q` 参数，该参数是一个或多个搜索词的组合。默认情况下，此方法会返回 *所有* 文件，包括已删除的文件。如果不想在列表中显示已删除的文件，请使用 `trashed=false` 查询参数来排除已删除的文件。
  - `listLabels` — 列出文件的标签。更多信息，请参阅 [列出文件的标签](https://developers.google.com/workspace/drive/api/guides/list-labels)。
  - `modifyLabels` — 修改应用于文件的标签集。更多信息，请参阅 [为文件设置标签](https://developers.google.com/workspace/drive/api/guides/set-label)。返回添加或修改的标签列表。
  - `update` — 更新文件的元数据或内容。调用此方法时，只需填写您想要修改的字段。在更新字段时，某些字段可能会自动更改，例如 `modifiedDate`。此方法支持补丁语义。此方法支持 `*/upload*` URI，并接受具有以下特性的上传媒体：  
    - **最大文件大小：** 5,120 GB  
    - **接受的媒体 MIME 类型：** `*/*`（请指定有效的 MIME 类型，而不是字面值 `*/*`）。
  - `watch` — 订阅文件的更改通知。更多信息，请参阅 [资源更改通知](https://developers.google.com/workspace/drive/api/guides/push)。

### operations

  - `get` — 获取长时间运行的操作的最新状态。客户端可以根据 API 服务的建议定期轮询操作结果。

### permissions

  - `create` — 为文件或共享 Drive 创建权限。更多信息，请参阅 [共享文件、文件夹和 Drive](https://developers.google.com/workspace/drive/api/guides/manage-sharing)。**警告：** 不支持对同一文件同时进行权限操作；只应用最后一次更新。
  - `delete` — 删除权限。更多信息，请参阅 [共享文件、文件夹和 Drive](https://developers.google.com/workspace/drive/api/guides/manage-sharing)。**警告：** 不支持对同一文件同时进行权限操作；只应用最后一次更新。
  - `get` — 通过 ID 获取权限信息。更多信息，请参阅 [共享文件、文件夹和 Drive](https://developers.google.com/workspace/drive/api/guides/manage-sharing)。
  - `list` — 列出文件或共享 Drive 的权限。更多信息，请参阅 [共享文件、文件夹和 Drive](https://developers.google.com/workspace/drive/api/guides/manage-sharing)。
  - `update` — 使用补丁语义更新权限。更多信息，请参阅 [共享文件、文件夹和 Drive](https://developers.google.com/workspace/drive/api/guides/manage-sharing)。**警告：** 不支持对同一文件同时进行权限操作；只应用最后一次更新。

### replies

  - `create` — 创建对评论的回复。更多信息，请参阅 [管理评论和回复](https://developers.google.com/workspace/drive/api/guides/manage-comments)。
  - `delete` — 删除回复。更多信息，请参阅 [管理评论和回复](https://developers.google.com/workspace/drive/api/guides/manage-comments)。
  - `get` — 通过 ID 获取回复信息。更多信息，请参阅 [管理评论和回复](https://developers.google.com/workspace/drive/api/guides/manage-comments)。
  - `list` — 列出评论的回复。更多信息，请参阅 [管理评论和回复](https://developers.google.com/workspace/drive/api/guides/manage-comments)。
  - `update` — 使用补丁语义更新回复。更多信息，请参阅 [管理评论和回复](https://developers.google.com/workspace/drive/api/guides/manage-comments)。

### revisions

  - `delete` — 永久删除文件版本。您只能删除 Google Drive 中包含二进制内容（如图片或视频）的文件的版本。其他文件（如 Google Docs 或 Sheets）的版本无法删除。更多信息，请参阅 [管理文件版本](https://developers.google.com/workspace/drive/api/guides/manage-revisions)。
  - `get` — 通过 ID 获取版本的元数据或内容。更多信息，请参阅 [管理文件版本](https://developers.google.com/workspace/drive/api/guides/manage-revisions)。
  - `list` — 列出文件的版本。更多信息，请参阅 [管理文件版本](https://developers.google.com/workspace/drive/api/guides/manage-revisions)。**注意：** 对于具有大量版本历史的文件（如经常编辑的 Google Docs、Sheets 和 Slides），此方法返回的版本列表可能不完整。较旧的版本可能会从响应中省略，因此返回的第一个版本可能不是最旧的版本。
  - `update` — 使用补丁语义更新版本。更多信息，请参阅 [管理文件版本](https://developers.google.com/workspace/drive/api/guides/manage-revisions)。

### teamdrives

  - `create` — 已弃用：请使用 `drives.create` 代替。
  - `get` — 已弃用：请使用 `drives.get` 代替。
  - `list` — 已弃用：请使用 `drives.list` 代替。
  - `update` — 已弃用：请使用 `drives.update` 代替。

## 发现命令

在调用任何 API 方法之前，请先检查其文档：

```bash
# Browse resources and methods
gws drive --help

# Inspect a method's required params, types, and defaults
gws schema drive.<resource>.<method>
```

使用 `gws schema` 的输出来构建您的 `--params` 和 `--json` 参数。