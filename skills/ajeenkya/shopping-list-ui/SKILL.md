---
name: shopping-list-ui
version: 1.0.0
description: >
  **购物清单功能的Web UI**  
  该Web UI为“Second Brain”平台添加了一个“/shopping”页面，支持完整的CRUD（创建、读取、更新、删除）操作：可以查看、添加、编辑、勾选和删除购物清单中的商品。使用此功能前，必须先安装“购物清单功能”（该功能与“Second Brain”共享相同的数据文件）。
---
# 购物清单UI

这是一个用于管理购物清单的Web界面。它为Second Brain门户添加了一个 `/shopping` 页面，支持分类列表视图和内联编辑功能。

## 先决条件

- Second Brain门户已运行（使用Next.js框架）
- `shopping-list` 技能已安装（通过 `clawhub install shopping-list` 命令安装）

## 文件结构

该技能为Second Brain应用程序添加了以下文件：

| 文件 | 用途 |
|------|---------|
| `second-brain/src/lib/shopping.ts` | 数据层代码——负责读取/写入购物清单相关的JSON文件 |
| `second-brain/src/app/api/shopping/route.ts` | 处理获取购物清单列表（GET请求）以及添加商品（POST请求）的逻辑 |
| `second-brain/src/app/api/shopping/[id]/route.ts` | 处理编辑商品（PUT请求）、删除商品（DELETE请求）以及标记商品为已购买（PATCH请求）的逻辑 |
| `second-brain/src/app/shopping/page.tsx` | 购物清单页面，包含CRUD（创建、读取、更新、删除）用户界面 |

同时修改了以下文件：
- `second-brain/src/components/Sidebar.tsx` — 在侧边栏中添加了购物清单的导航入口 |
- `second-brain/src/components/SFIcon.tsx` — 添加了表示购物车状态的图标

## 数据存储

该功能会读取和写入 `skills/shopping-list/data/active.json` 文件（该文件也被用于对话式购物清单CLI功能）。用户在Web界面中所做的任何更改会立即反映在聊天界面中，反之亦然。

`addedBy` 字段用于记录商品的添加者身份，其值从 `skills/shopping-list/data/config.json` 文件中获取。如果未设置，默认值为 “web”。