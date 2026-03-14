---
name: recipe-create-shared-drive
version: 1.0.0
description: "创建一个 Google 共享文件夹（Google Shared Drive），并为其添加具有相应角色的成员。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-drive"]
---
# 创建并配置共享驱动器

> **前提条件：** 需要加载以下技能才能执行此操作：`gws-drive`

创建一个 Google 共享驱动器，并为成员分配相应的角色。

## 步骤

1. 创建共享驱动器：`gws drive drives create --params '{"requestId": "unique-id-123"}' --json '{"name": "Project X"}'`
2. 添加成员：`gws drive permissions create --params '{"fileId": "DRIVE_ID", "supportsAllDrives": true}' --json '{"role": "writer", "type": "user", "emailAddress": "member@company.com"}'`
3. 列出成员：`gws drive permissions list --params '{"fileId": "DRIVE_ID", "supportsAllDrives": true}'`