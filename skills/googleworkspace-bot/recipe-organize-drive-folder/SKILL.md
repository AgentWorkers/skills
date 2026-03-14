---
name: recipe-organize-drive-folder
version: 1.0.0
description: "创建一个 Google Drive 文件夹结构，并将文件移动到正确的位置。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-drive"]
---
# 将文件组织到 Google Drive 文件夹中

> **先决条件：** 需要加载以下技能才能执行此操作：`gws-drive`

创建一个 Google Drive 文件夹结构，并将文件移动到相应的位置。

## 步骤

1. 创建一个项目文件夹：`gws drive files create --json '{"name": "Q2 Project", "mimeType": "application/vnd.google-apps.folder"}'`
2. 创建子文件夹：`gws drive files create --json '{"name": "Documents", "mimeType": "application/vnd.google-apps.folder", "parents": ["PARENT_FOLDER_ID"]}'`
3. 将现有文件移动到文件夹中：`gws drive files update --params '{"fileId": "FILE_ID", "addParents": "FOLDER_ID", "removeParents": "OLD_PARENT_ID"}'`
4. 验证文件夹结构：`gws drive files list --params '{"q": "FOLDER_ID in parents"}' --format table`